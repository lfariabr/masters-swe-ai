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

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class EnhancedTrainer:
    """
    Copy of `ModelTrainer` class with additional features for debugging purposes.
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
            # ----- v2.3.0 - `feature/tf-idf-deep-dive` --------
            # Before vectorization, analyze comment sizes
            with st.container(border=True):
                with st.container(border=True):
                    comment_stats = self.analyze_comment_sizes(df, feature_column)
                    st.write("Comment Size Statistics:", comment_stats)

                # Find optimal feature count
                with st.container(border=True):
                    # optimal_features = self.find_optimal_features(df, feature_column, target_column)

                    # -- v2.6.1: Change the return of find_optimal_features
                    best_params = self.find_optimal_features(df, feature_column, target_column) 
                    optimal_features = best_params['vectorizer__max_features']
                    # st.write(f"Using optimal feature count: {optimal_features}")
            
            # ----- v2.3.0 - `feature/tf-idf-deep-dive` --------
            
            # Create vectorizer with optimal feature count
            vectorizer = TfidfVectorizer(
                stop_words="english",
                max_features=optimal_features, # was hardcoded to 5000 ... now using optimal feature count from cross-validation
                ngram_range=(1, 2),  # Include bigrams for better context
                min_df=2,  # Ignore terms that appear in less than 2 documents
                max_df=0.95  # Ignore terms that appear in more than 95% of documents
            )

            # Using score column as additional feature
            if score_column and score_column in df.columns:
                X = self.create_combined_features(df, feature_column, score_column, vectorizer)
            else:
                X = vectorizer.fit_transform(df[feature_column].fillna(''))

            # Model evaluation
            # Scenario1: Try to find particular word from a page (finds 9/10. Precision 90%) [classification problem - always get accuracy]
            # Scenario2: Try to understand the severity of the problem [regression problem - single class]

            # 3 classes of classification: Promoter, Neutral, Detractor
            # 2 classes of classification: Positive or Negative
            
            # Get target values
            y = df[target_column] # output: Promoter, Neutral, Detractor
            
            # v2.5.0 - Three-way split: train (60%), validation (20%), test (20%)
            # Step 1: First split - separate test set (80/20)
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
            
            st.info(f"Data split: Train={train_samples} samples, Validation={val_samples} samples, Test={test_samples} samples")
            
            # Distribution analysis to ensure stratification worked properly
            train_dist = pd.Series(y_train).value_counts(normalize=True)
            val_dist = pd.Series(y_val).value_counts(normalize=True)
            test_dist = pd.Series(y_test).value_counts(normalize=True)
            
            dist_df = pd.DataFrame({
                'Train %': train_dist * 100,
                'Validation %': val_dist * 100,
                'Test %': test_dist * 100
            })
            
            st.write("Class distribution across splits:")
            st.dataframe(dist_df)
            
            # Model training
            # overfit x underfit
            # https://www.analyticsvidhya.com/blog/2020/02/underfitting-overfitting-best-fitting-machine-learning/
            model = LogisticRegression(
                ## -- v2.4.0 - `feature/tf-idf-iteration-check` --
                # max_iter=100, # This was hardcoded to 1000. Now using 100 because mean_token_length is 19 and standard token is 34
                max_iter=best_params['classifier__max_iter'],
                random_state=42,
                class_weight='balanced',  # Handle class imbalance

                ## -- v2.6.0 - `feature/logreg-hyperparam-tuning` --
                # C=10.0,
                # penalty='l2',
                # solver='lbfgs',
                # multi_class='ovr',

                ## -- v2.6.1 - `feature/logreg-hyperparam-tuning` --
                # removing hardcoded values
                C=best_params['classifier__C'],
                penalty=best_params['classifier__penalty'],
                solver=best_params['classifier__solver'],
                multi_class=best_params['classifier__multi_class'],
            )
            
            start_time = time.time()
            model.fit(X_train, y_train)
            training_time = time.time() - start_time

            n_iter = model.n_iter_[0]
            print(f"Iterations until convergence for {model_name}: {n_iter}")
            st.write(f"Iterations until convergence for {model_name}: {n_iter}")
            ## -- v2.4.0 - `feature/tf-idf-iteration-check` --
            
            # Store model artifacts
            self.models[model_name] = model
            self.vectorizers[model_name] = vectorizer
            
            # v2.5.0 - Evaluate on all three splits
            with st.container(border=True):
                st.subheader("Model Performance Across Data Splits")
                
                # Predictions on all splits
                y_train_pred = model.predict(X_train)
                y_val_pred = model.predict(X_val)
                y_test_pred = model.predict(X_test)
                
                # Calculate metrics for all splits
                train_metrics = self._calculate_split_metrics(y_train, y_train_pred, "Train")
                val_metrics = self._calculate_split_metrics(y_val, y_val_pred, "Validation")
                test_metrics = self._calculate_split_metrics(y_test, y_test_pred, "Test")
                
                # Combine metrics into a single dataframe for comparison
                metrics_df = pd.DataFrame([train_metrics, val_metrics, test_metrics])
                st.dataframe(metrics_df.set_index('Split'))
                
                # Create visualization to compare performance across splits
                self._visualize_split_performance(train_metrics, val_metrics, test_metrics)
                
                # Check for overfitting
                acc_drop_train_val = train_metrics["Accuracy"] - val_metrics["Accuracy"]
                acc_drop_val_test = val_metrics["Accuracy"] - test_metrics["Accuracy"]
                f1_drop_train_val = train_metrics["F1-Score"] - val_metrics["F1-Score"]
                
                # Create a summary box with color-coded metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Train-Validation Accuracy Gap", 
                             f"{acc_drop_train_val:.4f}",
                             delta_color="inverse")
                    
                with col2:
                    st.metric("Validation-Test Accuracy Gap", 
                             f"{acc_drop_val_test:.4f}",
                             delta_color="inverse")
                
                # Display overfitting analysis
                if acc_drop_train_val > 0.05:
                    st.warning(f"⚠️ Potential overfitting detected: Train-Validation accuracy drop = {acc_drop_train_val:.4f}")
                if acc_drop_val_test > 0.05:
                    st.warning(f"⚠️ Potential generalization issue: Validation-Test accuracy drop = {acc_drop_val_test:.4f}")
                if acc_drop_train_val <= 0.05 and acc_drop_val_test <= 0.05:
                    st.success("✅ Model generalizes well across splits")
            
            # Store comprehensive metrics using test set (for backward compatibility)
            self.metrics[model_name] = self._calculate_metrics(
                y_test, y_test_pred, model_name, training_time
            )
            
            return model, vectorizer, X_test, y_test, y_test_pred
            
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
            
            ## -- v2.6.0 - `feature/logreg-hyperparam-tuning` 
            ## hardcoding for starting point
            'classifier__C': [0.1, 1.0, 10.0], # how strict or flexible the model is: range from 0.001 to 100
            'classifier__penalty': ['l2'], # type of regularization: l1, l2, elasticnet, none
            'classifier__solver': ['lbfgs'], # algorithm to use: lbfgs, newton-cg, liblinear, sag, saga
            'classifier__multi_class': ['ovr', 'multinomial'], # all vs one or multinomial
            'classifier__max_iter': [100, 300, 500], # maximum number of iterations, was 1000 now 100 because mean_token_length is 19 and standard token is 34
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

        st.write(f"Best parameters: {grid_search.best_params_}")
        st.write(f"Best score: {grid_search.best_score_}")
        
        # Return the optimal feature count
        return grid_search.best_params_ #['vectorizer__max_features'] -- v2.6.1: Change the return of find_optimal_features

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


    def _visualize_split_performance(self, train_metrics, val_metrics, test_metrics):
        """Create visualizations comparing model performance across train/validation/test splits."""
        try:
            # Extract metrics for visualization
            splits = ['Train', 'Validation', 'Test']
            accuracy = [train_metrics["Accuracy"], val_metrics["Accuracy"], test_metrics["Accuracy"]]
            precision = [train_metrics["Precision"], val_metrics["Precision"], test_metrics["Precision"]]
            recall = [train_metrics["Recall"], val_metrics["Recall"], test_metrics["Recall"]]
            f1 = [train_metrics["F1-Score"], val_metrics["F1-Score"], test_metrics["F1-Score"]]
            
            # Create DataFrame for visualization
            viz_data = pd.DataFrame({
                "Split": splits * 4,
                "Metric": ["Accuracy"] * 3 + ["Precision"] * 3 + ["Recall"] * 3 + ["F1-Score"] * 3,
                "Value": accuracy + precision + recall + f1
            })
            
            # Create bar chart using Altair
            import altair as alt
            
            chart = alt.Chart(viz_data).mark_bar().encode(
                x=alt.X('Split:N', title='Data Split'),
                y=alt.Y('Value:Q', title='Score', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('Split:N', 
                               scale=alt.Scale(domain=['Train', 'Validation', 'Test'],
                                              range=['#5470C6', '#91CC75', '#FAC858'])),
                column=alt.Column('Metric:N', title='Performance Metrics')
            ).properties(
                title='Model Performance Across Data Splits',
                width=150
            )
            
            st.altair_chart(chart)
            
            # Add interpretation text
            st.write("**Interpretation Guide:**")
            st.write("""
            - **Similar heights** across all three splits indicate good generalization
            - **Significantly higher Train bars** compared to Validation/Test suggest overfitting
            - **Lower Test bars** compared to Validation suggest potential data leakage or sampling issues
            """)
            
        except Exception as e:
            st.error(f"Error creating performance visualization: {str(e)}")

# Module exports
__all__ = ['ModelTrainer']