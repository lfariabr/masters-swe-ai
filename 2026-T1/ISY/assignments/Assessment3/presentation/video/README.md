# A3 group presentation video

The presentation was delivered live in class, so there was never a group
recording. Dr Nandini asked for one, so each presenter records their own slides
and this directory stitches the parts into a single video.

## How to run

```bash
./build.sh            # build every slide listed in manifest.tsv, then concat
./build.sh 3 8        # rebuild only those slides, then re-concat
./build.sh --verify   # ffprobe report over the segments and the output
```

Output: `../../submission/ISY503_Faria_L_Assessment_3_Presentation.mp4`.
`*.mp4` is gitignored repo-wide, so committing the finished video needs
`git add -f`.

`raw/` (source recordings) and `work/` (slide renders, per-slide segments) are
gitignored - together they are around 700 MB.

## Current state

Complete: 12 slides, 10 min 59 s, 46 MB.

| Slides | Presenter | Source |
|---|---|---|
| 1, 4, 5, 6, 7, 12 | Luis | `luis_full.mp4` (one 14 min session, sliced) |
| 2, 9, 11 | Samiran | `samiran_slide*.mov` |
| 3, 8 | Victor | `victor_a.mp4`, `victor_b.mp4` |
| 10 | Luis | `luis_full.mp4` |

Victor sent two files. Scene detection and frame checks confirm each holds a
single slide start to finish (3 and 8), so slide 10 (Ethical considerations) was
never recorded by him. Luis had covered 8 and 10 in his own session as a backup
("Victor didn't do that part"), so slide 10 uses Luis's take while Victor's own
recording is still used for slide 8. If Victor later sends slide 10, swapping it
in is one manifest row.

### Finding the cut points in Luis's single-take recording

Luis recorded all his parts in one 14-minute session with retakes on camera. The
cuts came from two sources cross-checked against each other:

- **Slide boundaries** - `select='gt(scene,0.06)'` over the slide title band only.
  The body of each slide animates, so a full-frame scene detect fires on every
  bullet; the title band changes only when the slide does.
- **Take boundaries** - a whisper transcript (`work/luis_full.srt`) to find the
  retakes, snapped to a `silencedetect` map so no cut lands mid-word.

Word-level whisper timings (`-ml 1`) drift by several seconds across silences, so
where the two disagreed the silence map won. Every cut keeps the **last** take.

## How to record a part so it drops straight in

Open a Microsoft Teams meeting with yourself, share the deck in presenter view,
record, speak the slide, stop. That is what Victor did and it is the format the
pipeline treats as `passthru` - the slides and the webcam tile are already
composited by Teams. One file per slide, dropped into `raw/`, then add its row
to `manifest.tsv`.

A bare webcam recording also works (`mode=pip`): the slide is rendered from the
submission PDF and the face is composited into a Teams-style tile. That is how
Samiran's parts are handled. It looks identical in the final video, but it costs
an extra render step and the slide cannot be animated.

## Why the pipeline looks like this

Nothing the presenters sent matched anything else - 16 fps against 30 fps, h264
against HEVC, 16 kHz mono against 48 kHz stereo, 231 kbps against 15 Mbps. The
concat demuxer needs identical stream parameters, so every clip is rebuilt to
one spec (1920x1080, 30 fps, h264 CRF 21, AAC 192k stereo 48 kHz) before joining.

Audio gets two-pass EBU R128 normalisation to -16 LUFS. Victor's Teams audio is
far quieter and thinner than Samiran's webcam, and without it every speaker
change is a jolt. Measured across the current build, the five segments sit
between -16.1 and -17.2 LUFS.

The PiP geometry in `build.sh` is not guesswork - it was measured off a frame of
Victor's recording so the composited parts sit exactly where Teams puts them:
slide 1674x942 at (0, 68), webcam tile 246x138 at (1674, 94), name pills below
the tile and bottom-left. `make_label.py` recreates those purple name pills.
