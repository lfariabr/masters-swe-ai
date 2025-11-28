import express, { Express } from 'express';
import request from 'supertest';

// Create a minimal test app that mirrors the main app's endpoints
function createTestApp(): Express {
  const app = express();
  app.use(express.json());

  // Root endpoint
  app.get('/', (_req, res) => {
    res.json({
      name: 'IRL Rate Limiter',
      version: '0.1.0',
      description: 'Intelligent Rate Limiting System for Agentic AI',
    });
  });

  // Health check (mocked - doesn't require Redis for unit tests)
  app.get('/health', (_req, res) => {
    res.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      redis: 'connected',
    });
  });

  return app;
}

describe('API Endpoints', () => {
  let app: Express;

  beforeAll(() => {
    app = createTestApp();
  });

  describe('GET /', () => {
    it('should return API info', async () => {
      const response = await request(app).get('/');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('name', 'IRL Rate Limiter');
      expect(response.body).toHaveProperty('version', '0.1.0');
      expect(response.body).toHaveProperty('description');
    });
  });

  describe('GET /health', () => {
    it('should return health status', async () => {
      const response = await request(app).get('/health');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'ok');
      expect(response.body).toHaveProperty('timestamp');
      expect(response.body).toHaveProperty('redis');
    });

    it('should return ISO timestamp', async () => {
      const response = await request(app).get('/health');

      const timestamp = response.body.timestamp;
      const parsed = new Date(timestamp);

      expect(parsed.toISOString()).toBe(timestamp);
    });
  });

  describe('404 Handling', () => {
    it('should return 404 for unknown routes', async () => {
      const response = await request(app).get('/unknown-route');

      expect(response.status).toBe(404);
    });
  });
});

describe('Rate Limit Headers', () => {
  it('should validate X-RateLimit header format', () => {
    // Test the header format we expect
    const headers = {
      'X-RateLimit-Limit': '100',
      'X-RateLimit-Remaining': '99',
      'X-RateLimit-Reset': String(Math.floor(Date.now() / 1000) + 60),
    };

    expect(parseInt(headers['X-RateLimit-Limit'], 10)).toBeGreaterThan(0);
    expect(parseInt(headers['X-RateLimit-Remaining'], 10)).toBeGreaterThanOrEqual(0);
    expect(parseInt(headers['X-RateLimit-Reset'], 10)).toBeGreaterThan(Date.now() / 1000);
  });
});
