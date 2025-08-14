---

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov=utils --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov=utils --cov-report=html
```

### Code Quality

```bash
# Run linter
flake8 app/ utils/ tests/

# Type checking
mypy app/ utils/ tests/

# Format code
black app/ utils/ tests/
isort app/ utils/ tests/
```

### Using Makefile

For convenience, a Makefile is provided with common development tasks:

```bash
make install-test    # Install test dependencies
make test           # Run all tests
make test-cov       # Run tests with coverage
make test-html      # Generate HTML coverage report
make lint           # Run linter
make type-check     # Run type checking
make format         # Format code
make check          # Run all checks (tests, linting, type checking)
```

---
