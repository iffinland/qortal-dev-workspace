# Shadow Archives Phase 2B — real Qortal host boundary and owner capability (implementation + validation report)

- Project: `shadow-archives-webportal-QORTAL`
- Phase / task: Phase 2B — identity / owner-capability boundary against verified
  Qortal host contracts
- Date: 2026-09-11
- Author: Codex (implementation agent)
- Task class: platform-integration + architecture/identity; **permissioned
  account reads only, no write path**
- Related:
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md),
  [`../architecture/2026-09-11-phase-1a-architecture-report.md`](../architecture/2026-09-11-phase-1a-architecture-report.md) §11,
  [`2026-09-11-phase-1b-appshell-implementation-report.md`](2026-09-11-phase-1b-appshell-implementation-report.md),
  [`2026-09-11-phase-2a-qdn-read-pipeline-report.md`](2026-09-11-phase-2a-qdn-read-pipeline-report.md)

## 1. Status

**PASS WITH OWNER VALIDATION REQUIRED.**

The Phase 2B exit criterion is met at the source, automated and local-browser
layers: ordinary browsing remains permission-free, an explicit Owner/Studio
capability flow exists, capability is derived from the connected account plus
the **current** owner of the app's publishing name (resolved at runtime, never
from payload fields or hardcoded values), the missing-name / non-owner /
declined / unavailable states fail closed and are truthful, no write path
exists, and the Phase 2A visitor QDN read pipeline is regression-free.

Real Qortal host behaviour is **REAL HOST VALIDATION NOT VERIFIED**:
no local Qortal node, no node data directory, no node API port and no usable
Hub Developer Mode session are available in this environment, and the app's
`APP` resource is not published yet (`NOT_PUBLISHED`). Everything that depends
on a live host is **OWNER VALIDATION REQUIRED** (see §9–§10).

## 2. Baselines and preserved changes

| Repository | Path | Branch | HEAD (before) | origin/main | Worktree |
| --- | --- | --- | --- | --- | --- |
| Canonical workspace | `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace` | `main` | `919b975` | `919b975` | clean |
| Application | `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL` | `main` | `450dbcf` | `450dbcf` | clean |

No pre-existing uncommitted owner work was present; nothing was overwritten,
reverted, reset or restored. No commit, push, tag or GitHub mutation was
performed.

## 3. Objective and exit criterion

Implement and validate the Shadow Archives identity / owner-capability boundary
against the current verified Qortal host contracts while preserving entirely
permission-free public browsing, and add no QDN write, transaction, publishing,
comment, like, tip, mail or moderation-write behaviour. All bounds are met
(evidence in §4–§8 and §11–§15).

Phase 2B non-goals were respected: no publish/editor modal, no TipTap, no media
upload, no moderation writes, no catalog publication, no Q-Tube/Subwire
publishing interop, no `qapp-core` root import, no MUI/editor/video dependency.

## 4. Verified auth / name bridge contracts (source + live read-only research)

Reference revisions re-confirmed as upstream `HEAD` (`git ls-remote`) and present
locally at the pinned revisions:

- Qortal Core `108bf191d42d710ec617f535af30cfd82fc03c87` (v6.1.9) —
  `src/main/resources/q-apps/q-apps.js`, `src/main/java/org/qortal/api/resource/NamesResource.java`,
  `src/main/java/org/qortal/api/model/NameSummary.java`, `src/main/java/org/qortal/data/naming/NameData.java`,
  `src/main/java/org/qortal/api/proxy/resource/DevProxyServerResource.java`.
- Qortal Hub `12a573b27246e8a626b24794830c6bc432d1b05d` —
  `src/hooks/useQortalMessageListener.tsx`, `src/qortal/qortal-requests.ts`,
  `src/qortal/get.ts`, `src/background/background.ts`.

Live read-only contract verification used `https://api.qortal.org` (terminal,
read-only; **not** host-behaviour proof).

### 4.1 Operation classes

| Operation | Class | Verified behaviour |
| --- | --- | --- |
| `SEARCH_QDN_RESOURCES`, `FETCH_QDN_RESOURCE`, `GET_QDN_RESOURCE_STATUS`, `GET_QDN_RESOURCE_URL` | Public/idempotent node read | Handled locally by injected `q-apps.js` against the node API; no approval |
| `GET_NAME_DATA` | Public/idempotent node read | `GET /names/{name}` → `NameData` (`{name, owner, ...}`) |
| `GET_ACCOUNT_NAMES` | Public/idempotent node read | `GET /names/address/{address}` → `NameSummary[]` = `[{name, owner}]` |
| `GET_PRIMARY_NAME` | Host-mediated read (not approval-gated) | Hub `getNameInfoForOthers(address)` → `GET /names/primary/{address}` → name string, or `''` |
| `GET_USER_ACCOUNT` | **Permissioned host-mediated auth** | Hub checks saved permission (`qAPPAutoAuth-<appName>`) and session permission; otherwise opens an approval dialog; returns `{address, publicKey}` on accept; throws on decline |
| `PUBLISH_*`, `SIGN_TRANSACTION`, `SEND_CHAT_MESSAGE`, name/transaction ops | Writes | **Not used in this phase** |

### 4.2 Response-shape evidence

- `GET_USER_ACCOUNT` → `{address, publicKey}` only — no name.
- `GET_ACCOUNT_NAMES` → `[{name, owner}]` — **not** bare strings.
- `GET_NAME_DATA` → `NameData` with `owner`; unknown name → `HTTP 404 {"error":401,"message":"name unknown"}`, which `q-apps.js` surfaces as a bridge error.
- `GET_PRIMARY_NAME` → string (`''` when none).
- Core percent-encodes spaces in `_qdnName` (`Shadow%20Archives`); the app decodes it for display/ownership and re-encodes the path segment for the `/names/{name}` lookup.

### 4.3 Verified Hub permission UX and one documented limitation

Hub `getUserAccount` checks a persisted permission and a session permission
first; only otherwise does it call `getUserPermission` (approval dialog). Core
gives `GET_USER_ACCOUNT` a one-hour default timeout because the user may take a
long time to decide.

**Verified limitation (not app-fixable).** Hub wraps a declined dialog in a
generic error (`question:message.generic.user_declined_request` →
`auth:message.error.fetch_user_account` → posted as `error: 'Unable to get user
account'`). The app therefore cannot always distinguish a user decline from a
host/connection error by message text. Consequences, all safe:

- capability keeps a distinct `permission-denied` state when a denial is
  detectable, and an `error` state otherwise;
- a failure is cached for the session in both cases, so **no automatic retry**
  ever occurs;
- an explicit user-triggered retry is always available;
- no failure path can produce `owner` or `authenticated-non-owner`.

## 5. Capability state machine

Pure derivation lives in `src/qortal/capability.ts`; the lifecycle is owned by
`src/app/providers/AuthProvider.tsx`.

| State | Condition | Owner UI |
| --- | --- | --- |
| `unknown` | no bridge, dev-proxy context, auth idle, or resolution finished with no proof | hidden |
| `requesting-permission` | `GET_USER_ACCOUNT` in flight (approval dialog open) | pending + Cancel |
| `resolving-ownership` | account granted, names/ownership lookups not finished | pending |
| `permission-denied` | permission decision rejected (where detectable) | read-only + explicit Try again |
| `error` | host/bridge failure, including a Hub-masked decline | read-only + explicit Try again |
| `visitor` | permission granted but no account returned | read-only |
| `authenticated-no-name` | account owns zero registered names | truthful explanation, no owner controls |
| `authenticated-non-owner` | account owns names but not the app publishing name | truthful explanation, no owner controls |
| `owner` | `GET_NAME_DATA(publisherName).owner === account.address` | capability/status shell only |

Derivation order is fail-closed: no bridge / proxy → `unknown`; then lifecycle;
then `account`; then positive owner proof; then `no-name`; then `non-owner`;
then `resolving`; then `unknown`. Owner is never inferred optimistically.

## 6. Permission UX and session behaviour

- One explicit entry point: the lazy `/studio` route (Owner studio). Loading it
  issues **no** account request; the "Enter owner mode" button is the only thing
  that calls `GET_USER_ACCOUNT`.
- `requestAccount()` is single-flight and caches both the granted account and any
  session failure. Concurrent callers share one in-flight promise, so a user
  never sees duplicate simultaneous prompts.
- A rejection/failure is not replayed automatically. `retryAccount()` clears the
  cached failure and is only reachable from an explicit Studio control
  ("Try again" / "Check again" / "Re-check ownership").
- "Cancel" during a pending request abandons that capability run (generation
  token) and returns the app to a usable read-only state; a late host result is
  ignored by the UI.
- A user with a previously granted/remembered permission is not re-prompted:
  the cached session account is reused and ownership is re-resolved.
- No account secrets are persisted; only the in-memory session account
  (`address`, `publicKey`) as required by the verified contract. No custom
  password/login system exists.

## 7. Ownership-resolution algorithm

```text
publisherName = decodeQdnName(_qdnName)                 // never hardcoded
if no bridge or _qdnContext === "proxy" -> unknown      // never owner
explicit user action -> GET_USER_ACCOUNT -> {address, publicKey}
  -> GET_ACCOUNT_NAMES(address) -> ownNames[]           // NameSummary[]
  -> GET_NAME_DATA(encodePath(publisherName)).owner
  -> owner  iff ownerAddress === account.address
```

- Authority is the **current** registered owner of the publishing name; a name
  transfer changes the answer on the next explicit resolution (verified by test
  and by `Re-check ownership`).
- Payload `author`/`owner`/`publisher` fields never participate.
- A name lookup failure/malformed payload yields `null` (unknown), never `true`.
- A missing `_qdnName` yields `null` ownership → `unknown`, never `owner`.

## 8. Multiple-name behaviour and Studio UI

- `GET_ACCOUNT_NAMES` is parsed as `NameSummary[]` and every name is retained
  individually (`ownedNames`); names are never collapsed into one identity.
- The owner status shell shows the publishing name, the connected account
  (shortened) and the number of registered names — enough for a future
  acting-name selector, whose UI is not part of this phase.
- `authenticated-no-name` is reached when the account owns zero names, and says
  so truthfully.
- Studio/Owner Mode is an information/capability shell. It contains no publish,
  upload, edit, comment, like, moderation or editor control. An owner sees
  "Owner capability verified", "Re-check ownership" and "Sign out of owner
  mode" only.
- `/studio` is intentionally **not** linked from public navigation (Phase 1A
  decision; the existing `AppShell.test` asserts this). The entry point is the
  documented route; this is flagged as an owner decision in §14.

## 9. Real-host validation

**REAL HOST VALIDATION NOT VERIFIED.**

Environment detection performed on 2026-09-11:

- No `java`/Qortal node process is running; no Qortal node data directory and no
  packaged node (`qortal*.jar`/`qortal*.sh`) exists under `/home/iffi`.
- No node API is listening on `12391`, `62391` or other probed local ports.
  (Ports are environment-specific; this is a detection result, not a constant.)
- Qortal Hub 3.0.3 AppImage and a Hub profile exist, and an X display (`:0.0`)
  is present, but Hub Developer Mode is served by the **local Core node**
  (`DevProxyServerResource`; Hub calls `${baseApi}/developer/proxy/start`), so a
  synced local node is required. None is available, and syncing mainnet from
  genesis is out of scope for this task.
- The published-resource context is also unavailable: the `Shadow Archives` name
  is registered and currently owned by `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`, but
  the `APP` resource is `NOT_PUBLISHED` (live read-only status check), so no real
  render context with an injected `_qdnName` can exist yet.

The following host items therefore remain **NOT VERIFIED**: `_qdnBase` routing
under the real host path, injected `_qdnName`/`_qdnService`/`_qdnContext`,
live-host `SEARCH_QDN_RESOURCES`/`FETCH_QDN_RESOURCE` via `q-apps.js`, same-origin
`/arbitrary/...` media, `qortal://` link interception, production CSP, clipboard
behaviour inside the Q-App iframe, and the real `GET_USER_ACCOUNT` grant/reject
UX.

No host behaviour was substituted with public-node browser calls.

### 9.1 Local runtime / browser evidence actually obtained

A headless Chrome (CDP) smoke test ran against the production build with an
injected QDN environment and a mock `qortalRequest`, using an empty basename so
vite preview could serve the relative-asset build:

- Studio `/studio` before any action: `GET_USER_ACCOUNT` calls = **0**; the
  "Enter owner mode" control is present; only public `SEARCH_QDN_RESOURCES`
  reads occur.
- After the explicit action: `GET_USER_ACCOUNT` calls = **1**; `GET_NAME_DATA`
  was called with `name = "Shadow%20Archives"` (correct re-encoding); the only
  action button is "Sign out of owner mode" (plus "Re-check ownership"); no
  publish control.
- Home `/`: `GET_USER_ACCOUNT` calls = **0**.
- No uncaught exceptions or error-level console/CSP log entries.

This is local runtime/browser evidence only, not host validation.

### 9.2 Manual owner validation checklist (compact)

1. Start a synced local Qortal node and open Qortal Hub with a wallet/account;
   confirm Hub Developer Mode is enabled.
2. Publish the app (or an equivalent test APP) under a name — required for a real
   `_qdnName` render context; this is a future write-phase step.
3. `npm run dev`; add `127.0.0.1:5173` as a Hub dev app (proxy context).
4. In the host, confirm `_qdnBase`/`_qdnName`/`_qdnService` and that the shell +
   lazy chunks load under the real base path.
5. Browse Home/Blog/Videos/Gallery/taxonomy/Search: confirm **zero**
   `GET_USER_ACCOUNT` and no permission prompt.
6. Open `/studio` (no prompt on load) → "Enter owner mode" → approve: exactly one
   prompt; result matches current name ownership.
7. With a fresh profile, decline: confirm a distinct denial path, no auto-retry,
   and that "Try again" performs an explicit retry.
8. With a non-owner account, and after transferring the publishing name, use
   "Re-check ownership": capability must become non-owner.
9. Confirm no publish/transaction/write request is ever issued.

## 10. `_qdnBase` / `_qdnName` / QDN read / media / CSP / clipboard observations

- Source-verified: Core injects `_qdnContext`, `_qdnTheme`, `_qdnLang`,
  `_qdnService`, `_qdnName`, `_qdnIdentifier`, `_qdnPath`, `_qdnBase`,
  `_qdnBaseWithPath`; `_qdnName` percent-encodes spaces; dev proxy injects an
  empty name/base.
- The production build uses Vite `base: ''` (relative assets) with
  `_qdnBase` as the router basename — the current template pattern. A hard reload
  at a deep client route under the real host is **NOT VERIFIED**.
- Phase 2A read behaviour and media URL construction are unchanged; live
  `/names/*` reads were used only for contract verification.
- Host CSP, `qortal://` interception and in-iframe clipboard behaviour are
  **NOT VERIFIED**; the clipboard cascade implementation is unchanged from
  Phase 2A.

## 11. Tests

Full suite: **31 files / 295 tests passing** (Phase 2A: 29 files / 258 tests).

New / updated:

- `src/qortal/auth.test.ts` (new, 19 tests) — single-flight account request,
  session caching, cached rejection with no auto-retry, explicit retry,
  malformed response fails closed, `NameSummary[]` parsing (objects + tolerant
  strings + malformed fail-closed), `GET_NAME_DATA` encoding and malformed
  handling, `GET_PRIMARY_NAME`, ownership true/false/unknown.
- `src/qortal/capability.test.ts` (updated, 13 tests) — every state, transient
  states, `permission-denied` vs `visitor`, `error` vs `visitor`, no-name vs
  non-owner ordering, missing `_qdnName`, never-owner-optimistically.
- `src/features/owner/StudioPage.test.tsx` (rewritten, 14 tests) — no permission
  request on load, exactly one `GET_USER_ACCOUNT` from the explicit action, no
  second trigger while pending, cancel returns to read-only, decline does not
  auto-retry but explicit retry works, host error is not shown as non-owner,
  non-owner/no-name/missing-name/malformed states, name-transfer revokes owner,
  owner shell has no publish control, proxy and plain-browser notices.
- `src/app/providers/auth-isolation.test.tsx` (new, 2 tests) — public routes in
  an unscoped hosted context issue **no bridge call at all**, and a scoped
  archive read never issues `GET_USER_ACCOUNT`.

Commands run: `npm run lint`, `npm run typecheck`, `npm test`,
`npm run build`, `npm run format:check`, `git diff --check`,
`bash -n tools/validate-workspace.sh`, `bash tools/validate-workspace.sh`
(**PASS**, 5 warnings for human review, all pre-existing documentation
warnings).

## 12. Build sizes

Production build (Vite 7.3.6, 2026-09-11):

- Entry chunk: **383.72 kB raw / 120.51 kB gzip** (Phase 2A: 382.32 kB /
  120.25 kB → **+1.40 kB raw / +0.26 kB gzip**).
- Stylesheet: 25.24 kB / 4.88 kB gzip.
- Lazy `StudioPage` chunk: **5.68 kB / 1.86 kB gzip** (capability UI only; not
  in the visitor startup graph).
- Lazy `BlogPostPage` (DOMPurify) chunk unchanged: 36.49 kB / 14.15 kB gzip.

The owner-capability code adds no editor/video/framework dependency; the visitor
startup regression is negligible and explained by the extended capability
derivation.

## 13. Adversarial self-audit

| # | Check | Result | Class |
| --- | --- | --- | --- |
| 1 | `GET_USER_ACCOUNT` on startup | No call; AuthProvider has no mount effect; test + browser smoke | — |
| 2 | Auth prompt on normal read routes | None; isolation test proves zero on public routes | — |
| 3 | Duplicate auth prompts | Single-flight module promise + provider in-flight guard; test | — |
| 4 | Rejection retry loop | Failure cached; no auto-retry; explicit retry only; test | — |
| 5 | Owner inferred from hardcoded publishing name | No hardcoded name/address in logic (grep clean) | — |
| 6 | Owner inferred from payload fields | Ownership only from `GET_NAME_DATA.owner` | — |
| 7 | Stale cached ownership surviving a transfer | Re-resolved per explicit run; transfer test revokes owner | — |
| 8 | Dev proxy treated as owner | `isProxy` → `unknown`; test + proxy notice | — |
| 9 | Account address treated as acting-name identity | Address, `ownsAnyName`, `ownedNames[]` and `ownsPublisherName` are separate | — |
| 10 | Multiple names collapsed | `NameSummary[]` retained individually; test | — |
| 11 | Permission error shown as "not owner" | Distinct `permission-denied` / `error` states; test | — |
| 12 | Host unavailable shown as `visitor` | `unavailable` → `error`; bridge-less → `unknown`; test | — |
| 13 | Secret/account material logged | No `console.*` in new code; no persistence | — |
| 14 | Write bridge action accidentally invoked | None referenced in production code; types only | — |
| 15 | Publishing button accidentally enabled | Owner shell has no publish control; test + browser smoke | — |
| 16 | `qapp-core` reintroduced | Not a dependency | — |
| 17 | MUI/editor/video dependency reintroduced | Not a dependency | — |
| 18 | Phase 2A read regression | Full suite green; pipeline untouched | — |
| 19 | Startup bundle regression without explanation | +0.26 kB gzip, explained; Studio lazy chunk | — |
| H1 | `GET_ACCOUNT_NAMES` parsed as `string[]` but contract is `NameSummary[]` (names silently discarded; `no-name`/`non-owner` mis-classified on a real node) | **Fixed in phase** | HIGH |
| H2 | `authenticated-no-name` unreachable: provider hardcoded `ownsAnyName: null`, and derivation checked non-owner before no-name | **Fixed in phase** | HIGH |
| H3 | No user entry point: `authenticate` was dead code; a real host would have shown a permanent inert placeholder | **Fixed in phase** (Studio flow) | HIGH |
| H4 | No retry after decline (cached failure made explicit retry impossible) and no truthful denial state | **Fixed in phase** (`retryAccount`, `permission-denied`) | HIGH |
| M1 | Hub masks a declined dialog as a generic error; app cannot always distinguish decline from host error | **Mitigated + documented**: distinct where detectable, otherwise fail-closed `error`, no auto-retry, explicit retry | MEDIUM |
| M2 | `/studio` is not in public navigation (Phase 1A) | Left as approved architecture; flagged for owner decision | MEDIUM |
| M3 | `_qdnBase` deep-path hard reload with relative assets | **NOT VERIFIED** (host-only) | MEDIUM |

No BLOCKER or unresolved HIGH finding remains.

## 14. Unresolved unknowns / owner decisions

1. Real-host behaviour is unverified until a synced local node + Hub Developer
   Mode exist, and a real render context exists only after first publication
   (**first-publication bootstrap** — a future write phase; the authority model
   is not weakened for it).
2. Whether `/studio` should become discoverable from public navigation for a
   verified owner (currently URL-only, per Phase 1A). This is an owner product
   decision, not a defect.
3. Whether a future acting-name selector should list `ownedNames` in Studio.
4. Hub's masked-decline behaviour may make a real denial appear as `error` until
   Hub (or a future host action) exposes a distinct decline signal.

## 15. Files changed

Application (`/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`):

- `src/qortal/types.ts` — `QortalNameSummary`, transient capability states,
  `ownershipResolved`.
- `src/qortal/capability.ts` — fail-closed state derivation; no-name vs
  non-owner ordering.
- `src/qortal/auth.ts` — `NameSummary[]` contract fix, name re-encoding,
  explicit `retryAccount`, malformed-response fail-closed.
- `src/qortal/index.ts` — exports.
- `src/app/providers/AuthProvider.tsx` — lifecycle, single-flight, retry,
  cancel, separate name/ownership resolution.
- `src/app/providers/CapabilityProvider.tsx` — wire `ownsAnyName` /
  `ownershipResolved`.
- `src/features/owner/StudioPage.tsx` — real capability shell with one explicit
  auth entry and truthful states.
- `src/styles/content.css` — Studio status styles.
- `src/qortal/auth.test.ts` (new), `src/qortal/capability.test.ts` (updated),
  `src/features/owner/StudioPage.test.tsx` (rewritten),
  `src/app/providers/auth-isolation.test.tsx` (new).

Workspace:

- `projects/shadow-archives-webportal.md` — factual Phase 2B status.
- `docs/shadow-archives-webportal/implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md`
  (this report).

## 16. Git state

| Repository | Branch | HEAD | origin/main | Status |
| --- | --- | --- | --- | --- |
| Workspace | `main` | `919b975` | `919b975` | 1 modified + 1 new doc (uncommitted) |
| Application | `main` | `450dbcf` | `450dbcf` | 10 modified + 2 new files (uncommitted) |

No commit, push or tag was performed.

---

Report saved:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md`
