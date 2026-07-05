# A2 Video - Cue Card (take 2, v3 numbers)

One page. Tape it next to the camera. **Do NOT open the full script while recording** - the
stiffness in take 1 came from reading. Segment-by-segment cues live in
`assessment2-presentation-cues.md`; this page is the numbers + delivery rules.

## The story spine (say it as ONE sentence if you blank)

> **6,497 raw → 1,177 duplicates removed → 5,320 unique → zero train/test overlap →
> tree AUC 0.793 → low recall 0.59**

## The numbers (pause after each)

> **0.793** tuned tree AUC | **0.813** LogReg (leads by 0.020) | **0.736** Naive Bayes
> **0.657** default tree | **63/37** imbalance | **0.83 vs 0.59** recall high vs low
> **alcohol 0.58** | split **4,256 / 1,064** | winner: **gini, depth 5, leaf 20**

## Beats that CHANGED since the old draft (do not say the v2 lines)

1. **No more "tie".** LogReg 0.813 beats the tree 0.793 on this split. Line: "the simpler
   model edges ahead - honest comparison, evidence-based choice."
2. **Tuning now HELPS accuracy too** (0.682 → 0.739). The old "tuning lowered accuracy on
   purpose" line is dead. The honest-finding slot is now the DEDUP: "removing duplicates
   dropped my own AUC from 0.809 to 0.793 - and that is the more credible number."
3. **NB softened.** 0.736: above the default tree, below tuned tree and LogReg. "Useful
   despite the violated assumption, but not the best fit here" - do not oversell.
4. **New star beat = duplicate leakage.** 359 test rows used to have exact copies in
   training; v3 deduplicates first, overlap zero. This is YOUR methodological catch - say
   it with pride in Data Prep.

## Anti-stiffness rules

1. **Talk to ONE person** (a colleague at the warehouse), not to "the audience".
2. **Describe what you SEE.** Scroll the notebook and point ("here you can see...") - eyes
   on the plot, not on text. That is what kills the reading voice.
3. **Warm-up take per block:** say the block once with NOTHING in front of you, then record.
   The warm-up is the rehearsal; the recording is the second telling - always looser.
4. **Flubbed a phrase? Keep going.** Small stumbles read as human. Only re-do a block if
   you lost the thread entirely.
5. **Pause AFTER every number.** One breath. It reads as confidence.
6. **Smile at the open and the close.** First and last impressions carry the marker.

## Record in 4 blocks (not one 9-min take)

| Block | Segments (cue sheet nums) | ~Time |
|---|---|---|
| A | 0 + 1 (opening + business) | 1:15 |
| B | 2 + 3 (data + prep, incl. the DUPLICATE catch) | 2:15 |
| C | 4 + 5 (modelling + evaluation) | 3:15 |
| D | 6 + 7 + 8 (NB + lessons + close) | 1:45 |

Join the blocks in any editor (or QuickTime). Each block is short enough to hold entirely
in your head - that is what makes it sound spoken, not read.

## Pre-flight

- [ ] v3 notebook open at the top, font zoomed for video
- [ ] Webcam picture-in-picture ON, audio checked
- [ ] This card + cue sheet next to the camera, full script CLOSED
- [ ] Quiz gaps rehearsed out loud: "you get what you optimise" + "broken assumption,
      intact ranking" (now with the v3 caveat: NB not the best fit here)
- [ ] File: `MLN601FariaLuisBrief2.mp4`
