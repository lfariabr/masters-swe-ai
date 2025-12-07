// src/middleware/rateLimiter.middleware.ts
// Phase 1.4: Rate limit middleware using Token Bucket algorithm
// Wraps endpoints with Token Bucket protection
// Returns 429 with Retry-After header when rate limit is exceeded
//
// IMPORTANT: For correct IP-based rate limiting behind proxies/load balancers,
// ensure Express is configured with: app.set('trust proxy', true)
// or the appropriate value for your deployment (e.g., 'loopback', number of hops).
// See: https://expressjs.com/en/guide/behind-proxies.html

import { Request, Response, NextFunction } from 'express';
import crypto from 'crypto';
import redis from '../db/redis.js';
import { TOKEN_BUCKET_LUA } from '../core/rateLimiter/tokenBucket.js';
import logger from '../utils/logger.js';

/**
 * Extracts the client IP address with graceful fallback chain:
 * 1. req.ip (Express, requires 'trust proxy' setting for proxied requests)
 * 2. X-Forwarded-For header (leftmost IP, the original client)
 * 3. req.socket.remoteAddress (direct connection)
 * 4. Fingerprint based on User-Agent + Accept-Language (stable fallback)
 *
 * This prevents shared rate buckets from the literal 'unknown' fallback.
 */
function extractClientIdentifier(req: Request): string {
  // 1. Express req.ip (respects 'trust proxy' setting)
  if (req.ip && req.ip !== '::1' && req.ip !== '127.0.0.1') {
    return req.ip;
  }

  // 2. X-Forwarded-For header (take leftmost/original client IP)
  const xForwardedFor = req.headers['x-forwarded-for'];
  if (xForwardedFor) {
    const forwardedIps = Array.isArray(xForwardedFor)
      ? xForwardedFor[0]
      : xForwardedFor.split(',')[0];
    const clientIp = forwardedIps?.trim();
    if (clientIp) {
      return clientIp;
    }
  }

  // 3. Direct socket connection
  if (req.socket?.remoteAddress) {
    return req.socket.remoteAddress;
  }

  // 4. Fingerprint fallback: hash of User-Agent + Accept-Language
  // This provides a stable identifier when IP cannot be determined
  const userAgent = req.headers['user-agent'] || '';
  const acceptLanguage = req.headers['accept-language'] || '';
  const fingerprint = crypto
    .createHash('sha256')
    .update(`${userAgent}:${acceptLanguage}`)
    .digest('hex')
    .substring(0, 16);

  return `fingerprint:${fingerprint}`;
}

// Configuration interface for the middleware
export interface RateLimitConfig {
  /** Maximum tokens in the bucket (default: 100) */
  capacity?: number;
  /** Tokens added per second (default: 10) */
  rate?: number;
  /** Number of tokens to consume per request (default: 1) */
  tokensPerRequest?: number;
  /** Key prefix for Redis (default: 'ratelimit:middleware') */
  keyPrefix?: string;
  /** Function to extract identifier from request (default: IP address with fallbacks) */
  keyGenerator?: (req: Request) => string;
  /** Skip rate limiting for certain requests */
  skip?: (req: Request) => boolean;
  /** Custom handler when rate limit is exceeded */
  handler?: (req: Request, res: Response, next: NextFunction, retryAfterMs: number) => void;
}

// Default configuration
const defaultConfig: Required<RateLimitConfig> = {
  capacity: parseInt(process.env.RATE_LIMIT_CAPACITY || '100', 10),
  rate: parseFloat(process.env.RATE_LIMIT_RATE || '10'),
  tokensPerRequest: 1,
  keyPrefix: 'ratelimit:middleware',
  keyGenerator: extractClientIdentifier,
  skip: () => false,
  handler: (_req, res, _next, retryAfterMs) => {
    const retryAfterSeconds = Math.ceil(retryAfterMs / 1000);
    res.status(429).json({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded. Please try again later.',
      retryAfter: retryAfterSeconds,
    });
  },
};

/**
 * Helper to run the Token Bucket Lua script.
 * Performs defensive validation of the Lua script result.
 *
 * @throws Error if TOKEN_BUCKET_LUA returns unexpected data format
 */
async function evalTokenBucket(
  key: string,
  capacity: number,
  rate: number,
  amount: number,
): Promise<{ allowed: boolean; remaining: number; retryAfterMs: number }> {
  const result = await redis.eval(
    TOKEN_BUCKET_LUA,
    1,
    key,
    capacity,
    rate,
    amount,
    Date.now(),
  );

  // Defensive validation: TOKEN_BUCKET_LUA should return [allowed, remaining, retryAfterMs]
  if (!Array.isArray(result) || result.length !== 3) {
    throw new Error(
      `TOKEN_BUCKET_LUA returned invalid result: expected [allowed, remaining, retryAfterMs] ` +
        `as array of length 3, got ${JSON.stringify(result)}`,
    );
  }

  // Coerce and validate each value
  const allowed = Number(result[0]);
  const remaining = Number(result[1]);
  const retryAfterMs = Number(result[2]);

  if (!Number.isFinite(allowed) || !Number.isFinite(remaining) || !Number.isFinite(retryAfterMs)) {
    throw new Error(
      `TOKEN_BUCKET_LUA returned non-numeric values: expected [allowed (0|1), remaining, retryAfterMs] ` +
        `as finite numbers, got [${result[0]}, ${result[1]}, ${result[2]}]`,
    );
  }

  return {
    allowed: allowed === 1,
    remaining: Math.floor(remaining),
    retryAfterMs,
  };
}

/**
 * Creates a rate limiting middleware using the Token Bucket algorithm
 *
 * @example
 * // Basic usage - apply to all routes
 * app.use(rateLimiter());
 *
 * @example
 * // Custom configuration
 * app.use(rateLimiter({
 *   capacity: 50,
 *   rate: 5,
 *   keyGenerator: (req) => req.headers['x-api-key'] as string || req.ip,
 * }));
 *
 * @example
 * // Apply to specific routes
 * app.use('/api/expensive', rateLimiter({ capacity: 10, rate: 1 }));
 */
export function rateLimiter(config: RateLimitConfig = {}) {
  const {
    capacity,
    rate,
    tokensPerRequest,
    keyPrefix,
    keyGenerator,
    skip,
    handler,
  } = { ...defaultConfig, ...config };

  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    // Skip rate limiting if configured to do so
    if (skip(req)) {
      next();
      return;
    }

    try {
      const identifier = keyGenerator(req);
      const key = `${keyPrefix}:${identifier}`;

      const { allowed, remaining, retryAfterMs } = await evalTokenBucket(
        key,
        capacity,
        rate,
        tokensPerRequest,
      );

      // Compute X-RateLimit-Reset: timestamp when at least 1 token will be available
      // - If tokens are available now (remaining > 0), reset is now
      // - If bucket is empty, compute when tokensPerRequest tokens will refill
      // - For zero-rate buckets, omit X-RateLimit-Reset (tokens never refill)
      const nowSeconds = Math.floor(Date.now() / 1000);
      let resetTimestamp: number | null = null;

      if (remaining >= tokensPerRequest) {
        // Enough tokens for next request - reset is now
        resetTimestamp = nowSeconds;
      } else if (rate > 0) {
        // Compute seconds until enough tokens for next request
        const neededTokens = tokensPerRequest - remaining;
        const secondsUntilReady = Math.ceil(neededTokens / rate);
        resetTimestamp = nowSeconds + secondsUntilReady;
      }
      // For rate === 0, don't set X-RateLimit-Reset (tokens never refill)

      // Set rate limit headers
      const headers: Record<string, string> = {
        'X-RateLimit-Limit': capacity.toString(),
        'X-RateLimit-Remaining': remaining.toString(),
      };

      if (resetTimestamp !== null) {
        headers['X-RateLimit-Reset'] = resetTimestamp.toString();
      }

      res.set(headers);

      if (!allowed) {
        const retryAfterSeconds = Math.ceil(retryAfterMs / 1000);
        res.set('Retry-After', retryAfterSeconds.toString());

        logger.info('Rate limit exceeded (middleware)', {
          identifier,
          path: req.path,
          method: req.method,
          remaining,
          retryAfterMs,
        });

        handler(req, res, next, retryAfterMs);
        return;
      }

      logger.debug('Request allowed (middleware)', {
        identifier,
        path: req.path,
        remaining,
      });

      next();
    } catch (error) {
      // If Redis fails, we can either:
      // 1. Fail open (allow request) - better for availability
      // 2. Fail closed (deny request) - better for security
      // Here we fail open to maintain availability
      logger.error('Rate limiter error - failing open', {
        error,
        path: req.path,
      });
      next();
    }
  };
}

/**
 * Creates an agent-based rate limiter that uses agentId from request body or params.
 * Useful for API endpoints that identify clients by agent ID rather than IP.
 *
 * **Agent ID extraction precedence** (used by keyGenerator for rate limiting):
 * 1. `req.body.agentId` - Request body (requires body-parser middleware)
 * 2. `req.params.agentId` - URL route parameters (e.g., `/api/:agentId`)
 * 3. `req.headers['x-agent-id']` - Custom header `x-agent-id`
 * 4. `req.query.agentId` - Query string parameter (e.g., `?agentId=xxx`)
 *
 * If none of the above are present, falls back to:
 * - `req.ip` (Express IP, respects 'trust proxy' setting)
 * - `req.socket.remoteAddress` (direct socket connection)
 * - `'unknown'` (last resort fallback)
 *
 * The resolved agentId is cast to `String()` before use as the rate limit key.
 *
 * @param config - Rate limiter configuration (keyGenerator is overridden)
 * @returns Express middleware function
 *
 * @example
 * // Rate limit by agentId in request body
 * app.post('/api/action', express.json(), agentRateLimiter({ capacity: 10 }), handler);
 *
 * @example
 * // Rate limit by agentId in URL params
 * app.get('/api/agent/:agentId/status', agentRateLimiter(), handler);
 *
 * @example
 * // Rate limit by x-agent-id header
 * // Client sends: { headers: { 'x-agent-id': 'agent-123' } }
 * app.use('/api', agentRateLimiter({ capacity: 50, rate: 5 }));
 */
export function agentRateLimiter(config: Omit<RateLimitConfig, 'keyGenerator'> = {}) {
  return rateLimiter({
    ...config,
    keyPrefix: config.keyPrefix || 'ratelimit:agent',
    keyGenerator: (req: Request) => {
      // Try to get agentId from various sources
      const agentId =
        req.body?.agentId ||
        req.params?.agentId ||
        req.headers['x-agent-id'] ||
        req.query?.agentId;

      if (!agentId) {
        // Fall back to IP if no agentId provided
        return req.ip || req.socket.remoteAddress || 'unknown';
      }

      return String(agentId);
    },
  });
}

export default rateLimiter;
