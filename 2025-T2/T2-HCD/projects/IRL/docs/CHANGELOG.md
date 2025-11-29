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
- [X] Complete Phase 0 (Foundation) - 2-3 days ✅ DONE
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
    - [X] Configure ESLint + Prettier for code quality
        - created `.eslintrc.json` with TypeScript + Prettier integration
        - created `.prettierrc` with project code style
        - added npm scripts: `lint`, `lint:fix`, `format`, `format:check`
    - [X] Add Winston logger with structured logging
        - created `src/utils/logger.ts` with Winston
        - helper functions: `logRequest`, `logRateLimit`, `logRedisOperation`
        - integrated into `src/index.ts` for HTTP request logging
        - supports JSON format in production with file transports
    - [X] Set up Jest for unit testing
        - created `jest.config.js` with ts-jest and 80% coverage threshold
        - created `tests/setup.ts` for test configuration
        - created `tests/redis.test.ts` (9 tests for Redis operations)
        - created `tests/api.test.ts` (5 tests for API endpoints)
        - installed supertest for HTTP testing
        - **17 tests passing!**

#### Project Structure
 ```bash
IRL/
├── src/
│   ├── index.ts          # Express server + endpoints
│   ├── db/
│   │   └── redis.ts      # Redis client + waitForRedis()
│   └── utils/
│       └── logger.ts     # Winston structured logging
├── tests/
│   ├── setup.ts          # Jest setup (loads .env, sets NODE_ENV)
│   ├── redis.test.ts     # 9 Redis integration tests
│   └── api.test.ts       # 8 API integration tests
├── .eslintrc.json        # ESLint config
├── .prettierrc           # Prettier config
├── jest.config.js        # Jest config
├── docker-compose.yml    # Redis + Redis Commander
├── package.json          # Dependencies + scripts
└── tsconfig.json         # TypeScript config
```

- [ ] Complete Phase 1 (Rate Limiting)
    - [X] **1.1**: Set up Redis client with ioredis
    - [ ] Break down `src/index.ts` into modular files:
        - `src/routes/testRateLimit.ts` - Rate limit test endpoint
        - `src/routes/health.routes.ts` - Health check endpoint
    - [ ] **1.2**: Implement Token Bucket algorithm
        - Token generation rate calculation
        - Bucket capacity management
        - Atomic token consumption using Redis Lua scripts
    - [ ] **1.3**: Create REST API endpoints:
        - `POST /api/request` - Request access (consumes token)
        - `GET /api/quota/:agentId` - Check remaining quota
    - [ ] **1.4**: Add rate limit middleware
    - [ ] **1.5**: Write unit tests (>80% coverage)
    - [ ] **1.6**: Load test with Apache Bench or k6

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