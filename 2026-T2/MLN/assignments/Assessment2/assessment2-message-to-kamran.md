# Draft message to Dr Kamran

**Subject:** MLN601 Assessment 2 revised submission and test-set clarification

Dear Dr Kamran,

Thank you for taking the time last Monday to review my Assessment 2 notebook and for suggesting a
broader comparison of models and imbalance treatments.

When you asked whether I had resampled the test data, I incorrectly said yes. After checking the
implementation, I confirmed that the train/test split is created first, SMOTE is applied only
inside the training portion of each cross-validation fold, and the held-out test set is never
resampled. I am sorry my answer at the time did not describe the implementation correctly.

I have prepared a revised v8 submission that makes this explicit and incorporates your
recommendations. It compares nine model families, Logistic Regression, KNN, Decision Tree, SVM,
four Naive Bayes variants and Random Forest, under the original distribution, SMOTE and class
weighting where supported, using the same five folds and pre-declared gates.

On average, SMOTE increases sensitivity but reduces specificity, with little change in AUC. Class
weighting produces a similar cost-sensitive effect without synthetic observations. Based on the
declared gates, balanced accuracy and an interpretability tie-break, the revised notebook approves
Random Forest with class weighting, evaluated once on the untouched test set and explained with
SHAP.

The submission includes the executed notebook, PDF, text export and a newly recorded walkthrough
video. I edited the recording to fit the 10-minute limit, so the narration is sped up in places. I
have also attached a second, less compressed version in case you would prefer to watch it closer
to natural pace.

Thank you again for the feedback and the chance to improve both the experiment and my explanation
of it.

Kind regards,

Luis Faria
