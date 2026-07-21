# Draft message to Dr Kamran

**Subject:** MLN601 Assessment 2 revised submission and test-set clarification

Dear Dr Kamran,

Thank you for taking the time to review my Assessment 2 notebook and for suggesting a broader
comparison of models and imbalance treatments.

I also want to correct an answer I gave during our conversation. When you asked whether I had
resampled the test data, I incorrectly said yes. After checking the implementation, I confirmed
that the train/test split is created first, SMOTE is applied only inside the training portion of
each cross-validation fold, and the held-out test set is never resampled. I am sorry that my oral
answer did not describe the implementation correctly.

I have prepared a revised v8 submission that makes this boundary explicit and incorporates your
recommendations. It compares Logistic Regression, KNN, Decision Tree, SVM, Gaussian Naive Bayes,
Bernoulli Naive Bayes, Multinomial Naive Bayes, Complement Naive Bayes and Random Forest. The
models are compared under the original training distribution, SMOTE and class weighting where
supported, using the same five stratified folds and pre-declared business gates.

The comparison shows the trade-off directly. On average, SMOTE increases sensitivity but reduces
specificity, with little change in AUC. Class weighting produces a similar cost-sensitive effect
without synthetic observations. Random Forest also tests ensemble learning by reducing the
variance of a single tree. Based on the declared gates, balanced accuracy and interpretability
tie-break, the revised notebook approves Random Forest with class weighting. It is then evaluated
once on the untouched test set and explained with SHAP.

The revised submission includes the executed notebook, PDF, text export and a newly recorded
walkthrough video.

Thank you again for the feedback and the opportunity to improve both the experiment and my
explanation of it.

Kind regards,

Luis Faria
