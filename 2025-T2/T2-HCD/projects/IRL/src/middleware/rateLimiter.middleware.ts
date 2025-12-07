// src/middleware/rateLimiter.middleware.ts
// Phase 1.4: Rate limit middleware using Token Bucket algorithm
// Wraps endpoints with Token Bucket protection
// Returns 429 with Retry-After header when rate limit is exceeded

import { Request, Response, NextFunction } from 'express';
import redis from '../db/redis.js';
import { TOKEN_BUCKET_LUA } from '../core/rateLimiter/tokenBucket.js';
import logger from '../utils/logger.js';

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
  /** Function to extract identifier from request (default: IP address) */
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
  keyGenerator: (req: Request) => req.ip || req.socket.remoteAddress || 'unknown',
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
 * Helper to run the Token Bucket Lua script
 */
async function evalTokenBucket(
  key: string,
  capacity: number,
  rate: number,
  amount: number,
): Promise<{ allowed: boolean; remaining: number; retryAfterMs: number }> {
  const result = (await redis.eval(
    TOKEN_BUCKET_LUA,
    1,
    key,
    capacity,
    rate,
    amount,
    Date.now(),
  )) as [number, number, number];

  return {
    allowed: result[0] === 1,
    remaining: Math.floor(result[1]),
    retryAfterMs: result[2],
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

      // Always set rate limit headers
      const retryAfterSeconds = Math.ceil(retryAfterMs / 1000);
      res.set({
        'X-RateLimit-Limit': capacity.toString(),
        'X-RateLimit-Remaining': remaining.toString(),
        'X-RateLimit-Reset': Math.floor(Date.now() / 1000 + retryAfterSeconds).toString(),
      });

      if (!allowed) {
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
 * Creates an agent-based rate limiter that uses agentId from request body or params
 * Useful for API endpoints that identify clients by agent ID rather than IP
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
