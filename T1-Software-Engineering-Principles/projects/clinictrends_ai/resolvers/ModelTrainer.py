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
from sklearn.pipeline import Pipeline
from scipy.sparse import hstack

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class ModelTrainer:
    """
    ML model training and evaluation class.
    Implements standardized training pipelines with comprehensive metrics.
    """
    
    def __init__(self):
        self.models = {}
        self.vectorizers = {}
        self.metrics = {}
        
    def train_tfidf_model(self, 
                          df: pd.DataFrame, 
                          feature_column: str, 
                          target_column: str, 
                          model_name: str, 
                          score_column: str = None) -> Tuple[Any, Any, Any, Any, Any]:
        """
        Train TF-IDF (Term Frequency-Inverse Document Frequency) 
        + Logistic Regression model with standardized pipeline.
        
        Uses a three-way split (train/validation/test) 
        for robust model evaluation and early detection of overfitting.
        
        Args:
            df: Training dataframe
            feature_column: Column containing text features
            target_column: Column containing target labels
            model_name: Unique identifier for the model
            score_column: Optional column containing numerical scores to use as additional features
            
        Returns:
            Tuple of (trained_model, fitted_vectorizer, X_test, y_test, y_pred)
        """
        try:
            # **v2.3.0** - `feature/tf-idf-deep-dive`
            #   Before vectorization, we analyze comment sizes
            #   Then we found optimal feature count
            comment_stats = self.analyze_comment_sizes(df, feature_column)

            # **v2.6.1** - `feature/dynamic-hyperparameter-injection`
            #   Here we changed the return of find_optimal_features
            #   to return the best_params dictionary and use it to set the vectorizer

            best_params = self.find_optimal_features(df, feature_column, target_column) 
            optimal_features = best_params['vectorizer__max_features']
            
            # Create vectorizer with optimal feature count
            vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=optimal_features, # was hardcoded to 5000 ... now uses optimal feature count from cross-validation
                ngram_range=(1, 2), 
                min_df=2,  # Ignore terms that appear in less than 2 documents
                max_df=0.95  # Ignore terms that appear in more than 95% of documents
            )

            # Using score column as additional feature
            if score_column and score_column in df.columns:
                X = self.create_combined_features(df, feature_column, score_column, vectorizer)
            else:
                X = vectorizer.fit_transform(df[feature_column].fillna(''))

            # Get TARGET values
            y = df[target_column] # output: Promoter, Neutral, Detractor
            
            # **v2.5.0** - `feature/train-validation-test-split`
            #   Adds three-way split: train (60%), validation (20%), test (20%)
            #   Step 1: First split - separate test set (80/20)
            X_temp, X_test, y_temp, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Step 2: Split the remaining data into train and validation (75/25 = 60/20 of original)
            X_train, X_val, y_train, y_val = train_test_split(
                X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
            )
            
            # Get number of samples using shape[0] to handle sparse matrices
            train_samples = X_train.shape[0] if hasattr(X_train, 'shape') else len(X_train)
            val_samples = X_val.shape[0] if hasattr(X_val, 'shape') else len(X_val)
            test_samples = X_test.shape[0] if hasattr(X_test, 'shape') else len(X_test)
                        
            # Distribution analysis to ensure stratification worked properly
            train_dist = pd.Series(y_train).value_counts(normalize=True)
            val_dist = pd.Series(y_val).value_counts(normalize=True)
            test_dist = pd.Series(y_test).value_counts(normalize=True)
            
            dist_df = pd.DataFrame({
                'Train %': train_dist * 100,
                'Validation %': val_dist * 100,
                'Test %': test_dist * 100
            })
            
            model = LogisticRegression(
                ## **v2.4.0** - `feature/tf-idf-iteration-check`
                #   max_iter=100, # was hardcoded to 1000. Now using calculated max_iter
                max_iter=best_params['classifier__max_iter'],
                random_state=42,
                class_weight='balanced',

                ## **v2.6.0** - `feature/logreg-hyperparam-tuning`
                #   These params were hardcoded before
                #   Now using best_params from GridSearchCV
                #   C=10.0,
                #   penalty='l2',
                #   solver='lbfgs',
                #   multi_class='ovr',

                ## **v2.6.1** - `feature/logreg-hyperparam-tuning`
                #   removing hardcoded values
                C=best_params['classifier__C'],
                penalty=best_params['classifier__penalty'],
                solver=best_params['classifier__solver'],
                multi_class=best_params['classifier__multi_class'],
            )
            
            start_time = time.time()
            model.fit(X_train, y_train)
            training_time = time.time() - start_time

            n_iter = model.n_iter_[0]
            # print(f"Iterations until convergence for {model_name}: {n_iter}")
            # st.write(f"Iterations until convergence for {model_name}: {n_iter}")
            ## **v2.4.0** - `feature/tf-idf-iteration-check`
            
            # Store model artifacts
            self.models[model_name] = model
            self.vectorizers[model_name] = vectorizer
            
            # **v2.5.0** - `feature/train-validation-test-split`
            #   Evaluate on all 3 splits we've implemented
            y_train_pred = model.predict(X_train)
            y_val_pred = model.predict(X_val)
            y_test_pred = model.predict(X_test)
            
            #   Calculate metrics for all splits
            train_metrics = self._calculate_split_metrics(y_train, y_train_pred, "Train")
            val_metrics = self._calculate_split_metrics(y_val, y_val_pred, "Validation")
            test_metrics = self._calculate_split_metrics(y_test, y_test_pred, "Test")
            
            #   Combine metrics into a single dataframe for comparison
            metrics_df = pd.DataFrame([train_metrics, val_metrics, test_metrics])
            
            #   Check for overfitting
            acc_drop_train_val = train_metrics["Accuracy"] - val_metrics["Accuracy"]
            acc_drop_val_test = val_metrics["Accuracy"] - test_metrics["Accuracy"]
            f1_drop_train_val = train_metrics["F1-Score"] - val_metrics["F1-Score"]
            
            #   Store comprehensive metrics using test set (for backward compatibility)
            self.metrics[model_name] = self._calculate_metrics(
                y_test, y_test_pred, model_name, training_time
            )
            
            return model, vectorizer, X_test, y_test, y_test_pred
            
        except Exception as e:
            st.error(f"❌ Error training {model_name}: {str(e)}")
            return None, None, None, None, None
    
    def find_optimal_features(
                            self, 
                            df: pd.DataFrame, 
                            feature_column: str, 
                            target_column: str):
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
            
            ## -- v2.6.0 - `feature/logreg-hyperparam-tuning` 
            ## hardcoding for starting point
            'classifier__C': [0.1, 1.0, 10.0], # how strict or flexible the model is: range from 0.001 to 100
            'classifier__penalty': ['l2'], # type of regularization: l1, l2, elasticnet, none
            'classifier__solver': ['lbfgs'], # algorithm to use: lbfgs, newton-cg, liblinear, sag, saga
            'classifier__multi_class': ['ovr', 'multinomial'], # all vs one or multinomial
            'classifier__max_iter': [100, 300, 500], # maximum number of iterations, was 1000 now 100 because mean_token_length is 19 and standard token is 34
        }

        # Create pipeline
        pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(
                stop_words="english", 
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
            )),
            ('classifier', LogisticRegression(
                # max_iter removed because it is now in param_grid
                # max_iter=100, # maximum number of iterations, was 1000 now 100 because mean_token_length is 19 and standard token is 34
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
            verbose=1
        )

        X = df[feature_column].fillna('')
        y = df[target_column]

        # Fit GridSearchCV
        grid_search.fit(X, y)

        # Return the optimal feature count
        # **v2.6.1** - `feature/dynamic-hyperparameter-injection`
        #   We changed the return of this function to return the best_params_ instead of just the max_features
        return grid_search.best_params_ #['vectorizer__max_features']

    def create_combined_features(self, df, feature_column, score_column, vectorizer):
        """
        Combine text features with numerical score feature
        """
        # Get TF-IDF features
        text_features = vectorizer.transform(df[feature_column].fillna(''))
        # Get score feature and reshape for concatenation
        score_features = df[score_column].values.reshape(-1, 1)
        # Combine features
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
            # Fix for PyTorch device placement issues
            import torch
            
            # Force CPU usage to avoid device placement issues
            device = "cpu"
            
            # Initialize pipeline with explicit device and model configuration
            sentiment_pipeline = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=False,
                device=-1,  # Force CPU usage (-1 means CPU, 0+ means GPU)
                torch_dtype=torch.float32  # Explicit dtype to avoid meta tensor issues
            )
            
            # Process in smaller batches to avoid memory issues
            batch_size = 50  # Reduced batch size for stability
            results = []
            
            progress_bar = st.progress(0)
            total_batches = len(df) // batch_size + 1

            start_time = time.time()
            
            for i in range(0, len(df), batch_size):
                batch = df[feature_column].iloc[i:i+batch_size].fillna('').tolist()
                
                # Filter out empty strings and very short texts
                batch = [text if len(str(text).strip()) > 3 else "neutral comment" for text in batch]
                
                try:
                    batch_results = sentiment_pipeline(batch, truncation=True, max_length=512)
                    results.extend(batch_results)
                except Exception as batch_error:
                    # st.warning(f"⚠️ Batch processing error: {str(batch_error)}")
                    # Fallback: create neutral predictions for failed batch
                    fallback_results = [{"label": "NEUTRAL", "score": 0.5} for _ in batch]
                    results.extend(fallback_results)
                
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
                    "Class_Distribution": dict(pd.Series(df_copy["HF_Label"]).value_counts()),
                    "Total_Predictions": len(df_copy)
                }
            
            # st.success(f"✅ {model_name} completed successfully!")
            return df_copy
            
        except Exception as e:
            st.error(f"❌ Error with transformer model {model_name}: {str(e)}")
            st.info("💡 **Tip**: Transformer models are prototype implementations. Consider using Models 1 & 2 for stable results.")
            return None
    
    def _calculate_split_metrics(self, y_true, y_pred, split_name: str) -> Dict[str, Any]:
        """Calculate metrics for a specific data split (train/validation/test)."""
        try:
            # Basic metrics
            accuracy = accuracy_score(y_true, y_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(
                y_true, y_pred, average='weighted', zero_division=0
            )
            
            # Class distribution analysis
            class_distribution = pd.Series(y_pred).value_counts().to_dict()
            
            return {
                "Split": split_name,
                "Accuracy": round(accuracy, 4),
                "Precision": round(precision, 4),
                "Recall": round(recall, 4),
                "F1-Score": round(f1, 4),
                "Sample_Count": len(y_true),  # y_true is always a dense array
                "Class_Distribution": class_distribution
            }
        except Exception as e:
            st.error(f"Error calculating metrics for {split_name} split: {str(e)}")
            return {"Split": split_name, "Error": str(e)}
    
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