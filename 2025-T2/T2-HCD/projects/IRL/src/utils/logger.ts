import winston from 'winston';
import dotenv from 'dotenv';

dotenv.config();

const { combine, timestamp, printf, colorize, errors } = winston.format;

// Status code color helper
const getStatusColor = (statusCode: number): string => {
  if (statusCode >= 500) return '\x1b[31m'; // Red
  if (statusCode >= 400) return '\x1b[33m'; // Yellow
  if (statusCode >= 300) return '\x1b[36m'; // Cyan
  if (statusCode >= 200) return '\x1b[32m'; // Green
  return '\x1b[0m'; // Reset
};

const RESET = '\x1b[0m';
const DIM = '\x1b[2m';
const BOLD = '\x1b[1m';

// Custom log format for better terminal visibility
const logFormat = printf(({ level, message, timestamp, ...metadata }) => {
  const { service, ...rest } = metadata;

  const metaString = Object.keys(rest).length > 0 
    ? `\n${JSON.stringify(rest, null, 2)}` 
    : '';
  
  return `${timestamp || ''} [${level}] ${message}${metaString}`;
});

// Create Winston logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: combine(
    errors({ stack: true }), // Handle Error objects
    timestamp({ format: 'HH:mm:ss' }) // Shorter timestamp for dev
  ),
  defaultMeta: { service: 'irl-rate-limiter' },
  transports: [
    // Console transport with colors for development
    new winston.transports.Console({
      format: combine(colorize({ all: true }), logFormat),
    }),
  ],
});

// Add file transport in production
if (process.env.NODE_ENV === 'production') {
  logger.add(
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
      format: combine(timestamp(), winston.format.json()),
    })
  );
  logger.add(
    new winston.transports.File({
      filename: 'logs/combined.log',
      format: combine(timestamp(), winston.format.json()),
    })
  );
}

// Helper methods for structured logging
export const logRequest = (
  method: string,
  path: string,
  statusCode: number,
  duration: number,
  metadata?: Record<string, unknown>
) => {
  const statusColor = getStatusColor(statusCode);
  const methodPad = method.padEnd(6);
  const emoji = statusCode >= 400 ? '❌' : statusCode >= 300 ? '↪️ ' : '✓';

  // Clean, scannable format: ✓ GET    /health 200 12ms
  logger.info(
    `${emoji} ${methodPad} ${path} ${statusColor}${statusCode}${RESET} ${DIM}${duration}ms${RESET}`
  );
};

export const logRateLimit = (
  clientId: string,
  action: 'allowed' | 'blocked' | 'error',
  current: number,
  limit: number,
  metadata?: Record<string, unknown>
) => {
  const emoji = action === 'blocked' ? '🚫' : action === 'error' ? '⚠️' : '✅';
  const remaining = Math.max(0, limit - current);

  if (action === 'blocked') {
    logger.warn(`${emoji} Rate limit BLOCKED ${clientId} (${current}/${limit})`);
  } else if (action === 'error') {
    logger.error(`${emoji} Rate limit ERROR ${clientId} (${current}/${limit})`);
  } else {
    logger.info(`${emoji} Rate limit OK ${DIM}${remaining}/${limit} remaining${RESET}`);
  }
};

export const logRedisOperation = (
  operation: string,
  success: boolean,
  duration?: number,
  metadata?: Record<string, unknown>
) => {
  const level = success ? 'debug' : 'error';
  logger[level]('Redis Operation', {
    operation,
    success,
    duration: duration ? `${duration}ms` : undefined,
    ...metadata,
  });
};

export default logger;
