// tests/rateLimiter.middleware.test.ts
// Tests for Phase 1.4: Rate limit middleware

import express, { Request, Response } from 'express';
import request from 'supertest';
import { rateLimiter, agentRateLimiter } from '../src/middleware/rateLimiter.middleware';
import redis from '../src/db/redis';
import { waitForRedis } from '../src/db/redis';

describe('Rate Limiter Middleware (Phase 1.4)', () => {
  const TEST_PREFIX = 'test:ratelimiter:middleware';

  beforeAll(async () => {
    await waitForRedis();
  });

  beforeEach(async () => {
    // Clean up test keys before each test
    const keys = await redis.keys(`${TEST_PREFIX}*`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  });

  afterAll(async () => {
    // Clean up test keys only
    // Note: This test uses the shared Redis client from src/db/redis.
    // The shared client is not closed here to avoid race conditions with other test suites.
    // Jest's forceExit handles cleanup of shared connections.
    const keys = await redis.keys(`${TEST_PREFIX}*`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * Basic functionality
   * ───────────────────────────────────────────────────────────────────────── */
  describe('Basic functionality', () => {
    it('should allow requests within rate limit', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 10,
          rate: 1,
          keyPrefix: TEST_PREFIX,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      const response = await request(app).get('/test');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
    });

    it('should include rate limit headers in response', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 50,
          rate: 5,
          keyPrefix: TEST_PREFIX,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      const response = await request(app).get('/test');

      expect(response.headers).toHaveProperty('x-ratelimit-limit', '50');
      expect(response.headers).toHaveProperty('x-ratelimit-remaining');
      expect(response.headers).toHaveProperty('x-ratelimit-reset');
    });

    it('should decrement remaining tokens on each request', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 10,
          rate: 0, // No refill for predictable testing
          keyPrefix: `${TEST_PREFIX}:decrement`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      const response1 = await request(app).get('/test');
      const remaining1 = parseInt(response1.headers['x-ratelimit-remaining'], 10);

      const response2 = await request(app).get('/test');
      const remaining2 = parseInt(response2.headers['x-ratelimit-remaining'], 10);

      expect(remaining2).toBe(remaining1 - 1);
    });

    it('should return 429 when rate limit is exceeded', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 2,
          rate: 0, // No refill
          keyPrefix: `${TEST_PREFIX}:exceed`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      // First two requests should succeed
      await request(app).get('/test');
      await request(app).get('/test');

      // Third request should be rate limited
      const response = await request(app).get('/test');

      expect(response.status).toBe(429);
      expect(response.body).toHaveProperty('error', 'Too Many Requests');
    });

    it('should include Retry-After header when rate limited', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 1,
          rate: 1, // 1 token per second
          keyPrefix: `${TEST_PREFIX}:retry`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      // Exhaust the bucket
      await request(app).get('/test');

      // This should be rate limited
      const response = await request(app).get('/test');

      expect(response.status).toBe(429);
      expect(response.headers).toHaveProperty('retry-after');
      const retryAfter = parseInt(response.headers['retry-after'], 10);
      expect(retryAfter).toBeGreaterThan(0);
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * Configuration options
   * ───────────────────────────────────────────────────────────────────────── */
  describe('Configuration options', () => {
    it('should use custom capacity', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 25,
          rate: 1,
          keyPrefix: `${TEST_PREFIX}:capacity`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      const response = await request(app).get('/test');

      expect(response.headers['x-ratelimit-limit']).toBe('25');
    });

    it('should use custom tokens per request', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 10,
          rate: 0,
          tokensPerRequest: 3,
          keyPrefix: `${TEST_PREFIX}:tokens`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      const response1 = await request(app).get('/test');
      const remaining1 = parseInt(response1.headers['x-ratelimit-remaining'], 10);

      expect(remaining1).toBe(7); // 10 - 3 = 7
    });

    it('should use custom key generator', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 10,
          rate: 0,
          keyPrefix: `${TEST_PREFIX}:keygen`,
          keyGenerator: (req) => req.headers['x-custom-id'] as string || 'default',
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      // Request with custom ID
      await request(app).get('/test').set('x-custom-id', 'user-123');

      // Verify the key was created with custom ID
      const keys = await redis.keys(`${TEST_PREFIX}:keygen:user-123`);
      expect(keys.length).toBe(1);
    });

    it('should skip rate limiting when skip function returns true', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 1,
          rate: 0,
          keyPrefix: `${TEST_PREFIX}:skip`,
          skip: (req) => req.headers['x-skip-ratelimit'] === 'true',
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      // First request exhausts bucket
      await request(app).get('/test');

      // Second request would be blocked
      const response1 = await request(app).get('/test');
      expect(response1.status).toBe(429);

      // But with skip header, it should pass
      const response2 = await request(app).get('/test').set('x-skip-ratelimit', 'true');
      expect(response2.status).toBe(200);
    });

    it('should use custom handler when rate limited', async () => {
      const app = express();
      app.use(
        rateLimiter({
          capacity: 1,
          rate: 0,
          keyPrefix: `${TEST_PREFIX}:handler`,
          handler: (_req, res, _next, retryAfterMs) => {
            res.status(503).json({
              customError: 'Service Temporarily Unavailable',
              waitTime: retryAfterMs,
            });
          },
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      // Exhaust bucket
      await request(app).get('/test');

      // Custom handler should be called
      const response = await request(app).get('/test');

      expect(response.status).toBe(503);
      expect(response.body).toHaveProperty('customError', 'Service Temporarily Unavailable');
      expect(response.body).toHaveProperty('waitTime');
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * Agent-based rate limiter
   * ───────────────────────────────────────────────────────────────────────── */
  describe('agentRateLimiter', () => {
    it('should use agentId from request body', async () => {
      const app = express();
      app.use(express.json());
      app.use(
        agentRateLimiter({
          capacity: 10,
          rate: 0,
          keyPrefix: `${TEST_PREFIX}:agent`,
        }),
      );
      app.post('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      await request(app).post('/test').send({ agentId: 'agent-body-123' });

      const keys = await redis.keys(`${TEST_PREFIX}:agent:agent-body-123`);
      expect(keys.length).toBe(1);
    });

    it('should use agentId from URL params', async () => {
      const app = express();
      const middleware = agentRateLimiter({
        capacity: 10,
        rate: 0,
        keyPrefix: `${TEST_PREFIX}:agent`,
      });
      // Apply middleware to specific route so params are available
      app.get('/test/:agentId', middleware, (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      await request(app).get('/test/agent-param-456');

      const keys = await redis.keys(`${TEST_PREFIX}:agent:agent-param-456`);
      expect(keys.length).toBe(1);
    });

    it('should use agentId from header', async () => {
      const app = express();
      app.use(
        agentRateLimiter({
          capacity: 10,
          rate: 0,
          keyPrefix: `${TEST_PREFIX}:agent`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      await request(app).get('/test').set('x-agent-id', 'agent-header-789');

      const keys = await redis.keys(`${TEST_PREFIX}:agent:agent-header-789`);
      expect(keys.length).toBe(1);
    });

    it('should fallback to IP when no agentId provided', async () => {
      const app = express();
      app.use(
        agentRateLimiter({
          capacity: 10,
          rate: 0,
          keyPrefix: `${TEST_PREFIX}:agent:fallback`,
        }),
      );
      app.get('/test', (_req: Request, res: Response) => {
        res.json({ success: true });
      });

      await request(app).get('/test');

      // Should have created a key (with IP or 'unknown')
      const keys = await redis.keys(`${TEST_PREFIX}:agent:fallback:*`);
      expect(keys.length).toBe(1);
    });
  });
});
