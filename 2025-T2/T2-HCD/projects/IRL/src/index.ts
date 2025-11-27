import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import redis from './db/redis.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', async (req: Request, res: Response) => {
  try {
    const redisPing = await redis.ping();
    res.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      redis: redisPing === 'PONG' ? 'connected' : 'disconnected',
    });
  } catch (error) {
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      redis: 'disconnected',
    });
  }
});

// Test Redis endpoint
app.get('/test-redis', async (req: Request, res: Response) => {
  try {
    // Set a test value
    await redis.set('test:key', 'Hello from IRL!', 'EX', 60);
    
    // Get the value back
    const value = await redis.get('test:key');
    
    // Get Redis info
    const info = await redis.info('server');
    const redisVersion = info.match(/redis_version:(.+)/)?.[1]?.trim();
    
    res.json({
      success: true,
      message: 'Redis is working!',
      testValue: value,
      redisVersion,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// Basic rate limit test endpoint (placeholder for Phase 1)
app.get('/api/test', async (req: Request, res: Response) => {
  const clientIP = req.ip || 'unknown';
  const key = `ratelimit:${clientIP}`;
  
  try {
    const current = await redis.incr(key);
    
    // Set expiry on first request
    if (current === 1) {
      await redis.expire(key, 60); // 1 minute window
    }
    
    const limit = parseInt(process.env.DEFAULT_RATE_LIMIT || '100');
    const remaining = Math.max(0, limit - current);
    
    // Set rate limit headers
    res.set({
      'X-RateLimit-Limit': limit.toString(),
      'X-RateLimit-Remaining': remaining.toString(),
      'X-RateLimit-Reset': (Math.floor(Date.now() / 1000) + 60).toString(),
    });
    
    if (current > limit) {
      res.status(429).json({
        error: 'Too Many Requests',
        message: 'Rate limit exceeded. Please try again later.',
        retryAfter: 60,
      });
      return;
    }
    
    res.json({
      message: 'Request successful!',
      requestNumber: current,
      remaining,
      limit,
    });
  } catch (error) {
    res.status(500).json({
      error: 'Internal Server Error',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  res.json({
    name: 'IRL - Intelligent Rate Limiter',
    version: '0.1.0',
    endpoints: {
      health: '/health',
      testRedis: '/test-redis',
      testRateLimit: '/api/test',
    },
  });
});

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err.message);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message,
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
🚀 IRL Server running on http://localhost:${PORT}
📊 Redis Commander at http://localhost:8081 (if using docker-compose)

Available endpoints:
  GET /         - API info
  GET /health   - Health check
  GET /test-redis - Test Redis connection
  GET /api/test - Test rate limiting
  `);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('Shutting down gracefully...');
  await redis.quit();
  process.exit(0);
});

export default app;
