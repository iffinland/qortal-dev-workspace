# Report Storage Policy

## Purpose

Define the single canonical location for AI-generated Qortal work reports so
that handoffs are predictable, discoverable by ChatGPT/DeepSeek/Codex, and
separated from durable project documentation.

## Canonical report root

```
/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/<project-slug>/
```

Agents MUST NOT place these reports in an individual application repository's
`docs/` directory.

**OWNER DECISION (bootstrap, 2026-09-11).** For Qortal, the canonical report
root is inside this workspace repository, under `docs/<project-slug>/`. The
sibling Qortium workspace used a separate root outside its repository; Qortal
does not need that indirection and does not use SSH. Consequence: report files
may become git-tracked. Therefore report content MUST NOT contain secrets,
credentials, private keys, wallet seeds or private user data.

## Issue report location

All reports tied to an issue MUST use:

```
<workspace-root>/docs/<project-slug>/issues/
```

This includes issue investigations, implementations, runtime diagnostics,
validation, agent reviews, corrections and owner handoffs. Keep the report type
in the filename rather than creating a different directory for each phase.

## Non-issue report categories

For work that is genuinely not tied to an issue, use these report-type
subdirectories when applicable:

| Directory                              | Report type                     |
| -------------------------------------- | ------------------------------- |
| `docs/<project-slug>/audits/`          | audit reports                   |
| `docs/<project-slug>/investigations/`  | investigation reports           |
| `docs/<project-slug>/implementations/` | implementation reports          |
| `docs/<project-slug>/runtime/`         | runtime diagnostics             |
| `docs/<project-slug>/validation/`      | live-host / live-QDN validation |
| `docs/<project-slug>/reviews/`         | DeepSeek reviews, Codex reviews |
| `docs/<project-slug>/handoffs/`        | owner handoffs                  |
| `docs/<project-slug>/bootstrap/`       | workspace/organization bootstraps |

Also covered by this policy:

- comparison reports;
- pilot measurements;
- temporary technical findings that must be retained.

Do not create every directory in advance. Create only the required `issues/` or
non-issue report-type directory when a report is actually written.

## Project slug rules

- Use lowercase kebab-case matching the project name (e.g.
  `shadow-archives-webportal`, `q-tube`, `subwire`).
- The slug is derived from the project's repository or workspace directory name.

## File naming

Use the format:

```
YYYY-MM-DD-<task-or-issue>-<report-type>.md
```

Examples:

```
docs/shadow-archives-webportal/bootstrap/2026-09-11-qortal-workflow-v2-bootstrap-report.md
docs/shadow-archives-webportal/issues/2026-09-20-issue-12-review.md
docs/shadow-archives-webportal/runtime/2026-09-21-home-header-runtime-report.md
```

Use lowercase kebab-case throughout.

## Report storage vs. project documentation

### Workspace report storage

```
/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/<project-slug>/
```

For:

- issue-scoped reports under `issues/`;
- audits, investigations, implementations;
- runtime diagnostics;
- live-host/live-QDN validation reports;
- comparison reports;
- DeepSeek and Codex reviews;
- owner handoffs;
- bootstrap records;
- pilot measurements.

### Project repository documentation

```
<application repository>/docs/
```

Only for durable source-controlled documentation such as:

- project architecture;
- data-model documentation;
- user or operator guides;
- release instructions;
- migration specifications;
- API documentation;
- permanent diagnostics documentation that is part of the application itself.

## Directory creation behavior

- Missing `docs/<project-slug>/` directories are created automatically when the
  first report for that project is written.
- Missing `issues/` or non-issue report-type subdirectories are created
  automatically when the first matching report is written.
- Agents MUST NOT pre-create unused directories.

## Prohibited locations

Agents MUST NOT write AI-generated work reports into:

- any application repository's `docs/` directory;
- `agents/`, `projects/` or `templates/` in this workspace;
- the workspace's `docs/architecture/`, `docs/governance/` or `docs/workflows/`
  trees, which are reserved for workspace documentation;
- any temporary or scratch directory outside the canonical root.

## Required final report path disclosure

Every final report MUST include the exact absolute path where it was saved:

```
Report saved:
/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/<project-slug>/<type>/<filename>
```

If no report file was created, state:

```
Report saved:
Not created — <reason>
```

Agents MUST NOT claim that a report was saved unless the file exists on disk.

## Related files

- [`deepseek-primary-work-model.md`](deepseek-primary-work-model.md)
- [`../../agents/final-report-and-owner-handoff.md`](../../agents/final-report-and-owner-handoff.md)
- [`../../agents/00-SESSION-START.md`](../../agents/00-SESSION-START.md)
- [`../../templates/DEEPSEEK-TASK.md`](../../templates/DEEPSEEK-TASK.md)
- [`../../templates/OWNER-HANDOFF.md`](../../templates/OWNER-HANDOFF.md)
