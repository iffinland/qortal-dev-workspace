# Shadow Archives Phase 2C-A — first APP publication readiness

- Project: `shadow-archives-webportal-QORTAL`
- Phase / task: Phase 2C-A — prepare the first real QDN `APP` publication
  (preparation only; no publication performed)
- Date: 2026-09-11
- Author: Codex (implementation agent)
- Task class: release/artifact + platform integration (source verification);
  production build + packaging only, **no write path**
- Related:
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md),
  [`../architecture/2026-09-11-phase-1a-architecture-report.md`](../architecture/2026-09-11-phase-1a-architecture-report.md),
  [`../implementation/2026-09-11-phase-1b-appshell-implementation-report.md`](../implementation/2026-09-11-phase-1b-appshell-implementation-report.md),
  [`../implementation/2026-09-11-phase-2a-qdn-read-pipeline-report.md`](../implementation/2026-09-11-phase-2a-qdn-read-pipeline-report.md),
  [`../implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md`](../implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md)

## 1. Status

**PASS WITH OWNER VALIDATION REQUIRED.**

The Phase 2C-A exit criterion is met at the source, artifact and automated
layers: the current `APP` multi-file publication contract is source-verified
against the pinned Core/Hub revisions, the canonical deployed `APP` identity is
reduced to one explicit owner confirmation, a production artifact is built,
structurally validated and hash-recorded, build/revision provenance now proves
which build is served, and the owner publication procedure and post-publication
host-validation checklist are exact. **No QDN write, transaction, publication,
commit, push or release was performed.**

The remaining work is owner-authorized: one `APP` publication, then real-host
validation. Until that happens the app remains `NOT_PUBLISHED`, no genuine
`_qdnName` render context exists, and every real-host claim stays
`NOT VERIFIED`.

## 2. Baselines and preserved changes

| Repository | Path | Branch | HEAD (before) | origin/main | Worktree |
| --- | --- | --- | --- | --- | --- |
| Canonical workspace | `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace` | `main` | `2d4b90c` | `2d4b90c` | clean |
| Application | `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL` | `main` | `ac7cef1` | `ac7cef1` | clean |

No pre-existing uncommitted owner work was present; nothing was overwritten,
reverted, reset or restored. Commit, push, tag and GitHub mutation were not
performed.

## 3. Qortal reference revisions inspected

`git ls-remote` (read-only) confirmed both pinned revisions are still the
upstream `HEAD` on the execution date:

| Source | Revision inspected | Upstream HEAD 2026-09-11 | Used for |
| --- | --- | --- | --- |
| `Qortal/qortal` | `108bf191d42d710ec617f535af30cfd82fc03c87` (v6.1.9) | same | publish endpoints, `Service.APP`, `ZipUtils`, `ArbitraryDataResource`, `ArbitraryDataRenderer`, `HTMLParser`, `RenderResource`, `ArbitraryResource` API, `q-apps.js` |
| `Qortal/Qortal-Hub` | `12a573b27246e8a626b24794830c6bc432d1b05d` | same | `publishQDNResource`, `publishMultipleQDNResources`, `publishData`, `AppPublish`, `qortal-requests.ts`, `openNewTab`, `extractComponents`, `qortalLink` |

Local read-only clones at those exact revisions:
`/home/iffi/qortal-phase1a-research/qortal` and
`/home/iffi/qortal-phase1a-research/Qortal-Hub`.

Read-only live node used: `https://api.qortal.org` (mainnet, public node) on
2026-09-11. No other node or environment is claimed.

## 4. VERIFIED — current APP publication contract

All statements below are traced to the revisions in §3 and are marked as
verified facts, not inference.

### 4.1 Bridge write action

- **VERIFIED.** Core `q-apps.js` forwards both `PUBLISH_QDN_RESOURCE` and
  `PUBLISH_MULTIPLE_QDN_RESOURCES` to the host (`getDefaultTimeout` gives both a
  60-minute timeout because of proof-of-work). Hub handles both in
  `src/qortal/qortal-requests.ts` and dispatches to `publishQDNResource` /
  `publishMultipleQDNResources` (`src/qortal/get.ts`).
- **VERIFIED.** Both actions accept a multi-file ZIP: `PUBLISH_QDN_RESOURCE`
  takes one resource object; `PUBLISH_MULTIPLE_QDN_RESOURCES` takes
  `{ resources: [...] }`. Each resource object independently supports
  `isMultiFileZip === true`, which Hub maps to `uploadType: 'zip'`. For a single
  `APP` there is no need to use the multi-resource action.
- **VERIFIED.** Hub's own publishing UI (`src/components/Apps/AppPublish.tsx`)
  publishes an `APP`/`WEBSITE` by sending `uploadType: 'zip'` with **no
  identifier**. That is the ecosystem's current convention for an app bundle.

### 4.2 Accepted parameters (`PUBLISH_QDN_RESOURCE`)

From Hub `publishQDNResource` (`src/qortal/get.ts`) and `publishData`
(`src/qdn/publish/publish.ts`):

| Field | Required | Verified behaviour |
| --- | --- | --- |
| `service` | yes | `'APP'` for a Q-App. Core `Service.APP = 1000`, `requiresValidation = true`, `maxSize = 50 MB`, `single = false`, `isPrivate = false`. |
| `name` | no | Defaults to the host-selected name (`data?.name || getNameInfo()`). It must be a name owned by the connected account (Hub checks `getAllUserNames()` in the multi-resource path). |
| `identifier` | no | `null`/absent → Hub substitutes the literal string `'default'`. Core normalises `null`/`""`/`"default"` to the null/default resource (`ArbitraryDataResource` constructor). |
| `file` / `blob` | yes (one of) | A `File`; for a multi-file app this is the ZIP file. |
| `data64` / `base64` | yes (one of) | Alternative raw payload; not used for a ZIP. |
| `isMultiFileZip` | for ZIP | `data.isMultiFileZip === true` selects `uploadType: 'zip'` (Hub), which appends `isZip=true` to the Core finalize call. |
| `filename` | no | Passed through to Core; used for size/mime detection. |
| `title`, `description`, `category` | no | QDN metadata, surfaced in the Hub app library. |
| `tags` / `tag1..tag5` | no | Up to five tags. |
| `encrypt`, `publicKeys`, `encryption` | no | Not applicable to a public `APP`. |
| `appFee`, `appFeeRecipient` | no | Optional app fee; not used here. |

### 4.3 What Core does with a ZIP

- **VERIFIED.** Hub chunk-uploads the ZIP to
  `/arbitrary/{service}/{name}/{identifier}/chunk` and finalises with
  `.../finalize?...&isZip=true` (`src/qdn/publish/publish.ts` `uploadData`).
- **VERIFIED.** Core `ArbitraryResource.finalizeUpload` (identifier path) merges
  the chunks and calls `upload(..., zipped = true)`; `upload` unzips with
  `ZipUtils.unzip` (`src/main/java/org/qortal/utils/ZipUtils.java`).
- **VERIFIED.** After unzip, if the extraction directory contains exactly one
  root entry (ignoring names starting with `_`), Core descends into that single
  entry. A ZIP therefore works whether its root is the app content or a single
  enclosing folder — but the unambiguous, recommended form is a ZIP whose root
  already contains `index.html` (no parent `dist/`).
- **VERIFIED.** `ZipUtils.unzip` recreates parent directories itself, so a ZIP
  without explicit directory entries extracts correctly.
- **VERIFIED.** `Service.APP` does not itself require an index file, but the
  renderer does: `ArbitraryDataRenderer.getFilename` looks for
  `index.html`, `index.htm`, `default.html`, `default.htm`, `home.html`,
  `home.htm` in the resource root, and `APP` forwards any unhandled path back to
  that index file (`usingCustomRouting = true`).

### 4.4 Identifier / default-resource behaviour

- **VERIFIED.** Default and explicit identifiers are the same mechanism:
  `null`, `""` and the literal `"default"` all denote the default resource.
- **VERIFIED.** Hub's render path always sends `identifier=` (empty for the
  default resource): `AppViewer.tsx` builds
  `/render/{service}/{name}?...&identifier={id ?? ''}`.
- **VERIFIED.** `RenderResource` accepts `identifier` as a **query parameter**
  (`?identifier=...`), not a path segment. If the parameter is absent, Core's
  renderer sets `identifier = "default"`.
- **VERIFIED.** For a **non-default** identifier in `render` context,
  `HTMLParser` appends `?identifier=<id>` to every relative `<script src>` and
  `<link href>`. The default identifier does not trigger this rewrite.
- **Consequence.** `_qdnIdentifier` may be `""` or `"default"` depending on how
  the host opened the resource; both mean the default identity. Owner detection
  uses `_qdnName` only and is unaffected.

### 4.5 Approval, fee and success response

- **VERIFIED.** Publishing is host-mediated and approval-gated:
  `publishQDNResource` calls `getUserPermission` with `service`, `identifier`
  and `name`, unless a session permission
  (`hasSessionPermission(tabId, appName, 'PUBLISH_QDN_RESOURCE')`) already
  exists. A decline throws; there is no silent success.
- **VERIFIED.** The fee is `getFee('ARBITRARY')`, passed as `fee` with
  `withFee: true`. The live read-only value on 2026-09-11 was
  `1000000` satoshi = `0.01 QORT` (fees vary over time — read it at publish
  time, do not hardcode).
- **VERIFIED.** Size limits: Hub's app-publish UI caps the ZIP at
  `50 MB` for `APP`; Core caps the **uncompressed** `APP` resource at
  `50 MB`; Hub-wide limits are 2 GB (`MAX_SIZE_PUBLISH`) and 500 MB on a public
  gateway node (`MAX_SIZE_PUBLIC_NODE`).
- **VERIFIED.** Success response: Hub returns the raw
  `/transactions/process` result; callers check `response.signature`. This is a
  **submission acknowledgment** (transaction built, signed and broadcast), not a
  network confirmation and not proof that the served resource is the new build.

### 4.6 Submission vs confirmation vs status vs intended revision

These are four separate states and MUST NOT be conflated:

1. **Submission** — the write call returns a result with `signature`.
2. **Transaction confirmation** — the arbitrary transaction is in a block
   (verify via the transaction/signature, not via a resource status).
3. **Resource status** — `GET_QDN_RESOURCE_STATUS` →
   `/arbitrary/resource/status/{service}/{name}[/{identifier}]?build=true`
   returns `NOT_PUBLISHED` / `PUBLISHED` / `DOWNLOADING` / `DOWNLOADED` /
   `BUILDING` / `READY` / `MISSING_DATA` / `BUILD_FAILED` / `BLOCKED`.
4. **Intended revision/content verification** — the served bytes match the
   build that was intended (§7). **A `READY` resource is not proof of the
   intended revision**: an older revision of the same resource can already be
   `READY`.

### 4.7 Timeout ambiguity

- **VERIFIED.** Core gives `PUBLISH_*` a 60-minute timeout because proof-of-work
  can be slow.
- **VERIFIED.** Hub internally retries its HTTP posts up to 3 times
  (`resuablePostRetry`) with 25-second backoff, and Core's `/transactions/process`
  can be re-submitted; a client-side timeout therefore does **not** prove the
  write failed.
- **Rule.** An ambiguous publish MUST NOT be automatically retried. Check the
  resource status and (where possible) the signature/transaction before any
  resubmission (see §8).

## 5. RECOMMENDED — canonical APP resource identity

**Owner decision required before live publication.**

- Recommended: **default/null identifier** — `(service=APP, name="Shadow Archives", identifier=default)`.
  - Renders exactly at `qortal://APP/Shadow Archives` (Hub's `extractComponents`
    parses `qortal://APP/Shadow Archives` → `service=APP`, `name="Shadow
    Archives"`, no identifier, path empty).
  - Matches the current ecosystem convention used by Hub's own app-publish UI
    (no identifier).
  - Avoids the non-default-identifier asset-URL rewriting in `HTMLParser`.
- Alternative (not recommended): an explicit identifier such as `saw_app`.
  Technically viable and supported, but:
  - `qortal://APP/Shadow Archives` (no identifier) would then resolve to a
    different, empty resource;
  - the app would be addressed as `qortal://APP/Shadow Archives?identifier=saw_app`;
  - the render context rewrites relative script/link URLs with
    `?identifier=saw_app`, adding avoidable failure surface.
- **Do NOT reuse the content namespace `saw_` as the APP identifier.** `saw_` is
  the Shadow Archives **content** namespace (owner decision D1) for content
  resources such as `saw_post_*`; the `APP` resource is the application bundle
  and is identified by its name under the `APP` service.
- Owner confirmation needed: "Publish the app bundle under the default
  identifier so `qortal://APP/Shadow Archives` is the canonical URL." If the
  owner later wants a versioned/alternate APP resource, that is a separate
  explicit decision and must not be inferred from the `saw_` content prefix.

## 6. Production artifact

Built from the clean application baseline plus the Phase 2C-A provenance change
(working tree at `ac7cef1` + uncommitted Phase 2C-A edits; `dirty: true` in
`build.json`).

| Item | Value |
| --- | --- |
| Artifact | `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL/release/shadow-archives-app-0.1.0-20260911.zip` |
| Manifest | `…/release/shadow-archives-app-0.1.0-20260911.zip.manifest.json` |
| Layout | `index.html`, `build.json`, `sa-avatar.png`, `assets/*` at ZIP root (no parent `dist/`) |
| File count | 24 |
| Uncompressed size | 774964 bytes |
| Compressed size | 458078 bytes |
| SHA-256 | `697aa9664a03fac0e1a1ea90d7631a899a4b27ea6f273aa56bf1dccde2a46c96` |
| Build identity | v0.1.0 + `ac7cef1` (base commit; worktree `dirty`) |
| Reproducibility | Deterministic ZIP layout (sorted entries, normalized 1980-01-01 UTC mtimes, `zip -X -D`); `SOURCE_DATE_EPOCH` overrides both the timestamp and the archive mtimes. Verified: packaging the same `dist/` twice yields the identical SHA-256. |

Structural verification performed by the packaging script (fails closed):
`index.html` present and at the ZIP root; `build.json` present and well-formed;
all lazy route chunks present (`AboutPage`, `BlogPage`, `BlogPostPage`,
`CategoryPage`, `ContactPage`, `GalleryAlbumPage`, `GalleryDetailPage`,
`GalleryItemPage`, `GalleryPage`, `ListingGrid`, `NotFoundPage`, `Pagination`,
`SearchPage`, `StudioPage`, `TagPage`, `VideoDetailPage`, `VideosPage`);
banner WebP present; entry CSS present; no `.map`, `node_modules`, `.env`,
`*.ts`/`*.tsx`; `index.html` contains only relative asset URLs.

Key per-file SHA-256 (for intended-revision comparison):

| File | Bytes | SHA-256 |
| --- | --- | --- |
| `index.html` | 671 | `bf1620595793faa91df1210a943c1d7cf9869562de51c560b16cd2ab7dbdad94` |
| `build.json` | 205 | `0f58c8b6e1d9c3d46c2d895c63df6b0474aacfe0b75c7db68a4c665f21ac2e3a` |
| `assets/index-Du42F_sz.js` | 383959 | `df05200e632c3c56d27f88e25b483d968de2220867a82aa9db5c22bf45b730c7` |
| `assets/index-C1kic4fh.css` | 25243 | `d4d0ca2e7bc88174e62f4ee82bcd1d5349dbff5b0dd4749637f6eb379a56ac77` |
| `assets/BlogPostPage-BoDys3j6.js` | 36491 | `bab34c9e8882c874d9f64954138fa5b0d4cf2ac60bee722e69b7e1b822b87ad0` |
| `assets/banner-shadow-archives-MsX27Odr.webp` | 202888 | `e23ae33bba52e1e139a0bc2ed9ace60964da66031559fe1e8f9de4383d752841` |

The release artifact and manifest are intentionally **not** committed
(`.gitignore` now ignores `/release/`); they are owner-facing local inputs.

## 7. Build / revision provenance

- Added `src/build/buildInfo.ts` (typed, frozen build identity) and a Vite
  plugin in `vite.config.ts` that:
  - injects `__BUILD_INFO__` (`app`, `version` from `package.json`, `commit`,
    `commitShort`) at build time;
  - emits `dist/build.json` with the full record
    (`app`, `version`, `commit`, `commitShort`, `builtAt`, `dirty`).
- `commit` is deliberately timestamp-free in the bundle, so identical source
  produces identical executable bytes and the emitted content hashes stay
  meaningful. `builtAt` and `dirty` live only in `build.json`.
- The footer provenance line and the `/studio` page now show
  `v<version> · <commitShort>`; `/studio` shows the full short-commit label.
- **Intended-revision verification method (authoritative):**
  1. `GET https://<node>/arbitrary/resource/status/APP/Shadow%20Archives?build=true`
     → expect a non-`NOT_PUBLISHED` status (this alone does **not** prove the
     revision).
  2. `GET https://<node>/arbitrary/APP/Shadow%20Archives?filepath=build.json`
     → expect `version` `0.1.0`, `commit` `ac7cef1b…`, and compare `builtAt`.
  3. `GET https://<node>/arbitrary/APP/Shadow%20Archives?filepath=assets/index-Du42F_sz.js`
     and compare the SHA-256 with the recorded file hash. Non-HTML assets are
     served byte-for-byte (Core streams them unchanged), so a hash match proves
     the served revision is this build. (`index.html` itself is rewritten at
     render time by `HTMLParser`, so do not hash-compare `index.html`.)
  4. Cross-check the served `index.html` references the same hashed asset
     filenames (`./assets/index-Du42F_sz.js`, `./assets/index-C1kic4fh.css`).
- A hash match on step 3 + metadata match on step 2 is the required evidence; a
  `READY` status is not.

## 8. EXACT owner live-publish procedure (DO NOT RUN without owner authorization)

**Prerequisites**

- A synced Qortal node and the current Qortal Hub (desktop/web) with the
  connected account that owns the name `Shadow Archives`
  (`QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`).
- The account holds enough QORT for the arbitrary fee (read it live; ~0.01 QORT
  on 2026-09-11).
- The artifact in §6 (unchanged SHA-256
  `697aa9664a03fac0e1a1ea90d7631a899a4b27ea6f273aa56bf1dccde2a46c96`).

**Recommended path — Hub app-publish UI (source-verified, no custom code)**

1. Confirm the resource is still unpublished:
   `GET /arbitrary/resource/status/APP/Shadow%20Archives` → `NOT_PUBLISHED`.
   If a previous attempt already produced any other status, **stop** and verify
   the served revision (§7) before uploading again.
2. In Hub, open the Apps/Publish-App screen, choose the **publishing name
   `Shadow Archives`** (never a different owned name), and service **`APP`**.
3. Select `release/shadow-archives-app-0.1.0-20260911.zip`. Leave the
   **identifier empty** (default). Do not prefix with `saw_`.
4. Fill metadata: title/description/category/tags as desired. Metadata is
   advisory QDN metadata; it does not change the rendered app.
5. Approve the single Hub fee/approval dialog. Do **not** approve more than once.
6. Wait. Publishing does proof-of-work; Hub's publish timeout is up to 60
   minutes. Do **not** re-submit while a submission is in flight.

**Duplicate-avoidance rule.** The APP address is
`(service=APP, name="Shadow Archives", identifier=default)`; re-publishing the
same triple overwrites. Before any resubmission: check the resource status and
§7 intended-revision evidence. Only resubmit if there is positive evidence the
previous attempt never reached the network (no signature/transaction and the
status is still `NOT_PUBLISHED`).

**If the call times out or the UI is ambiguous.** Treat the write as **possibly
submitted**. Do not auto-retry. Check status, `build.json` and the asset hash
first; only then decide. A resource that is `DOWNLOADING`/`BUILDING` is not a
failure.

**Confirmation.** Success requires, in order: (1) the Hub dialog returned a
successful publish (`signature` present); (2) the arbitrary transaction is
confirmed on chain; (3) the resource status becomes `READY`; (4) the §7
intended-revision check matches. Only (4) proves the intended build is served.

**After confirmation.** Run the post-publication validation in §9 with the owner
account. No further QDN write is part of validation.

## 9. Post-publication real-host validation checklist (exact)

Environment to record: node URL/port + network, Hub build, host context
(`render`), account/name, and the served build id from §7.

**A. Open `qortal://APP/Shadow Archives`** in the Hub (app search/address field
or a `qortal://APP/Shadow Archives` link). Confirm it renders the app, not a
loading/404 page. Also confirm the URL-encoded form
`qortal://APP/Shadow%20Archives` behaves the same.

**B. Injected context.** In the rendered frame confirm:
`_qdnService === 'APP'`; `_qdnName === 'Shadow%20Archives'` (percent-encoded);
`_qdnIdentifier` is `''` or `'default'` (both mean default — record which);
`_qdnContext === 'render'`; `_qdnBase === '/render/APP/Shadow%20Archives'`;
`_qdnBaseWithPath` matches the current path; `qortalRequest` is a function.

**C. Routes and chunks.** Visit and verify each: Home, Blog, Blog detail,
Videos, Video detail, Gallery, Gallery album, Gallery item, taxonomy
(`/category/...`, `/tag/...`), Search, a deep route, and a refresh/route reload
(direct load of a deep path — `APP` must route it back to `index.html`).
Confirm lazy route chunks load from the resource (no 404s), and confirm the
banner asset loads.

**D. Phase 2A read pipeline.** Confirm live `SEARCH_QDN_RESOURCES` responses,
that the empty/partial/stale states are truthful (no fabricated content), that
`FETCH_QDN_RESOURCE` works for a known existing resource, and that a same-origin
QDN image/media path resolves inside the render origin (`/arbitrary/...`).

**E. External Qortal navigation.** From the app click Q-Tube, SubWire and
Quitter; confirm each opens via `qortal://` interception (new tab) and not a
blocked web navigation.

**F. CSP and clipboard.** Watch the console for CSP violations (the render CSP
is `default-src 'self' 'unsafe-inline' 'unsafe-eval'; font-src 'self' data:;
media-src 'self' data: blob: http://127.0.0.1:* http://localhost:*;
img-src 'self' data: blob:; connect-src 'self' wss: blob:`) and verify the
clipboard cascade (copy action + DOM-selection fallback, no silent failure).

**G. Owner flow.** Confirm `/studio` load causes **no** auth request; "Enter
owner mode" triggers exactly one permission flow; the result matches the
**current** name ownership (owner for the owning account, non-owner for
another); no publish controls exist. Confirm the served build label shown on
`/studio` matches §7.

**Non-goals.** No content or transaction writes are part of validation after the
single authorized APP publication.

## 10. First-publication bootstrap

```text
production bundle (this artifact)
    ↓
owner-authorized APP publication under name "Shadow Archives", service APP
    ↓
submission ⇒ transaction confirmation ⇒ READY
    ↓
real qortal://APP/Shadow Archives render
    ↓
injected _qdnName / _qdnBase / _qdnService / _qdnContext
    ↓
Phase 1B / 2A / 2B real-host validation (this checklist)
```

What changes after first publication: the resource exists, so Core injects the
real `_qdn*` context and owner detection can be exercised. Nothing in the app is
changed by publication, and no pre-publication owner bypass was added. The
unpublished state remains fail-closed (`unknown`, never owner).

## 11. Studio discoverability (recommendation only — not implemented)

- Keep Studio **out** of primary public navigation.
- A later, discreet "Studio"/"Owner" entry may be placed in the footer or
  another secondary location.
- Opening `/studio` remains permission-free; only "Enter owner mode" requests
  account access.
- No navigation change was made in this task.

## 12. Tests / build / validation results

Application (`npm` scripts, Node 20.19.2):

| Command | Result |
| --- | --- |
| `npm run lint` | PASS |
| `npm run typecheck` | PASS |
| `npm test` | PASS — 32 files / 299 tests (was 31/295; +4 for build identity) |
| `npm run build` | PASS — 144 modules; entry 383.96 kB raw / 120.64 kB gzip; `build.json` emitted |
| `npm run format:check` | PASS |
| `git diff --check` | PASS (clean) |
| `npm run package:app` | PASS — 24 files, deterministic ZIP, structure validated |
| Batch structural checks | PASS (no source maps, node_modules, `.env`, TS source, absolute asset URLs) |

Workspace:

| Command | Result |
| --- | --- |
| `bash -n tools/validate-workspace.sh` | PASS (syntax OK) |
| `bash tools/validate-workspace.sh` | PASS (5 pre-existing human-review warnings; no failures) |

Dependency audit of `dist`: no MUI, no `qapp-core`, no TipTap editor, no video
player, no publishing/content-write implementation (the only changed runtime
imports are the build-identity module and its display in the footer/studio).

Not run / not available: real Qortal host rendering, live `_qdn*` injection and
live QDN resource verification — the APP resource is still `NOT_PUBLISHED`.
These remain `NOT VERIFIED`.

## 13. Self-audit

| # | Risk | Result |
| --- | --- | --- |
| 1 | Wrong APP service | `service: 'APP'` recommended and documented; artifact named for APP. OK |
| 2 | Content `saw_` prefix used as APP identifier | Rejected and explicitly documented; APP uses the default identifier. OK |
| 3 | `index.html` at wrong archive level | ZIP verified to have `index.html` at root; no parent `dist/`. OK |
| 4 | Absolute asset URLs under QDN | Built `index.html` is all-relative; script asserts no `/`, `//` or external URLs. OK |
| 5 | Lazy chunks missing from artifact | All 17 route chunks verified present. OK |
| 6 | Secrets / node_modules in artifact | Structural check forbids `.env`, `node_modules`, `.ts`/`.tsx`; only 24 build files. OK |
| 7 | Source maps shipped | `sourcemap: false`; no `.map` in artifact. OK |
| 8 | MUI / qapp-core / editor / video reintroduced | Not present in `package.json` or `dist`. OK |
| 9 | `READY` treated as intended-update proof | Explicitly rejected; intended-revision method is per-file hash + `build.json`. OK |
| 10 | Ambiguous timeout auto-retried | No retry logic added; procedure forbids auto-retry. OK |
| 11 | Hardcoded owner bypass added | None; unpublished state stays `unknown`. OK |
| 12 | APP publication accidentally performed | None; no write action invoked; node status still `NOT_PUBLISHED`. OK |
| 13 | Content-publishing research started | None; out-of-scope areas untouched. OK |
| 14 | Build provenance non-reproducible/random | Bundle identity is timestamp-free; `build.json` carries `builtAt`/`dirty`; ZIP is deterministic and verified. OK |

No unresolved BLOCKER/HIGH finding remains.

## 14. Files changed

Application (`/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`):

- `vite.config.ts` — build-provenance plugin (`__BUILD_INFO__`, `dist/build.json`, `dirty`).
- `src/build/buildInfo.ts` — new typed/frozen build identity.
- `src/build/buildInfo.test.ts` — new build-identity tests.
- `src/components/layout/SiteFooter.tsx` — real build id in the footer.
- `src/features/owner/StudioPage.tsx` — served build id on `/studio`.
- `src/app/config/siteConfig.ts` — truthful `phaseLabel`.
- `package.json` — `package:app` script.
- `.gitignore` — ignore `/release/`.
- `scripts/package-app.mjs` — new deterministic packager + structural validator + hash manifest.
- Generated (ignored, not committed): `dist/`, `release/shadow-archives-app-0.1.0-20260911.zip`, `…zip.manifest.json`.

Workspace (`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`):

- `projects/shadow-archives-webportal.md` — factual Phase 2C-A status.
- `docs/shadow-archives-webportal/release/2026-09-11-first-app-publication-readiness-report.md` (this report).

## 15. Git status (after task)

| Repository | Branch | HEAD | Status |
| --- | --- | --- | --- |
| Workspace | `main` | `2d4b90c` | modified `projects/shadow-archives-webportal.md` + new report (uncommitted) |
| Application | `main` | `ac7cef1` | 6 modified + 2 new source paths (uncommitted); `dist/`, `release/` ignored |

No commit, push, tag, release or GitHub mutation was performed.

## 16. Explicit no-write statement

**No QDN write occurred.** `PUBLISH_QDN_RESOURCE`,
`PUBLISH_MULTIPLE_QDN_RESOURCES`, every other QDN write action, every
transaction and every signing operation were **not** invoked. No resource was
published, no transaction was submitted, and the `APP` resource remains
`NOT_PUBLISHED` (`GET /arbitrary/APP/Shadow%20Archives` →
`Couldn't find PUT transaction …`). All live access was read-only against
`https://api.qortal.org`.
