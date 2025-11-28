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

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseEnvInt(process.env.REDIS_PORT, 6379, 'REDIS_PORT'),
  password: process.env.REDIS_PASSWORD || undefined,
  db: parseEnvInt(process.env.REDIS_DB, 0, 'REDIS_DB'),
  retryDelayOnFailover: 100,
  maxRetriesPerRequest: 3,
});

redis.on('connect', () => {
  console.log('✅ Connected to Redis');
});

redis.on('error', (err) => {
  console.error('❌ Redis connection error:', err.message);
});

export default redis;
