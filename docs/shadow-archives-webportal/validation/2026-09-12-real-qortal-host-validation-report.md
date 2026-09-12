# Shadow Archives Phase 2C-B — real Qortal host validation after the first APP publication

- Project: `shadow-archives-webportal-QORTAL`
- Phase / task: Phase 2C-B — validate the published `APP` resource and runtime
  read-only, and close as many host-only `NOT VERIFIED` items as possible
- Date: 2026-09-12
- Author: Codex (validation agent)
- Task class: live QDN / host validation + release provenance verification,
  **read-only**. No QDN write, transaction, publication or content write.
- Related:
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md),
  [`../implementation/2026-09-11-phase-2a-qdn-read-pipeline-report.md`](../implementation/2026-09-11-phase-2a-qdn-read-pipeline-report.md),
  [`../implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md`](../implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md),
  [`../release/2026-09-11-first-app-publication-readiness-report.md`](../release/2026-09-11-first-app-publication-readiness-report.md),
  [`../implementation/2026-09-11-owner-runtime-visual-correction-report.md`](../implementation/2026-09-11-owner-runtime-visual-correction-report.md),
  [`../implementation/2026-09-11-owner-runtime-visual-correction-followup-report.md`](../implementation/2026-09-11-owner-runtime-visual-correction-followup-report.md)

## 1. Status

**PASS WITH OWNER VALIDATION REQUIRED.**

Phase 2C-B is ready on the automated, source and public-node layers:

- the published `APP` resource identity `(service=APP, name="Shadow Archives",
  identifier=default)` exists and is confirmed by two independent public nodes;
- the **served revision is identified** from chain-anchored resource metadata and
  is **not** the committed baseline artifact (see §5 — classified
  `MISMATCH` by revision identity, `EQUIVALENT` by served content);
- the owner's already-provided runtime observations are recorded at
  `OWNER RUNTIME VERIFIED` level (§6) rather than promoted to platform proof;
- the remaining real-host boundary (`_qdn*` injection, owner-capability click
  flow, live read pipeline, media, clipboard, CSP) is either source-verified or
  explicitly bounded as owner-checkable, with exact owner steps (§7, §8, §10,
  §12–§15, §22);
- the complete validation suite passes (§18);
- no write of any kind occurred (§23).

**Headline finding.** The published resource currently serves the
**2026-09-11 artifact** (`release/shadow-archives-app-0.1.0-20260911.zip`, build
commit `1b099c1`, `dirty: true`), not the 2026-09-12 artifact built from the
committed baseline `6354c88`. Its chain-anchored file list is byte-for-byte the
2026-09-11 artifact file set and differs from the 2026-09-12 artifact in 19 of
24 files. After normalizing Vite chunk names and the embedded build-identity
strings, the two artifacts are **identical in every served file**; only
`build.json`, the embedded build label and the chunk filenames differ. Behaviour
conclusions from the owner's runtime observations therefore remain valid for the
current committed code, but **the app displays the build label `1b099c1`** and
the served bytes could not be hash-verified because the public network currently
cannot retrieve the resource data (§4.4).

**Second finding (availability, not an app defect).** Both public nodes can
serve the resource *metadata* but report the resource **data** as
`DOWNLOADING` 1 of 2 chunks (50%) / `MISSING_DATA` with `peerCount: 0`, and
`/render/APP/Shadow%20Archives/` returns HTTP 503 with the node's own loading
page. The published APP data is therefore not currently retrievable from the
public network tested here.

## 2. Baselines and preserved changes

| Repository | Path | Branch | HEAD at task start | origin/main | Worktree at task start |
| --- | --- | --- | --- | --- | --- |
| Canonical workspace | `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace` | `main` | `38cd2e065261a5d64ffa5a93f5071b11522329b8` (`38cd2e06`, "Record Shadow Archives parchment visual baseline") | same | one pre-existing **untracked** owner file: `docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md` |
| Application | `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL` | `main` | `6354c883f5c9e914c39daf2a591e0993a946862b` (`6354c883`, "Checkpoint Shadow Archives parchment visual baseline") | same | clean |

Both baselines matched the values stated in the task prompt. The pre-existing
untracked workspace file was **not** modified, moved or deleted. Nothing was
committed, pushed, tagged or reverted.

## 3. Evidence classification used in this report

| Label | Meaning |
| --- | --- |
| `AUTOMATED VERIFIED` | Reproduced locally by the project's own commands/tests/build and local artifact inspection. |
| `PUBLIC-NODE VERIFIED` | Read from a named public Qortal node's API on the recorded date; no host/wallet involved. |
| `SOURCE VERIFIED` | Traced to the pinned Core/Hub source revisions, not to memory or docs. |
| `OWNER RUNTIME VERIFIED` | Reported by the owner from a real Qortal host session; recorded, not independently reproduced. |
| `NOT VERIFIED` | Not reached; no substitute evidence used. |

## 4. Published APP resource — read-only public-node evidence

### 4.1 Environment

- Node A (primary): `https://api.qortal.org` — mainnet public node, height
  `2721342` at check time.
- Node B (cross-check): `https://api.qortal.link` — mainnet public node, height
  `2721343` at check time.
- The developer environment has **no local Qortal node** (nothing listening on
  `12391`/`62391`) and **no SSH tunnel to the owner's node**; none was required
  or attempted.
- Requests issued were all HTTP `GET` (§23).

### 4.2 Resource identity and metadata — `PUBLIC-NODE VERIFIED`

`GET /arbitrary/resources/search?service=APP&query=Shadow&includeMetadata=true`
on both nodes returned the same single matching entry:

```json
{"name":"Shadow Archives","service":"APP",
 "latestSignature":"5fVoqGEc79aJqtyzdRES2uzxunywdZbNXqgAXe37kVyBBkaypxC8D9jrDVkUjXm4SsjwBvBkcgpB6Jn1BiadXm1G",
 "size":459360,"created":1789147042931,"updated":1789151543887}
```

`GET /arbitrary/metadata/APP/Shadow%20Archives/default` (chain-anchored metadata
record, referenced by the latest transaction's `metadataHash`) returned:

- `title`: `Shadow Archives`
- `description`: `Uncovering the past, exposing the truth. What was erased must be remembered.`
- `tags`: `["secrets","archives","truth","history"]`
- `category`: `HISTORY`
- `files`: **24** paths

`GET /names/Shadow%20Archives` returned owner
`QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA` — i.e. the publishing name is owned by the
account that also signed the publish transaction (§4.3). No private data was
requested or disclosed.

### 4.3 Chain-level confirmation — `PUBLIC-NODE VERIFIED`

`GET /transactions/signature/5fVoqGEc…` returned the latest ARBITRARY
transaction for this resource:

| Field | Value |
| --- | --- |
| `type` | `ARBITRARY` |
| `timestamp` | `1789151543887` = **2026-09-11T18:32:23.887Z** |
| `blockHeight` | `2720709` (block timestamp 2026-09-11T18:33:38Z) |
| `creatorAddress` | `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA` (matches name owner) |
| `name` / `service` | `Shadow Archives` / `1000` (`APP`) |
| `method` / `compression` | `PUT` / `ZIP` |
| `size` | `459360` |
| `metadataHash` | present |

**Conclusion.** The most recent publish of `APP/Shadow Archives` happened on
**2026-09-11 at 18:32 UTC**, and no later publish exists in the chain at the
recorded heights. The task prompt's "manually published/updated" state
therefore corresponds to that publication, not to a new publish on 2026-09-12.

### 4.4 Data-plane availability — `PUBLIC-NODE VERIFIED` (finding)

| Request | Result |
| --- | --- |
| `GET /arbitrary/resource/status/APP/Shadow%20Archives/default?build=true` | `DOWNLOADING`, `localChunkCount:1`, `totalChunkCount:2`, `percentLoaded:50.0` (both nodes, reproduced across several attempts over ~40 minutes) |
| `GET /arbitrary/resource/status/APP/Shadow%20Archives/default` (no build) | `MISSING_DATA` — "Unable to locate all files. Please try again later" |
| `GET /arbitrary/resource/status/APP/Shadow%20Archives/default` immediately after a build attempt | `PUBLISHED` — Core's 30-second "recently requested" window, not a different resource state |
| `GET /arbitrary/resource/request/peers/APP/Shadow%20Archives/default` | `{"peerCount":0}` — no peer served the data |
| `GET /arbitrary/APP/Shadow%20Archives/default/{build.json,index.html,sa-avatar.png,assets/index-CAMO8KQj.js}` | HTTP **404** for every file |
| `GET /render/APP/Shadow%20Archives/` | HTTP **503** with the node's own "Loading - Qortal Network" page |
| `GET /arbitrary/metadata/APP/Shadow%20Archives/default` | **200** — the small metadata record *is* available locally on the node |

Interpretation: the resource exists and is `PUBLISHED` on chain; only its
**data** is currently unavailable from the public network tested. The metadata
record (1 chunk) is retrievable; the content payload (2 chunks, 1 local) is not.
This is a network/hosting availability condition, not an application defect —
the app cannot influence it, and no workaround is proposed here.

Consequence: **served-byte** verification (fetching `build.json`, `index.html`
and asset bytes from the network and hashing them) is `NOT VERIFIED`, and the
served-revision identification in §5 rests on chain-anchored metadata plus local
artifact comparison instead.

### 4.5 Served revision identification — `PUBLIC-NODE VERIFIED` (metadata) + `AUTOMATED VERIFIED` (correlation)

The chain-anchored `files` list was compared, as a set, with the local release
manifests:

| Artifact | File set identical to served metadata? | Files only in manifest | Files only in served metadata |
| --- | --- | --- | --- |
| `shadow-archives-app-0.1.0-20260911.zip` | **yes (24/24)** | 0 | 0 |
| `shadow-archives-app-0.1.0-20260912.zip` | no | 19 | 19 |

This is the strongest available identification of the served revision without
the data payload: Vite emits content-hashed filenames, so an identical file-name
set implies identical file contents for every emitted chunk, stylesheet, banner,
avatar, `index.html` and `build.json` entry.

## 5. Served build provenance vs. the committed baseline

| Item | Value |
| --- | --- |
| Local committed HEAD (app) | `6354c883f5c9e914c39daf2a591e0993a946862b` (`6354c88`), clean at task start |
| Served build commit (identified) | `1b099c1f4edcf4e2138b35fb1f1e494a016b8059` (`1b099c1`), `dirty: true` |
| Served artifact | `release/shadow-archives-app-0.1.0-20260911.zip`, 24 files, 774600 B raw, 458076 B zip, SHA-256 `354065b96f40f61cb226ba0836c71e058895fb1a1511c0a8eefca3f7331d6128`, built `2026-09-11T18:30:30.078Z` |
| Local HEAD artifact | `release/shadow-archives-app-0.1.0-20260912.zip`, 24 files, 774601 B raw, 458080 B zip, SHA-256 `8f2be5f4538d3618bd4eff29c50b5d6f0567c5b18985f01b123dc9f41bbf45ca`, built `2026-09-12T07:10:48.145Z`, `dirty: false` |
| App version (both) | `0.1.0` |
| Served revision identity vs. HEAD | **MISMATCH** (served commit `1b099c1` ≠ HEAD `6354c88`) |
| Served content vs. HEAD artifact | **EQUIVALENT** — every file is byte-identical after normalizing the 8-character Vite chunk-name hashes and the embedded commit/`build.json` identity strings |
| Raw served bytes hash-verified against the artifact | `NOT VERIFIED` (network data unavailable, §4.4) |

Equivalence evidence (`AUTOMATED VERIFIED`, local): both zips were extracted and
compared. After normalization, all 19 JS chunks, the single CSS file, the banner
WebP, `sa-avatar.png` and `index.html` are byte-identical; the only residual
differences are `build.json` (`commit`, `commitShort`, `builtAt`, `dirty`) and the
`build.json`/chunk-name strings compiled into the entry chunk.

**Why this is not a defect in this phase.** The published artifact is exactly
the Phase 2C-A artifact the project file's step 3 prescribed for the first
publication, published 8 minutes before the parchment-baseline commit was made
and 13 hours before the newer artifact was built. Nothing in this phase
authorized a publication, so the served revision was left untouched.

**Consequences the owner should know.**

1. The footer and `/studio` in the published app display
   `Build v0.1.0 · 1b099c1`, not `6354c88`. That is truthful for the served
   build and is itself an owner-visible provenance check.
2. Because the served content is equivalent to HEAD except for that label, the
   owner's runtime observations (§6) are valid evidence about the current code's
   behaviour, and are **not** evidence about a build that does not exist.
3. Any future feature work will need a new (owner-authorized) publication before
   it can be host-validated.

**Documentation discrepancy (report vs artifact).** The Phase 2C-A report and
the project context record SHA-256
`697aa9664a03fac0e1a1ea90d7631a899a4b27ea6f273aa56bf1dccde2a46c96` for
`shadow-archives-app-0.1.0-20260911.zip`. The artifact on disk (mtime
2026-09-11 21:30 local, unchanged during this task) hashes to
`354065b9…`, which its own `.manifest.json` also records. The 2C-A report was
written at ~20:08 and the artifact was re-packaged at 21:30 (after the final
parchment correction) and published at 21:32. The recorded hash is therefore
**stale, not evidence of tampering**; it should be corrected where it is quoted.

## 6. Owner runtime observations already provided — `OWNER RUNTIME VERIFIED`

Recorded exactly as owner-supplied, and only at this level:

| Observation | Level |
| --- | --- |
| APP opens in Qortal at `qortal://APP/Shadow Archives` | OWNER RUNTIME VERIFIED |
| Layout renders | OWNER RUNTIME VERIFIED |
| Primary navigation selections work | OWNER RUNTIME VERIFIED |
| Primary action buttons work | OWNER RUNTIME VERIFIED |
| Route pages open | OWNER RUNTIME VERIFIED |
| Published/updated manually through Qortal Hub as `APP` / `Shadow Archives` / default identifier | OWNER RUNTIME VERIFIED (corroborated by §4.2–§4.3 PUBLIC-NODE evidence) |

These were **not** promoted to platform guarantees. In particular they are not
evidence that every future route dependency, every QDN media path, the
clipboard cascade or the owner-capability approval flow works.

## 7. Real host context (`_qdn*`)

### 7.1 Source-verified injection — `SOURCE VERIFIED`

Pinned Core `108bf191` (v6.1.9):

- `api/restricted/resource/RenderResource.java` — `@Path("/render")`;
  `prefix = String.format("/render/%s", service)`; `includeResourceIdInPrefix =
  true` for name-based resources; render context literal `"render"`.
- `arbitrary/ArbitraryDataRenderer.java:61` — `identifier = identifier != null ?
  identifier : "default"`; `:176` — `resourceId.replace(" ", "%20")`; `:158-165`
  — for `Service.APP` an unhandled path is forwarded to the index file with
  `usingCustomRouting = true`.
- `api/HTMLParser.java:72` — injects
  `_qdnContext`, `_qdnTheme`, `_qdnLang`, `_qdnService`, `_qdnName`,
  `_qdnIdentifier`, `_qdnPath`, `_qdnBase`, `_qdnBaseWithPath`; `:79` adds
  `<base href="{usingCustomRouting ? qdnBase : qdnBaseWithPath}/">`; `:89-115`
  rewrites relative `script`/`link` URLs with `?identifier=` **only** for a
  non-blank, non-`default` identifier.

Expected values for this resource in `render` context:

| Global | Expected value |
| --- | --- |
| `_qdnService` | `APP` |
| `_qdnName` | `Shadow%20Archives` (Core percent-encodes the space) |
| `_qdnIdentifier` | `""` (Hub sends `identifier=` empty) or `"default"` (parameter absent) — both mean the default resource and both are handled by the app |
| `_qdnContext` | `render` |
| `_qdnBase` | `/render/APP/Shadow%20Archives` |
| `_qdnBaseWithPath` | `/render/APP/Shadow%20Archives` + current directory path |
| `qortalRequest` | a function (from the injected `/apps/q-apps.js`) |

### 7.2 Application handling — `SOURCE VERIFIED` + `AUTOMATED VERIFIED`

`src/qortal/environment.ts` reads the globals through `typeof`-guarded
accessors, memoizes once per document, percent-decodes `_qdnName` for display and
comparison, and exposes `getRouterBasename()` from `_qdnBase`. `readQdnEnvironment`
is pure with respect to the passed window and is covered by
`src/qortal/environment.test.ts` (8 tests). No component calls the raw global.

### 7.3 Owner-observable check available **in the currently published build**

The published build already contains a `_qdnName`-dependent string: on `/studio`,
the idle panel renders “checks whether that account is the current owner of the
publishing name “Shadow Archives””, and the string only appears when the injected
`_qdnName` decoded to a non-empty publisher name. If that quoted name is
**missing** in the published app, `_qdnName` was not injected as expected.

### 7.4 Instrumentation added (authorized, non-secret) — `AUTOMATED VERIFIED`, host result `NOT VERIFIED`

A bounded read-only **Host context diagnostics** block was added to `/studio`
only. It displays `_qdnService`, `_qdnName`, `_qdnIdentifier`, `_qdnContext`,
`_qdnBase` and `_qdnBaseWithPath` (plus bridge availability), marking
missing values as `not injected` and an empty value as `empty string`. It reads
nothing from the host: no `GET_USER_ACCOUNT`, no QDN read, no write, no account
or secret data. Two tests cover the populated and absent cases and assert that no
permission/account request is issued.

**Important honesty note.** The block is in the working tree, **not** in the
currently published build. It therefore cannot verify the *currently served*
frame; it makes the exact `_qdn*` values owner-readable at the next
owner-authorized publication (or in any other authenticated render session that
serves a build containing it). Until then, `_qdn*` in the live frame remains
`NOT VERIFIED` at exact-string level, with §7.1/§7.3 as the available evidence.

## 8. Routing and lazy chunks in the real APP context

- `SOURCE VERIFIED`: `createBrowserRouter(appRoutes, { basename: getRouterBasename() })`
  (`src/app/router/router.tsx`), `base: ''` and relative asset URLs in
  `vite.config.ts`/`dist/index.html` — the current verified Q-App pattern.
- `SOURCE VERIFIED`: only `HomePage` is in the startup graph; Blog, Videos,
  Gallery, About, Contact, Category, Tag, Search, NotFound and Studio are lazy
  `import()` chunks (`src/app/router/routes.tsx`).
- `SOURCE VERIFIED`: routes exist for Home, `/blog`, `/blog/:id`, `/videos`,
  `/videos/:id`, `/gallery`, `/gallery/album/:id`, `/gallery/item/:id`,
  legacy `/gallery/:id`, `/about`, `/contact`, `/category/:slug`, `/tag/:slug`,
  `/search`, `/studio`, `*`.
- `AUTOMATED VERIFIED`: route table and lazy boundaries are covered by
  `src/app/router/routes.test.tsx`; the built bundle emits 19 JavaScript files
  under `dist/assets` — the entry chunk, 15 lazy route modules, the shared
  `format` chunk and two lazy shared list chunks — so no route is in the startup
  graph.
- `OWNER RUNTIME VERIFIED`: route pages open and primary navigation works
  (owner-observed).
- `NOT VERIFIED`: **hard reload / deep-load** of a deep route (for example
  `/blog/<id>` loaded directly, not via in-app navigation). Core's
  `APP` custom-routing fallback to `index.html` is source-verified, but the
  actual deep-load in the owner's host was not exercised. This does not block
  anything else and is listed as an owner check in §22.
- Assets resolve under `_qdnBase` because every emitted URL is relative and Core
  injects `<base href="/render/APP/Shadow%20Archives/">`; a non-default
  identifier — which would trigger query rewriting — is deliberately not used.

## 9. External Qortal app links (Q-Tube, SubWire, Quitter)

- `SOURCE VERIFIED`: `src/components/layout/PrimaryActions.tsx` renders **real
  anchors** with `href` built by `buildQortalAppUrl()` →
  `qortal://APP/<encodeURIComponent(name)>` (`src/qortal/navigation.ts`), for
  names `Q-Tube`, `SubWire`, `Quitter` from `siteConfig.externalApps`.
- `SOURCE VERIFIED`: no Web2 workaround exists. A repository-wide search for
  `window.open`, `location.href`/`assign`, `target="_blank"` and `http(s)://`
  found no navigation workaround — the only external string in `src/` is the
  unused repository URL in configuration text.
- `OWNER RUNTIME VERIFIED`: the primary action buttons work in the published app.
- `NOT VERIFIED`: per-app confirmation that each of the three opens a new tab via
  the host's `LINK_TO_QDN_RESOURCE` interception rather than an in-frame
  behaviour. No code change was made — the mechanism matches the verified Core
  `q-apps.js` link interception and no defect was observed.

## 10. Owner capability — exact real-host test

`OWNER RUNTIME VERIFIED` for a partially completed earlier run is **not**
available: the flow has not been exercised in a real host yet. The following is
the exact owner sequence, and the application-side guarantees it should confirm.

Preconditions: open `qortal://APP/Shadow Archives` in Qortal Hub (or another
Qortal host) with the account that owns the `Shadow Archives` name
(`QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`), then open `/studio`.

1. **Before clicking anything** — `SOURCE VERIFIED` + `AUTOMATED VERIFIED`:
   loading `/studio` issues **no** `GET_USER_ACCOUNT`; no Hub permission dialog
   appears; capability stays unverified/read-only. (`StudioPage.test.tsx`
   "issues no permission request on load".) Expected to observe: the "Owner
   mode" panel with the **Enter owner mode** button.
2. **Click "Enter owner mode"** — expected: exactly **one** Hub account-access
   permission flow; after approval the app resolves the account, then
   `GET_ACCOUNT_NAMES` and `/names/Shadow Archives`, and reports
   **"Owner capability verified"** with the publishing name, a shortened
   connected address and the owned-name count.
3. Because the connected account owns the name, state must become `owner`; if the
   account does **not** own it the app must report "Signed in — not the owner".
   Owner name/address are resolved at runtime and never hardcoded.
4. **No publishing/editor controls exist** — the owner panel shows only status
   and capability controls. Expected buttons: `Re-check ownership` and
   `Sign out of owner mode`.
5. **Sign out of owner mode** then **Enter owner mode** again if required:
   sign-out clears all capability state; re-entry issues a fresh request. A
   remembered or session permission may be returned without a new dialog — that
   is the accepted path, not a loop.
6. **If permission is declined** — expected: `permission-denied` state, the app
   stays usable read-only, **no automatic retry**, and an explicit `Try again`
   button. A cached rejection is never replayed automatically.

## 11. Owner-capability diagnostics rules

The fail-closed rules are `SOURCE VERIFIED` and `AUTOMATED VERIFIED`, not merely
intended: `deriveCapability()` (`src/qortal/capability.ts`) returns `unknown`
when the bridge is absent or the context is the dev proxy, reports `owner` only
when the connected address equals the **current** owner resolved from
`/names/{name}`, and returns `unknown` (never owner) when resolution finishes
without a positive answer. No payload `author`/`owner` field participates, no
address or name is hardcoded, `GET_USER_ACCOUNT` is never bypassed, and no
render/proxy path grants owner automatically. `capability.test.ts` (13 tests) and
`auth-isolation.test.tsx` cover these, including a name-transfer revocation case.

## 12. QDN read pipeline in the real host

- `SOURCE VERIFIED` + `AUTOMATED VERIFIED`: the visitor path is catalog-first
  (`DOCUMENT`/`saw_cat_manifest`), then bounded `SEARCH_QDN_RESOURCES` fallback
  discovery under the `saw_` prefix, with `mode: 'ALL'`, bounded pages, and no
  body/media fetch for listings. It never authenticates.
- Truthful no-catalog states: with no catalog and a successful empty search the
  snapshot is `partial` with "the archive catalog index is unavailable. A bounded
  live search found no matching resources; **this is not proof** that the archive
  is empty"; a failed catalog **read** is reported as `error` rather than silently
  downgraded; a dead bridge yields `unavailable` (`src/services/contentRepository.ts`).
- `NOT VERIFIED` (real host): that `SEARCH_QDN_RESOURCES` through the injected
  `q-apps.js` reaches the owner's node and returns one of those truthful states in
  the published frame. The code path is verified against the pinned Core
  `q-apps.js` field mapping; the live round trip is not.
- No Shadow Archives content/catalog entities are expected to exist yet
  (catalog publication is not implemented). Nothing was fabricated to populate
  the page.

## 13. QDN content media path

`NOT VERIFIED`, and it stays that way deliberately. Thumbnails would resolve via
`buildQdnResourcePath()` → same-origin `/arbitrary/<service>/<name>[/<identifier>][?filepath=…]`
(`src/qortal/qdn.ts`), mirroring the verified non-link branch of Core's
`buildResourceUrl()`. There is no content entity, hence no real QDN image to
serve, and no write was performed to create one. The **local banner** is a
bundled app asset (`src/assets/banner-shadow-archives.webp`) served from the APP
resource itself and is **not** evidence about arbitrary QDN `IMAGE`/`THUMBNAIL`
serving.

## 14. Clipboard

`NOT VERIFIED`. The three-step cascade
(`navigator.clipboard.writeText` → selected-text `execCommand('copy')` → manual
selectable input) is implemented and unit-tested
(`src/features/content/richText/clipboard.ts`,
`clipboard.test.ts`), but the in-iframe behaviour depends on a stored content
entity with a Web2 link, which does not exist. No QDN post was created to test
it. This does not block further architecture work.

## 15. CSP

- `SOURCE VERIFIED` (guide/Core): render CSP is
  `default-src 'self' 'unsafe-inline' 'unsafe-eval'; font-src 'self' data:; media-src 'self' data: blob: http://127.0.0.1:* http://localhost:*; img-src 'self' data: blob:; connect-src 'self' wss: blob:`.
- `AUTOMATED VERIFIED`: no third-party origin is referenced by the shipped app —
  the built CSS contains no external `url(...)`, and no runtime `fetch`/image
  reference points at an external origin.
- `OWNER RUNTIME VERIFIED` (partial): the owner observed startup, styling and
  route pages rendering, which is runtime evidence that the shell stylesheet,
  banner and the lazy route chunks actually load under the real CSP.
- `NOT VERIFIED`: a console-level CSP-violation review, and specifically
  DOMPurify/blog-detail behaviour, which needs a real stored Blog entity.

## 16. Visual baseline

Unchanged. No design token, palette, stylesheet or layout change was made in
this task. Exact colour-code fine-tuning remains owner-deferred and is expected
to be a small future token patch. The parchment baseline committed as `6354c88`
is byte-identical to the served build's CSS
(`assets/index-CQebDnmN.css`, SHA-256
`3314cb8769b37d488cc2b9c198973eb563d0a4db765dee95530161e2065dd714` in both
artifacts).

## 17. Studio discoverability

Unchanged. `/studio` remains outside primary navigation and is not linked from
the footer; it is reachable only by direct route. A discreet owner/footer entry
remains an open future product decision, not changed here.

## 18. Test and build regression

Application repository, after the diagnostics addition:

| Command | Result |
| --- | --- |
| `npm run lint` | PASS (no output) |
| `npm run typecheck` | PASS |
| `npm test` | PASS — 32 files / **303 tests** |
| `npm run build` | PASS — `tsc -b && vite build` |
| `npm run format:check` | PASS |
| `git diff --check` | PASS (clean) |

Build output (Node/local, `dirty: true` because of the uncommitted diagnostics
change): entry `dist/assets/index-*.js` 383082 B (gzip 120.46 kB per Vite),
stylesheet 25755 B (gzip 5.01 kB), Studio chunk 6685 B (gzip 2.21 kB). The
diagnostics code stayed **out of the startup graph**: the new entry chunk is
byte-equivalent to the `6354c88` entry chunk modulo chunk-name strings, and the
string "Host context diagnostics" appears only in the Studio chunk.

Workspace repository:

| Command | Result |
| --- | --- |
| `bash -n tools/validate-workspace.sh` | PASS |
| `bash tools/validate-workspace.sh` | PASS (5 hygiene warnings for human review; all pre-existing and expected) |

Validation did not modify the user's worktree beyond the two intended
application source files.

## 19. Feature-phase boundary

Not started, as instructed: no Gallery/Blog/Video publishing, no TipTap editor,
no Q-Tube/SubWire publishing research, no catalogs, likes, comments, tips,
Q-Mail or search-index implementation. The only code change is the read-only
`/studio` diagnostics block authorized by the task.

## 20. Self-audit

| Check | Result |
| --- | --- |
| Public-node evidence mislabelled as real-host evidence | **Clear.** §4 evidence is labelled `PUBLIC-NODE VERIFIED`; §6 is labelled `OWNER RUNTIME VERIFIED`; `_qdn*` in the live frame is `NOT VERIFIED`. |
| Owner observations mislabelled as automated evidence | **Clear.** §6 keeps them owner-level and states they are not platform proof. |
| `READY` treated as intended-revision proof | **Clear.** The resource was never `READY` here; revision identification used chain metadata + file-set correlation, and `READY` is explicitly rejected as revision proof in §5. |
| Owner granted without current name ownership | **Clear.** `deriveCapability` requires the connected address to equal the current `/names/{name}` owner; tests cover transfer revocation. |
| `GET_USER_ACCOUNT` triggered on public browsing | **Clear.** Only the explicit `/studio` action issues it; tests assert zero account calls on load. |
| Debugging leaks account/private data | **Clear.** The diagnostics block shows only non-secret injected `_qdn*` values; no account data, no secrets, no `GET_USER_ACCOUNT`. |
| Visual baseline changed accidentally | **Clear.** No style/token changes; served CSS hash matches HEAD artifact. |
| APP write accidentally performed | **Clear.** Only HTTP `GET`s were issued. |
| Content write accidentally performed | **Clear.** No content, catalog or entity resource was created. |
| Feature phase accidentally started | **Clear.** §19. |
| Unresolved in-scope BLOCKER/HIGH | None. The two findings (served-revision mismatch, public data-plane unavailability) are recorded with owner actions rather than hidden. |

## 21. Files changed

Application repository (uncommitted, on top of `6354c88`):

- `src/features/owner/StudioPage.tsx` — added the bounded, read-only
  `HostContextDiagnostics` block on `/studio` only.
- `src/features/owner/StudioPage.test.tsx` — two tests for the diagnostics block.

Workspace repository:

- `docs/shadow-archives-webportal/validation/2026-09-12-real-qortal-host-validation-report.md` — this report (new file).
- `projects/shadow-archives-webportal.md` — current-state update (baselines,
  served-build identity, diagnostics, public-node availability finding).

Not modified: any existing style, routing, QDN-read, auth, capability or content
contract file; the pre-existing untracked owner report
`docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md`.

## 22. Remaining NOT VERIFIED items and exact owner actions

| Item | Status | Exact owner action |
| --- | --- | --- |
| `_qdn*` exact strings in the served frame | NOT VERIFIED (source-verified injection; indirect `_qdnName` check available) | On `/studio` in the published app, confirm the idle panel quotes “Shadow Archives”. Exact values require the new diagnostics block, i.e. a future authorized publication. |
| Hard reload / deep-load of a deep route in the host | NOT VERIFIED | In the published app open `/blog/<id>` (or any deep path) and hard-reload the frame; the APP must fall back to `index.html` and not 404. |
| Owner capability click flow end-to-end | NOT VERIFIED | Run the §10 sequence with the owning account and report what Hub showed. |
| `SEARCH_QDN_RESOURCES` live round trip through the injected bridge | NOT VERIFIED | On `/blog` or `/videos` in the published app, confirm the listing shows a truthful no-content state (expected: "not proof that the archive is empty") rather than an error. |
| QDN content media serving (`/arbitrary/…` for IMAGE/THUMBNAIL) | NOT VERIFIED, bounded | Not testable without a published content entity; do not publish one just to test. |
| In-host clipboard cascade | NOT VERIFIED, bounded | Not testable without stored content carrying a Web2 link. |
| Console CSP-violation review; DOMPurify/blog detail | NOT VERIFIED, bounded | Requires a real stored Blog entity. |
| Per-app Q-Tube/SubWire/Quitter new-tab interception | NOT VERIFIED (mechanism source-verified, buttons owner-confirmed working) | Observe whether each button opens a new tab on the target app. |
| Raw served bytes hash-verified against the artifact | NOT VERIFIED | Retry later, or from a node that has the data; the public nodes tested could not serve it. |
| Public availability of the published APP data | Finding | Keep the publishing node online, or re-publish when convenient (requires a new owner authorization); the served revision is otherwise unchanged. |

## 23. No-write statement

**No QDN write, transaction, publication, update, deletion, content write,
like, comment, tip or Q-Mail send was performed.** Every network request in this
task was an HTTP `GET`:

- `GET https://api.qortal.org/blocks/height`, `/blocks/byheight/2720709`
- `GET https://api.qortal.link/blocks/height`
- `GET {node}/arbitrary/resource/status/APP/Shadow%20Archives[/default][?build=true]`
- `GET {node}/arbitrary/resources/search?service=APP&query=Shadow&includeMetadata=true`
- `GET {node}/arbitrary/metadata/APP/Shadow%20Archives/default`
- `GET {node}/arbitrary/resource/request/peers/APP/Shadow%20Archives/default`
- `GET {node}/transactions/signature/5fVoqGEc…`
- `GET {node}/names/Shadow%20Archives`
- `GET {node}/arbitrary/APP/Shadow%20Archives/default/{build.json,index.html,sa-avatar.png,assets/index-CAMO8KQj.js}` (all 404)
- `GET {node}/render/APP/Shadow%20Archives/` (503)

Nothing was committed, pushed, tagged or released. No SSH tunnel was used or
created.

## 24. Git state

| Repository | HEAD | Worktree |
| --- | --- | --- |
| Application | `6354c88` (unchanged) | modified: `src/features/owner/StudioPage.tsx`, `src/features/owner/StudioPage.test.tsx` (uncommitted per task authority) |
| Workspace | `38cd2e0` (unchanged) | modified: `projects/shadow-archives-webportal.md`; new: this report; pre-existing untracked owner report left untouched |

Report saved:
/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/validation/2026-09-12-real-qortal-host-validation-report.md
