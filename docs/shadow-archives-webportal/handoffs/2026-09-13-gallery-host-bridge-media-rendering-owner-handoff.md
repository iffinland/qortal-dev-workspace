# Owner handoff — Gallery real-host read contract, media rendering, index convergence

- Project: `shadow-archives-webportal-QORTAL`
- Date: 2026-09-13
- Author: DeepSeek (primary autonomous implementation agent)
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
- Detailed report (evidence, method, self-audit):
  `docs/shadow-archives-webportal/runtime/2026-09-13-gallery-host-read-contract-and-media-rendering-report.md`
- Application repo:
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Branch: `agent/shadow-archives-webportal/gallery-index-coherence`, base `b247ccd`
- Status: implementation + automated + live read-only validation complete;
  **owner live-host validation pending** (procedure in §8)
- No QDN write, transaction, publication, deploy, merge or push occurred
  (`handoff_sync = pending_authorization`).

## 1. Confirmed root cause

**The injected bridge returns the JSON-parsed body for `FETCH_QDN_RESOURCE`, but
the app required a `string`.** `q-apps.js` `handleResponse()` runs every fetched
body through `JSON.parse` and only falls back to raw text when the body is not
JSON, so every `DOCUMENT` read through the bridge threw
`FETCH_QDN_RESOURCE did not return text`.

This single defect produced all four owner symptoms:

1. Album/item detail: the entity read failed → "did not return text".
2. Gallery cards: the index could not be read → no catalog entry → the
   discovery-only listing has `thumbnail: null` → the card renders the
   missing-media picture glyph.
3. "The Gallery index could not be read" during publication: the pre-write
   `loadCatalog` used the same bridge port.
4. "index update incomplete": with no readable index, the partition + manifest
   were never planned, so the new entity was orphaned from the index.

The previous coherence fix was correct but was validated with the *same-origin
REST* reader; owner mode uses the *bridge* reader, which was never exercised.

A second, smaller read-path gap was fixed as well: a published entity the
(index-lagging) catalog does not carry was listed without media, canonical title
or album membership, so its card and its album page could not render it.

The generated media URLs were **verified correct**, not defective: in the real
render frame `/arbitrary/THUMBNAIL/Shadow%20Archives/saw_img_thumb_askdqb7749wh`
loads (480 px) and `/arbitrary/IMAGE/…/saw_img_media_askdqb7749wh` loads
(1024 px), in both bridge and same-origin mode, despite the document's
`<base href="/render/APP/Shadow%20Archives/">`. A *relative* media URL
(`arbitrary/...` with no leading slash) resolves under the render base and the
node answers `200 text/html` — that is precisely the broken-image shape, and the
app never emits it.

## 2. Exact bridge/runtime contract evidence

Live nodes (reachability re-checked): `http://127.0.0.1:24991` and
`http://127.0.0.1:24992`, both `qortal-6.1.9-108bf19` (nodeIds
`NgrZWCr5ZUFZz768gsfBcStPqJErWUekTS` / `NNgJx6Ur669FvMf9pcvnm9o5ijmmahh4b7`).

Both nodes serve `/apps/q-apps.js` byte-identical to the clean reference clone
(`github-clones/Qortal/qortal` @ `108bf191d42d710ec617f535af30cfd82fc03c87` =
upstream master, re-checked live 2026-09-13 13:46 UTC): `md5
3ae7deaa55f353dc0ae4e8d13f3c1034`, 37 604 bytes.

Executed inside the real render frame with the real shim:

| Action | Result shape |
| --- | --- |
| `FETCH_QDN_RESOURCE` `DOCUMENT saw_img_askdqb7749wh` | **object** (parsed JSON entity) |
| `FETCH_QDN_RESOURCE` `DOCUMENT saw_cat_manifest` | **object** (parsed JSON) |
| `FETCH_QDN_RESOURCE` `DOCUMENT …, encoding: 'base64'` | string (base64) |
| `FETCH_QDN_RESOURCE` `IMAGE saw_img_media_askdqb7749wh` | string (raw bytes) |
| `GET_QDN_RESOURCE_STATUS` | object `{status:'READY', localChunkCount:2, totalChunkCount:2}` |
| `GET_QDN_RESOURCE_URL` `IMAGE …` | string `"/arbitrary/IMAGE/Shadow Archives/saw_img_media_askdqb7749wh"` (unencoded space) |
| `SEARCH_QDN_RESOURCES` | array |

## 3. Files changed (7, application repo)

- `src/qortal/qdn.ts` — `bridgeFetchResultToText()`; `fetchQdnResourceText`
  normalizes a parsed JSON bridge result back to text (verified contract
  documented at the boundary).
- `src/domain/catalog.ts` — `listingFromGalleryItem()` (listing from an
  authoritative entity).
- `src/domain/constants.ts` — `LIMITS.listingHydrationMax = 24`.
- `src/services/contentRepository.ts` — bounded `hydrateListingMedia()` for
  gallery items the index does not carry (thumbnail, album membership,
  canonical display fields) with `listings-hydrated` /
  `listings-hydration-failed` diagnostics, plus `withDerivedAlbumCovers()`.
- `src/qortal/qdn.test.ts`, `src/services/catalogRepository.test.ts`,
  `src/services/contentRepository.test.ts` — 8 new focused tests for the
  confirmed runtime contracts.

## 4. Exact live resource evidence (`saw_img_askdqb7749wh`)

| Resource | 24991 | 24992 | Served bytes (24992) |
| --- | --- | --- | --- |
| `DOCUMENT saw_img_askdqb7749wh` | `MISSING_DATA` 1/2 | `READY` 2/2 | 624 B JSON, created `1789304741034`, sig `4qHSwqS16naRe3Q8MeFWDAM79LmHj4vV48H5jkJsr4Pzs87uS96JxrXHdebcPGwGau3VZyAhdtkffQAh9By1AMFY` |
| `IMAGE saw_img_media_askdqb7749wh` | `MISSING_DATA` 1/2 | `READY` 2/2 | 200 `image/webp`, 225 972 B, WebP 1024×1024, created `1789304735284` |
| `THUMBNAIL saw_img_thumb_askdqb7749wh` | `MISSING_DATA` 0/1 | `READY` 1/1 | 200 `image/webp`, 46 164 B, WebP 480×480, created `1789304737008` |

Entity body: `gallery-item`, title `SA Branded Logo`, albumId `n8ew5pjid5s2`,
media → `IMAGE saw_img_media_askdqb7749wh`, thumbnail →
`THUMBNAIL saw_img_thumb_askdqb7749wh`, 1024×1024.

Published index (unchanged, read-only): `saw_cat_manifest` `catalogVersion 1`,
one partition `saw_cat_album_p000` with `5q3o5mln1yda`; the new item is absent.

## 5. Tests / build

- `npx vitest run` → 41 files / **443 tests passed**.
- `npx tsc -b` → clean; `npx eslint .` → clean; `npx prettier --check .` → clean.
- `npm run build` → success (`index-BSv3DDNW.js`, md5
  `7273f59612959f0929b4bf06dba07aff`); `git diff --check` → clean.
- One pre-existing, unrelated flake in `HomePage.data.test.tsx` was seen once
  under full-suite load; it passes in isolation and in the final full run.

## 6. Why image URLs now render correctly

The URL construction was already correct and is now proven live. What changed is
that cards finally **have** a media reference to render: the catalog read over
the bridge succeeds again (so indexed entries carry their thumbnail refs), and
gallery items the index does not yet carry are resolved from their authoritative
entity (thumbnail + album membership + canonical fields). Album cards without a
published cover show their newest member item's thumbnail. The app's `<img>`
source is the leading-slash same-origin path
`/arbitrary/<service>/<name>/<identifier>`, which the node serves as real
`image/webp` inside the render frame.

## 7. Why "index update incomplete" is fixed

The publication never failed to *write*; it failed to *read the index first*
(`readCatalogContext` → `loadCatalog` → `readJsonResource` → `fetchText` threw).
With the bridge result normalized, the real published index reads through the
bridge contract (§2) and the plan for the real item is produced:

```
plannedPartition:      saw_cat_img_p000
planned entries:       [saw_img_askdqb7749wh]
planned manifest:      saw_cat_album_p000 kept + saw_cat_img_p000
                       (count 1, maxUpdated 1789304731689,
                        checksum sha256:dbd2a0ec…), catalogVersion 2
```

This was produced with the real shim contract against live node 24992 (temporary
probe, deleted afterwards; the suite has no live-node dependency). A later owner
publication therefore converges the index, and `repairExistingListings` also
re-indexes the already-orphaned entities. No external blocker remains.

## 8. Owner live-host validation procedure (one pass)

Precondition (owner action): the fix exists only in the working tree. Node 24992's
render route still serves the pre-fix bundle
(`/render/APP/Shadow%20Archives/assets/index-Bdr6TrQX.js`, md5
`f87d64918aa5bbfc1cc0031b7173f21f` = the pre-fix build of the committed revision).
Run `npm run build && npm run package:app`, then publish the ZIP
as `Shadow Archives` / `APP` (the date-based name overwrites the existing
`release/shadow-archives-app-0.1.0-20260913.zip`, so copy it aside first if the
deployed artifact must be preserved). Then:

1. Open `qortal://APP/Shadow Archives` as owner and hard-reload.
2. Gallery: `SA Branded Logo` and `Shadow Archives Banner` cards show real
   thumbnails; the notice mentions a reconciled/index-out-of-date index, **not**
   an unavailable catalog.
3. Open `SA Branded Logo`: the full 1024×1024 image renders; no
   `FETCH_QDN_RESOURCE did not return text`.
4. Open `first album`: the album loads and `Items` lists `SA Branded Logo` with
   its thumbnail; no `FETCH_QDN_RESOURCE did not return text`.
5. Publish one new gallery image (owner action). Expected: `Content published`
   **without** "index update incomplete", and the new item appears with a
   thumbnail after refresh.
6. Reload Gallery: no placeholder card for a published gallery item.

Please report the step 2/6 notice text and whether step 5 ended without
"index update incomplete".

## 9. Owner decisions requested (non-blocking)

1. Album cards now derive a cover from their newest member item when the album
   has no published `coverThumbnail`. Keep this, or show a placeholder until
   albums publish a real cover (separate write-path change)?
2. Confirm the bounded hydration budget (`LIMITS.listingHydrationMax = 24`
   gallery entity envelopes per archive load).

## 10. Branch / Git status

- App repo: `agent/shadow-archives-webportal/gallery-index-coherence`, 7 modified
  files, **not committed** (HEAD still `b247ccd`); pre-existing untracked
  `AGENTS.md` untouched.
- Workspace repo: this handoff and the runtime report are untracked; no commit.
