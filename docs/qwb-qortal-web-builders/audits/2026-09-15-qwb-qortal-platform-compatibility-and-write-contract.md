# Current Qortal compatibility + QDN write/delete contract — qwb-qortal-web-builders/architecture-audit-20260915

Executing agent (registered role of the agent that actually produced this work): `DeepSeek`
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence: source inspection and the freshness gate were performed by the DeepSeek
model through the local Codex CLI profile (the profile is not the executor).
Report type: platform compatibility + contract verification (read-only; no QDN reads or writes)
Scope: **Qortal only.** No Qortium behavior or contract was transferred.

All statements below are **VERIFIED** against the pinned revisions in §1 unless marked otherwise.
Nothing here is from memory or from stale documentation.

---

## 1. Reference freshness gate (executed 2026-09-15 12:51 UTC)

The gate was run per `AI-Orchestration/ENVIRONMENT.md`: live `git fetch`, then local-vs-upstream SHA
comparison. All four references are **clean, tracking, and equal to upstream — no delta**.

| Reference | Local path | Branch | HEAD (local = upstream) | Upstream date | Result |
| --- | --- | --- | --- | --- | --- |
| Qortal Core | `/home/iffi/VsCodec-Projects/github-clones/Qortal/qortal` | `master` | `108bf191d42d710ec617f535af30cfd82fc03c87` (v6.1.9) | 2026-07-08 | FRESH |
| Qortal Hub | `…/Qortal/Qortal-Hub` | `develop` | `12a573b27246e8a626b24794830c6bc432d1b05d` | 2026-08-23 | FRESH |
| qapp-core | `…/Qortal/qapp-core` | `master` | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` (1.0.79) | 2026-05-25 | FRESH |
| qapp-templates | `…/Qortal/qapp-templates` | `main` | `143cc7bffd265f543f96ef25bf1b58ef7bb04472` | 2026-05-25 | FRESH |
| Reference app | `…/Qortal/iffi-vaba-mees-QORTAL` | `main` | `64f55bf7b6f4a1a093f19413d3a985e61a9fad37` | 2026-06-11 | new clean clone |

Runtime correlation (recorded, **not** re-probed in this audit): `ENVIRONMENT.md` records that
`/apps/q-apps.js` served by live nodes `127.0.0.1:24991` / `:24992` (Core `qortal-6.1.9-108bf19`)
was byte-identical to the inspected clone file (md5 `3ae7deaa55f353dc0ae4e8d13f3c1034`, 37 604 bytes).
The inspected local file has the same md5 and size, so the bridge source read here is the code the
node serves. Node reachability was **not** re-verified in this task (no node query was needed).

Bridge actions classified by approval boundary — the essential model:

| Class | Actions (current) | Where handled | Retry policy |
| --- | --- | --- | --- |
| Public/idempotent node reads | `SEARCH_QDN_RESOURCES`, `FETCH_QDN_RESOURCE`, `GET_QDN_RESOURCE_STATUS`, `GET_QDN_RESOURCE_PROPERTIES`, `GET_QDN_RESOURCE_METADATA`, `GET_QDN_RESOURCE_URL`, `LIST_QDN_RESOURCES`, `GET_NAME_DATA`, `GET_ACCOUNT_NAMES`, `GET_ACCOUNT_DATA`, `SEARCH_NAMES`, `GET_PRICE`, block/tx reads | Core `q-apps.js` → node API | bounded retry allowed |
| Host-mediated permissioned reads | `GET_USER_ACCOUNT` (returns `{address, publicKey}`), `GET_WALLET_BALANCE`, `GET_LIST_ITEMS` | Hub approval dialog / session permission | **no** automatic retry |
| Host-mediated signed writes | `PUBLISH_QDN_RESOURCE`, `PUBLISH_MULTIPLE_QDN_RESOURCES`, `SEND_CHAT_MESSAGE`, `SEND_COIN`, group/AT/trade actions, `ADD_LIST_ITEMS`, `DELETE_LIST_ITEM` | Hub approval + signing | **no** automatic retry |

`q-apps.js` handles the first class locally and forwards everything else to the host
(`default:` → `requestedHandler = "UI"` → `parent.postMessage`). Current bridge action list read
from `src/main/resources/q-apps/q-apps.js`.

## 2. Injected context variables (what the app can know about itself)

Core `src/main/java/org/qortal/api/HTMLParser.java:72` injects, into the app's own document:

```js
var _qdnContext, _qdnTheme, _qdnLang, _qdnService, _qdnName, _qdnIdentifier,
    _qdnPath, _qdnBase, _qdnBaseWithPath;
```

- `_qdnName` = the **registered name that published/owns the rendered resource** (`resourceId`) —
  this is the app's publishing identity.
- `_qdnService` = `APP` / `WEBSITE` (or other service being rendered).
- `_qdnContext` ∈ `render` | `proxy` | `gateway` | `domainMap`.
- `<base href>` is set from `_qdnBase` (or `_qdnBaseWithPath` when Core auto-routed to the index),
  so **relative asset/route URLs resolve against the resource path**.
- Documentation discrepancy to report rather than silently resolve: the public Q-Apps API page
  documents only `_qdnTheme` and `_qdnContext`, while the source injects the nine variables above
  (already recorded in the workspace standard; source remains authoritative).
- **Developer-mode caveat (VERIFIED in the workspace guide and consistent with Core's dev proxy
  implementation):** under the Hub Developer Mode proxy, `_qdnName`, `_qdnIdentifier` and `_qdnBase`
  are empty. Consequence for QWB: **owner mode cannot be exercised through the dev proxy at all**;
  it must be validated in a real published-app context. Do not "fix" this by hardcoding a name.

## 3. Rendering, routing and CSP constraints

- **VERIFIED** production render CSP:
  `default-src 'self' 'unsafe-inline' 'unsafe-eval'; font-src 'self' data:; media-src 'self' data:
  blob: http://127.0.0.1:* http://localhost:*; img-src 'self' data: blob:; connect-src 'self' wss:
  blob:`.
  Consequences: no Google Fonts/CDN scripts; self-hosted webfonts only (`font-src 'self' data:`);
  images must be same-origin (`img-src 'self' data: blob:`) — i.e. served from the node.
- **VERIFIED** (Core `arbitrary/ArbitraryDataRenderer.java`): index-fallback routing is applied
  **only when `service == APP`** — an unhandled path is forwarded to `index.html` and the base is
  switched to `usingCustomRouting` mode. For `WEBSITE`, a missing file is a 404. This matches the
  official documentation, so no discrepancy.
- **VERIFIED** (`WEBSITE` validation in `Service.java`): a `WEBSITE` resource must contain an index
  file at its root (`index.html`/`index.htm`/`default.html`/`default.htm`).
- **VERIFIED** (Core `q-apps.js` click interceptor): clicks on `http://`, `https://` and `//` links
  are `preventDefault()`-ed ("Block external links"); `qortal://` links are converted into
  `LINK_TO_QDN_RESOURCE` requests. External web links are therefore dead inside a Qortal host.
- **VERIFIED** (Core `q-apps.js`): relative `img` sources are rewritten to resource URLs, but the
  implementation calls `document.querySelector("img")` (first match) rather than the current
  element, so it must not be relied on. Use **absolute** `/arbitrary/<service>/<name>[/<identifier>]`
  URLs for media, and never a relative path (a relative path resolves under `<base href>` and the
  node returns the app shell HTML, rendering as a broken image).

## 4. Host events available to an app

Only these host→app messages were found in Hub `src/components/Apps/AppViewer.tsx` and
`src/hooks/useQortalMessageListener.tsx` (source-verified list): `THEME_CHANGED`,
`LANGUAGE_CHANGED`, `NAVIGATE_TO_PATH`, `NAVIGATE_FORWARD`, `SET_TAB_SUCCESS`,
`PUBLISH_STATUS`, group/direct/notification events. **There is no account-changed or
account-switched event.** Owner mode therefore cannot rely on a push notification after the user
switches accounts; it must re-derive ownership on load and before any write.

`PUBLISH_STATUS` is an optional progress channel posted during chunk submission with
`{ publishLocation, chunks, totalChunks, retry, filename, processed }`; it is host-internal in shape
and is not a substitute for verifying the served resource.

## 5. QDN service limits relevant to this content model

Read from Core `arbitrary/misc/Service.java` (value, requiresName, maxSize, …):

| Service | Max size | Notes |
| --- | --- | --- |
| `JSON` | **25 KB** | override validates that the payload parses as JSON (`objectMapper.readTree`) |
| `THUMBNAIL` | **500 KB** | the natural home for card/cover images |
| `IMAGE` | **10 MB** | larger stills |
| `DOCUMENT` | no size limit | JSON-in-DOCUMENT is what the reference app uses |
| `APP` | 50 MB | multi-file; **unknown paths route to `index.html`** |
| `WEBSITE` | no explicit limit | multi-file; **missing paths 404**; must contain a root index file |
| `LIST` / `PLAYLIST` | none | node/API-managed lists |

`SEARCH_QDN_RESOURCES` bridge fields (current, camelCase, translated to lowercase REST names by
`q-apps.js`): `service`, `query`, `identifier`, `name`, `names`, `keywords`, `title`, `description`,
`prefix`, `exactMatchNames`, `default`, `mode`, `minLevel`, `includeStatus`, `includeMetadata`,
`nameListFilter`, `followedOnly`, `excludeBlocked`, `before`, `after`, `limit`, `offset`, `reverse`.
Passing the node's lowercase REST names to the bridge silently produces an unfiltered query.
Identifier matching is substring matching unless `prefix: true`; correctness therefore requires
post-filtering on exact `service`/`name`/`identifier`.

## 6. Publish / update semantics (the write contract)

- **Overwrite on identical identity.** Core indexes the latest transaction by
  `(name, service, identifier)` (`ArbitraryTransaction.java` ~415–470): the newest transaction wins,
  `created` is kept as the oldest timestamp, `updated` is set to the latest transaction timestamp
  (and is `null` when the resource was never updated). There is no "create vs update" distinction
  and no optimistic concurrency check — the last accepted publish wins.
- **Host approval.** Hub `publishQDNResource` requires `service`, one of `file`/`data64`/`base64`,
  and asks for approval unless a **session permission** for `PUBLISH_QDN_RESOURCE` already exists
  for that app name + tab; the dialog shows service, identifier, name and fee. Practical
  consequence: only the *first* publish in a session prompts; later writes are silent. The app must
  therefore make its own intent explicit (e.g. an "Edit" modal) rather than relying on the host
  dialog as a confirmation step.
- **Timeouts (Core `getDefaultTimeout`)**: `PUBLISH_QDN_RESOURCE` /
  `PUBLISH_MULTIPLE_QDN_RESOURCES` = 60 min (proof-of-work can be slow), `FETCH_QDN_RESOURCE` =
  60 s, `SEARCH_QDN_RESOURCES` = 30 s, `GET_USER_ACCOUNT` = 60 min (the user may take time at the
  permission dialog).
- **Result semantics.** A resolved publish means the host accepted, signed and relayed a
  submission. It is **not** proof that the node now serves the new bytes. Verification requires a
  later read (`GET_QDN_RESOURCE_STATUS` and/or re-reading the payload) and an explicit comparison
  against the intended revision.
- `PUBLISH_MULTIPLE_QDN_RESOURCES` is grouped UI approval over independent resources, so partial
  success is possible and must be handled per resource.
- **Gateway behaviour is a trap (VERIFIED).** In `q-apps-gateway.js`, `GET_USER_ACCOUNT`,
  `PUBLISH_QDN_RESOURCE`, `PUBLISH_MULTIPLE_QDN_RESOURCES`, `SEND_CHAT_MESSAGE`, `ADD_LIST_ITEMS`,
  `DELETE_LIST_ITEM`, etc. do **not** reject: they call `handleResponse` with the string
  `{"error": "Interactive features were requested, but these are not yet supported when viewing via
  a gateway…"}` (unless a browser extension is installed). `handleResponse` `JSON.parse`s it, so the
  caller receives a **resolved object with an `error` property**. An app that only catches
  exceptions will report a successful publish on a gateway. Every write path must treat
  `response?.error` as a failure and every identity path must treat a missing `address` as
  "no owner".

## 7. Delete contract — what actually exists (decisive for the content model)

**There is no app-accessible QDN resource delete in current Qortal.**

| Candidate | Verdict |
| --- | --- |
| `DELETE_QDN_RESOURCE` bridge action | **Does not exist.** Not in Core `q-apps.js`'s action list, not in Hub `src/qortal/qortal-requests.ts`, not referenced anywhere in Core Java. |
| Core REST `DELETE /arbitrary/resource/{service}/{name}/{identifier}` | Exists (`ArbitraryResource.java:726`) but requires `@SecurityRequirement(name="apiKey")` + `Security.checkApiCallAllowed(request)` — a **node-admin API-key call**. It also deletes **locally on that node only** (`ArbitraryDataResource.delete(repository, false)` removes local files + cached index entries). It does not remove the on-chain transaction, does not propagate, and other nodes keep serving the resource. Not available to a Q-App, and not a network-level delete even for an admin. |
| Host `DELETE_LIST_ITEM` | Exists (Hub `deleteListItems` → `DELETE /lists/{listName}`), user-approved, but operates on **node-local named lists**, not QDN resources. Useful for "follow/list"-style local state only. |
| Host `DELETE_HOSTED_DATA` | Hub-internal hosted-data management, not a QDN resource delete. |
| On-chain tombstone / "deleted" resource state | **Does not exist** for arbitrary resources. Status values describe availability (`READY`, `DOWNLOADING`, `MISSING_DATA`, `BUILDING`, `PUBLISHED`, `NOT_PUBLISHED`, `UNSUPPORTED`, `BLOCKED`), not intent. |

Consequences for the design (carried into the architecture proposal):

1. "Delete" must be **logical**: republish the same `(name, service, identifier)` with a payload that
   marks the entity withdrawn (e.g. `state: 'deleted'` + `deletedAt`), and filter those entities out
   of every read path — listing, detail, search, and any derived index rebuild.
2. A tombstoned entity must never be re-added as active by a repair/reconcile pass (the rule already
   recorded in `skills/qortal/qdn-derived-index-coherence`, §6).
3. Physical purge is only possible for the publishing account by publishing *new content* under the
   same identifier; the old bytes remain retrievable from the chain/other nodes. The UI must not
   promise "removed from the network".
4. Because the identifier can never be reused for a different entity without destroying history,
   identities must be generated once and never recycled.

## 8. Ambiguous-write risks to design against

| Risk | Why | Required handling |
| --- | --- | --- |
| Silent no-op after user cancellation | The host permission dialog may be declined; the bridge call rejects (exception) — distinguishable from submission | Surface "rejected", keep the draft |
| Session permission suppresses later dialogs | After the first publish, further publishes in the session are silent | The app owns confirmation UX; never treat silence as success |
| 60-minute publish timeout | Resolves long after a UI change of context; PoW can be slow | In-flight state per entity, no auto-retry, no double-submit |
| Gateway resolves `{error}` instead of rejecting | See §6 | Treat `error` property as failure everywhere |
| Publish accepted but not yet served | Submission ≠ availability | Verify by re-read before showing the new value as authoritative |
| Two quick edits of the same identifier | Overwrite semantics: last wins, no merge | Disable concurrent edits per entity; compare a revision counter after write |
| `GET_ACCOUNT_NAMES` parameter expectations | The bridge ignores `limit`/`offset`/`reverse` for that action | Treat the response as the complete current name list |

## 9. Old assumptions in the reference app that must be modernized for QWB

| Reference-app assumption | Current reality | Action |
| --- | --- | --- |
| Owner name hardcoded in source | `_qdnName` is injected and identifies the publishing name | derive from `_qdnName` |
| `names[0]` is the owner | `GET_ACCOUNT_NAMES` returns an unordered list | membership check |
| `limit/offset/reverse` on `GET_ACCOUNT_NAMES` | ignored by the bridge | remove |
| `window.parent`/`window.top` bridge probing | Core injects the bridge into the app's own window | remove |
| `GET_QDN_RESOURCE_URL` returns the literal `'Resource does not exist'` | still true, but brittle; status/`GET_QDN_RESOURCE_STATUS` exists | prefer status + absolute URL |
| `btoa(unescape(encodeURIComponent()))` | `unescape` is deprecated | `TextEncoder` |
| Optimistic UI after publish | submission ≠ served bytes | verify, or label as unconfirmed |
| No delete, no tombstones | no QDN delete exists | implement logical deletion |
| DM to a hardcoded address | current owner must be resolved from the publishing name | reuse `skills/qortal/private-chat-contact-form` |
| `PUBLISH_QDN_RESOURCE` with `data64` base64 for everything | still valid, but base64 of large files is memory-expensive in the frame | reserve base64 for JSON payloads and small thumbs; use the host's file/zip path for large media |

## 10. Validation and non-claims

Executed: live `git fetch` freshness gate on four references; source inspection of Core
(`q-apps.js`, `q-apps-gateway.js`, `HTMLParser.java`, `ArbitraryDataRenderer.java`, `Service.java`,
`ArbitraryTransaction.java`, `ArbitraryDataResource.java`, `ArbitraryResource.java`,
`ListsResource.java`, `NamesResource.java`) and Hub (`get.ts`, `qortal-requests.ts`, `AppViewer.tsx`,
`useQortalMessageListener.tsx`) at the pinned SHAs.

**Not executed and not claimed:** no node API call, no QDN read, no QDN write, no real-host
render, no publish, no delete, no owner-runtime acceptance. The `.webmanifest`/external-link and
`img` rewriting findings are source-level verifications, not host-observed behaviour.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-qortal-platform-compatibility-and-write-contract.md`
