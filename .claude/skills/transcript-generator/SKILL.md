---
name: transcript-generator
description: Transcribe a local audio/video file (lecture recording, meeting, podcast) into a text transcript plus SRT subtitles, fully offline using whisper.cpp on Apple Silicon. Use when asked to transcribe an mp4/mov/m4a/wav/mp3, generate a transcript or captions from a media file, or get the text of a recorded lecture.
argument-hint: "<path-to-media-file> [model]"
---

# Transcript Generator — Local Media → Text + Subtitles

You turn a local audio/video file into a clean `.txt` transcript and a timestamped `.srt`
subtitle file, fully offline, using `whisper.cpp` (Metal-accelerated on Apple Silicon).
Built for macOS + Homebrew. The file size of the video is irrelevant — only the **audio
duration** matters.

## Arguments

- **Media file path**: `$0` (e.g. `~/Downloads/lecture.mp4`). Required. If missing, ask the user.
- **Model**: `$1` (optional). One of `small.en`, `medium.en` (default), `large-v3`.
  - `small.en` (~470 MB) — fast draft, clean English audio.
  - `medium.en` (~1.5 GB) — **default**, best balance for lectures in English.
  - `large-v3` (~3 GB) — best accuracy, heavy jargon, or **non-English / mixed-language**
    audio (e.g. Portuguese). The `.en` models are English-only.

## Step 0 — Verify input

Run `ls -lh "<media>"`. If the file does not exist, stop and tell the user what you looked for.

## Step 1 — Ensure dependencies

Check `which ffmpeg whisper-cli`. If either is missing:

```bash
brew install whisper-cpp ffmpeg
```

Run this in the **background** (it can take a few minutes) and wait for it to finish before
continuing. If `brew` itself is missing, stop and tell the user to install Homebrew.

## Step 2 — Ensure the model (cached & reused)

Models live in `~/.cache/whisper/` as `ggml-<model>.bin` and are reused across runs.
If the chosen model file is missing, download it (in the **background**, 0.5–3 GB):

```bash
mkdir -p ~/.cache/whisper
curl -L -C - -o ~/.cache/whisper/ggml-<model>.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-<model>.bin
```

`ggml-medium.en.bin` is normally already cached, so the default run skips this step.

## Step 3 — Extract audio (16 kHz mono WAV)

`whisper.cpp` requires a 16 kHz mono PCM WAV:

```bash
ffmpeg -y -i "<media>" -ar 16000 -ac 1 -c:a pcm_s16le "<basename>.wav"
```

For anything longer than a few minutes, run in the **background**; confirm exit `0` and that
the `.wav` exists. Optionally report duration with
`ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "<basename>.wav"`.

## Step 4 — Transcribe

Run in the **background** (long for >20 min audio; roughly real-time or faster on M-series):

```bash
whisper-cli -m ~/.cache/whisper/ggml-<model>.bin -f "<basename>.wav" \
  -otxt -osrt -of "<output-base>" -t 8 -pp
```

- Produces `<output-base>.txt` (clean text) and `<output-base>.srt` (timestamped).
- Default `<output-base>` = the media path without its extension, in the same folder.
  Honor an output directory if the user specifies one.
- Monitor progress by reading the background task's output file and looking for
  `progress = NN%` and the latest `[hh:mm:ss --> ...]` timestamp.

## Step 5 — Clean up & report

- Delete the intermediate `.wav` (large and disposable). **Keep** the cached model.
- **Never delete the user's original media file** unless they explicitly ask.
- Report the output paths. If useful, read the `.txt` and give a 3–5 bullet summary of what
  the recording covers.

## Notes

- Apple GPU (Metal) is used automatically; `-t 8` sets CPU threads for the non-GPU parts.
- This skill was extracted from the MLN601 Week-1 lecture transcription workflow.
- If the user has many recordings to do, keep the model cached and only re-run Steps 3–5.
