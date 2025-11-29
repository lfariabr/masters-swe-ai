// src/routes/testRedisRouter.ts
import { Router, Request, Response } from 'express';
import redis from '../db/redis.js';
import logger from '../utils/logger.js';

const router = Router();

router.get('/', async (_req: Request, res: Response) => {
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
  } catch (error: any) {
    logger.error('Redis test endpoint failed', error);
    res.status(500).json({
      success: false,
      error: error.message,
    });
  }
});

export default router;