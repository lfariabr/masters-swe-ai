import Redis from 'ioredis';

// Environment variables are loaded in setup.ts

describe('Redis Connection', () => {
  let redis: Redis;

  beforeAll(() => {
    // Create a test Redis connection using environment variables
    redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT || '6379', 10),
      password: process.env.REDIS_PASSWORD,
      db: parseInt(process.env.REDIS_DB || '0', 10),
      maxRetriesPerRequest: 3,
      connectTimeout: 5000,
    });
  });

  afterAll(async () => {
    // Clean up test keys
    const keys = await redis.keys('test:*');
    if (keys.length > 0) {
      await redis.del(...keys);
    }
    // Close the test-specific Redis connection
    if (redis && redis.status !== 'end') {
      await redis.quit();
    }
  });

  describe('Basic Operations', () => {
    it('should connect and respond to PING', async () => {
      const result = await redis.ping();
      expect(result).toBe('PONG');
    });

    it('should SET and GET a value', async () => {
      const key = 'test:basic:setget';
      const value = 'Hello, IRL!';

      await redis.set(key, value);
      const result = await redis.get(key);

      expect(result).toBe(value);
    });

    it('should SET with expiration (TTL)', async () => {
      const key = 'test:basic:ttl';
      const value = 'expires soon';

      await redis.set(key, value, 'EX', 10); // 10 seconds TTL
      const ttl = await redis.ttl(key);

      expect(ttl).toBeGreaterThan(0);
      expect(ttl).toBeLessThanOrEqual(10);
    });

    it('should INCR a counter atomically', async () => {
      const key = 'test:basic:counter';

      // Reset the counter
      await redis.del(key);

      const first = await redis.incr(key);
      const second = await redis.incr(key);
      const third = await redis.incr(key);

      expect(first).toBe(1);
      expect(second).toBe(2);
      expect(third).toBe(3);
    });

    it('should DELETE a key', async () => {
      const key = 'test:basic:delete';

      await redis.set(key, 'to be deleted');
      const beforeDelete = await redis.exists(key);

      await redis.del(key);
      const afterDelete = await redis.exists(key);

      expect(beforeDelete).toBe(1);
      expect(afterDelete).toBe(0);
    });
  });

  describe('Rate Limiting Operations', () => {
    const RATE_LIMIT_SCRIPT = `
      local current = redis.call('INCR', KEYS[1])
      if current == 1 then
        redis.call('EXPIRE', KEYS[1], ARGV[1])
      end
      return current
    `;

    it('should execute Lua script for atomic rate limiting', async () => {
      const key = 'test:ratelimit:lua';
      await redis.del(key);

      // First request - should set expiry
      const first = (await redis.eval(RATE_LIMIT_SCRIPT, 1, key, 60)) as number;
      expect(first).toBe(1);

      // Second request - should increment without resetting expiry
      const second = (await redis.eval(RATE_LIMIT_SCRIPT, 1, key, 60)) as number;
      expect(second).toBe(2);

      // Check TTL was set correctly
      const ttl = await redis.ttl(key);
      expect(ttl).toBeGreaterThan(0);
      expect(ttl).toBeLessThanOrEqual(60);
    });

    it('should simulate rate limit scenario', async () => {
      const key = 'test:ratelimit:scenario';
      const limit = 5;
      await redis.del(key);

      const results: number[] = [];

      // Simulate 7 requests
      for (let i = 0; i < 7; i++) {
        const current = (await redis.eval(RATE_LIMIT_SCRIPT, 1, key, 60)) as number;
        results.push(current);
      }

      // First 5 should be under limit
      expect(results.slice(0, 5).every((r) => r <= limit)).toBe(true);

      // Last 2 should exceed limit
      expect(results[5]).toBe(6);
      expect(results[6]).toBe(7);
    });
  });

  describe('Error Handling', () => {
    it('should handle non-existent key gracefully', async () => {
      const result = await redis.get('test:nonexistent:key:12345');
      expect(result).toBeNull();
    });

    it('should return -2 for TTL on non-existent key', async () => {
      const ttl = await redis.ttl('test:nonexistent:key:67890');
      expect(ttl).toBe(-2); // -2 means key does not exist
    });
  });
});
