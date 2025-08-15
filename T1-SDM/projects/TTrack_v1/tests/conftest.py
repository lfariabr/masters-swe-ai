"""
Configuration file for pytest.
Contains fixtures and other test configurations.
"""
import pytest
from PyQt5.QtWidgets import QApplication

# Make sure QApplication is created only once per test session
@pytest.fixture(scope="session")
def qapp():
    """Fixture providing a QApplication instance for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

# Add command line options
def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption(
        "--run-slow", 
        action="store_true", 
        default=False, 
        help="run slow tests"
    )

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow to run"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on command line options."""
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
