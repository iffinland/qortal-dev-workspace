# QWB Phase 2 implementation — qwb-qortal-web-builders/phase-2-20260915

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): every artefact in this task — the
`src/qortal/` and `src/owner/` modules, the stylesheet, the tests, the headless-browser harness
session, the measurements, the screenshots and the commit — was produced by the **DeepSeek** model
executing through the local Codex CLI profile. Per `AI-Orchestration/GIT-AND-HANDOFF.md` the
CLI/orchestration profile is not the executor, so the executing agent is recorded as DeepSeek, not
Codex/Codex Local. No third-party curating agent wrote or reviewed this work.
Report type: implementation report (Phase 2 — automatic owner recognition + inline owner UI shell)
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- branch `agent/qwb/phase-2` @ `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`
- base SHA: `18d760d011e956829714e7489432949829fa1840` (`main` = `agent/qwb/phase-0-1`, Phase 1)
Canonical report path / SHA-256 / authorized remote evidence:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-2-implementation.md`
(SHA-256 of the body recorded in the "Report saved" section). Remote evidence: `git ls-remote origin
refs/heads/agent/qwb/phase-2` → `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c` (equal to the local
commit, verified after push). Companion evidence directory:
`…/implementations/2026-09-15-qwb-phase-2-visual-evidence/`.

---

## 1. Objective and exit criterion

Add the owner-approved owner-mode architecture to QWB without changing the accepted public visual
baseline, and stop there. Owner recognition uses the audited modernized model — `_qdnName` +
`GET_USER_ACCOUNT` + `GET_ACCOUNT_NAMES` → case-folded membership → owner | visitor — automatically,
with no hardcoded identity, never `names[0]`, failing closed, persisting nothing, and re-verifying
before privileged actions and on visibility regain. The owner gets the same public site plus a compact
owner bar and contextual inline controls, with modal/sheet shells, dirty-state/cancel UX and the
interaction state Phase 3 needs. **No QDN CRUD in this phase.**

Exit criterion as stated by the task, and how it is met:

| Exit-criterion clause | Status | Evidence |
| --- | --- | --- |
| Visitor UI remains the accepted Phase 1 baseline | met | `tests/phase-2-visitor-baseline.test.ts` (5 non-owner contexts × 5 routes: the owner layer adds nothing and `#app` markup is byte-identical to the Phase 1 render); harness `harness-visitor-1440.json` (no owner bar/controls/modal/toast host); `05-visitor-home-1440.png` is byte-identical (same SHA-256, zero-pixel diff) to a capture taken earlier on this same branch, so the review fixes below changed no visitor pixel |
| Current publishing-name owner is automatically recognized in a valid real-host-compatible architecture | met client-side | `src/qortal/{context,bridge,identity}.ts` + harness: two automatic bridge calls, owner bar rendered for the owner, `unavailable` in dev proxy/gateway |
| Non-owner never receives owner controls | met | visitor baseline test (5 visitor causes), `qortal-identity` fail-closed tests, harness visitor report |
| Owner gets the complete inline editing shell | met | 17 inline control groups, 5 `+ Add …` rows, owner bar, modals/sheets, forms (harness `harness-owner-1440.json`, images 01–04) |
| Privileged identity is revalidated correctly | met | `session.assertOwner()` on every flow; visibility-regain and route-change triggers; `tests/owner-session.test.ts`, `tests/owner-bar.test.ts` (bar re-check removes the whole owner layer) |
| No UI can falsely claim content was saved/published | met | disabled primary action with its reason, `Validate draft` says nothing was saved, `writeActions: []`, `documentTextHasClaim: false`, `tests/support/claims.ts` source scan |
| Phase 3 can add QDN persistence without restructuring the UI | met | §10 |

---

## 2. Owner-recognition contract implemented

### 2.1 The model

```text
_qdnName                     (Core-injected publishing name)
  + GET_USER_ACCOUNT         (host-mediated: permission dialog; 60-minute host timeout)
  + GET_ACCOUNT_NAMES        (node read answered by q-apps.js)
  → case-folded membership over the complete name list
  → owner | visitor | unavailable | inconclusive
```

Module split (one concern per file, and no duplicated identity helper anywhere):

| Module | Responsibility |
| --- | --- |
| `src/qortal/context.ts` | Reads the injected globals with their **exact** Core names (`_qdnContext`, `_qdnTheme`, `_qdnLang`, `_qdnService`, `_qdnName`, `_qdnIdentifier`, `_qdnPath`, `_qdnBase`, `_qdnBaseWithPath`), classifies `render \| proxy \| gateway \| domainMap \| unknown`, and reports *why* owner mode is structurally impossible (`no-bridge \| non-interactive-context \| empty-publishing-name`). |
| `src/qortal/bridge.ts` | The single wrapper over `window.qortalRequest`. Normalises resolved / rejected / timed-out calls into one `BridgeOutcome`; per-action timeouts (`GET_USER_ACCOUNT` = 60 min); treats a resolved `{error}` as a failure (the gateway shim answers interactive actions that way); marks host-mediated actions so a permissioned read is never auto-retried. Nothing else in the app touches `window.qortalRequest`. |
| `src/qortal/identity.ts` | `determineOwner()`: the two calls, the case-folded set test, and the decision record (`status`, `reason`, `detail`, publishing name, service, context, account address, account names, `checkedAt`). |
| `src/qortal/write.ts` | Truthful write vocabulary + the Phase 3 read-back gate. Ships now because the classifier had to exist before any write path may. |

### 2.2 Rules, and where each one is enforced

| Requirement | Enforcement |
| --- | --- |
| Automatic | One derivation at boot; no login, no account picker, no "logged in as" surface anywhere. |
| No hardcoded owner name/address | The owner's name appears only in `README.md`, docs, comments and tests; no `src/` code branches on a literal address or name. |
| Never `names[0]` | `decideFromNames()` normalises the whole list and uses `includes()`; response order is never read. Verified live (below) that the owner's account holds **two** names, so a positional read would have been wrong. |
| Fail closed | Every failure path returns a non-`owner` status; only `status === 'owner'` mounts owner UI (`shell.render` returns immediately otherwise). |
| No persisted `owner=true` | Nothing is written to `localStorage` / `sessionStorage` / IndexedDB — asserted by the source scan in `tests/support/claims.ts` and by `tests/qortal-identity.test.ts` ("persists nothing about ownership"). |
| Re-verify before privileged actions | Every flow begins with `await session.assertOwner()`; a failure is reported to the user instead of being silently ignored. A control rendered while the account owned the name therefore does nothing after an account switch. |
| Re-verify on visibility regain | `visibilitychange → visible` triggers a bounded re-check (rate-limited to one attempt per 15 s), because the host sends no account-changed event. |
| Automatic re-checks are bounded | A confirmed owner/visitor is not re-prompted on every navigation; a route change only re-checks while the last attempt was inconclusive; concurrent attempts are deduplicated into one pair of bridge calls. |
| Truthful host limitations | `proxy` (Hub Developer Mode) → `unavailable` ("the host injected no publishing name (developer-mode proxy), so owner mode cannot exist here"); `gateway` / `domainMap` → `unavailable` ("the injected context … cannot carry host-mediated requests"); no bridge → `unavailable`. A declined dialog, timeout, malformed payload or node read failure → `inconclusive` (explicitly **not** `visitor`), and `inconclusive` still refuses privileged actions. |

### 2.3 Platform facts this rests on (verified, not remembered)

- Injected globals are declared by Core `108bf191` `src/main/resources/qortal/HTMLParser.java`
  (`addAdditionalHeaderTags`) as `var _qdnContext="%s"; … var _qdnBaseWithPath="%s";` — the leading
  underscore is mandatory and reading an underscore-less variant silently yields nothing.
- `qortalRequest` is injected by `/apps/q-apps.js` into the **app's own window** (the legacy
  `window.parent` probing of the reference app is obsolete); it resolves with the parsed result and
  **rejects** with the host's error object or a string. Gateway serving answers interactive actions
  with `{error: "Interactive features … not yet supported when viewing via a gateway…"}`, which is why
  a resolved `{error}` is classified as a failure.
- `GET_ACCOUNT_NAMES` ignores `limit`/`offset`/`reverse`; the response is the complete list for that
  address (the app sends only `address`, asserted in `tests/qortal-identity.test.ts`).
- Live read-only probe (2026-09-15, node `127.0.0.1:24991`, sync 100 %): publishing name
  `Qortal Web Builders`, owner `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`;
  `/names/address/<owner>` returns **two** entries (`Qortal Web Builders`, `Q-Website`) — the direct
  proof that `names[0]` would have been an incorrect owner test.
- Reference-app audit weaknesses modernized away: no hardcoded identity, no `names[0]`, no legacy
  `window.parent` bridge probing, no optimistic write assumption, no duplicated identity helpers.

---

## 3. Inline owner UX implemented

Visitor → the unchanged public site (proven at pixel level). Owner → the same site plus:

**Compact owner bar** (`src/owner/bar.ts`) — deliberately not a CMS dashboard (`§9.4`): owner badge,
publishing name, `WEBSITE · verified by name ownership`, publishing status line (*"Publishing: off
(Phase 2) — nothing is saved or published"*), unsaved-change line, `Publishing status` and
`Re-check owner mode` actions, plus a collapse toggle. It is expanded by default where there is room
(`≥768 px`) and collapses to its badge on a phone, where the toggle opens the same information as a
sheet (`§9.5`; sheet behaviour asserted in `tests/owner-bar.test.ts` and captured in image 03). The
bar publishes its own measured height as `--qwb-owner-bar-height` so toasts stack above it instead of
covering the actions they were raised from (harness: `toastClearsBar: true`).

**Contextual inline controls** (`src/owner/targets.ts`, `src/owner/controls.ts`) — `✎ edit`,
`🗑 delete`, `↑`/`↓` reorder, and one `+ Add …` row per section, on the home page's featured cards,
steps, featured works, build-service lines, pricing tiers and the hero/contact/footer singletons, and
on the works page, the article index and an article header. They are created as DOM nodes and appended
**after** the public render, so no view emits owner markup. `mountOwnerControls` compares the number
of matching DOM nodes with the expected number of entities per group and, on any mismatch, attaches
**no** controls for that group and records one diagnostic (`renderer drift`) — attaching a control to
the wrong entity would be worse than showing none.

**Modal / sheet / toast shells** (`src/ui/modal.ts`, `src/ui/toast.ts`, `src/owner/forms.ts`,
`src/owner/fields.ts`) — `role="dialog"` + `aria-modal` + `aria-labelledby`, focus moved in and
restored on close, Escape cancels, a **dirty** form asks before discarding, backdrop click goes through
the same guard, background scroll is locked while a dialog is open, mobile is a bottom sheet with
≥44 px targets, and toasts are a polite live region that never steals focus. Forms are
descriptor-driven: one `FieldDescriptor[]` per entity kind drives both the rendered form and the draft
assembler, so a form cannot drift from its own reader.

**Dirty-state / cancel UX** (`src/owner/drafts.ts`, `src/owner/flows.ts`) — a reorder is DOM-only,
so it is recorded as an explicit unsaved change; the bar counts them ("N unsaved changes — not
published"), offers `Discard unsaved changes`, and the reorder toast says the change is on this screen
only. Closing a dirty form asks first; if owner mode ends while a form is open the draft is **kept**
and the form explains why instead of being thrown away.

**Truthfulness by construction** — `src/owner/phase.ts` holds `QDN_WRITE_ENABLED = false` and the
notices; the primary form action is rendered **disabled** with *"Not saved (Phase 3 adds publishing)"*
next to it, and the only enabled action (`Validate draft`) runs the real assembly and the read path's
validator and then states that nothing was saved or published. Delete opens a confirmation that
explains tombstone semantics and keeps the destructive button disabled. `Reorder` never claims
persistence. `Publishing status` shows the four-state vocabulary (`submitted / rejected / ambiguous /
failed`) and says pending writes = 0.

Three defects in this shell were found by looking at the rendered result rather than the markup, and
are fixed in this commit (details in §6): the add-row stretching to the pricing-column height, the
desktop bar hiding its global information behind a click, and the toast layer overlapping the
expanded bar.

---

## 4. Validation by layer

All commands were run in `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`
at the exact revision `b53edc1a` (local time, Europe/Helsinki).

| # | Layer | Command | Result |
| --- | --- | --- | --- |
| 1 | Unit / integration | `npx vitest run` (18:43) | **17 files, 174 tests passed**, 0 failed |
| 2 | Types | `npx tsc --noEmit` (18:45) | clean (strict + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` + `verbatimModuleSyntax`) |
| 3 | Lint | `npx eslint .` (18:45) | clean (type-checked config) |
| 4 | Format | `npx prettier --check .` (18:45) | clean |
| 5 | Build | `npm run build` (18:43) | `tsc --noEmit && vite build` OK, `dist/` emitted (`style` 213.91 kB / 31.84 kB gzip, `index` 94.20 kB / 28.22 kB gzip) |
| 6 | Whitespace / diff sanity | `git diff --check` (18:45) | clean |
| 7 | Source-level write guard | `tests/support/claims.ts` (inside #1) | no write-capable bridge action outside `src/qortal/{bridge,write}.ts`; no `localStorage`/`sessionStorage`/`indexedDB` anywhere in `src/` |
| 8 | Real browser, structural | headless Chrome 153 harness over the built `dist/` (18:42–18:43) | owner bar/controls/modal present for an owner, absent for a visitor, **no `PUBLISH_*` call**, no "saved/published" claim text |
| 9 | Visual identity | SHA-256 + pixel diff of the visitor home capture, taken twice on this branch (before and after the §6 review fixes, both from the production build) | **identical** (`28bc7fb7800c2ecec0ab11ebf40cd026d0fa81fc5fea42078112dcd10e734b62`), pixel diff bbox `None` |

Test coverage added in this phase — 17 files, 174 tests, of which **127 in the 12 Phase 2 files**
(the other 47 are the pre-existing Phase 1 files: `schema` 16, `views` 12, `router` 7, `repository` 6,
`media` 6): `qortal-identity` 19 (membership, `names[0]`, empty name, malformed payloads, decline,
timeout, gateway/proxy, no persistence), `qortal-bridge` 14, `identifier` 13, `owner-flows` 13
(edit/add/delete/status/reorder, claims scan), `owner-forms` 13 (descriptors, pre-fill, rev bump,
schema rejection, site-slice preservation, footer-credit round trip, escaping, media affordance,
`nextOrder`), `qortal-context` 10, `owner-session` 10 (boot, action, visibility, route change, rate
limit, dedupe, subscribe), `modal` 8 (a11y, focus trap, dirty guard, backdrop, teardown releases the
key handler and the scroll lock), `phase-2-visitor-baseline` 8, `owner-controls` 7 (target map,
fail-closed drift, reorder unit), `qortal-write` 7 (outcome classification + served-revision gate),
`owner-bar` 5 (content, expanded/collapsed defaults, toggle, re-check removes the owner layer, no bar
for a non-owner).

Notable regression proofs (a fix was removed again to confirm the test fails without it):
- `modal` teardown: with the previous `closeAllModals()` body the new test fails
  (`escape.defaultPrevented === true` — the removed dialog was still trapping Escape), and passes with
  the fix.
- `qortal-context`: the underscore-less lookalike globals (`qdnName`) must yield `unknown` /
  non-interactive, which is the guard against the mis-named-global BLOCKER recorded in §6.

---

## 5. Real-browser harness evidence

Harness: built `dist/` served over `http.server`, loaded in headless Chrome with the Core-injected
globals and a stub `qortalRequest` that answers with two names — `Q-Website` **first**,
`Qortal Web Builders` second — so a positional membership read would be exposed. Full detail and the
raw JSON are in the companion evidence directory.

| Check | Result |
| --- | --- |
| Owner bar at 1440 px | present, name `Qortal Web Builders`, meta `WEBSITE · verified by name ownership`, **expanded**, toggle `Hide owner tools` |
| Owner bar at 390 px | `ownerBarExpanded: false`, toggle `Show owner tools`; after the toggle click `sheetOpenAfterClick: true` |
| Bridge calls (owner) | exactly `[GET_USER_ACCOUNT, GET_ACCOUNT_NAMES]` — no other action, no `PUBLISH_*` |
| Inline controls | `controls: 17` (14 entity groups + 3 section singletons), `editButtons: 17`, `moveButtons: 28`, `deleteButtons: 14`, `addRows: 5` |
| Add rows | heights `[68, 68, 0, 0, 68]` (the two 0 px ones are inside the hidden tab panes); `#section_3 .pricing-container > .qwb-owner-add-row` is **68 px**, `flex-basis: 100%`, `align-self: flex-start`, beside a 634 px pricing box |
| Edit flow | `✎` → `Edit featured card`, pre-filled, `saveDisabled: true`, label `Save & publish`, notice *"Nothing you change here is saved or published — QDN persistence arrives in Phase 3"*, `writeActions: []` |
| Re-check + toast | `Owner mode confirmed: the current account owns "Qortal Web Builders".`, `toastClearsBar: true` |
| Claim text scan | `documentTextHasClaim: false` (no "published successfully" / "saved successfully" anywhere) |
| Visitor | `ownerBar: false`, `ownerControls: 0`, `ownerClasses: 0`, `modalHost: false`, `toastHost: false`; screenshot byte-identical to the earlier capture on this branch |

---

## 6. Adversarial self-audit

Findings that were confirmed and fixed before handoff (this is one Phase 2 delivery; findings marked
[pre-review] were found while producing the modules and fixing them is part of the same commit):

| # | Severity | Finding | Evidence it was real | Fix | Regression guard |
| --- | --- | --- | --- | --- | --- |
| 1 | **BLOCKER** [pre-review] | Injected globals were read as `qdnName`/`qdnContext` (underscore-less). Behaviour was silently "no host" — i.e. owner mode could never work in a real host, while unit tests (which encoded the same wrong name) passed. | Core `HTMLParser` declares `var _qdnName="%s"`; the real-browser run reported `unknown`/non-interactive instead of owner | Read the exact `_qdn*` names in `context.ts`; tests re-encoded | `tests/qortal-context.test.ts` asserts underscore-less lookalikes yield `unknown` and a non-interactive identity |
| 2 | HIGH | `decideFromNames()` could return `owner` when both the publishing name and the matching entry were empty/whitespace | code path review | Require `publishingKey !== ''` | `qortal-identity`: "never confirms owner mode for an empty or whitespace publishing name" |
| 3 | HIGH | `session` internals bypassed its own API (`maybeReverify`/`start` called the local `reverify`), so the re-verification paths were neither observable nor testable and could drift from the public entry point | review of `session.ts` internals | All internal callers go through `session.*` | `owner-session` tests observe the public API; `owner-bar` re-check test removes the layer |
| 4 | HIGH | `closeAllModals()` removed the dialog DOM but left its capturing `keydown` listener and scroll lock behind — a closed dialog kept trapping Escape/Tab and consuming them from the page | reproduced: new test fails with the previous body, passes with the fix | New `dispose(restoreFocus)` path + an open-dialog registry; `closeAllModals()` disposes then empties | `tests/modal.test.ts` "releases the document key handler and the scroll lock…" (fails on the old body) |
| 5 | MEDIUM | `slugifyTitle` left combining marks (`ü` → `u` + U+0308 → `-u-ni-code`) | unit test | NFKD + strip `[\u0300-\u036f]` | `identifier.test.ts` fold test |
| 6 | MEDIUM | The build-service control group used `#panel-3 article.custom-block ul > li`; the actual markup is `div.custom-block`, so the group failed closed and the owner silently had no service controls | harness count (17 vs expected) + markup inspection | Corrected selector | `owner-controls.test.ts` "maps every editable home section to a container that exists in the page" |
| 7 | MEDIUM | Footer-credit round trip was lossy (`|¤|` separators inline in segment text) — an edit would have silently changed the published footer | round-trip review/test | Target-aware parsing (`splitTail`, `splitLinkPairs`, `splitIconPairs`, `parseInlineSegments`) preserving spacing | `owner-forms.test.ts` "round-trips the footer credit line segments through the form" |
| 8 | MEDIUM | The focus trap used `offsetParent`, which is `false` for every element in a non-laid-out document; the hidden dirty-guard buttons joined the Tab cycle | modal test | Visibility = "not inside a `[hidden]` subtree" | `tests/modal.test.ts` "keeps Tab inside the dialog" |
| 9 | MEDIUM (visual) | `+ Add pricing tier` was appended into `.pricing-container` (a wrapping flex row) and stretched to the full column height (≈500 px tall bar in the screenshot) | rendered owner screenshot + measurement | `flex-basis: 100%; align-self: flex-start` | harness measurement (68 px) + image 01 |
| 10 | MEDIUM (visual) | The desktop owner bar hid its global information (`Publishing status`, `Re-check owner mode`) behind a click, conflicting with `§9.4` which makes them bar content | rendered owner screenshot | Bar starts expanded at `≥768 px` (collapsed on a phone, per `§9.5`), via `matchMedia` with a collapsed fallback | `owner-bar` "starts expanded where there is room and collapsed on a phone" (matchMedia stubbed) |
| 11 | MEDIUM (visual) | With the bar expanded, the toast layer (fixed `bottom: 84px`) overlapped the bar and painted over the actions it was raised from | geometry review after #10 | The bar publishes its measured height as `--qwb-owner-bar-height`; toasts stack above it | harness `toastClearsBar: true` (toast bottom 2888 ≤ bar top 2900) |
| 12 | MEDIUM | The scroll lock was a no-op: `modal.ts` added `.qwb-modal-open` but no stylesheet rule consumed it, so the page scrolled behind an open dialog | `grep` showed the class was written nowhere else | `html.qwb-modal-open, html.qwb-modal-open body { overflow: hidden }` in `owner.css` | covered by the modal teardown test (class released) + image 04 |
| 13 | MEDIUM | Duplicated tombstone wording in two modules (drift risk in the one message that must stay truthful) | review | The delete modal uses the canonical `TOMBSTONE_NOTICE` from `write.ts` | `owner-flows.test.ts` tombstone test |
| 14 | LOW | Reorder notice said "Nothing was published" but not "saved" | review | `REORDER_NOTICE` now says "Nothing was saved or published" | `owner-flows` reorder test |
| 15 | LOW | Dead code in `owner.css`: `prefers-reduced-motion` block with no transitions to disable, and an unused `.qwb-owner-add-edge` rule | review | Removed; the owner layer defines no animation or transition, so no reduced-motion override is needed (the public baseline's own motion handling is untouched) | `prettier --check`, review |
| 16 | LOW | Test-only: the bridge rejection helper rejected `Error` instances, while the real host rejects a plain object/string | Core `q-apps.js` path review | Helper rejects the raw value; ESLint exception documented in `eslint.config.js` | `qortal-bridge.test.ts` decline/timeout cases |

Examined and found sound (no change made):

- **`withTimeout` timer leak** (suspected): the timer is cleared in both settle paths, and if the host
  promise never settles the timer firing is what settles the wrapper — no leak, no dangling rejection.
- **`session.start()` after the first render**: `attach()` subscribes before `start()` runs, and the
  first state read is synchronous, so no notification can be lost; `render` is called before `start`
  exactly so owner UI is never mounted before the public DOM exists.
- **Control-count arithmetic**: 17 control groups = 14 entity rows (2 highlights + 3 steps + 3 featured
  works + 4 services + 2 prices) + 3 singletons, matching `ownerTargetsFor` and the harness count.
- **Reorder cannot imply persistence**: it mutates the DOM, records an unsaved change, and its toast
  says the change is on this screen only; the bar reports the count as "not published".
- **Visitor cleanliness**: the shell adds nothing for a non-owner (asserted per context and per route),
  and the visitor screenshot is byte-identical across the change.
- **Escaping**: forms escape every content-derived value (`escapeHtml`), and no owner value is passed
  as HTML except through `ModalOptions.bodyHtml`, whose callers escape their interpolations.

No BLOCKER or HIGH finding remains open.

---

## 7. Files changed

`git show --stat b53edc1a` → **36 files changed, 6947 insertions(+), 33 deletions(-)**.

New modules (production):

| File | Lines | Purpose |
| --- | --- | --- |
| `src/qortal/context.ts` | 139 | injected-global reader, host-context classification, owner-mode block reasons |
| `src/qortal/bridge.ts` | 258 | the single `qortalRequest` wrapper, `BridgeOutcome`, per-action timeouts, retry policy |
| `src/qortal/identity.ts` | 326 | `determineOwner()` + the pure membership decision |
| `src/qortal/write.ts` | 165 | truthful write-result vocabulary, tombstone wording, served-revision gate |
| `src/owner/session.ts` | 245 | owner state machine + the re-verification rules |
| `src/owner/targets.ts` | 293 | attachment points per route, expected entity counts, reorder units |
| `src/owner/controls.ts` | 227 | inline affordances, fail-closed group rendering |
| `src/owner/bar.ts` | 163 | compact owner bar + measured height for the toast layer |
| `src/owner/shell.ts` | 131 | owner-UI attachment, responsive expansion default, teardown |
| `src/owner/flows.ts` | 404 | edit/add/delete/status/reorder flows, each re-verifying owner mode |
| `src/owner/fields.ts` | 728 | field descriptors, value round-trip, draft assembly via the read path's validator |
| `src/owner/forms.ts` | 133 | descriptor-driven form rendering |
| `src/owner/drafts.ts` | 55 | in-memory unsaved-change store |
| `src/owner/phase.ts` | 31 | Phase gate constants and truthful notices |
| `src/ui/modal.ts` | 256 | dialog host, focus trap, dirty guard, scroll lock, teardown registry |
| `src/ui/toast.ts` | 68 | owner status toasts (live region, `textContent` only) |
| `src/content/identifier.ts` | 71 | identifier generation + slug folding |
| `src/styles/owner.css` | 507 | owner-only, `qwb-`-scoped style layer |

Changed: `src/main.ts` (owner session/shell wiring, `owner.css` import), `eslint.config.js` (one
documented test-only rule exception), `README.md` and `docs/architecture.md` (Phase 2 module map,
owner contract, phase seams).

Tests added: `tests/{qortal-context,qortal-bridge,qortal-identity,qortal-write,identifier,owner-session,owner-controls,owner-flows,owner-forms,owner-bar,modal,phase-2-visitor-baseline}.test.ts`
plus `tests/support/{owner,claims}.ts` (≈3 150 lines with the harness).

No file in the golden master (`-PUBLISHED-versioon`) was read, written, built or formatted.

---

## 8. Checks not executed, and why

| Not executed | Reason |
| --- | --- |
| Qortal Hub / Home run of owner mode | Requires the owner's real account in a real Qortal host. See §9 for the exact procedure; this is the remaining acceptance step. |
| Host-mediated `GET_USER_ACCOUNT` permission dialog | Only the host can raise it; the harness stubs the bridge, so the app-side handling of a decline/timeout is unit-tested rather than host-tested. |
| Any QDN read or write | Out of scope for Phase 2 by the task and by `QDN_WRITE_ENABLED === false`; no publish, update or delete path exists. |
| Owner mode through the Hub Developer-Mode proxy | Structurally impossible: the proxy injects an empty `_qdnName`, so the contract reports `unavailable`. This is a recorded platform limitation, not a skipped test. |
| Gateway / domain-mapped serving | Non-interactive (`§2.3`): the app reports `unavailable` with the reason; no Hub is attached to answer. |
| Deployment / publication of this build | Not authorized in this task. |
| Visual regression against the golden master | Phase 1 already established the descent and documented intentional deltas; Phase 2 changes nothing on the visitor render, which is instead proven by the byte-identical visitor capture (§4 row 9). |

---

## 9. Exact owner-runtime procedure required before owner-mode PASS

The client-side contract is verified; the following host run is what turns owner mode from
"implemented" into "accepted". It needs the owner's real account and a real Qortal host.

1. **Publish or locate the build.** Owner-mode recognition needs `_qdnName` and an interactive
   render context, so the app must be served by a Qortal host as a QDN resource under the name
   `Qortal Web Builders` (service `WEBSITE`, identifier `default`). Publishing is a separate
   authorized action; the reproducible local alternative for a read-only smoke test is Hub's
   app-open for an already-published identifier.
2. **Open the app in Qortal Hub / Home** (desktop for the expanded bar, mobile for the sheet) so
   `_qdnContext === 'render'` and `qortalRequest` is injected. Confirm in the app console:
   `_qdnContext === 'render'`, `_qdnName === 'Qortal Web Builders'`, `typeof qortalRequest === 'function'`.
3. **Sign in with the account that owns the publishing name** (`QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` as
   recorded on 2026-09-15) and **approve the host permission dialog** for account access.
4. **Expect, and record:** the owner bar bottom-left, expanded, with the owner badge, the publishing
   name, `WEBSITE · verified by name ownership`, and — in the browser console — exactly two bridge
   actions (`GET_USER_ACCOUNT`, `GET_ACCOUNT_NAMES`) and **no** `PUBLISH_*`. Screenshot the source list
   as it stood (`GET /names/address/<owner>`) so the ownership claim is recorded next to it.
5. **Exercise the shell:** open `✎` on a featured card, a step, a service line and a pricing tier; check
   the form is pre-filled from the served content, that `Save & publish` is disabled, that
   `Validate draft` reports valid/invalid without any write, that `🗑` and `Publishing status` open
   their shells, and that `↑`/`↓` moves and counts an unsaved change. Nothing may appear in the host's
   transaction/notification history.
6. **Negative control (must fail closed):** run the same app with an account that does **not** own the
   name, and separately decline the permission dialog. Expected: the bare public site — no owner bar,
   no controls, no re-check affordance (declined → `inconclusive`, which also refuses privileged
   actions).
7. **Re-validation:** with owner mode confirmed, switch the Hub account (or lock/unlock to another
   account), leave the app and return (visibility regain) and press `Re-check owner mode`. Expected:
   the owner layer disappears when the account no longer owns the name and returns when it does, with
   a truthful toast and no write.
8. **Mobile:** repeat steps 2–5 in the mobile Hub at ≤767 px: the bar must begin collapsed as a badge,
   `Show owner tools` must open the sheet, and every target must be ≥44 px.
9. **Record the outcome** (host + version, screenshots, bridge-call log, ownership listing, pass/fail
   per step) in a Phase 4 owner-runtime validation report. Note that Hub Developer-Mode proxy renders
   the app with an empty `_qdnName`; owner mode is *designed* to be unavailable there and must be
   recorded as not exercisable, never as a failure.

---

## 10. Phase 3 readiness

Phase 3 can add QDN persistence without restructuring the UI, because the seams already exist and are
exercised in this phase:

- **Write vocabulary and verification**: `classifyPublishOutcome()` returns
  `submitted | rejected | ambiguous | failed` with `availability` fixed at `unverified`, and
  `verifyServedRevision()` only reports `verified` on an exact revision match — the UI is written
  against these labels, so no optimistic copy has to be unwound later.
- **Draft assembly**: `assembleDraft()` builds a full `AnyEntity` per kind, sets `rev + 1`, keeps
  `createdAt`/`order`, clears `deletedAt`, and validates through the same `validateEntity()` the read
  path uses; the descriptors round-trip every field the forms expose.
- **Identifiers**: `generateIdentifier()`/`isValidIdentifier()` implement the approved policy so an add
  flow can publish under the identifier the form already displays.
- **Attachment and ordering**: `ownerTargetsFor()` already carries entity ids, host indices, expected
  counts and reorder units, so a write can map a control back to the entity it edits.
- **Interaction state**: the dirty/discard contract, in-flight-safe flows, owner-mode-ended handling
  and the modal shells exist; `phase.ts`'s `QDN_WRITE_ENABLED` is the single flip, and the disabled
  primary action is the seam the publish pipeline plugs into.
- **Content source**: swapping `createSeedSource()` for a QDN-backed `ContentSource` remains a
  one-module change; the owner layer reads the bundle through `getContent()`, so it follows
  automatically.

---

## 11. External actions

- `git commit` on `agent/qwb/phase-2` → `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`
  ("Phase 2: automatic owner recognition + inline owner UI shell"), base `18d760d0`.
- `git push -u origin agent/qwb/phase-2` → new remote branch;
  `git ls-remote origin refs/heads/agent/qwb/phase-2` = `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`
  (verified after the push). Worktree clean afterwards.
- **No** QDN write, no transaction, no signature, no tag, no release, no deployment, no merge into
  `main`, no issue mutation, no repository settings change.

---

## 12. Capability harvest

Two reusable capabilities were identified and are **deliberately left unpromoted**:

| Candidate | Why not promoted now |
| --- | --- |
| `qortal/registered-name-owner-mode` (recognise the account that owns the app's registered name; `_qdnName` + `GET_USER_ACCOUNT` + `GET_ACCOUNT_NAMES`, case-folded, fail-closed, never positional) | The platform half is verified against Core/Hub source and a live node, but owner-mode acceptance in a real host is still pending (§9). Promotion without that evidence would create a skill at unsupported maturity. |
| `qortal/inline-owner-editing` (owner bar + contextual inline controls over a preserved public DOM, fail-closed DOM↔content count matching, truthful no-write wording) | Same reason: the interaction pattern needs a real owner run before it is generalisable. |

No skill file was created or updated in this task; no orchestration knowledge was changed. Re-harvest
after the Phase 4 owner-runtime run, which is the evidence that would let both candidates be recorded
with a real maturity level and freshness test.

---

## 13. Remaining risks and follow-up

| Risk / follow-up | Note |
| --- | --- |
| Owner mode has not run in a real host | The single remaining acceptance gate (§9). Everything else is client-side-verified only. |
| Recognition depends on the injected publishing name | If a future host serves the app under a *different* registered name (or with an empty `_qdnName`), owner mode silently becomes `unavailable`; the reason is surfaced in the bar and in console diagnostics, but the owner should be told which name is expected. |
| `GET_USER_ACCOUNT` prompts the owner | The first derivation raises the host permission dialog. This is inherent to the approved model; the app never re-prompts on navigation, and automatic re-checks are rate-limited to 15 s. |
| Two dialogs can be open at once | Field ids (`qwb-field-*`) repeat across stacked dialogs. Harmless for behaviour and screen-reader order (each dialog is `aria-modal` with its own labelled title) but worth unique-scoping in Phase 3. |
| Reorder is DOM-only | Intended in Phase 2 and labelled as such; Phase 3 must re-derive order from the loaded bundle rather than trusting the DOM after a reload. |
| Media, derived index, publication | Out of scope for Phase 2; unchanged from the Phase 0–1 handoff. |

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-2-implementation.md`
- SHA-256 of the report **body** (415 lines, measured immediately before this block was appended):
  `055bcdac951af572435a709a70f3556b2af99754ef16819b8d8ab8cd22ad0b6f`
  This block is the only part of the file written after that measurement, so the digest remains the
  identity check for everything above it.
- Companion evidence directory (13 files, digests in its `SHA256SUMS.txt`):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-2-visual-evidence/`
- Local harness workspace used to produce that evidence (transient, not durable):
  `/tmp/qwb-check-3/` (built `dist/` + generated harness pages), `/tmp/qwb-shots-3/` (raw dumps),
  script `/tmp/qwb-harness.py`, runner `/tmp/qwb-run.sh`.
