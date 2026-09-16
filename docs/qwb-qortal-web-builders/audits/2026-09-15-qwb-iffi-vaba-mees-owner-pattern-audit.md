# Iffi Vaba Mees owner/editing pattern audit — qwb-qortal-web-builders/architecture-audit-20260915

Executing agent (registered role of the agent that actually produced this work): `DeepSeek`
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence: source reading and classification were produced by the DeepSeek model
through the local Codex CLI profile (the profile is not the executor).
Report type: reference-implementation audit (read-only)
Audited revision: `iffinland/iffi-vaba-mees-QORTAL`, branch `main`,
`64f55bf7b6f4a1a093f19413d3a985e61a9fad37` (2026-06-11), clean clone at
`/home/iffi/VsCodec-Projects/github-clones/Qortal/iffi-vaba-mees-QORTAL`
Second branch inspected: `origin/production` `7b2145a71ecb692ccf03b5dc8dd6e7b3596b7784`
(2025-08-28) — **28 commits behind `main`, 0 ahead**, i.e. an ancestor; `main` is the current
reference. No other branch exists.
Platform claims in this report are cross-checked against Qortal Core `108bf191` and Qortal Hub
`12a573b2` in the companion platform report.

**This is a reference, not a template.** The task explicitly excludes the Shadow Archives
Studio owner-auth architecture; nothing from it was used here.

---

## 0. What the app is

React 19 + Vite 7 + `react-router-dom` 7 (`HashRouter`), 42 `.jsx` files, 35 `.js` files, ~13 CSS
modules; no TypeScript; no tests (`eslint` + `vite build` only). Content types: videos, galleries,
blog posts + comments/likes, guestbook, life-story entries, projects, monthly support. QDN
services used: `DOCUMENT`, `IMAGE`, `VIDEO`, `THUMBNAIL`, `PRODUCT` (support records). Identifier
prefixes are documented in `PROJECT_ROADMAP.md` (`ivm_prj_`, `ivm_blog_`, `ivm_ls_`, `ivm_sup_`).

Its own roadmap (`PROJECT_ROADMAP.md`, 2026-06-10) states the product rule that matters most for
QWB: *"The website should remain a Qortal/QDN-powered personal website with modal-based publishing
tools. It should not become a traditional WordPress/Joomla-style CMS."* — directly aligned with the
owner's QWB intent ("no general backend/admin dashboard").

## 1. Owner recognition

### 1.1 Mechanism as implemented

1. `src/utils/siteConfig.js:1-7` hardcodes the owner identity:

   ```js
   export const OWNER_QORTAL_NAME = 'iffi vaba mees';
   export const APP_QORTAL_NAME  = 'iffi vaba mees';
   export const isOwnerName = (name) =>
     typeof name === 'string' && name.trim().toLowerCase() === OWNER_QORTAL_NAME;
   ```

2. `src/services/videoService.js:166-195` `getCurrentUserProfile()` resolves the current account
   and its **first** name:

   ```js
   const account = await requestQortal({ action: 'GET_USER_ACCOUNT' });     // -> { address, publicKey }
   if (!account?.address) return { address: '', name: '', names: [] };      // fail closed
   const namesResponse = await requestQortal({
     action: 'GET_ACCOUNT_NAMES', address: account.address, limit: 20, offset: 0, reverse: false,
   });
   const names = Array.isArray(namesResponse)
     ? namesResponse.map((e) => (typeof e === 'string' ? e : e?.name)).filter(Boolean) : [];
   return { address: account.address, names, name: names[0] ?? '' };
   ```

3. A **byte-for-byte duplicate** of that helper exists at `src/services/guestbookService.js:173-193`.
4. UI owner mode is a client-side boolean derived from `profile.name`:
   `canPublishProjects = isOwnerName(profile.name)` (list page), `canEditProject` (detail page),
   `canPublishEntries`/`canPublishPosts`/`canEditEntry`/`canEditPost` on the other pages.
5. Controls render conditionally: `{canPublishProjects && <button …>Publish project</button>}` and
   the modal is additionally guarded: `isOpen={canPublishProjects && isPublishOpen}`.
6. Write paths re-check the name and throw (`projectService.js:358`, `:411`;
   `lifeStoryService.js:346`, `:401`): `if (!isOwnerName(authorName)) throw new Error('Only the
   site owner can publish projects.')`.
7. Read paths re-check the publisher of every resource: `sanitizeProjectPayload()`
   (`projectService.js:162-200`) returns `null` unless `isOwnerName(summary.name)`, and
   `fetchProjectFromSummary()` (`:222`) and `fetchProjectByIdentifier()` (`:259`) discard
   resources whose `name` is not the owner's.

### 1.2 Evaluation

What is genuinely good and worth keeping:

- **Fail-closed identity resolution**: a missing bridge, no account, a rejected permission dialog
  or an empty response all collapse to `{ address: '', name: '' }`, and `isOwnerName('')` is
  `false`. There is no persisted `owner=true`, no localStorage flag and no default-allow path.
- **Owner mode is derived, not stored**: every page re-resolves the profile on mount, so a reload
  after an account switch re-evaluates.
- **Reader-side publisher gate**: because the app rejects content published under any name other
  than the owner's, a third party cannot inject entries into the app's feed by copying its
  identifier prefix. This is the single most valuable pattern in the whole app and it must be
  carried into QWB.
- **Write-side guard as defence in depth** (not as the security boundary — the real boundary is
  the host approval + the ledger enforcing that only the name owner can publish under that name).
- **No hardcoded address**: identity is name-based, which survives address changes on the same
  name.

What must be modernized or dropped:

| Finding | Impact | Classification |
| --- | --- | --- |
| Hardcoded owner name in app source | The app decides who is owner instead of deriving it from its own publishing identity; a differently-named re-publication of the same code would still grant owner mode to `iffi vaba mees` | **obsolete / avoid** — derive from `_qdnName` |
| `name: names[0]` (first name only) | An account with several names is misdetected when the relevant name is not first; `GET_ACCOUNT_NAMES` ordering is not a contract | **reusable but must be modernized** — membership test, never index 0 |
| `limit: 20, offset: 0, reverse: false` passed to `GET_ACCOUNT_NAMES` | Silently ignored: the bridge maps the action to `/names/address/{address}` with no query parameters | **obsolete / avoid** — misleading dead parameters |
| No verification that the app's publishing name is the owner's | Owner mode and publishing identity are decoupled | **reusable but must be modernized** — compare against `_qdnName` |
| `_qdnName` / `_qdnService` / `_qdnContext` never read anywhere (verified: zero occurrences in the whole repo) | The app cannot tell whether it is in `render`, `proxy`, `gateway` or `domainMap` context, nor which name published it | **obsolete / avoid** — QWB must read the injected context |
| Profile resolved once per mount with no re-verification trigger | After an account switch inside the Hub the app keeps showing owner controls until a remount (the host sends no account-changed event — verified) | **reusable but must be modernized** — re-verify on demand before each write and on visibility regain |
| Duplicate `getCurrentUserProfile` in two services | Divergent behaviour risk | **obsolete / avoid** |
| `getQortalBridge()` probing `window.parent.qortalRequest` and `window.top.qortalRequest` (`qortalClient.js:1-40`) | Legacy assumption; current Core injects the bridge into the app's own window and cross-origin parent access can throw | **obsolete / avoid** |

## 2. Inline editing, modals and quick actions

### 2.1 Where controls are injected (the honest picture)

The task's preferred QWB model is *per-item, in-context* controls. **The reference application does
not implement that model.** Its owner controls are:

| Location | Control | Trigger for visibility |
| --- | --- | --- |
| Page hero of a list page (`ProjectListPage.jsx`) | one "Publish project" button in the header row | `canPublishProjects` |
| Detail page header (`ProjectDetailPage.jsx:129-136`) | one "Edit project" button | `canEditProject` |
| List cards (`ProjectCard.jsx`) | **none** — cards only open the detail route | — |
| Delete | **none anywhere for entities** (see §3) | — |

So the reusable parts are: *owner-only conditional rendering*, the *modal form lifecycle*, and the
*publish/verify service shape*. QWB's per-card `[ Edit ] [ Delete ]` and section-level
`+ Add item` affordances are **new work**, not a port. Concretely, reuse the modal and service
patterns and design the inline affordances fresh.

### 2.2 Modal pattern (`components/projects/ProjectPublishModal.jsx`)

- A single component serves both create and edit: `editProject` prop switches the title
  ("Publish project" / "Edit project") and the initial form (`toEditForm(project)` vs
  `initialForm`).
- Form state is one local `useState(initialForm)` object; `updateField(field, value)` and
  `updateLink`. Repeatable sub-rows are supported (up to 6 links, add/remove) — a directly
  reusable convention for QWB's repeatable fields (service bullet lists, pricing lines).
- The form is re-seeded and errors cleared each time the modal opens (`useEffect` on `isOpen`).
- Client validation is minimal and explicit: title required; "add a summary or description";
  errors surface as an inline `setError(...)` string.
- The overlay is `<div role="dialog" aria-modal="true">`; the close control is a labelled
  `<button aria-label="Close">`.
- `isPublishing`/`isSaving` props flow down to disable the submit control (no double submit).
- On success the page shows a toast and closes the modal; on failure the error stays in the modal.
- Gaps: no focus trap, no Escape-to-close, no `aria-labelledby`, no dirty-state guard on close,
  and the overlay does not stop background scroll.

### 2.3 Publish / update flow

```text
[media]   publish THUMBNAIL cover (same identifier)      ─┐
[entity]  publish DOCUMENT JSON payload (data64 base64)   ─┴─► optimistic local list update
```

- `publishCover()` (`projectService.js:317-355`): client-side canvas downscale (≤1600 px on the
  long edge), JPEG quality iteration until ≤500 KB, `5 MB` upload cap, published to `THUMBNAIL`
  with **the same identifier** as the entity, then `GET_QDN_RESOURCE_URL` resolves a display URL.
- `publishProject()` (`:357-407`): identifier `ivm_prj_<slug>_<base36 timestamp>_<random>`
  (≤60 chars, `sanitizeIdentifierSegment` lowercases/strips); payload published as
  `data64` + `encoding: 'base64'` with `title` ≤80 and `description` ≤240 characters of metadata.
- `updateProject()` (`:410-465`): same identifier, same service, `updated: Date.now()` — i.e. an
  **overwrite by (name, service, identifier)**, which matches current Core semantics.
- Discovery: `SEARCH_QDN_RESOURCES` with `identifier: 'ivm_prj_'`, `prefix: true`, `mode: 'ALL'`,
  `includeStatus: true`, `includeMetadata: true`, `excludeBlocked: true`, `limit/offset/reverse`.
- After publishing, **nothing is verified**: the list is optimistically updated with the returned
  payload. `waitForQdnResourceReady()` exists in `qdnResourceService.js` (bounded poll + one
  `build: true` trigger + terminal statuses) but is used only by the video flow.
- There is no revision counter or content-hash check, so "published" in the UI means "the host
  accepted the submission", not "the node now serves this version".

### 2.4 Delete flow

**There is none.** Verified exhaustively in the audited revision:

- no `DELETE_QDN_RESOURCE` anywhere in the app;
- no tombstone/`deleted`/`withdrawn`/`state` field in any sanitizer or payload;
- the only `delete` occurrences in `.jsx` files are `delete obj[key]` object mutations in the
  comment trees;
- the `FaTrash` icon imported by the publish modal removes a *form row* (a link), not an entity.

This is a **gap QWB must close by design** (see the platform report for the current Core/Hub
capability boundary: there is no app-level QDN delete at all).

### 2.5 Quick actions and visitor-side patterns

- `AudienceActions` (above the nav) exposes visitor actions: **Follow** (writes the app/owner names
  into the node-local `followedNames` list through host-mediated `ADD_LIST_ITEMS`) and **Monthly
  Support** (routes to a support page, voluntary QORT payments, supporter-owned `PRODUCT` records
  with `ivm_sup_`, status shown as an in-page badge rather than a global notification).
- `FooterSocialBar` + `useFooterSocialActions` centralise footer links/actions (Q-Blog, Q-Tube,
  Q-Music, Q-Mail, "Let's chat" which reuses `DirectMessageModal`).
- Convention worth reusing: `canUseFollowAction()` returns false without a bridge and the UI shows
  a plain-language note ("Open this website inside Qortal UI to enable follow controls") instead of
  failing silently.
- `directMessageService.js` sends a DM using `{ action: 'SEND_CHAT_MESSAGE', recipient,
  fullContent: {messageText: {…}, version: 3} }` to a **hardcoded address**
  (`OWNER_CHAT_ADDRESS`). Current Hub accepts both `destinationAddress || recipient` and
  `fullMessageObject || fullContent`, so the app still works, but the canonical current envelope is
  `{ destinationAddress, message }` and the recipient should be resolved from the current owner of
  the app's publishing name. See the verified skill
  `skills/qortal/private-chat-contact-form` (maturity `verified-runtime`, 2026-09-15) — QWB should
  reuse that skill rather than this service.

### 2.6 Other reusable utilities

- `htmlSanitizer.js`: DOMParser-based allowlist (tags + `a[href|title|target|rel]`), scheme
  allowlist (`http`, `https`, `qortal://`, `mailto:`), forced `rel="noopener noreferrer"`, with a
  regex fallback when `DOMParser` is unavailable. Correct in intent, but hand-rolled and only
  regex-guarded in the fallback path.
- `qdnResourceService.js` status normalisation (`localChunkCount`/`totalChunkCount`/`percentLoaded`
  aliases, `READY` / buildable / terminal-error sets) and `waitForQdnResourceReady()`.
- Toast convention: `setToast(msg); setTimeout(() => setToast(''), 2600)`.
- `getQdnResourceUrl()` guards the literal string `'Resource does not exist'`.
- Routing: `HashRouter` — a deliberate choice that keeps deep links working regardless of which
  QDN service renders the app.

## 3. Pattern classification summary

| # | Pattern | Classification |
| --- | --- | --- |
| 1 | Reader-side publisher gate (reject resources not published by the owner name) | **reusable as-is** |
| 2 | Fail-closed identity helper (empty profile on any error) | **reusable as-is** |
| 3 | Owner mode derived per mount, never persisted | **reusable as-is** |
| 4 | Write-side owner guard (defence in depth) | **reusable as-is** |
| 5 | Modal serving both create and edit, re-seeded on open | **reusable as-is** |
| 6 | Repeatable form sub-rows with add/remove | **reusable as-is** |
| 7 | Toast + in-modal error + `isPublishing` disable | **reusable as-is** |
| 8 | Identifier scheme `prefix_slug_timestamp36_random` ≤60 chars | **reusable as-is** |
| 9 | `SEARCH_QDN_RESOURCES` prefix search + post-filter by exact `name`/`identifier` | **reusable as-is** |
| 10 | Bounded QDN status poll with one build trigger and terminal errors | **reusable as-is** |
| 11 | Canvas downscale → JPEG quality iteration → `THUMBNAIL` cover with the entity identifier | **reusable but must be modernized** (route >500 KB media to `IMAGE`; watch base64 memory) |
| 12 | Discovery by per-item body fetch to filter/search (N+1) | **reusable but must be modernized** — filter on metadata/payload fields; cap and document partiality |
| 13 | Hand-rolled HTML sanitizer | **reusable but must be modernized** (use a vetted sanitizer; keep the allowlist policy) |
| 14 | DM envelope `recipient`/`fullContent` with a hardcoded address | **reusable but must be modernized** to `destinationAddress` + resolved current owner (reuse the verified contact-form skill) |
| 15 | `getQdnResourceUrl` string-sniffing `'Resource does not exist'` | **reusable but must be modernized** (status check + absolute `/arbitrary/…` URL) |
| 16 | Optimistic list update after publish with no read-back | **obsolete / avoid** — verify the served revision |
| 17 | `window.parent` / `window.top` bridge probing | **obsolete / avoid** |
| 18 | `btoa(unescape(encodeURIComponent(json)))` | **obsolete / avoid** (deprecated `unescape`; use `TextEncoder`/`Buffer`) |
| 19 | Hardcoded owner name and owner chat address | **obsolete / avoid** |
| 20 | Per-item `[Edit] [Delete]` inline controls | **not present in the reference — new design work for QWB** |
| 21 | Entity delete / tombstones | **not present in the reference — new design work for QWB** |
| 22 | `names[0]` owner detection, single profile load, duplicated profile helper, `limit/offset` on `GET_ACCOUNT_NAMES` | **obsolete / avoid** |

The reference app's own `PROJECT_ROADMAP.md` "Future Cleanup" section independently lists four of
the weaknesses found here (centralised owner checks, shared rich-text sanitisation, extraction of
common publishing helpers, focused tests) — useful corroboration that these are known debt rather
than intentional design.

## 4. Evidence by layer

| Layer | Action | Result |
| --- | --- | --- |
| Clone | `git clone` of `iffinland/iffi-vaba-mees-QORTAL` into the shared reference area | new clean clone; `main` = `64f55bf7…`; `production` is an ancestor |
| Source read | full read of `utils/`, `services/`, `hooks/`, `components/`, `pages/`, `PROJECT_ROADMAP.md` | patterns above |
| Action inventory | `grep` for `action: '…'` | `PUBLISH_QDN_RESOURCE` ×29, `SEARCH_QDN_RESOURCES` ×19, `FETCH_QDN_RESOURCE` ×11, `SEND_COIN` ×2, `GET_USER_ACCOUNT` ×2, `GET_NAME_DATA` ×2, `GET_ACCOUNT_NAMES` ×2, `SEND_CHAT_MESSAGE`, `GET_WALLET_BALANCE`, `GET_QDN_RESOURCE_URL`, `GET_QDN_RESOURCE_STATUS`, `ADD_LIST_ITEMS` — **no delete action** |
| Runtime | **not executed** | this audit is source-level; no build, install or host run was performed |

## 5. Checks not executed and why

- `npm install` / `npm run build` / `eslint` were **not** run: not needed for the pattern audit, and
  the task forbids unnecessary modification of the reference clone.
- No Qortal host run of the reference app; its runtime maturity is irrelevant to this audit because
  every contract it depends on was re-verified against current Core/Hub source instead.

## 6. Adversarial self-audit

- I initially recorded the DM payload (`recipient` + `fullContent`) as obsolete/broken; checking Hub
  `sendChatMessage` showed it accepts `destinationAddress || recipient` and
  `fullMessageObject || fullContent`, so the app still works. The classification was corrected to
  "reusable but must be modernized".

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-iffi-vaba-mees-owner-pattern-audit.md`
