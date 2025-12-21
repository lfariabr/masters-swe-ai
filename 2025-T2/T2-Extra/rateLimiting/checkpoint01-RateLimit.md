# ⚡ ROUND 1 — CONCEPTUAL WARFARE

1. Explain in your own words the purpose of rate limiting in backend systems. Then — what kind of attacks or abuses does it help mitigate?

---

> **Reply**: 
It acts as a filter in between exchanged information on the system. It mitigates abuses of intense usage with increased costs on tokens and protects against DDos, brute-force, spam attacks to unlimited endpoints. 
This way we're covered in both performance and costs.

---

2. Differentiate between these three rate limiting strategies:
	1.	Fixed Window Counter
	2.	Sliding Window Log
	3.	Token Bucket
When would you choose each one?

---

> **Reply**: 
1. Fixed window sets how much time an action will be allowed to be executed. i.e.: 10 requests per day (24h). 
2. Sliding window allows customizing the recalculation of time based on first/last action. i.e, my 10th action was now (7h48am), and the next one available will be only  07h48am tomorrow.
3. Token allows limit usage per different sort of window (in Y time, in X amount of requests X time). A token can be access to information in terms of the number requests or value consumption of the requested data, for example.

---

3. Let’s say your app allows 10 OpenAI API calls per user per day.
What would the Redis key structure look like if you were implementing this in Express + Redis?
(Describe the key pattern and TTL logic.)

---

> **Reply**:
I'll have an express server with a redis client attached to it working as my in-memory database, storing user id and amount of requests made on that 1 day limit window, monitoring if user has reached or exceeded the limit to act. If the limit has been reached, it would block further requests to next day.
The key would be the user id, the value would be the amount of requests associated to that id on the interval (24h) and the TTL would store how much time for the access to be returned.

```typescript
rateLimit:<userId>:openai
value = 17
TTL = 86400 (24)
```

On that, I'd expand with the reset policy dilemma that we'd have to discuss:
1. Should we reset 24h after the first or last request sent by the user?
2. Alternativaly, if the reset's time is set to midnight, we wouldn't have to think about this.

---