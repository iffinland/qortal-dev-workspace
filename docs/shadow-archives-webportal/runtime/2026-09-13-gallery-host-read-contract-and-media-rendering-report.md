# Shadow Archives Gallery — real-host read contract and media rendering

- Project: `shadow-archives-webportal-QORTAL`
- Task class: platform-boundary defect investigation → implementation → live
  read-only QDN validation (Workflow v2, follow-up to the 2026-09-13 Gallery
  index-coherence task)
- Date: 2026-09-13
- Author: DeepSeek (autonomous implementation agent, primary)
- Agent identity correction (2026-09-13): this task was executed by **DeepSeek**.
  The earlier `Codex` attribution was incorrect (inferred from an orchestration
  role/template rather than the actual executor) and is corrected above. This
  work must not be attributed to Codex. Closure status is recorded in the
  checkpoint note below.
- Checkpoint (2026-09-13, closure): owner real-host runtime validation
  **PASSED**; the Gallery owner workflow is accepted. The implementation is
  committed and pushed on `agent/shadow-archives-webportal/gallery-index-coherence`
  as `472f244` ("Fix Gallery bridge reads and media hydration"). Durable record:
  `projects/shadow-archives-webportal.md`.
- Application repo:
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Base revision: `b247ccd` (`agent/shadow-archives-webportal/gallery-index-coherence`)
- Status: implementation + automated + live read-only validation complete;
  **owner live-host validation pending** (one procedure, §9)
- No QDN write, transaction, publication, deploy, merge or push occurred.
- `handoff_sync = pending_authorization` (no commit/push authorization given;
  the changes are left in the working tree).

## 1. Confirmed root cause (first mismatch)

**RC-A (BLOCKER, read path).** The injected Qortal bridge returns the
**JSON-parsed body** for `FETCH_QDN_RESOURCE`, but the application required a
`string`. Every `DOCUMENT` read issued through the bridge therefore failed with
`FETCH_QDN_RESOURCE did not return text`.

Evidence chain (all reproduced, not assumed):

1. `qortal/src/main/resources/q-apps/q-apps.js` `handleResponse()` does
   `responseObj = JSON.parse(response)` for every `FETCH_QDN_RESOURCE` result and
   only falls back to the raw `response.text()` when the body is not JSON. The
   live nodes serve exactly this file (byte-identical, §4).
2. Executed inside the **real render frame** `http://127.0.0.1:24992/render/APP/Shadow%20Archives`
   in headless Chrome against the real injected shim:
   - `FETCH_QDN_RESOURCE {DOCUMENT, saw_img_askdqb7749wh}` → `typeof === 'object'`
     (parsed entity), not a string.
   - `FETCH_QDN_RESOURCE {DOCUMENT, saw_cat_manifest}` → `typeof === 'object'`.
   - `FETCH_QDN_RESOURCE {DOCUMENT, …, encoding: 'base64'}` → string (base64).
   - `FETCH_QDN_RESOURCE {IMAGE, saw_img_media_askdqb7749wh}` → string (raw bytes).
   - `GET_QDN_RESOURCE_STATUS` → object; `GET_QDN_RESOURCE_URL` → string;
     `SEARCH_QDN_RESOURCES` → array.
3. The **published** build then reproduced the owner's report verbatim on the
   live node: Gallery cards all rendered the empty-media glyph
   (`.sa-card__media--empty`, 4 of 4 cards, no `<img>`), the notice read
   "The archive catalog index is unavailable; showing bounded live search
   results that may be incomplete.", and
   `/gallery/album/n8ew5pjid5s2` rendered
   **"This resource could not be loaded / FETCH_QDN_RESOURCE did not return text"**.

Consequences of RC-A (single cause, all four owner symptoms):

| Symptom | Mechanism |
| --- | --- |
| Album/item detail error | `loadEntityDetail` → `reader.fetchText` → bridge object → thrown |
| "The Gallery index could not be read" | publish path `loadCatalog` → `readJsonResource` → same thrown error → `.kind: 'error'` → `skipReason` |
| "index update incomplete" after a successful publication | partition + manifest were never planned because the pre-write index read failed |
| Gallery cards show the missing-media glyph | no readable index ⇒ no catalog entry ⇒ discovery-only listing has `thumbnail: null`; the card renders the picture glyph |

The previous task's retry/reconciliation work (RC-1…RC-3 of the 2026-09-13
handoff) was correct but its live validation drove `loadArchive`/`loadCatalog`
through the **same-origin REST reader**. Owner mode uses `bridgeQdnReadPort`
(`resolveQdnReadPort` prefers the bridge whenever it is reachable, and
`createGalleryPublishDeps` always does), so the defective transport was never
exercised. That is why the exit criterion was still not met on the real host.

**RC-B (HIGH, read-path coherence).** With RC-A fixed the index becomes readable
again, but a published entity that the (already lagging) index does not carry is
still listed **without media**: bounded discovery supplies a locator plus Core
search metadata only, so `thumbnail`, `albumId`, canonical title and dimensions
are unknown. Cards show the placeholder and an album cannot resolve its members.
The published image `askdqb7749wh` (album `n8ew5pjid5s2`) is exactly this case.

**Not defects (verified, contrary to the initial hypotheses):**

- Media URL shape is **correct**. `buildQdnResourcePath` mirrors the verified
  non-link branch of the shim's `buildResourceUrl()`
  (`/arbitrary/<service>/<name>[/<identifier>][?filepath=]`). In the real render
  frame the app's exact URL loads (`naturalWidth` 480 for the thumbnail, 1024 for
  the media) in both bridge mode and same-origin mode, and the document's
  `<base href="/render/APP/Shadow%20Archives/">` does not affect absolute paths.
- Percent-encoding is fine: the encoded and the raw-space forms both resolve to
  the same request (`GET_QDN_RESOURCE_URL` returns the unencoded form; the
  browser encodes it identically).
- Text `DOCUMENT` and binary `IMAGE`/`THUMBNAIL` reads do share
  `fetchQdnResourceText`, but binary media is never read through it — media is
  rendered by `<img src>` straight from the node. The shared helper is therefore
  only wrong for the JSON branch, which is what was fixed.
  The one genuinely dangerous shape is a **relative** media URL
  (`arbitrary/...` without a leading slash): it resolves under the render base and
  the node answers `200 text/html` (the app shell) — that is what a broken image
  icon looks like here. The app never emits it; it is recorded as the guard rail.

## 2. What changed

| File | Change |
| --- | --- |
| `src/qortal/qdn.ts` | New exported `bridgeFetchResultToText()`; `fetchQdnResourceText` now normalizes a JSON-parsed bridge result (`object`/`array` → `JSON.stringify`) instead of throwing, with the verified live contract documented at the boundary. Non-JSON primitives still fail closed with the original error. |
| `src/domain/catalog.ts` | New `listingFromGalleryItem(entity, partitionIdentifier = 'entity')`: build a validated `CatalogListing` directly from an authoritative gallery-item entity (title, slug, excerpt, taxonomy, thumbnail, width/height, albumId). |
| `src/domain/constants.ts` | `LIMITS.listingHydrationMax = 24`. |
| `src/services/contentRepository.ts` | `loadArchive` now runs a bounded `hydrateListingMedia()` pass over merged listings (gallery items with no thumbnail that came from discovery only; `runBounded`, `LIMITS.entityConcurrency`, cached, best-effort) and `withDerivedAlbumCovers()` (a coverless album card uses its newest member item's thumbnail, read-side only). New diagnostics `listings-hydrated` / `listings-hydration-failed`; both the catalog branch and the bounded-discovery recovery branch build their snapshot from the hydrated listing set. |
| `src/qortal/qdn.test.ts` | +3 tests: parsed-object normalization, `bridgeFetchResultToText` table, non-JSON primitive still rejected. |
| `src/services/catalogRepository.test.ts` | +1 test: `loadCatalog` through `bridgeQdnReadPort` with a shim-contract fake whose JSON bodies arrive parsed (the owner-mode index read that produced "index update incomplete"). |
| `src/services/contentRepository.test.ts` | +4 tests: entity hydration in the catalog branch, hydration in the bounded-discovery recovery branch, honest degradation when the entity cannot be read, `withDerivedAlbumCovers` semantics (newest member wins, existing cover never overwritten). |

No wire contract, schema, taxonomy, identifier, authority or write-path change.
No architecture document was edited. `withDerivedAlbumCovers` is a **read-side
presentation decision** and is flagged for owner awareness in §9/§10: album
entities still publish `coverThumbnail: null`, so an album card would otherwise
always show the placeholder even when the album contains published media.

## 3. Live resource evidence — `saw_img_askdqb7749wh`

Nodes (read-only tunnels, reachability re-checked first; `/admin/info`
`buildVersion` recorded):

| Endpoint | Provenance |
| --- | --- |
| `http://127.0.0.1:24991` | `qortal-6.1.9-108bf19`, nodeId `NgrZWCr5ZUFZz768gsfBcStPqJErWUekTS` |
| `http://127.0.0.1:24992` | `qortal-6.1.9-108bf19`, nodeId `NNgJx6Ur669FvMf9pcvnm9o5ijmmahh4b7` |

| Resource | 24991 status | 24992 status | bytes served (24992) |
| --- | --- | --- | --- |
| `DOCUMENT saw_img_askdqb7749wh` | `MISSING_DATA` 1/2 | `READY` 2/2 | 624 B JSON, `created 1789304741034`, sig `4qHSwqS16naRe3Q8MeFWDAM79LmHj4vV48H5jkJsr4Pzs87uS96JxrXHdebcPGwGau3VZyAhdtkffQAh9By1AMFY` |
| `IMAGE saw_img_media_askdqb7749wh` | `MISSING_DATA` 1/2 | `READY` 2/2 | HTTP 200 `image/webp`, 225 972 B, RIFF WebP 1024×1024, `created 1789304735284` |
| `THUMBNAIL saw_img_thumb_askdqb7749wh` | `MISSING_DATA` 0/1 | `READY` 1/1 | HTTP 200 `image/webp`, 46 164 B, RIFF WebP 480×480, `created 1789304737008` |

Entity body served by both nodes (24992, 200 `application/json`):

```json
{"schemaVersion":1,"kind":"gallery-item","id":"askdqb7749wh","publisher":"Shadow Archives","createdAt":1789304731689,"updatedAt":1789304731689,"state":"active","data":{"title":"SA Branded Logo","description":"Shadow Archives branded logo","albumId":"n8ew5pjid5s2","media":{"service":"IMAGE","name":"Shadow Archives","identifier":"saw_img_media_askdqb7749wh","mimeType":"image/webp"},"thumbnail":{"service":"THUMBNAIL","name":"Shadow Archives","identifier":"saw_img_thumb_askdqb7749wh","mimeType":"image/webp"},"width":1024,"height":1024,"categories":["logos"],"tags":["logos","shadow archives logo"],"language":"en"}}
```

Index state (unchanged by this task, read-only): `saw_cat_manifest`
`catalogVersion 1`, `compiledAt 1789226023915`, single partition
`saw_cat_album_p000` (count 1); `saw_cat_album_p000` carries only
`5q3o5mln1yda`. The published item is genuinely absent from the published index.

## 4. Reference freshness (platform-dependent work)

- `github-clones/Qortal/qortal` — clean, `HEAD = master
  = 108bf191d42d710ec617f535af30cfd82fc03c87`; upstream `refs/heads/master`
  re-checked live (`git ls-remote`, 2026-09-13 13:46 UTC) = same SHA.
- `github-clones/Qortal/Qortal-Hub` — clean, `HEAD = develop
  = 12a573b27246e8a626b24794830c6bc432d1b05d`; upstream `refs/heads/develop`
  re-checked live = same SHA.
- **Runtime-provenance check:** `/apps/q-apps.js` fetched from *both* live nodes
  is byte-identical to the clone file:
  `md5 3ae7deaa55f353dc0ae4e8d13f3c1034`, 37 604 bytes. The inspected bridge
  source is therefore the code the host actually executes.
- No reference checkout was fetched, reset, cleaned or modified; no owner
  worktree was touched.

## 5. Verification method (why this is real-host evidence)

The published build cannot be changed without publishing, so the fixed build was
verified through a **faithful local render harness**: a local origin that serves
the freshly built `dist/`, injects the node's exact render head
(`<base href="/render/APP/Shadow%20Archives/">`, the `_qdn*` globals and
`<script src="/apps/q-apps.js">`), fetches the real shim from the live node, and
proxies `/arbitrary/*` to live node 24992. Consequences: the app runs in the real
render context, over the real bridge implementation, against the real published
resources. Headless Chrome (Playwright, `/usr/bin/google-chrome`) drove the app.

### Before (published `index-Bdr6TrQX.js`, live node, real shim)

- Gallery page: 4 cards, `fallbacks: 4`, `imgs: 1` (banner only) — every gallery
  card is the missing-media picture glyph.
- `/gallery/album/n8ew5pjid5s2`: `This resource could not be loaded` /
  `FETCH_QDN_RESOURCE did not return text`.
- Notice: `The archive catalog index is unavailable; showing bounded live search
  results that may be incomplete.`
- Two unhandled `pageerror: The request timed out`.

### After (built `dist/`, `index-BSv3DDNW.js`, md5 `7273f59612959f0929b4bf06dba07aff`)

Bridge mode (real shim) — identical results in same-origin REST mode (shim
omitted, `runtimeState: qortal-render-readonly`):

| View | Result |
| --- | --- |
| Home gallery strip | `THUMBNAIL saw_img_thumb_askdqb7749wh` 480 px, `saw_img_thumb_zud9a5dwv350` 480 px |
| `/gallery` | notice = "The archive index was out of date; it has been reconciled with live discovery…" ⇒ `catalog.kind === 'loaded'`; cards: `SA Branded Logo` img 480 ✔, `Shadow Archives Banner` img 480 ✔, `first album` img 480 ✔ (derived cover), `no-sorted` placeholder (that album has no published items) |
| `/gallery/item/askdqb7749wh` | entity parsed; `IMAGE saw_img_media_askdqb7749wh` 1024 px rendered; no error text |
| `/gallery/album/n8ew5pjid5s2` | album entity loads; `Items` lists `SA Branded Logo` with a 480 px thumbnail |
| Failure markers | none: no "did not return text", no "could not be read", no console error, no failed `/arbitrary/` request |

Network evidence (bridge mode, in order): `200 DOCUMENT saw_cat_manifest`,
`200 DOCUMENT saw_cat_album_p000`, `200 DOCUMENT saw_img_askdqb7749wh`,
`200 DOCUMENT saw_img_zud9a5dwv350` (hydration), `200 THUMBNAIL …`, `200 IMAGE
saw_img_media_askdqb7749wh`, `200 DOCUMENT saw_album_n8ew5pjid5s2`.

### Index-convergence proof (temporary probe, deleted after the run)

A throwaway vitest probe (not part of the suite, `git status` clean afterwards)
installed a shim-contract transport against live node 24992 and ran the real
publish-path read/plan code:

```
loadCatalog(bridgeQdnReadPort, 'Shadow Archives') -> kind: 'loaded'
existing listings:            [gallery-album:5q3o5mln1yda]
planCatalogWrite(gallery-item, askdqb7749wh):
  plannedPartition:           saw_cat_img_p000
  planned entries:            [saw_img_askdqb7749wh]
  planned manifest partitions:[saw_cat_album_p000 (kept), saw_cat_img_p000
                               count 1, maxUpdated 1789304731689,
                               checksum sha256:dbd2a0ec…]
  catalogVersion:             2
```

That is exactly the payload pair the next owner publication will write, so the
"index update incomplete" path is resolved: the failure was the pre-write index
**read**, and that read now succeeds through the same port the publish path uses.
The publish path additionally re-indexes known-orphaned entities
(`repairExistingListings`), so the two already-published items converge too.

## 6. Automated validation

| Command | Result |
| --- | --- |
| `npx vitest run` | 41 files / **443 tests passed** |
| `npx tsc -b` | clean |
| `npx eslint .` | clean |
| `npx prettier --check .` | clean |
| `npm run build` | success (`index-BSv3DDNW.js`, 391.90 kB / 123.28 kB gzip) |
| `git diff --check` | clean |

One pre-existing flake was observed once under full-suite load
(`src/features/home/HomePage.data.test.tsx › renders Home content from the
injected publishing identity`, a 1 s `findByRole` timeout while skeletons are
still rendered). It passes in isolation and in the final full run; it is
unrelated to this change (the injected archive loader bypasses `loadArchive`).

## 7. Self-audit (adversarial)

| # | Question | Finding |
| --- | --- | --- |
| 1 | Does the fix cover both transports? | Bridge normalized; same-origin already returned raw text. Both verified live (§5). |
| 2 | Could JSON re-serialization corrupt a payload? | Values are what the validators consume; timestamp integers are far below 2^53 and no field depends on key order or formatting. A non-object/array primitive still fails closed. |
| 3 | Does the shared text helper wrongly touch binary reads? | No; binary media is never read through `fetchText` (rendered via `<img>`). |
| 4 | Are media URLs valid inside `/render/APP/Shadow%20Archives`? | Yes, measured. The dangerous relative form returns `200 text/html` and is not emitted. |
| 5 | Does hydration break the "no body fetch per listing" rule? | It fetches ≤ 24 **entity envelopes** (≤ 256 KiB cap, ~600 B real) only for gallery items the index does not carry, cached by the existing entity cache; full-size media is still never downloaded. Flagged in §2. |
| 6 | Is hydration failure fatal? | No: the discovery listing is kept and a warning diagnostic is reported. |
| 7 | Does the derived album cover invent data or write QDN? | No: it reuses a member item's own thumbnail ref, read-side only. |
| 8 | Does the change alter publish semantics/order/authority? | No write-path change; `readCatalogContext`/`planCatalogWrite` untouched. |
| 9 | Any new dependence on the live node in tests/suite? | None; the live probe was deleted and the permanent tests use fixtures. |
| 10 | Remaining unresolved defect? | `no-sorted` (`5q3o5mln1yda`) album card still shows the placeholder because that album has no published member item at all — honest, not a rendering defect. |
| 11 | Did validation modify owner work? | `git status` shows only the 7 intended modified files plus the pre-existing untracked `AGENTS.md`; `dist/` is ignored. |

No BLOCKER or HIGH finding remained after the fixes above.

## 8. Branches / Git

- Application repo: branch `agent/shadow-archives-webportal/gallery-index-coherence`
  (base `b247ccd`, still tracking `origin/…`), 7 modified files, **not
  committed** (`b247ccd` is unchanged); `?? AGENTS.md` pre-existed this task.
- Workspace repo: this report and the owner handoff are added as untracked files;
  no commit (not authorized).

## 9. One owner live-host validation procedure

Prerequisite (owner action, one time): the fix exists only in the working tree.
Node 24992's render route still serves the **pre-fix** bundle
(`/render/APP/Shadow%20Archives/assets/index-Bdr6TrQX.js`, md5
`f87d64918aa5bbfc1cc0031b7173f21f`; it contains `b247ccd`'s `catalog-reconciled`
diagnostic and none of this change's new diagnostics, so it is the pre-fix build
of the committed revision), so a new APP artifact must be published first:
`npm run build && npm run package:app`, then publish the ZIP as
`Shadow Archives` / `APP`. Note: the packaging name is date-based, so this
overwrites the existing `release/shadow-archives-app-0.1.0-20260913.zip` — copy it
aside first if the currently deployed artifact must be preserved. No publication
was performed by this task.

1. Open `qortal://APP/Shadow Archives` in the Qortal host as owner, hard-reload
   (bypass cache) so the new bundle is served.
2. Open **Gallery**. Expected: `SA Branded Logo` and `Shadow Archives Banner`
   cards show real image thumbnails (not the picture glyph); the notice says the
   index is out of date and was reconciled, **not** that the catalog is
   unavailable.
3. Open **SA Branded Logo**. Expected: the full 1024×1024 image renders; no
   "FETCH_QDN_RESOURCE did not return text".
4. Open **first album** (`n8ew5pjid5s2`). Expected: the album entity loads and
   `Items` lists `SA Branded Logo` with its thumbnail; no
   "FETCH_QDN_RESOURCE did not return text".
5. Publish one new gallery image (owner action only). Expected: it ends with
   `Content published` **without** "index update incomplete", and after the
   automatic refresh the new item appears in Recent items with a thumbnail.
6. Reload the Gallery again. Expected: the index notice is gone or reduced to
   "showing the last cached archive index", and no card for a published gallery
   item falls back to the placeholder.

Report back: the exact notice text in step 2/6, and whether step 5 finished
without "index update incomplete".

## 10. Owner decisions requested (non-blocking)

1. `withDerivedAlbumCovers` (album card shows its newest member item's
   thumbnail). Acceptable read-side presentation, or should album cards keep the
   placeholder until albums publish a real `coverThumbnail`? Publishing a real
   album cover is a separate, write-path change and was deliberately not made.
2. Confirm the bounded hydration budget (`LIMITS.listingHydrationMax = 24`
   gallery items per archive load, entity envelopes only).
