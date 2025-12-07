// tests/quota.routes.test.ts
// Tests for Phase 1.3 endpoints: POST /api/request and GET /api/quota/:agentId

import request from 'supertest';
import { app, redis } from '../src/index';
import { waitForRedis } from '../src/db/redis';

describe('Quota Routes (Phase 1.3)', () => {
  const TEST_AGENT_ID = 'test-agent-quota-routes';

  beforeAll(async () => {
    await waitForRedis();
  });

  beforeEach(async () => {
    // Clean up test keys before each test
    const keys = await redis.keys(`ratelimit:agent:${TEST_AGENT_ID}*`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  });

  afterAll(async () => {
    // Clean up test keys only
    // Note: This test uses the shared Redis client from src/index.
    // The shared client is not closed here to avoid race conditions with other test suites.
    // Jest's forceExit handles cleanup of shared connections.
    const keys = await redis.keys(`ratelimit:agent:${TEST_AGENT_ID}*`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * POST /api/request
   * ───────────────────────────────────────────────────────────────────────── */
  describe('POST /api/request', () => {
    it('should allow request with valid agentId', async () => {
      const response = await request(app)
        .post('/api/request')
        .send({ agentId: TEST_AGENT_ID });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('success', true);
      expect(response.body).toHaveProperty('message', 'Request allowed');
      expect(response.body).toHaveProperty('tokensConsumed', 1);
      expect(response.body).toHaveProperty('remaining');
      expect(response.body).toHaveProperty('limit');
    });

    it('should include rate limit headers in response', async () => {
      const response = await request(app)
        .post('/api/request')
        .send({ agentId: TEST_AGENT_ID });

      expect(response.headers).toHaveProperty('x-ratelimit-limit');
      expect(response.headers).toHaveProperty('x-ratelimit-remaining');
      expect(response.headers).toHaveProperty('x-ratelimit-reset');

      const limit = parseInt(response.headers['x-ratelimit-limit'], 10);
      const remaining = parseInt(response.headers['x-ratelimit-remaining'], 10);

      expect(limit).toBeGreaterThan(0);
      expect(remaining).toBeGreaterThanOrEqual(0);
      expect(remaining).toBeLessThanOrEqual(limit);
    });

    it('should consume multiple tokens when specified', async () => {
      const response = await request(app)
        .post('/api/request')
        .send({ agentId: TEST_AGENT_ID, tokens: 5 });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('tokensConsumed', 5);
    });

    it('should decrement remaining tokens on subsequent requests', async () => {
      // First request
      const response1 = await request(app)
        .post('/api/request')
        .send({ agentId: TEST_AGENT_ID });

      const remaining1 = response1.body.remaining;

      // Second request
      const response2 = await request(app)
        .post('/api/request')
        .send({ agentId: TEST_AGENT_ID });

      const remaining2 = response2.body.remaining;

      expect(remaining2).toBeLessThan(remaining1);
    });

    it('should return 400 when agentId is missing', async () => {
      const response = await request(app).post('/api/request').send({});

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error', 'Bad Request');
      expect(response.body.message).toContain('agentId');
    });

    it('should return 400 when agentId is not a string', async () => {
      const response = await request(app)
        .post('/api/request')
        .send({ agentId: 12345 });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error', 'Bad Request');
    });

    it('should return 400 when tokens is invalid', async () => {
      const response = await request(app)
        .post('/api/request')
        .send({ agentId: TEST_AGENT_ID, tokens: -1 });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error', 'Bad Request');
      expect(response.body.message).toContain('tokens');
    });

    it('should return 429 when rate limit is exceeded', async () => {
      const agentId = `${TEST_AGENT_ID}-exhausted`;

      // Exhaust all tokens at once (assuming default capacity of 100)
      await request(app)
        .post('/api/request')
        .send({ agentId, tokens: 100 });

      // This request should be blocked
      const response = await request(app)
        .post('/api/request')
        .send({ agentId, tokens: 1 });

      expect(response.status).toBe(429);
      expect(response.body).toHaveProperty('error', 'Too Many Requests');
      expect(response.body).toHaveProperty('retryAfter');
      expect(response.headers).toHaveProperty('retry-after');

      // Cleanup
      await redis.del(`ratelimit:agent:${agentId}`);
    });

    it('should include Retry-After header when rate limited', async () => {
      const agentId = `${TEST_AGENT_ID}-retry-after`;

      // Exhaust tokens
      await request(app)
        .post('/api/request')
        .send({ agentId, tokens: 100 });

      const response = await request(app)
        .post('/api/request')
        .send({ agentId, tokens: 1 });

      expect(response.headers).toHaveProperty('retry-after');
      const retryAfter = parseInt(response.headers['retry-after'], 10);
      expect(retryAfter).toBeGreaterThan(0);

      // Cleanup
      await redis.del(`ratelimit:agent:${agentId}`);
    });
  });

  /* ─────────────────────────────────────────────────────────────────────────
   * GET /api/quota/:agentId
   * ───────────────────────────────────────────────────────────────────────── */
  describe('GET /api/quota/:agentId', () => {
    it('should return full quota for new agent', async () => {
      const agentId = `${TEST_AGENT_ID}-new`;
      const response = await request(app).get(`/api/quota/${agentId}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('agentId', agentId);
      expect(response.body).toHaveProperty('remaining');
      expect(response.body).toHaveProperty('limit');
      expect(response.body).toHaveProperty('rate');
      expect(response.body).toHaveProperty('status', 'new');
      expect(response.body.remaining).toBe(response.body.limit);
    });

    it('should return active status after requests are made', async () => {
      const agentId = `${TEST_AGENT_ID}-active`;

      // Make a request to create the bucket
      await request(app)
        .post('/api/request')
        .send({ agentId, tokens: 10 });

      const response = await request(app).get(`/api/quota/${agentId}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'active');
      expect(response.body).toHaveProperty('lastActivity');
      expect(response.body.remaining).toBeLessThanOrEqual(response.body.limit);

      // Cleanup
      await redis.del(`ratelimit:agent:${agentId}`);
    });

    it('should show reduced quota after consuming tokens', async () => {
      const agentId = `${TEST_AGENT_ID}-consumed`;
      const tokensToConsume = 20;

      // Consume some tokens
      await request(app)
        .post('/api/request')
        .send({ agentId, tokens: tokensToConsume });

      const response = await request(app).get(`/api/quota/${agentId}`);

      expect(response.status).toBe(200);
      // Remaining should be less than limit (accounting for some refill)
      expect(response.body.remaining).toBeLessThanOrEqual(
        response.body.limit - tokensToConsume + 5, // +5 for potential refill
      );

      // Cleanup
      await redis.del(`ratelimit:agent:${agentId}`);
    });

    it('should return correct quota structure', async () => {
      const response = await request(app).get(`/api/quota/${TEST_AGENT_ID}`);

      expect(response.status).toBe(200);
      expect(typeof response.body.agentId).toBe('string');
      expect(typeof response.body.remaining).toBe('number');
      expect(typeof response.body.limit).toBe('number');
      expect(typeof response.body.rate).toBe('number');
      expect(typeof response.body.status).toBe('string');
    });
  });
});
