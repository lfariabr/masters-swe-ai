# A2 Video - Cue Card (take 2)

One page. Tape it next to the camera. **Do NOT open the full script while recording** - the
stiffness in take 1 came from reading. Triggers only; your brain fills the sentences.

## The 6 numbers (say them, pause after each)

> **0.809** tuned tree AUC | **0.814** LogReg (the tie!) | **0.771** Naive Bayes
> **63/37** class imbalance | **0.78 vs 0.66** recall high vs low | **alcohol 0.49**

## Beat sheet (~9 min)

| # | Beat | Triggers | The number |
|---|---|---|---|
| 0 | Intro (0:45) | name, MLN601, A1 same data as regression → now classification | - |
| 1 | Hook (0:45) | "how far off?" → "which side of the line?" | RMSE → AUC |
| 2 | Business (0:45) | cheap screen flags weak batches; low = positive; decision support not automation | < 6 = low |
| 3 | Data (1:30) | 6,497 wines red+white; imbalance; heatmap alcohol strongest; pairplot = classes OVERLAP → expect good-not-perfect; kept duplicates (no wine ID) | 63/37 |
| 4 | Prep (1:00) | drop quality (leak); stratified 80/20; tree scale-invariant, LogReg scaler INSIDE Pipeline (refit per fold) | 5,197 / 1,300 |
| 5 | Modelling (1:30) | 5 models; GridSearchCV 5-fold scored on roc_auc; pruned tree does not memorise | depth 6, leaf 20 |
| 6 | Evaluation (2:00) | metrics table → ROC (point at orange) → HONEST PART: LogReg ties → tuning dropped accuracy ON PURPOSE (optimised ranking) → confusion matrix trade-off → importance matches chemistry | 0.809 / 0.814 / 0.786→0.737 / 0.78 vs 0.66 / 0.49 |
| 6.5 | Naive Bayes (0:30) | Module 5; generative = Bayes rule; independence VIOLATED (sulfur 0.72) yet robust for ranking | 0.771 |
| 7 | Deployment (1:00) | white-box wins for QC; screen not oracle; next: Random Forest + tune the threshold to cost | - |
| 8 | Close (0:30) | camera only: A1 = how wrong, A2 = how well separated; honest evaluation > complexity | - |

## Anti-stiffness rules

1. **Talk to ONE person** (a colleague at the warehouse), not to "the audience".
2. **Describe what you SEE.** Scroll the notebook and point ("here you can see...") - your
   eyes on the plot, not on text. That is what kills the reading voice.
3. **Warm-up take per block:** say the block once with NOTHING in front of you, then record.
   The warm-up is the rehearsal; the recording is the second telling - always looser.
4. **Flubbed a phrase? Keep going.** Small stumbles read as human, not as error. Only re-do
   a block if you lost the thread entirely.
5. **Pause AFTER every number.** One breath. It reads as confidence.
6. **Smile at beat 0 and beat 8.** First and last impressions carry the marker.

## Record in 4 blocks (not one 9-min take)

| Block | Beats | ~Time |
|---|---|---|
| A | 0 + 1 (intro + hook) | 1:30 |
| B | 2 + 3 + 4 (business + data + prep) | 3:15 |
| C | 5 + 6 (modelling + evaluation) | 3:30 |
| D | 6.5 + 7 + 8 (NB + deploy + close) | 2:00 |

Join the blocks in any editor (or QuickTime). Each block is short enough to hold entirely in
your head - that is what makes it sound spoken, not read.

## Pre-flight

- [ ] Self-test done (85+? go record)
- [ ] Notebook open at the top, font zoomed for video
- [ ] Webcam picture-in-picture ON, audio checked
- [ ] This card next to the camera, full script CLOSED
- [ ] File: `MLN601FariaLuisBrief2.mp4`
