import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import redis from './db/redis.js';
import logger, { logRequest, logRateLimit } from './utils/logger.js';

import rateLimitRouter from './routes/testRateLimit.js';
import healthRouter from './routes/health.routes.js';
import testRedisRouter from './routes/testRedisRouter.js';
import quotaRouter from './routes/quota.routes.js';

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

app.use('/api', rateLimitRouter);
app.use('/api', quotaRouter);
app.use('/test-redis', testRedisRouter);
app.use('/health', healthRouter);

// Root endpoint
app.get('/', (_req: Request, res: Response) => {
  res.json({
    name: 'IRL - Intelligent Rate Limiter',
    version: '0.1.0',
    endpoints: {
      health: '/health',
      testRedis: '/test-redis',
      testRateLimit: '/api/test-rate-limit',
      request: '/api/request',
      quota: '/api/quota/:agentId',
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
  GET /api/test-rate-limit - Test rate limiting
  POST /api/request - Request access (consumes token)
  GET /api/quota/:agentId - Check remaining quota
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
