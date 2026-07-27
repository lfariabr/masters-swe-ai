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

| Slides | Presenter | Source | Status |
|---|---|---|---|
| 2, 9, 11 | Samiran | `samiran_slide*.mov` | built |
| 3 | Victor | `victor_a.mp4` | built |
| 8 | Victor | `victor_b.mp4` | built |
| 10 | Victor | - | **missing** |
| 1, 4, 5, 6, 7, 12 | Luis | - | missing |

Victor sent two files. Scene detection and frame checks confirm each one holds a
single slide start to finish (3 and 8), so slide 10 (Ethical considerations) was
never recorded.

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
