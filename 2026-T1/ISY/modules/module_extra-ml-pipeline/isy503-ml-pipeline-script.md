# ISY503 — Speaker Script
## ML Pipelines: From Excel to Prediction (20–30 min)

---

### Slide 1 — Title

**Say:** "Hey everyone. I'm Luis — same course, a few years ahead of some of you in the industry. Today I want to show you something that took me way too long to figure out: what a machine learning pipeline actually is. Not the theory — the code. We're going to build one, live, right now, using a dataset you may have heard of."

"Everything I show you today runs in Google Colab. Nothing to install. Just open the notebook link, hit 'Run All', and follow along."

---

### Slide 2 — What Is a Pipeline?

**Say:** "When people say 'machine learning pipeline' it sounds intimidating. But it's just... a series of steps. Let me use an analogy — packing a suitcase."

"Think about the last time you packed for a trip. You decided what to bring — that's choosing your features. You folded the clothes — that's encoding and cleaning the data. You weighed the bag — that's your train/test split, making sure you're not overpacking. You took the trip — that's training the model. And then — did the trip go well? — that's evaluating accuracy."

"No magic. No black box. Just structured steps. If you can follow a recipe, you can follow a pipeline."

---

### Slide 3 — The Titanic Problem

**Say:** "The dataset we're using is the Titanic. 1912, the ship sinks. We have records on 891 passengers: how old they were, male or female, what ticket class they were in, how much they paid, who they were travelling with."

"And we know one more thing: whether they survived or not."

"Our job: given a new passenger we've never seen before, predict whether they would have survived."

"I like this dataset because it's not abstract. These were real people. The stakes were life and death. And the patterns in the data — who survived — tell a story about how the world worked in 1912."

---

### Slide 4 — EDA: The Excel Mindset

**Say:** "Before we build any model, let's ask a simpler question: what would Excel tell us?"

"If you've ever done a pivot table, you've done exploratory data analysis — you just didn't call it that."

"Watch this. [Run the groupby cells.] Survival rate by sex: 74% of women survived. Only 19% of men. Just from one pivot."

"Survival rate by class: 63% of first-class passengers survived. 24% of third-class. 'Women and children first' — and apparently wealthy people too."

"Now pause. Does this mean we should just sort by sex and class and call it ML? No — because these are group averages. Real prediction is about individuals. Machine learning finds the combination of factors that best predicts the outcome for *each specific person*."

---

### Slide 5 — EDA Visualizations

**Say:** "Here are those insights as charts. [Show 3-panel plot.] Sex, ticket class, age band."

"Quick question for the class: what do you notice that surprises you?" [Pause for answers]

"Children had a higher survival rate than adults. Makes sense — 'women and children first' was the evacuation order."

"But here's the thing: these charts can't tell us what happens for a 45-year-old male in second class who paid a mid-range fare and had two kids with him. For that, we need ML."

---

### Slide 6 — Cleaning the Data

**Say:** "This is the part nobody talks about in YouTube tutorials but takes 80% of the time in real projects: cleaning the data."

"Our raw dataset has 177 missing ages. What do we do? We fill them with the median age — 28. That's a reasonable estimate. Not perfect, but better than dropping 177 rows."

"Sex is stored as text: 'male', 'female'. Algorithms don't understand text — they only understand numbers. So we encode: female=0, male=1. This is called label encoding."

"Then we split: 80% of the data is for training — the algorithm learns from this. The remaining 20% is held back and used only for testing. This is critical. You never evaluate on data you trained on — that's like a teacher marking their own exam."

---

### Slide 7 — Algorithm 1: Linear Regression

**Say:** "First algorithm. Linear Regression. You've seen this — it's the trendline in Excel. The 'line of best fit'."

"We're going to train it on our Titanic data to predict survival. Watch what happens. [Run the cell]"

"Look at these raw predictions. Minus 0.2. 1.3. 0.8. Minus 0.1. The actual answers should be 0 or 1. But Linear Regression doesn't know that — it's trying to fit a continuous line, and the line overshoots."

"This is not a bug in the code. It's a fundamental mismatch between the tool and the task. Linear Regression is designed for continuous outputs like house prices or temperature — not binary outcomes like survived/died."

---

### Slide 8 — Why Linear Regression Fails Here

**Say:** "We can patch it — if the prediction is above 0.5, we call it 1. If below, we call it 0. And we get about 79% accuracy. That's actually not terrible."

"But we're using the wrong tool. It's like using a butter knife to cut a steak. It kind of works, but there are better options."

"This is WHY classification algorithms were invented. The first one we'll look at is probably the most intuitive: the Decision Tree."

---

### Slide 9 — Algorithm 2: Decision Tree

**Say:** "A Decision Tree learns a set of if/else rules from the data. Exactly like a flowchart."

"'Is this passenger male? Yes — is their fare under 26? Yes — they probably died.' That kind of logic."

"The superpower of decision trees is that you can read them. I mean literally read them, out loud, like English. And you can check: does this rule make sense? Does it match what we know about the world?"

"In regulated industries — banking, healthcare, insurance — this is incredibly valuable. You can explain to a regulator exactly why the model made a decision."

---

### Slide 10 — Decision Tree Visual

**Say:** "Here's the tree we trained. [Show plot_tree output.] Don't be intimidated — let me walk you through one node."

"This node at the top says: pclass <= 2.5. That means: is the passenger in 1st or 2nd class (1 or 2), versus 3rd class (3)? If yes, go left. If no, go right."

"The next line — gini = 0.48 — that's how mixed the node is. Zero means every passenger in this node has the same outcome. 0.5 means it's 50/50. We want lower gini — purer nodes."

"This tree gets us to 82% accuracy. Higher than Linear Regression, and fully transparent."

---

### Slide 11 — Algorithm 3: KNN

**Say:** "Third algorithm: K-Nearest Neighbors. This one is probably the most intuitive of all."

"Imagine you're a new student at school and you want to know if you'll like the canteen. You don't have enough information to decide on your own. So what do you do? You ask the 5 students most similar to you — same year, same taste in food, similar background — and you go with whatever the majority says."

"That's KNN. For a new passenger, we find the 5 most similar passengers in our training data, count how many survived, and predict the majority outcome."

"k=5 means 5 neighbors. You can change k — we'll see how that affects accuracy."

---

### Slide 12 — KNN: How k Affects Accuracy

**Say:** "Look at this chart. [Show k vs accuracy plot.] As we change k from 1 to 20, accuracy changes."

"Very small k — like k=1 — means we're using just one neighbor. That's too sensitive. One noisy data point can throw off the whole prediction. We call this overfitting."

"Very large k — like k=20 — means we're asking so many neighbors that the local patterns get lost. Everything regresses to the average. We call this underfitting."

"k=5 to k=7 tends to work well for this dataset. Finding the right k is an example of what we call 'hyperparameter tuning' — adjusting the settings of the algorithm."

---

### Slide 13 — All 3 Compared

**Say:** "Here's the side-by-side. [Show comparison table and bar chart.]"

"Linear Regression: 79%, wrong tool for the job, but useful as a baseline."
"Decision Tree: 82%, interpretable, visual rules."
"KNN: 80%, no training assumptions, but slow on large datasets."

"There's no single winner. The right algorithm depends on what you value: accuracy, interpretability, speed, or simplicity."

"In the optional sections — 7 and 8 — I go further: Random Forest is 100 Decision Trees voting together, and SVM draws the widest possible boundary between classes. Both usually beat 82% on this dataset."

"But here's the key insight: every advanced ML technique uses this same pipeline. EDA → clean → split → train → evaluate. Master this, and the rest is just plugging in different algorithms."

---

### Slide 14 — What's Next

**Say:** "Where does this go? Three directions."

"Random Forest: instead of one tree making decisions, 100 trees vote. Their errors cancel out. Typically 84–86% on this dataset. Still interpretable via feature importances."

"SVM — Support Vector Machine: draws the widest road between the two classes. Excellent for high-dimensional data like text or images."

"Neural Networks and Deep Learning: layers of connected 'neurons' that learn complex non-linear patterns. The foundation of GPT, image recognition, everything you read about in the news."

"The Titanic pipeline we built today is the foundation for ALL of these. The syntax changes. The concepts don't."

---

### Slide 15 — Q&A

**Say:** "That's it. Let me recap what we covered in 25 minutes."

"We started with a pivot table — what Excel would tell us. We cleaned the data, encoded it, and split it. Then we ran three algorithms: Linear Regression as a baseline, Decision Tree for explainable classification, and KNN for distance-based prediction."

"We compared them side by side. None of them is perfect. All of them are understandable."

"The notebook is available. Open it in Google Colab, run every cell, and try changing things: change max_depth in the Decision Tree, change k in KNN, see what happens."

"Questions?" [Pause and engage]

**If asked about which algorithm to use in practice:**
> "It depends on your constraints. If you need to explain decisions to a human — use a tree. If you need maximum accuracy and don't need to explain — use Random Forest or XGBoost. If you're working with images or text — neural networks. Start simple, add complexity only when you need it."

**If asked about overfitting:**
> "Great question. Overfitting is when the model memorizes the training data but can't generalize. That's why we have a test set — data the model has never seen. If accuracy on training is 95% but test is 70%, you're overfitting. The fix: more data, simpler model, or regularization."
