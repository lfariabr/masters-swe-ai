# ITW601 — de-identified public material

This folder contains the public versions of workplace-derived ITW601 project and assessment text.
Study notes about public course resources live under `modules/`. The placement is real; the
people, the school and its vendor systems are not named in workplace-derived prose.

## Rules

| Private detail | Public form |
|---|---|
| People | Their role: academic stakeholder, ICT sponsor, placement supervisor (workplace), academic supervisor (approves and oversees the placement scope), facilitator (the subject lecturer), data owner. The author is named. |
| The school | "the school" (or "an independent school in Sydney" where context needs it) |
| Vendor systems | Generic names: SIS (student information system), LMS (learning management system), report server, data warehouse. Microsoft SSIS and Power BI stay named as generic technology. |
| The workplace repository and its paths | "the workplace repository"; evidence described by kind, not path |
| Staff portal and its modules | "the school portal", "uniform ordering", "mandatory data collection" |
| Data | Counts, statuses and synthetic examples only. No rows, identifiers, screenshots of live data, hostnames or credentials. |
| Dates | Kept when they are project milestones; dropped when they would identify a person or incident. |

## How the files here are produced

`plan.md` and `data-foundation.md` are generated from the private originals by a script and a
replacement map that live in the ignored `../notes/` folder, then checked by a leak scan that must
return zero hits. Do not edit the generated files by hand — change the original and regenerate.
The private generator and replacement map are intentionally absent from a fresh public clone;
that clone must not regenerate these copies without the approved local originals and map.

Journal drafts written from the corner's evidence follow the same rules and pass the same scan
before they are committed or submitted.

## Contents

- [DataWrestler implementation plan](plan.md)
- [Data foundation and proposed ML pipeline](data-foundation.md)
