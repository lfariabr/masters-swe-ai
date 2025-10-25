 # 🧩 ROUND 3 — SYSTEM DESIGN SCENARIO

1. Your system has 3 tiers:
Free plan → 5 req/min
Pro plan → 60 req/min
Enterprise → 500 req/min
What would your middleware flow look like from request → Redis → response?
(Hint: mention JWT decode, plan lookup, key generation, Redis eval script, and error response.)

---

> **Reply**:
My middleware flow would have 5 steps:
1. Request has an Authorization header
2. Decode the JWT token on a fetch to bring back the user and plan
3. Generate a request on redis client with `<userId>:<plan>:<timestamp>`
4. Atomic operation redis + lua script using `INCR` and `EXPIRE` logic to avoid race conditions
    - if count <= limit -> next()
    - else http 429 with `Retry-After` and `RateLimitResetTime`
5. Handlers and response to everyone who made till here.

Additional things we could add to the sprint planning:
- 2nd middleware for Rate Limiting per IP
- Throttling
- Leaky Bucket

*Note: In clustered environments, ensure all instances use the same Redis cluster and synchronized clock (UTC) for consistent TTL-based windowing.*

---

2.You've noticed a lot of users hit the limit, but Redis memory is ballooning.
What's a smart optimization to reduce memory usage while keeping accuracy?

---

> **Reply**:
Her's a few improvements that could have been made to the system:
- Switch to fixed window counter (single integer + TTL) → tiny memory. 
- Or sliding window counter (two buckets): keep only 2 counters (current minute and previous minute) and interpolate → smooth like sliding window, minimal memory.
- Token bucket stored as just {tokens, lastRefillAt} → constant O(1) memory.
- Reduce key cardinality (e.g., per-user, not per-user-per-route unless needed).
- Short, tight TTLs; compact key names.
- If you must do global abuse detection, use Count-Min Sketch (approximate, low memory).

---

3. What's the difference between rate limiting and throttling?
---

> **Reply**:
- Rate limiting: a policy/ceiling on how many requests are allowed per time window (enforced with 429, or by delaying). It’s about maximum allowed rate.
- Throttling: the mechanism to slow down processing (e.g., queue/delay/jitter) to meet a desired rate. You can throttle before hitting limits to smooth bursts.

---

4. Your rate limiter needs to work across multiple Node.js instances (horizontal scaling).
What's the critical requirement to make it consistent?

---

> **Reply**:
The most critical requirement is a shared authoritative store and atomic ops. Steps to make it consistent:
- Use a centralized/shared datastore (Redis/Redis Cluster) for counters.
- Use atomic Lua scripts (or Redis INCRBY/EXPIRE combos in scripts).
- Ensure all instances compute the same window (clock/tz uniform; prefer TTL-based windows vs server clocks).
- If behind a proxy, normalize client IP (X-Forwarded-For) consistently.

---