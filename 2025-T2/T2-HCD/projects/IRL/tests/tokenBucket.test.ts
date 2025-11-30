// tests/tokenBucket.test.ts
// Unit tests for Token Bucket algorithm (Phase 1.2, 1.5)

import {
  TokenBucket,
  createTokenBucket,
  refill,
  consume,
  retryAfter,
  serialize,
  deserialize,
  TOKEN_BUCKET_LUA,
} from '../src/core/rateLimiter/tokenBucket';

describe('TokenBucket', () => {
  /* ─────────────────────────────────────────────────────────────────────────
   * createTokenBucket
   * ───────────────────────────────────────────────────────────────────────── */
  describe('createTokenBucket', () => {
    it('should create a bucket with full capacity by default', () => {
      const bucket = createTokenBucket(10, 1);
      expect(bucket.capacity).toBe(10);
      expect(bucket.rate).toBe(1);
      expect(bucket.tokens).toBe(10);
      expect(bucket.lastRefill).toBeCloseTo(Date.now(), -2); // within ~100ms
    });

    it('should accept custom initial tokens', () => {
      const bucket = createTokenBucket(10, 1, 5);
      expect(bucket.tokens).toBe(5);
    });

    it('should clamp initial tokens to capacity', () => {
      const bucket = createTokenBucket(10, 1, 20);
      expect(bucket.tokens).toBe(10);
    });

    it('should clamp initial tokens to 0 minimum', () => {
      const bucket = createTokenBucket(10, 1, -5);
      expect(bucket.tokens).toBe(0);
    });

    it('should accept custom lastRefill timestamp', () => {
      const past = Date.now() - 5000;
      const bucket = createTokenBucket(10, 1, 5, past);
      expect(bucket.lastRefill).toBe(past);
    });

    it('should throw if capacity <= 0', () => {
      expect(() => createTokenBucket(0, 1)).toThrow('capacity must be positive');
      expect(() => createTokenBucket(-5, 1)).toThrow('capacity must be positive');
    });

    it('should throw if rate < 0', () => {
      expect(() => createTokenBucket(10, -1)).toThrow('rate cannot be negative');
    });

    it('should allow rate = 0 (one-shot bucket)', () => {
      const bucket = createTokenBucket(10, 0);
      expect(bucket.rate).toBe(0);
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * refill
   * ───────────────────────────────────────────────────────────────────────── */
  describe('refill', () => {
    it('should add tokens based on elapsed time', () => {
      const now = Date.now();
      const bucket = createTokenBucket(10, 2, 0, now - 1000); // 1 sec ago, rate=2/s
      refill(bucket, now);
      expect(bucket.tokens).toBeCloseTo(2, 1);
      expect(bucket.lastRefill).toBe(now);
    });

    it('should cap tokens at capacity', () => {
      const now = Date.now();
      const bucket = createTokenBucket(10, 100, 5, now - 1000); // would add 100 tokens
      refill(bucket, now);
      expect(bucket.tokens).toBe(10);
    });

    it('should not refill if now <= lastRefill (clock skew protection)', () => {
      const now = Date.now();
      const bucket = createTokenBucket(10, 2, 5, now);
      refill(bucket, now - 1000); // time went backwards
      expect(bucket.tokens).toBe(5);
      expect(bucket.lastRefill).toBe(now);
    });

    it('should handle fractional tokens', () => {
      const now = Date.now();
      const bucket = createTokenBucket(10, 1, 0, now - 500); // 0.5 seconds
      refill(bucket, now);
      expect(bucket.tokens).toBeCloseTo(0.5, 2);
    });

    it('should do nothing when rate is 0', () => {
      const now = Date.now();
      const bucket = createTokenBucket(10, 0, 5, now - 10000);
      refill(bucket, now);
      expect(bucket.tokens).toBe(5); // no change
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * consume
   * ───────────────────────────────────────────────────────────────────────── */
  describe('consume', () => {
    it('should consume tokens when available', () => {
      const bucket = createTokenBucket(10, 1, 5);
      const result = consume(bucket, 3);
      expect(result.allowed).toBe(true);
      expect(result.remaining).toBe(2);
      expect(bucket.tokens).toBe(2);
    });

    it('should reject when insufficient tokens', () => {
      const bucket = createTokenBucket(10, 1, 2);
      const result = consume(bucket, 5);
      expect(result.allowed).toBe(false);
      expect(result.remaining).toBe(2);
      expect(bucket.tokens).toBe(2); // unchanged
    });

    it('should consume exactly available tokens', () => {
      const bucket = createTokenBucket(10, 1, 5);
      const result = consume(bucket, 5);
      expect(result.allowed).toBe(true);
      expect(result.remaining).toBe(0);
    });

    it('should default to consuming 1 token', () => {
      const bucket = createTokenBucket(10, 1, 5);
      const result = consume(bucket);
      expect(result.allowed).toBe(true);
      expect(result.remaining).toBe(4);
    });

    it('should refill before consuming', () => {
      const now = Date.now();
      const bucket = createTokenBucket(10, 10, 0, now - 1000); // +10 tokens from refill
      const result = consume(bucket, 5);
      expect(result.allowed).toBe(true);
      expect(result.remaining).toBeCloseTo(5, 0);
    });

    it('should handle multiple sequential consumes', () => {
      const bucket = createTokenBucket(10, 0, 10); // no refill
      expect(consume(bucket, 3).remaining).toBe(7);
      expect(consume(bucket, 3).remaining).toBe(4);
      expect(consume(bucket, 3).remaining).toBe(1);
      expect(consume(bucket, 3).allowed).toBe(false);
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * retryAfter
   * ───────────────────────────────────────────────────────────────────────── */
  describe('retryAfter', () => {
    it('should return 0 when enough tokens available', () => {
      const bucket = createTokenBucket(10, 1, 5);
      expect(retryAfter(bucket, 3)).toBe(0);
    });

    it('should return seconds until tokens available', () => {
      const bucket = createTokenBucket(10, 2, 0); // rate=2/s, need 1 token → 0.5s → ceil to 1
      expect(retryAfter(bucket, 1)).toBe(1);
    });

    it('should return ceiling of fractional seconds', () => {
      const bucket = createTokenBucket(10, 1, 0); // rate=1/s, need 3 tokens → 3s
      expect(retryAfter(bucket, 3)).toBe(3);
    });

    it('should return Infinity when rate is 0', () => {
      const bucket = createTokenBucket(10, 0, 0);
      expect(retryAfter(bucket, 1)).toBe(Infinity);
    });

    it('should account for partial tokens', () => {
      const bucket = createTokenBucket(10, 1, 0.5); // have 0.5, need 1, rate=1 → 0.5s → ceil to 1
      expect(retryAfter(bucket, 1)).toBe(1);
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * serialize / deserialize
   * ───────────────────────────────────────────────────────────────────────── */
  describe('serialize / deserialize', () => {
    it('should round-trip a bucket', () => {
      const original = createTokenBucket(100, 5, 42.5, 1700000000000);
      const json = serialize(original);
      const restored = deserialize(json);

      expect(restored.capacity).toBe(100);
      expect(restored.rate).toBe(5);
      expect(restored.tokens).toBe(42.5);
      expect(restored.lastRefill).toBe(1700000000000);
    });

    it('should serialize to compact JSON array', () => {
      const bucket = createTokenBucket(10, 1, 5, 1700000000000);
      const json = serialize(bucket);
      expect(json).toBe('[10,1,5,1700000000000]');
    });

    it('should throw on invalid JSON', () => {
      expect(() => deserialize('not json')).toThrow();
    });

    it('should throw on non-array JSON', () => {
      expect(() => deserialize('{"a":1}')).toThrow('Invalid TokenBucket JSON');
    });

    it('should throw on too-short array', () => {
      expect(() => deserialize('[1,2,3]')).toThrow('Invalid TokenBucket JSON');
    });

    it('should throw on non-numeric values', () => {
      expect(() => deserialize('[10,"bad",5,1700000000000]')).toThrow('Invalid TokenBucket JSON');
    });

    it('should throw on NaN/Infinity values', () => {
      expect(() => deserialize('[10,1,NaN,1700000000000]')).toThrow();
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * TOKEN_BUCKET_LUA (structure check)
   * ───────────────────────────────────────────────────────────────────────── */
  describe('TOKEN_BUCKET_LUA', () => {
    it('should be a non-empty string', () => {
      expect(typeof TOKEN_BUCKET_LUA).toBe('string');
      expect(TOKEN_BUCKET_LUA.length).toBeGreaterThan(100);
    });

    it('should contain key operations', () => {
      expect(TOKEN_BUCKET_LUA).toContain('redis.call');
      expect(TOKEN_BUCKET_LUA).toContain('cjson.decode');
      expect(TOKEN_BUCKET_LUA).toContain('cjson.encode');
    });

    it('should have validation for corrupt data', () => {
      expect(TOKEN_BUCKET_LUA).toContain('pcall');
      expect(TOKEN_BUCKET_LUA).toContain("type(t) ~= 'table'");
    });

    it('should have clock-skew protection', () => {
      expect(TOKEN_BUCKET_LUA).toContain('now > lastRefill');
    });

    it('should guard against rate == 0 in TTL', () => {
      expect(TOKEN_BUCKET_LUA).toContain('if rate > 0');
    });

    it('should return -1 for retryAfterMs when rate == 0', () => {
      expect(TOKEN_BUCKET_LUA).toContain('retryAfterMs = -1');
    });
  });
});
