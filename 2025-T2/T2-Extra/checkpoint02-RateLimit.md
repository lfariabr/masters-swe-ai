# 🧠 ROUND 2 — TECHNICAL EXECUTION

1. Imagine this Redis script runs when a user sends a request:
```lua
local count = redis.call('INCR', KEYS[1])
if count == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return count
```
What’s happening here?
Explain each line and why it’s atomic.

---

> **Reply**: 
```lua
local count = redis.call('INCR', KEYS[1])
```
- It increments the counter stored at `KEYS[1]` (example: `rateLimit:userLuis:openai`)
- If the key doesn't exist yet, Redis automatically creates it and sets its value to 1
- The return value (new counter) is stored in `count`

```lua
if count == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
```
- On the **first increment only**, it sets a **TTL** (`ARGV[1]`, like 86400 s = 24 h)
- This ensure that the counter expires automatially after the time window ends.

```lua
return count
```
- Returns the updated count to the app so we can compare against set limit.

The entire script runs inside Redis as **one transaction**, meaning that all commands inside are executed sequentially with no interruption. So we never risk the "INCR succeeded but EXPIRE failed" race condition that can happen with separate network calls.

---

2. What’s the difference between 
```typescript
app.use(rateLimiter)
```
and
```typescript
app.get('/messages', rateLimiter, getMessages)
```
in Express.js?

---

> **Reply**: 
One the first example, the rate limiter is being used on the express server, meaning that it is being applied to all endpoints which run through the server, while on the second one limits the usage to the getMessages endpoint.

---

3. You want to rate limit per IP address instead of per user.
How would you modify your key generation logic?

---

> **Reply**: 
On my express server, instead of key per usedId, I would setup key per IP where the request is comming from.
The implementation pattern used could look like:
```typescript
const ip = req.ip || req.headers['x-firwarded-for'];
const key = `rateLimit:ip:${ip}`
```
I would also have a token budget or timed window logic implemented for in-depth cover strategy and could think about `rateLimit:${userId || ip}` to handle both logged-in and anonymous users in a cool way.

---