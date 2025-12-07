# Intelligent Rate Limiting System (IRL)

> **Human-centered governance middleware for Agentic AI systems**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0-red.svg)](https://redis.io/)

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Architecture](#️-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [NEXT STEPS - Development Roadmap](#️-next-steps---development-roadmap)
- [Learning Objectives](#-learning-objectives)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚨 Problem Statement

**Agentic AI systems** (AutoGPT, Devin, GPT-Engineer) operate autonomously—making API calls without human intervention. This creates critical failures:

- **💸 Financial**: $15k-$50k overnight billing disasters
- **🌍 Environmental**: 800kg CO₂/month with zero carbon awareness
- **👥 Human**: 47,000+ Stack Overflow questions on opaque throttling
- **⚖️ Ethical**: Accountability diffusion when agents cause harm

Current solutions? **Generic HTTP 429 errors** with zero context, zero fairness, zero human control.

---

## ✅ Solution Overview

The **Intelligent Rate Limiting (IRL) System** is a governance middleware that transforms rate limiting from an automated constraint into a **collaborative dialogue** between humans and AI systems.

### The 5 HCD Pillars

1. **👁️ Visibility**: Real-time dashboard showing quota consumption, costs, carbon footprint
2. **💬 Feedback**: Contextual explanations for throttling decisions (not just "429 error")
3. **⚖️ Fair Allocation**: Weighted quotas prioritizing research/education/non-profits
4. **📝 Accountability**: Immutable audit logs for every decision
5. **♻️ Sustainability**: Carbon-aware throttling using real-time grid intensity data

---

## 🎯 Features

### Core Rate Limiting
- ✅ **Token Bucket Algorithm** with distributed Redis backend
- ✅ **Sliding Window Counter** for precise quota enforcement
- ✅ **Weighted Fair Queuing** for multi-tier allocation
- ✅ **Dynamic Quota Adjustment** based on usage patterns

### Carbon Awareness
- ✅ **Real-time Grid Intensity** via Carbon Aware SDK
- ✅ **Temporal Workload Shifting** (15-30% emission reduction)
- ✅ **Carbon Cost Visibility** alongside financial costs

### Human-Centered Design
- ✅ **Contrastive Explanations**: "Why blocked" + "What would succeed"
- ✅ **Human-in-the-Loop Overrides** with justification logging
- ✅ **Multi-language Support** (i18n ready)

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|----------|
| **Node.js** | 18+ | Async-first runtime |
| **TypeScript** | 5.0+ | Type safety |
| **Apollo Server** | 4.x | GraphQL API |
| **Redis** | 7.0+ | Distributed tokens |
| **PostgreSQL** | 15+ | Audit logs |

### Frontend (Dashboard)
| Technology | Purpose |
|------------|----------|
| **Next.js 14** | React framework |
| **shadcn/ui** | Component library |
| **TailwindCSS** | Styling |

### Why These Choices?
- **Redis**: Proven at scale (Twitter, GitHub use it). Atomic operations critical for distributed rate limiting.
- **GraphQL**: Real-time subscriptions for dashboard updates. Clients request exactly what they need.
- **TypeScript**: Type safety prevents production bugs in async workflows.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Agentic AI  │  │   Dashboard  │  │   Admin CLI  │     │
│  │   Agents     │  │   (Next.js)  │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│              IRL Governance Middleware (Node.js)            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              GraphQL API (Apollo Server)             │   │
│  │  • Queries: getQuota, getUsage, getAuditLogs         │   │
│  │  • Mutations: requestAccess, requestOverride         │   │
│  │  • Subscriptions: quotaUpdates, throttlingEvents     │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Rate Limiting Engine (Core Logic)          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐      │   │
│  │  │   Token    │  │  Sliding   │  │  Weighted  │      │   │
│  │  │   Bucket   │  │   Window   │  │Fair Queue  │      │   │
│  │  └────────────┘  └────────────┘  └────────────┘      │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Carbon Aware Scheduler (Green Logic)         │   │
│  │  • Real-time grid intensity monitoring               │   │
│  │  • Temporal workload shifting                        │   │
│  └────────────────────────┬─────────────────────────────┘   │
└───────────────────────────┼─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Redis     │  │  PostgreSQL  │  │  Prometheus  │       │
│  │  (Quotas)    │  │ (Audit Logs) │  │  (Metrics)   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

### Required
- **Node.js** 18+ ([download](https://nodejs.org/))
- **npm** 8+ (`npm install -g npm`)
- **Docker** & **Docker Compose** ([download](https://www.docker.com/))

### Optional
- **Kubernetes** (minikube for local testing)
- **Carbon Aware SDK** API key

---

## 🚀 Quick Start

```bash
# 1. Clone & Install
git clone https://github.com/lfariabr/masters-swe-ai.git
cd masters-swe-ai/2025-T2/T2-HCD/projects/IRL
npm install

# 2. Environment Setup
cp .env.example .env
# Edit .env with your configuration

# 3. Start Infrastructure
docker-compose up -d
npm db:migrate
npm db:seed

# 4. Start Development Server
npm run dev
```

**GraphQL Playground**: http://localhost:4000/graphql

---

## 🗺️ NEXT STEPS - Development Roadmap

> **Learning-First Approach**: Each phase builds progressively more complex features while teaching you the underlying technologies.

### **Phase 0: Foundation Setup** ⏱️ 2-3 days
**Goal**: Get comfortable with the tech stack and project structure

#### Tasks:
- [X] Set up Node.js + TypeScript project with proper tsconfig
- [X] Configure ESLint + Prettier for code quality
- [X] Set up Docker Compose for Redis + PostgreSQL
- [X] Create basic Express server with health check endpoint
- [X] Add Winston logger with structured logging
- [X] Set up Jest for unit testing

#### Learning Objectives:
- ✅ Understand TypeScript compilation and type system
- ✅ Learn Docker networking and volume management
- ✅ Master async/await patterns in Node.js
- ✅ Practice test-driven development (TDD)

#### Resources:
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [Jest Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

---

### **Phase 1: Basic Rate Limiting** ⏱️ 5-7 days
**Goal**: Implement Token Bucket algorithm with Redis

#### Tasks:
- [X] **1.1**: Set up Redis client with ioredis
- [X] **1.2**: Implement Token Bucket algorithm
  - Token generation rate calculation
  - Bucket capacity management
  - Atomic token consumption using Redis Lua scripts
- [X] **1.3**: Create REST API endpoints:
  - `POST /api/request` - Request access (consumes token)
  - `GET /api/quota/:agentId` - Check remaining quota
- [X] **1.4**: Add rate limit middleware
- [X] **1.5**: Write unit tests (>80% coverage)
- [ ] **1.6**: Load test with Apache Bench or k6

#### Learning Objectives:
- ✅ Master Redis data structures (Strings, Hashes, Sorted Sets)
- ✅ Understand atomic operations and race conditions
- ✅ Learn Lua scripting for Redis EVAL commands
- ✅ Practice performance testing and optimization

#### Key Concepts:
```typescript
// Token Bucket: Tokens refill at constant rate
interface TokenBucket {
  capacity: number;  // max tokens
  rate: number;      // tokens added per second
  tokens: number;    // current available
  lastRefill: number; // timestamp
}
```

#### Resources:
- [Token Bucket Algorithm Explained](https://en.wikipedia.org/wiki/Token_bucket)
- [Redis Lua Scripting](https://redis.io/docs/manual/programmability/eval-intro/)
- [ioredis Documentation](https://github.com/redis/ioredis)

---

### **Phase 2: GraphQL API Layer** ⏱️ 5-7 days
**Goal**: Replace REST with GraphQL for flexible querying

#### Tasks:
- [ ] **2.1**: Set up Apollo Server 4
- [ ] **2.2**: Define GraphQL schema:
  ```graphql
  type Agent {
    id: ID!
    name: String!
    tier: TierLevel!
    quotas: QuotaAllocation!
  }
  
  type Query {
    agent(id: ID!): Agent
    quota(agentId: ID!): QuotaAllocation
  }
  
  type Mutation {
    requestAccess(agentId: ID!, action: String!): ThrottlingDecision!
  }
  
  type Subscription {
    quotaUpdates(agentId: ID!): QuotaAllocation!
  }
  ```
- [ ] **2.3**: Implement resolvers with DataLoader
- [ ] **2.4**: Add JWT authentication
- [ ] **2.5**: Set up GraphQL subscriptions with WebSockets
- [ ] **2.6**: Write integration tests

#### Learning Objectives:
- ✅ Understand GraphQL vs REST trade-offs
- ✅ Master resolver patterns
- ✅ Learn DataLoader for N+1 query prevention
- ✅ Practice JWT authentication

#### Resources:
- [Apollo Server Docs](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Schema Design](https://www.apollographql.com/blog/graphql-schema-design-building-evolvable-schemas)

---

### **Phase 3: Multi-Tier Fair Allocation** ⏱️ 4-5 days
**Goal**: Implement weighted fair queuing

#### Tasks:
- [ ] **3.1**: Design tier system:
  ```typescript
  enum TierLevel {
    RESEARCH = "RESEARCH",     // 3x priority weight
    EDUCATION = "EDUCATION",   // 2.5x weight
    NONPROFIT = "NONPROFIT",   // 2x weight
    STARTUP = "STARTUP",       // 1.5x weight
    ENTERPRISE = "ENTERPRISE"  // 1x weight
  }
  ```
- [ ] **3.2**: Implement Weighted Fair Queuing algorithm
- [ ] **3.3**: Add tier-based quota allocation
- [ ] **3.4**: Create admin mutations for tier management
- [ ] **3.5**: Priority queue using Redis Sorted Sets
- [ ] **3.6**: Write fairness validation tests

#### Learning Objectives:
- ✅ Understand fairness vs equality
- ✅ Learn priority queue implementation
- ✅ Practice Value-Sensitive Design
- ✅ Master statistical testing

#### Key Algorithm:
```typescript
// Weighted Fair Queuing: Virtual finish time
function calculateVirtualFinishTime(
  agent: Agent,
  requestSize: number
): number {
  const weight = getTierWeight(agent.tier);
  return Math.max(
    agent.lastFinishTime,
    Date.now()
  ) + (requestSize / weight);
}
```

---

### **Phase 4: Carbon-Aware Throttling** ⏱️ 6-8 days
**Goal**: Integrate real-time carbon intensity data

#### Tasks:
- [ ] **4.1**: Integrate Carbon Aware SDK
- [ ] **4.2**: Implement carbon intensity fetcher (5-min TTL cache)
- [ ] **4.3**: Add carbon cost calculator:
  ```typescript
  function calculateCarbonCost(
    energyKWh: number,
    gridIntensity: number // gCO2/kWh
  ): number {
    return energyKWh * gridIntensity;
  }
  ```
- [ ] **4.4**: Implement temporal workload shifting
- [ ] **4.5**: Add carbon budget enforcement
- [ ] **4.6**: Create carbon dashboard
- [ ] **4.7**: Carbon impact reports

#### Learning Objectives:
- ✅ Understand electricity grid carbon intensity
- ✅ Learn temporal scheduling algorithms
- ✅ Practice environmental impact measurement

#### Key Research:
- **Wiesner et al. (2023)**: 15-30% emission reduction via temporal shifting
- **Alevizos et al. (2025)**: Algorithmic carbon efficiency varies 50%+

#### Resources:
- [Green Software Foundation](https://greensoftware.foundation/)
- [Carbon Aware SDK](https://github.com/Green-Software-Foundation/carbon-aware-sdk)

---

### **Phase 5: Audit Logging** ⏱️ 4-5 days
**Goal**: Implement immutable audit trail

#### Tasks:
- [ ] **5.1**: Design PostgreSQL schema:
  ```sql
  CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    agent_id VARCHAR(255) NOT NULL,
    action VARCHAR(255) NOT NULL,
    decision VARCHAR(50) NOT NULL,
    metadata JSONB
  );
  ```
- [ ] **5.2**: Implement append-only log writer
- [ ] **5.3**: Add log querying with pagination
- [ ] **5.4**: Create retention policy (90 days active)
- [ ] **5.5**: Add export to CSV/JSON
- [ ] **5.6**: Implement integrity verification

#### Learning Objectives:
- ✅ Understand append-only structures
- ✅ Learn PostgreSQL JSONB querying
- ✅ Practice compliance-focused design

---

### **Phase 6: Dashboard UI (Next.js)** ⏱️ 7-10 days
**Goal**: Build human-centered dashboard

#### Tasks:
- [ ] **6.1**: Set up Next.js 14 with App Router
- [ ] **6.2**: Integrate Apollo Client
- [ ] **6.3**: Build pages:
  - Overview: Quota, carbon, costs
  - Agents: List with status
  - Audit Logs: Searchable viewer
  - Settings: Tier management
- [ ] **6.4**: Real-time updates with subscriptions
- [ ] **6.5**: Data visualizations (Recharts)
- [ ] **6.6**: Override request workflow
- [ ] **6.7**: Responsive design
- [ ] **6.8**: Dark mode toggle

#### Learning Objectives:
- ✅ Master Next.js App Router
- ✅ Learn Apollo Client hooks
- ✅ Practice data visualization
- ✅ Understand HCD principles

#### HCD Guidelines:
- **G2**: Make clear what the system can do
- **G7**: Support efficient invocation
- **G16**: Convey consequences
- **G18**: Provide global controls

---

### **Phase 7: Contextual Feedback** ⏱️ 4-5 days
**Goal**: Replace generic errors with explanations

#### Tasks:
- [ ] **7.1**: Design explanation templates:
  ```typescript
  interface ExplanationTemplate {
    reason: string;         // Why blocked
    currentState: string;   // Current usage
    threshold: string;      // Limit triggered
    resetTime: string;      // When quota resets
    alternatives: string[]; // What would succeed
  }
  ```
- [ ] **7.2**: Implement contrastive explanation generator
- [ ] **7.3**: Add i18n support (EN, PT, ES)
- [ ] **7.4**: Create quality metrics
- [ ] **7.5**: A/B test with user surveys

#### Learning Objectives:
- ✅ Understand Explainable AI (XAI)
- ✅ Learn contrastive vs descriptive explanations
- ✅ Practice internationalization

---

### **Phase 8: Abuse Detection (ML)** ⏱️ 7-10 days
**Goal**: Detect anomalous behavior with ML

#### Tasks:
- [ ] **8.1**: Collect training data
- [ ] **8.2**: Feature engineering:
  - Request frequency
  - Burst patterns
  - API diversity
  - Time-of-day patterns
- [ ] **8.3**: Train models:
  - Isolation Forest
  - Autoencoder
  - Statistical baseline
- [ ] **8.4**: Real-time scoring pipeline
- [ ] **8.5**: Automatic circuit breaker
- [ ] **8.6**: False positive review workflow
- [ ] **8.7**: Measure precision/recall/F1

#### Target Metrics:
- **Precision**: >90%
- **Recall**: >85%
- **Latency**: <10ms

---

### **Phase 9: Observability** ⏱️ 5-6 days
**Goal**: Production monitoring with Prometheus + Grafana

#### Tasks:
- [ ] **9.1**: Add Prometheus metrics
- [ ] **9.2**: Set up Grafana dashboards
- [ ] **9.3**: Add alerting rules
- [ ] **9.4**: Distributed tracing (OpenTelemetry)
- [ ] **9.5**: Structured logging with correlation IDs

---

### **Phase 10: Kubernetes Deployment** ⏱️ 6-8 days
**Goal**: Production-ready deployment

#### Tasks:
- [ ] **10.1**: Create Dockerfile (multi-stage)
- [ ] **10.2**: Write K8s manifests
- [ ] **10.3**: Set up Helm chart
- [ ] **10.4**: Configure Redis Cluster
- [ ] **10.5**: Add health checks
- [ ] **10.6**: Graceful shutdown
- [ ] **10.7**: CI/CD pipeline (GitHub Actions)
- [ ] **10.8**: Deploy to staging

---

### **Phase 11: Documentation & Testing** ⏱️ 5-6 days
**Goal**: >85% test coverage

#### Tasks:
- [ ] **11.1**: Comprehensive README
- [ ] **11.2**: API documentation
- [ ] **11.3**: Architecture decision records
- [ ] **11.4**: Incident runbooks
- [ ] **11.5**: Unit tests
- [ ] **11.6**: Integration tests
- [ ] **11.7**: E2E tests (Playwright)
- [ ] **11.8**: Code coverage reporting

---

### **Phase 12: User Research** ⏱️ 4-6 weeks
**Goal**: Empirical validation

#### Tasks:
- [ ] **12.1**: Design usability study protocol
- [ ] **12.2**: Recruit diverse participants
- [ ] **12.3**: Conduct think-aloud sessions
- [ ] **12.4**: Measure comprehension (Likert scales)
- [ ] **12.5**: Assess fairness perception
- [ ] **12.6**: Collect trust metrics
- [ ] **12.7**: Cultural validation
- [ ] **12.8**: Iterate based on feedback
- [ ] **12.9**: Write research paper (optional)

---

## 📚 Learning Objectives

### Technical Skills
- ✅ **Backend**: Node.js, TypeScript, GraphQL, Redis, PostgreSQL
- ✅ **Frontend**: Next.js, React, shadcn/ui
- ✅ **DevOps**: Docker, Kubernetes, CI/CD
- ✅ **Algorithms**: Token Bucket, Weighted Fair Queuing
- ✅ **ML**: Anomaly detection

### Domain Knowledge
- ✅ **Rate Limiting**: Distributed systems, edge cases
- ✅ **Carbon Awareness**: Grid intensity, impact measurement
- ✅ **Ethical AI**: Fairness, accountability, transparency
- ✅ **HCD**: Amershi's 18 guidelines

---

## 📁 Project Structure

```
IRL/
├── README.md
├── package.json
├── tsconfig.json
├── docker-compose.yml
│
├── src/
│   ├── core/rateLimiter/
│   ├── core/carbonAware/
│   ├── core/ethicalGovernance/
│   ├── graphql/
│   └── db/
│
├── dashboard/ (Next.js)
├── tests/
├── k8s/
└── docs/
```

---

## 🙏 Acknowledgments

- **Dr. Omid Haas** (Torrens University) - Academic supervision
- **Julio & Tamara** - Project teammates
- **Green Software Foundation** - Carbon Aware SDK

---

## 📧 Contact

**Luis Faria**  
- LinkedIn: [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)
- Portfolio: [luisfaria.dev](https://luisfaria.dev)

---

**Built with ❤️ at Torrens University Australia 🇦🇺**