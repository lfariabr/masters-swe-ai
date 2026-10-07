# Final-file pass

Run this on the **submission export**: a `.docx` or `.pdf` whose file name contains the student's surname (`Faria`). Search `<assessment-dir>/` and its `_drafts/`. Briefs are named after the subject, so the surname keeps them out. If several exports match, check the newest pair and name it in the report.

Each check ends in PASS or a one-line fix for the report. The pass is done when every check has a result and every PDF page has been looked at.

## 1. Fresh files

- `stat` both files. The PDF must be newer than the `.docx`; an older PDF is **stale** and needs a new export.
- A Word lock file (`~$` plus the file name) in the same folder means Word still has the document open, and unsaved edits are not in the file. Ask the student to close Word, then check.

## 2. Text and word count from the file itself

- Extract the text: `textutil -convert txt -output <scratch>/export.txt <file>.docx`.
- Count each assessable section from this text. textutil prints the next heading's list number as a lone `•` at the end of each section; drop it, or every section counts one word high.
- If Steps 2-4 ran on a Markdown copy, diff it against this text and report any difference, even one word.

## 3. Clean document

- `unzip -p <file>.docx word/document.xml | grep -c '<w:ins \|<w:del '` returns 0: no tracked changes.
- `unzip -l <file>.docx | grep comments` returns nothing: no comments.

## 4. Contents table and heading numbers

- The contents table is cached text that Word refreshes only on request. Compare each entry (paragraphs styled `TOC1`, `TOC2` and so on) with the body heading it points to: numbers and wording must match. Fix: right-click the table → Update Field → Update entire table.
- Every numbered heading sits on one list: the same `<w:numId w:val="…"/>` in `word/document.xml`. A heading on its own list numbers differently, for example "4.3" beside "4.2.". Fix: Format Painter from a correctly numbered heading, then refresh the contents table.

## 5. Styling and cover facts

- Product and software names in the body are plain text.
- In each reference, the italics cover the work's title, or the journal name with its volume, and nothing else.
- The cover page's name, student ID, subject code, assessment number and lecturer match the subject README.

## 6. Live links

- Each reference URL and DOI is a hyperlink in the Word file: `unzip -p <file>.docx word/_rels/document.xml.rels` lists it with `TargetMode="External"`. A plain-text URL stays plain in every export. Fix: select it in Word → Cmd+K → paste the same URL.
- `pdfinfo -url <file>.pdf` lists the links in the PDF. A URL that wraps across lines is listed once per line.

## 7. The PDF itself

- `pdfinfo`: `Creator` is Microsoft Word and `Tagged` is yes. A Quartz producer means Print → Save as PDF, which drops links and tags. Fix: File → Save As → PDF, "Best for electronic distribution and accessibility".
- `pdffonts`: every font shows `emb yes`.
- The `pdftotext` text matches the `.docx` text, apart from words hyphenated at line breaks.
- Render every page (`pdftoppm -r 60 -png <file>.pdf <scratch>/page`) and look at each one: figures and tables present, nothing cut off, headings and contents table as expected.
