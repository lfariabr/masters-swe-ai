import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import redis from './db/redis.js';
import logger, { logRequest, logRateLimit } from './utils/logger.js';

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

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    logRequest(req.method, req.path, res.statusCode, duration, {
      ip: req.ip,
      userAgent: req.get('User-Agent'),
    });
  });
  next();
});

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
      logRateLimit(clientIP, 'blocked', current, limit);
      res.status(429).json({
        error: 'Too Many Requests',
        message: 'Rate limit exceeded. Please try again later.',
        retryAfter: 60,
      });
      return;
    }
    
    logRateLimit(clientIP, 'allowed', current, limit);
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
app.use((err: Error, req: Request, res: Response, _next: NextFunction) => {
  logger.error('Unhandled error', { error: err.message, stack: err.stack, path: req.path });
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message,
  });
});

// Server instance for graceful shutdown
let server: ReturnType<typeof app.listen> | null = null;

// Start server only when run directly (not when imported for tests)
const startServer = () => {
  server = app.listen(PORT, () => {
    logger.info(`🚀 IRL Server started`, { port: PORT });
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
  return server;
};

// Only start if this is the main module (not imported)
// Check if running via tsx/node directly vs being imported
if (process.env.NODE_ENV !== 'test' && require.main === module) {
  startServer();
}

// Graceful shutdown - properly drain connections before exiting
const shutdown = async (signal: string) => {
  logger.info(`Received ${signal}. Shutting down gracefully...`);

  // Stop accepting new connections and wait for existing ones to finish
  if (server) {
    await new Promise<void>((resolve, reject) => {
      server!.close((err) => {
        if (err) {
          logger.error('Error closing HTTP server', { error: err.message });
          reject(err);
        } else {
          logger.info('HTTP server closed');
          resolve();
        }
      });
    });
  }

  // Now close Redis connection
  try {
    await redis.quit();
    logger.info('Redis connection closed');
  } catch (err) {
    logger.error('Error closing Redis connection', {
      error: err instanceof Error ? err.message : 'Unknown error',
    });
  }

  process.exit(0);
};

process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));

export { app, redis, startServer };
