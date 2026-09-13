# Shadow Archives Gallery — owner workflow, catalog/index coherence, and live-evidence handoff

- Project: `shadow-archives-webportal-QORTAL`
- Task class: QDN publication / discovery / catalog implementation + read-only
  live-QDN validation (Workflow v2)
- Date: 2026-09-13
- Author: DeepSeek (autonomous implementation agent)
- Agent identity correction (2026-09-13): this task was executed by **DeepSeek**.
  The earlier `Codex` attribution was incorrect (inferred from an orchestration
  role/template rather than the actual executor) and is corrected above. This
  work must not be attributed to Codex. Closure status is recorded in the
  checkpoint note below.
- Checkpoint (2026-09-13, closure): owner real-host runtime validation
  **PASSED**; the Gallery owner workflow is accepted. The implementation is
  committed and pushed on `agent/shadow-archives-webportal/gallery-index-coherence`
  as `b247ccd` ("Fix Gallery catalog coherence and recovery"). Durable record:
  `projects/shadow-archives-webportal.md`.
- Application repo:
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Base revision: `6ec2915a47b8310348daf537ac83caf5ff625959` (`6ec2915`, `main`)
- Status: implementation + automated + live read-only validation complete;
  **owner live-host validation pending** (one step, §8)
- No QDN write, transaction, publication, delete, deploy, merge or push occurred.
- `handoff_sync = pending_authorization` (no commit/branch/push authorization was
  given; changes are left in the working tree on `main`).

## 1. Root cause(s)

The owner-visible failure was **not** a bad metadata submission and **not** a
wire-contract mismatch. Media, thumbnail, entity and catalog resources were all
published correctly. Two app-side coherence defects turned a *transient Qortal
data-availability state* into permanently wrong behavior.

**RC-1 (primary, read path) — a catalog data-read failure was treated as a fatal
error with no discovery fallback.**
`catalogRepository.loadCatalog` resolves the resource by search, then fetches the
resource **bytes**. On a Qortal node the search index can be available while the
resource data is still not (status `MISSING_DATA` / `DOWNLOADING`, body
`{"error":1401,"message":"Data unavailable. Please try again later."}` or HTTP
404). `contentRepository.loadArchive` had an explicit branch that returned an
empty `status: 'error'` snapshot for that case *before* running the bounded
fallback discovery, deliberately ("A failed catalog read (network) is reported as
an error rather than silently retried as a fallback discovery"). Result: a node
that could not serve catalog bytes showed **no Gallery content at all**, even
though every entity was discoverable. This directly violates the owner-approved
contract §7.3 recovery rule ("missing/corrupt/stale catalog → direct prefix
search; never present catalog absence as no content").

**RC-2 (primary, publish path) — the same transient read failure permanently
orphaned the new entity from the index.**
`galleryPublishService.readCatalogContext` performed a single, un-retried
`loadCatalog` before any write. On `kind: 'error'` it set `plan: null`, so the
catalog partition + manifest were never written for that publication ("Content
published, index update incomplete. The Gallery index could not be read…"). Every
later publication then planned from the catalog alone, so the skipped entity was
never re-added.

**RC-3 (coherence) — a readable but incomplete catalog was trusted as complete.**
Once a *valid* manifest existed, `loadArchive` returned `source: 'catalog'` with
exactly the catalog's entries and never confirmed them against authoritative
entities. The derived index therefore became the de-facto source of truth for the
listing set, contrary to "entity resources stay authoritative".

### Confirmed live mismatch (first mismatch, not assumed)

The published index is demonstrably behind the authoritative entities:

- `saw_cat_manifest` (DOCUMENT, `Shadow Archives`): `catalogVersion: 1`,
  `partitions: [{ identifier: "saw_cat_album_p000", type: "gallery-album",
  count: 1, maxUpdated: 1789226023770, checksum: null }]` — **one album partition
  only**.
- `saw_cat_album_p000`: one entry (`5q3o5mln1yda`).
- Authoritative entities that exist but are **absent from the index**:
  `saw_img_zud9a5dwv350` (gallery item) and `saw_album_n8ew5pjid5s2` (album).
- Reproduced at source level: on live node `24991` the manifest **bytes** are
  `MISSING_DATA` (`localChunkCount: 1 / totalChunkCount: 2`) and
  `GET /arbitrary/DOCUMENT/Shadow%20Archives/saw_cat_manifest` returns
  `{"error":1401,"message":"Data unavailable. Please try again later."}`; on live
  node `24992` all resources are `READY`/`DOWNLOADED` (100 %).
- Before the fix, the app's own code over a same-origin reader produced exactly
  the owner's symptoms: `loadArchive(24991)` → `status: 'error'`, `source: 'none'`,
  **0 listings**; `loadArchive(24992)` → `source: 'catalog'`, **1 listing**
  (`5q3o5mln1yda` only) — the published image was invisible.

## 2. Scope and non-goals

In scope and changed: Gallery owner publication, albums, image/thumbnail/entity
publication, Gallery metadata, catalog/index write path, fallback discovery,
Gallery listing/detail, reload persistence.

Not touched: Blog, Video, SubWire, Q-Tube, engagement, visual design, moderation,
authority/auth model, Qortal integration boundary, wire contracts.

## 3. Files changed (5, all in the application repo)

| File | Change |
| --- | --- |
| `src/services/contentRepository.ts` | New exported `mergeListings`; `loadArchive` now runs a bounded metadata-only discovery alongside a readable catalog and merges it, and uses full bounded discovery as the recovery path for a missing/invalid/**unreadable** catalog instead of an empty error snapshot. New `catalog-unreadable` / `catalog-reconciled` diagnostics; `loadCatalogSafely` normalizes a thrown transport error to a result. |
| `src/services/catalogWriter.ts` | `planCatalogWrite` now re-indexes **unassigned** listings of the target type (e.g. entries restored from discovery) into the target partition via a shared `listingToEntry` + `upsertEntry`, with `isPlannableEntry` guarding validation. |
| `src/services/galleryPublishService.ts` | `readCatalogContext(deps, name, type)` now (a) retries a transient index read (`CATALOG_READ_MAX_ATTEMPTS = 3`, 600 ms, injectable `delay`) and (b) repairs the index by fetching the payloads of authoritative entities the readable catalog is missing (`repairExistingListings`, bounded to 25, gallery kinds only). |
| `src/services/contentRepository.test.ts` | +2 tests: catalog reconciliation from discovery; catalog bytes unreadable → fallback discovery (not a hard error). |
| `src/services/galleryPublishService.test.ts` | +3 tests: transient index-read retry; index repair of an orphaned entity; end-to-end "index write skipped → item still listed" through the real read pipeline. Test `makeDeps` injects a no-op `delay`. |

No architecture document was edited. The read-path behavior change is a
contract-consistent implementation of the owner-approved §7.3 recovery rule
(always run bounded prefix discovery; the catalog never proves completeness) and
is called out here for owner awareness rather than silently changed.

## 4. Exact live Qortal evidence (read-only)

Nodes (per `AI-Orchestration/ENVIRONMENT.md` tunnels, verified reachable first):

| Endpoint | Provenance (read-only `/admin/info`, `/admin/status`) |
| --- | --- |
| `http://127.0.0.1:24991` | mainnet full node `qortal-6.1.9-108bf19`, `syncPercent: 100`, height 2722777, nodeId `NNgJx6Ur669FvMf9pcvnm9o5ijmmahh4b7`, 49 connections |
| `http://127.0.0.1:24992` | same build; used for the reproducible happy path |

Exact resource evidence (2026-09-13, both nodes):

- `DOCUMENT / Shadow Archives / saw_img_zud9a5dwv350` — size 608, created
  `1789226111115`, signature `3FdYKdBRGqt3jsQTU77BU2jg42kSAEkjGpfFwtL4uzfrnhffZQQvhiDTdwwBCngjqcgnKWNCvwV8zJz5cUVsGpF8`. Body: valid `gallery-item`, title "Shadow Archives Banner", media → `IMAGE / saw_img_media_zud9a5dwv350`, thumbnail → `THUMBNAIL / saw_img_thumb_zud9a5dwv350`, 1202×683.
- `DOCUMENT / saw_cat_manifest` — size 512, created `1789226030850`; body as quoted in §1 (`catalogVersion: 1`, single album partition).
- `DOCUMENT / saw_cat_album_p000` — size 608; one `gallery-album` entry `5q3o5mln1yda`.
- `DOCUMENT / saw_album_5q3o5mln1yda` ("no-sorted") and
  `DOCUMENT / saw_album_n8ew5pjid5s2` ("first album") — both valid; the second is
  not in the index.
- `IMAGE / saw_img_media_zud9a5dwv350` — `saw-img-zud9a5dwv350.webp`, 177854 B,
  `image/webp`; byte fetch on 24992 → HTTP 200, 177714 B, real WebP 1201×682.
- `THUMBNAIL / saw_img_thumb_zud9a5dwv350` — `saw-img-zud9a5dwv350-thumb.webp`,
  44478 B, `image/webp`; byte fetch → HTTP 200, 44338 B, real WebP 479×272.
- 24991 manifest/partition/entity **bytes**: unavailable (`MISSING_DATA`,
  1/2 chunks; `/arbitrary/...` → error 1401; item data HTTP 404) — a node data
  condition, not an app defect (consistent with the Phase 2C-B finding).

App code run against the live nodes with a same-origin read transport
(`sameOriginQdnReadPort`):

- Before fix — `loadArchive(24991)`: `status: 'error'`, `source: 'none'`,
  `listings: []`. `loadArchive(24992)`: `source: 'catalog'`, 1 listing only.
- After fix — `loadArchive(24992)`: `source: 'catalog'`, `status: 'partial'`,
  3 listings (`n8ew5pjid5s2`, `zud9a5dwv350`, `5q3o5mln1yda`), diagnostic
  `catalog-reconciled`: "2 published item(s) were missing from the archive index
  and were restored from live discovery."
- After fix — `loadArchive(24991)`: `source: 'fallback'`, `status: 'partial'`,
  the same 3 listings, diagnostic `catalog-unreadable`: "The archive catalog index
  could not be read; showing live discovery instead."
- `loadEntityDetail('gallery-item','zud9a5dwv350')` on 24992: `status: 'ready'`
  with the full valid entity. (On 24991: `status: 'error'` — node lacks bytes.)
- `discoverArchive`: 3 listings, `pagesFetched: 4`, no diagnostics.

Reference freshness gate (per `ENVIRONMENT.md`), re-run 2026-09-13:
`github-clones/Qortal/qortal` clean, `HEAD == origin/master == 108bf191`
(= running node `6.1.9-108bf19`); `Qortal-Hub` `12a573b2`, `qapp-core` `0f9d6ac5`,
`qapp-templates` `143cc7b` — all clean. No reference clone was modified.

## 5. Design of the fix (why this shape)

1. **The catalog is derived; entities are authoritative.** Reconciliation is done
   at read time (`mergeListings`) so an incomplete or unreadable index can never
   hide a published entity. Catalog entries win on identifier conflicts because
   they carry richer compiled summaries; discovered-only entries are added.
2. **Cost is bounded.** A readable catalog reconciles with one newest-first page
   per kind (≤4 metadata-only searches, never a body fetch). Only an unusable
   catalog uses the full bounded fallback discovery that already existed.
3. **The index converges, not just the view.** A later successful publish repairs
   the catalog: `repairExistingListings` finds authoritative entities the readable
   catalog is missing, fetches only those payloads (≤25), rebuilds rich entries
   (thumbnail, dimensions, taxonomy) and `planCatalogWrite` re-indexes them.
4. **Safety is preserved.** An invalid/partial/unreadable index is still left
   untouched (rebuilding from a partial view could drop entries); failures in
   repair are best-effort and never block the authoritative content write; the
   write path's authority order (media → thumbnail → entity → catalog) is
   unchanged.

## 6. Validation

Automated (application repo, Node 20):

- `npm run typecheck` (`tsc -b`) — pass.
- `npm run lint` (`eslint .`) — pass.
- `npx prettier --check` on the 5 changed files — pass (after formatting).
- `npm run test` (`vitest run`) — **41 files / 434 tests pass** (two consecutive
  full green runs). One transient failure was observed in
  `src/features/home/HomePage.data.test.tsx > published render runtime without a
  bridge > renders Home content from the injected publishing identity`; it uses an
  injected loader and is **off the changed path**. Reproduced on a clean detached
  worktree at base `6ec2915`: **4/10 failures at baseline vs 1/10 with this
  change** — pre-existing flake, not a regression. Scratch worktree removed.
- `npm run build` — pass. Entry `dist/assets/index-Cs8w9OOu.js` 389.63 kB raw /
  122.70 kB gzip; `GalleryOwnerPanel` stays a lazy chunk (45.76 kB / 13.62 kB
  gzip).
- Live read-only (both nodes) as recorded in §4.
- `git diff --check` — clean. Validation did not modify the worktree beyond the 5
  intended files (`dist/` is git-ignored).

Focused tests added for the request/response coherence contract:

- `contentRepository.test.ts`: "restores published entities the catalog is
  missing, from live discovery"; "falls back to bounded live discovery when the
  catalog data cannot be read".
- `galleryPublishService.test.ts`: "retries a transient index read before treating
  the index as unavailable"; "re-indexes an authoritative gallery item a previous
  publish left out of the catalog"; "still lists a published item when the index
  write was skipped".

## 7. Adversarial self-audit

| # | Check | Result |
| --- | --- | --- |
| 1 | Does reconciliation duplicate cards when catalog and discovery agree? | No — `mergeListings` dedupes by exact identifier; verified live (3 unique listings). |
| 2 | Can a malformed discovered entry fail the whole index plan? | No — `isPlannableEntry` bounds title/excerpt and drops invalid candidates; the plan is still gated by `assertCatalogPlanValid`. |
| 3 | Can a repair re-add a withdrawn entity as active? | No — entries are rebuilt from the validated payload and carry the payload's `state`. |
| 4 | Can a repair drop existing catalog entries? | No — existing entries are preserved and `upsertEntry` only replaces by identifier. |
| 5 | Does a repair failure block publishing? | No — best-effort, degrades to the untouched catalog. |
| 6 | Does the retry create duplicate writes? | No — the retry is a read only; the catalog read is read-only. |
| 7 | Does the retry slow a genuine failure unreasonably? | Bounded: 3 attempts, 600 ms apart (≤1.2 s), index-read only. |
| 8 | Does reconciliation break listing performance/scale? | Bounded to one newest-first page per kind for a readable catalog; no entity-body fetch. Full discovery only when the catalog is unusable. |
| 9 | Does a fully readable, complete catalog still report `ready`? | Yes — unchanged; new tests and the existing "reports ready for a complete catalog" test pass. |
| 10 | Does the UI stay truthful when the index lagged? | Yes — `partial` + `catalog-reconciled` diagnostic + an explicit "index was out of date…" notice via `ListingNotice`. |
| 11 | Is the publish-time authority order unchanged? | Yes — media → thumbnail → entity → catalog; pre-write and per-stage authority re-checks untouched. |
| 12 | Any new secrets/hardcoded owner identity? | No. |
| 13 | Working tree hygiene | Only the 5 intended files modified; the pre-existing untracked `AGENTS.md` was left untouched; no commit/push/branch. |

Confirmed findings: none outstanding at BLOCKER/HIGH. RC-1/RC-2/RC-3 are fixed and
covered by tests. Residual (MEDIUM, documented): on a *large* archive, a
reconciliation page bound (20/kind) may not surface an index gap older than the
newest page; the publish-time repair is the convergence mechanism for those, and
it repairs only the entity kind being published. Not a BLOCKER for the Gallery
slice.

Capability harvest: recorded as **project-specific**. The finding (Qortal node
search index can be available while resource bytes are `MISSING_DATA`; a catalog
must therefore be reconciled against discovery and the index repaired from
authoritative entities) is reusable for any Qortal indexed-app pattern, but no
shared skill was created or modified in this task (none existed to update, and
skill changes were not authorized).

## 8. Remaining owner validation (one live-host step)

In the real Qortal host as the verified owner, on the updated build:

1. Open Gallery and confirm the three existing live items now appear
   (`Shadow Archives Banner`, `first album`, `no-sorted`) — they are shown even
   though `saw_cat_manifest` still only declares the single album partition.
2. Publish one gallery **image**: confirm the message is a full success
   ("Published. …"), not "index update incomplete". Then:
   - confirm the item is immediately listed in Gallery and its detail route renders
     the image + thumbnail;
   - re-read `saw_cat_manifest` / `saw_cat_img_p000`: `catalogVersion` incremented,
     a `saw_cat_img_p000` descriptor exists, and the partition contains the new
     item **plus** the previously orphaned `saw_img_zud9a5dwv350`;
3. Publish one gallery **album**: confirm `saw_cat_album_p000` now contains both
   `saw_album_5q3o5mln1yda` and the previously orphaned `saw_album_n8ew5pjid5s2`.
4. Reload the app: the listing and detail must persist.
5. Report the exact new entity/partition/manifest identifiers back for closure.

Expected: a full PASS with no "index could not be read" message.

## 9. Git status

- Repo: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Branch: `main`; base `HEAD` `6ec2915a47b8310348daf537ac83caf5ff625959`
- Working tree: 5 modified files (uncommitted), `git diff --check` clean.
- Untracked `AGENTS.md` is pre-existing owner content — untouched.
- No commit, branch, push, merge, tag, release, QDN write, transaction or deploy
  was performed. Recommended agent branch/worktree if the owner wants durable
  history: `agent/shadow-archives-webportal/gallery-index-coherence`.
- `handoff_sync = pending_authorization`.

## 10. Saved report

`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-13-gallery-owner-workflow-index-coherence-owner-handoff.md`
