"""
ClinicTrends AI - BERTopicModel Test Suite
==========================================

Comprehensive test suite for the BERTopicModel functionality.
Tests topic modeling, embedding generation, and error handling.

Author: Luis Faria
Version: v2.8.5 - Comprehensive Testing Coverage
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Robust import handling for test dependencies
try:
    from resolvers.BERTopicModel import train_bertopic_model
    BERTOPIC_MODEL_AVAILABLE = True
except ImportError as e:
    BERTOPIC_MODEL_AVAILABLE = False
    print(f"BERTopicModel not available: {e}")

try:
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    BERTOPIC_DEPENDENCIES_AVAILABLE = True
except ImportError:
    BERTOPIC_DEPENDENCIES_AVAILABLE = False
    BERTopic = Mock()
    SentenceTransformer = Mock()


@pytest.mark.skipif(not BERTOPIC_MODEL_AVAILABLE, reason="BERTopicModel not available")
class TestBERTopicModel:
    """Test suite for BERTopicModel functionality."""
    
    @pytest.fixture
    def sample_comments(self):
        """Create sample comments for testing."""
        return pd.Series([
            "Excellent customer service and fast delivery",
            "Poor product quality, very disappointed",
            "Great value for money, highly recommend",
            "Terrible experience with customer support",
            "Outstanding product features and design",
            "Delivery was delayed, not satisfied",
            "Amazing user interface and experience",
            "Product broke after one week of use",
            "Fantastic overall experience with service",
            "Customer service was unhelpful and rude"
        ])
    
    @pytest.fixture
    def empty_comments(self):
        """Create empty/invalid comments for testing."""
        return pd.Series([None, "", "   ", None, ""])
    
    def test_train_bertopic_model_basic_functionality(self, sample_comments):
        """Test basic BERTopic model training functionality."""
        with patch('sentence_transformers.SentenceTransformer') as mock_st, \
             patch('bertopic.BERTopic') as mock_bertopic, \
             patch('streamlit.warning'), \
             patch('streamlit.stop'):
            
            # Mock SentenceTransformer
            mock_encoder = Mock()
            mock_embeddings = np.random.rand(len(sample_comments), 384)
            mock_encoder.encode.return_value = mock_embeddings
            mock_st.return_value = mock_encoder
            
            # Mock BERTopic
            mock_topic_model = Mock()
            mock_topics = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            mock_probs = np.random.rand(len(sample_comments))
            mock_topic_model.fit_transform.return_value = (mock_topics, mock_probs)
            mock_bertopic.return_value = mock_topic_model
            
            # Test the function
            result = train_bertopic_model(sample_comments)
            
            # Verify results
            assert result is not None
            topic_model, topics, probs, embeddings = result
            
            assert topic_model is not None
            assert topics is not None
            assert probs is not None
            assert embeddings is not None
            
            # Verify mocks were called correctly
            mock_st.assert_called_once_with("all-MiniLM-L6-v2")
            mock_encoder.encode.assert_called_once()
            mock_bertopic.assert_called_once_with(language="english")
            mock_topic_model.fit_transform.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])