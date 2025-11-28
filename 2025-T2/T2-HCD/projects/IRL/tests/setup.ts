// Jest setup file
// This runs before each test file

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

// Clean up after all tests
afterAll(async () => {
  // Give time for any async operations to complete
  await new Promise((resolve) => setTimeout(resolve, 100));
});
