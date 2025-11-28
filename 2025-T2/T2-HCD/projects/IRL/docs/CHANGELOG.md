## Changelog

### **Immediate (Today)**
```bash
# 1. Review the README
# 2. Star Phase 0 (Foundation Setup)
# 3. Set up your initial project structure:


cd 2025-T2/T2-HCD/projects/IRL
mkdir -p src/{core,graphql,db,models,services,middleware,utils}
mkdir -p dashboard tests k8s docs
touch package.json tsconfig.json docker-compose.yml .env.example
```

### **This Week**
- [X] Complete Phase 0 (Foundation) - 2-3 days
    - [X] Get a running Node.js server with Redis connected
        - created `package.json` and installed dependencies: node, express, ioredis, typescript, jest
        - created `tsconfig.json` for TypeScript configuration
        - created `docker-compose.yml` to set up Redis service
        - created .env.example, .env and .gitignore for environment variables
        - created a basic Redis client in `src/db/redis.ts`
        - created a comprehensive `src/index.ts` to:
            - start the Express server 
            - connect to Redis
            - basic rate limit test endpoint*
        NEXT:
            - add jest tests for Redis connection and basic endpoint
    - [ ] Document your learnings as you go
- [ ] Set up your GitHub repo structure

### **This Month**
- [ ] Phase 1 Basic Rate Limiting 7 days
    Goal: Token Bucket algorithm with Redis backend
    Exit Criteria: API returns 200 or 429 with Retry-After header, tests pass
- [ ] Phase 2 GraphQL Layer 7 days
    Goal: Replace REST with GraphQL API
    Exit Criteria: GraphQL Playground works, subscriptions fire on quota change
- [ ] Phase 3 Multi-Tier Allocation Layer 7 days
    Goal: Weighted Fair Queuing for different user tiers
    Exit Criteria: Research tier gets 3x priority, verified by load tests
- [ ] Start building your dev.to article as you progress

### **Final Expected Result**
Working rate limiter with
✅ Token Bucket + Sliding Window algorithms
✅ GraphQL API with real-time subscriptions
✅ Multi-tier fair allocation
✅ Redis-backed distributed state
✅ >80% test coverage

---

## 💡 Pro Tips

1. **Track Progress**: Use the checkboxes in the README
2. **Learn by Doing**: Don't skip the "why" - understand each technology
3. **Document Everything**: Future you (and dev.to readers) will thank you
4. **Start Simple**: Phase 0 is intentionally basic - master it before moving on
5. **Build in Public**: Share your journey on Twitter/LinkedIn/dev.to

---

## 📊 Estimated Timeline

- **Months 1-2**: Phases 0-4 (Foundation + Core Features)
- **Month 3**: Phases 5-7 (Logging + UI + Feedback)
- **Month 4**: Phases 8-11 (ML + Production)
- **Months 4-5**: Phase 12 (User Research)

**By end of T2**: You'll have a production-ready, research-validated AI governance system! 