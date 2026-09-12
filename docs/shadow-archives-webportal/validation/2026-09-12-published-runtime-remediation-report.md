# Shadow Archives — published-runtime remediation report

- **Task type:** runtime remediation / correctness fix (Workflow v2).
- **Primary class:** platform integration + runtime correctness.
- **Date:** 2026-09-12.
- **Application:** `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- **Workspace:** `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`
- **Application revision:** `91cd0b1` (`main`) + uncommitted changes from this task.
- **Status:** implementation complete; static + automated + production-browser
  emulation verified; **real published-host re-validation still required**.
- **No live write occurred:** no QDN publication, no transaction, no APP update,
  no commit, no push.

## 1. Owner-visible failure

The owner ran the **published** APP and reported:

1. Gallery showed *"No production Qortal publisher identity is available in this
   context, so QDN content cannot be scoped or verified."*
2. `/studio` was reachable only by typing the route.
3. Studio said *"Not running in a Qortal host"*.
4. The Studio diagnostics showed injected identity but no bridge:

```text
Bridge available: no
_qdnService: APP
_qdnName: Shadow%20Archives
_qdnIdentifier: not injected
_qdnContext: render
_qdnBase: /render/APP/Shadow%20Archives
_qdnBaseWithPath: /render/APP/Shadow%20Archives
```

## 2. Root cause (first confirmed mismatch)

The app was not in a bridge-less runtime. It was in a real published render
runtime while **failing to detect the bridge**, and then collapsed that false
negative into "not hosted" and "no publisher identity".

**Platform-boundary evidence (re-verified 2026-09-12):**

| Source | Revision | Fact |
| --- | --- | --- |
| `Qortal/qortal` | `108bf191` (v6.1.9) | `HTMLParser.addAdditionalHeaderTags` prepends `/apps/q-apps.js` to `<head>` as a **classic** script (no `type="module"`). |
| `qortal/src/main/resources/q-apps/q-apps.js` | `108bf191` | The bridge is declared `const qortalRequest = (request) => { ... }` at top level. |
| `qortal/src/main/java/org/qortal/api/resource/AppsResource.java` | `108bf191` | Serves that file verbatim as `text/plain` JavaScript. |
| `qortal/src/main/**` (whole tree) | `108bf191` | **No** `window.qortalRequest` / `globalThis.qortalRequest` assignment exists. |
| `Qortal-Hub` `src/components/Apps/AppViewer.tsx` | `12a573b2` | The host renders the app in an iframe pointed at the **node's** `/render/{service}/{name}` URL; the host does not inject a bridge into that frame. |
| `qapp-core/src/global.ts` | `0f9d6ac5` (1.0.79) | Declares `function qortalRequest(...)` as a global and calls the bare identifier. |
| `Subwire/src/utils/articleQdn.ts` | `a933a6c4` | `declare const qortalRequest`; calls the bare identifier. |
| `q-tube/src/global.d.ts` | `68c3ea70` | `function qortalRequest<T>(...)`; calls the bare identifier. |

A top-level `const` in a classic script is created in the realm's global
**declarative** environment record. It is reachable as the bare identifier
`qortalRequest` from every script in the realm (including the app's ES modules),
but it is **not** a property of `window`. Therefore:

- the real published runtime **does** have a callable bridge;
- `typeof window.qortalRequest === 'function'` is `false` there;
- the app's `hasQortalBridge()` checked only `window.qortalRequest`, so it
  reported `Bridge available: no`.

**Defect chain in app source (before this fix):**

1. `src/qortal/environment.ts`: `hasQortalBridge()` → `window.qortalRequest`
   only ⇒ `bridgeAvailable === false` in a real render frame;
   `isHosted = bridgeAvailable && (...)` ⇒ `isHosted === false`.
2. `src/services/publisher.ts`: `resolvePublisherScope()` returned
   `{ scoped: false, reason: 'no-bridge' }` ⇒ `UNSCOPED_MESSAGE` ⇒ the Gallery /
   Home no-publisher banner.
3. `src/features/owner/StudioPage.tsx`: `!bridgeAvailable` ⇒ *"Not running in a
   Qortal host"*, masking the injected `_qdnContext=render`.
4. `src/services/qdnReader.ts` / `contentRepository.ts`: the only read transport
   was `bridgeQdnReadPort`, so even a correctly scoped read could not proceed
   without the bridge.

The requested premise — *"the bridge is absent in the published runtime"* — is
therefore **not confirmed**. The observed state is *"the bridge was not
detected"*. This is a platform-boundary defect in the app, not a Core
limitation, and it is reported as such rather than being worked around.

## 3. Runtime model correction

An explicit, total state model now replaces every implicit "no bridge ⇒ not
hosted" inference (`src/qortal/types.ts`, `deriveRuntimeState` in
`src/qortal/environment.ts`):

| State | Injected `_qdn*` | Bridge | Meaning |
| --- | --- | --- | --- |
| `plain-browser` | no | no | Not running inside Qortal at all. |
| `qortal-render-readonly` | yes | no | **Valid published read-only runtime.** Identity is real; owner/auth/write are not available. |
| `qortal-host` | yes | yes | Read-only + owner capability possible (after explicit permission and ownership proof). |
| `qortal-dev-proxy` | yes (empty name) | yes | Node development proxy; identity not authoritative. |
| `qortal-bridge-unidentified` | no | yes | Bridge reachable but no published identity injected; never treated as a published publisher. |

Rules preserved: owner capability requires `qortal-host` only; the states are
never collapsed; `plain-browser` is reserved for a document with no injected
`_qdn*` identity.

`src/qortal/bridgeGlobal.ts` resolves the bridge from **both** access styles:
the bare global binding (authoritative for the pinned Core revision) and a
`window.qortalRequest` property. The bare-global read is guarded (`typeof` in a
`try`) so a temporal-dead-zone or absent binding can never crash startup, and it
is only consulted for the real global object so a synthetic test window cannot
inherit another test's bridge.

## 4. Read-only publisher identity

`resolvePublisherScope` (`src/services/publisher.ts`) now derives the publisher
from the decoded `_qdnName` and **does not require the bridge**:

- `qortal-render-readonly` + `_qdnName=Shadow%20Archives` ⇒
  `{ scoped: true, name: 'Shadow Archives', service: 'APP' }`;
- identical scope with and without the bridge (unit-tested);
- `GET_USER_ACCOUNT` is never involved in read-only identity;
- the proxy context and a frame with no injected name remain unscoped, with
  their own truthful copy.

The single misleading message is replaced by per-reason messages
(`UNSCOPED_MESSAGES`): plain browser, dev proxy, and "Qortal-served but no name
injected" are three distinct statements. No message claims a missing publisher
identity for a published render context.

## 5. Read layer fallback (read-only only)

`src/services/readPort.ts` adds `sameOriginQdnReadPort`, using **exactly** the
same-origin routes the injected shim itself issues with `fetch()` in the frame
the node served (verified from `q-apps.js` `108bf191`):

| Read action | Route used by the fallback | Status |
| --- | --- | --- |
| `SEARCH_QDN_RESOURCES` | `GET /arbitrary/resources/search?<lowercase REST params>` | used by the read repository |
| `FETCH_QDN_RESOURCE` | `GET /arbitrary/{service}/{name}[/{identifier}]` | used by the read repository |
| `GET_QDN_RESOURCE_STATUS` | `GET /arbitrary/resource/status/{service}/{name}[/{identifier}]` | implemented + tested; not used by the current read path |
| `GET_QDN_RESOURCE_URL` | status check, then `/arbitrary/{service}/{name}[/{identifier}]` | equivalent to the existing `buildQdnResourcePath()` used for media `src` — already bridge-free |
| `GET_NAME_DATA` / `GET_ACCOUNT_NAMES` | `GET /names/...` | **not** part of the fallback; ownership reads stay bridge-gated |

Design points:

- The REST query namespace is **lowercase** and must not be unified with the
  camelCase bridge namespace; both mappings are explicit and separately tested
  (`toBridgeSearchParams` vs `toSameOriginSearchQuery`).
- Failure classification reuses the bridge error taxonomy, so the domain layer
  keeps distinguishing `timeout` / network / `malformed`; an empty body is
  `malformed` and a `{"error": ...}` body is a failure — never valid empty
  content.
- Bounded deadline (20 s default), `AbortSignal` forwarding, and a clean
  `unavailable` failure when the runtime has no `fetch`.
- CSP compatibility: the production render CSP is
  `connect-src 'self' wss: blob:`, so same-origin GETs are permitted.
- **Transport selection** (`resolveQdnReadPort`): bridge when reachable;
  same-origin REST **only** for `qortal-render-readonly`; otherwise the bridge
  port, which fails closed as `unavailable` rather than reading an unrelated
  origin.
- The chosen transport is exposed by `ContentProvider` and reused by the entity
  detail hook, so Home, Blog, Videos, Gallery, taxonomy, search, catalog
  loading/fallback discovery and content detail all share one decision point.

## 6. Studio / owner / write gating

- Studio messaging is truthful per state; the plain-browser state is explicitly
  labelled *"Plain browser — no Qortal context"* and the published read-only
  state reports the detected publishing identity, the service/context, that the
  account bridge is unavailable in this frame, and that owner mode is
  unavailable for that reason.
- `Enter owner mode` is rendered **only** in `qortal-host`. In
  `qortal-render-readonly` there is no owner control and no `GET_USER_ACCOUNT`
  request (asserted).
- `deriveCapability` / `isOwnerCapableRuntime` (`src/qortal/capability.ts`)
  grant capability only for `qortal-host`; a published read-only context resolves
  to `unknown` even when a signed-out account fixture claims ownership.
- `galleryPublishService.authorityCheck` now requires
  `runtimeState === 'qortal-host'` explicitly. Adding a read fallback cannot
  authorise a write: `readPort.ts` is imported only by the read layer, and
  `src/qortal/publish.ts` still goes exclusively through `request()`.
- Gallery owner affordances remain lazy and owner-gated
  (`GalleryOwnerPanel` returns `null` unless `isOwner`), so `Add image` /
  `Create album` are absent in the read-only published runtime (asserted in
  tests and in the browser smoke run).
- **Owner decision unchanged:** Studio navigation is appended only for
  `capability === 'owner'`; visitors never see it, and the owner still reaches
  `/studio` manually first.

## 7. Files changed

Application (`QORTAL`, all uncommitted):

- New: `src/qortal/bridgeGlobal.ts`, `src/services/readPort.ts`,
  `src/qortal/bridgeGlobal.test.ts`, `src/services/readPort.test.ts`,
  `src/services/publisher.test.ts`,
  `src/features/gallery/GalleryItemPage.fallback.test.tsx`.
- Modified (runtime): `src/qortal/types.ts`, `src/qortal/environment.ts`,
  `src/qortal/bridge.ts`, `src/qortal/capability.ts`, `src/qortal/qdn.ts`,
  `src/qortal/index.ts`, `src/services/publisher.ts`,
  `src/services/contentRepository.ts`, `src/services/galleryPublishService.ts`,
  `src/services/index.ts`, `src/app/providers/ContentProvider.tsx`,
  `src/features/content/hooks.ts`, `src/features/owner/StudioPage.tsx`.
- Modified (tests/fixtures/docs): `src/test/environment.ts`,
  `src/qortal/environment.test.ts`, `src/qortal/capability.test.ts`,
  `src/qortal/qdn.test.ts`, `src/app/providers/ContentProvider.test.tsx`,
  `src/app/providers/auth-isolation.test.tsx`,
  `src/features/home/HomePage.data.test.tsx`,
  `src/features/owner/StudioPage.test.tsx`,
  `src/services/contentRepository.test.ts`,
  `src/services/galleryPublishService.test.ts`, `README.md`.

Workspace:

- `projects/shadow-archives-webportal.md` — factual runtime findings, corrected
  project rule, `Current state` entry.
- This report, plus the smoke harness artifact
  `docs/shadow-archives-webportal/validation/2026-09-12-published-runtime-smoke-harness.cjs`.

## 8. Validation

### Static / automated (application, Node 20.19.2)

| Command | Result |
| --- | --- |
| `npm run lint` | PASS |
| `npm run typecheck` | PASS |
| `npm test` | PASS — 40 files / 422 tests (baseline 36 / 375) |
| `npm run build` | PASS — entry 387.90 kB raw / 122.20 kB gzip (+3.53 kB / +1.12 kB vs Phase 3A `384.37 / 121.08`); lazy `GalleryOwnerPanel` 44.33 kB / 13.17 kB gzip; `StudioPage` 8.81 kB / 2.83 kB gzip |
| `npm run format:check` | PASS |
| `git diff --check` | PASS (no whitespace errors) |

New/changed test coverage (all requested cases are present):

- plain browser, no `_qdn*` ⇒ `plain-browser`;
- render + `_qdnName` + no bridge ⇒ `qortal-render-readonly` (fixture uses the
  owner's exact values);
- render + bridge ⇒ `qortal-host`;
- render context + bridge declared as a **classic-script global `const`** (Core's
  exact injection) ⇒ detected as a live bridge via `vm.runInThisContext`,
  asserting `window.qortalRequest === undefined` in the same test;
- published read-only context establishes the publisher from `_qdnName`;
- published read-only context never issues `GET_USER_ACCOUNT`;
- Home/Gallery/Blog/Videos no longer show "no production publisher identity"
  when `_qdnName` exists;
- read repository/detail use the same-origin fallback when the bridge is
  missing, and issue no read at all in a plain browser;
- owner/write actions remain unavailable without the bridge (capability unit
  test + `not-hosted` publish refusal + no `Add image` / `Create album` in the
  read-only Gallery);
- Studio messaging is truthful in each context;
- the existing owner-capability path with a bridge is unchanged (pre-existing
  Studio/Gallery-nav/owner-panel suites still pass);
- no visitor startup auth prompt.

### Production browser smoke (headless Chrome over CDP, built `dist/`)

The harness serves the production build the way Core's render path does
(injects `<base>` + `_qdn*`, and — for the bridged case — a classic-script
`const qortalRequest`, i.e. **not** a `window` property). Result: **16/16 checks
PASS**.

- **A. plain browser**: `/studio` shows the plain-browser state and is not
  mislabelled as published; `/gallery` never claims a missing publisher identity.
- **B. render context without a bridge** (the owner's exact runtime):
  `/studio` reports *"Published in a Qortal render context — read-only"*, shows
  the detected publishing identity `Shadow Archives` / service `APP` /
  context `render`, never says plain browser, and diagnostics still report
  `Bridge available: no`; `/gallery` renders without the no-publisher message;
  the app really issued same-origin browser GETs to
  `/arbitrary/resources/search?...`; `window.qortalRequest` is `undefined`
  (matching Core).
- **C. render context with an emulated bridge** (classic-script `const`):
  `/studio` keeps the owner flow (`Enter owner mode`), diagnostics report
  `Bridge available: yes`, `typeof qortalRequest === 'function'` while
  `window.qortalRequest === undefined`, `/gallery` issued **zero** direct
  `/arbitrary/...` HTTP reads (bridge path used), and no `GET_USER_ACCOUNT` was
  requested.

This run also doubles as the "exact observed owner case" reproduction requested
in the task.

### Not verified / remaining

- **Real published host (Qortal Hub + Core) rendering of the corrected build:**
  NOT VERIFIED. No local node/host was available, and the current live APP
  resource still serves the older build (`release/shadow-archives-app-0.1.0-20260911.zip`).
  Owner re-validation requires re-publishing the corrected artifact (an owner
  decision that remains open; no write was performed).
- **Live QDN node read of real `saw_*` content:** NOT VERIFIED (no content has
  been published yet).
- The smoke harness emulates Core's injection faithfully but is not Core.

## 9. Self-audit

| Check | Result |
| --- | --- |
| Render context still treated as plain browser | Fixed; `qortal-render-readonly` is a distinct state and is tested. |
| Publisher identity still tied to bridge presence | Fixed; `resolvePublisherScope` no longer reads `bridgeAvailable`. |
| `GET_USER_ACCOUNT` in read-only render mode | Not issued; asserted in unit and browser tests. |
| Writes enabled without bridge | No; `authorityCheck` requires `qortal-host`. |
| Owner capability granted without bridge | No; `deriveCapability` returns `unknown`. |
| Gallery/Home show no-production-identity in the published runtime | Fixed; asserted in tests and the browser run. |
| Read fallback accidentally used for writes | No; the read port is not reachable from the write path. |
| Studio nav visible to visitors | No; unchanged owner-only rule, confirmed in the browser run. |
| Studio messaging still misleading | Fixed; four distinct truthful states. |
| Phase 3A write security regressed | No; the gate is stricter and writes remain bridge/host-gated only. |

No unresolved BLOCKER/HIGH finding remains in scope.

## 10. Explicit statements

- **No live write occurred.** No QDN publish, no transaction, no APP update, no
  resource deletion, no moderation action.
- **No commit and no push occurred.** All application changes are uncommitted in
  the working tree; `origin/main` is unchanged.
- The owner-owned untracked workspace file
  `docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md`
  was left untouched.
- Out-of-scope work was not started: no Blog publishing, no Video publishing, no
  SubWire/Q-Tube research, no engagement, no Q-Mail, no visual changes.
