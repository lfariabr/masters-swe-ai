"""
Pytest configuration and shared fixtures for ClinicTrends AI tests.
"""
import pytest
import pandas as pd
from pathlib import Path
import sys
import os

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Sample test data
SAMPLE_DATA = {
    'feedback': [
        'Great service!',
        'Not satisfied with the wait time.',
        'The doctor was very professional.',
        'Could be better.',
        'Excellent experience overall.'
    ],
    'rating': [5, 2, 4, 3, 5],
    'sentiment': ['positive', 'negative', 'positive', 'negative', 'positive']
}

@pytest.fixture(scope="session")
def sample_dataframe():
    """Return a sample DataFrame for testing."""
    return pd.DataFrame(SAMPLE_DATA)

@pytest.fixture(scope="session")
def test_data_path(tmp_path_factory):
    """Create a temporary test CSV file and return its path."""
    df = pd.DataFrame(SAMPLE_DATA)
    path = tmp_path_factory.mktemp("data") / "test_data.csv"
    df.to_csv(path, index=False)
    return path
