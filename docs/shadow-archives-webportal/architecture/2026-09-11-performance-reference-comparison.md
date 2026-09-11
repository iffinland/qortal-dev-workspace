# Shadow Archives — Performance and Reference-Application Comparison

- Project: `shadow-archives-webportal-QORTAL`
- Phase: 1A (architecture / evidence gathering)
- Date: 2026-09-11
- Author: Codex (Phase 1A research)
- Status: evidence record; contains measured, source-observed, inferred and
  not-verified items
- Related: [`./2026-09-11-phase-1a-architecture-report.md`](./2026-09-11-phase-1a-architecture-report.md),
  [`./2026-09-11-qdn-data-contracts.md`](./2026-09-11-qdn-data-contracts.md),
  [`./2026-09-11-phase-1b-implementation-plan.md`](./2026-09-11-phase-1b-implementation-plan.md),
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md)

## Purpose

Record the actual evidence behind the Shadow Archives startup-architecture
recommendation. Nothing in this document is a performance budget. Where a
number was not measured in a real Qortal host, it is labelled as such.

## Fact labels used

- **MEASURED** — a production build or command was executed in this session and
  the number was read from its output.
- **SOURCE-OBSERVED** — read from a pinned current source file.
- **INFERRED** — reasoned from measured/source-observed evidence, not itself
  measured.
- **NOT VERIFIED** — not established; must not be treated as fact.

## 1. Sources and revisions inspected

All repositories were cloned read-only into
`/home/iffi/qortal-phase1a-research/` on 2026-09-11 and their `HEAD` was
recorded. Every revision below matches the revisions already pinned in
[`../../architecture/qortal-dapp-development-standard.md`](../../architecture/qortal-dapp-development-standard.md)
§Reference revisions, i.e. the workspace pins were still current.

| Source | HEAD revision | Date | Branch/tag |
| ------ | ------------- | ---- | ---------- |
| `Qortal/qortal` | `108bf191d42d710ec617f535af30cfd82fc03c87` | 2026-07-08 | `master`, `v6.1.9` |
| `Qortal/Qortal-Hub` | `12a573b27246e8a626b24794830c6bc432d1b05d` | 2026-08-23 | `develop` |
| `Qortal/qapp-core` | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` | 2026-05-25 | `master`, `v1.0.79` |
| `Qortal/qapp-templates` | `143cc7bffd265f543f96ef25bf1b58ef7bb04472` | 2026-05-25 | `main` |
| `Qortal/q-tube` | `68c3ea706c4ab110ffa44a7f55f8e09bdf7e85ff` | 2026-07-15 | `main`, `2.1.0` |
| `Qortal/Subwire` | `a933a6c44d60db19cd219408e36c747aebcce994` | 2026-06-27 | `master` |
| `Qortal/Quitter` | `4e4246c3283bcbc8e05e683260692ed36144f862` | 2026-05-25 | `master` |
| `Qortal/q-mail` | `ddf3aa928e0b51f89e2a6a7e86e5b44bdfd7b6d0` | 2026-05-28 | `main`, `3.2.1` |
| `Qortal/create-qortal-app` | `ea9d720bb31fa42b777659aceccd69ad20393abb` | 2025-05-12 | `main` |
| `iffinland/iffi-vaba-mees-QORTAL` | `64f55bf7b6f4a1a093f19413d3a985e61a9fad37` | 2026-06-11 | `main` (non-authoritative reference) |

Build environment (MEASURED): Node `v20.19.2`, npm `10.8.2`, Linux, Vite as
declared per project.

Upstream repositories were not modified. Builds ran inside the scratch clones
only.

## 2. Build-output measurements (MEASURED)

Every number below was produced by `npm ci`/`npm install` + the project's own
`build` script inside the scratch clone and read from the build output.

| App / baseline | Tooling | Entry JS (raw) | Entry JS (gzip) | Extra initial JS | CSS | Fonts emitted | Lazy chunks |
| -------------- | ------- | -------------- | --------------- | ---------------- | --- | ------------- | ----------- |
| Minimal React 19 + Router 7 baseline (this session, hand-written) | Vite 6.4.3, no chunk config | 317.50 kB | 101.08 kB | — | none | — | — |
| Minimal React 19 + Router 7 + MUI 7 subset (AppBar/Toolbar/Card/Button/Typography/1 icon) | Vite 6.4.3 | 435.35 kB | 139.67 kB | — | none | — | — |
| `qapp-templates/react-default-template` (React 19 + MUI 7 + `qapp-core` 1.0.79 + i18next + jotai, near-empty UI) | Vite 6.3.5, no chunk config | 1,882.85 kB | 590.74 kB | — | 47.44 kB (12.65 kB gzip) | 4 × Inter TTF ≈ 1,260 kB | none |
| `baseline-qappcore-min`: imports **only** `RequestQueueWithPromise` + `formatTimestamp` from `qapp-core` | Vite 6.4.3 | 1,908.62 kB | 596.00 kB | — | 47.06 kB (12.55 kB gzip) | — | none |
| `Qortal/Quitter` | Vite 6.3.5, `manualChunks`, terser, gzip+brotli, `lazy(App)` | 1,488.19 kB | 454.98 kB | 7 modulepreload chunks = 583.56 kB | 48.95 kB (13.07 kB gzip) | 4 × Inter TTF ≈ 1,260 kB | App 185.90 kB, editor 232.24 kB, emoji-picker 268.92 kB, VideoMetadataDialog 14.64 kB, NewPostModal 2.61 kB |
| `Qortal/Subwire` | Vite 6.3.5, no chunk config, no lazy | 2,621.26 kB | 804.93 kB | — | 72.93 kB (16.34 kB gzip) | 4 × Inter TTF ≈ 1,260 kB | none |
| `Qortal/q-tube` | Vite 7.3.2, no chunk config, no lazy | 3,389.48 kB | 1,015.14 kB | — | 89.22 kB (19.34 kB gzip) | 14 × Roboto TTF ≈ 2,050 kB | none |

Quitter's initial (modulepreloaded) JavaScript set, MEASURED from
`dist/index.html` + build report:

| Chunk | raw | gzip |
| ----- | --- | ---- |
| `index-*.js` (entry) | 1,488.19 kB | 454.98 kB |
| `mui-core-*.js` | 380.05 kB | 110.35 kB |
| `react-vendor-*.js` | 89.85 kB | 29.71 kB |
| `utils-*.js` | 47.00 kB | 16.54 kB |
| `i18n-*.js` | 45.91 kB | 14.60 kB |
| `mui-icons-*.js` | 13.09 kB | 4.97 kB |
| `state-*.js` | 7.66 kB | 3.13 kB |
| **initial total** | **2,071.75 kB** | **634.28 kB** |

`q-mail` was **not built** (its declared stack is materially older: React 18,
MUI 5, TipTap 2 + Slate + react-quill, `react-router-dom` 6, no chunking
configuration). It is recorded as SOURCE-OBSERVED only.

## 3. Why the `qapp-core` baseline is large (MEASURED + SOURCE-OBSERVED)

`baseline-qappcore-min` imports two small pure utilities and still produces a
1.91 MB / 596 kB gzip bundle. The cause is source-observed:

- **SOURCE-OBSERVED.** `qapp-core`'s published package exposes only the root
  entry (`package.json` `exports` has `"."` plus a types-only `"./global"`).
  There are no deep import subpaths, so any import loads the whole root module.
- **SOURCE-OBSERVED.** The published ESM entry
  (`qapp-core@1.0.79`, `dist/index.mjs`, 531,838 bytes) contains top-level
  static imports including `import videojs2 from "video.js"` and
  `import "video.js/dist/video-js.css"`, `zustand`, `@mui/material`,
  `react-idle-timer`, `react-hot-toast`, `dayjs`, `crypto-js`, `aes-js` and a
  vendored `nacl-fast` (`src/deps/nacl-fast.ts`).
- **SOURCE-OBSERVED.** `qapp-core`'s `package.json` declares **no**
  `sideEffects` field and 22 runtime `dependencies`; its `tsup.config.ts`
  externalises only React, MUI, emotion and `react-router-dom`, so everything
  else is inlined into the published bundle.
- **MEASURED.** In the `baseline-qappcore-min` output, video.js is present:
  `vjs-` × 355, `videojs` × 44, plus a 47 kB CSS file that includes video.js
  skin rules.
- **SOURCE-OBSERVED.** `qapp-core`'s `GlobalProvider` statically imports
  `IndexManager`, `MultiPublishDialog`, `GlobalPipPlayer` and `Toaster`, and
  `GlobalPipPlayer` statically imports `video.js`. The conditional render
  (`config.enableGlobalVideoFeature && <GlobalPipPlayer/>`) does not remove the
  static import graph.
- **SOURCE-OBSERVED.** The `react-default-template`'s `index.html` also loads
  `sw-video-decrypt.js` on every page and ships four Inter TTF weights.

**Consequence.** Under the current `qapp-core@1.0.79`, "use `GlobalProvider`"
and "ship video.js + a broad MUI surface + the whole framework component set in
the first paint" are the same decision. This is the single largest startup-cost
lever available to Shadow Archives.

## 4. Chunking, lazy loading and route splitting (SOURCE-OBSERVED)

| App | `manualChunks` | `lazy()` / dynamic `import()` | Route-level split |
| --- | -------------- | ----------------------------- | ----------------- |
| `qapp-templates/react-default-template` | no | none | no |
| `q-tube` | no | **0 occurrences** in `src` | no |
| `Subwire` | no | **0 occurrences** in `src` | no |
| `Quitter` | yes (react-vendor, mui-core, mui-icons, editor, emoji-picker, state, utils, i18n) | 4 (`App`, `NewPostModal`, `EmojiPicker`, `VideoMetadataDialog`) | yes (`lazy(() => import('../App'))`) |
| `q-mail` | no | none | no |
| `qapp-core` itself | tsup single root entry, no `splitting` configured for consumers | n/a | n/a |

**INFERRED.** Quitter is the only inspected app that pays for the shell before
heavy features, and it still initialises ~634 kB gzip of JavaScript. There is no
current Qortal app in this sample that demonstrates a genuinely small first
screen.

## 5. Startup-path observations per app (SOURCE-OBSERVED)

### q-tube

- Single 3.39 MB chunk; no code splitting.
- `@mui/material` 7 + `@mui/icons-material` 7, `framer-motion`,
  `react-quill-new` (editor), `mediainfo.js` (WASM), `localforage`, `idb-keyval`,
  `moment`, `react-dropzone`, 14 Roboto weights.
- Discovery uses one paginated `SEARCH_QDN_RESOURCES` per listing
  (`identifier: 'qtube_vid_'`, `limit: 20`, `mode`, `reverse`, with optional
  `names`/`description` filters) — a good batching pattern.
- Comments use service `BLOG_COMMENT`, paginated `/arbitrary/resources/search`
  calls (`limit=20`, `offset`, `reverse=false`).
- Likes use `qtube_like_`-style identifiers and `limit: 0` lookups.
- App taxonomy is encoded into the `description` metadata as
  `**category:<id>;subcategory:<id>;**` because Core search can filter
  `description`/`keywords` but not metadata `tags`.

### Subwire

- Single 2.62 MB chunk; no code splitting and no lazy imports.
- Editor (`react-quill-new`), `marked`, `mediainfo.js`, MUI 7 all in the entry.
- IndexedDB caches written by hand: primary names 24 h
  (`src/utils/primaryNamesCache.ts`), profiles with `expiresAt`
  (`src/utils/profileCache.ts`, `idb`).
- Uses only `DOCUMENT` and `METADATA` services, with `LIST_ARTICLES_FEED`,
  `ALL_ARTICLES`, `user-articles-<name>` etc. as **local cache list keys**, not
  published QDN `LIST` resources.
- Like/comment lookups use `limit: 0` (unbounded).

### Quitter

- Best splitting of the sample, but the entry chunk still carries the framework
  bundle (video.js markers present in `index-*.js`).
- `lazy(App)` at the router plus lazy editor/emoji/video-metadata dialogs.
- Likes: identifier = `hash('like') + hash(postIdentifier)` under the actor's
  own name; `hasLiked` = lookup filtered by `name`; count = raw result length.
  Unlike republishes the same identifier with a one-byte placeholder
  (`data64: 'RA=='` in `qapp-core` `deleteResource`).
- Comments: service `BLOG_COMMENT`, identifier
  `qc_v1_qtube_<hashPostId>_base_<uid>` / `..._reply_<parentSuffix>_<uid>`,
  edit = republish the same identifier.

### q-mail (SOURCE-OBSERVED only)

- React 18, MUI 5, TipTap 2 + Slate + react-quill, redux-toolkit,
  `react-grid-layout`, `react-joyride`, `react-virtuoso`, `axios`. No chunking
  config. Treat as a functional reference for the MAIL convention, not as a
  performance model.

### Reference app `iffi-vaba-mees-QORTAL` (non-authoritative)

- React 19 + `react-router-dom` 7 + `react-icons`; **`HashRouter`** and no
  `_qdnBase` handling; static content committed in `src/data/postsData.js`.
- Like counts are computed as `page.length` of a single capped page
  (`PAGE_SIZE`) with `prefix: true` — i.e. a capped scan presented as a count.
  The global rule forbids this; Shadow Archives must not copy it.
- Like identifiers are readable and app/type-prefixed
  (`ivm_bl_`, `ivm_vl_`, `ivm_gl_` + entity key + 16-char actor suffix), which is
  a useful contrast to `qapp-core`'s opaque hashing.

## 6. Live published APP sizes (read-only node evidence)

Environment recorded: node `https://api.qortal.org`, queried 2026-09-11
(UTC ~11:40), read-only `GET /arbitrary/resources/search?service=APP`.

| Published name | APP resource observed | Reported size |
| -------------- | --------------------- | ------------- |
| `Q-Tube` | yes | 3,075,872 bytes |
| `SubWire` | yes | 2,488,912 bytes |
| `Quitter` | yes | 3,925,296 bytes |

**INFERRED.** Published APP bundles are multi-file zips in the low single-digit
MB. This is the delivery cost an end user pays once per app version, on top of
per-session catalog/media traffic. Startup JS structure still matters because it
determines how much of that bundle must be parsed and executed before the first
useful screen.

## 7. Platform performance-relevant constraints (SOURCE-OBSERVED)

Traced to `Qortal/qortal` `v6.1.9` and `Qortal/Qortal-Hub` `12a573b2`:

- `Service` size limits (`Service.java`): `JSON` 25 KB (single, validated),
  `THUMBNAIL` 500 KB, `IMAGE` 10 MB, `COMMENT`/`BLOG_COMMENT` 500 KB (single),
  `MAIL` 1 MB / `MAIL_PRIVATE` 5 MB, `CHAIN_COMMENT`/`CHAIN_DATA` 239 bytes,
  `APP` 50 MB. `DOCUMENT` and `LIST` declare **no** `maxSize`.
  `ArbitraryDataFile.MAX_FILE_SIZE` = 2 GiB; chunk size 512 KiB.
- Metadata limits (`ArbitraryDataTransactionMetadata.java`):
  title ≤ 80, description ≤ 240, tag ≤ 20, **max 5 tags**.
- Identifier limit (`ArbitraryTransaction.MAX_IDENTIFIER_LENGTH`): **64** UTF-8
  bytes, enforced when a transaction is deserialised.
- Search (`ArbitraryResource.java` `/resources/search`): `query` matches
  **name, identifier, title and description only** — never body content.
  `limit` is applied only when `> 0`, so `limit=0` means *unbounded*.
- Search response entries expose `name`, `service`, `identifier`,
  `latestSignature`, `status`, `size`, `created`, `updated` and — with
  `includemetadata=true` — `title`, `description`, `tags`, `category`,
  `categoryName`, `mimeType`.
- Bridge request budget: `q-apps.js` caps concurrent requests at
  `MAX_CONCURRENT_REQUESTS = 30`; `SEARCH_QDN_RESOURCES` default timeout 30 s,
  `FETCH_QDN_RESOURCE` 60 s, `PUBLISH_*` and `GET_USER_ACCOUNT` 1 h.
- Core has a node-side index/search facility: `GET /arbitrary/indices?terms=...`
  and `GET /arbitrary/indices/{name}/{idPrefix}`; `qapp-core`'s `IndexManager`
  publishes index resources as `JSON` with identifiers
  `idx-<hashedRootName>-<hashedLink>-<uid>`. There is **no `qortalRequest`
  bridge action** for it; q-app-core calls `/arbitrary/indices/...` directly.
- Production render CSP: `default-src 'self' 'unsafe-inline' 'unsafe-eval';
  font-src 'self' data:; media-src 'self' data: blob:
  http://127.0.0.1:* http://localhost:*; img-src 'self' data: blob:;
  connect-src 'self' wss: blob:`. Third-party CDNs, remote fonts and remote
  image hosts are therefore unavailable by default.
- `q-apps.js` `interceptClickEvent` calls `preventDefault()` on every
  `http(s)`/`//` anchor click and converts `qortal://` anchors into
  `LINK_TO_QDN_RESOURCE`. External-link navigation is blocked by the platform,
  which is why the copy-to-clipboard policy is the correct one.

## 8. Recommended Shadow Archives startup architecture

Target: first useful screen from shell + cached catalog metadata only.

1. **Shell-first render.** Header, primary action row, navigation, footers and
   layout skeletons render without waiting for any QDN content.
2. **No framework-wide root import.** Do not import `qapp-core`'s root entry in
   the shell. Recommended: an in-repo, typed Qortal integration layer
   (`src/qortal/`) with a bridge wrapper, auth/owner detection, identifier
   helpers, a bounded request queue and a publish wrapper. Alternative: accept
   `qapp-core` and ~590 kB gzip of baseline JavaScript (rejected — the owner
   approved the in-repo layer, D7).
3. **No MUI (owner-approved D6).** Custom CSS-variable token layer plus small
   in-repo components and inline SVG icons. Exception: keep a documented escape
   hatch if a required accessible primitive (e.g. focus-trapped dialog) proves
   too costly to build; adding a framework still needs a new evidence-backed
   reason and owner approval.
4. **Route-level code splitting.** `React.lazy` + `Suspense` per top-level
   route; detail views are their own chunks; the owner/studio subtree is a
   single lazy chunk that normal visitors never download.
5. **Dynamic import of heavy features.**
   - Rich-text owner editor (TipTap) — owner chunk only.
   - Comment composer rich-text surface — lazy, loaded on first focus/opening.
   - Video player — lazy, only on the video detail route, and only after the
     user starts playback; never request video bytes on listing pages.
   - Gallery originals — viewport-driven `loading="lazy"` on thumbnails; full
     originals only on explicit open.
6. **Catalog + IndexedDB cache.** Cache catalog partitions and a compiled local
   search index in IndexedDB with explicit success/failure TTLs, stale-while-
   revalidate, and a visible "last updated" indicator. Repeat visits must render
   from cache before any network call resolves.
7. **Bounded request queue.** In-repo concurrency-limited queue (start at 4–6;
   `q-apps.js` itself allows up to 30). Never issue per-card requests for
   metadata, status, engagement and media simultaneously.
8. **Skeletons that reserve layout.** Fixed heights for the 240 px Top
   Posts/Top Videos columns and the 300–340 px banner; explicit aspect-ratio
   boxes for cards and gallery tiles so content arrival does not shift layout.
9. **Selective prefetch only.** On idle, prefetch the next probable route's
   *metadata* (never media, never the editor). Prefetch is capped and skipped on
   save-data / slow connections.
10. **Font discipline.** Ship at most two brand weights, `font-display: swap`,
    preload only the banner face. Do not inherit the template's four Inter
    weights or q-tube's fourteen Roboto weights.
11. **Honest partial states.** Loading, ready, empty-valid, partial,
    unavailable, malformed and error are distinct render states. `limit`
    truncation is shown as partial, never as a total.

### Explicit anti-goals (do not load on startup)

- owner publishing editor and any `@tiptap/*` code;
- owner/studio management panels or moderation tooling;
- video player code (`video.js` or equivalent) when no video is being watched;
- gallery originals;
- full comment bodies;
- any per-card engagement resource.

### Budget position

No millisecond budget is set here. The only quantitative target this phase
supports is **comparative**: keep Shadow Archives' initial JavaScript
meaningfully below the inspected apps' 590 kB–1,015 kB gzip entry range by not
inheriting the `qapp-core` root graph and MUI. A concrete budget must be set in
Phase 1B from a real measured baseline in the dev proxy and a real host.

## 9. What was NOT measured / not verified

- **NOT VERIFIED.** No real Qortal host or dev-proxy runtime measurement was
  taken (no node/dev-proxy timing, no browser paint metrics, no waterfall).
- **NOT VERIFIED.** No mobile-device (Android/iOS WebView) measurement.
- **NOT VERIFIED.** `q-mail` was not built.
- **NOT VERIFIED.** Whether `qapp-core`'s published bundle can be tree-shaken
  under a different bundler configuration than Vite/Rollup default. The
  measured Vite result is the one that matters for this project.
- **NOT VERIFIED.** LD/parsing cost on low-end hardware for any of the measured
  bundles.
- **NOT VERIFIED.** Whether the metadata-`tags`-as-engagement-state mechanism
  proposed in
  [`./2026-09-11-qdn-data-contracts.md`](./2026-09-11-qdn-data-contracts.md)
  survives a real republish (source-observed only). It must be proven with one
  controlled owner publication in Phase 1B/live validation.

## 10. Validation performed for this document

- All claims above are traceable to the pinned revisions listed in §1, to the
  build outputs recorded in §2/§3, or to the read-only node response in §6.
- Live evidence node and time are recorded in §6.
- No upstream repository was modified; all builds ran in scratch clones.
