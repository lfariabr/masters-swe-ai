# DLE602 A2 - Presentation (Review Pulse v2)

First version of the 5-7 minute audio-visual proposal seminar. Built in **Marp** so the
same markdown renders straight to the **PDF** the brief requires, and speaker notes travel
with each slide for the voice-over.

- `DLE602_A2_Slides_v1.md` - the deck (7 slides: 6 content + references). Speaker notes are
  the HTML comments under each slide (`<!-- PRESENTER ... -->`).
- Content mirrors `../DLE602_A2_Presentation_Outline.md` and the report; slides carry visual
  cues only, not the full report (rubric requirement).

## How to render to PDF

**Option A - VS Code (no install):** install the *Marp for VS Code* extension, open the deck,
then "Export slide deck..." -> PDF.

**Option B - CLI:**
```bash
npx @marp-team/marp-cli DLE602_A2_Slides_v1.md --pdf --allow-local-files
# speaker notes + slides (for rehearsal):
npx @marp-team/marp-cli DLE602_A2_Slides_v1.md --pdf --pdf-notes
# editable slides if the group prefers PowerPoint:
npx @marp-team/marp-cli DLE602_A2_Slides_v1.md --pptx
```

Submission naming (per brief): `DLE602GroupnameAssessment2.pdf` and the recording `...mp4`.

## Speaking split (~equal time, rubric)

| Presenter | Slides | Time |
|---|---|---|
| **Victor** (literature) | 1 Title, 3 Literature | ~115 s |
| **Juan** (project mgmt) | 2 Problem, 5 Plan & risks | ~120 s |
| **Luis** (methods) | 4 Approach, 6 Contribution | ~120 s |

## Before recording - checklist

- [ ] Add Victor + Juan **student IDs** on the title slide (currently `[ID]`)
- [ ] Render to **PDF**, check the flow diagrams and colours survived the export
- [ ] Rehearse to land inside **5-7 min**; each member ~equal time
- [ ] Record voice-over (online: audio only, no webcam); save as `...Assessment2.mp4`
- [ ] Keep template/fonts/colours consistent (already themed here - do not fork styles)
