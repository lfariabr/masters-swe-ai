// src/core/rateLimiter/tokenBucket.ts
// Phase 1: Token Bucket algorithm (README §1.2)
// - Token generation rate calculation
// - Bucket capacity management
// - Serialize/deserialize for Redis storage
// - Atomic consumption via Redis Lua script (see TOKEN_BUCKET_LUA below)

/* ─────────────────────────────────────────────────────────────────────────────
 * Interface
 * ───────────────────────────────────────────────────────────────────────────── */

export interface TokenBucket {
  capacity: number;   // max tokens
  rate: number;       // tokens added per second
  tokens: number;     // current available (may be fractional)
  lastRefill: number; // ms timestamp
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Factory
 * ───────────────────────────────────────────────────────────────────────────── */

/**
 * Create a TokenBucket. Starts full by default.
 */
export function createTokenBucket(
  capacity: number,
  rate: number,
  tokens: number = capacity,
  lastRefill: number = Date.now(),
): TokenBucket {
  if (capacity <= 0) throw new Error('TokenBucket capacity must be positive');
  if (rate < 0) throw new Error('TokenBucket rate cannot be negative');
  return {
    capacity,
    rate,
    tokens: clamp(tokens, 0, capacity),
    lastRefill,
  };
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Core Operations
 * ───────────────────────────────────────────────────────────────────────────── */

/** Refill bucket based on elapsed time. Mutates bucket. */
export function refill(bucket: TokenBucket, now = Date.now()): void {
  if (now <= bucket.lastRefill) return;
  const elapsed = (now - bucket.lastRefill) / 1000;
  bucket.tokens = clamp(bucket.tokens + elapsed * bucket.rate, 0, bucket.capacity);
  bucket.lastRefill = now;
}

/** Try to consume tokens. Returns success + remaining. */
export function consume(bucket: TokenBucket, amount = 1): { allowed: boolean; remaining: number } {
  refill(bucket);
  if (bucket.tokens >= amount) {
    bucket.tokens -= amount;
    return { allowed: true, remaining: bucket.tokens };
  }
  return { allowed: false, remaining: bucket.tokens };
}

/** Seconds until `amount` tokens available (for Retry-After header). */
export function retryAfter(bucket: TokenBucket, amount = 1): number {
  refill(bucket);
  if (bucket.tokens >= amount) return 0;
  if (bucket.rate <= 0) return Infinity;
  return Math.ceil((amount - bucket.tokens) / bucket.rate);
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Serialization (for Redis GET/SET)
 * ───────────────────────────────────────────────────────────────────────────── */

/** Compact JSON array: [capacity, rate, tokens, lastRefill] */
export function serialize(bucket: TokenBucket): string {
  return JSON.stringify([bucket.capacity, bucket.rate, bucket.tokens, bucket.lastRefill]);
}

/** Parse serialized bucket. Throws on invalid data. */
export function deserialize(json: string): TokenBucket {
  const arr = JSON.parse(json);
  if (!Array.isArray(arr) ||
    arr.length < 4 ||
    !arr.slice(0, 4).every((v) => typeof v === 'number' && Number.isFinite(v))
  ) {
    throw new Error('Invalid TokenBucket JSON');
  }
  const [capacity, rate, tokens, lastRefill] = arr as number[];
  return createTokenBucket(capacity, rate, tokens, lastRefill);
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Redis Lua Script (for atomic consumption in distributed setup)
 * Usage: redis.eval(TOKEN_BUCKET_LUA, 1, key, capacity, rate, amount, nowMs)
 * Returns: [allowed (0|1), remaining, retryAfterMs]
 *          retryAfterMs: -1 means Infinity (rate == 0, will never refill)
 * ───────────────────────────────────────────────────────────────────────────── */

export const TOKEN_BUCKET_LUA = `
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local amount = tonumber(ARGV[3])
local now = tonumber(ARGV[4])

local data = redis.call('GET', key)
local tokens, lastRefill

if data then
  local ok, t = pcall(cjson.decode, data)
  -- validate structure (mirrors TS deserialize paranoia)
  if not ok or type(t) ~= 'table' or #t < 4 or
     type(t[1]) ~= 'number' or type(t[2]) ~= 'number' or
     type(t[3]) ~= 'number' or type(t[4]) ~= 'number' then
    -- corrupt data: re-initialize
    tokens = capacity
    lastRefill = now
  else
    tokens = t[3]
    lastRefill = t[4]
  end
else
  tokens = capacity
  lastRefill = now
end

-- refill (only if clock moved forward; mirrors TS early-return)
if now > lastRefill then
  local elapsed = (now - lastRefill) / 1000
  tokens = math.min(capacity, tokens + elapsed * rate)
  lastRefill = now
end

-- consume
local allowed = 0
if tokens >= amount then
  tokens = tokens - amount
  allowed = 1
end

-- persist (guard against rate == 0 to avoid division by zero)
local ttl = 60
if rate > 0 then
  ttl = math.ceil(capacity / rate) + 60
end
redis.call('SET', key, cjson.encode({capacity, rate, tokens, lastRefill}), 'EX', ttl)

-- retry-after (ms): -1 = Infinity (zero-rate bucket, will never refill)
local retryAfterMs = 0
if allowed == 0 then
  if rate > 0 then
    retryAfterMs = math.ceil((amount - tokens) / rate * 1000)
  else
    retryAfterMs = -1
  end
end

return {allowed, tokens, retryAfterMs}
`;

/* ─────────────────────────────────────────────────────────────────────────────
 * Helpers
 * ───────────────────────────────────────────────────────────────────────────── */

function clamp(v: number, lo: number, hi: number): number {
  return Math.max(lo, Math.min(hi, v));
}