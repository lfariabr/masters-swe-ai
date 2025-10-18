# 🧩 ROUND 3 — SYSTEM DESIGN SCENARIO

1. Your system has 3 tiers:
Free plan → 5 req/min
Pro plan → 60 req/min
Enterprise → 500 req/min
What would your middleware flow look like from request → Redis → response?
(Hint: mention JWT decode, plan lookup, key generation, Redis eval script, and error response.)

---

> **Reply**:
I would have the requests requiring and decoding a JWT token on the API to start with. My middleware would also have a timed window logic with userID being key and value being counter using a lua script to cover race conditions.
If the counter is not exceeded, return the response requested. If exceeded, return an error.
Future enhancement could be add a token bucket improvement on redis to instead of counting up, count requests down from starting point.

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