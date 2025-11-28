import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import redis from './db/redis.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Trust proxy for proper client IP behind load balancers/proxies
app.set('trust proxy', true);

// Middleware
app.use(cors({
  origin: '*', // Adjust as needed for security
  // process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
}));
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

// Lua script for atomic rate limiting: INCR + conditional EXPIRE
const RATE_LIMIT_SCRIPT = `
  local current = redis.call('INCR', KEYS[1])
  if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
  end
  return current
`;

// Basic rate limit test endpoint (placeholder for Phase 1)
app.get('/api/test', async (req: Request, res: Response) => {
  const clientIP = req.ip || 'unknown';
  const key = `ratelimit:${clientIP}`;
  const windowSeconds = 60;
  
  try {
    // Atomic increment + expire using Lua script (no race condition)
    const current = await redis.eval(RATE_LIMIT_SCRIPT, 1, key, windowSeconds) as number;
    
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
// # Consider using a proper logging library like pino or winston for production
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
const shutdown = async (signal: string) => {
  console.log(`Received ${signal}. Shutting down gracefully...`);
  await redis.quit();
  process.exit(0);
};
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

export default app;
