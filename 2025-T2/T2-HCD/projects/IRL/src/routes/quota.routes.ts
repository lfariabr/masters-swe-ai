// src/routes/quota.routes.ts
// Phase 1.3: REST API endpoints for rate limiting
// POST /api/request - Request access (consumes token)
// GET /api/quota/:agentId - Check remaining quota

import { Router, Request, Response } from 'express';
import redis from '../db/redis.js';
import { TOKEN_BUCKET_LUA } from '../core/rateLimiter/tokenBucket.js';
import logger from '../utils/logger.js';

const router = Router();

// Safe defaults
const SAFE_DEFAULT_CAPACITY = 100;
const SAFE_DEFAULT_RATE = 10;
const MAX_CAPACITY = 10000; // Sensible upper bound to prevent misconfiguration

/**
 * Safely parse and validate environment configuration.
 * Falls back to safe defaults if values are missing, invalid, or out of range.
 */
function parseEnvConfig(): { capacity: number; rate: number } {
  // Parse capacity: must be a positive integer
  const capacityEnv = process.env.TOKEN_BUCKET_CAPACITY?.trim();
  let capacity = SAFE_DEFAULT_CAPACITY;
  if (capacityEnv && capacityEnv !== '') {
    const parsed = parseInt(capacityEnv, 10);
    if (Number.isFinite(parsed) && parsed > 0 && Number.isInteger(parsed)) {
      capacity = Math.min(parsed, MAX_CAPACITY); // Clamp to sensible max
    }
  }

  // Parse rate: must be a positive number
  const rateEnv = process.env.TOKEN_BUCKET_RATE?.trim();
  let rate = SAFE_DEFAULT_RATE;
  if (rateEnv && rateEnv !== '') {
    const parsed = parseFloat(rateEnv);
    if (Number.isFinite(parsed) && parsed > 0) {
      rate = parsed;
    }
  }

  return { capacity, rate };
}

// Default configuration (validated from env vars with safe fallbacks)
const { capacity: DEFAULT_CAPACITY, rate: DEFAULT_RATE } = parseEnvConfig();

/**
 * Helper to run the Token Bucket Lua script
 * @returns [allowed (0|1), remaining, retryAfterMs]
 */
async function evalTokenBucket(
  key: string,
  capacity: number,
  rate: number,
  amount: number,
  nowMs: number = Date.now(),
): Promise<{ allowed: boolean; remaining: number; retryAfterMs: number }> {
  const result = (await redis.eval(
    TOKEN_BUCKET_LUA,
    1,
    key,
    capacity,
    rate,
    amount,
    nowMs,
  )) as [number, number, number];

  return {
    allowed: result[0] === 1,
    remaining: Math.floor(result[1]), // Floor for cleaner API response
    retryAfterMs: result[2],
  };
}

/**
 * POST /api/request
 * Request access (consumes tokens from the bucket)
 *
 * Body:
 *   - agentId: string (required) - Unique identifier for the agent/client
 *   - tokens: number (optional, default: 1) - Number of tokens to consume
 *
 * Response:
 *   - 200: Access granted
 *   - 429: Rate limit exceeded (includes Retry-After header)
 *   - 400: Invalid request
 */
router.post('/request', async (req: Request, res: Response) => {
  try {
    const { agentId, tokens = 1 } = req.body;

    // Validate agentId
    if (!agentId || typeof agentId !== 'string') {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'agentId is required and must be a string',
      });
    }

    // Validate tokens
    const tokensToConsume = Number(tokens);
    if (isNaN(tokensToConsume) || tokensToConsume < 1) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'tokens must be a positive number',
      });
    }

    const key = `ratelimit:agent:${agentId}`;
    const { allowed, remaining, retryAfterMs } = await evalTokenBucket(
      key,
      DEFAULT_CAPACITY,
      DEFAULT_RATE,
      tokensToConsume,
    );

    // Set standard rate limit headers
    const retryAfterSeconds = Math.ceil(retryAfterMs / 1000);
    res.set({
      'X-RateLimit-Limit': DEFAULT_CAPACITY.toString(),
      'X-RateLimit-Remaining': remaining.toString(),
      'X-RateLimit-Reset': Math.floor(Date.now() / 1000 + retryAfterSeconds).toString(),
    });

    if (!allowed) {
      res.set('Retry-After', retryAfterSeconds.toString());

      logger.info('Rate limit exceeded', {
        agentId,
        tokensRequested: tokensToConsume,
        remaining,
        retryAfterMs,
      });

      return res.status(429).json({
        error: 'Too Many Requests',
        message: 'Rate limit exceeded. Please try again later.',
        retryAfter: retryAfterSeconds,
        remaining,
      });
    }

    logger.debug('Request allowed', {
      agentId,
      tokensConsumed: tokensToConsume,
      remaining,
    });

    return res.status(200).json({
      success: true,
      message: 'Request allowed',
      tokensConsumed: tokensToConsume,
      remaining,
      limit: DEFAULT_CAPACITY,
    });
  } catch (error) {
    logger.error('Error processing request', { error });
    return res.status(500).json({
      error: 'Internal Server Error',
      message: 'An unexpected error occurred',
    });
  }
});

/**
 * GET /api/quota/:agentId
 * Check remaining quota for an agent (does NOT consume tokens)
 *
 * Response:
 *   - 200: Quota information
 *   - 400: Invalid agentId
 */
router.get('/quota/:agentId', async (req: Request, res: Response) => {
  try {
    const { agentId } = req.params;

    // Validate agentId
    if (!agentId || typeof agentId !== 'string') {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'agentId is required',
      });
    }

    const key = `ratelimit:agent:${agentId}`;

    // Check if bucket exists
    const data = await redis.get(key);

    if (!data) {
      // No bucket exists yet = full quota available
      return res.status(200).json({
        agentId,
        remaining: DEFAULT_CAPACITY,
        limit: DEFAULT_CAPACITY,
        rate: DEFAULT_RATE,
        status: 'new',
        message: 'No requests made yet. Full quota available.',
      });
    }

    // Parse existing bucket data
    try {
        const parsed = JSON.parse(data);
        if (!Array.isArray(parsed) || parsed.length < 4 || 
            parsed.some(v => typeof v !== 'number')) {
            throw new Error('Invalid bucket format');
            }
      const [capacity, rate, tokens, lastRefill] = parsed;

      // Calculate current tokens with refill
      const now = Date.now();
      const elapsed = Math.max(0, (now - lastRefill) / 1000);
      const currentTokens = Math.min(capacity, tokens + elapsed * rate);

      return res.status(200).json({
        agentId,
        remaining: Math.floor(currentTokens),
        limit: capacity,
        rate,
        status: 'active',
        lastActivity: new Date(lastRefill).toISOString(),
      });
    } catch {
      // Corrupted data - treat as new bucket
      return res.status(200).json({
        agentId,
        remaining: DEFAULT_CAPACITY,
        limit: DEFAULT_CAPACITY,
        rate: DEFAULT_RATE,
        status: 'reset',
        message: 'Bucket data was corrupted. Reset to full quota.',
      });
    }
  } catch (error) {
    logger.error('Error checking quota', { error });
    return res.status(500).json({
      error: 'Internal Server Error',
      message: 'An unexpected error occurred',
    });
  }
});

export default router;
