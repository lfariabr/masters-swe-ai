// src/routes/health.routes.ts
import { Router, Request, Response } from 'express';
import redis from '../db/redis.js';
import logger from '../utils/logger.js';

const router = Router();

// Health check endpoint
router.get('/', async (_req: Request, res: Response) => {
  try {
    const redisPing = await redis.ping();
    res.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      redis: redisPing === 'PONG' ? 'connected' : 'disconnected',
    });
  } catch (error: any) {
    logger.error('Health check failed', error);
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      redis: 'disconnected',
    });
  }
});

export default router;