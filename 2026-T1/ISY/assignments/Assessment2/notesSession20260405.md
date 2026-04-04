## Concepts Consolidated — Session 2026-04-05

> Follow-up Q&A after updating Task 4, validating regressor coverage, and refining how to explain model choice in the manual.

---

**Q1: Can we trust the latest results?**

Yes, but only selectively.

The key rule is: **saved execution output is stronger evidence than comments or summary prose**.

What is trustworthy from the saved notebook:
- **LinearRegressor** final `average_loss = 56,000,984`
- **DNN [64, 32]** final `average_loss = 15,550,921`
- **DNN [128, 64]** final `average_loss = 13,630,101`
- **Task 4 lr=0.01** final `average_loss = 141,106,200`
- **Task 4 lr=0.5** final `average_loss = 835,841.5`

Those values are present in the executed notebook outputs, so they are legitimate evidence.

What is still shaky:
- the claimed **Task 1 best = 10,822,464**

That number appears in comments / tuning notes, but the saved output in the latest notebook execution does not cleanly line up with it in the same way the newer sections do. So the safe academic approach is:

> trust the newest executed outputs first, treat older summary numbers carefully, and never let a comment outrank a printed metric.

This is a useful reporting principle:
- **Code comment** = intention or memory
- **Notebook output** = experiment evidence
- **Manual** = interpretation of evidence

---

**Q2: What is the difference between `LinearRegressor` and `DNNRegressor`?**

A `LinearRegressor` learns one weighted sum:

```text
price = w1*x1 + w2*x2 + ... + b
```

That means:
- every feature contributes in a straight-line way
- the effect of one feature is assumed to be independent of others unless interactions are manually engineered
- the model is simple, interpretable, and useful as a baseline

A `DNNRegressor` adds hidden layers and nonlinear activations between input and output. That gives it the ability to learn:
- curved relationships
- threshold effects
- interactions between features
- combinations that are not well represented by a single straight-line equation

In this car dataset, that matters because price is unlikely to be determined by a simple additive pattern. Features such as:
- `engine-size`
- `horsepower`
- `make`
- `body-style`
- `aspiration`

do not operate independently in a purely linear way. A DNN can learn that some combinations matter more than the individual variables alone.

That is exactly what the experiment shows:
- `LinearRegressor` underperforms badly
- all DNN variants beat it
- therefore, the problem appears to contain meaningful nonlinear structure

The academic interpretation is:

> the linear model was the control condition; the DNN was justified because the baseline showed linear structure alone was insufficient.

---

**Q3: Why did the linear model still matter if it performed badly?**

Because a weak baseline is still valuable evidence.

The `LinearRegressor` was not wasted work. It answered an important modelling question:

> “Can a simple linear relationship explain car price well enough?”

The answer was no.

That gives you a strong justification for using deep learning. Without the linear baseline, the DNN choice can look arbitrary. With it, the logic becomes much stronger:

1. test the simplest reasonable regressor
2. observe that it underfits
3. move to a nonlinear model
4. compare whether extra depth helps

That is exactly the sort of progression the rubric is asking for under:
- model exploration
- hyperparameter tuning
- analysis of efficiency

So the linear model is useful not because it wins, but because it proves why the stronger model is needed.

---

**Q4: How do I explain the architecture decisions behind my DNN choice?**

The strongest explanation is not “I chose a deep model because deep learning is powerful.”

The stronger explanation is:

> I chose the smallest architecture that was expressive enough for the problem and supported by the evidence.

A concise justification:

- `LinearRegressor` was used first as a baseline
- it performed much worse, showing the task is not purely linear
- `DNNRegressor` with one hidden layer of 64 units was then used as the main numeric model
- this architecture balanced expressiveness and simplicity for a dataset with only 201 cleaned rows
- deeper models `[64, 32]` and `[128, 64]` were tested
- both were worse than the single-layer model
- therefore, extra depth added complexity without improving performance

That means the final architecture choice was evidence-based:

> the single hidden layer was enough to capture nonlinearity, but the dataset was too small to benefit from a deeper network.

This is a very good academic conclusion because it shows restraint. You are not just saying “bigger network = better.” You are showing that you tested that assumption and rejected it based on results.

---

**Q5: How should I frame the architecture choice in the context of Assessment 2 specifically?**

Frame it around the brief’s real goal:

> explore multiple models, vary hyperparameters and features, and evaluate their effectiveness.

That means your architecture discussion should sound progressive, not fixed from the start.

A strong framing:

1. start with the simplest baseline (`LinearRegressor`)
2. move to a nonlinear model (`DNNRegressor [64]`)
3. test whether more depth improves the result (`[64, 32]`, `[128, 64]`)
4. conclude that feature representation and learning-rate tuning mattered more than extra hidden layers
5. show that the final major improvement came from combining numeric + categorical features in Task 4

This helps separate two ideas:

- **architecture choice**
  - linear vs shallow DNN vs deeper DNN
- **representation choice**
  - numeric only vs normalized numeric vs categorical only vs combined features

That distinction makes the report sound more mature:
- Task 1 and regressor coverage answer “what model shape is appropriate?”
- Tasks 2 to 4 answer “what input representation and hyperparameters work best?”

---

**Q6: What would a good transcript-style explanation sound like?**

This version is natural and still academically grounded:

> “I approached the model design in stages. First, I tested a `LinearRegressor` to check whether car price could be explained as a simple linear combination of the numeric features. It underperformed badly, which indicated the problem was not purely linear. I then moved to a `DNNRegressor` with a single hidden layer of 64 units. That architecture was chosen because it is flexible enough to learn nonlinear relationships, but still small enough for a dataset with only 201 cleaned examples. To test whether additional model depth would help, I also trained `[64, 32]` and `[128, 64]` architectures. Both were worse than the single-layer model, which suggests the extra parameters increased complexity without improving performance on this small dataset. Based on that, the single-layer DNN was the best numeric-only architecture. The strongest improvement overall came later in Task 4, where combining normalized numeric features with categorical indicators produced the best model in the notebook.” 

That transcript works because it tells a story:
- baseline
- failure of linearity
- shallow DNN succeeds
- deeper DNNs do not help
- final gain comes from better features, not more layers

---

**Q7: What is the key insight about Task 4?**

Task 4 changes the story from architecture-first to representation-first.

The best overall result did **not** come from making the network deeper.
It came from:
- using all 25 features
- normalizing the numeric ones correctly
- one-hot encoding the categorical ones
- fixing the mixed-data statistics bug
- increasing the learning rate to `0.5`

So the biggest lesson from the full notebook is:

> on this dataset, better feature representation and better learning-rate calibration mattered more than deeper architecture.

That is an excellent conclusion for the manual because it shows actual ML reasoning:
- not all gains come from bigger models
- sometimes the decisive improvement comes from data representation and optimizer settings

---

**Q8: How do I explain why deeper DNNs were worse?**

A safe explanation is:

- the dataset is small (`201` usable examples)
- deeper networks add more parameters
- more parameters require more data to train reliably
- with limited data, extra capacity can lead to less efficient learning or unstable convergence
- therefore, the deeper models did not outperform the simpler one

This does **not** need to be overclaimed as “definite overfitting.” A better phrasing is:

> “The deeper architectures increased model complexity without producing a performance benefit on this dataset.”

That is precise and defensible.

If you want a slightly stronger interpretation:

> “This suggests the dataset is too small to justify additional depth, so the simpler single-layer network offered the best trade-off between capacity and stability.”

---

**Q9: What would be the cleanest final takeaway for the report?**

Use this throughline:

> The experiments show that model choice should be justified incrementally. A linear regressor was insufficient, which justified a nonlinear model. A shallow DNN improved performance substantially, but deeper DNNs did not help, showing that additional architectural complexity was not the main driver of improvement. The largest gain came from combining numeric and categorical features with an appropriate learning rate in Task 4. This indicates that, for this dataset, feature representation and hyperparameter calibration were more important than simply increasing network depth.

That line ties together:
- regressor coverage
- architecture choice
- hyperparameter tuning
- Task 4 as the final best result

---

**Throughline from today's session:**

> The updated notebook supports the newer regressor-comparison and Task 4 results, but the important methodological lesson is bigger than the numbers: deep learning was justified only after the linear baseline failed, and deeper architecture was not automatically better. The strongest performance gain came from the right features plus the right learning rate, not from blindly adding more layers.
