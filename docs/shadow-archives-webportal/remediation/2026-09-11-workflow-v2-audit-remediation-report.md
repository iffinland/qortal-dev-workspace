# Workflow v2 pre-commit audit remediation report

Date: 2026-09-11. Agent/role: DeepSeek primary local implementer. Task class:
governance/documentation remediation (bounded; no application implementation).

## Task and objective

Remediate every confirmed BLOCKER/HIGH and the concrete MEDIUM findings from the
independent Codex pre-commit audit of the active Qortal Workflow v2 guidance
before the first canonical commit.

Exit criterion: active guidance contains no unresolved BLOCKER/HIGH finding,
reconciles the seven concrete MEDIUM contradictions where they affect active
canonical guidance, preserves the historical audit/bootstrap reports as
evidence, passes structural validation and independent link/whitespace checks,
survives an adversarial self-audit, and is ready for a focused Codex
correction-diff review.

## Status

`PASS WITH OWNER VALIDATION REQUIRED`

Automated and structural work is complete and verified. The remaining explicit
gates are the independent Codex correction-diff review requested by the task and
owner authorization for any initial commit or push. No application runtime or
live QDN/host evidence is required or claimed for this documentation task.

Source audit:
[`../audits/2026-09-11-independent-workflow-v2-pre-commit-audit.md`](../audits/2026-09-11-independent-workflow-v2-pre-commit-audit.md).
Historical bootstrap:
[`../bootstrap/2026-09-11-qortal-workflow-v2-bootstrap-report.md`](../bootstrap/2026-09-11-qortal-workflow-v2-bootstrap-report.md).
Neither historical file was modified.

## Baseline and authority

- Repository: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`.
- Branch: unborn `main`; no commits; all workspace content untracked.
- Remote: `origin https://github.com/iffinland/qortal-dev-workspace.git`
  (tracking shown as `[gone]`; zero refs at audit time). No commit, push, tag,
  release, QDN publication, deployment, transaction or GitHub mutation occurred.
- Platform contracts were re-verified against the read-only clones under
  `/tmp/qortal-investigation/` at the revisions recorded in the standard:
  Core `108bf191…`, Hub `12a573b2…`, `qapp-core` `0f9d6ac5…`.
- Existing uncommitted workspace content was treated as user-owned and
  preserved; only the intended active-guidance files were edited.

## Files changed

1. `agents/qortal-qdn-and-bridge.md` — H1, M7; retry/timeout and validation
   reconciliation.
2. `agents/qortal-architecture-and-data-integrity.md` — H2 global rendering
   rule; M5 entity-vs-operation and authority corrections.
3. `agents/qdn-publication-discovery-and-scaling.md` — M1, M2, M3; retry-policy
   refinement.
4. `agents/live-qdn-validation.md` — M1 intended-revision verification.
5. `agents/app-release-and-provenance.md` — M1, M3.
6. `docs/architecture/qortal-dapp-development-standard.md` — H1, H2, M1, M2, M5
   and a malicious-fixture validation requirement.
7. `docs/governance/source-of-truth-and-lifecycle.md` — M6 authority split.
8. `README.md` — H1 summary reconciliation; M4 validator-scope correction.
9. `projects/shadow-archives-webportal.md` — new owner decisions; H2 reference;
   M5 open product decision; revision-scoping of the unlike convention.
10. `tools/validate-workspace.sh` — M4 scope, failure behavior, reference-style
    link and heading-anchor support, historical-report exclusion.
11. `templates/IMPLEMENTATION-ISSUE.md` — rich-text malicious-fixture checklist.
12. `templates/PROJECT-CONTEXT.md` — rendering-safety/trust-boundary checklist.
13. New: this report.

## Finding-by-finding remediation

### H1 — GET_USER_ACCOUNT / permission classification

- `agents/qortal-qdn-and-bridge.md` §2 was rewritten from a two-way
  reads-vs-writes split into three approval classes: (1) public/idempotent node
  reads, (2) permissioned host-mediated reads/authentication, (3) signed
  approved writes.
- `GET_USER_ACCOUNT` is now explicitly a permissioned authentication/account
  operation, not an approval-free read. Documented behavior: first-time
  permission request, previously remembered permission, session permission,
  user rejection, and unresolved/pending approval.
- Requirements added: no ordinary short background-read deadline on an
  unresolved permission dialog; no automatic retry of a rejection or unresolved
  approval; no duplicate concurrent prompts; deduplicated account/auth requests;
  bounded retries only for genuinely idempotent public reads.
- Evidence re-verified: Hub `src/qortal/get.ts` (`getUserAccount` saved/session
  permission + `getUserPermission`, rejection throws), Hub
  `src/qortal/qortal-requests.ts` (`GET_PRIMARY_NAME` host dispatch), Core
  `q-apps.js` one-hour default timeout for `GET_USER_ACCOUNT`.
- Reconciled summaries: `README.md` platform-model bullet; standard §4 new
  "permissioned authentication" paragraph and §5 intro; architecture guide
  unchanged except cross-reference.

### H2 — untrusted HTML / rich-text rendering boundary

- Added a reusable global rule at
  `agents/qortal-architecture-and-data-integrity.md` §11 "Render untrusted
  content safely". Schema validation, publisher authority and rendering safety
  are separated; plain text is escaped; rich HTML is sanitized with a maintained
  sanitizer or a constrained safe document model; scripts, event-handler
  attributes and executable markup are blocked; URL schemes are validated and
  `javascript:`/`data:` handled intentionally; media/link and post-sanitization
  transformations must not reintroduce unsafe markup; owner-authored content is
  not exempt.
- Applied conceptually to comments, rich-text posts, imported content, owner
  preview, cached/stored content and any other publisher.
- Standard §6 gained "Rendering safety is a separate gate" and a pointer to the
  global rule; §14 now requires malicious HTML/URL fixtures in static/automated
  checks.
- Project context references the global rule instead of duplicating it. The
  Shadow Archives editor/sanitizer library remains undecided.
- No application code was written and no editor library was chosen.

### M1 — publication revision / intended content verification

- Standard §5, `agents/live-qdn-validation.md` §3,
  `agents/qdn-publication-discovery-and-scaling.md` §3 and
  `agents/app-release-and-provenance.md` §6 now separate publication
  submission, transaction confirmation, resource availability/status and
  intended-revision/content verification, and require comparing the served
  resource against the intended operation (revision/version/content-hash/exact
  relevant payload). A `READY` resource alone is no longer presented as proof
  of a new revision. No universal QDN version field was invented.

### M2 — node API parameters vs bridge SEARCH_QDN_RESOURCES fields

- `agents/qdn-publication-discovery-and-scaling.md` §4 and standard §8/§9 now
  label the lowercase names as node endpoint query parameters and document the
  bridge action's camelCase fields separately: `includeStatus`,
  `includeMetadata`, `exactMatchNames`, `minLevel`, `nameListFilter`, plus
  `names` (array) versus singular `name`. Verified against Core
  `q-apps.js`. Lowercase REST names sent to the bridge are documented as
  silently ignored.
- Identifier matching is documented as substring matching unless
  `prefix: true`; exact identity requires post-filtering `service`, `name` and
  `identifier`, and null/default identifiers are distinguished. Verified against
  `HSQLDBArbitraryRepository.java` (`LIKE '%…%'` vs `'…%'`).
- Fixed the project scalability example that still used lowercase bridge names.

### M3 — multi-file ZIP publication

- `agents/qdn-publication-discovery-and-scaling.md` §1 and
  `agents/app-release-and-provenance.md` §5 no longer claim in-app multi-file
  publication is unavailable. They document `isMultiFileZip` /
  `uploadType: 'zip'` as source-supported for the inspected Hub revision, with
  host approval, correct ZIP/root layout, an explicit caution that source
  support is not proof of a successful live publication, and a runtime
  validation requirement. Verified against Hub `src/qortal/get.ts`.

### M4 — workspace validator scope

- `README.md` now describes the checker as a structural gate, states it is not
  semantic proof, preserves semantic/source (and live where applicable) review
  as a separate mandatory gate, and notes historical reports are excluded from
  the stale-marker check.
- `tools/validate-workspace.sh` rewritten: `set -uo pipefail`, fatal errors exit
  non-zero, checker execution failures fail, reference-style local link
  definitions are validated, local heading anchors are validated (GitHub-style
  slug with duplicate suffixes), and the stale `24891` marker is hard-failed in
  active guidance only. Historical reports are excluded so honest quotation of
  an obsolete assumption cannot cause a false hard failure. No keyword-ban
  validator was built.

### M5 — engagement semantics

- Standard §10 and `agents/qortal-architecture-and-data-integrity.md` §2/§4 now
  distinguish a content entity from an interaction/operation resource. Authority
  applies to the operation resource being created/updated; the target/parent
  reference is validated independently and need not be owned by the actor, so
  liking/commenting on another author's content no longer requires owning the
  target.
- Like counts: raw matching-resource count is not the active-like count;
  tombstone/inactive state must be interpreted before counting and exact target
  identity validated. The placeholder/delete convention is marked
  revision-scoped framework behavior, not a timeless Core rule.
- Transport is documented as operation-specific; tips and shares are not
  universally prescribed as QDN publications.
- The unresolved "one like per user" choice (account/address vs acting
  registered name) is recorded explicitly in the project context as a required
  owner decision and was not resolved here.

### M6 — owner decisions vs implementation-state authority

- `docs/governance/source-of-truth-and-lifecycle.md` now splits
  "Factual / implemented-state authority" from "Product / authorization
  authority". Owner decisions determine desired behavior and authorize changes;
  a conflicting implementation is evidence of an implementation gap and does not
  automatically override an owner decision; owner decisions cannot override
  verified platform facts.

### M7 — external HTTP(S) link behavior

- `agents/qortal-qdn-and-bridge.md` §8 no longer states a workspace-wide
  copy-to-clipboard working assumption. It now requires each project to define
  an explicit external-link policy compatible with current host/platform
  behavior and security rules, with verified host support.
- The Shadow Archives copy-to-clipboard decision remains in
  `projects/shadow-archives-webportal.md` only, labelled as project-specific and
  not a global Qortal rule.

### L1 — archive-date provenance correction

- `qortal-ui` remains correctly excluded as current authority.
- The historical bootstrap report associated `qortal-ui`'s archived state with
  2025-06-14. The GitHub repository banner reports archive date July 5, 2025.
  The earlier bootstrap provenance date was inaccurate. The historical bootstrap
  report was **not** rewritten; this correction report records the discrepancy.
- No active canonical guide contained the incorrect date; only the historical
  bootstrap report did, so no active guide needed a date change.

## New Shadow Archives owner decisions recorded

In `projects/shadow-archives-webportal.md`:

- **Publishing name:** `Shadow Archives` (human-readable canonical publishing
  name).
- **QDN service:** `APP`.
- **Identifier/prefix:** still undecided; deliberately not invented.
- Platform encoding (for example percent-encoding of spaces) is handled only
  where technically required; the product identity is not redefined as the
  encoded string.
- The project's external-link copy-to-clipboard policy is confirmed as
  project-specific.

## Validation executed

| Check | Command | Result |
| --- | --- | --- |
| Workspace structural validator | `bash tools/validate-workspace.sh` | PASS, exit 0, 5 expected hygiene warnings |
| Script syntax | `bash -n tools/validate-workspace.sh` | exit 0 |
| Independent Markdown link/anchor check (Python) | full-tree scan of inline links, reference definitions and anchors | 33 files, 164 relative targets, 0 broken |
| Validator fixture behavior | disposable `/tmp/qvtest.*` copy | missing inline link → FAIL; bad anchor → FAIL; reference-style missing target → FAIL; valid reference/anchor → PASS; historical `24891` → PASS; active `24891` → FAIL |
| CRLF scan | `grep -rlU $'\r'` over all files incl. untracked | none |
| Conflict-marker scan | `grep -rnE '^(<{7}|={7}|>{7})( \|$)'` | none |
| Trailing-whitespace scan | `grep -rnE ' +$'` | none |
| Per-file whitespace check | `git diff --no-index --check /dev/null <file>` for all 34 files | 0 warnings |
| Tree/status inspection | `find`, `git status --short --branch`, `git remote -v` | see below |

Only the historical bootstrap report contains tab characters (inside a code
block); it is historical evidence and was intentionally not rewritten. Active
guidance has no tabs.

## Adversarial self-audit

| Check | Verdict |
| --- | --- |
| `GET_USER_ACCOUNT` still described as approval-free somewhere | CLEAR — only negations remain ("is not an approval-free read") |
| Automatic retry guidance that can repeat a user denial | CLEAR — rejection/unresolved explicitly not retried |
| Security guidance that treats schema validation as HTML safety | CLEAR — three concerns separated in both the guide and the standard |
| Sanitizer guidance ignoring dangerous URLs / post-sanitization transformations | CLEAR — `javascript:`/`data:` and post-sanitization reintroduction covered |
| `READY`/status presented as proof of the new publication revision | CLEAR — revised in four active locations |
| REST query argument names copied into bridge actions | CLEAR — split and mapped; project example fixed |
| Obsolete claim that multi-file ZIP publication is unavailable | CLEAR — corrected in both locations |
| Validator documentation promising semantic proof | CLEAR — structural scope stated, semantic review a separate gate |
| Raw resource count presented as active-like count | CLEAR — corrected in the standard |
| Target-content ownership confused with operation-resource authority | CLEAR — corrected in guide and standard |
| Owner product decisions subordinated to current implementation | CLEAR — authority split in the governance file |
| Shadow Archives clipboard behavior present as a global rule | CLEAR — global guide now requires a per-project policy; the decision lives only in the project file |

No new BLOCKER/HIGH finding was confirmed during the self-audit. No new MEDIUM
contradiction originating from the audit was left unfixed. One documentation
residual noted for the correction-diff review: the historical bootstrap report
still shows `includestatus`/`includemetadata` and the 2025-06-14 archive date;
these are historical-evidence statements and were deliberately not rewritten.

## Not verified / limitations

- No Shadow Archives application code was inspected, built or run; the
  application source directory remains empty.
- No live Qortal host, node API, QDN publication or account permission dialog
  was exercised. H1/H2/M1/M2/M3 are documented from current source and the
  independent audit, not from live runtime.
- Host/version parity with the inspected Hub revision was not re-established;
  the standard's Reference-revisions re-verification requirement still applies
  before dependent work.
- The independent Codex correction-diff review has not yet been performed.

## Unresolved owner decisions

- Shadow Archives identifier/prefix scheme (not invented here).
- Which editor/sanitizer library to use.
- "One like per user": per Qortal account/address (A) or per acting registered
  name (B).
- Taxonomy model (fixed `Category` enum vs free-form tags vs both).
- Contact-form Q-Mail fallback and success feedback.
- Owner controls beyond the publishing name (delegated moderators).
- Whether report files enter the initial commit.

## Git / external action state

- Commit state: **not committed** (unborn `main`; no commits).
- Push state: **not pushed** (no refs advertised; no push issued).
- No tag, release, QDN publication, deployment, transaction, issue/PR mutation,
  or other external write was performed.
- Working tree: all workspace content remains untracked; this report is a new
  untracked file.

## Owner next actions

1. Request the focused Codex correction-diff review of the twelve edited files
   plus this report.
2. Decide the unresolved owner decisions above before shadow-archives
   scaffolding.
3. Authorize (or withhold) the initial commit/push explicitly; none was taken.

## Saved report

- Report type: remediation / correction report
- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/remediation/2026-09-11-workflow-v2-audit-remediation-report.md`
- File created: yes
