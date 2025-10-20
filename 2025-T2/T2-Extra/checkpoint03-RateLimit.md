# 🧩 ROUND 3 — SYSTEM DESIGN SCENARIO

1. Your system has 3 tiers:
Free plan → 5 req/min
Pro plan → 60 req/min
Enterprise → 500 req/min
What would your middleware flow look like from request → Redis → response?
(Hint: mention JWT decode, plan lookup, key generation, Redis eval script, and error response.)

---

> **Reply**:
My middleware flow would be as follows:
1. Check for the presence of a JWT token in the request header
2. Decode the JWT token to extract user ID + plan type
3. Build key value relation `rate:usr:<userId>:<plan>`
4. Atomic operation with Redis + Lua script using `INCR` and `EXPIRE` logic
5. Decision and headers: `if count <= limit -> next()`
`else http 429 with Retry-Afer + RateLimitResetTime`
6. Handlers and response to everyone who made till here.
*Note: In clustered environments, ensure all instances use the same Redis cluster and synchronized clock (UTC) for consistent TTL-based windowing.*

---

2.You've noticed a lot of users hit the limit, but Redis memory is ballooning.
What's a smart optimization to reduce memory usage while keeping accuracy?

---

> **Reply**:
We could add a token bucket with a decreasing counter and on top of that add a leaky bucket limitation to keep memory in control.

---

3. What's the difference between rate limiting and throttling?
---

> **Reply**:
Rate limiting is the filtering layer for controlled request flow while throttling is what we do with failed attemps: do we discard? retry? queue?

---

4. Your rate limiter needs to work across multiple Node.js instances (horizontal scaling).
What's the critical requirement to make it consistent?

---

> **Reply**:
Idempotency. Avoid race conditions across different instances.

---