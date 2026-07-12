1 - b
2 - so that low quality is what we want to seek and destroy, meaning that low_quality will either be true or false
3 - b
4 - ROC analyzes sensitivity and specificity of a model... the true positive rate against the false positive rate, used to measure the performance of a classification model at different thresholds, which trades off the rate of correctly identifying positive cases against falsely triggering on negative ones.

The diagnoal line means no prediction capaability, random guessing. A tuned tree above that line demonstrates the model posesses discriminative power, better than simply guessing.

5 - dont know
i searched on google and understood that decision threshold problem but did not get it well.. im finding harder to measure from previous rmse and r square. makes sense?

6 - Tuned-tree recall is 0.78 for high wines but only 0.66 for low wines.

(a) In plain words, what does "recall 0.66 for low" mean?
(b) Which of the two errors (missing a low wine vs flagging a good wine as low) is more costly for the business framing (a screen that flags weak batches for expert tasters), and what lever could shift the balance?

recall is the correct catch, the rest goas as undetected false negatives. on this case, 66 means that the model correctly identified 66% of truly low quality wines, while 34% of low quality wines were missed (false negatives) - the model guessed it was high quality when it was actually low quality.

missing slow wine is more costly for business because it means that a low quality wine is not flagged and goes to the market, which could damage the brand reputation, customer disatisfaction... 

and the lever to adjust that is the probability threshold for classification. If we decrease it, recall will grow, making the model more sensitive and flagging high quality wines as low quality. If we increase the threshold, the contrary happens, as recall drops making the model less sensitive and flagging low quality wines as high quality - scenario we want to avoid

7 - b as it preserve class imbalance on train/test split phases

Part 2 (written, one line): the StandardScaler sits inside the Logistic Regression Pipeline (not applied to all of X_train first). State the leakage rule this enforces - careful with the DIRECTION of the arrow.
the standardScaler sits inside to enforce the fundamental leakage rule, info must flow from training set to test/validation set, never vice-versa

8 - GridSearchCV chose max_depth=6 and min_samples_leaf=20.

(a) What does each parameter control in the tree?
(b) What would an UNconstrained tree (no depth limit, leaf size 1) do on this data, and why does that hurt test performance?
(c) Why was the grid scored on roc_auc instead of accuracy?

max_depth controls the max depth of the tree, on this we case we limit to 6 levels of splits, which is a way to control the complexity of the model and avoid overfitting
min_samples_leaf controls the min number of training samples to be at a terminal node, in this case we limit to 20 samples, which is another way to control the complexity of the model and avoid overfitting

an unconstrained tree would grow undefinitely, creating a complex model that would perfectly fit the training data, but would not generalize well to unseen data, leading to poor test performance due to overfitting.

we used roc_auc instead of accuracy because of dataset imbalance, so we opted to push the threshold to favor recall over precision, and roc_auc is a better metric to evaluate the model performance in this case, as it considers both true positive and false positive rates across different thresholds.

Q9. Generative vs discriminative (13 pts) - written
The tree and logistic regression are discriminative; Gaussian Naive Bayes is generative.

(a) What does each type of model actually learn / model?
(b) NB assumes features are independent given the class - your own heatmap shows the two sulfur-dioxide features correlate at 0.72, so the assumption is violated. Yet NB still scores AUC 0.771. Why does it stay usable despite the broken assumption?

discriminative learns the boundary of separating different classes directly from the data, while generative learns underlying distribution of features for each individual class

i dont know how to explain that second part.

10. The honest finding (15 pts) - written
Logistic Regression (0.814) essentially ties with the tuned Decision Tree (0.809).

(a) What does that near-tie tell you about the shape of the decision boundary in this data?
it tells us that the decision boundary in this data is likely to be linear...
(b) Why is reporting this openly a STRENGTH of the assessment, not a failure of the tree?
because it means that we've digged deep into the data, trained multiple models and approaches, explored possibilities and challenged the assumptions, and reporting honestly
(c) Given the tie, name one concrete reason you might still deploy the tree over the logistic regression for the wine-screening use case.
definitely its interpretability stands out... easy to showcase!
> **Archive notice:** These answers were written against the pre-deduplication/v3 experiment.
> Use `assessment2-self-test.md` for the current v5 operational lot-screening rehearsal. This file
> is retained as study history and its old metrics must not be used in the final presentation.
