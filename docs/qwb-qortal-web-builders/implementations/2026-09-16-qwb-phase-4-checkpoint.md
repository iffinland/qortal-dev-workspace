# QWB Phase 4 checkpoint closure and production-readiness state — qwb-qortal-web-builders/phase-4-checkpoint-20260916

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): the source analysis, the pre-fix
reproduction, the isolated worktree, the gate runs, the documentation synchronization and this report
were produced by the **DeepSeek** model executing through the local Codex CLI profile
(`CODEX_HOME=/home/iffi/.codex-deepseek`, `model = "deepseek-flash"`, `model_provider = "deepseek"`).
Per `AI-Orchestration/GIT-AND-HANDOFF.md` the CLI/orchestration profile is not the executor.
Report type: **implementation + validation report (Phase 4 checkpoint closure)**
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- **release candidate** `agent/qwb/phase-4-runtime-fix` @ `7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a`
  (**pushed, remote-verified** by `git ls-remote origin refs/heads/agent/qwb/phase-4-runtime-fix`)
- accepted Phase 3 baseline `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` —
  unchanged
- `main` @ `18d760d011e956829714e7489432949829fa1840` — untouched, **not merged**
Canonical report path:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-checkpoint.md`
Companion evidence directory:
`…/implementations/2026-09-16-qwb-phase-4-checkpoint-evidence/`
Entry report (Phase 4 owner-runtime validation, `PASS`):
`…/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md`

---

## 1. Objective and result

**Objective.** Close the development/runtime-validation phase before production publication:
synchronize the canonical documentation with the accepted state, make the Phase 4 report/evidence and
the three verified-runtime skills durable under the canonical Git/handoff rules, and settle one
production-bootstrap edge case from the actual code.

**Result: checkpoint closed.** The bootstrap edge case is a **real defect**, it was reproduced on the
release candidate, the smallest correct fix was implemented and validated, the documentation is
synchronized, and the branch is pushed. **Production was not published and
`WEBSITE / Qortal Web Builders / default` was not touched.**

| Item | Outcome |
| --- | --- |
| Bootstrap edge case | **Real defect**, reproduced at `741754b`; fixed in `e7bf357` |
| Transition validation (zero → first write → reload → second write) | PASS (pre-fix: FAIL) |
| Gate on the checkpoint HEAD | typecheck / eslint / prettier clean, **294 tests in 25 files**, build OK |
| Canonical documentation | synchronized (application README + `docs/architecture.md`, workspace project context, orchestration registry + skill index) |
| Phase 4 report/evidence durability | workspace documentation branch pushed |
| Three verified-runtime skills durability | orchestration documentation branch pushed |
| Production publication | **not performed** (out of scope) |

## 2. Production-bootstrap edge case — analysis from the actual code

### 2.1 The question

Zero QDN content renders the full shipped seed bundle. After the first published entity, does the QDN
source render only the seed shell plus published entities, so that progressively editing the initial
seed site makes untouched seed entities disappear after reload?

### 2.2 The answer: yes, at `741754b`

Read path in `src/content/qdn-source.ts` at the release candidate `741754b`:

1. `load()` builds `bundle` from `emptyBundle(seed.site)` or `emptyBundle(site.site)` — i.e. **empty
   entity lists**, not the seed entity lists.
2. Each kind is then assigned wholesale: `bundle = withKind(bundle, read)`, where `withKind` returns
   `{ ...bundle, highlights: read.entities }`. `read.entities` is **only** what discovery returned and
   hydrated for that kind.
3. The full seed bundle is rendered in exactly one place: the `nothing-published` early return, which
   requires `entityCount === 0 && tombstones === 0 && site.site === null && searchErrors === 0 &&
   simplyUnpublished`.

Consequence: the first successful write makes `entityCount > 0`, so the early return can never fire
again. Every kind is thereafter exactly its discovered set. A shipped item that has never been
published is in no discovered set, so it stops rendering — and its inline `✎ / 🗑 / ↑ / ↓` controls
stop rendering with it. Those controls are the **only** way that item can ever be published, so the
approved §6.4 flow ("replace the shipped content one entity at a time through the inline editor")
could not bootstrap: the owner could replace the first entity and then lose the controls for
everything else.

Two further details from the same code path:

- the `site` singleton is a fixed-identifier read, so the shell, brand, hero, contact and footer copy
  survive; the loss is at **entity** level (highlights, services, steps, works, prices, articles);
- **media** entities are unaffected in kind, but the same wholesale replacement applies to a media
  file that was published before its entity.

**Reproduced, not inferred.** The three test cases added by the fix were run unchanged against a
detached worktree of `741754b` (application source untouched):
`…/2026-09-16-qwb-phase-4-checkpoint-evidence/bootstrap-transition-prefix-failure.txt`. Two fail
there — after the first published highlight only **1 of the 2** shipped highlights renders
(`expected [ … ] to have a length of 2 but got 1`), and a tombstoned shipped item is immediately
resurrected in the visitor view.

### 2.3 The smallest correct fix (implemented in `e7bf357`)

`src/content/qdn-source.ts` gained `KindRead.identifiers` (every identifier discovery returned for the
kind, after the exact name/service/prefix re-filter, whatever the payload read then did with it) and
`applySeedBaseline(read, shipped)`, which adds a shipped item **only when discovery did not report its
identifier at all**, and only when that kind's discovery actually answered without hitting the page
budget. The baseline is per entity, has no flag or mode, and ends by itself once every shipped
identifier has been published or tombstoned. A diagnostic
(`bootstrap-defaults: N shipped item(s) render from the seed …`) reports how many items currently
render this way.

Why this is the smallest correct change rather than a broader redesign:

- it reuses the existing per-kind read result; no new module, store, importer, migration or index;
- no duplicate rendering is possible, because the identifier is the entity identity and the inline
  editor re-publishes the existing identifier — `assembleDraft` takes `id: request.id`, the edit flow
  passes `id: entity.id`, and no form field can change it;
- it preserves the existing truthfulness invariant — a reported identifier (active, tombstoned,
  invalid or unreadable) is **never** replaced by its shipped default, so "exists but failed to load"
  stays a reported failure and a tombstone cannot resurrect;
- a discovery that failed or was truncated contributes **no** default, consistent with
  `agents/qortal-architecture-and-data-integrity.md` ("partial discovery MUST NOT grant authority") —
  the fail-closed direction, with a diagnostic;
- termination is emergent, not a state to clean up.

## 3. Transition validation

`tests/qdn-source.test.ts` — `pre-publication bootstrap baseline`, through the real bridge wrapper and
the real read/publish modules against the scripted node (`tests/support/qdn.ts`), the whole way
through zero content → first write → reload → second write:

| Case | At `741754b` | At `7fd03fc` |
| --- | --- | --- |
| Untouched shipped items survive the transition (2/2 highlights, all other kinds intact across both reloads) | **FAIL** (1/2) | PASS |
| A shipped item the owner tombstoned is never resurrected | **FAIL** | PASS |
| The baseline contributes nothing once every identifier is reported | PASS | PASS |

Evidence: `bootstrap-transition-prefix-failure.txt` (pre-fix) and `bootstrap-transition-test.txt`
(post-fix) in the companion evidence directory.

**Not re-run, deliberately:** the Hub 3.0.3 owner-runtime run. This change is a read-path merge rule;
the write, owner-mode and inline-editing contracts, their interlocks and their runtime evidence are
unchanged. See §6 for the one consequence that matters for publication.

## 4. Gate on the checkpoint HEAD

`…/2026-09-16-qwb-phase-4-checkpoint-evidence/gates-checkpoint.txt`, all at
`7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a`, node v20.19.2:

| Command | Result |
| --- | --- |
| `npm run typecheck` (`tsc --noEmit`) | clean |
| `npm run lint` (`eslint .`) | clean |
| `npm run format:check` (`prettier --check .`) | clean |
| `npm test` (`vitest run`) | **25 files / 294 tests passed** |
| `npm run build` | succeeded, `dist/assets/index-Cc7rTXmF.js` (127.73 kB, gzip 37.91 kB) |

`git status --porcelain` is empty and `git diff --check 741754b..HEAD` is clean
(`git-state.txt`). No other validation was re-run, because no other source changed.

## 5. Canonical documentation synchronization

| Document | Change |
| --- | --- |
| Application `README.md` | Phase 3 = owner-runtime validated; Phase 4 = PASS, checkpoint closed; write contract records the real staging run instead of "no write has been exercised against a live node"; read contract documents the per-entity bootstrap baseline; states that the app never republishes the `WEBSITE` bundle and that `WEBSITE / Qortal Web Builders / default` has never been written (commit `7fd03fc`) |
| Application `docs/architecture.md` §3.4/§5 | the same baseline rule as the read-path contract (commit `7fd03fc`) |
| Workspace `projects/qwb-qortal-web-builders.md` | D1–D9 recorded as owner-approved with the accepted (implemented) state per decision; production identity `WEBSITE / Qortal Web Builders / default` and staging identity `WEBSITE / Q-Website / default` recorded; `qwb_*` recorded as the shipped, runtime-verified model rather than a proposal; the pre-work "not yet decided" list marked answered; test counts and the "no QDN call exists anywhere in the code" statement corrected |
| Orchestration `PROJECT-REGISTRY.md` | `qortal/qwb-qortal-web-builders` registered with its canonical context (production publication pending) |
| Orchestration `skills/README.md` | the three promoted skills indexed |
| Orchestration `skills/qortal/{qdn-content-crud,registered-name-owner-mode,inline-owner-editing}` | the three verified-runtime skills, ready to be committed as durable handoff |

`python3 tools/validate_skills.py` → **`Skills validation passed: 13 active skills indexed exactly
once`**.

Nothing in this synchronization changed an approved architecture decision: D1–D9 are recorded as
approved and as implemented, and the only new statement is the per-entity bootstrap baseline that
makes the approved "one entity at a time" flow actually possible.

## 6. Production publication readiness

**Readiness: the release candidate is ready for an owner-authorized production publication.** Not
published by this task.

Remaining items, none of which is a source defect:

1. **Owner authorization to publish** `WEBSITE / Qortal Web Builders / default` — the only external
   step left, unchanged from D9 (staging first, production last).
2. **The runtime-validated artifact predates the checkpoint's read-path change.** The Hub 3.0.3 run
   validated the build of `741754b`; the release candidate `7fd03fc` builds differently
   (`dist/assets/index-Cc7rTXmF.js`) and, once any content is published, renders the untouched shipped
   items that the validated build hid. This is the intended fix, it is covered by the transition tests
   above, and it changes no write or owner-mode behaviour — but it is a **visible** difference from the
   run that produced the owner-runtime evidence. A bounded owner confirmation is therefore
   recommended before or at publication: on staging, load the site, confirm the untouched shipped
   items still render **and remain editable** next to the already published synthetic entities, then
   hard-reload. It is a one-minute check and is not a technical blocker.
3. **Two owner decisions carried over unchanged** from the Phase 4 report, neither blocking: the
   licence position of the three bundled unDraw illustrations, and the inherited white-on-gradient
   navbar contrast (2.10:1, identical to the currently published site).
4. **Explicitly unverified, unchanged from the Phase 4 report:** the §14 step 6 failure half (image
   failure must block the entity publish) was not exercised; step 13's literal in-form refusal notice
   is unreachable in Hub 3.0.3 because an account switch tears the render frame down. The equivalent
   guarantees were verified instead.

No QDN write of any kind was made by this checkpoint. The production resource is byte-identical to its
2026-07-07 placeholder.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-checkpoint.md`
- Companion evidence directory:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-checkpoint-evidence/`

---

## Addendum — 2026-09-16: §6 item 2 closed by the bounded staging confirmation

§6 item 2 — "the runtime-validated artifact predates the checkpoint's read-path change" — is now
**closed**. The release candidate `7fd03fc` was published to the staging resource
`WEBSITE / Q-Website / default` (signature
`2egexP3JFzX5pkyVKkPrt9Pidcv9QWvcrvYoxCb8KDtmZa1iY76TUjd4CxLG128xUszoJV2rxKCmyza1gDFJ9sLd`,
880 368 B, `READY`), and the five bounded checks passed in Qortal Hub 3.0.3: the published synthetic
entities still render, 14 untouched shipped items render beside them **with** their
`✎ / 🗑 / ↑ / ↓` owner controls, a hard reload preserves both, and no tombstoned item is
resurrected. The pre-fix defect was additionally reproduced live on the previous staging revision
(build `741754b`: 0 highlights, 0 featured works, 0 prices, 2 services, 1 step).

`7fd03fc` is **production-ready**. Production was **not** published, and
`WEBSITE / Qortal Web Builders / default` was not touched.

- Report: `…/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation.md`
- Evidence: `…/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation-evidence/`

No source changed for this confirmation, so the gate recorded in §4 still describes the tree, and the
full §14 owner-runtime suite was deliberately not repeated.
