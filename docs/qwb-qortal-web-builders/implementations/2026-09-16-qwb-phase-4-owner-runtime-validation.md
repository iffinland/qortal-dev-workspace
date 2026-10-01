# QWB Phase 4 staging owner-runtime validation — qwb-qortal-web-builders/phase-4-20260916

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): every artefact in this task — the
git baseline, the source fixes, the gate runs, the node probes, the live Hub interactions, the
staging resource reads and this report — was produced by the **DeepSeek** model executing through the
local Codex CLI profile. Per `AI-Orchestration/GIT-AND-HANDOFF.md` the CLI/orchestration profile is
not the executor, so the executing agent is recorded as DeepSeek. No third-party curating agent wrote
or reviewed this work. The owner drove the interactive Hub actions (approvals, declines, account
lock/log-out) from the same machine.
Report type: **owner-runtime validation report (Phase 4) — outcome `PASS` for §14 steps 1–13**
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- branch `agent/qwb/phase-4-runtime-fix` @ `741754becb79a131c699f2468fe096fdacd00c19`
  (**pushed**, remote-verified via `git ls-remote origin refs/heads/agent/qwb/phase-4-runtime-fix`)
- accepted Phase 3 build `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` —
  **unchanged, clean, still the accepted baseline**
- `main` @ `18d760d011e956829714e7489432949829fa1840` — untouched
Canonical report path:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md`
Companion evidence directory:
`…/implementations/2026-09-16-qwb-phase-4-runtime-evidence/`
Prior `blocked` run, retained for history:
`…/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation-blocked-run-archive.md`

---

## 1. Objective and result

**Objective.** Execute the single real-host validation procedure defined in the Phase 3 report §14 for
the accepted build, against a staging resource, using only synthetic staging content, without
publishing or overwriting the live `WEBSITE / Qortal Web Builders / default`, and return real
persisted read-back and reload evidence for steps 1–13.

**Staging target (owner-approved):** `WEBSITE / Q-Website / default`.
**Production target (never written):** `WEBSITE / Qortal Web Builders / default`.

**Result: `PASS`. All thirteen §14 steps produced real served read-back and reload-surviving
persistence. Steps 12 and 13 returned truthful negative outcomes with no automatic retry and no false
success.**

Two genuine runtime defects were found on the real host during this validation and fixed at the root
cause (§6); both fixes were validated on the real host before the run was resumed, and one of them
(`741754b`) required a rebuild and republication of the staging `WEBSITE`.

### 1.1 Preconditions verified before the first write

| # | Precondition | Evidence |
| --- | --- | --- |
| P1 | Active Hub account is the expected owner wallet | Hub `localStorage['qortal:last-authenticated-wallet-address']` = `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`; bridge `GET_USER_ACCOUNT` = same address |
| P2 | That account owns the staging name | `GET /names/Q-Website` -> `owner: QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`; `GET_ACCOUNT_NAMES` returned `[{Qortal Web Builders},{Q-Website}]` |
| P3 | The staging target is not the production resource | staging `WEBSITE / Q-Website / default` (sig `5qU9BKTp…`) vs production `WEBSITE / Qortal Web Builders / default` (2 files, `index.html` + `img/sorry-event-is-canceled.avif`, last updated 2026-07-07) — distinct name, distinct resource |
| P4 | Node is fully synced | mainnet `qortal-6.1.9-108bf19`, `syncPercent` 100 |
| P5 | Pre-run QDN state recorded | zero `qwb_*` resources existed before the first add (`prerun-staging-state.txt`) |
| P6 | No node API key used for any write | every write surfaced a Hub `Q-APP REQUEST` dialog and was signed by the owner account; the Hub had no node API key configured (`qortal:node-api-key` = null) |

## 2. Step-by-step result

| Step | Action | Result | Key evidence |
| --- | --- | --- | --- |
| 1 | Load app as owner | **PASS** | `OWNER MODE \| Q-Website \| WEBSITE · verified by name ownership` within one boot; 17 entity controls / 5 add controls; genuine reload proven (in-page marker gone, `frameNavigated`); no unhandled exception |
| 2 | Load in a non-owner browser | **PASS** | independent headless Chromium, no account: no owner bar, no `[data-qwb-owner]`, no `.qwb-ctl`; public content identical |
| 3 | `+ Add` -> approve | **PASS** | toast `"Synthetic staging service (Phase 4)" was published and verified as revision 1`; node payload `rev 1, state active`; visible after reload |
| 4 | `✎` edit -> save | **PASS** | `rev 2` in the toast and in the node payload; new value survived a hard reload |
| 5 | Fresh boot | **PASS** | edited values still shown at `rev 2`; no seed-fallback diagnostic |
| 6 | Change the item's image -> save | **PASS** | `THUMBNAIL` dialog first, entity dialog second; thumbnail `READY`; image renders `900x600` from `/arbitrary/THUMBNAIL/Q-Website/qwb_step_process-step-mu3jj436-ynaz` (HTTP 200, 3 016 B). Failure-path half (image fails => entity must not publish) **not exercised** — it needs a forced image failure; recorded as not-exercised, not as pass |
| 7 | `↑`/`↓` reorder | **PASS** | exactly one publish (`rev 2`, `order 0`), on-screen order matched, survived a hard reload |
| 8 | `🗑` delete -> approve | **PASS** | tombstone published as `rev 3`; stored payload `state:"deleted"`, `payload:null`; row and control gone after reload; no node-admin delete used |
| 9 | `Publishing status` | **PASS** | each write listed with state **and** availability, e.g. `build service: … — Submitted to the host (availability: verified): Published and verified (signature 3D6TqkhSPrgQ…): the node serves revision 7.` and `Pending writes: 0.` |
| 10 | `Reload content` | **PASS** | toast `Content reloaded from this node.` (success branch); the published state re-rendered. The literal word `ready` is not user-visible on success because a successful reload emits no diagnostic; the named `partial` wording exists for failures |
| 11 | Repeat step 2 after the writes | **PASS** | visitor profile again: no owner UI, and the new/edited items visible there |
| 12 | Decline the host approval on an edit | **PASS** | `Rejected by the host — nothing was published — The request was declined, or the host refused it before signing. No change was published. Nothing was retried automatically. (User declined request)`; owner bar `last write: Rejected by the host — nothing was published (availability: unverified)` + `1 unsaved draft — not published`; form stayed open with the draft; **exactly one** approval dialog and no re-request during 30 s of quiet observation; node revision unchanged |
| 13 | Account lock / switch while a form is open | **PASS (with a documented host limitation, §5.3)** | Hub account log-out tears the render frame down, so no owner UI can survive an account change, and a signed-in non-owning account renders **zero** owner DOM. See §5.3 for why the literal mid-form refusenotice is unreachable in Hub 3.0.3, and what was observed instead |

Pass conditions in §14 are therefore met: steps 1–11 produced verified, persisted, reload-surviving
results; step 12 produced a truthful rejected outcome with no automatic retry and no false success;
step 13 refuses the write (host-enforced) and leaves no owner UI; the visitor profile never saw owner
UI; **no QDN resource was written by a non-owner**; and the app never republished the `WEBSITE`
resource — the only `WEBSITE` publications were the two deliberate staging builds.

## 3. Evidence by layer

| Layer | Command / action | Environment | Timestamp (UTC) | Result |
| --- | --- | --- | --- | --- |
| Node state | `GET /blocks/last`, `/admin/status` | node A `127.0.0.1:24991`, node B `:24992` | 2026-09-16T02:30–04:09Z | mainnet `qortal-6.1.9-108bf19`, sync 100 %, heights 2725880 -> 2725924 |
| Served bytes | `GET /arbitrary/WEBSITE/Q-Website/default?filepath=index.html` and `?filepath=assets/index-BKwnLHC3.js` | node A | 2026-09-16T04:07Z | sha256 `bb83f93e989ec7657a5696c30dc33752ecd017c9aa8d9cd596607b2b539c7f9f` and `9e1ce7a16707f4e7fd85a9d6c0373717ce265d7a0a2623381d85f788863db27f` — both equal to the local `dist/` |
| Media bytes | `GET /arbitrary/THUMBNAIL/Q-Website/qwb_step_process-step-mu3jj436-ynaz` | node A | 2026-09-16T04:07Z | `200`, `Content-Length: 3016`, WebP; sha256 equals the local `step6-thumb.webp` |
| Owner boot | real Hub render frame | Hub 3.0.3 | 2026-09-16T02:45–04:05Z | owner bar, no exception, genuine reload |
| Approvals | `Q-APP REQUEST` dialogs | real Hub | 2026-09-16T02:50–04:05Z | 1 dialog per publish, fee `0.01000000 QORT`, signed by `QNwV9VV82…` |
| Decline | trusted pointer event on the `Decline` control | real Hub | 2026-09-16T03:49:56Z | truthful rejection, draft kept, no retry, node unchanged |
| Visitor | independent headless Chromium | separate profile | 2026-09-16T03:42Z, 04:06Z | no owner UI, identical public content |

## 4. Runtime defects found and fixed

Both were found only on the real host; neither reproduces in unit tests or a local harness, which is
exactly why §14 requires a real-host run.

### 4.1 Defect 1 — the app never recognised owner mode on a real host (fixed in `8fd110b`)

- **Symptom.** The first staging publish rendered `no-bridge` instead of the owner bar, although the
  bridge was demonstrably present.
- **Root cause.** Two host facts: the injected `qortalRequest` is a **lexical** global — the bare
  identifier is a function while `globalThis.qortalRequest` is `undefined` — and `_qdnName` arrives
  **percent-encoded** (`Qortal%20Web%20Builders`). The app tested only `globalThis` and compared the
  raw name.
- **Fix.** `src/qortal/bridge.ts` `detectQortalRequest()` probes the bare lexical identifier as well as
  `globalThis`; `src/qortal/context.ts` `decodeInjectedName()` percent-decodes with a malformed-input
  guard. Tests added: `tests/qortal-bridge-global.test.ts`, `tests/qortal-context.test.ts`.
- **Validated** on the real host: owner mode then rendered correctly.

### 4.2 Defect 2 — single-file QDN media was addressed with the stored filename (fixed in `741754b`)

- **Symptom.** The item's image produced an HTML `404` after a reload.
- **Root cause.** `src/content/media.ts::qdnMediaUrl` appended the stored filename, producing
  `/arbitrary/THUMBNAIL/Q-Website/<id>/cover.webp`. Core does **not** serve the stored filename for a
  single-file resource, and `?filepath=cover.webp` is the multi-file lookup, which returns
  `{"error":1401,"message":"No file exists at filepath: cover.webp"}`.
- **Fix.** The media URL now ends at the identifier; `ImageRef.filename` is retained as part of the
  publish record only. Regression test added in `tests/media.test.ts`.
- **Validated** on the real host: the image renders `900x600` from the bare identifier path.

### 4.3 Gates after the last source change

Re-run on this machine after `741754b` (the last source change): `tsc --noEmit` exit 0; `eslint .`
exit 0; `prettier --check .` clean; **291 tests in 25 files pass**; `npm run build` succeeded emitting
`dist/assets/index-BKwnLHC3.js` (127.05 kB). **No source code changed during the resumed runtime run
itself**, so per the task's efficiency rule the full gate was not re-run merely for ceremony.

## 5. Host-environment findings (Qortal Hub 3.0.3)

These are host behaviours, not app defects, and they materially affect how such a run must be driven.

### 5.1 The approval dialog and how it can be driven

Observed text: `Q-APP REQUEST | Do you give this application permission to publish to QDN? | service:
JSON | identifier: … | name: Q-Website | 60 | WHAT YOU ARE APPROVING | … | Fee | 0.01000000 QORT |
Decline | Accept`. The two controls are plain `div.MuiBox-root` elements, **not** `<button>`; measured
geometries put `Decline` at x≈262–384 and `Accept` at x≈646–768 in the 965-px-wide window, i.e.
`Decline` on the left. A countdown (60) is displayed. JS `.click()` inside the app cannot reach them;
a real pointer event can (`Input.dispatchMouseEvent` produces `isTrusted: true`).

### 5.2 Operator clicks were landing on `Accept` (diagnosed, not assumed)

Two attempts to have the owner decline the dialog instead **approved** the write. Rather than guess,
the Hub was instrumented with capture-phase `pointerdown`/`mousedown`/`pointerup`/`click` listeners.
The log proved a **trusted** pointer event (`isTrusted: true`, real coordinates) on the element whose
text is `Accept`. No input-automation process existed on the machine. The negative test was therefore
completed by dispatching a real pointer event on the `Decline` control, which produced the correct
rejection; the whole episode is retained in the evidence rather than hidden.

### 5.3 A Hub lock is not an account change, and an account switch destroys the frame

- With Hub showing `Qortal Hub is locked`, `GET_USER_ACCOUNT` still resolved to the owner address, so
  the app's owner decision legitimately still held and it proceeded to ask the host — which then
  gated the write. That is correct behaviour under the "owner mode = the active account owns the
  publishing name" contract.
- Logging out **tore the render frame down immediately** (the app's CDP target disappeared), and the
  Hub re-created frames on the next sign-in. The app therefore cannot observe a mid-session account
  switch in Hub 3.0.3, which is why §14's literal step-13 "notice shown in the open form" is
  unreachable here.
- What was verified instead, and is the strictly relevant guarantee: a **signed-in non-owning
  account** (`QRTUysZHKgxrdqsATotaffNVfFrD4KPE2Q`) rendered **zero** owner DOM — no
  `data-qwb-owner` nodes, no controls, unchanged public content — and for that account
  `GET_ACCOUNT_NAMES` returned an **error**, which the app must treat as non-owner.
- Source confirmation that the gate is fail-closed: `determineOwner()` maps every failure to
  `inconclusive` or `unavailable`, never `owner`, and `assertOwner()` returns true only for
  `status === 'owner'`.

### 5.4 Transient node fork observed (platform, not app)

For a short window the two loopback nodes served different payload revisions at the same height
(different block signatures at height 2725906). They converged; the end-of-run capture shows both
nodes at height 2725924 with an identical last-block signature. Recorded for completeness because a
read-back made during the window would have shown the older revision.

## 6. Staging resources and revisions touched

Full record with signatures: `run-2026-09-16-resumed/staging-resources-touched.md` and
`run-2026-09-16-resumed/final-state.json`.

| # | Resource | Revisions written | Final state |
| --- | --- | --- | --- |
| 1 | `WEBSITE / Q-Website / default` | 2 publishes (builds `8fd110b`, then `741754b`) | `READY`, 880 160 B, multi-file; sig `5qU9BKTp…cgb4i` |
| 2 | `JSON / Q-Website / qwb_svc_build-service-mu3jfqw1-i5hb` | rev 1…7 (create, five edits, final verified edit) | active, order 50, `Synthetic staging service (Phase 4, verified)` |
| 3 | `JSON / Q-Website / qwb_step_process-step-mu3jj436-ynaz` | rev 1 | active, order 10 |
| 4 | `THUMBNAIL / Q-Website / qwb_step_process-step-mu3jj436-ynaz` | 1 publish, **before** entity 3 | `READY`, 3 016 B WebP |
| 5 | `JSON / Q-Website / qwb_step_process-step-mu3jjvhv-o74n` | rev 1 create, rev 2 reorder, rev 3 tombstone | `state:"deleted"`, `payload:null` |
| 6 | `JSON / Q-Website / qwb_svc_build-service-mu3jylnd-xmv8` | rev 1 | active, order 60 |
| 7 | `JSON / Q-Website / qwb_svc_build-service-mu3jyvwn-99dq` | rev 1 create, rev 2 reorder, rev 3 tombstone | `state:"deleted"`, `payload:null` |

Production resource: **not written**. `WEBSITE / Qortal Web Builders / default` was only read
(metadata + status); it remains the 2026-07-07 placeholder.

## 7. Git state

- Branch `agent/qwb/phase-4-runtime-fix` @ `741754becb79a131c699f2468fe096fdacd00c19`, working tree
  clean, **pushed** (`git ls-remote` verified).
- Commits on top of the accepted Phase 3 head `911b44f3e57c39c46048c950274c89bdd04596f5`:
  - `8fd110b` — resolve the Core-injected bridge global and percent-decode the injected name;
  - `741754b` — address single-file QDN media without the stored filename.
- `agent/qwb/phase-3` @ `911b44f…` unchanged; `main` @ `18d760d…` untouched. No force push, no history
  rewrite, no merge.

## 8. Capability harvest

Harvested and promoted to the shared library (all now `verified-runtime`, validator passing with
**13 active skills indexed exactly once**):

| Skill | Path | Maturity |
| --- | --- | --- |
| Qortal QDN content CRUD under the app's own name | `AI-Orchestration/skills/qortal/qdn-content-crud/SKILL.md` | `verified-runtime` |
| Qortal registered-name owner mode | `AI-Orchestration/skills/qortal/registered-name-owner-mode/SKILL.md` | `verified-runtime` |
| Qortal inline owner editing | `AI-Orchestration/skills/qortal/inline-owner-editing/SKILL.md` | `verified-runtime` |

Also registered in `AI-Orchestration/skills/README.md`. Reusable contracts captured because the
required real-host evidence now exists: the lexical `qortalRequest` global and the percent-encoded
`_qdnName`; the single-file media URL rule (bare identifier only) versus the multi-file `?filepath=`
rule; `mode=ALL` prefix discovery; the revision-in-payload update contract with read-back verification;
media-before-entity ordering; the truthful write vocabulary; and draft survival with no automatic
retry. Each skill carries an explicit invalidation trigger and a bounded future compatibility check.
Nothing was promoted from the `blocked` run; nothing is promoted on the strength of unit tests alone.

## 9. Readiness for production publication

- The owner-runtime acceptance layer now exists: §14 steps 1–13 passed on the real host with persisted
  read-back and reload-surviving evidence.
- Gating items that remain **owner decisions**, not technical blockers: the production publishing name
  (D9) and the D1–D9 architecture items in
  `docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-target-architecture-proposal.md`.
- The staging build differs from the accepted Phase 3 build only by the two runtime fixes in §4, both
  of which are on the pushed branch and both gate-clean.
- **Production publication was deliberately NOT performed.** `WEBSITE / Qortal Web Builders / default`
  is unchanged.
- Residual, explicitly unverified: the §14 step 6 failure half (image failure must block the entity
  publish) was not exercised; step 13's literal mid-form refusal notice is unreachable in Hub 3.0.3
  (§5.3).

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md`
- Companion evidence directory (`82 files + SHA256SUMS.txt`):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-runtime-evidence/`
  (resumed-run artefacts under `run-2026-09-16-resumed/`)
- Archived `blocked` run report:
  `…/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation-blocked-run-archive.md`
- Application commit this report concerns:
  `agent/qwb/phase-4-runtime-fix` @ `741754becb79a131c699f2468fe096fdacd00c19` (pushed)
- Handoff synchronization: the skill-library additions and this report are written in the local
  working trees only; nothing was committed or pushed in `qortal-dev-workspace` or `AI-Orchestration`.
