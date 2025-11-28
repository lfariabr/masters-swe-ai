// Jest setup file
// This runs before each test file

import dotenv from 'dotenv';
import path from 'path';

// Load environment variables for tests
dotenv.config({ path: path.resolve(__dirname, '../.env') });

// Set test environment to prevent server from auto-starting
process.env.NODE_ENV = 'test';

// Increase timeout for integration tests
jest.setTimeout(10000);

// Suppress console output during tests (optional)
// Uncomment if you want quieter test output
// global.console = {
//   ...console,
//   log: jest.fn(),
//   info: jest.fn(),
//   debug: jest.fn(),
// };
