import winston from 'winston';
import dotenv from 'dotenv';

dotenv.config();

const { combine, timestamp, printf, colorize, errors } = winston.format;

// Custom log format for structured logging
const logFormat = printf(({ level, message, timestamp, ...metadata }) => {
  let msg = `${timestamp} [${level}]: ${message}`;

  // Add metadata if present (structured logging)
  if (Object.keys(metadata).length > 0) {
    msg += ` ${JSON.stringify(metadata)}`;
  }

  return msg;
});

// Create Winston logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: combine(
    errors({ stack: true }), // Handle Error objects
    timestamp({ format: 'YYYY-MM-DD HH:mm:ss' })
  ),
  defaultMeta: { service: 'irl-rate-limiter' },
  transports: [
    // Console transport with colors for development
    new winston.transports.Console({
      format: combine(
        colorize({ all: true }),
        logFormat
      ),
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
  logger.info('HTTP Request', {
    method,
    path,
    statusCode,
    duration: `${duration}ms`,
    ...metadata,
  });
};

export const logRateLimit = (
  clientId: string,
  action: 'allowed' | 'blocked',
  current: number,
  limit: number,
  metadata?: Record<string, unknown>
) => {
  const level = action === 'blocked' ? 'warn' : 'info';
  logger[level]('Rate Limit Decision', {
    clientId,
    action,
    current,
    limit,
    remaining: Math.max(0, limit - current),
    ...metadata,
  });
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
