// tests/tokenBucketRedis.test.ts
// Integration tests for TOKEN_BUCKET_LUA with real Redis

import Redis from 'ioredis';
import { TOKEN_BUCKET_LUA } from '../src/core/rateLimiter/tokenBucket';

describe('TokenBucket Lua Script (Redis Integration)', () => {
  let redis: Redis;
  const TEST_KEY = 'test:tokenbucket:lua';

  beforeAll(() => {
    redis = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT || '6379', 10),
      password: process.env.REDIS_PASSWORD,
      db: parseInt(process.env.REDIS_DB || '0', 10),
      maxRetriesPerRequest: 3,
      connectTimeout: 5000,
    });
  });

  beforeEach(async () => {
    await redis.del(TEST_KEY);
  });

  afterAll(async () => {
    // Clean up test key
    await redis.del(TEST_KEY);
    // Close the test-specific Redis connection
    if (redis && redis.status !== 'end') {
      await redis.quit();
    }
  });

  /**
   * Helper to run the Lua script
   * @returns [allowed (0|1), remaining, retryAfterMs]
   */
  async function evalTokenBucket(
    key: string,
    capacity: number,
    rate: number,
    amount: number,
    nowMs: number = Date.now(),
  ): Promise<[number, number, number]> {
    const result = await redis.eval(
      TOKEN_BUCKET_LUA,
      1,
      key,
      capacity,
      rate,
      amount,
      nowMs,
    );
    return result as [number, number, number];
  }

  describe('Basic consumption', () => {
    it('should allow request from new bucket (full capacity)', async () => {
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 1, 1);
      expect(allowed).toBe(1);
      expect(remaining).toBe(9);
    });

    it('should consume multiple tokens', async () => {
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 1, 5);
      expect(allowed).toBe(1);
      expect(remaining).toBe(5);
    });

    it('should reject when requesting more than capacity', async () => {
      const [allowed, remaining, retryAfterMs] = await evalTokenBucket(TEST_KEY, 10, 1, 15);
      expect(allowed).toBe(0);
      expect(remaining).toBe(10); // full bucket, still can't satisfy 15
      expect(retryAfterMs).toBeGreaterThan(0);
    });

    it('should track consumption across multiple calls', async () => {
      await evalTokenBucket(TEST_KEY, 10, 0, 3); // consume 3
      await evalTokenBucket(TEST_KEY, 10, 0, 3); // consume 3
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 0, 3); // consume 3
      expect(allowed).toBe(1);
      expect(remaining).toBe(1);

      // Next request should fail (only 1 left, need 3)
      const [allowed2, remaining2] = await evalTokenBucket(TEST_KEY, 10, 0, 3);
      expect(allowed2).toBe(0);
      expect(remaining2).toBe(1);
    });
  });

  describe('Refill behavior', () => {
    it('should refill tokens over time', async () => {
      const now = Date.now();

      // Consume all tokens
      await evalTokenBucket(TEST_KEY, 10, 10, 10, now); // empty bucket, rate=10/s

      // 500ms later: should have ~5 tokens
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 10, 4, now + 500);
      expect(allowed).toBe(1);
      expect(remaining).toBeCloseTo(1, 0); // 5 refilled - 4 consumed ≈ 1
    });

    it('should not exceed capacity on refill', async () => {
      const now = Date.now();

      // Start with bucket at 5 tokens
      await evalTokenBucket(TEST_KEY, 10, 100, 5, now); // consume 5, left with 5

      // 1 second later at rate=100/s would add 100, but cap at 10
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 100, 1, now + 1000);
      expect(allowed).toBe(1);
      expect(remaining).toBe(9); // capped at 10, consumed 1
    });

    it('should not refill when clock goes backward (clock-skew)', async () => {
      const now = Date.now();

      // First request at time T
      await evalTokenBucket(TEST_KEY, 10, 10, 5, now); // 5 left

      // Request at T-1000 (clock went backward) - should NOT add tokens
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 10, 5, now - 1000);
      expect(allowed).toBe(1);
      expect(remaining).toBe(0); // no refill, consumed remaining 5
    });
  });

  describe('Zero-rate bucket (one-shot)', () => {
    it('should never refill when rate is 0', async () => {
      const now = Date.now();

      // Consume some tokens
      await evalTokenBucket(TEST_KEY, 10, 0, 8, now);

      // Much later - still no refill
      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 0, 3, now + 60000);
      expect(allowed).toBe(0);
      expect(remaining).toBe(2);
    });

    it('should return -1 for retryAfterMs when rate is 0 and blocked', async () => {
      const now = Date.now();

      // Empty the bucket
      await evalTokenBucket(TEST_KEY, 5, 0, 5, now);

      // Try to consume more
      const [allowed, , retryAfterMs] = await evalTokenBucket(TEST_KEY, 5, 0, 1, now + 1000);
      expect(allowed).toBe(0);
      expect(retryAfterMs).toBe(-1); // sentinel for Infinity
    });
  });

  describe('Corrupt data handling', () => {
    it('should reinitialize on corrupt JSON', async () => {
      await redis.set(TEST_KEY, 'not valid json');

      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 1, 1);
      expect(allowed).toBe(1);
      expect(remaining).toBe(9); // reinitialized to full capacity
    });

    it('should reinitialize on malformed array', async () => {
      await redis.set(TEST_KEY, '[1,2]'); // too short

      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 1, 1);
      expect(allowed).toBe(1);
      expect(remaining).toBe(9);
    });

    it('should reinitialize on wrong types in array', async () => {
      await redis.set(TEST_KEY, '[10,"bad",5,1700000000000]');

      const [allowed, remaining] = await evalTokenBucket(TEST_KEY, 10, 1, 1);
      expect(allowed).toBe(1);
      expect(remaining).toBe(9);
    });
  });

  describe('TTL behavior', () => {
    it('should set TTL on the key', async () => {
      await evalTokenBucket(TEST_KEY, 100, 10, 1); // TTL = ceil(100/10) + 60 = 70

      const ttl = await redis.ttl(TEST_KEY);
      expect(ttl).toBeGreaterThan(0);
      expect(ttl).toBeLessThanOrEqual(70);
    });

    it('should use fallback TTL when rate is 0', async () => {
      await evalTokenBucket(TEST_KEY, 100, 0, 1); // TTL = 60 (fallback)

      const ttl = await redis.ttl(TEST_KEY);
      expect(ttl).toBeGreaterThan(0);
      expect(ttl).toBeLessThanOrEqual(60);
    });
  });

  describe('Retry-After calculation', () => {
    it('should return correct retryAfterMs', async () => {
      const now = Date.now();

      // Empty the bucket
      await evalTokenBucket(TEST_KEY, 10, 2, 10, now); // rate=2/s, 0 left

      // Need 1 token at rate 2/s → 0.5s → 500ms (ceil)
      const [allowed, , retryAfterMs] = await evalTokenBucket(TEST_KEY, 10, 2, 1, now);
      expect(allowed).toBe(0);
      expect(retryAfterMs).toBe(500);
    });

    it('should return 0 when request succeeds', async () => {
      const [allowed, , retryAfterMs] = await evalTokenBucket(TEST_KEY, 10, 1, 1);
      expect(allowed).toBe(1);
      expect(retryAfterMs).toBe(0);
    });
  });
});
