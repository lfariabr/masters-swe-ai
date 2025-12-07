// tests/globalTeardown.ts
// Global teardown for Jest - closes Redis connection exactly once after all tests
//
// Note: Due to Jest's module isolation, global teardown imports a fresh Redis client
// which may not be the same instance used during tests. We attempt to close it gracefully
// but silently ignore failures since the actual test connections are already closed.

import redis from '../src/db/redis';

export default async function globalTeardown(): Promise<void> {
  // Check if Redis connection is open before attempting to close
  // ioredis status values: 'wait', 'connecting', 'connect', 'ready', 'close', 'reconnecting', 'end'
  const openStatuses = ['connecting', 'connect', 'ready', 'reconnecting'];

  if (openStatuses.includes(redis.status)) {
    try {
      await redis.quit();
      // Silently succeed - no need to log in normal operation
    } catch {
      // Silently ignore - connection may already be closed by forceExit or test cleanup
      // This is expected behavior when Jest uses forceExit: true
    }
  }
  // If already closed, nothing to do
}
