# QWB Phase 3 implementation — qwb-qortal-web-builders/phase-3-20260915

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): every artefact in this task —
the `src/content/`, `src/qortal/` and `src/owner/` modules, the tests, the headless-browser harness
run, the live-node probes, the measurements and the commit — was produced by the **DeepSeek** model
executing through the local Codex CLI profile. Per `AI-Orchestration/GIT-AND-HANDOFF.md` the
CLI/orchestration profile is not the executor, so the executing agent is recorded as DeepSeek, not
Codex/Codex Local. No third-party curating agent wrote or reviewed this work.
Report type: implementation report (Phase 3 — QDN-backed content persistence for the existing
inline owner UI)
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- branch `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` (single commit)
- base SHA: `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c` (`agent/qwb/phase-2`, the accepted Phase 2
  head); `main` remains `18d760d011e956829714e7489432949829fa1840` and was not touched
Canonical report path / SHA-256 / authorized remote evidence:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-3-implementation.md`
(SHA-256 of the body recorded in the "Report saved" section). Remote evidence:
`git ls-remote origin refs/heads/agent/qwb/phase-3` →
`911b44f3e57c39c46048c950274c89bdd04596f5` (equal to the local commit; `refs/heads/main` and
`refs/heads/agent/qwb/phase-2` unchanged). Companion evidence directory:
`…/implementations/2026-09-15-qwb-phase-3-runtime-evidence/`.

---

## 1. Objective and exit criterion

Connect the accepted Phase 2 inline owner UI to real QDN-backed content CRUD, media publishing and
persistent ordering, without changing the accepted visitor design, and stop there.

Phase 3 is **code-complete**: the read path, the write pipeline, media, tombstones, persistent
ordering, the truthful write-result model and the interlocks are implemented and validated
client-side (283 tests, a headless-browser harness against a scripted node, and read-only probes of
a live node). **No runtime PASS is claimed.** The exit criterion — one staging owner-runtime run in
which the owner is recognised automatically, adds, edits, tombstone-deletes, reorders, changes media,
reloads and sees the *verified persisted* result while a visitor sees only the public content — is
Phase 4 and is spelled out in §14 as a single procedure.

## 2. QDN read/write contract actually implemented

### 2.1 Sources re-checked before coding (not remembered)

| Source | Revision / evidence | What it pinned |
| --- | --- | --- |
| Qortal Core | `108bf191d42d710ec617f535af30cfd82fc03c87` (6.1.9) | service limits, publish/overwrite semantics, approval wording |
| Qortal Hub | `12a573b27246e8a626b24794830c6bc432d1b05d` | `publishQDNResource` request shape, signature in the response |
| Live node `/apps/q-apps.js` | `http://127.0.0.1:24991/apps/q-apps.js`, md5 `3ae7deaa55f353dc0ae4e8d13f3c1034`, re-fetched 2026-09-15T17:22:20Z | camelCase search fields, `handleResponse` JSON-parses *every* response, fetch returns text then parses, request dedup key, per-action timeouts |
| Live nodes | `:24991` and `:24992`, height `2725391`→`2725392`, `syncPercent` 100, `isSynchronizing` false, observed 2026-09-15T17:20–17:22Z | read-only observation; no write was made |
| Audit set | `…/audits/2026-09-15-qwb-qortal-platform-compatibility-and-write-contract.md`, `…-target-architecture-proposal.md`, `…-iffi-vaba-mees-owner-pattern-audit.md`, `…-static-site-forensics.md` | approved kind table (§6.1), write semantics (§6), media rule (§6.3) |
| Reference app | `iffinland/iffi-vaba-mees-QORTAL` @ `64f55bf7` / `origin/production` `7b2145a7` | DOCUMENT-with-JSON publish/read is proven in production |

The re-check found **no contract delta** since the audit pins (same md5, same response handling), so
the requested shapes were implemented as audited. One deviation *from the audit's approved kind
table* was found in the incoming Phase 3 code and corrected — see §3.2.

### 2.2 Read contract

```text
site singleton   FETCH_QDN_RESOURCE   service JSON, name <_qdnName>, identifier qwb_site_v1
other kinds      SEARCH_QDN_RESOURCES service = the kind's service,
                   identifier = <kind prefix>, prefix: true, mode: 'ALL',
                   names: [<_qdnName>], exactMatchNames: true,
                   includeStatus: true, excludeBlocked: true,
                   limit 50, offset page*50, reverse: true   (<= 3 pages)
                 → re-filter every summary: exact name AND exact service AND identifier prefix
                 → FETCH_QDN_RESOURCE per summary in that service, concurrency 4
                 → readStoredEntity() (the same validator the seed uses)
```

- `mode: 'ALL'` is always sent: the node default (`LATEST`) keeps only the newest row per
  `(name, service)`, which would hide every entity after the first of its kind.
- `prefix: true` turns the identifier field from substring into prefix matching; the exact-name
  filter is mandatory, not cosmetic: a live `qwb_` prefix search in `service=JSON` returns other
  publishers' resources (`LE PAV`, `CosmicEnergetics`, `curriedgoat`, … with `qwb_ix_…` identifiers)
  as well as any of our own.
- `includeStatus` + `excludeBlocked` are sent so a blocked or not-yet-downloaded resource is visible
  as such instead of silently missing.
- A payload that is not served is **not** "no content": an unavailable fetch, an invalid payload and
  a kind/prefix mismatch are counted and reported as diagnostics with status `partial`.
- `status: 'ready' | 'partial' | 'error'` is the whole read result; `error` renders the content-error
  state and never owner UI.

### 2.3 Seed fallback (the only fallback, and why it is narrow)

| Case | Result |
| --- | --- |
| `_qdnName` empty, or no bridge in the document | seed bundle, `ready`, diagnostic naming the context |
| nothing published at all: every search answered, no QWB resource found, site singleton reported *unavailable* | seed bundle, `ready`, `nothing-published: …` |
| the site singleton alone is unreadable (transport/malformed/tombstoned) | seed **shell** + the entities that did load, `partial`, `site-singleton-unavailable: …` |
| no search answered *and* the site singleton is unreadable | `error` (content-error state), no owner UI |

The seed is **never** substituted for entities that exist and failed to load, and a single failed
kind never blanks the others.

### 2.4 Write contract

```text
PUBLISH_QDN_RESOURCE {
  service: the kind's service, name: _qdnName (always sent),
  identifier, filename: qwb.json, data64: base64(JSON.stringify(entity)),
  title <= 80 chars, description <= 240 chars
}
```

- `name` is always sent. Omitting it makes the Hub fall back to the user's last-used name and
  publish the site's content under someone else's identity.
- Core indexes the newest transaction per `(name, service, identifier)`; there is no
  compare-and-swap and no create/update distinction, so "the same coordinate with `rev + 1`" is the
  update model and a stale writer can only be *detected* after the fact (`superseded`), never
  prevented.
- No retry of any kind is issued for a write: a declined, timed-out or unreadable publish outcome is
  reported as `rejected`, `ambiguous` or `failed` and left unresolved until the owner acts.

## 3. Resource model and identifiers

### 3.1 Entities

One QDN resource per editable entity, under the app's own name; the entity envelope from the
approved schema (`schema`, `id`, `kind`, `rev`, `state`, `createdAt`, `updatedAt`, `deletedAt`,
`order`, `title`, `payload`). `rev` is the write-verification handle; `state: 'deleted'` is the
tombstone; `order` is sparse (10, 20, 30 …).

| Kind | Service | Identifier | Notes |
| --- | --- | --- | --- |
| `site` | `JSON` | `qwb_site_v1` (fixed) | one exact read, never discovered by prefix |
| `highlight` | `JSON` | `qwb_hl_*` | |
| `service` | `JSON` | `qwb_svc_*` | |
| `step` | `JSON` | `qwb_step_*` | |
| `work` | `JSON` | `qwb_work_*` | |
| `price` | `JSON` | `qwb_price_*` | |
| `article` | `DOCUMENT` | `qwb_post_*` | prose bodies |
| media | `THUMBNAIL` / `IMAGE` | the owning entity's identifier | one image per entity in v1 |

Identifier policy: lowercase `[a-z0-9_-]`, ≤ 60 characters (app policy), kind prefix, minted
**once per opened add form** (`qwb_<kind>_<slug>-<ts36>-<rand>`), reused for every submit of that
form, and never recycled for a different entity. `generateIdentifier()` now takes a `taken`
predicate and re-mints (≤ 5 draws) if the candidate is already in the loaded content, so an add can
never republish another entity's coordinate.

### 3.2 Corrected deviation: articles were published as JSON

The incoming Phase 3 code read and wrote **every** kind in the `JSON` service, while the approved
kind table (audit §6.1) puts `article` in `DOCUMENT`. That is a material divergence: `Service.JSON`
is capped at 25 KB by the node, so the shipped implementation silently imposed a 25 KB ceiling on
article payloads and contradicted the documented resource model.

Phase 3 now implements the approved map (`schema.ts`: `serviceForKind` / `serviceForIdentifier`).
Both sides derive the service from the **kind**, and the kind from the **identifier prefix**, so a
read-back can never look in a different service than the write used. Because `Service.DOCUMENT` has
no node-side limit, the app bounds article payloads itself at `DOCUMENT_MAX_BYTES = 200 KB` — the
payload is fetched by every visitor read of that kind, so an unbounded article would be a permanent
page-load cost and an unbounded publish fee. The refusal is explicit and truthful. Evidence that the
documented shape works end-to-end: the pinned shim's `handleResponse` `JSON.parse`s *every* response
body (so a DOCUMENT payload arrives parsed, exactly like a JSON one), and the reference app
publishes its records as JSON-in-DOCUMENT. Browser-level evidence is in §10.

## 4. Update / delete / reorder semantics

| Action | Writes | Verification |
| --- | --- | --- |
| **Add** | 1 resource: the entity at the minted identifier, `rev` 1 | read-back `rev` |
| **Edit** | 1 resource: the same identifier, `rev + 1`, `updatedAt` refreshed | read-back `rev` |
| **Delete** | 1 resource: tombstone at the same identifier, `state: 'deleted'`, `deletedAt`, `rev + 1` | read-back `rev` (the tombstone's) |
| **Reorder** | 1 resource: the moved entity with a midpoint `order`; the gap-renumber fallback writes only the entities whose `order` actually changes | read-back `rev` per write |
| **Media** | 1 resource before the entity when an image is chosen/changed | byte identity, then the entity |

- **Delete is logical.** Qortal has no app-accessible QDN delete, so a delete is a republish of the
  same `(name, service, identifier)` with `state: 'deleted'`; the previous bytes stay retrievable.
  Every read path filters tombstones (`activeEntities`), a tombstones count is reported as a
  diagnostic, and because tombstones are filtered *before* the bundle reaches the owner layer a
  deleted entity cannot be re-opened or resurrected by an edit — the only way back is a new add with
  a new identifier. Node-admin delete APIs are not used anywhere.
- **Reorder is persistent and sparse.** `planReorder()` re-derives the order from the loaded bundle
  (never from the DOM), refuses edge moves with a reason, and otherwise computes one value strictly
  between the new neighbours; `MIN_ORDER_GAP` triggers a `ORDER_GAP` renumber that reports how many
  entities it republished. `order` is `<kind>:<value>`-scoped by being per entity list, so a reorder
  never touches another kind.
- **Order is written for the moved entity only**, so a reorder costs one publish fee in the common
  case.

## 5. Media pipeline

```text
choose file → jsdom-safe injected encoder (browser: decode → downscale to 1200 px long edge →
  WebP (JPEG fallback) at q 0.82) → THUMBNAIL if <= 500 KB else IMAGE if <= 10 MB else refuse
→ PUBLISH_QDN_RESOURCE (same identifier as the entity, filename from the encoded type)
→ verify: base64 byte identity when <= 1 400 000 decoded bytes, else GET_QDN_RESOURCE_STATUS == READY
→ the returned ImageRef is handed to the entity only if the image is *verified*
→ the entity is published (data64 JSON) referencing /arbitrary/<service>/<name>/<id>/<file>
```

- Media publishes **before** the entity that references it (audit §6.3); if the image cannot be
  verified the entity is not published at all, and the form keeps the chosen image as part of the
  draft.
- Only WebP/JPEG/PNG are accepted; PNG input is re-encoded to WebP and the served filename follows
  the *encoded* type because the node derives the content type from it.
- Verification compares the served bytes with the submitted bytes for payloads inside the compare
  bound (the constant is a decoded-byte bound, not a base64-character bound), and normalizes
  whitespace, padding and the URL-safe alphabet before comparing, so a transport formatting
  difference is not mistaken for different content. Above the bound the node's own status is used
  and the wording says that byte identity was **not** compared.
- The image is addressed at render time through an **absolute** `/arbitrary/…` path (never relative,
  which would resolve against the frame's `<base href>` and return the shell), and the ref is stored
  explicitly in the entity.

## 6. Truthful write-result model

Two independent facts are recorded, and they are never folded into one sentence:

| Stage-1 state (`WriteState`) | Label |
| --- | --- |
| `submitted` | "Submitted to the host" |
| `rejected` | "Rejected by the host — nothing was published" |
| `ambiguous` | "Outcome unknown — the request may or may not have been signed" |
| `failed` | "Failed — nothing was published" |

| Stage-2 availability | Meaning |
| --- | --- |
| `verified` | the read-back returned exactly the submitted `rev` |
| `superseded` | the node serves a *higher* `rev` — another write won; not retryable |
| `not-yet-served` | the read-back did not show the submitted revision within the budget |
| `unverified` | no read-back happened (rejected/failed/ambiguous) |

- Only `verified` may be described as published; the sentence the owner sees is composed from the
  read-back's own detail plus the signature prefix, and every other case says what is *not* proven.
- `submitted` can only be reached with a signature in the response. A resolved response *without* a
  signature is `ambiguous`, not success — the app cannot tell whether the host signed.
- A resolved `{error: …}` object (how the shim reports HTTP failures) is a failure, and the node's
  own `message` is preserved so the owner sees "Couldn't find PUT transaction for name …" rather
  than a bare code; that wording is also what lets the read path tell "not served" apart from
  "broken read".
- The four states are rendered verbatim by the owner bar, the form status line, the delete dialog
  and the "Publishing status" dialog; `submitted | ambiguous` disable the submit button
  ("Not retryable — check status") so a second non-idempotent submission cannot be made by reflex,
  while `rejected | failed` (nothing was published) allow an explicit retry.
- Ambiguity is left unresolved until the owner presses **Check status**, which re-reads the resource
  and either promotes it to `verified` (then re-reads and re-renders the content) or reports the
  detail. Nothing is retried automatically anywhere in the write path.

## 7. Interlocks, drafts and failure handling

- **One in-flight write per identifier** (`owner/writes.ts`): a second submit for the same
  identifier is refused with an explanation; the lock covers media too, because media shares the
  entity's identifier. The owner gate (`session.assertOwner()`, an `await`) is followed by a
  *second* lock check, so two rapid clicks share one gate promise and the faster continuation
  reserves the identifier — one publish per click, verified by tests for the form and the tombstone
  dialog.
- **Drafts survive every non-verified result**: rejected, failed, ambiguous and not-yet-served all
  leave the form open with its values and its chosen image; a verified write is the only case that
  closes it. An unverified *image* submission sets `submittedData64` and reveals `Check status`,
  which re-reads the image first and only then publishes the item.
- **Owner mode is re-verified immediately before every write**, and the form is disabled with an
  explanation if owner mode ends mid-session. Authority is the Phase 2 model (unchanged):
  `_qdnName` + `GET_USER_ACCOUNT` + `GET_ACCOUNT_NAMES` → case-folded membership → owner | visitor;
  nothing is persisted, nothing is hardcoded, `names[0]` is never read.
- **Publishing identity is the served WEBSITE resource's `_qdnName`**, captured at boot; the app
  never republishes the WEBSITE resource itself.
- **Content after a verified write is always re-read from the node** and re-rendered, so the page
  shows served truth rather than the draft. The owner bar also offers "Reload content" (re-read +
  re-render) and "Check last write" (re-check the newest unresolved write).
- **Source-level guards** (`tests/support/claims.ts`): no bridge action name and no direct
  `qortalRequest` call outside `src/qortal/`, and no `localStorage`/`sessionStorage`/`indexedDB`
  anywhere.

## 8. Validation by layer

All commands run in `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders` on the
committed tree (`911b44f`), 2026-09-15 17:04–17:23Z:

| Layer | Command | Result |
| --- | --- | --- |
| Types | `npx tsc --noEmit` | clean (exit 0) |
| Lint | `npx eslint .` | clean (exit 0) |
| Format | `npx prettier --check .` | clean |
| Tests | `npx vitest run` | **24 files / 283 tests passed** |
| Build | `npm run build` | success — `dist/assets/index-CLC6fuj3.js` 126.57 kB (gzip 37.56 kB), `dist/assets/style-BgNavAWw.css` 215.35 kB |
| Whitespace | `git diff --check` | clean |
| Live node (read-only) | `/admin/status`, `/apps/q-apps.js`, `/arbitrary/resources/search` | both nodes height 2725391→2725392, sync 100 %, not synchronizing; shim md5 unchanged (HTTP 200, `3ae7deaa…`, verified 17:22:20Z); `qwb_` prefix search returns foreign publishers (see §2.2) |

Test coverage added for this phase (the 109 new tests over the 174 Phase 2 tests):
`tests/qdn-source.test.ts` (discovery fields, exact filtering, tombstones, the three seed fallbacks,
per-kind service consistency, DOCUMENT round-trip), `tests/qdn-publish.test.ts` (request shape,
payload limits, publish classification, read-back verification, media verification bounds,
tombstones), `tests/qortal-read.test.ts` (search paging, dedup, normalization, error
classification), `tests/qortal-base64.test.ts`, `tests/ordering.test.ts`,
`tests/owner-writes.test.ts`, `tests/owner-media.test.ts`, and a rewritten
`tests/owner-flows.test.ts` (25 real write-path tests: add/edit/delete/reorder/media/ambiguous/
rejected/in-flight/draft-preservation/service-selection).

## 9. Adversarial self-audit

Findings raised and their disposition (all in-scope BLOCKER/HIGH findings are fixed; the two
non-verified deviations are recorded as accepted limitations):

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | **HIGH** | `Check status` was inert when a *media* submission was the unverified write: the form recorded its "last attempt" only after the media step, so the image re-check branch could never run, and the flow told the owner to use a button that did nothing — leaving an ambiguous image with no recovery path in the UI | Fixed: the attempt (id, rev, label, title) is recorded as soon as the draft validates, i.e. **before** media publishing; the media re-check recomputes the service with `planMediaService`, and `tests/owner-flows.test.ts` drives the whole sequence (image unverified → still unverified → verified → item published) |
| 2 | **HIGH** | §3.2 — articles were published as `JSON`, contradicting the approved kind table and imposing a 25 KB ceiling silently | Fixed: per-kind service map + `serviceForIdentifier`; DOCUMENT round-trip covered by unit and browser tests |
| 3 | MEDIUM | An image submission that was `submitted`/`ambiguous` left the submit button enabled as "Save & publish", inviting a second non-idempotent publish of an ambiguous write | Fixed: one `applySubmitPolicy` decides the button for item *and* media writes; a rejected/failed image re-enables the retry, an ambiguous one does not |
| 4 | MEDIUM | The "Publishing status" dialog's footer **Close** button had no handler (only ×/Escape/backdrop closed it) — a visible control that did nothing | Fixed in `src/ui/modal.ts`: `[data-qwb-modal-cancel]` is now the module's own contract and closes through the dirty guard; the duplicate wiring in the delete flow was removed; two modal tests pin it |
| 5 | MEDIUM | The node's live 404 body (`{"error":1401,"message":"Couldn't find PUT transaction for name …"}`) was not recognised by the read classifier, so an empty publisher could be reported as a broken read (and vice versa) | Fixed: `rejectionMessage` prefers the node's `message`, the unavailable pattern covers `couldn't find`/`not published`/`1401`/`404`, and the contract fake now answers the *live* body |
| 6 | MEDIUM | `MEDIA_BYTE_COMPARE_LIMIT` was compared against the base64 string length (1.33× the bytes), so the documented byte bound was not what the code enforced | Fixed: `base64ByteLength()` + `normalizeBase64()`; a payload under the byte bound is byte-compared even though its base64 is over it, and formatting differences can no longer look like different bytes |
| 7 | LOW | The `ambiguous` label claimed a timeout for the "host answered without a signature" case too | Fixed: "Outcome unknown — the request may or may not have been signed"; the label is asserted not to claim the timeout shape |
| 8 | LOW | A multi-run bullet in the article body editor joined a bullet's inline runs with a space, silently rewriting the entity on save (a second link absorbed the rest of the bullet) | Fixed with a `+ ` continuation marker and an untrimmed-line reader; every shipped article round-trips losslessly |
| 9 | LOW | Two add forms opened in the same millisecond with the same title could mint the same identifier, which would overwrite an existing entity | Fixed: `generateIdentifier(..., { taken })` re-mints (≤ 5 draws) against the loaded content |
| 10 | LOW | The "Publishing status" dialog wrote `Submitted to the host … not yet verified (verified)` — a self-contradiction produced by folding availability into the state label | Fixed: state and availability are separate facts everywhere; a test asserts the settled line cannot read that way |
| 11 | — | Re-verified by inspection/tests: tombstone filtered on every read path and not resurrectable by edit; every read path re-filters exact name + service + prefix; media verified before the entity; no automatic retry and no storage APIs (`tests/support/claims.ts`); visitor DOM untouched (§10) | No change needed |
| 12 | — | **Accepted limitation:** verification compares `rev`, not payload identity. If another writer publishes the *same* identifier at the *same* `rev` inside the verification window (two owner devices), a read-back can match while the served bytes are the other writer's. Core offers no compare-and-swap, and the approved model does not require more; the app re-reads and re-renders served truth after every verified write, and identifiers are app-minted with one in-flight write per identifier. Recorded as a runtime risk (§13) rather than redesigned. |
| 13 | — | **Accepted limitation:** a gap-renumber reorder that fails part-way leaves a mixed order (some entities republished). Impossible to make atomic without a derived index (explicitly out of v1 scope); the flow stops, re-reads and reports which item was not verified, and this is exercised by the renumber tests. |
| 14 | — | A test-only fixture writer (`tests/tmp-fixture.test.ts`, which wrote the browser harness's seed file) was removed from the tree before the commit; the fixture is now regenerated by `dump-seed-fixture.mjs` in the evidence directory. `git status` is clean. |

## 10. Browser harness evidence

Headless Chrome, the production `dist/` bundle, a scripted node injected as `window.qortalRequest`
plus `_qdnName` (owner page) and no bridge at all (visitor page). Full data, script and screenshots:
`…/implementations/2026-09-15-qwb-phase-3-runtime-evidence/`.

Owner page (recognised automatically, `errors: []`):

- bar meta `WEBSITE · verified by name ownership`; 17 inline controls; bar buttons
  `Hide owner tools / Publishing status / Reload content / Check last write / Re-check owner mode`;
- read: `FETCH_QDN_RESOURCE qwb_site_v1`, then one search per kind with `prefix: true`,
  `mode: 'ALL'`, `exactMatchNames: true` and the kind's service (`JSON` ×5, `DOCUMENT` for
  `qwb_post_`), then per-entity fetches in that service;
- **highlight edit** (`JSON`): one publish carrying `name: "Qortal Web Builders"`, a read-back, the
  form closed, toast `"Harness published headline" was published and verified as revision 2`, the
  home page re-rendered with the new headline, and the status dialog showing
  `Submitted to the host (availability: verified)`;
- **article edit** (`DOCUMENT`): one publish with `service: DOCUMENT`, a `FETCH_QDN_RESOURCE`
  read-back in `DOCUMENT`, the form closed on verification, and the posts index re-rendered with
  the new title `Harness article headline`.

Visitor page (same bundle, no bridge): `ownerBar: false`, `ownerControls: 0`, `ownerClasses: 0`,
`modalHost: false`, `toastHost: false`, `appHtmlLength: 23603`, `appHtmlHash: -264186793` —
byte-identical to the accepted Phase 2 baseline — and `visitor-home-1440.png` has the same SHA-256
(`28bc7fb7800c2ecec0ab11ebf40cd026d0fa81fc5fea42078112dcd10e734b62`) as the Phase 2 evidence
screenshot. The public rendering is unchanged.

## 11. Files changed

46 files, `+6175 / −499` (single commit `911b44f`).

New modules — `src/content/qdn-source.ts` (QDN-backed source: discovery, hydration, tombstones,
seed fallbacks), `src/content/ordering.ts` (sparse-order planning), `src/qortal/read.ts` (search /
fetch / status / base64 / bounded concurrency), `src/qortal/publish.ts` (request building, publish,
read-back verification, media, limits), `src/qortal/base64.ts` (UTF-8 base64 + comparison
normalization), `src/owner/writes.ts` (in-flight lock + truthful write log), `src/owner/media.ts`
(accept/downscale/encode), and the test-side contract fake `tests/support/qdn.ts`.

Modified — `src/main.ts` (QDN source wiring), `src/content/schema.ts` (service-per-kind map,
`serviceForIdentifier`), `src/content/identifier.ts` (collision-aware mint), `src/content/
repository.ts`, `src/owner/flows.ts` (the write pipeline: add/edit/delete/reorder/media/retry
policy), `src/owner/bar.ts`, `src/owner/shell.ts`, `src/owner/drafts.ts`, `src/owner/fields.ts`
(article round-trip fix), `src/owner/forms.ts`, `src/owner/phase.ts` (`OWNER_PHASE = 3`,
`QDN_WRITE_ENABLED = true` + the notices the UI renders), `src/owner/targets.ts`, `src/owner/
controls.ts`, `src/qortal/bridge.ts` (node error wording), `src/qortal/write.ts` (labels), `src/ui/
modal.ts` (footer cancel contract), `src/styles/owner.css` (media/status affordances), `README.md`
and `docs/architecture.md` (Phase 3 read/write contract, resource model, media, write-result model,
status table).

Tests — rewritten `tests/owner-flows.test.ts` (25 write-path tests) and updated `owner-bar`,
`owner-controls`, `owner-forms`, `owner-session`, `schema`, `qortal-bridge`, `qortal-write`,
`modal`, `identifier` tests plus `tests/support/{owner,claims}.ts`; new `qdn-source`, `qdn-publish`,
`qortal-read`, `qortal-base64`, `ordering`, `owner-writes`, `owner-media` test files.

## 12. Checks not executed, and why

| Not executed | Reason |
| --- | --- |
| Any QDN **write** against a live node | The task forbids publishing the WEBSITE resource and authorizes only a Phase 4 staging owner run; every write here was made against the scripted contract fake |
| Owner-runtime acceptance in a real host | The Phase 4 exit criterion; no runtime PASS is claimed |
| Serving the built bundle from a Qortal host (gateway/domain-map) | Requires publishing; the visitor-side gateway behaviour is unchanged from Phase 2 and was not re-tested |
| Real image encoding (`createImageBitmap` + canvas) | jsdom has no image decoder; the encoder is injected and the pipeline is tested with a fake encoder, while the pure planning pieces (target size, filename, service choice, limits) are unit-tested. The real encoder remains a runtime risk (§13) |
| A real multi-megabyte media verification above the byte-compare bound | Needs a published resource; the status-based branch is unit-tested instead |
| Cross-node/replication behaviour | Out of scope for Phase 3 and not observable without publishing |

## 13. Remaining risks and follow-up

| Risk | Note |
| --- | --- |
| **Read-back proves only the local node** | `verified` means "the node this app talks to serves revision N", not "the network does". Replication lag elsewhere is invisible to the app; wording already says "this node" |
| Verify budget may be short on a slow node | 4 attempts × 5 s. A node that needs longer reports `not-yet-served` (truthful, recoverable via Check status) but the owner may have to press it. Consider making the budget adaptive after the staging run |
| `rev` equality is not payload identity | Two writers publishing the same coordinate at the same `rev` are indistinguishable (no compare-and-swap in Core). One in-flight write per identifier and a re-read/re-render after every verified write mitigate it; a pre-write freshness read is the follow-up if the staging run shows multi-device use |
| Reorder renumber is not atomic | A failure part-way leaves a mixed order; reported, not hidden (§9 finding 13) |
| Media above the byte-compare bound is verified by node status only | Byte identity is not proven for images > 1 400 000 bytes; the wording says so |
| `SEARCH_QDN_RESOURCES` with `mode: 'ALL'` + `includeStatus` costs more than `LATEST` | 6 searches per page load (≤ 3 pages each) plus up to 4 concurrent fetches per kind. Acceptable at the approved volume; a derived index would be the answer if the volume grows (explicitly out of v1 scope) |
| No account-changed host event | An account switch is only noticed on visibility change, route change, an explicit re-check, or the pre-write `assertOwner()` — inherent to the platform (verified: no such event in `q-apps.js`) |
| DOCUMENT path has no browser-runtime history in this repo | Proven by the reference app and by the simulated shim, but the first real article publish is the staging run; if DOCUMENT were wrong, the failure mode is a truthful "not verified" plus a missing article, not silent corruption |
| The app never republishes the WEBSITE archive | Publishing the site itself remains a separate, explicitly authorized owner action |
| Two dialogs can be open at once (Phase 2 note) | Field ids repeat across stacked dialogs; harmless for behaviour, cosmetic for assistive tech |
| Reorder/media during a reload | `Reload content` replaces the bundle while a form may be open; the form keeps its own draft and its own identifier, so a subsequent publish still targets a valid coordinate |

## 14. Exact single staging validation procedure for Phase 4

One run, in a real host, by the owner account. Nothing else may be published to the WEBSITE resource
during the run.

**Preconditions** (record each as evidence)

1. A staging build of `911b44f` (`npm run build`) published/served as a QDN `WEBSITE` resource whose
   `_qdnName` is the intended publishing name, and a Qortal node that is fully synced; record the
   node URL, height and the app resource revision.
2. Record the pre-run state: no `qwb_*` resource exists under that name (or record what exists), so
   the first add is unambiguous.
3. Open DevTools console (or capture console output). The run passes only if no unhandled error and
   no unexpected `PUBLISH_QDN_RESOURCE` appears.

**Procedure (in order, recording the result of every step)**

| Step | Action | Evidence to capture |
| --- | --- | --- |
| 1 | Load the app while logged in as the owner | owner bar appears within one boot; bar meta shows the expected publishing name and `verified by name ownership`; console shows no diagnostic |
| 2 | Load the same URL in a second browser/profile with no owner account (or logged out) | no owner bar, no inline controls, public content identical to the published site |
| 3 | `+ Add` in a section, fill it, `Save & publish`, approve the host dialog | toast names the minted identifier and revision 1; status dialog shows `Submitted to the host (availability: verified)`; the item appears after reload; record the identifier and the resource's `rev` from the node API |
| 4 | `✎` on that item, change a field, save | revision increments to 2 in the toast and in the node's stored payload; new value survives a hard reload |
| 5 | Reload the page (fresh boot) | the change is still shown, still `rev` 2; no seed fallback diagnostic |
| 6 | Change the item's image, save | TWO publishes in order (`THUMBNAIL`/`IMAGE` first, then the entity), the image renders from `/arbitrary/…` after reload; if the image fails, the entity must NOT be published and the draft must stay open |
| 7 | `↑`/`↓` the item within its group | exactly one publish (or a reported renumber), order survives a hard reload and matches the on-screen order |
| 8 | `🗑` the item, confirm, approve | tombstone published; the item disappears after reload; the item is gone from every read (no card, no control); `state: "deleted"` visible in the node's stored payload; no attempt to delete via node-admin |
| 9 | Owner bar → `Publishing status` | every step above is listed with its state *and* availability; `Pending writes: 0` |
| 10 | Owner bar → `Reload content` | the page shows the published state, status `ready` (or a named `partial` diagnostic) |
| 11 | Repeat step 2 with the second profile | the new/edited items are visible there too, no owner UI |
| 12 | **Negative test (strongly recommended):** decline the host approval dialog on an edit / let the timeout expire | result is `Rejected by the host` or `Outcome unknown`, nothing is claimed as published, the draft stays open, and the write is not retried automatically |
| 13 | **Negative test:** switch accounts (or lock the owner account) while a form is open, then try to save | the save is refused with the owner-mode explanation, the draft is preserved, and `Re-check owner mode` removes both the bar and the inline controls |

**Pass conditions** — steps 1–11 all produce verified, persisted, reload-surviving results; step 12
produces a truthful rejected/ambiguous outcome with no automatic retry and no false success; step 13
refuses the write and removes owner UI; the visitor profile never sees owner UI; no QDN resource was
written by a non-owner; and the app never republishes the WEBSITE resource.

**Recorded after the run:** node URL/height, the identifiers and revisions of every resource touched,
console output, screenshots of owner and visitor states, and the pre/post `SEARCH_QDN_RESOURCES`
results for the `qwb_*` prefixes under that name.

## 15. External actions

- **Committed and pushed** (authorized by the task: "commit/push agent branch"): branch
  `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5`, one commit on top of
  `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`; `git ls-remote origin` verified the pushed SHA and
  showed `refs/heads/main` and `refs/heads/agent/qwb/phase-2` unchanged. No force push, no history
  rewrite, no merge into `main`.
- **No** QDN write, transaction, signature, tag, release, deployment, repository-settings change or
  issue mutation. The WEBSITE resource was not published or touched.
- Live-node access was **read-only** (`/admin/status`, `/apps/q-apps.js`, `/arbitrary/resources/
  search`).
- Platform report and evidence bundle written under
  `…/qortal-dev-workspace/docs/qwb-qortal-web-builders/` (that working tree is untracked for this
  path; nothing there was committed). Handoff synchronization for `AI-Orchestration` was **not**
  authorized: `handoff_sync = pending_authorization`.

## 16. Capability harvest

Candidates identified, **deliberately not promoted** — owner-runtime evidence is still missing and
the owner ruled out promoting skills before owner-runtime evidence:

| Candidate | What it would capture | Why not promoted now |
| --- | --- | --- |
| `qortal/qdn-content-crud` | The whole verified contract: camelCase search fields, `mode: 'ALL'`, exact-name re-filtering, `(name, service, identifier)` update with `rev`, tombstone delete, media-before-entity, read-back verification, non-retry of ambiguous writes, upload limits per service | Verified against Core/Hub/`q-apps.js` and a live node, and exercised against a scripted node, but **no live publish has been made** from this repository |
| `qortal/registered-name-owner-mode` (Phase 2 candidate) | `_qdnName` + `GET_USER_ACCOUNT` + `GET_ACCOUNT_NAMES` → case-folded, fail-closed owner derivation and its re-verification triggers | Still awaiting the same owner-runtime run (unchanged from Phase 2) |
| `qortal/inline-owner-editing` (Phase 2 candidate) | Owner bar + contextual inline controls over a preserved public DOM, fail-closed DOM↔content matching, truthful write wording, per-entity in-flight protection, draft preservation | Same reason |
| `shared/headless-browser-evidence-harness` (orchestration) | The pattern used here and in Phases 1–2: build the real bundle, inject a scripted platform bridge, drive the real UI, capture DOM hash + screenshots, and compare against the accepted baseline | Illustrative but only two consumers so far, and its value depends on the platform fakes being contract-accurate; re-harvest after Phase 4 |

No skill file was created or updated; no orchestration knowledge was changed. Re-harvest after the
Phase 4 owner-runtime run, which is the evidence that would set a real maturity and freshness for the
first three candidates.

---

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-3-implementation.md`
- SHA-256 of the report **body** (468 lines, measured immediately before this block was appended):
  `1904c573bc00e9ade0c6420602cbb83da5c9020dac714574219c5ce88ac387b0`
  This block is the only part of the file written after that measurement, so the digest remains the
  identity check for everything above it.
- Companion evidence directory (9 files + `SHA256SUMS.txt`):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-3-runtime-evidence/`
- Application commit this report describes:
  `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` (base
  `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`); remote-verified with `git ls-remote origin`.
- Handoff synchronization: `handoff_sync = pending_authorization` — no commit or push was made in
  `AI-Orchestration/` or in the `qortal-dev-workspace` working tree.
- Transient local harness workspace used to produce the evidence (not durable): `/tmp/qwb-p3-check/`
  (built `dist/` + generated pages), `/tmp/qwb-p3-shots/` (raw dumps), `/tmp/qwb-p3-harness.py`,
  `/tmp/qwb-p3-run.sh`, `/tmp/qwb-p3-seed.json`.
