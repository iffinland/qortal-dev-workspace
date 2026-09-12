# Shadow Archives Phase 3A — Owner-only Studio navigation + Gallery publishing

- Date: 2026-09-12
- Workflow: Qortal Development Workflow v2 (phase implementation)
- Status: **implementation complete, ready for owner runtime validation**
- Live write performed: **NO** (see the explicit statement at the end)

## 1. Baselines

| Repository | Path | Branch | Baseline commit | State at start |
| --- | --- | --- | --- | --- |
| Canonical workspace | `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace` | `main` | `8af255c` | clean (1 pre-existing untracked owner report) |
| Application | `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL` | `main` | `3bd9173` ("Add Shadow Archives host diagnostics") | clean |

Baseline application verification (before any Phase 3A change, re-confirmed):

- `npm test` → 32 files / **303 tests** pass.
- `npm run lint`, `npm run typecheck`, `npm run format:check` → pass.
- `npm run build` → entry `index-CDc6bLtA.js` **383.08 kB** raw / **120.46 kB** gzip.
- Workspace `bash tools/validate-workspace.sh` → PASS (5 pre-existing warnings).

Reference sources re-read from disk (not memory):

- Qortal Core `qortal` @ `108bf191d42d710ec617f535af30cfd82fc03c87` (v6.1.9) —
  `/home/iffi/qortal-phase1a-research/qortal`
- Qortal Hub `Qortal-Hub` @ `12a573b27246e8a626b24794830c6bc432d1b05d` —
  `/home/iffi/qortal-phase1a-research/Qortal-Hub`

Both were still the pinned upstream revisions.

## 2. Qortal write contracts re-verified (2026-09-12)

Re-inspected before writing any writer code:

- **`q-apps.js` (Core `108bf191`)** forwards the whole flat request object to the
  host for `PUBLISH_QDN_RESOURCE` and `PUBLISH_MULTIPLE_QDN_RESOURCES`, and gives
  both a default timeout of `60 * 60 * 1000` ms because of proof-of-work
  (`q-apps.js` `getDefaultTimeout`).
- **Request fields (Hub `12a573b2`, `src/qortal/get.ts`).**
  - `publishQDNResource`: requires `service`; requires one of
    `file` / `blob` / `data64` / `base64`; accepts `name`, `identifier`,
    `filename`, `title`, `description`, `category`, `tags` (and legacy
    `tag1..tag5`), `isMultiFileZip`, `encryption`, `appFee`. A null/absent
    `identifier` becomes `'default'`. Unknown fields are ignored.
  - `publishMultipleQDNResources`: requires a non-empty `resources[]`; each entry
    accepts the same per-resource fields.
- **File/data handling.** `data64`/`base64` carry base64 bytes; `file`/`blob`
  carry a `File`/`Blob`. Hub checks `file.size > MAX_SIZE_PUBLISH` (2 GB) and,
  on a public node, `> MAX_SIZE_PUBLIC_NODE` (500 MB). We send base64 for
  deterministic size control and because the owner approves from the host UI.
- **Metadata + identifiers.** Identifier is a 64-byte-bounded string; metadata is
  `title` / `description` / `category` / `tags`. Core's
  `ArbitraryDataTransactionMetadata` caps title ≤ 80, description ≤ 240, and 5
  tags of ≤ 20 characters each — the writer mirrors app taxonomy into Core
  metadata inside those caps.
- **Services (Core `Service.java`, authoritative over any Hub copy).**
  `Service(int value, boolean requiresValidation, Long maxSize, boolean single,
  boolean isPrivate, List<String> requiredKeys)`:
  - `IMAGE(400, true, 10*1024*1024L, false, false, null)` → 10 MiB cap.
  - `THUMBNAIL(410, true, 500*1024L, true, false, null)` → 500 KiB, single file.
  - `DOCUMENT(800, false, null, false, false, null)` → no Core cap (the app
    imposes its own 256 KiB entity / 1 MiB catalog payload caps).
  - `APP(1000, true, 50*1024*1024L, false, false, null)` → 50 MB.
- **Permission.** The Hub asks for permission per call unless the tab already
  holds a session permission for that action; `getUserPermission` resolves
  `false` after one minute with no answer. We do not suppress or pre-grant it.
- **Fee.** The host computes and displays the fee from the fee table; nothing is
  hardcoded in the app.
- **Ownership enforcement.** Hub verifies that each resource `name` belongs to
  the publisher before publishing; Core's `ArbitraryTransaction.isValid()`
  requires the signer to own the name. This is server-side enforcement in
  addition to our client-side gate.
- **Publish response shape.** `PUBLISH_QDN_RESOURCE` resolves the raw
  `/transactions/process` transaction JSON (an object with `signature`).
- **`PUBLISH_MULTIPLE_QDN_RESOURCES` semantics.** The Hub publishes the resources
  **sequentially** and, when any fail, returns
  `{ message, error: { unsuccessfulPublishes: [{ reason, identifier, service,
  name }] } }`. Successful resources are **not** rolled back — this is a genuine
  partial success. Hub retries its own HTTP POSTs (up to 3 attempts, 25 s
  backoff), so a client-side timeout does **not** prove failure.

### 2.1 Single vs. multi-resource decision (evidence-based)

**Decision: staged publication — three host calls per Gallery item.**

1. `PUBLISH_MULTIPLE_QDN_RESOURCES` — `IMAGE` media + `THUMBNAIL` (2 resources).
2. `PUBLISH_QDN_RESOURCE` — the authoritative `DOCUMENT` entity.
3. `PUBLISH_MULTIPLE_QDN_RESOURCES` — catalog partition + manifest (2 resources).

Album publication is two calls: entity, then catalog partition + manifest.

Evidence and rationale:

- One single 5-resource multi-call would violate the mandated ordering, because
  the Hub gives no per-resource ordering guarantee beyond array order and no
  per-resource commit boundary; a mid-array failure would leave the entity
  published with unknown media and no way to attribute the failure precisely.
- The mandated authority order is media → thumbnail → entity → catalog
  partition → manifest. Staging makes each boundary explicit and each failure
  attributable (`unsuccessfulPublishes` per service+identifier).
- Grouped calls still reduce host dialogs: the owner sees three approvals for an
  image (not five) and two for an album.
- Per-call payload size stays bounded (media pair ≤ ~10.5 MiB, entity ≤ 256 KiB,
  catalog ≤ 2 × 1 MiB), well inside Hub/Core limits.

This is recorded here because the task explicitly forbids choosing from memory.

## 3. Owner decision — Studio navigation

Main navigation is unchanged: **HOME / BLOG / VIDEOS / GALLERY / ABOUT /
CONTACT**. **STUDIO is appended as the last item only when `capability ===
'owner'`.**

Behaviour:

- visitor → no Studio
- unauthenticated / unknown → no Studio
- authenticated-no-name → no Studio
- authenticated non-owner → no Studio
- permission denied / error → no Studio
- positively verified owner → Studio visible **after Contact**

Additional constraints implemented:

- Rendering navigation **never** calls `GET_USER_ACCOUNT`; the nav only reads the
  capability the explicit `/studio` flow established.
- Public browsing stays permission-free; there is no automatic account request on
  ordinary startup.
- The normal first owner entry remains `/studio` → Enter owner mode → capability
  verified → Studio appears for that active SPA session; sign-out removes it.

Implementation: `ownerNavItems` in `src/app/config/siteConfig.ts`, exported via
`src/app/config/navigation.ts`, consumed in `src/components/layout/SiteNav.tsx`.
The existing `iffinland/iffi-vaba-mees-QORTAL` owner/admin navigation UX was only
consulted as a reference for behaviour; no deprecated pattern was copied and no
authority rule was weakened.

## 4. Gallery UI

- `GalleryPage` renders `<GalleryOwnerPanel>` (lazy) **only** when `isOwner`, so
  visitors get no owner affordance in the DOM at all — nothing disabled.
- `GalleryOwnerPanel` is the single lazy boundary for the whole write path. It
  offers `Add image` and `Create album` and states the publishing name and the
  host-fee/approval expectation.
- `GalleryImageModal` (final contract, not a generic dialog): image file, live
  local preview, dimensions, title, description, album (from the loaded catalog
  listing, optional), categories, tags, language. It shows a "Prepared for
  upload" summary (source vs. output dimensions/sizes, notices, warnings),
  truthful step progress, and a result panel. Validation covers missing file,
  file error, empty title, title/description caps and language.
- `GalleryAlbumModal`: title, description, categories, tags, language;
  `coverThumbnail: null` (no separate upload required to create an album).
- `Modal` (`src/components/overlay/Modal.tsx`): `role="dialog"` with
  `aria-modal` + labelled heading and description, focus moved in and restored on
  close, Tab/Shift+Tab trap, background scroll lock, backdrop pointer blocking,
  and Escape closing **only** while `canClose` (never during an in-flight
  submission). It is intentionally not exported from `components/common` so it
  stays in the lazy owner boundary.
- Taxonomy uses the existing loaded catalog taxonomy for suggestions via
  `TaxonomyInput`; no QDN request per keypress, and normalization goes through
  the existing taxonomy utilities.
- `StudioPage` keeps owner capability, host diagnostics and build provenance, and
  adds a `Manage Gallery` link plus non-interactive roadmap text for Blog/video.
  Gallery content can also be added from the Gallery page itself.

## 5. Media preprocessing rules

Central policy: `src/domain/galleryMedia.ts` (`GALLERY_MEDIA_POLICY`).

| Setting | Value |
| --- | --- |
| Accepted source formats | JPEG, PNG, WebP stills |
| Max source file | 25 MiB |
| Max decoded pixels | 40,000,000 |
| Max source edge | 12,000 px |
| Full web copy | longest edge 2400 px, WebP quality 0.85 |
| Thumbnail | longest edge 480 px, WebP quality 0.8 |
| Service caps enforced client-side | IMAGE 10 MiB, THUMBNAIL 500 KiB |

Pipeline (`src/services/imageProcessing.ts`, native browser APIs only — no image
library, no new dependency):

- Magic-byte sniffing (`sniffImageFormat`) so a renamed file cannot pass on its
  declared MIME string alone; a declared type must agree with the bytes.
- Decode with `createImageBitmap(file, { imageOrientation: 'from-image' })` (with
  a plain fallback), so EXIF-oriented photos are not silently rotated.
- Aspect ratio preserved by `planScale`; images are **never upscaled**.
- Re-encode via `<canvas>` + `toBlob`; EXIF and other metadata are dropped by
  re-encoding.
- The untouched source is kept only when no downscale happened, the declared type
  agrees, the file already fits the IMAGE cap, and re-encoding would not save at
  least 5 % — so an already-optimized small image is not made heavier or lossier.
- Output size is checked against the verified Core service caps before any write;
  a failure raises a typed `ImageProcessingError` and nothing is published.
- Format-fallback and downscale facts are reported to the owner as
  notices/warnings rather than hidden.

Rationale for WebP: the verified Core `IMAGE`/`THUMBNAIL` services accept any
bytes (extension/validation is not restricted for these services), and `q-tube`
and modern Hub flows already serve WebP. WebP at q0.85 in the 1500–2400 px range
is visually close to the source at roughly a third of the JPEG size, which
directly reduces QDN weight and publication fee. The owner sees the resulting
dimensions/size before publishing. Values are centrally configurable so the owner
can retune after real-host validation.

## 6. Identifiers

- Item entity: `saw_img_<id12>` (`DOCUMENT`)
- Album entity: `saw_album_<id12>` (`DOCUMENT`)
- Original image media: `saw_img_media_<id12>` (`IMAGE`)
- Thumbnail: `saw_img_thumb_<id12>` (`THUMBNAIL`)

`id12` is exactly 12 lowercase base36 characters generated from
`crypto.getRandomValues` with rejection sampling (no modulo bias), with a bounded
collision check/retry against the catalog and an exact-resource lookup.
`Date.now`, `Math.random` and title slugs are not used for identity. Media and
thumbnail identifiers are deterministically coupled to the item id (and the
entity's `media`/`thumbnail` references must reproduce them).

## 7. Entity / album contracts

Gallery item `DOCUMENT` payload (unchanged contract, `schemaVersion: 1`): `title`,
`description`, `albumId | null`, `media` (explicit `service`/`name`/`identifier`/
`mimeType`), `thumbnail` (same shape, nullable), `width`, `height`, `categories`,
`tags`, `language`. No binary image data is embedded in the `DOCUMENT` entity.

Album payload: `title`, `description`, `coverThumbnail` (initially `null`),
`categories`, `tags`, `language`.

Both envelopes are validated with the existing `validateEntityPayload` (with
`expectedKind`) before any write; the entity `publisher` field is informational
and is never treated as authority (authority is resource name + verified current
name ownership). Both are exercised by tests that decode the published `data64`
and run it through the existing runtime validator.

## 8. Write orchestration

Centralized, with React components never calling `qortalRequest`:

- `src/qortal/publish.ts` — verified host write mechanics
  (`PUBLISH_QDN_RESOURCE` / `PUBLISH_MULTIPLE_QDN_RESOURCES`), the `PublishPort`
  boundary, timeouts, and parsing of `unsuccessfulPublishes` into a typed
  `PublishAttempt` (`submitted` / `partial` / `ambiguous` / `failed`). It is
  deliberately **not** re-exported from `qortal/index.ts`.
- `src/services/galleryPublishService.ts` — Shadow Archives Gallery semantics:
  authority gate, ordering, progress, results, cache invalidation and
  verification. Imported only from the lazy owner boundary.

Authority gate for a Gallery write (all required):

1. `environment.bridgeAvailable && isHosted && !isProxy` (real Qortal host);
2. account permission explicitly granted (`capability === 'owner'`);
3. `capability === 'owner'` (positively verified, never optimistic);
4. a connected account;
5. `publisherName` derived from `_qdnName` and equal to the environment name.

Then, **immediately before every write stage**, `assertAuthorityFresh` re-reads
`GET_NAME_DATA` and requires the current name owner to equal the connected
account address. A name transfer, an ownership lookup failure, or a missing
owner fails closed with a typed `GalleryPublishError` and no write. There is no
primary-name fallback, no other owned name, no hardcoded address and no bypass.
Content is always published under the actual app publishing name.

Timeout policy: single resource 60 min (host default); grouped
`max(30 min per resource) + 60 s` buffer so the host's own timeout surfaces
first. A timeout produces `ambiguous`, which is **never** retried automatically.

## 9. Catalog bootstrap and update

- Entity is authoritative; catalog is derived and never proves ownership.
- Partition family tokens match the read pipeline: `saw_cat_img_p000`,
  `saw_cat_album_p000`, manifest `saw_cat_manifest`.
- **First-catalog bootstrap.** A missing manifest is not an error: the writer
  constructs the first valid partition (`partition: 0`) and manifest
  (`catalogVersion: 1`) from the existing approved contract and publishes them
  after the entity.
- **Merge.** Existing partitions of the type are read, the target partition is
  chosen (or a new one created when the last is full), the entry is upserted by
  identifier so a retry cannot duplicate or move an entry, the manifest
  `catalogVersion` increments, and the manifest taxonomy merges app labels.
- **Bounded growth.** Partition capacity is 200 entries / ~256 KiB; a new
  partition is started when full, and the manifest validator caps partitions at
  64. If a manifest can no longer be planned validly, the index write is skipped
  and reported, never fatal (see below). Beyond that scale a catalog rebuild is
  required — documented, not a Phase 3A blocker.
- **Never blocks content.** If the catalog is unreadable, invalid, partial, or
  cannot be planned/validated, the derived index is left untouched, the entity is
  still published, and the UI reports "Content published, index update
  incomplete" (or the unconfirmed variant for an index timeout) — never a full
  content failure, and never a fabricated success.
- **Validation.** Planned partition/manifest payloads are validated with the same
  runtime validators the read path uses before any catalog bytes are published.

## 10. Partial / timeout handling

| Situation | Reported status | UI truth |
| --- | --- | --- |
| All stages submitted | `published` | "Published." with availability confirmed/pending from a bounded read |
| Grouped stage partially published | `partial` | failures listed per service/identifier; entity not written without its media |
| A stage timed out | `ambiguous` | result uncertain; **no automatic retry**; Verify offered; retry reuses the same identity |
| Entity submitted, catalog failed/timed out | `index-incomplete` | "Content published, index update incomplete/unconfirmed" |
| Nothing acknowledged | `failed` | nothing claimed to exist |

Progress is reported as concrete monotonic steps matching the real plan
(`preparing-media` → per stage `checking-authority` → `awaiting-approval` →
`publishing-media` / `publishing-metadata` / `updating-index` → `confirming`),
with the step total derived from whether an index write is possible. 100 % is not
shown merely because a bridge call returned; `confirming` is a separate step.

Post-publication verification uses only bounded reads (15 s), never a write, and
does not require `READY`. When the intended payload is available it compares the
**served payload** to the intended one (`contentMatches`), which is stronger than
a status check. Results distinguish submitted / confirmed-available / index
updated / verification pending.

## 11. Cache refresh

After a publication (successful or partial) the entity cache entry and the
affected catalog manifest/partition entries are invalidated, then the shared
`ContentProvider` refresh is triggered so newly published Gallery content appears
without a full app reload. No unverified optimistic entity is appended to UI
state — the refresh re-reads through the normal pipeline. A cache-invalidation
failure never turns a successful publication into a reported failure.

The newly published item renders through the **same production read path** as
older content; there is no owner-only rendering path. `/gallery/album/:id` and
`/gallery/item/:id` continue to work, and album membership keeps the existing
bare-stable-id semantics and alias normalization.

## 12. Tests

New/updated test files (all passing):

| File | Tests | Focus |
| --- | --- | --- |
| `src/components/layout/SiteNav.owner.test.tsx` | 8 | public nav items/order; no Studio for visitor/non-owner/no-name/denied; owner gets Studio last after Contact; reset removes it; nav issuance never calls `GET_USER_ACCOUNT` |
| `src/services/galleryPublishService.test.ts` | 31 | authority gate + fresh re-check + transfer block + fail-closed; staged order; entity/album envelope validation; metadata caps; stable id + media coupling; catalog bootstrap/merge/no-duplicate/rollover; catalog-unreadable and catalog-planning-failure degradation; partial failure; ambiguous timeout not retried (media + entity); index-only failure = partial success; cache invalidation; bounded verification; **round-trip of the published entity + catalog through the unchanged read pipeline** (`loadCatalog` + `loadEntityDetail`) |
| `src/services/imageProcessing.test.ts` | 18 | magic-byte sniffing; size/type/mismatch/dimension/service-limit boundaries; no upscaling; bounded thumbnail; truthful warnings |
| `src/domain/identifiers.test.ts` (extended) | +8 | stable id format/rejection sampling/crypto failure; bounded unique-id retry; media/thumbnail identifier derivation and parsing |
| `src/features/gallery/owner/GalleryOwnerPanel.test.tsx` | 7 | owner control hidden from visitors; owner sees both controls; Escape dismisses the labelled modal; cancel performs no write; **publish only after explicit Publish**; ambiguous timeout offers Verify and no auto-retry; unsupported file rejected before write |

## 13. Validation results

| Command | Result |
| --- | --- |
| `npm run lint` | PASS |
| `npm run typecheck` | PASS |
| `npm test` | PASS — **36 files / 375 tests** (303 baseline + 72 new) |
| `npm run build` | PASS |
| `npm run format:check` | PASS |
| `git diff --check` | clean |
| `bash -n tools/validate-workspace.sh` | PASS |
| `bash tools/validate-workspace.sh` | PASS (5 pre-existing warnings for human review; none Phase 3A) |

Local production browser smoke test (headless Chrome via Playwright against
`vite preview` of the built `dist/`, 15/15 checks):

- Visitor: nav is exactly Home/Blog/Videos/Gallery/About/Contact; no Studio;
  Gallery renders read-only with no owner panel and no Add image; no uncaught
  errors.
- Simulated owner (host globals + bridge injected before app load): Studio absent
  before entering owner mode; public load issues **0** `GET_USER_ACCOUNT`; after
  owner mode Studio appears **last, after Contact**; Gallery shows Add image and
  Create album; the publish dialog is labelled + modal; opening it issues **0**
  writes; Escape dismisses it; no uncaught errors.

Test-environment note: `src/test/setup.ts` gained a `Blob.prototype.arrayBuffer`
polyfill because jsdom lacks it and the real browser pipeline depends on it. This
lets tests exercise production code instead of mocking the pipeline away.

## 14. Build sizes / chunks

Production build (`npm run build`):

| Chunk | Raw | Gzip |
| --- | --- | --- |
| `index-*.js` (entry / visitor startup) | 384.37 kB | 121.08 kB |
| `GalleryOwnerPanel-*.js` (lazy owner boundary) | 44.36 kB | 13.18 kB |
| `GalleryOwnerPanel-*.css` (owner styles) | 5.91 kB | 1.19 kB |
| `StudioPage-*.js` | 7.06 kB | 2.35 kB |
| `GalleryPage-*.js` | 1.54 kB | 0.67 kB |
| `index-*.css` (shared) | 25.76 kB | 5.01 kB |

Baseline entry was 383.08 kB raw / 120.46 kB gzip → **+1.29 kB raw / +0.62 kB
gzip** (the owner nav item + config only).

Startup-bundle verification (string presence in the built entry chunk):
`PUBLISH_QDN_RESOURCE` 0, `PUBLISH_MULTIPLE` 0, `createImageBitmap` 0, `data64` 0,
`toBlob` 0, `ImageProcessing` 0 — all present (1 each) only in
`GalleryOwnerPanel-*.js`. `dist/index.html` references only the entry chunk. The
public visitor startup therefore loads no image-processing code, publish service,
write bridge or modal implementation.

## 15. Adversarial self-audit

| # | Check | Result | Class |
| --- | --- | --- | --- |
| 1 | Studio visible to visitor | Not possible (capability-gated; smoke + tests) | OK |
| 2 | Studio visibility triggers auth | No — nav never calls auth; public load issues 0 `GET_USER_ACCOUNT` | OK |
| 3 | Non-owner gets Studio | Blocked; tested for non-owner / no-name / denied | OK |
| 4 | Publisher name hardcoded for authority | No — derived from `_qdnName`; only tests hardcode | OK |
| 5 | Writes use another owned/primary name | No — `name` is always `environment.publisherName` | OK |
| 6 | Ownership not rechecked before write | Rechecked via `GET_NAME_DATA` before **every** stage | OK |
| 7 | UI calls `qortalRequest` directly | No — only `src/qortal/*` wrappers; grep-verified | OK |
| 8 | Media data embedded in DOCUMENT | No — entity holds explicit QDN references only | OK |
| 9 | Catalog treated as authoritative | No — entity written first; catalog derived | OK |
| 10 | Catalog required before first content | No — missing catalog bootstraps; tested | OK |
| 11 | Catalog failure shown as content failure | No — reported as index-incomplete/partial success | OK |
| 12 | Unbounded catalog growth | Bounded (200 entries/partition, 64 partitions); beyond that the index is skipped and a rebuild required — **documented, not a blocker** | LOW |
| 13 | Duplicate ids | Bounded collision retry + identifier upsert; tested | OK |
| 14 | Bad file accepted by MIME string only | No — magic-byte sniff + declared-type agreement | OK |
| 15 | Unbounded image dimensions/memory | Bounded by bytes/pixels/edge before decode | OK |
| 16 | Automatic retry after ambiguous timeout | None; Verify is an explicit action; tested | OK |
| 17 | Fake success before Qortal approval | No — result derives from host-returned submissions + bounded read | OK |
| 18 | Permanent optimistic content after failed write | No — refresh re-reads; nothing fake is appended | OK |
| 19 | Gallery publisher in visitor startup bundle | No — verified absent from the entry chunk | OK |
| 20 | Blog/Video interoperability work started | No — untouched | OK |
| 21 | Parchment baseline changed | No — `owner.css` uses existing tokens and contains no literal colours; `src/styles/**` untouched | OK |
| 22 | Catalog planning failure blocks content | **Found and fixed** — a catalog plan/validate or content-hash failure now degrades to a skipped index with a truthful message instead of aborting the publish (test added) | MEDIUM → fixed |

No unresolved BLOCKER or HIGH remains. The one MEDIUM found during the audit was
fixed in this phase (item 22) with a regression test.

Known limitations recorded for the owner: the catalog partition/manifest growth
ceiling (item 12) and the fact that a Gallery item's `IMAGE`/`THUMBNAIL`
resources are published before the entity, so a failed entity stage can leave
orphaned media (harmless, discoverable only by exact identifier, and never
referenced by any entity).

## 16. Files changed

New:

- `src/qortal/publish.ts` — verified write mechanics / `PublishPort`
- `src/services/galleryPublishService.ts`, `src/services/catalogWriter.ts`,
  `src/services/imageProcessing.ts`, `src/services/base64.ts`
- `src/domain/galleryMedia.ts`
- `src/components/overlay/Modal.tsx`
- `src/features/gallery/owner/GalleryOwnerPanel.tsx`,
  `GalleryImageModal.tsx`, `GalleryAlbumModal.tsx`, `TaxonomyInput.tsx`,
  `publishFeedback.tsx`, `owner.css`
- Tests: `src/components/layout/SiteNav.owner.test.tsx`,
  `src/services/galleryPublishService.test.ts`,
  `src/services/imageProcessing.test.ts`,
  `src/features/gallery/owner/GalleryOwnerPanel.test.tsx`

Modified:

- `src/app/config/siteConfig.ts`, `src/app/config/navigation.ts`,
  `src/components/layout/SiteNav.tsx` (owner nav item)
- `src/features/gallery/GalleryPage.tsx` (lazy owner panel),
  `src/features/owner/StudioPage.tsx` (Manage Gallery + roadmap text)
- `src/qortal/bridge.ts` (retain raw rejection detail for partial-failure parsing)
- `src/qortal/actions.ts` (write action names)
- `src/domain/identifiers.ts` (stable id generation + media identifiers)
- `src/services/catalogRepository.ts`, `src/services/contentRepository.ts`
  (cache invalidation helpers)
- `src/domain/identifiers.test.ts` (extended), `src/test/setup.ts` (Blob polyfill)

No dependency was added. No MUI, no `qapp-core` root import, no image library.

## 17. Workspace changes

- `projects/shadow-archives-webportal.md` — added the factual Phase 3A
  current-state block and recorded the Studio navigation owner decision; marked
  the previously open Studio-navigation question as decided.

## 18. Git status at handoff

- Application repo (`3bd9173` baseline): all Phase 3A changes present as modified
  and untracked files; **not committed, not pushed, not tagged**.
- Workspace repo (`8af255c` baseline): `projects/shadow-archives-webportal.md`
  modified, this new report added; the pre-existing untracked owner report
  `docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md`
  was left untouched. **Not committed, not pushed, not tagged.**
- No unexpected owner work was overwritten, reverted or deleted.

## 19. Explicit no-write statement

The implementation agent performed **no live QDN write and no real transaction**.
No `PUBLISH_QDN_RESOURCE` / `PUBLISH_MULTIPLE_QDN_RESOURCES` call was ever issued
against mainnet or any node. All write-orchestration testing used injected fakes
and mocked browsers. `PUBLISH_*` calls were exercised only against a local mock
`window.qortalRequest` inside the test process and a local `vite preview` server,
never against a Qortal host.

## 20. Owner next steps (not performed here)

1. Commit and push the Phase 3A changes.
2. Build and package the APP.
3. Update the Shadow Archives APP resource manually in Qortal.
4. Enter Owner mode and publish one real Gallery item to validate the runtime.
5. Report back the real-host result, including exact `_qdn*` values from the
   Studio diagnostics block.

Blog and Video publishing research must not start until the owner authorizes a
separate bounded task.
