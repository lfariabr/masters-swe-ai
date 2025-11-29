// src/routes/testRateLimit.ts
import { Router, Request, Response } from 'express';
import redis from '../db/redis.js';
import { logRateLimit } from '../utils/logger.js';

const router = Router();

// Lua script for atomic rate limiting: INCR + conditional EXPIRE
const RATE_LIMIT_SCRIPT = `
  local current = redis.call('INCR', KEYS[1])
  if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
  end
  return current
`;

router.get('/test', async (req: Request, res: Response) => {
  const clientIP = req.ip || 'unknown';
  const key = `ratelimit:${clientIP}`;
  const windowSeconds = 60;

  try {
    const current = (await redis.eval(
      RATE_LIMIT_SCRIPT,
      1,
      key,
      windowSeconds,
    )) as number;

    const limit = parseInt(process.env.DEFAULT_RATE_LIMIT || '100', 10);
    const remaining = Math.max(0, limit - current);

    res.set({
      'X-RateLimit-Limit': limit.toString(),
      'X-RateLimit-Remaining': remaining.toString(),
      'X-RateLimit-Reset': (
        Math.floor(Date.now() / 1000) + windowSeconds
      ).toString(),
    });

        if (current > limit) {
            logRateLimit(clientIP, 'blocked', current, limit);
            return res.status(429).json({
                error: 'Too Many Requests',
                message: 'Rate limit exceeded. Please try again later.',
                retryAfter: windowSeconds,
            });
    }

    logRateLimit(clientIP, 'allowed', current, limit);
    return res.json({
      message: 'Request successful!',
      requestNumber: current,
      remaining,
      limit,
    });
  } catch (error) {
    return res.status(500).json({
      error: 'Internal Server Error',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

export default router;