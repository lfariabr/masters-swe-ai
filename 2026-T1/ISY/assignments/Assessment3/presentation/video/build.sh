#!/usr/bin/env bash
#
# Assemble the ISY503 Assessment 3 group presentation video.
#
# The three presenters recorded separately and nothing matches: Victor and Luis
# used Microsoft Teams screen-share (slides + webcam tile burned in, 16 fps,
# 16 kHz mono), Samiran sent bare webcam footage with no slides at all
# (HEVC, 30 fps, 48 kHz). The concat demuxer needs byte-identical stream
# parameters, so every clip is rebuilt to one spec before joining.
#
# Samiran's clips are composited onto slides rendered from the submission PDF,
# reproducing the Teams layout measured off Victor's recording, so all three
# speakers look like one continuous session.
#
# How to run:   ./build.sh              (builds every slide listed in manifest.tsv)
#               ./build.sh 2 9 11       (rebuilds only those slides, then re-concats)
# How to test:  ./build.sh --verify     (ffprobe report over the segments + output)
#
# Rows marked mode=missing are skipped with a warning, so the video can be
# assembled incrementally as recordings arrive.

set -euo pipefail

cd "$(dirname "$0")"

RAW=raw
WORK=work
SLIDE_PDF=../../submission/ISY503_Faria_L_Assessment_3_Presentation.pdf
OUT=../../submission/ISY503_Faria_L_Assessment_3_Presentation.mp4

# --- target spec -------------------------------------------------------------
W=1920; H=1080; FPS=30
CRF=21; PRESET=slow
ARATE=48000; ABITRATE=192k
GOP=$((FPS * 2))

# --- Teams layout, measured from a frame of Victor's recording ---------------
# Slide occupies the left of the canvas, webcam tile top-right, name pills below
# the tile and bottom-left. Everything else is black.
SLIDE_W=1674; SLIDE_H=942; SLIDE_X=0;    SLIDE_Y=68
TILE_W=246;   TILE_H=138;  TILE_X=1674;  TILE_Y=94
PILL_X=1684;  PILL_Y=296
BAR_X=8;      BAR_Y=1050

VF_COMMON="fps=${FPS},format=yuv420p"
X264="-c:v libx264 -preset ${PRESET} -crf ${CRF} -profile:v high -pix_fmt yuv420p \
      -g ${GOP} -keyint_min ${GOP} -sc_threshold 0 -fps_mode cfr"
AAC="-c:a aac -b:a ${ABITRATE} -ar ${ARATE} -ac 2"

mkdir -p "$WORK"

log()  { printf '\033[1m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[33m[skip]\033[0m %s\n' "$*" >&2; }

# Two-pass EBU R128 loudness normalisation. Victor's 16 kHz Teams mono is much
# quieter and thinner than Samiran's webcam audio; single-pass dynamic loudnorm
# pumps on speech, so measure first and apply the fixed correction.
loudnorm_filter() {
  local src=$1 ss=$2 dur=$3
  local json
  json=$(ffmpeg -nostdin -hide_banner -nostats -ss "$ss" ${dur:+-t "$dur"} -i "$src" \
    -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 \
    | sed -n '/^{/,/^}/p')
  python3 - "$json" <<'PY'
import json, sys
m = json.loads(sys.argv[1])
print(
    "loudnorm=I=-16:TP=-1.5:LRA=11"
    f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
    f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
    f":offset={m['target_offset']}:linear=true:print_format=summary"
)
PY
}

# Render one slide of the deck at the size it occupies inside the Teams layout.
#
# The deck was exported to PDF as A4 landscape (842x595pt), not 16:9, so every
# page carries the 16:9 slide letterboxed between two white bands. Forcing the
# page to 1674x942 would both stretch the slide and bake those bands in, so
# render at the target width and crop the centre band out.
render_slide() {
  local n=$1 out="$WORK/slide_$(printf '%02d' "$1").png"
  [[ -f $out ]] && { echo "$out"; return; }
  pdftoppm -png -f "$n" -l "$n" -scale-to-x $SLIDE_W -scale-to-y -1 \
    "$SLIDE_PDF" "$WORK/_slide_tmp"
  python3 - "$WORK" "$out" "$SLIDE_W" "$SLIDE_H" <<'PY'
import glob, sys
from PIL import Image
work, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
src = glob.glob(f"{work}/_slide_tmp-*.png")[0]
im = Image.open(src)
band = round(im.width * 9 / 16)
top = round((im.height - band) / 2)
im.crop((0, top, im.width, top + band)).resize((w, h), Image.LANCZOS).save(out)
PY
  rm -f "$WORK"/_slide_tmp-*.png
  echo "$out"
}

# The purple name pills Teams burns into Victor's frames, recreated for Samiran.
render_labels() {
  local name=$1 slug=$2
  [[ -f $WORK/label_tile_$slug.png ]] || python3 make_label.py "$name" "$WORK/label_tile_$slug.png" 226
  [[ -f $WORK/label_bar_$slug.png  ]] || python3 make_label.py "$name" "$WORK/label_bar_$slug.png"  246
}

# Segments are named by manifest row, not by slide, because a slide can need more
# than one row: Luis fluffed a line mid-way through slide 12, so that slide is two
# takes from the same source with the bad stretch cut out between them.
build_segment() {
  local row=$1 slide=$2 speaker=$3 mode=$4 src=$5 tin=$6 tout=$7
  local seg="$WORK/seg_$(printf '%02d' "$row").mp4"
  local dur=""
  [[ $tout != "-" ]] && dur=$(python3 -c "print(round($tout - $tin, 3))")

  local af; af=$(loudnorm_filter "$src" "$tin" "$dur")
  af="${af},aresample=${ARATE}"

  if [[ $mode == passthru ]]; then
    # Already the target layout - just conform frame rate, size and audio.
    ffmpeg -nostdin -y -v warning -nostats -ss "$tin" ${dur:+-t "$dur"} -i "$src" \
      -vf "scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2,${VF_COMMON}" \
      -af "$af" $X264 $AAC -movflags +faststart "$seg"
  else
    local slide_png label_tile label_bar slug
    slide_png=$(render_slide "$slide")
    slug=$speaker
    render_labels "$SPEAKER_NAME" "$slug"
    label_tile="$WORK/label_tile_$slug.png"
    label_bar="$WORK/label_bar_$slug.png"

    ffmpeg -nostdin -y -v warning -nostats -loop 1 -i "$slide_png" \
      -ss "$tin" ${dur:+-t "$dur"} -i "$src" -i "$label_tile" -i "$label_bar" \
      -filter_complex "\
        color=c=black:s=${W}x${H}:r=${FPS},format=rgba[canvas];\
        [0:v]scale=${SLIDE_W}:${SLIDE_H},format=rgba[slide];\
        [canvas][slide]overlay=${SLIDE_X}:${SLIDE_Y}[bg];\
        [1:v]fps=${FPS},scale=${TILE_W}:${TILE_H},format=rgba[tile];\
        [bg][tile]overlay=${TILE_X}:${TILE_Y}:shortest=1[a];\
        [a][2:v]overlay=${PILL_X}:${PILL_Y}[b];\
        [b][3:v]overlay=${BAR_X}:${BAR_Y},format=yuv420p[v]" \
      -map "[v]" -map 1:a -af "$af" -shortest \
      $X264 $AAC -movflags +faststart "$seg"
  fi
  log "built $seg"
}

speaker_name() {
  case $1 in
    luis)    echo "Luis Faria" ;;
    victor)  echo "Victor Javier Dorantes Meneses" ;;
    samiran) echo "Samiran Shrestha" ;;
    *)       echo "$1" ;;
  esac
}

verify() {
  log "segment uniformity"
  printf '%-22s %-6s %-10s %-7s %-6s %-4s %s\n' FILE CODEC RES FPS RATE CH DUR
  for f in "$WORK"/seg_*.mp4; do
    [[ -e $f ]] || continue
    ffprobe -v error -of csv=p=0 \
      -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate,channels \
      -show_entries format=duration "$f" \
      | tr '\n' ' ' | awk -v n="$(basename "$f")" \
        '{printf "%-22s %s\n", n, $0}'
  done
  if [[ -f $OUT ]]; then
    log "output"
    ffprobe -v error -of default=noprint_wrappers=1 \
      -show_entries format=duration,size,bit_rate "$OUT"
  fi
}

concat() {
  local list="$WORK/concat.txt" total=0 row=0 missing=()
  : > "$list"
  while IFS=$'\t' read -r slide speaker mode src tin tout; do
    [[ $slide == \#* || -z ${slide:-} ]] && continue
    row=$((row + 1))
    local seg="$WORK/seg_$(printf '%02d' "$row").mp4"
    if [[ -f $seg ]]; then
      echo "file '$(basename "$seg")'" >> "$list"
      total=$((total + 1))
    else
      missing+=("slide $slide ($speaker)")
    fi
  done < manifest.tsv

  (( total > 0 )) || { echo "nothing to concat" >&2; exit 1; }
  log "concatenating $total segments"
  ( cd "$WORK" && ffmpeg -nostdin -y -v warning -f concat -safe 0 -i concat.txt \
      -c copy -movflags +faststart "../$OUT" )

  if (( ${#missing[@]} )); then
    warn "NOT in the video yet: ${missing[*]}"
  fi
  log "wrote $OUT ($(du -h "$OUT" | cut -f1))"
}

# --- main --------------------------------------------------------------------
if [[ ${1:-} == --verify ]]; then verify; exit 0; fi

ONLY=("$@")
ROW=0
while IFS=$'\t' read -r slide speaker mode src tin tout; do
  [[ $slide == \#* || -z ${slide:-} ]] && continue
  # Increment before filtering so row numbers stay stable on partial rebuilds.
  ROW=$((ROW + 1))
  if (( ${#ONLY[@]} )); then
    [[ " ${ONLY[*]} " == *" $slide "* ]] || continue
  fi
  if [[ $mode == missing ]]; then
    warn "slide $slide ($speaker) not recorded yet - expecting $src"
    continue
  fi
  [[ -f $src ]] || { warn "slide $slide: $src not found"; continue; }
  SPEAKER_NAME=$(speaker_name "$speaker")
  log "slide $slide - $SPEAKER_NAME ($mode)"
  build_segment "$ROW" "$slide" "$speaker" "$mode" "$src" "$tin" "$tout"
done < manifest.tsv

concat
verify
