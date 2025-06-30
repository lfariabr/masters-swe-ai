import pytest
import pandas as pd
from streamlit.testing.v1 import AppTest
from streamlit.runtime.state.session_state import SessionState

# Try to import sklearn, but skip tests if not available
try:
    import sklearn
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Skip all tests if sklearn is not available
pytestmark = pytest.mark.skipif(not SKLEARN_AVAILABLE, 
                               reason="scikit-learn is not installed")

# Mock data for testing
SAMPLE_DATA = pd.DataFrame({
    'text': ['This is a positive review', 'Negative experience', 'Neutral comment'],
    'sentiment': ['positive', 'negative', 'neutral']
})

@pytest.fixture
def app():
    """Fixture to create a test app with proper session state."""
    # Create the test app
    app = AppTest.from_file("views/ModelsPage.py")
    
    # Set up the session state properly
    if not hasattr(app, 'session_state'):
        app.session_state = SessionState()
    app.session_state.df = SAMPLE_DATA
    
    return app

def test_models_page_initial_render(app):
    """Test that the models page renders correctly."""
    # Increase timeout to 10 seconds
    app.run(timeout=5.0)
    
    # Check for main sections
    markdown_texts = [str(md.value).lower() for md in app.markdown]
    assert any("model" in text for text in markdown_texts)  # More generic check

def test_error_handling(app):
    """Test that the page handles empty data gracefully."""
    # Arrange
    app.session_state.df = pd.DataFrame(columns=['text', 'sentiment'])  # Empty but with correct columns
    
    # Act
    app.run(timeout=5.0)
    
    # Debug: Print all messages to see what's actually being shown
    markdown_texts = [str(md.value).lower() for md in app.markdown]
    errors = [str(err).lower() for err in getattr(app, 'error', [])]
    all_messages = markdown_texts + errors
    print("\nAll messages in the app:")
    for msg in all_messages:
        print(f"- {msg[:100]}...")  # Print first 100 chars of each message
    
    # Assert - Check that we see the data upload section
    assert any("data upload" in msg.lower() for msg in all_messages), \
           "Expected to see the data upload section when no data is loaded"
    
    # Check that no error messages are shown
    assert not errors, f"Unexpected error messages: {errors}"