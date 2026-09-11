# Shadow Archives Phase 2A — read-only QDN content pipeline and real content rendering (implementation report)

- Project: `shadow-archives-webportal-QORTAL`
- Phase / task: Phase 2A — read-only QDN content pipeline and real content
  rendering
- Date: 2026-09-11
- Author: Codex (implementation agent)
- Task class: product/feature + platform-integration read work; **no write path**
- Related:
  [`../architecture/2026-09-11-qdn-data-contracts.md`](../architecture/2026-09-11-qdn-data-contracts.md),
  [`../architecture/2026-09-11-phase-1b-implementation-plan.md`](../architecture/2026-09-11-phase-1b-implementation-plan.md),
  [`2026-09-11-phase-1b-appshell-implementation-report.md`](2026-09-11-phase-1b-appshell-implementation-report.md),
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md)

## 1. Status

**PASS WITH OWNER VALIDATION REQUIRED.**

The Phase 2A exit criterion is met at the source, automated and local-browser
layers: a centralized verified read-only QDN layer exists, validated Blog /
Video / Gallery read models are implemented, the partitioned catalog is consumed
with a bounded fallback, listings do not fetch bodies or media bytes, detail
routes fetch the authoritative entity resource, malformed/untrusted content
fails safely, stored rich content cannot execute unsafe markup or URLs, archive
states distinguish empty from unavailable/partial/stale, and **no write, auth or
publishing behaviour was added**.

A real Qortal host / Hub Developer Mode check remains **NOT VERIFIED** (no local
node or host session was available). Everything that depends on the live host
(`_qdnBase` routing, injected `_qdnName`, live `SEARCH_QDN_RESOURCES`, QDN media
`<img>` serving, clipboard inside the Q-App iframe) is **OWNER VALIDATION
REQUIRED**.

## 2. Baselines and preserved changes

- Canonical workspace `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`:
  branch `main`, HEAD `830e84b` (matches the expected baseline), clean before
  and after (one intentional doc edit — see §15).
- Application `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`:
  branch `main`, HEAD `19ce35b` (matches the expected baseline); `origin/main`
  is also `19ce35b`. The worktree was clean before editing.
- No existing uncommitted user work was present and none was overwritten,
  reverted or reset.

## 3. Objective and exit criterion

The task required the first production-shaped **read-only** QDN pipeline:
discover content through verified read contracts, validate untrusted payloads at
runtime, model Blog/Video/Gallery, render listings without full-body fetches,
fetch authoritative resources only on detail routes, render stored content
safely, keep honest loading/empty/partial/unavailable/error states, and avoid
N+1 discovery. All bounds are met (evidence in §4–§13 and §16–§17).

Phase 2A non-goals were respected: no publishing, editing, owner studio, TipTap
editor, likes/unlikes, comments, tips, shares, moderation publishing, Q-Mail,
Q-Tube/Subwire/Quitter publishing research, catalog publication, startup auth
prompt, or any Qortal transaction.

## 4. Verified read contracts (source-verified, not from memory)

Verified 2026-09-11 against pinned local reference sources re-confirmed as
upstream `HEAD` via `git ls-remote`:

- `qortal` Core `108bf191d42d710ec617f535af30cfd82fc03c87` (v6.1.9) —
  `src/main/resources/q-apps/q-apps.js`, `ArbitraryResource.java`,
  `ArbitraryResourceData.java`, `HSQLDBArbitraryRepository.java`.
- `Qortal-Hub` `12a573b27246e8a626b24794830c6bc432d1b05d`.
- `qapp-core` `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` (read-only reference;
  not imported).

Bridge payload fields (camelCase) mapped 1:1 in `src/qortal/qdn.ts`:

| Typed field | Bridge field | Notes |
| --- | --- | --- |
| `service` | `service` | e.g. `DOCUMENT`, `IMAGE`, `VIDEO`, `THUMBNAIL` |
| `identifier` | `identifier` | empty is treated as null node-side |
| `defaultResource` | **`default`** | only resources without identifiers |
| `exactMatchNames` | `exactMatchNames` | bridge→REST `exactmatchnames` |
| `nameListFilter` | `nameListFilter` | bridge→REST `namefilter` |
| `includeStatus` / `includeMetadata` | same names | bridge→REST lowercase |
| `mode` | `mode` | `SearchMode` |
| `prefix` | `prefix` | prefix-match on name/identifier/title/description |
| others | `query,name,names,keywords,title,description,minLevel,followedOnly,excludeBlocked,before,after,limit,offset,reverse` | |

Confirmed behaviours that the implementation depends on:

- **`mode` defaults to `LATEST`** (`HSQLDBArbitraryRepository.searchArbitraryResources`
  sets `mode = SearchMode.LATEST` when null), which returns only the newest
  resource per `(name, service)`. Fallback discovery therefore sends
  `mode: 'ALL'`; without it, all but one entity per kind would be silently
  hidden. Covered by `src/services/fallbackDiscovery.test.ts`.
- **Prefix discovery**: `prefix` matches the beginning of the identifier field,
  so `identifier: 'saw_post_'` + `prefix: true` enumerates the namespace.
- **Default identifier**: node search maps the stored identifier `"default"`
  back to `null`; `identifier: null` means "the resource's default resource".
  Media references in the Shadow Archives contract always carry an explicit
  identifier, so default media is rejected by the validators.
- `FETCH_QDN_RESOURCE` (`params: service, name, identifier?, filepath?,
  encoding?`) returns the resource text; Shadow Archives `DOCUMENT` envelopes
  are UTF-8 JSON.
- `GET_QDN_RESOURCE_STATUS` returns an `ArbitraryResourceStatus` object
  (`{ status, ... }`); `GET_QDN_RESOURCE_URL` runs a status check then returns a
  URL. The read pipeline uses neither at runtime today; it builds the verified
  same-origin media path instead (see below). Both wrappers exist and are unit
  tested as verified read primitives.
- Non-link resource URL, from `buildResourceUrl(service,name,identifier,path,false)`:
  `/arbitrary/<service>/<name>[/<identifier>][?filepath=<path>]`. `buildQdnResourcePath`
  mirrors this exactly and is used for `<img>` sources.
- `q-apps.js` installs a document-level click interceptor that
  `preventDefault()`s `http://`, `https://` and `//` links and routes
  `qortal://` links through `LINK_TO_QDN_RESOURCE`; `convertToResourceUrl`
  returns null for non-`qortal://` URLs, so same-origin `/arbitrary/...` image
  sources pass through unmodified.

Live read-only checks against `https://api.qortal.org` were used only for
read-only research (no writes). The app never calls a public node from browser
code.

## 5. Domain model and runtime validation

New `src/domain/` layer (types + explicit hand-written validators; no schema
dependency added):

- `BlogPost`, `VideoEntry`, `GalleryItem`, `GalleryAlbum`;
- `CatalogManifest`, `CatalogPartition`, `CatalogEntry`/`CatalogListing`,
  `CatalogPartitionDescriptor`;
- `TaxonomyReference`, `QdnResourceIdentity`, `QdnMediaReference`,
  `RichTextDocument`/`RichTextNode`/`RichTextMark`.

Every untrusted QDN payload passes a validator before entering the trusted
layer. Validators check object shape, `schemaVersion === 1`, entity kind, stable
id (`^[0-9a-z]{12}$`), timestamps, required/optional strings, bounded arrays,
taxonomy shape, QDN references (service/name/identifier, no whitespace/slashes),
rich-text structure and budgets, and catalog entry identity/type coupling. A
malformed catalog entry is isolated and counted; a malformed entity payload
yields a state panel instead of a crash. `schemaVersion` is preserved on every
validated value.

Self-imposed caps live in `src/domain/constants.ts` (entity/catalog byte caps,
title/slug/excerpt/bodyText lengths, taxonomy-array max, partitions ≤64,
entries/partition ≤512, rich-text depth/nodes/text budgets).

## 6. Read-layer architecture (centralization)

- `src/qortal/` — verified bridge mechanics only: `bridge.ts` is the single
  place that touches `window.qortalRequest`; `qdn.ts` is the typed, mapped read
  surface; `actions.ts` classifies public-read vs permissioned vs write actions.
- `src/services/` — Shadow Archives content semantics: publisher scope,
  identity post-filtering, search-hit normalization, JSON parsing/caps, catalog
  and entity repositories, fallback discovery, bounded queue, cache, and the
  domain error taxonomy.

React components import `src/services` / `src/features/content` and never issue
`qortalRequest` (an audit grep over `src/features`, `src/components`, `src/app`
finds raw `qortalRequest` only in test fakes). UI does not scatter
`SEARCH_QDN_RESOURCES`; it is referenced only in `actions.ts`/`qdn.ts`.

## 7. Content scope / publisher authority

`resolvePublisherScope` derives the canonical publisher **only** from the
injected `_qdnName` (decoded). There is no hardcoded address, and payload
`author`/`owner`/`publisher` fields are never used as authority (the entity
`publisher` field is an informational display hint only). Outside a Qortal host
the scope is explicitly unresolved, so the archive reports `unavailable` rather
than pretending production identity exists.

## 8. Catalog consumer and fallback discovery

Catalog read pipeline: `manifest → partition descriptors → bounded concurrent
partition fetches (limit 3) → validated entries → dedupe by newest`. The
manifest is validated; a missing/invalid partition is isolated (the rest still
loads, result becomes `partial`); if every declared partition fails, the catalog
is `invalid` and the caller falls back. Duplicate entries keep the newest
`updatedAt`. The catalog is treated as derived and stale-tolerant; it never
overrides the authoritative entity resource.

Fallback (`mode: 'ALL'`, `exactMatchNames`, `prefix: true` on the `saw_*`
namespace, `includeMetadata: true`, bounded `limit`/`offset`, `maxPages` bound,
never `limit: 0`) is used only when the catalog is missing/unusable. It is
**always** reported as `partial` and, for a zero-result search, states that the
result is "not proof that the archive is empty". Per-kind failures are isolated.

## 9. Listing model, detail fetch and routes

- Listings consume validated `CatalogListing` records (identity, id, type,
  title, excerpt, timestamps, taxonomy, thumbnail/media reference, update
  marker) — no body fetch. Video cards never request video bytes; gallery cards
  never request originals.
- Detail routes fetch the authoritative `DOCUMENT` entity via exact identity
  (`findExactResource` → `FETCH_QDN_RESOURCE`), validate it, and re-check the
  embedded `id` against the request.
- Routes: `/blog/:id`, `/videos/:id`, `/gallery/item/:id`, `/gallery/album/:id`.
  The canonical URL uses the bare 12-char stable id; the full `saw_*` identifier
  is accepted as a cheap alias (`resolveEntityReference`). The Phase 1B generic
  `/gallery/:id` route now `<Navigate replace>`s to `/gallery/item/:id`, so the
  two competing schemes are resolved in favour of the approved album/item model.

## 10. Safe rich-text rendering

- Read-only allowlisting renderer (`renderTipTap.ts`) understands only the
  supported TipTap node/mark subset; text is HTML-escaped; unknown nodes are
  dropped with their subtree and unknown marks ignored; only an explicit
  per-node attribute allowlist is read; rejected link URLs keep their text but
  lose the anchor.
- URL policy (`urlPolicy.ts`): `http(s)` allowed as external-web (never
  navigated directly), `qortal://` allowed, everything else (`javascript:`,
  `data:`, `vbscript:`, `file:`, relative, fragments, control chars) rejected.
  Image sources are limited to same-origin `/arbitrary/...` and raster
  `data:image/*;base64`.
- DOMPurify (`sanitizeHtml.ts`) runs as a defence-in-depth boundary on the
  renderer output, lazily imported only on the blog-detail route. Its explicit
  `ALLOWED_TAGS`/`ALLOWED_ATTR` allowlist is authoritative (the `html`
  `USE_PROFILES` union was deliberately removed — see §19); post-sanitize hooks
  strip `target` and force `rel="noopener noreferrer"`. Stored content is never
  injected as trusted raw HTML.
- Web2 links: `SafeRichText` intercepts `http(s)` clicks and copies via the
  documented cascade (`navigator.clipboard.writeText` → off-screen
  `execCommand('copy')` → manual selectable input), with visible success/failure.
  The platform's own interceptor is a second layer. Real-host clipboard remains
  OWNER VALIDATION REQUIRED.
- Malicious/partial fixtures cover script tags, raw HTML nodes, event-handler
  attributes, `javascript:`/`data:` URLs, malformed TipTap docs, nested
  unexpected objects, unknown-node wrapping, and style-injection attempts.

## 11. Video and Gallery read models

Video metadata is modelled with an explicit `QdnMediaReference` adapter boundary;
no player is added and no video bytes are requested. The detail page shows the
stored metadata and media reference and states that playback is not implemented
in this phase. Listing/detail thumbnails use `THUMBNAIL`/`IMAGE` services only;
gallery item dimensions are reserved from the contract.

## 12. Taxonomy, Home and Search

- Taxonomy is the app's hybrid contract; Core metadata `tags`/`category` are
  explicitly not canonical (fallback listings carry empty taxonomy).
  `/category/:slug` and `/tag/:slug` filter the already-loaded validated
  listings locally (no per-keystroke/per-card requests).
- Home renders Latest Posts / Latest Videos / Latest Gallery from the shared
  snapshot; Latest Posts/Videos are capped (`HOME_PREVIEW_COUNT`/`GALLERY_STRIP_COUNT`).
  Top Posts / Top Videos report the honest
  "Ranking unavailable until engagement data is implemented." state and issue no
  like query.
- Search is bounded local filtering over loaded listing metadata only (no QDN
  request per keystroke, no body text, no new index).

## 13. Cache, concurrency, error model

- Cache: app-namespaced IndexedDB `shadow-archives-qdn` v1, store `records`,
  typed keys, success-only TTL (5 min), version-based invalidation, in-memory
  fallback when IndexedDB is unavailable. Failures are never written, so a
  failed read cannot permanently hide a later success. Stale-while-revalidate:
  an expired-but-usable record is served and a forced refresh runs.
- Concurrency: a tiny in-repo `runBounded` pool (partition reads limit 3,
  per-kind discovery/entity concurrency limit 4); no unbounded `Promise.all`
  over arbitrary result sets, no dependency added for this.
- Errors are normalized at the domain boundary into distinguishable kinds
  (`bridge-unavailable`, `publisher-unscoped`, `network`, `timeout`, `rejected`,
  `resource-missing`, `malformed`, `unsupported-schema`, `oversized`,
  `partial-catalog`, `stale-catalog`, `unknown`) with archive states
  `loading/ready/empty/partial/stale/unavailable/error` and per-entity detail
  states `ready/withdrawn/missing/invalid/error/unavailable`.

## 14. Auth and write-path exclusion

`AuthProvider` remains dormant (no call on mount). `ContentProvider`
short-circuits when the publisher scope is unresolved, so no request is made at
all. A browser test with a recording host bridge over the real bundle saw only
`SEARCH_QDN_RESOURCES`/`FETCH_QDN_RESOURCE` and **no `GET_USER_ACCOUNT`**. No
write action name is imported or invoked by feature code; the only write
references are string-literal type declarations in `src/qortal/actions.ts`.

## 15. Files changed

Application repository (uncommitted): see `git status` in §21 for the exact
list. Summary:

- New `src/domain/`: `constants.ts`, `types.ts`, `validation.ts`,
  `identifiers.ts`, `taxonomy.ts`, `richText.ts`, `entities.ts`, `catalog.ts`,
  `index.ts` (+ 5 test files).
- New `src/services/`: `errors.ts`, `publisher.ts`, `queue.ts`, `cache.ts`,
  `qdnReader.ts`, `identity.ts`, `fallbackDiscovery.ts`, `catalogRepository.ts`,
  `contentRepository.ts`, `types.ts`, `index.ts` (+ 7 test files).
- New `src/qortal/qdn.ts` (+ test); `src/qortal/actions.ts` and
  `src/qortal/index.ts` extended with read primitives.
- New `src/app/providers/ContentProvider.tsx` (+ test).
- New `src/features/content/` (listing/richText helpers, hooks, state panels)
  and `src/features/gallery/GalleryAlbumPage.tsx` / `GalleryItemPage.tsx`.
- New `src/test/fixtures/` (test-only content + QDN fakes).
- Rewritten for real data: `types/content.ts`, home sections/`homeContent.ts`,
  `topContent.ts`, Blog/Video/Gallery pages, gallery detail alias, taxonomy
  pages, Search, About.
- Updated routing/config/providers/styles: `routes.tsx`, `navigation.ts`,
  `siteConfig.ts`, `AppProviders.tsx`, providers `index.ts`, `styles/content.css`.
- Dependency added: `dompurify` `^3.4.15`.

Canonical workspace: `projects/shadow-archives-webportal.md` (updated current
state only; clearly labelled historical snapshots preserved).

## 16. Validation executed

- `npm run lint` — PASS.
- `npm run typecheck` (`tsc -b`) — PASS.
- `npm test` (`vitest run`) — **PASS: 29 files, 258 tests** (Phase 1B baseline
  was 9 files / 59 tests).
- `npm run build` (`tsc -b && vite build`) — PASS.
- `npm run format:check` — PASS.
- `git diff --check` — clean in both repositories.
- Canonical workspace: `bash -n tools/validate-workspace.sh` and
  `bash tools/validate-workspace.sh` — **PASS** (5 expected human-review
  warnings, unchanged).

Production bundle (Node 20.19.2, 2026-09-11):

- Entry `index-*.js`: 382.32 kB raw / **120.25 kB gzip** (Phase 1B baseline
  345.07 kB / 109.36 kB gzip → **+10.89 kB gzip, ~+10.0%**). The increase is the
  read pipeline itself now being in the startup graph (domain validators,
  services, `ContentProvider`, eager Home/listing model). No heavy library
  entered the entry graph.
- Lazy blog-detail chunk `BlogPostPage-*.js`: 36.49 kB raw / 14.15 kB gzip —
  this is where **DOMPurify** lands (confirmed by grep: DOMPurify appears only in
  that chunk, not in the entry).
- Stylesheet 24.69 kB / 4.81 kB gzip; banner WebP 202.89 kB; each other route a
  separate 0.2–2.0 kB chunk.
- Bundle audit (grep over `dist/assets/*.js`): no `@mui`, no `qapp-core` /
  `MyAppDB`, no `prosemirror` / TipTap editor (only the `tiptap-json-v1` format
  token appears in the entry), no `video.js` / `hls.js` / `plyr`, no
  `PUBLISH_QDN_RESOURCE` / `SEND_CHAT_MESSAGE`. Q-Tube/SubWire/Quitter appear
  only as pre-existing Phase 1B external app-link targets, not as interop code.

## 17. Browser smoke test (production build, headless Chrome)

- Unscoped mode (no host): every route rendered with the correct `<h1>` and no
  error boundary — `/`, `/blog`, `/videos`, `/gallery`, `/about`, `/contact`
  style routes, `/category/:slug`, `/tag/:slug`, all detail routes (including
  the lazy blog-detail chunk), `/studio`, and the not-found route. The home
  region honestly reported "No production Qortal publisher identity is available
  in this context…" rather than a fake empty archive. Screenshots captured at
  390/768/1440 px.
- Hosted simulation (production bundle served with an injected `<base>` and a
  recording fake `window.qortalRequest` host bridge returning **test-only**
  catalog/entity fixtures):
  - Home rendered real cards from the catalog (Latest Posts, Latest Videos with
    duration badge, Gallery strip).
  - **No N+1**: home issued exactly **8** bridge reads (manifest search+fetch, 3
    partition searches+fetches) with 3 catalog entries, and **still 8** with 30
    catalog entries — proving listings never fetch bodies and discovery does not
    scale with results.
  - No `GET_USER_ACCOUNT` (or any auth/write action) was recorded.
  - Blog detail rendered hostile stored rich text safely: a literal
    `<img src=x onerror=alert(1)>` was escaped to text, a `javascript:` link was
    blocked (text kept, no anchor, no `javascript:` in output), and an
    `https://` link rendered with the product class and
    `rel="noopener noreferrer"`.
  - `/category/field-notes` and `/tag/archive` rendered 3 filtered cards;
    `/search?q=footage` rendered 1 — all from one shared load.
  - Gallery album detail (opened with both the bare id and the full
    `saw_album_*` alias) resolved the album entity and listed its catalog items.

## 18. Real Qortal host result

**NOT VERIFIED — OWNER VALIDATION REQUIRED.** No local Qortal node or Hub
Developer Mode session was available, so these layers could not be exercised:

- `_qdnBase` routing and relative asset resolution under
  `/render/APP/Shadow%20Archives` with an injected `<base>`.
- Injected `_qdnName` → publisher scope.
- Live `SEARCH_QDN_RESOURCES` / `FETCH_QDN_RESOURCE` against a real node.
- QDN media `<img src="/arbitrary/...">` serving in-host.
- Clipboard availability inside the Q-App iframe (the cascade is implemented and
  unit-tested; in-host behaviour is unverified).
- CSP behaviour for the lazy chunks and DOMPurify.

No public node was used from browser code as a workaround.

## 19. Adversarial self-audit (findings and remediation)

Checked against the full Phase 2A self-audit list. Results:

- **BLOCKER:** none.
- **HIGH — fixed.** DOMPurify's `USE_PROFILES: { html: true }` unioned a broad
  default tag set into the explicit `ALLOWED_TAGS`, re-admitting elements such
  as `<form>` at the sanitization boundary. Removed `USE_PROFILES` so the
  explicit allowlist is authoritative; `sanitizeHtml.test.ts` now asserts
  `iframe`/`form` are stripped and `target` is dropped with `rel` forced.
- **HIGH — fixed.** Gallery album item membership compared the raw route
  parameter against bare stable ids, so opening an album through the full
  `saw_album_<id>` alias showed no items. Fixed with the shared
  `resolveEntityReference` normalizer plus preference for the authoritative
  loaded album id; browser-verified for both URL forms and unit-tested.
- **MEDIUM — fixed.** `loadEntityDetail` rejected the full `saw_*` identifier
  even though the alias was intended, contradicting the documented behaviour.
  Now normalized via the shared resolver (wrong-kind identifiers still
  rejected).
- **MEDIUM — fixed.** `ContentProvider` invoked the injected loader even when no
  publisher scope existed (harmless with the real loader, but a needless call
  and a test-seam inconsistency). It now short-circuits and records
  `unavailable` without calling the loader.
- **LOW — fixed.** Lazy route chunks (blog detail importing DOMPurify) could
  exceed Testing Library's 1 s async default under parallel load; a global
  `asyncUtilTimeout` is configured in the test setup and Home tests pin an
  explicit unscoped environment.
- **LOW — accepted/documented.** `getQdnResourceStatus` and
  `getQdnResourceUrl` are verified read primitives retained for completeness but
  unused by the current pipeline (tree-shaken from the bundle: the entry chunk
  contains none of their bodies). `isAllowedImageSource` permits inline raster
  `data:image/*` while DOMPurify's URI allowlist strips `data:` URIs; the second
  gate fails closed, so such images are dropped rather than rendered.
- **LOW — explained.** Entry gzip +10.89 kB over Phase 1B (see §16).

All other audit items passed: no UI `qortalRequest`; bridge camelCase fields
distinct from REST names; exact identity post-filtering (no substring
collisions); catalog never authoritative; payload `publisher` never used as
authority; no hardcoded owner address; publisher scope from `_qdnName`; no
listing body/media fetches; no N+1; bounded pagination and concurrency; failures
never cached; stale/partial states explicit; one malformed entry cannot blank
the archive; no raw HTML insertion; `javascript:`/dangerous `data:` rejected;
stored web links do not navigate the Q-App away; no video bytes on
home/listing; no fabricated Top rankings; no startup auth; no
Q-Tube/Subwire/Quitter publishing work; no Qortium import.

## 20. Remaining unknowns

- Real-host validation items listed in §18 (OWNER VALIDATION REQUIRED).
- In-host media `<img>` reliability and clipboard success/failure visibility.
- Whether an owner-published catalog/manifest will exist at first; until then
  the app correctly shows bounded, explicitly-partial live discovery.
- End-to-end behaviour of the `q-apps.js` image `MutationObserver` interceptor
  in-host (it appears to target the first `img` only); same-origin
  `/arbitrary/...` sources should pass through untouched, but this is host-side
  and unverified here.
- Future deep/persisted full-text search over `bodyText` remains a separate
  bounded task (Phase 2A only does local listing-metadata filtering).

## 21. Git, commit and external-action state

- Application worktree: modified/untracked Phase 2A files only; `dist/` is
  git-ignored. No commit, tag, push, PR, issue or project mutation was
  performed.
- Canonical workspace: one documentation file modified
  (`projects/shadow-archives-webportal.md`); no commit.
- No QDN resource was published, no transaction was signed or sent, and no
  content was edited.

`git status --short` (application) at handoff:

```
 M package-lock.json
 M package.json
 M src/app/config/navigation.ts
 M src/app/config/siteConfig.ts
 M src/app/providers/AppProviders.tsx
 M src/app/providers/index.ts
 M src/app/router/routes.test.tsx
 M src/app/router/routes.tsx
 M src/components/layout/TopListPanel.tsx
 M src/features/about/AboutPage.tsx
 M src/features/blog/BlogPage.tsx
 M src/features/blog/BlogPostPage.tsx
 M src/features/engagement/topContent.ts
 M src/features/gallery/GalleryDetailPage.tsx
 M src/features/gallery/GalleryPage.tsx
 M src/features/home/HomePage.tsx
 M src/features/home/components/GalleryStrip.tsx
 M src/features/home/components/LatestPostsSection.tsx
 M src/features/home/components/LatestVideosSection.tsx
 M src/features/home/homeContent.ts
 M src/features/search/SearchPage.tsx
 M src/features/taxonomy/CategoryPage.tsx
 M src/features/taxonomy/TagPage.tsx
 M src/features/videos/VideoDetailPage.tsx
 M src/features/videos/VideosPage.tsx
 M src/qortal/actions.ts
 M src/qortal/index.ts
 M src/styles/content.css
 M src/test/setup.ts
 M src/test/utils.tsx
 M src/types/content.ts
?? src/app/providers/ContentProvider.test.tsx
?? src/app/providers/ContentProvider.tsx
?? src/domain/
?? src/features/content/
?? src/features/gallery/GalleryAlbumPage.tsx
?? src/features/gallery/GalleryItemPage.tsx
?? src/features/home/HomePage.data.test.tsx
?? src/qortal/qdn.test.ts
?? src/qortal/qdn.ts
?? src/services/
?? src/test/fixtures/
```

## 22. Owner next actions

1. Validate in a real Qortal host / Hub Developer Mode (read-only): `_qdnBase`
   routing, injected `_qdnName`, live search/fetch, media `<img>` serving,
   clipboard, CSP.
2. Confirm whether a catalog/manifest should be published (Phase 2A deliberately
   implements no publication); until then the fallback is partial by design.
3. Review and then commit/push the Phase 2A work if acceptable; nothing has been
   committed.

## 23. Saved report

`docs/shadow-archives-webportal/implementation/2026-09-11-phase-2a-qdn-read-pipeline-report.md`
