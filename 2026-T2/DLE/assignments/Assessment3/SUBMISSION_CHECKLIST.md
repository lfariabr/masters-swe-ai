# DLE602 A3 — Submission Checklist (short form)

**Due:** 19 August 2026, 11:55pm AEST · **Today:** 13 August · **6 days left**
**Submit:** report PDF (and DOCX), source code, execution instructions, submission ZIP

This is the academic-side summary. The full engineering gate list lives in the ReviewPulse repo at
[`docs/submission-checklist.md`](https://github.com/lfariabr/review-pulse/blob/main/docs/submission-checklist.md);
that file is authoritative for anything touching artifacts, packaging or the release.

---

## Done

Implementation, frozen experiments, six model artifacts, 363-test suite, clean-room install,
CPU-only inference, deterministic package builder, Juan's 12-case Streamlit QA, and the full
report content including Appendices A–H.

Report source: `report/DLE602_A3_Report_v4.md`, current at `masters-swe-ai@419f7ab`.

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

### 2. Victor — scientific validation delivered; Appendix F release checks remain

Hard cutoff: **16 August**. Rows without evidence are removed from the appendix, never shipped
as empty claims.

- [x] Independent RQ1/RQ2 validation and CUDA reproduction merged in ReviewPulse PR #123 (`8787a73`)
- [x] Validation record available at `docs/dle602-a3/validation-victor.md`
- [ ] F1 clean constrained installation
- [ ] F2 `git lfs pull`, six artifacts materialised, no unresolved pointer
- [ ] F3 full test suite, not the 48 focused tests
- [ ] F4 offline smoke with no SemEval data present
- [ ] F5 the explicit counts: 1,120 retained test / 228 mixed / 80 sentences
- [ ] F6 Table 3 reproduced **from the shipped artifacts**, kept separate from his retrain
- [x] F7 reference verification — seven cited works audited; the DistilBERT venue uncertainty was resolved against the official EMC² NeurIPS 2019 programme and workshop paper

His fresh DistilBERT retrain stays a separately versioned reproduction and does not replace the
canonical numbers. The second PR must validate the shipped artifacts without running the training
runner. BERT-Small FP16 stays on the experimental branch as post-submission work.

### 3. Package and release

- [ ] Confirm the LMS upload limit
- [ ] Build both archives: `lightweight` (~52 MB) and `all` (~288 MB)
- [ ] Record both sizes and SHA-256 digests
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
2. Land Victor's second PR with the remaining Appendix F release evidence, or remove unevidenced rows.
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
