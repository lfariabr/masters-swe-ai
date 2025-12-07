import request from 'supertest';
import { app, redis } from '../src/index';
import { waitForRedis } from '../src/db/redis';

describe('API Endpoints (Real App)', () => {
  beforeAll(async () => {
    // Wait for Redis to be fully connected before running tests
    await waitForRedis();
  });

  afterAll(async () => {
    // Clean up test keys only
    // Note: This test uses the shared Redis client from src/index.
    // The shared client is not closed here to avoid race conditions with other test suites.
    // Jest's forceExit handles cleanup of shared connections.
    const keys = await redis.keys('ratelimit:*');
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  });

  describe('GET /', () => {
    it('should return API info with correct structure', async () => {
      const response = await request(app).get('/');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('name', 'IRL - Intelligent Rate Limiter');
      expect(response.body).toHaveProperty('version', '0.1.0');
      expect(response.body).toHaveProperty('endpoints');
      expect(response.body.endpoints).toHaveProperty('health', '/health');
      expect(response.body.endpoints).toHaveProperty('testRedis', '/test-redis');
      expect(response.body.endpoints).toHaveProperty('testRateLimit', '/api/test-rate-limit');
    });
  });

  describe('GET /health', () => {
    it('should return health status with Redis connected', async () => {
      const response = await request(app).get('/health');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'ok');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('redis', 'connected');
    });

    it('should return valid ISO timestamp', async () => {
      const response = await request(app).get('/health');

      const timestamp = response.body.timestamp;
      const parsed = new Date(timestamp);

      expect(parsed.toISOString()).toBe(timestamp);
    });
  });

  describe('GET /test-redis', () => {
    it('should verify Redis connection and operations', async () => {
      const response = await request(app).get('/test-redis');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('message', 'Redis is working!');
      expect(response.body).toHaveProperty('testValue', 'Hello from IRL!');
      expect(response.body).toHaveProperty('redisVersion');
    });
  });

  describe('GET /api/test (Rate Limiting)', () => {
    beforeEach(async () => {
      // Clean up rate limit keys before each test
      const keys = await redis.keys('ratelimit:*');
      if (keys.length > 0) {
        await redis.del(...keys);
      }
    });

    it('should return success with rate limit headers', async () => {
      const response = await request(app).get('/api/test-rate-limit');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message', 'Request successful!');
      expect(response.body).toHaveProperty('requestNumber', 1);
      expect(response.body).toHaveProperty('remaining');
      expect(response.body).toHaveProperty('limit');

      // Verify rate limit headers exist and have valid values
      expect(response.headers).toHaveProperty('x-ratelimit-limit');
      expect(response.headers).toHaveProperty('x-ratelimit-remaining');
      expect(response.headers).toHaveProperty('x-ratelimit-reset');

      // Validate headers parse to proper numbers
      const limit = parseInt(response.headers['x-ratelimit-limit'], 10);
      const remaining = parseInt(response.headers['x-ratelimit-remaining'], 10);
      const reset = parseInt(response.headers['x-ratelimit-reset'], 10);

      expect(limit).toBeGreaterThan(0);
      expect(remaining).toBeGreaterThanOrEqual(0);
      expect(remaining).toBeLessThanOrEqual(limit);
      expect(reset).toBeGreaterThan(Math.floor(Date.now() / 1000));
    });

    it('should increment request count on subsequent requests', async () => {
      const response1 = await request(app).get('/api/test-rate-limit');
      const response2 = await request(app).get('/api/test-rate-limit');
      const response3 = await request(app).get('/api/test-rate-limit');

      expect(response1.body.requestNumber).toBe(1);
      expect(response2.body.requestNumber).toBe(2);
      expect(response3.body.requestNumber).toBe(3);

      // Remaining should decrease
      expect(response2.body.remaining).toBeLessThan(response1.body.remaining);
      expect(response3.body.remaining).toBeLessThan(response2.body.remaining);
    });

    it('should return 429 when rate limit is exceeded', async () => {
      // Set a very low rate limit for testing
      const originalLimit = process.env.DEFAULT_RATE_LIMIT;
      process.env.DEFAULT_RATE_LIMIT = '3';

      try {
        // Make requests up to and beyond the limit
        await request(app).get('/api/test-rate-limit'); // 1
        await request(app).get('/api/test-rate-limit'); // 2
        await request(app).get('/api/test-rate-limit'); // 3
        const blockedResponse = await request(app).get('/api/test-rate-limit'); // 4 - should be blocked

        expect(blockedResponse.status).toBe(429);
        expect(blockedResponse.body).toHaveProperty('error', 'Too Many Requests');
        expect(blockedResponse.body).toHaveProperty('retryAfter');
      } finally {
        // Restore original limit
        if (originalLimit) {
          process.env.DEFAULT_RATE_LIMIT = originalLimit;
        } else {
          delete process.env.DEFAULT_RATE_LIMIT;
        }
      }
    });
  });

  describe('404 Handling', () => {
    it('should return 404 for unknown routes', async () => {
      const response = await request(app).get('/unknown-route-that-does-not-exist');

      expect(response.status).toBe(404);
    });
  });
});
