# Owner handoff — Shadow Archives Phase 1A (architecture, QDN contracts, performance baseline)

> **Subsequent owner acceptance — 2026-09-13: OWNER-RUNTIME PASS.** Gallery,
> Video/Q-Tube, Blog/SubWire and optional Quitter announcement are accepted.
> This supersedes earlier FUTURE / NOT VERIFIED or owner-validation-pending
> statements for those surfaces only. Original observations below remain a dated
> historical record; no new runtime test is claimed by this update.
> See [checkpoint and pinned evidence](2026-09-13-owner-runtime-checkpoint.md).
> Implementation executor: DeepSeek; acceptance: owner; update writer: Codex Local.


## Closure note (2026-09-11)

**This handoff is a historical Phase 1A record.** The owner subsequently
recorded the final Phase 1A decisions **D1–D9** (and the moderation and video
decisions) — see
[`../architecture/2026-09-11-phase-1a-architecture-report.md`](../architecture/2026-09-11-phase-1a-architecture-report.md)
§14, which is now the implementation-authoritative decision record for Phase 1B.
The decision-count reference below was corrected from "D1–D10" to "D1–D9"
during this documentation closure. No application code was scaffolded and
nothing was committed or pushed.

## Task and issue

- **Project:** Shadow Archives web portal (`shadow-archives-webportal`).
- **Phase/task:** Phase 1A — architecture, QDN contracts and performance baseline.
- **Primary objective:** produce the evidence-backed Phase 1A architecture
  package so the owner can approve remaining design decisions and Phase 1B can
  scaffold the Qortal APP without inventing platform behavior or avoidable
  performance/data-model debt.
- **Issue:** not tied to a tracked issue; delivered as an architecture package.
- **Authority limit:** documentation only. No application scaffold, no source
  code, no Git init in the target repository, no commit/push/tag/PR/issue,
  no QDN publication, deployment or transaction.

## Completion status

**PASS WITH OWNER VALIDATION REQUIRED.**

- Phase 1A architecture package produced and self-audited.
- All 18 architecture questions answered; remaining choices are owner decisions.
- Canonical workspace validation passes.
- At handoff time, owner approval was still required on the decision matrix
  (D1–D9) before Phase 1B scaffolding; runtime host validation remains a
  separate gate. (Now resolved — see the closure note above.)

## Files changed

Created (tracked-as-new under `docs/shadow-archives-webportal/architecture/`):

- `2026-09-11-phase-1a-architecture-report.md` (625 lines — main report + decision matrix + self-audit)
- `2026-09-11-qdn-data-contracts.md` (600 lines)
- `2026-09-11-performance-reference-comparison.md` (338 lines)
- `2026-09-11-responsive-appshell-and-design-tokens.md` (318 lines)
- `2026-09-11-phase-1b-implementation-plan.md` (233 lines)

Created (this handoff):

- `docs/shadow-archives-webportal/handoffs/2026-09-11-shadow-archives-phase-1a-handoff.md`

Modified:

- `projects/shadow-archives-webportal.md` — added a "Phase 1A architecture
  package" section that links the artifacts, separates **PROPOSED** items from
  **VERIFIED** facts, updates the verified snapshot, and rewrites "Recommended
  next steps" so scaffolding is gated on the decision matrix. Recommendations
  were not converted into owner decisions.

Removed:

- Two accidental untracked debris directories at the workspace root
  (`Quitter/`, `Subwire/`) each containing only an 86-byte empty
  `package-lock.json`, produced by a stray `npm` invocation during research.
  They were not user work and duplicated nothing; removed to leave the tree clean.

## Implementation summary

No application code was written. The package answers the task scope:

- **Foundation (Q1):** current Vite + React 19 + TypeScript, `createBrowserRouter`
  with `window._qdnBase` basename, HashRouter rejected, provider/error-boundary
  structure, QDN basename handling.
- **UI/dependency (Q2):** measured comparison leads to a no-MUI recommendation
  (CSS design tokens + in-repo components + inline SVG).
- **Performance baseline (Q3):** MEASURED build outputs for a minimal
  React+Router baseline, a MUI subset, the current starter template,
  `qapp-core`-minimal, Quitter, Subwire and q-tube, plus SOURCE-OBSERVED startup
  paths and a recommended startup architecture.
- **Routes (Q4), QDN contracts (Q5), identifier namespace (Q6), catalog (Q7),
  deep search (Q8), engagement (Q9), moderation (Q10), taxonomy (Q11),
  editor/rich text (Q12), Q-Mail contact (Q13), external app links (Q14),
  owner detection (Q15), responsive AppShell (Q16) and design tokens (Q17).**
- **Phase 1B plan (Q18):** bounded scaffold sequence, approved dependency set,
  acceptance checklist.

### Key recommendations (owner approval required where noted)

- **Foundation:** Vite + React 19 + TS; `createBrowserRouter` + `window._qdnBase`.
- **Router:** BrowserRouter family; **HashRouter rejected** for this new app.
- **UI:** no MUI — tokens + in-repo components + SVG (D6).
- **Qortal integration:** in-repo `src/qortal/` layer, **no `qapp-core` root
  import** (root entry statically pulls video.js + MUI ≈ 596 kB gzip) (D7).
- **Identifiers:** `saw_<type>_<id12>`, `saw_cmt_<type><id12>_<uid8>`,
  `saw_lk_<type><id12>`; actor **not** in the identifier (name-scoped likes) (D1).
- **Taxonomy:** hybrid app categories/tags + optional Core mirror (D2).
- **Editor:** TipTap, canonical `tiptap-json-v1` + `bodyText`, single allowlisting
  renderer + DOMPurify (D3/D4).
- **Catalog:** `DOCUMENT` partitioned + manifest (D8); deep search served from a
  local compiled index, never per-keystroke QDN requests.
- **Engagement:** one active like per acting registered **name** per target;
  raw resource count is never the active count; `>= N` when partial (D9).
- **Moderation:** owner overlay = "hidden in Shadow Archives"; never described
  as network deletion.
- **Q-Mail fallback:** retain draft + explain unavailability + copy message to
  clipboard; never silently fall back to `SEND_CHAT_MESSAGE` (D5).
- **Owner detection:** runtime-derived from decoded `_qdnName` + current name
  ownership; capability states visitor / authenticated-no-name /
  authenticated-non-owner / owner; no hardcoded owner.

## Validation executed

- `bash tools/validate-workspace.sh` → **PASS (5 warnings for human review)**.
  The five warnings are pre-existing workspace-wide hygiene hits
  (Qortium/SSH/QAVS/port/legacy-`qortal-ui` mention checks) covering routed
  global guides and this new package; they are expected for their categories,
  not new defects.
- `git diff --check` → clean (exit 0); no conflict markers found
  (`<<<<<<<`, `=======`, `>>>>>>>`) in changed/new files.
- Relative Markdown link check across the architecture package → **NONE broken**.
- Live read-only node re-confirmation (`https://api.qortal.org`, 2026-09-11):
  `APP` resources for `Q-Tube`, `SubWire`, `Quitter` → **READY**.
- Current-source claims checked against the pinned revisions listed in the
  performance comparison §1.
- Target application directory state re-verified (see below).
- No external write of any kind performed.

## Failed or unavailable checks

- **No real-host / dev-proxy runtime measurement.** No browser paint, timing,
  request-count or memory metrics were captured; build-output byte sizes are
  MEASURED, runtime behavior is SOURCE-OBSERVED or INFERRED only. No millisecond
  budget was fabricated. Owner/runtime validation in a real Qortal host remains
  a required, separate gate.
- **No controlled QDN publication test.** Metadata-tag engagement-state
  overwrite behavior, `COMMENT` service with a base64 envelope, clipboard inside
  the production iframe, and Hub behavior under a non-primary owned name remain
  NOT VERIFIED (listed in the report's unresolved unknowns).

## Working-tree state

- Branch `main`, HEAD `e39a881` ("Bootstrap Qortal Development Workflow v2").
- `git status`: `M projects/shadow-archives-webportal.md` plus untracked
  `docs/shadow-archives-webportal/architecture/` and
  `docs/shadow-archives-webportal/handoffs/`. No other tracked changes; no user
  work was overwritten, reverted or restored.
- Target app dir
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
  is **empty** and is **not** a Git repository (no `.git`). No Shadow Archives
  source code exists anywhere.

## Git/external actions performed

- **None.** No commit, push, tag, release, PR, issue, project, QDN publication,
  deployment or Qortal transaction was performed. Upstream repositories were not
  modified. No external write occurred.

## Owner actions required

**Status update (docs closure, 2026-09-11).** Items 1, 3 and 4 below are
resolved: the owner recorded D1–D9, the moderation decision, and the video /
future-Q-Tube decision in
[`../architecture/2026-09-11-phase-1a-architecture-report.md`](../architecture/2026-09-11-phase-1a-architecture-report.md)
§14. Item 3 is decided as: publish own video + preserve future Q-Tube
interoperability as FUTURE / NOT VERIFIED. Item 4 is decided as: no delegated
moderators for alpha. Items 2 and 5 (brand assets/palette; explicit Phase 1B
authorization) remain open.

1. Approve or amend the decision matrix (D1 identifier namespace, D2 taxonomy,
   D3/D4 editor + sanitizer, D5 Q-Mail fallback, D6 UI strategy, D7 `qapp-core`
   usage, D8 catalog service, D9 like-activeness signal).
2. Provide brand font/asset set and final palette (tokens are provisional).
3. Decide whether Shadow Archives publishes its own video media or only
   references other apps' resources.
4. Decide whether delegated moderators are needed (default: publishing-name
   owner only).
5. Authorize Phase 1B scaffolding once decisions are approved.

## Saved Report

- Report type: owner handoff (Phase 1A architecture)
- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-11-shadow-archives-phase-1a-handoff.md`
- File created: yes

## Remaining risks and follow-up issues

- Runtime performance and host behavior are unmeasured; budgets must be set from
  a real host/dev-proxy measurement.
- Several QDN behaviors (like-state metadata, `COMMENT` envelope, clipboard under
  iframe CSP) are NOT VERIFIED and need one controlled publication to prove.
- The identifier namespace and taxonomy/editor choices are blocking decisions
  (D1, D2, D3, D6, D7) for Phase 1B.
- External app names are verified for 2026-09-11 only and must live in
  owner-editable config, not as timeless constants.
