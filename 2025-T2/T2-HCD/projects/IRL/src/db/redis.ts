import Redis from 'ioredis';
import dotenv from 'dotenv';

dotenv.config();

const parseEnvInt = (
  envValue: string | undefined, 
  defaultValue: number,
  name: string
): number => {
  const raw = envValue ?? defaultValue.toString();
  const parsed = Number.parseInt(raw, 10);
  if (Number.isNaN(parsed) || parsed < 0) {
    throw new Error(`Invalid value for ${name}: ${raw}`);
  }
  return parsed;
};

const redisPassword = process.env.REDIS_PASSWORD;
if (!redisPassword) {
  throw new Error('REDIS_PASSWORD is required (see docker-compose.yml/.env)');
}

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseEnvInt(process.env.REDIS_PORT, 6379, 'REDIS_PORT'),
  password: process.env.REDIS_PASSWORD || undefined,
  db: parseEnvInt(process.env.REDIS_DB, 0, 'REDIS_DB'),
  maxRetriesPerRequest: 3,
  enableOfflineQueue: false, // Don't queue commands when disconnected
  connectTimeout: 10000, // 10 second connection timeout
  
  retryStrategy: (times: number) => {
    // 'times' = number of connection attempts
    // Return: delay in milliseconds
    // Return null/undefined to stop retrying

    // Exponential backoff: delay = min(times * 50, 2000)
    const delay = Math.min(times * 50, 2000);
    return delay;
  },
});

redis.on('connect', () => {
  console.log('✅ Connected to Redis');
});

redis.on('error', (err) => {
  console.error('❌ Redis connection error:', err.message);
});

// Helper function to wait for Redis to be ready
export const waitForRedis = (): Promise<void> => {
  return new Promise((resolve, reject) => {
    if (redis.status === 'ready') {
      resolve();
      return;
    }

    let timeoutId: NodeJS.Timeout;

    const cleanup = () => {
      clearTimeout(timeoutId);
      redis.off('ready', onReady);
      redis.off('error', onError);
    };

    const onReady = () => {
      cleanup();
      resolve();
    };

    const onError = (err: Error) => {
      cleanup();
      reject(err);
    };

    redis.once('ready', onReady);
    redis.once('error', onError);

    // Timeout after 5 seconds
    timeoutId = setTimeout(() => {
      cleanup();
      reject(new Error('Redis connection timeout'));
    }, 5000);
  });
};

export default redis;
