// src/routes/health.routes.ts
import { Router, Request, Response } from 'express';
import redis from '../db/redis.js';

const router = Router();

// Health check endpoint
router.get('/health', async (req: Request, res: Response) => {
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

export default router;