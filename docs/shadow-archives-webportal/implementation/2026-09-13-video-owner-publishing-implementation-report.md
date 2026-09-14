# Shadow Archives Webportal — Owner Video Publishing with native Q-Tube interoperability

> **Subsequent owner acceptance — 2026-09-13: OWNER-RUNTIME PASS.** Gallery,
> Video/Q-Tube, Blog/SubWire and optional Quitter announcement are accepted.
> This supersedes earlier FUTURE / NOT VERIFIED or owner-validation-pending
> statements for those surfaces only. Original observations below remain a dated
> historical record; no new runtime test is claimed by this update.
> See [checkpoint and pinned evidence](../handoffs/2026-09-13-owner-runtime-checkpoint.md).
> Implementation executor: DeepSeek; acceptance: owner; update writer: Codex Local.


**Date:** 2026-09-13
**Type:** feature vertical implementation (Video owner publishing + cross-app interoperability)
**Executing agent:** DeepSeek
**Agent identity correction (2026-09-13):** this task was executed by **DeepSeek**
(the autonomous implementation agent). The earlier `Codex` attribution was
incorrect — it was inferred from the orchestration role/CLI profile rather than
from the actual executor — and is corrected above. This work must not be
attributed to Codex.
**Application:** `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
**Project context:** `projects/shadow-archives-webportal.md`
**Companion validation report:**
`docs/shadow-archives-webportal/validation/2026-09-13-video-qtube-contract-live-read-only-validation.md`

**Owner authorization:** inspect/edit the local project; run tests/lint/build;
inspect and update clean reference clones under orchestration rules; read-only
Qortal nodes; inspect current public Q-Tube QDN resources.

**Not authorized / not performed:** live QDN publication, any transaction, any
modification of Q-Tube, deploy/release, commit, branch change, push, tag, merge.
No Q-Tube source was imported or vendored. No Shadow Archives video exists on
QDN as a result of this work.

---

## 1. Objective and exit criterion

**Objective.** One Shadow Archives owner workflow publishes a video to QDN so
that (a) Shadow Archives lists, opens and plays it, and (b) the *current* Q-Tube
application discovers and displays the same publication naturally from QDN —
without importing Q-Tube, without a runtime dependency on Q-Tube, and without a
fake integration.

**Exit criterion.** owner → open the Video publish modal → select video +
required metadata/thumbnail → publish → exact QDN resources verified → the
Shadow Archives Videos listing discovers it → detail/player loads it → reload
persists → the current Q-Tube discovery contract can discover the same
publication. The last condition is demonstrated from source + read-only live
evidence; the single remaining step is the owner's own authorized live
publication.

---

## 2. Verified Q-Tube publication/discovery contract

Full command outputs and raw payloads: companion validation report. Summary of
what was verified against current source and live read-only QDN data on
2026-09-13:

**Pins.** `Qortal/q-tube` `main` `68c3ea706c4ab110ffa44a7f55f8e09bdf7e85ff`,
`Qortal/Subwire` `master` `a933a6c44d60db19cd219408e36c747aebcce994` (both
re-checked as upstream heads), Qortal Core `6.1.9` / `108bf191` (live node
reported `qortal-6.1.9-108bf19`), Qortal Hub `12a573b2`, `qapp-core` `0f9d6ac5`.

**Publication.** Q-Tube writes two resources per video
(`useVideoPublishingWorkflow.tsx`):

| Purpose | Service | Identifier | Notes |
| --- | --- | --- | --- |
| media bytes | `VIDEO` | `qtube_vid_<slug30>_<id>` | `tag1 = 'qtube_vid_'`, `filename = <original name>` |
| metadata | `DOCUMENT` | `<media identifier>_metadata` | `filename = 'video_metadata.json'`, `tag1 = 'qtube_vid_'`, Core `title` = `title.slice(0,50)`, Core `description` = `**category:<id>;subcategory:<sub>;code:<code>**` + `fullDescription.slice(0,150)` |

The metadata body is `VideoMetadata`: `title, version(1), fullDescription,
htmlDescription, videoImage (data URL), videoReference{name,identifier,service},
extracts[], commentsId, category, subcategory, code, videoType, filename,
fileSize, duration`. A live payload was fetched and matched field for field.

**Discovery.** `SEARCH_QDN_RESOURCES { service: 'DOCUMENT', identifier:
'qtube_vid_', mode: 'ALL', reverse: true, limit: 20 }` (`Home.tsx`,
`Home/Components/VideoListComponentLevel.tsx`, `Search.tsx`). Verified
empirically: the `identifier` value is matched as a **substring** (Q-Tube sets no
`prefix` flag), and `mode: 'ALL'` is required — Core's default `LATEST` returns
one resource per `(name, service)`. Category tabs add
`description: 'category:<id>;'`. **No index/list resource and no playlist is
required** for a video to be discovered; playlists are discovered separately from
the `PLAYLIST` service and are irrelevant to video visibility.

**Display gate.** `src/utils/checkStructure.ts` `isValidVideoMetadata` requires
`title`, a `videoReference` with a non-empty `name`/`identifier`/`service` drawn
from the Qortal service set, and a non-empty `filename`; `duration`/`fileSize`
are optional. `src/pages/Home/Components/VideoList.tsx` drops every discovered
payload that fails that gate, so it is the real display condition.

**Playback.** `VideoContent-State.ts` resolves the metadata `DOCUMENT` by exact
`name`+`identifier` and plays `videoReference` through
`/arbitrary/<service>/<name>/<identifier>`. Because the media identifier is the
metadata identifier minus `_metadata` (`Qortal/Subwire`
`src/utils/articleQdn.ts` encodes exactly that), a compatible publisher must put
the bytes at the Q-Tube media coordinate — publishing them anywhere else would
require either a second copy or a Q-Tube-side change.

**Hover preview.** `VideoCardImageContainer` iterates `extracts` with
`index % extracts.length`; an empty array blanks the card on hover. A
single-element array is safe. (Source-verified; this is why the adapter seeds
`extracts` with the poster frame.)

---

## 3. Architecture chosen and why

```
Video entity (Shadow Archives, canonical)
  → Shadow Archives catalog/listing + detail/player
  → QDN media resources (published once)
  → Q-Tube-compatible adapter (derived artifact, one module)
```

**Boundary.** Every Q-Tube-specific fact (identifier family, metadata schema,
core metadata mirror, category mirror, discovery query, validity gate) lives in
exactly one module, `src/services/qtubeVideoContract.ts`. No Q-Tube source is
imported, vendored or bundled, and no Shadow Archives read path consults Q-Tube
artifacts: Shadow Archives discovery reads only its own `saw_vid_` namespace and
its own catalog. A future Q-Tube contract change is a one-file change plus a
re-run of the pinned-source check.

**Why the media resource lives in the Q-Tube family.** The ecosystem convention
(used by Q-Tube and Subwire) is that the media identifier is the metadata
identifier minus `_metadata`. Publishing the bytes once at
`qtube_vid_<id>` therefore satisfies Q-Tube's `videoReference` *and* keeps the
Shadow Archives entity pointing at a single authoritative resource — no double
publication, no second copy of large media, no Q-Tube change.

**Why the Shadow Archives entity is separate.** The canonical entity
(`saw_vid_<id>`) carries the app's own title/description/taxonomy/language/media
reference and is what the app's catalog, listing cards, detail route and player
resolve. The Q-Tube artifact is derived and non-authoritative: if it is missing
or rejected, Shadow Archives still works and reports the difference truthfully.

**Why stages, not one call.** The host repeats an approval dialog per publish
call (`PUBLISH_MULTIPLE_QDN_RESOURCES` groups resources but shows one summary
dialog and can partially fail), so grouping is used where the resources share a
failure meaning, and the derived index is isolated last so an unusable index can
never block, roll back or corrupt the authoritative content write.

**Reuse of established Shadow Archives infrastructure (not a Gallery copy):**
`services/ownerAuthority.ts` (extracted from Gallery) for the two-step authority
gate, `services/catalogPublishSupport.ts` (extracted from Gallery) for
read/plan/write of the derived index, `services/imageProcessing.ts`
`processPosterImage` for a bounded single-image poster pipeline,
`domain/identifiers.ts` for the app id/identifier families, `qortal/publish.ts`
(extended, not duplicated) for the write transport, `features/owner/owner.css`
and `features/owner/TaxonomyInput.tsx` (moved to a shared owner location) for the
owner surface. The Video service, modal, feedback view and Q-Tube adapter are
new code with Video-specific semantics.

---

## 4. QDN resource model

For one video with stable id `<id12>` (12 chars of base36, same id family as the
rest of the app):

| Resource | Service | Identifier | Authority |
| --- | --- | --- | --- |
| Shadow Archives entity | `DOCUMENT` | `saw_vid_<id>` | authoritative |
| Poster | `THUMBNAIL` | `saw_vid_thumb_<id>` | authoritative for the app |
| Media bytes | `VIDEO` | `qtube_vid_<id>` | published once, referenced by both |
| Q-Tube metadata | `DOCUMENT` | `qtube_vid_<id>_metadata` | derived |
| Derived Videos index | `DOCUMENT` | `saw_cat_vid_p###` + `saw_cat_manifest` | derived, skippable |

Write order and meaning:

1. **media + poster** (one grouped call) — the entity must never exist without
   the bytes it references.
2. **entity + Q-Tube metadata** (one grouped call) — the authoritative record and
   the interoperability artifact; a host-reported partial result is surfaced
   per resource.
3. **derived index** (one grouped call) — skipped and reported when the existing
   index cannot be safely rewritten; the bounded `saw_vid_` prefix scan covers
   discovery in that case.

Payload encodings: the media is sent to the host as a `File` (the host encodes
it; the app never materialises a second base64 copy of a multi-GB video), all
other payloads as `data64`. `tag1 = 'qtube_vid_'` is carried as
`tags: ['qtube_vid_']` on both the media and the Q-Tube metadata resource
(source-verified Hub mapping `tags[i] → tag{i+1}`).

Field mapping into the Q-Tube artifact: `title` = entity title (Core metadata
mirrors the first 50 chars), `version: 1`, `fullDescription` = plain-text
description, `htmlDescription` = plain text fallback, `videoImage` = poster data
URL, `extracts` = `[poster data URL]`, `commentsId` =
`qtube_vid__cm_<code>`, `category` = mirrored numeric Q-Tube category id,
`subcategory: ''`, `code` = 5 chars of the app id, `videoType` = declared video
type (`video/mp4` fallback), `filename` = sanitised original file name,
`fileSize`, `duration`.

---

## 5. Partial-failure design

- **Never retried automatically.** Each stage issues exactly one publish call;
  a timeout is `ambiguous`, never re-submitted. Tests assert one call per stage.
- **Never reported better than the evidence.** Result statuses:
  `published` | `index-incomplete` | `partial` | `ambiguous` | `failed`.
  `published` requires every resource submitted, the entity confirmed by a
  bounded read when the read succeeds, and the index updated; otherwise the
  message says exactly what is unconfirmed.
- **Exact identity always returned.** Every result carries
  `entityIdentifier`, `videoIdentifier`, `metadataIdentifier`,
  `thumbnailIdentifier`, `id`, `publisherName`, per-resource submissions and
  failures, and the exact entity payload — enough to verify or recover without
  guessing.
- **Retry reuses identity.** The modal keeps the returned id across attempts, so
  re-publishing after an ambiguous/partial outcome overwrites the same
  coordinates instead of minting a duplicate video.
- **Fail closed before any write.** Input validation, poster encoding, payload
  size caps and the Q-Tube validity self-check all run *before* stage 1, so a
  rejected payload can never leave a half-published video.
- **Distinct failure codes.** `not-hosted`, `not-owner`, `authority-unresolved`,
  `authority-changed`, `invalid-input`, `poster-processing`,
  `id-generation-failed`, `payload-too-large`, `unexpected`.
- **Bounded, read-only Verify.** `verifyVideoPublication` re-reads the four
  resources, compares the served entity payload, runs Q-Tube's own validity gate
  on the served artifact, checks that `videoReference` points at this
  publication's media, and replays Q-Tube's discovery query — read-only, and it
  reports `null`/`unknown` rather than fabricating a result.

---

## 6. Files changed

**New — Q-Tube adapter / services / domain**

| File | Lines | Purpose |
| --- | --- | --- |
| `src/services/qtubeVideoContract.ts` | 407 | The only Q-Tube-aware module: identifier family, metadata schema + builder, Q-Tube validity gate mirror, Core metadata description mirror, category mirror, discovery request, parsers. Documents the pins. |
| `src/services/qtubeVideoContract.test.ts` | 287 | Gate parity, identifier round-trips/rejections, category mapping, live-shape regression. |
| `src/services/videoPublishService.ts` | 1069 | Staged publication, authority gates, partial/ambiguous reporting, readback verification. |
| `src/services/videoPublishService.test.ts` | 980 | 24 tests: authority, input, staged writes, exact identifiers, payload validity, partial/ambiguous/index-failure, verify paths, catalog round-trip. |
| `src/services/videoMetadataProbe.ts` | 137 | Bounded injectable `<video>` metadata probe (duration/intrinsic size). |
| `src/services/videoMetadataProbe.test.ts` | 136 | Success/error/timeout/single-settle. |
| `src/services/catalogPublishSupport.ts` | 212 | Extracted Gallery+Video shared derived-index read/plan/write support. |
| `src/services/ownerAuthority.ts` | 116 | Extracted Gallery+Video shared owner-write authority gate. |
| `src/domain/videoMedia.ts` | 128 | Video/poster policy: container allow/deny, 2 GB host ceiling mirror, 500 KiB `THUMBNAIL` cap mirror, duration formatting. |

**New — Video owner UI (lazy)**

| File | Lines | Purpose |
| --- | --- | --- |
| `src/features/videos/owner/VideoOwnerPanel.tsx` | 56 | Owner-only lazy boundary (renders `null` for non-owners). |
| `src/features/videos/owner/VideoPublishModal.tsx` | 531 | The single owner workflow: video + poster selection, duration probe/manual entry, taxonomy, validation, staged publish, Verify, truthful outcome. |
| `src/features/videos/owner/videoPublishFeedback.tsx` | 228 | Progress list and outcome view (exact identifiers, failures, verify detail incl. Q-Tube gate/reference/discovery). |
| `src/features/videos/owner/VideoOwnerPanel.test.tsx` | 333 | 7 UI tests through the real router/bridge: visitor isolation, dialog semantics, cancel, validation, full publish call order/shape, container rejection. |
| `src/features/videos/VideoDetailPage.test.tsx` | 108 | Detail route renders a native player bound to the stored media and never fetches video bytes. |

**Modified**

| File | Change |
| --- | --- |
| `src/features/videos/VideosPage.tsx` | Lazy `VideoOwnerPanel` boundary (owner only) + truthful lead copy. |
| `src/features/videos/VideoDetailPage.tsx` | Native `<video controls preload="metadata" playsInline>` player with poster, duration, media-resource provenance; no autoplay; no bytes on listing. |
| `src/features/owner/StudioPage.tsx` | Corrected owner-mode copy (video publishing is available), added a `Manage Videos` link next to `Manage Gallery`. |
| `src/qortal/publish.ts` | `PublishResourceInput` now takes exactly one of `data64`/`file`; the `file` field is forwarded to the host; params are built inside the async body. |
| `src/services/imageProcessing.ts` | Added `processPosterImage` + `PosterImagePolicy`/`PosterImageResult`: bounded 3-step encode ladder, fail-closed byte cap, `dataUrl` output for cross-app metadata. |
| `src/services/galleryPublishService.ts` | Refactored onto `catalogPublishSupport` + `ownerAuthority` (behaviour preserved; 35 Gallery tests still pass); re-exports `OwnerWriteContext`. |
| `src/services/galleryPublishService.test.ts` | Test helper for the now-optional `data64` field. |
| `src/services/contentRepository.ts` | Listing hydration now also covers `video` entities (poster + duration), still never fetching media bytes. |
| `src/services/contentRepository.test.ts` | +1 test: a video listing is hydrated from its authoritative entity in the bounded-discovery path. |
| `src/services/catalogWriter.ts` | `catalogEntryFromVideoEntry` (duration populated; width/height/albumId null). |
| `src/domain/catalog.ts` | `listingFromVideoEntry` (video listings are 16:9 and carry the duration badge). |
| `src/domain/identifiers.ts` | Video poster identifier family (`buildVideoThumbnailIdentifier` / parser). |
| `src/domain/index.ts` | Exports for the above. |
| `src/styles/content.css` | `.sa-video-player` (public detail player styles). |
| `README.md` | New "Video publishing and Q-Tube interoperability" section recording the verified contract, resource model and partial-failure semantics. |

**Moved (shared owner surface; `git mv` so history is preserved)**

| From | To |
| --- | --- |
| `src/features/gallery/owner/TaxonomyInput.tsx` | `src/features/owner/TaxonomyInput.tsx` (+ `Gallery*Modal` import paths, + `.sa-preview__video` in `owner.css`) |
| `src/features/gallery/owner/owner.css` | `src/features/owner/owner.css` (+ `GalleryOwnerPanel` import path) |

**Untouched user-owned file:** the pre-existing untracked `AGENTS.md` at the repo
root was neither read-for-edit nor modified.

---

## 7. Tests and build results

| Check | Command | Result |
| --- | --- | --- |
| Type check | `npx tsc -b` | clean |
| Lint | `npx eslint .` | clean |
| Formatting | `npx prettier --check` on every changed file | clean |
| Whitespace | `git diff --check` | clean |
| Unit/UI tests | `npm test` | **502 passed / 46 files** (re-run after the final edit) |
| Production build | `npm run build` | clean (`tsc -b && vite build`, 170 modules) |

New coverage added by this work: 21 (Q-Tube contract) + 24 (publish service) + 5
(probe) + 7 (owner panel UI, driving the real router, capability gate, bridge and
modal) + 1 (video detail player) + 1 (video listing hydration) = **59 tests**.
The 7 UI tests are the end-to-end owner flow in jsdom: they assert the exact
publish-call sequence (`media+poster → entity+metadata → index`), that the media
payload is sent as raw `file` bytes with the `qtube_vid_<id>` identifier and the
poster as a `THUMBNAIL`, that nothing is written before the owner presses
Publish, and that cancelling writes nothing.

**Bundle impact (visitor startup graph).** Production chunk comparison against
the previously packaged build of HEAD (`release/…-20260913.zip.manifest.json`,
entry `index-27bgAv3t.js`, 391,898 bytes):

- entry now `index-D0LUCL5E.js`, **392,678 bytes (+780 bytes, +0.2%)**. A byte
  comparison shows the delta is entirely Vite's `__vite__mapDeps` dynamic-import
  bookkeeping (hash renames plus one added shared chunk) and minifier identifier
  shifts — no application code was added to the entry.
- No video/owner/publish/Q-Tube-adapter symbol is present in the entry chunk
  (checked: `qtube_vid_`, `Add video`, `processPosterImage`, `probeVideoFile`,
  `sa-video-player`, `Owner video controls` → 0 occurrences; the pre-existing
  `qtube` match is the static `siteConfig.externalApps` entry).
- Owner and video code stays in lazy chunks: `VideoOwnerPanel-*.js` 30.5 kB,
  `owner-*.js` 20.6 kB (shared owner surface), `videoMedia-*.js` 1.3 kB,
  `VideoDetailPage-*.js` 2.7 kB, `VideosPage-*.js` 1.4 kB; the shared owner
  stylesheet `owner-*.css` 6.1 kB. Entry CSS `index-*.css` grew by ~200 bytes
  (the public `.sa-video-player` rule).

---

## 8. Adversarial self-audit

Audited against the exit criterion, the partial-failure requirement and the
authority boundary; every finding below was either remediated or is recorded as
a residual risk in §9.

| # | Finding | Severity | Action |
| --- | --- | --- | --- |
| 1 | `publishVideo` contained an unreachable `partial` branch (the live partial path already returns earlier), whose text claimed Shadow Archives "cannot list it until its entity metadata exists" — misleading when the *entity* succeeded and only the Q-Tube artifact failed. | HIGH (truthfulness) | **Remediated:** dead branch removed; the single live partial message now names the failed resource, states the retry reuses the identity ("no duplicate video is created"), and the test asserts the exact identifiers survive. |
| 2 | Could the media be published twice, or the app depend on Q-Tube? | BLOCKER if present | **Not present:** one `VIDEO` resource referenced by both records; Shadow Archives discovery reads only `saw_` identifiers; the Q-Tube adapter is one module with no Q-Tube import. |
| 3 | Could an ambiguous write be retried automatically (duplicate/double-fee)? | BLOCKER if present | **Not present:** one write per stage; tests assert `mediaStage` timeout ⇒ exactly 1 call, metadata timeout ⇒ exactly 2; the modal offers Verify, and Publish-again reuses the id. |
| 4 | Could a payload that is too large or fails Q-Tube's gate leave a partial publication? | HIGH | **Not present:** payload sizing, poster encoding and the `isValidQtubeVideoMetadata` self-check all execute before stage 1 (code order verified; `payload-too-large`/`poster-processing`/`invalid-input` all fail closed). |
| 5 | Does the owner surface leak into the visitor graph? | HIGH | **Not present:** dist-level verification (§7). |
| 6 | Does this work touch any user-owned change, or perform an unauthorized write? | BLOCKER if present | **Not present:** `AGENTS.md` untouched; no commit/branch/push; live node search shows 0 `saw_vid_` resources. |
| 7 | Is the `tags` → `tag1` and per-resource `file` transport assumption safe for a grouped publish? | HIGH | **Verified in pinned Hub source** (`publishMultipleQDNResources`: `tags[i] → tag{i+1}`; `resource.file → fileToBase64 → publishData`) and surfaced as a residual "live write not yet executed" risk in §9. |
| 8 | `extracts` with one frame vs Q-Tube's four. | MEDIUM | Deliberate and source-justified: an empty array blanks Q-Tube's hover card; a real multi-frame extraction would require decoding video frames in the browser. Recorded as a cosmetic difference in §9. |
| 9 | `commentsId` uses the 5-char `code` while Q-Tube uses its id suffix. | LOW | Same `qtube_vid__cm_<token>` shape, unique per publication, only a comments-namespace hint; documented in the adapter comments. |
| 10 | Video card has no intrinsic width/height (16:9 default). | LOW | `listingFromVideoEntry` intentionally omits dimensions so cards use the 16:9 default; the entity stores the media coordinate, not poster pixels. |

Unrelated observation (not introduced or touched by this work): one run of the
pre-existing `src/features/home/HomePage.data.test.tsx` failed an assertion under
heavy parallel load and passed on an immediate clean re-run (502/502). The file
is unmodified by this work.

---

## 9. Unresolved risks

1. **The live write itself is unproven.** No authorized live publication was
   performed, so the real host hop — a `File` surviving the app's
   `qortalRequest` → `parent.postMessage` structured clone into the Hub, the
   two-resource approval dialog, and a live node's search index returning a
   freshly published metadata resource — is source-verified but not executed.
   This is precisely what the single owner validation in §10 proves.
2. **Browser codec/container variance.** The policy accepts MP4/WebM/Ogg/
   QuickTime and rejects MKV/AVI/WMV/FLV/TS/M4V, and the probe reports when the
   browser cannot read a file's metadata. A container the browser cannot decode
   plays in neither Shadow Archives nor Q-Tube; the owner gets a truthful
   pre-publish signal but not a guarantee of playback on every client.
3. **Q-Tube hover preview depth.** Shadow Archives publishes one extract frame
   (the poster); native Q-Tube videos carry several. Cards still render and
   hover safely, with a single frame instead of a frame sequence.
4. **Search-index lag.** Immediately after publication a node may not yet return
   the new metadata resource from the discovery query; Verify says
   "not returned yet" with a lag note instead of claiming failure. Reload/retry
   resolves it.
5. **Upstream contract drift.** All Q-Tube facts are pinned to `68c3ea70`; a
   Q-Tube change requires re-running the pinned-source check (documented in the
   adapter header and README).
6. **Host size ceilings.** 2 GB for a local node (`MAX_SIZE_PUBLISH`) vs 500 MB
   when the Hub runs as a public gateway; a >500 MB video will be refused by the
   host at approval time on a public gateway.
7. **Poster is mandatory** in the workflow even though Q-Tube's gate treats
   `videoImage`/`extracts` as optional, because Q-Tube's listing card needs an
   image; this is a product decision, not a contract requirement.
8. **Derived index capacity/latency.** The catalog partition is capped
   (~200 entries / 256 KiB); beyond that the index write is skipped and reported
   and discovery falls back to the bounded prefix scan (pre-existing behaviour,
   unchanged).

**Recommendation (not performed, outside the authorized repo scope):** promote
`AI-Orchestration/skills/qortal/cross-app-video-publishing/SKILL.md` from
`candidate` and fold in the now-verified facts (gate, `mode: 'ALL'`, substring
identifier, `tags → tag1`, per-resource `file` in grouped publishes, the empty
`extracts` hover-card trap, and the pinned revisions). The evidence is in the
companion validation report.

---

## 10. ONE owner live-host validation procedure

Prerequisites: the app published/deployed as the Shadow Archives Q-App (or the
dev build loaded inside a real Qortal host with an account bridge), signed in as
the account that owns the publishing name; Node A or B reachable read-only in a
second browser tab.

1. **Open owner mode.** Navigate to `/studio`, press **Enter owner mode** and
   confirm with the host. Expect "Owner capability verified" and the publishing
   name shown.
2. **Open the Video workflow.** Press **Manage Videos** (or open `/videos`).
   Expect the Videos page with an **Owner controls** panel and an **Add video**
   button. (Confirm the visitor view in a private window: no panel, no
   "Add video", no account prompt.)
3. **Open the modal and fill it in.** Press **Add video**. Select an MP4/WebM
   file ≤ 2 GB; the browser fills the duration (type it if it cannot), and the
   file name/size and poster preview are shown. Select a JPEG/PNG/WebP poster.
   Enter a title, description, categories/tags and language.
4. **Publish.** Press **Publish** and approve each host prompt (expect three
   submissions: media+poster, entity+Q-Tube metadata, derived index). The modal
   shows step progress and is not dismissible mid-submission.
5. **Read the truthful outcome.** Expect `Published.` with the four exact
   identifiers: `saw_vid_<id>`, `qtube_vid_<id>`, `qtube_vid_<id>_metadata`,
   `saw_vid_thumb_<id>`. Anything else (partial / ambiguous / index-incomplete)
   is reported with the exact failing resources — press **Verify** before any
   retry, and note that retrying reuses the same identity.
6. **Verify from the UI.** Press **Verify** and confirm: entity/VIDEO/THUMBNAIL/
   metadata all present, "served entity matches", "Q-Tube validity gate: passed",
   "Q-Tube media reference: points at this publication", and the discovery query
   result (allow for index lag on the first attempt).
7. **Read-only cross-check (independent of the app).** In the node tab:
   `GET /arbitrary/resources/search?service=DOCUMENT&identifier=qtube_vid_&mode=ALL&reverse=true&limit=20`
   and confirm the new `qtube_vid_<id>_metadata` is listed; fetch
   `/arbitrary/DOCUMENT/<name>/qtube_vid_<id>_metadata` and confirm the metadata
   fields; fetch `/arbitrary/VIDEO/<name>/qtube_vid_<id>` and confirm the bytes
   play.
8. **Shadow Archives listing + detail + reload.** Close the modal: the new video
   must appear in the Videos listing (poster + duration). Open it via
   `/videos/<id>`: the player loads with the poster, plays with `controls`, and
   no bytes were requested before pressing play. Hard-reload the page and
   confirm the listing and detail still resolve.
9. **Q-Tube discovery.** Open Q-Tube against the same node/host, and confirm the
   publication appears under Home/Search (and under the matching category tab)
   with its poster, title and duration, and that pressing it opens Q-Tube's own
   player. Because Q-Tube's Home defaults to Core `LATEST` (one video per
   publisher), use the Search tab or the **All** mode to see every video; the
   newest video also appears in the default recent view.
10. **Record.** Capture the four identifiers, the Verify output and a Q-Tube
    screenshot into `docs/shadow-archives-webportal/validation/` as the live
    validation record (nothing here writes to QDN during verification).

---

## 11. Branch, commit and git state

- Branch: `agent/shadow-archives-webportal/gallery-index-coherence`
- HEAD: `472f244bd8cbb8f6ef11d60d7ee1baaaac6c0c83` (`Fix Gallery bridge reads
  and media hydration`) — **unchanged**
- No commit, no branch change, no tag, no push, no merge was made by this work.
- Worktree: 18 modified files, 2 renames (`TaxonomyInput.tsx`, `owner.css`), 14
  new untracked source files, plus the pre-existing user-owned untracked
  `AGENTS.md` (left untouched).
- Index state: the only staged entries are the two `git mv` rename pairs
  (`TaxonomyInput.tsx`, `owner.css` → `src/features/owner/`), which is what
  `git mv` stages; **no content change is staged** (all file content changes sit
  in the worktree, and `git diff --cached --stat` reports 0 insertions).

---

## 12. Saved report paths

- Implementation report (this document):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/implementation/2026-09-13-video-owner-publishing-implementation-report.md`
- Live read-only contract validation:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/validation/2026-09-13-video-qtube-contract-live-read-only-validation.md`
