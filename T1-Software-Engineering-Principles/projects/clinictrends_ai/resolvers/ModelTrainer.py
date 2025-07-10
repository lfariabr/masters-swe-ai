import numpy as np
import pandas as pd
import streamlit as st
import time
from typing import Any, Dict, Optional, Tuple

# ML/AI Libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

# Optional: Transformers
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class ModelTrainer:
    """
    Enterprise-grade ML model training and evaluation class.
    Implements standardized training pipelines with comprehensive metrics.
    """
    
    def __init__(self):
        self.models = {}
        self.vectorizers = {}
        self.metrics = {}
        
    def train_tfidf_model(self, df: pd.DataFrame, feature_column: str, 
                         target_column: str, model_name: str, score_column: str = None) -> Tuple[Any, Any, Any, Any, Any]:
        """
        Train TF-IDF (Term Frequency-Inverse Document Frequency) + Logistic Regression model with standardized pipeline.
        
        Args:
            df: Training dataframe
            feature_column: Column containing text features
            target_column: Column containing target labels
            model_name: Unique identifier for the model
            
        Returns:
            Tuple of (trained_model, fitted_vectorizer, X_test, y_test, y_pred)
        """
        try:
            # ----- new, td-idf deep dive --------
            # Before vectorization, analyze comment sizes
            with st.container(border=True):
                with st.container(border=True):
                    comment_stats = self.analyze_comment_sizes(df, feature_column)
                    st.write("Comment Size Statistics:", comment_stats)

                # Find optimal feature count
                with st.container(border=True):
                    optimal_features = self.find_optimal_features(df, feature_column, target_column)
                    st.write(f"Using optimal feature count: {optimal_features}")
            # ----- new, td-idf deep dive --------
            
            # Create vectorizer with optimal feature count
            vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=optimal_features, # was hardcoded to 5000 ... now using optimal feature count from cross-validation
                ngram_range=(1, 2),  # Include bigrams for better context
                min_df=2,  # Ignore terms that appear in less than 2 documents
                max_df=0.95  # Ignore terms that appear in more than 95% of documents
            )

            # If you have a score column, use it as an additional feature
            if score_column and score_column in df.columns:
                X = self.create_combined_features(df, feature_column, score_column, vectorizer)
            else:
                X = vectorizer.fit_transform(df[feature_column].fillna(''))

            # model evaluation
            # scenario1 model try to find particular word from a page (finds 9/10. Precision 90%) [classification problem - always get accuracy]
            # scenario2 model try to understand the severity of the problem [regression problem - single class]

            # 3 classes of classification: Promoter, Neutral, Detractor
            # 2 classes of classification: Positive or Negative
            
            # Get target values
            y = df[target_column] # output: Promoter, Neutral, Detractor
            
            # Train-test split with stratification
            X_train, X_test, y_train, y_test = train_test_split( # X refers to the feature and Y refers to the label that we want it to find
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            # overfit or underfit - check more #TODO
            # Model training
            model = LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'  # Handle class imbalance
            )
            
            start_time = time.time()
            model.fit(X_train, y_train)
            training_time = time.time() - start_time
            
            # Store model artifacts
            self.models[model_name] = model
            self.vectorizers[model_name] = vectorizer
            
            # Calculate comprehensive metrics
            y_pred = model.predict(X_test)
            self.metrics[model_name] = self._calculate_metrics(
                y_test, y_pred, model_name, training_time
            )
            
            return model, vectorizer, X_test, y_test, y_pred
            
        except Exception as e:
            st.error(f"❌ Error training {model_name}: {str(e)}")
            return None, None, None, None, None
    
    def find_optimal_features(self, df: pd.DataFrame, feature_column: str, target_column: str):
        """
        Find the optimal number of features for the given dataset.
        
        Args:
            df: Input dataframe
            feature_column: Column containing text features
            target_column: Column containing target labels
            
        Returns:
            int: Optimal number of features
        """    
        # Define parameter grid - for Pipeline, use format: step_name__parameter_name
        param_grid = {
            'vectorizer__max_features': [100, 300, 500, 700, 1000],
        }

        # Create pipeline
        from sklearn.pipeline import Pipeline
        pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(
                stop_words="english", 
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
            )),
            ('classifier', LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'
            ))
        ])
    
        # Initialize GridSearchCV
        grid_search = GridSearchCV(
            pipeline,
            param_grid=param_grid,
            cv=5,
            scoring='f1_weighted',
            n_jobs=-1,
        )

        X = df[feature_column].fillna('')
        y = df[target_column]

        # Fit GridSearchCV
        grid_search.fit(X, y)

        st.write(f"Best parameters: {grid_search.best_params_}")
        st.write(f"Best score: {grid_search.best_score_}")
        
        # Return the optimal feature count
        return grid_search.best_params_['vectorizer__max_features']

    def create_combined_features(self, df, feature_column, score_column, vectorizer):
        """Combine text features with numerical score feature"""
        # Get TF-IDF features
        text_features = vectorizer.transform(df[feature_column].fillna(''))
        
        # Get score feature and reshape for concatenation
        score_features = df[score_column].values.reshape(-1, 1)
        
        # Combine features
        from scipy.sparse import hstack
        combined_features = hstack([text_features, score_features])
        
        return combined_features

    def analyze_comment_sizes(self, df, feature_column):
        """Analyze the size distribution of comments"""
        # Calculate token counts
        token_counts = df[feature_column].fillna('').apply(lambda x: len(x.split()))
        
        # Calculate statistics
        stats = {
            'mean_tokens': token_counts.mean(),
            'median_tokens': token_counts.median(),
            'min_tokens': token_counts.min(),
            'max_tokens': token_counts.max(),
            'std_tokens': token_counts.std()
        }
    
        return stats
    
    def train_transformer_model(self, df: pd.DataFrame, feature_column: str, 
                              model_name: str) -> Optional[pd.DataFrame]:
        """
        Apply pre-trained transformer model for sentiment analysis.
        
        Args:
            df: Input dataframe
            feature_column: Column containing text features
            model_name: Unique identifier for the model
            
        Returns:
            Optional[pd.DataFrame]: Transformed dataframe with sentiment scores
        
        Note: This is a prototype implementation as noted in README.
        """
        if not TRANSFORMERS_AVAILABLE:
            st.warning(f"⚠️ Transformers not available for {model_name}")
            return None
            
        try:
            sentiment_pipeline = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=False
            )
            
            # Process in batches to avoid memory issues
            batch_size = 100
            results = []
            
            progress_bar = st.progress(0)
            total_batches = len(df) // batch_size + 1

            start_time = time.time()
            
            for i in range(0, len(df), batch_size):
                batch = df[feature_column].iloc[i:i+batch_size].fillna('').tolist()
                batch_results = sentiment_pipeline(batch, truncation=True)
                results.extend(batch_results)
                progress_bar.progress((i // batch_size + 1) / total_batches)
            
            training_time = time.time() - start_time
            progress_bar.empty()
            
            # Convert results to dataframe format
            df_copy = df.copy()
            df_copy["HF_Label"] = [res["label"] for res in results]
            df_copy["HF_Score"] = [res["score"] for res in results]

            # Calculate metrics if ground truth exists
            if "Sentiment" in df.columns:
                y_true = df["Sentiment"]
                y_pred = df_copy["HF_Label"]
                
                accuracy = accuracy_score(y_true, y_pred)
                precision, recall, f1, _ = precision_recall_fscore_support(
                    y_true, y_pred, average="weighted", zero_division=0
                )
                
                class_counts = dict(pd.Series(y_pred).value_counts())
                
                self.metrics[model_name] = {
                    "Model": model_name,
                    "Accuracy": round(accuracy, 4),
                    "Precision": round(precision, 4),
                    "Recall": round(recall, 4),
                    "F1-Score": round(f1, 4),
                    "Training_Time": round(training_time, 2),
                    "Class_Distribution": class_counts,
                    "Total_Predictions": len(df_copy)
                }
            else:
                # No ground truth to compare
                self.metrics[model_name] = {
                    "Model": model_name,
                    "Accuracy": None,
                    "Precision": None,
                    "Recall": None,
                    "F1-Score": None,
                    "Training_Time": round(training_time, 2),
                    "Class_Distribution": None,
                    "Total_Predictions": len(df_copy)
                }
            
            return df_copy
            
        except Exception as e:
            st.error(f"❌ Error with transformer model {model_name}: {str(e)}")
            return None
    
    def _calculate_metrics(self, y_true, y_pred, model_name: str, 
                          training_time: float) -> Dict[str, Any]:
        """Calculate comprehensive model performance metrics."""
        try:
            # Basic metrics
            accuracy = accuracy_score(y_true, y_pred)
            precision, recall, f1, support = precision_recall_fscore_support(
                y_true, y_pred, average='weighted', zero_division=0
            )
            
            # Class distribution
            unique_labels = np.unique(np.concatenate([y_true, y_pred]))
            class_counts = {label: sum(y_pred == label) for label in unique_labels}
            
            return {
                "Model": model_name,
                "Accuracy": round(accuracy, 4),
                "Precision": round(precision, 4),
                "Recall": round(recall, 4),
                "F1-Score": round(f1, 4),
                "Training_Time": round(training_time, 2),
                "Class_Distribution": class_counts,
                "Total_Predictions": len(y_pred)
            }
        except Exception as e:
            st.error(f"Error calculating metrics for {model_name}: {str(e)}")
            return {}


# Module exports
__all__ = ['ModelTrainer']