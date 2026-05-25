---
name: gh-issue-creator
description: Create GitHub subject-tracking issues for this masters repository by using the lfariabr/gh-issue-creator repository. Use when asked to create module issues, assessment issues, subject epics, labels, or milestones based on a subject README or recent closed issue patterns.
---

# GH Issue Creator

Use this skill to create subject issue sets in `lfariabr/masters-swe-ai` in the same style as prior terms, while routing batch issue creation through `https://github.com/lfariabr/gh-issue-creator`.

## Required Tool

Treat the GitHub repository as the canonical source:

```bash
https://github.com/lfariabr/gh-issue-creator
```

Use one of these setup paths:

```bash
git clone https://github.com/lfariabr/gh-issue-creator /private/tmp/gh-issue-creator
python3 /private/tmp/gh-issue-creator/issue_creator.py --help
```

or download only the script:

```bash
curl -fsSL -o /private/tmp/issue_creator.py https://raw.githubusercontent.com/lfariabr/gh-issue-creator/main/issue_creator.py
python3 /private/tmp/issue_creator.py --help
```

If a clone already exists in a temporary path, update it with `git -C /private/tmp/gh-issue-creator pull` before use. Do not hardcode a user-machine-specific path.

## Workflow

1. Resolve repository and subject context.
   - Confirm the GitHub repo from `git remote -v` or `gh repo view`.
   - Read the subject README and supporting notes if needed.
   - Check for existing issues before creating anything:
     ```bash
     gh issue list --state all --limit 1000 --search <SUBJECT_CODE> --json number,title,state,url
     ```

2. Copy the current repo pattern.
   - Inspect recent closed issues:
     ```bash
     gh issue list --state closed --limit 30 --json number,title,body,labels,milestone,closedAt,url
     ```
   - In this repo, subject issue sets normally use:
     - `[Epic] <SUBJECT>-Modules`
     - `[Epic] <SUBJECT>-Assessments`
     - `Module N: <module title>`
     - `Assessment N: <type> - <title>`
     - labels: subject label plus `learning`, `assessment`, and `epic`
     - assessment milestones attached only to assessment issues

3. Prepare labels and milestones before the batch create.
   - `gh-issue-creator` can attach labels and milestones, but it does not create them.
   - Check labels:
     ```bash
     gh label list --limit 100 --json name,color,description
     ```
   - Create the subject label if missing. Use a distinct readable color and description:
     ```bash
     gh label create <SUBJECT_CODE> --color <HEX> --description "<Subject name> subject"
     ```
   - Check milestones:
     ```bash
     gh api --method GET 'repos/<owner>/<repo>/milestones?state=all&per_page=100'
     ```
   - Create subject-prefixed assessment milestones if missing:
     ```bash
     gh api repos/<owner>/<repo>/milestones -f title='<SUBJECT> Assessment 1 Due' -f description='<deliverable>' -f due_on='YYYY-MM-DDT00:00:00Z'
     ```
   - Verify due dates after creation because GitHub timezone display can be surprising.

4. Generate a JSON template for `gh-issue-creator`.
   - Write the template outside the repo by default, for example `/private/tmp/<subject>-issues.json`, unless the user wants a committed artifact.
   - Include all epics, module issues, and assessment issues in one JSON template.
   - Use placeholder epic bodies if child issue numbers are not known yet, then update epics after creation.
   - Use milestone titles, not numbers, in the JSON template because `gh issue create --milestone` accepts milestone names.
   - Example issue object:
     ```json
     {
       "title": "Module 1: Introduction to Big Data and Analytics",
       "body": "**Week 1** - Introduction to Big Data and Analytics\n\n**Learning Outcomes:** SLO a\n\n**Parent Epic:** #TBD\n\n---\nPart of BDA601 Big Data and Analytics learning modules.",
       "labels": ["learning", "BDA601"],
       "assignees": [],
       "milestone": null
     }
     ```

5. Dry-run, inspect, then create.
   - Always run a dry-run first:
     ```bash
     python3 /private/tmp/gh-issue-creator/issue_creator.py --template /private/tmp/<subject>-issues.json --repo <owner>/<repo>
     ```
   - If the user already asked to create the issues and the dry-run exactly matches the requested scope, proceed with:
     ```bash
     python3 /private/tmp/gh-issue-creator/issue_creator.py --template /private/tmp/<subject>-issues.json --repo <owner>/<repo> --create
     ```
   - If the dry-run reveals duplicates, missing labels, missing milestones, or an unexpected issue count, stop and resolve that before creating.

6. Update parent epics after creation.
   - List the new subject issues:
     ```bash
     gh issue list --state open --label <SUBJECT_CODE> --limit 50 --json number,title,labels,milestone,url
     ```
   - Update the module epic with actual module issue numbers.
   - Update the assessment epic with actual assessment issue numbers, due dates, weights, dependencies, and milestone names.
   - Use `gh issue edit --body-file` or the GitHub connector if available.

7. Verify and report.
   - Verify the final issue set:
     ```bash
     gh issue list --state open --label <SUBJECT_CODE> --limit 50 --json number,title,labels,milestone,url
     ```
   - Confirm:
     - expected issue count
     - subject label on every issue
     - `learning` labels on module issues and module epic
     - `assessment` labels on assessment issues and assessment epic
     - `epic` label on both epics
     - assessment milestones attached to assessment issues
   - Final response should list created epics, module issue range, assessment issues, labels, milestones, and any assumptions.
