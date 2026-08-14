# DLE602 A3 — Submission Checklist (short form)

**Due:** 19 August 2026, 11:55pm AEST · **Today:** 15 August · **4 days left**
**Submit:** report PDF (and DOCX), source code, execution instructions, submission ZIP

This is the academic-side summary. The full engineering gate list lives in the ReviewPulse repo at
[`docs/submission-checklist.md`](https://github.com/lfariabr/review-pulse/blob/main/docs/submission-checklist.md);
that file is authoritative for anything touching artifacts, packaging or the release.

---

## Done

Implementation, frozen experiments, six model artifacts, 363-test suite, clean-room install,
CPU-only inference, deterministic package builder, Juan's 12-case Streamlit QA, and the full
report content including Appendices A–H.

Report source: `report/DLE602_A3_Report_v4.md`, current at `masters-swe-ai@6eaad14`.

---

## Left to do

### 1. Export — blocks submission

The Markdown is complete; the PDF export loses things. Fix and re-export.

- [ ] Word count restored at the end of Section 6, before References (brief requirement)
- [ ] References return to their §7 position; the exporter currently moves them to the end
- [x] Heading reads "Statement of Acknowledgement", not "Acknowledgment"
- [x] Page numbers move to the footer, with the three student IDs
- [x] Cover retitled, generic copyright notice dropped
- [ ] Export **both** DOCX and PDF — Dr Tayab annotates the Word file

Verify after re-export:

```bash
pdftotext v6_DLE602_Faria_L_Assessment_3.pdf export.txt
grep -ic "word count" export.txt   # must be 1 or more, was 0 in v5
```

### 2. Victor — complete

Appendix F is closed. All seven checks record observed command output and a Pass, and Table F2
reports the shipped-artifact results alongside the separately versioned CUDA retrain.

- [x] Independent RQ1/RQ2 validation and CUDA reproduction merged in ReviewPulse PR #123 (`8787a73`)
- [x] Validation record available at `docs/dle602-a3/validation-victor.md`
- [x] F1 clean constrained installation
- [x] F2 `git lfs pull`, six artifacts materialised, no unresolved pointer
- [x] F3 full test suite: 366 passed, zero skips, because that checkout held the licensed corpus
- [x] F4 offline smoke with no SemEval data present
- [x] F5 the explicit counts: 1,120 retained test / 228 mixed / 80 sentences
- [x] F6 Table 3 reproduced **from the shipped artifacts**, kept separate from his retrain
- [x] F7 reference verification — seven cited works audited; the DistilBERT venue uncertainty was resolved against the official EMC² NeurIPS 2019 programme and workshop paper

His fresh DistilBERT retrain stays a separately versioned reproduction and does not replace the
canonical numbers; Table F2 keeps the shipped artifact and the retrain on separate rows.
BERT-Small FP16 stays on the experimental branch as post-submission work, reported in F.3 as a
storage-versus-quality comparison and never as a shipped result.

### 3. Package and release

**Dry run, 15 August, from `review-pulse@8787a73` with no report bundled.** The pipeline is proven
end to end; the final build only adds the report PDF, which changes both digests. The stale July
ZIPs in `dist/` are superseded and must not be shipped: the lightweight one is 11 MB because it was
built before the LFS artifacts were materialised.

| Mode | Bytes | Size | SHA-256 |
|---|---:|---:|---|
| `lightweight` | 54,042,836 | 51.5 MB | `08ee82d7962352aca82f54ad54b82e6e17ac178d590b901d2b58a70f4fcc9181` |
| `all` | 301,248,404 | 287.3 MB | `60f99ae6a2ee28ae773ec3ffe8246a0c6ef0f57a30c55ccbd4c6c180a08f2e30` |

Verified on the extracted lightweight archive: no `.git`, `.venv`, `__pycache__`, `.pytest_cache`,
`.env`, `.DS_Store`, no SemEval XML, no `predictions.csv`, no unresolved LFS pointer. `data/`
carries only `.gitkeep`. Nine artifacts ship: five small v3 models and the four legacy v2 files.
Full suite on the source tree: **363 passed / 3 skipped**, matching the recorded baseline.

- [ ] Confirm the LMS upload limit
- [ ] Rebuild both archives **with the final report PDF** once the export is settled
- [ ] Record the rebuilt sizes and SHA-256 digests, superseding the dry-run values above
- [ ] Extract each to a clean directory and run the documented quickstart
- [ ] Upload both to the LMS; if the larger is refused, put it on OneDrive and include the link
- [ ] Final PDF copied into the package
- [ ] Tag `v3.0.0` — the remote currently carries only `v3.0.0-rc.1`
- [ ] GitHub release notes match the submitted package
- [ ] Close ReviewPulse #88 and #89

### 4. Optional, non-blocking

- [x] Public Streamlit link opens without authentication, confirmed in an incognito session
- [ ] Fix the EV-02E / EV-02F labelling slip in Juan's source document, where the fifth model
      appears twice and the sixth is absent

---

## Order of operations

1. Fix the export and re-export both formats.
2. Refresh `docs/releaseNotes/v3.0.0.md`, which ships inside the package and still reads as a
   release candidate with closed items listed as open gates.
3. Freeze the report and source commits.
4. Build both archives from the frozen commit; extract and retest.
5. Record sizes and digests.
6. Group sign-off.
7. Tag `v3.0.0`, publish the release, submit.

---

## Decisions already taken

- Juan's UI-06/07/08/10/12 findings ship as **accepted risk**, documented and not triaged.
- Anonymous public access is **not** a blocking gate; no report claim depends on it.
- Appendix E is frozen. Its only edit was removing the anonymous-access sentence.
- No retraining. Every number in the report comes from frozen artifacts.
- The canonical four-model experiment stays separate from the exploratory GRU and TextCNN track.
