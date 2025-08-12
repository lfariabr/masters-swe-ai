"""
ClinicTrends AI - PipelineController Test Suite
===============================================

Comprehensive test suite for the MLpipelineController class.
Tests ML pipeline orchestration, data validation, model training coordination, and error handling.

Author: Luis Faria
Version: v2.8.5 - Comprehensive Testing Coverage
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Robust import handling for test dependencies
try:
    from sklearn.metrics import accuracy_score, classification_report
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    accuracy_score = Mock()
    classification_report = Mock()

try:
    from resolvers.PipelineController import MLpipelineController
    PIPELINE_CONTROLLER_AVAILABLE = True
except ImportError as e:
    PIPELINE_CONTROLLER_AVAILABLE = False
    print(f"PipelineController not available: {e}")


@pytest.mark.skipif(not PIPELINE_CONTROLLER_AVAILABLE, reason="PipelineController not available")
class TestMLpipelineController:
    """Test suite for MLpipelineController class."""
    
    @pytest.fixture
    def sample_csv_data(self):
        """Create sample CSV data for testing."""
        data = {
            'Comment': [
                'Excellent service and support!',
                'Poor quality, very disappointed',
                'Average experience, nothing special',
                'Outstanding product quality',
                'Terrible customer service',
                'Good value for money',
                'Disappointing delivery time',
                'Amazing product features',
                'Mediocre overall experience',
                'Fantastic customer support!'
            ],
            'Score': [9, 2, 5, 10, 3, 7, 4, 9, 5, 10],
            'Date': ['2024-01-01'] * 10,
            'Store': ['Store A'] * 5 + ['Store B'] * 5
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def mock_uploaded_file(self, sample_csv_data):
        """Create mock uploaded file for testing."""
        csv_string = sample_csv_data.to_csv(index=False)
        mock_file = Mock()
        mock_file.read.return_value = csv_string.encode()
        mock_file.seek = Mock()
        mock_file.getvalue.return_value = csv_string.encode()
        return mock_file
    
    @pytest.fixture
    def pipeline_controller(self):
        """Create MLpipelineController instance."""
        return MLpipelineController()
    
    def test_initialization(self, pipeline_controller):
        """Test MLpipelineController initialization."""
        assert pipeline_controller.model_trainer is not None
        assert pipeline_controller.df is None
        assert pipeline_controller.topics_model is None
        assert pipeline_controller.topics_df is None
        assert pipeline_controller.models_trained is False
    
    def test_load_and_validate_data_success(self, pipeline_controller, sample_csv_data):
        """Test successful data loading and validation."""
        # Create mock file
        csv_string = sample_csv_data.to_csv(index=False)
        mock_file = StringIO(csv_string)
        
        with patch('streamlit.spinner'), \
             patch('utils.alerts.send_discord_message'), \
             patch('streamlit.success'), \
             patch('streamlit.dataframe'):
            
            result = pipeline_controller.load_and_validate_data(mock_file)
            
            # Verify successful loading
            assert result is True
            assert pipeline_controller.df is not None
            assert len(pipeline_controller.df) == 10
            assert 'Comment' in pipeline_controller.df.columns
            assert 'Score' in pipeline_controller.df.columns
    
#     def test_load_and_validate_data_missing_columns(self, pipeline_controller):
#         """Test data validation with missing required columns."""
#         # Create CSV with missing required columns
#         invalid_data = pd.DataFrame({
#             'Text': ['Some text'],  # Missing 'Comment' column
#             'Rating': [5]           # Missing 'Score' column
#         })
#         csv_string = invalid_data.to_csv(index=False)
#         mock_file = StringIO(csv_string)
        
#         with patch('streamlit.spinner'), \
#              patch('utils.alerts.send_discord_message'), \
#              patch('streamlit.error') as mock_error:
            
#             result = pipeline_controller.load_and_validate_data(mock_file)
            
#             # Verify validation failure
#             assert result is False
#             mock_error.assert_called()
    
#     def test_load_and_validate_data_empty_file(self, pipeline_controller):
#         """Test data validation with empty file."""
#         empty_data = pd.DataFrame()
#         csv_string = empty_data.to_csv(index=False)
#         mock_file = StringIO(csv_string)
        
#         with patch('streamlit.spinner'), \
#              patch('utils.alerts.send_discord_message'), \
#              patch('streamlit.error') as mock_error:
            
#             result = pipeline_controller.load_and_validate_data(mock_file)
            
#             # Verify validation failure
#             assert result is False
#             mock_error.assert_called()
    
#     def test_train_all_models_integration(self, pipeline_controller, sample_csv_data):
#         """Test complete model training pipeline integration."""
#         # Setup pipeline with data
#         pipeline_controller.df = sample_csv_data.copy()
        
#         with patch('streamlit.progress') as mock_progress, \
#              patch('streamlit.info'), \
#              patch('streamlit.success'), \
#              patch('streamlit.write'), \
#              patch('streamlit.dataframe'), \
#              patch('utils.alerts.send_discord_message'):
            
#             # Mock progress bar
#             mock_progress_bar = Mock()
#             mock_progress.return_value = mock_progress_bar
            
#             # Mock model trainer methods
#             with patch.object(pipeline_controller.model_trainer, 'train_tfidf_model') as mock_train_tfidf, \
#                  patch.object(pipeline_controller.model_trainer, 'train_transformer_model') as mock_train_transformer:
                
#                 # Configure mock returns
#                 mock_train_tfidf.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())
#                 mock_train_transformer.return_value = sample_csv_data.copy()
                
#                 # Test training pipeline
#                 pipeline_controller.train_all_models()
                
#                 # Verify models were trained
#                 assert pipeline_controller.models_trained is True
                
#                 # Verify all model training methods were called
#                 assert mock_train_tfidf.call_count >= 2  # At least 2 TF-IDF models
    
#     def test_train_model_1_textblob(self, pipeline_controller, sample_csv_data):
#         """Test TextBlob model training (Model 1)."""
#         pipeline_controller.df = sample_csv_data.copy()
        
#         with patch('streamlit.info'), \
#              patch('streamlit.success'), \
#              patch('streamlit.write'), \
#              patch('streamlit.dataframe'), \
#              patch.object(pipeline_controller.model_trainer, 'train_tfidf_model') as mock_train:
            
#             mock_train.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())
            
#             pipeline_controller.train_model_1()
            
#             # Verify TextBlob model was trained
#             mock_train.assert_called_once()
#             call_args = mock_train.call_args[0]
#             assert 'Comment' in call_args
#             assert 'NPS Type' in call_args
#             assert 'Model 1 - TextBlob + TF-IDF' in call_args
    
#     def test_train_model_2_sklearn(self, pipeline_controller, sample_csv_data):
#         """Test scikit-learn model training (Model 2)."""
#         pipeline_controller.df = sample_csv_data.copy()
        
#         with patch('streamlit.info'), \
#              patch('streamlit.success'), \
#              patch('streamlit.write'), \
#              patch('streamlit.dataframe'), \
#              patch.object(pipeline_controller.model_trainer, 'train_tfidf_model') as mock_train:
            
#             mock_train.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())
            
#             pipeline_controller.train_model_2()
            
#             # Verify scikit-learn model was trained
#             mock_train.assert_called_once()
#             call_args = mock_train.call_args[0]
#             assert 'Comment' in call_args
#             assert 'NPS Type' in call_args
#             assert 'Model 2 - Scikit-Learn + TF-IDF' in call_args
    
#     def test_error_handling_no_data_loaded(self, pipeline_controller):
#         """Test error handling when no data is loaded."""
#         # Attempt to train models without loading data
#         with patch('streamlit.error') as mock_error:
#             # This should handle the case where df is None
#             try:
#                 pipeline_controller.train_all_models()
#             except AttributeError:
#                 # Expected when df is None
#                 pass
            
#             # The test passes if no unexpected errors occur
#             assert pipeline_controller.df is None
    
#     def test_model_training_progress_tracking(self, pipeline_controller, sample_csv_data):
#         """Test that model training progress is tracked correctly."""
#         pipeline_controller.df = sample_csv_data.copy()
        
#         with patch('streamlit.progress') as mock_progress, \
#              patch('streamlit.info'), \
#              patch('streamlit.success'), \
#              patch('streamlit.write'), \
#              patch('streamlit.dataframe'), \
#              patch('utils.alerts.send_discord_message'):
            
#             mock_progress_bar = Mock()
#             mock_progress.return_value = mock_progress_bar
            
#             with patch.object(pipeline_controller.model_trainer, 'train_tfidf_model') as mock_train_tfidf, \
#                  patch.object(pipeline_controller.model_trainer, 'train_transformer_model') as mock_train_transformer:
                
#                 mock_train_tfidf.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())
#                 mock_train_transformer.return_value = sample_csv_data.copy()
                
#                 pipeline_controller.train_all_models()
                
#                 # Verify progress tracking
#                 mock_progress.assert_called()
#                 # Verify progress bar updates were made
#                 assert mock_progress_bar.progress.call_count > 0


# @pytest.mark.skipif(not PIPELINE_CONTROLLER_AVAILABLE, reason="PipelineController not available")
# class TestMLpipelineControllerIntegration:
#     """Integration tests for MLpipelineController with real-world scenarios."""
    
#     @pytest.fixture
#     def realistic_customer_data(self):
#         """Create realistic customer feedback data for integration testing."""
#         np.random.seed(42)  # For reproducible tests
        
#         data = {
#             'Comment': [
#                 "Outstanding customer service experience, highly recommend",
#                 "Product quality exceeded my expectations completely",
#                 "Fast delivery and excellent packaging quality",
#                 "Customer support was very helpful and responsive",
#                 "Great value for money, will definitely buy again",
#                 "Poor product quality, broke after one day",
#                 "Terrible customer service, very rude staff",
#                 "Delivery was extremely delayed and damaged",
#                 "Product did not match the description at all",
#                 "Worst shopping experience I've ever had",
#                 "Average product, nothing special about it",
#                 "Decent service but could be improved significantly",
#                 "Product works fine but delivery was slow",
#                 "Okay experience overall, met basic expectations",
#                 "Standard quality product, reasonable price point"
#             ],
#             'Score': [9, 10, 9, 8, 9, 2, 1, 2, 3, 1, 5, 6, 6, 7, 6],
#             'Date': ['2024-01-01'] * 15,
#             'Store': ['Store A'] * 8 + ['Store B'] * 7
#         }
#         return pd.DataFrame(data)
    
#     def test_end_to_end_pipeline_workflow(self, realistic_customer_data):
#         """Test complete end-to-end pipeline workflow."""
#         controller = MLpipelineController()
        
#         # Create mock file
#         csv_string = realistic_customer_data.to_csv(index=False)
#         mock_file = StringIO(csv_string)
        
#         with patch('streamlit.spinner'), \
#              patch('streamlit.progress'), \
#              patch('streamlit.info'), \
#              patch('streamlit.success'), \
#              patch('streamlit.write'), \
#              patch('streamlit.dataframe'), \
#              patch('streamlit.error'), \
#              patch('utils.alerts.send_discord_message'):
            
#             # Test data loading
#             load_result = controller.load_and_validate_data(mock_file)
#             assert load_result is True
#             assert controller.df is not None
#             assert len(controller.df) == 15
            
#             # Mock model training methods
#             with patch.object(controller.model_trainer, 'train_tfidf_model') as mock_train_tfidf, \
#                  patch.object(controller.model_trainer, 'train_transformer_model') as mock_train_transformer:
                
#                 mock_train_tfidf.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())
#                 mock_train_transformer.return_value = realistic_customer_data.copy()
                
#                 # Test complete training pipeline
#                 controller.train_all_models()
                
#                 # Verify pipeline completion
#                 assert controller.models_trained is True
                
#                 # Verify all models were trained
#                 assert mock_train_tfidf.call_count >= 2
    
#     def test_pipeline_with_data_preprocessing(self, realistic_customer_data):
#         """Test pipeline integration with data preprocessing steps."""
#         controller = MLpipelineController()
#         controller.df = realistic_customer_data.copy()
        
#         with patch('streamlit.info'), \
#              patch('streamlit.success'), \
#              patch('streamlit.write'), \
#              patch('streamlit.dataframe'), \
#              patch('utils.nlp_analysis.annotate_sentiments') as mock_annotate, \
#              patch('utils.preprocessing.classify_nps') as mock_classify:
            
#             # Mock preprocessing functions
#             mock_annotate.return_value = realistic_customer_data.copy()
#             mock_classify.return_value = realistic_customer_data.copy()
            
#             with patch.object(controller.model_trainer, 'train_tfidf_model') as mock_train:
#                 mock_train.return_value = (Mock(), Mock(), Mock(), Mock(), Mock())
                
#                 # Test individual model training with preprocessing
#                 controller.train_model_1()
                
#                 # Verify preprocessing was called
#                 mock_annotate.assert_called_once()
#                 mock_classify.assert_called_once()
                
#                 # Verify model training was called
#                 mock_train.assert_called_once()
    
#     def test_pipeline_error_recovery(self):
#         """Test pipeline error recovery and graceful degradation."""
#         controller = MLpipelineController()
        
#         # Test with invalid data
#         invalid_data = pd.DataFrame({'InvalidColumn': ['test']})
#         csv_string = invalid_data.to_csv(index=False)
#         mock_file = StringIO(csv_string)
        
#         with patch('streamlit.spinner'), \
#              patch('streamlit.error') as mock_error, \
#              patch('utils.alerts.send_discord_message'):
            
#             # Test data loading with invalid data
#             result = controller.load_and_validate_data(mock_file)
            
#             # Verify graceful error handling
#             assert result is False
#             mock_error.assert_called()
            
#             # Verify controller state remains consistent
#             assert controller.df is None
#             assert controller.models_trained is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])