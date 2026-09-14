# Shadow Archives Webportal — Owner Blog Publishing with native SubWire interoperability and an optional Quitter announcement

> **Subsequent owner acceptance — 2026-09-13: OWNER-RUNTIME PASS.** Gallery,
> Video/Q-Tube, Blog/SubWire and optional Quitter announcement are accepted.
> This supersedes earlier FUTURE / NOT VERIFIED or owner-validation-pending
> statements for those surfaces only. Original observations below remain a dated
> historical record; no new runtime test is claimed by this update.
> See [checkpoint and pinned evidence](../handoffs/2026-09-13-owner-runtime-checkpoint.md).
> Implementation executor: DeepSeek; acceptance: owner; update writer: Codex Local.


**Date:** 2026-09-13
**Type:** feature vertical implementation (Blog owner publishing + cross-app interoperability)
**Executing agent:** DeepSeek
**Agent identity evidence (2026-09-13):** the executor is the local agent whose runtime is
`CODEX_HOME=/home/iffi/.codex-deepseek`, whose `config.toml` sets `model = "deepseek-flash"`,
`model_provider = "deepseek"` and `base_url = "https://api.deepseek.com/"`, and which runs with
`DEEPSEEK_API_KEY`. The CLI harness is Codex (`CODEX_VERSION=0.154.0`); per orchestration rules this
work is **not** attributed to Codex merely because the harness is Codex.
**Application:** `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
**Project context:** `projects/shadow-archives-webportal.md`
**Companion live validation report:**
`docs/shadow-archives-webportal/validation/2026-09-13-blog-subwire-quitter-contract-live-read-only-validation.md`
**Owner handoff:**
`docs/shadow-archives-webportal/handoffs/2026-09-13-blog-subwire-quitter-owner-live-validation-handoff.md`

**Owner authorization:** inspect/edit the local project; run tests/lint/typecheck/build; inspect and
update clean reference clones under orchestration rules; read-only Qortal nodes; inspect current
public SubWire/Quitter QDN resources.

**Not authorized / not performed:** live QDN publication, any transaction, any modification of
SubWire or Quitter, deploy/release, commit, branch change, push, tag, merge. No SubWire or Quitter
source was imported or vendored. No Shadow Archives Blog post exists on QDN as a result of this
work; the single remaining step is the owner's own authorized live-host publication.

---

## 1. Objective and exit criterion

**Objective.** One Shadow Archives owner workflow publishes a Blog post to QDN so that
(a) Shadow Archives discovers, lists and renders it, and (b) the *current* SubWire application
discovers and displays the same article naturally from QDN — without importing SubWire, without a
runtime dependency on SubWire, and without a fake integration. Additionally: investigate SubWire's
current Quitter cross-post and, only if the contract proves implementable independently, expose an
optional owner-controlled Quitter announcement.

**Exit criterion (not fully reachable without the owner).** owner → open the Blog publish modal →
compose → publish → exact QDN resources verified → Shadow Archives Blog listing discovers it →
detail renders correctly → reload persists → the current SubWire discovery contract discovers the
same article; and, if chosen, → owner explicitly announces on Quitter with its own approval. The
SubWire interoperability conditions are demonstrated from source + read-only live evidence; the
single remaining step is the owner's own authorized live publication.

## 2. Reference revisions (freshness gate, re-checked 2026-09-13)

| Repo | Branch | Revision | Local clone |
| --- | --- | --- | --- |
| `Qortal/qortal` (Core 6.1.9) | `master` | `108bf191d42d710ec617f535af30cfd82fc03c87` | same |
| `Qortal/Qortal-Hub` | `develop` (default) | `12a573b27246e8a626b24794830c6bc432d1b05d` | same |
| `Qortal/Subwire` | `master` | `a933a6c44d60db19cd219408e36c747aebcce994` | same |
| `Qortal/Quitter` | `master` | `4e4246c3283bcbc8e05e683260692ed36144f862` | same |
| `Qortal/qapp-core` | `master` | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` | same |

Note on the Hub: `git ls-remote refs/heads/master` now reports `f3b75daa...`, but the Hub's default
branch (`origin/HEAD`) is `develop`, still `12a573b2...`. The earlier pin referred to `develop`; both
are recorded here so the discrepancy is not silently ignored.

## 3. Verified SubWire publication/discovery contract

Derived from current source (`Qortal/Subwire` `a933a6c`, `qapp-core` `0f9d6ac`) and confirmed with
read-only live QDN evidence (see the companion validation report).

- **Identity math.** `qapp-core` derives identifiers with `hashWord(word, strength, publicSalt)` =
  `safeBase64(sha256(publicSalt + word)).slice(0, strength)`, where `safeBase64` maps `+`→`.`,
  `/`→`~`, `_`→`!` and strips `=`; then `buildIdentifier` returns
  `${appHash}-${entityPrefix}-${parentRef}-${uid}-v1`.
  SubWire uses `appName = 'subwire'`, `publicSalt = '0drEPfUciLNhQZF9NFBg6RLnwcff/g3Ic7mm3VrIJKw='`,
  `entityType = 'SUBWIRE_ARTICLE'` under `parentId = 'SUBWIRE_ROOT'`.
- **Article identifier prefix (live-verified):** `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-`.
- **Resource:** `service = DOCUMENT`, `name = <publisher>`, `data64 = base64(JSON article)`; Core
  metadata `title` truncated to 75 bytes, `description` to 180 bytes (SubWire's own
  `truncateByBytes`).
- **Payload schema:** `{ title, subtitle?, content (GFM Markdown), coverImage { name, src }, images?,
  media?, timestamp, name, type: 'essay'|'episode', published: true }`. The cover is *inline bare
  base64* of WebP bytes; SubWire renders it as literally `data:image/webp;base64,<src>`.
- **Discovery:** `SEARCH_QDN_RESOURCES { service: 'DOCUMENT', identifier: <prefix>, prefix: true,
  mode: 'ALL', reverse: true, limit: 20 }`; qapp-core adds `mode: 'ALL'` and `excludeBlocked: true`
  and drops hits with `size === 32` or `>= 5 MiB`. Confirmed in `pages/DiscoverPage.tsx`
  (`service: DOCUMENT, limit: 20, reverse: true, identifier: searchPrefix, prefix: true`).
- **No index/list resource is required** for an article to be discovered (prefix search only).
- **Deep link:** `qortal://APP/Subwire/article/<percentEncodedName>/<identifier>`; SubWire route
  `article/:name/:identifier` fetches the DOCUMENT by exact identifier.
- **Rendering gate:** SubWire has no structural validator; `ArticleCard`/`ArticlePage` read the
  fields directly and render `content` through `marked.parse(content, { breaks: true, gfm: true })`
  + `dangerouslySetInnerHTML` **without a sanitizer** — which is why the derived artifact escapes
  text (below).

## 4. Verified SubWire → Quitter cross-post contract

- **Mechanism:** a separate QDN `DOCUMENT` in **Quitter's own** namespace, not a SubWire resource and
  not a chat/social transaction. `SubWire/src/utils/quitterQdn.ts` hardcodes `appName = 'quitter'`,
  `publicSalt = '6hMqDBxky6j1G2wZEHgIiOeApj3x3CP8LQwg0Ok0RVc='` and builds
  `buildIdentifier(ENTITY_POST='POST', ENTITY_ROOT='ROOT', false)`.
- **Quitter post prefix (live-verified):** `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-`.
- **Payload:** `{ text, timestamp, name, images?: [{ src: <bare base64> }] }`, `service = DOCUMENT`,
  max 2 images; Quitter sniffs image magic bytes (`components/Post.tsx`). SubWire compresses the
  cover and attaches one image.
- **Text:** `New publication: <title>` + `qortal://APP/Subwire/article/<name>/<identifier>`.
- **Separate approval:** SubWire publishes it with its own `publishMultipleResources` call; it is an
  explicit, optional owner action.
- **Independently reproducible:** the identifier math, service and payload are all public contracts,
  so Shadow Archives performs the identical write directly with **no runtime dependency on SubWire
  or Quitter**. A partial failure (article succeeded, Quitter failed) affects only the announcement;
  an ambiguous Quitter submission is never retried automatically.

**Quitter support was therefore implemented** (prefilled text, explicit opt-in, its own approval,
truthful announced/ambiguous/failed outcome), because the contract is proven implementable without
modifying either app. Live evidence: SubWire's own cross-post for the existing Shadow Archives
article was found and read back (text references the article identifier, one WebP image attached).

## 5. Chosen architecture

```
Blog entity (Shadow Archives canonical: tiptap-json-v1 body + normalized bodyText)
  -> Shadow Archives catalog/listing/detail (authoritative; DOMPurify render boundary)
  -> shared QDN resources where compatible (saw_post_<id> DOCUMENT, saw_post_thumb_<id> THUMBNAIL)
  -> SubWire-compatible publication adapter  (services/subwireArticleContract.ts)   [derived artifact]
  -> optional Quitter announcement adapter    (services/quitterAnnouncementContract.ts) [separate write]
```

- The canonical body stays `tiptap-json-v1`; `domain/richTextMarkdown.ts` derives the GFM Markdown
  artifact and the normalized `bodyText` from that same document. The derived artifact is rebuildable
  and never authoritative.
- SubWire/Quitter knowledge is isolated in two adapter modules plus one shared identifier-math module
  (`services/qappIdentifierContract.ts`). Nothing from SubWire or Quitter is imported or bundled, and
  Shadow Archives has no runtime dependency on either UI.
- The whole Blog write path sits behind the lazy `features/blog/owner/BlogOwnerPanel.tsx` boundary,
  dynamically imported only for a positively verified owner, so TipTap, the cover pipeline and the
  adapters never enter the visitor startup graph (confirmed by the production build chunking).

## 6. Exact QDN resource / identifier model (one post, stable id `<id12>`)

| Resource | Service | Identifier | Notes |
| --- | --- | --- | --- |
| Shadow Archives entity (authoritative) | `DOCUMENT` | `saw_post_<id>` | `tiptap-json-v1` body + `bodyText`; catalog source of truth |
| Cover | `THUMBNAIL` | `saw_post_thumb_<id>` | WebP, app cap 320 KiB, Core cap 500 KiB |
| SubWire-compatible article (derived) | `DOCUMENT` | `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-<id>-v1` | GFM Markdown + inline WebP base64 cover; Core title ≤75 B, description ≤180 B |
| Derived Blog index | `DOCUMENT` | `saw_cat_post_p###` + `saw_cat_manifest` | rebuildable listing index |
| Optional Quitter announcement | `DOCUMENT` | `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-<id>-v1` | only after an explicit owner action + approval |

The derived identifiers replace qapp-core's random 15-char uid with the Shadow Archives 12-char stable
id, so the cross-app coordinate is recoverable from the canonical id and an explicit retry overwrites
instead of duplicating. The uid is opaque to both consumers (prefix discovery + exact-identifier
fetch), and the derived prefixes were confirmed against real QDN search results.

## 7. Publish workflow and truthful states

Stages (each with a fresh owner-authority re-verification and its own host approval):
1. cover (`THUMBNAIL`);
2. authoritative entity + derived SubWire-compatible article (one grouped approval, per-resource
   outcomes preserved);
3. derived Blog index (partition + manifest).

Then, only if the owner opted in and only after the article is acknowledged, the optional Quitter
announcement runs as a **separate** write with its own approval.

Reported outcomes: `published`, `index-incomplete` (article authoritative, index failed/timed out),
`partial` (some article-stage resource failed — points at the authoritative entity and to Verify),
`ambiguous` (timeout; never auto-retried), `failed`. The Quitter step reports `announced` /
`ambiguous` / `failed`, and `declined` by the owner. The whole operation is never reported as failed
while the authoritative article exists.

## 8. Rich text and security boundary

- Canonical representation stays `tiptap-json-v1` (owner decision D4); the editor is TipTap
  (`features/blog/owner/BlogEditor.tsx`), prose only, with a link toolbar restricted to
  `http/https/qortal/mailto`.
- `domain/richTextMarkdown.ts` derives GFM Markdown for the SubWire artifact: literal text is
  Markdown-escaped, link/image URLs are scheme-allowlisted, unknown nodes are traversed instead of
  dropped, and inline code spans are kept literal. The only raw HTML emitted is the fixed `<u>…</u>`
  underline wrap. This matters because SubWire's renderer has **no** sanitizer.
- Shadow Archives' own rendering keeps its DOMPurify boundary (`features/content/richText/SafeRichText`).

## 9. Files changed (Blog vertical)

New:
- `src/domain/blogMedia.ts` — single-sourced cover policy.
- `src/domain/richTextMarkdown.ts`, `src/domain/richTextMarkdown.test.ts`
- `src/services/qappIdentifierContract.ts` — mirrored qapp-core identifier math.
- `src/services/subwireArticleContract.ts`, `src/services/subwireArticleContract.test.ts`
- `src/services/quitterAnnouncementContract.ts`, `src/services/quitterAnnouncementContract.test.ts`
- `src/services/blogPublishService.ts`, `src/services/blogPublishService.test.ts`
- `src/features/blog/owner/BlogEditor.tsx`, `BlogPublishModal.tsx`, `BlogOwnerPanel.tsx`,
  `blogPublishFeedback.tsx`, `blogOwner.css`, `BlogPublishModal.test.tsx`
- `scripts/live-blog-interop-check.ts` — read-only live interop check.

Modified:
- `src/domain/identifiers.ts` — `buildBlogThumbnailIdentifier` / `parseBlogThumbnailIdentifier`.
- `src/domain/catalog.ts` — `listingFromBlogPost`.
- `src/domain/index.ts` — re-exports.
- `src/services/catalogWriter.ts` — `catalogEntryFromBlogPost`.
- `src/services/contentRepository.ts` — route `blog-post` entities into the listing builder.
- `src/features/blog/BlogPage.tsx` — lazy owner panel behind `useCapability().isOwner`.
- `package.json` / `package-lock.json` — `@tiptap/react`, `@tiptap/starter-kit`, `@tiptap/pm` `^3.31.3`.
- `README.md` — documents the Blog/SubWire/Quitter contract and updates stale phase text.

The worktree also contains the pre-existing, uncommitted **Video/Q-Tube vertical** and shared
refactors; those were preserved and not reverted.

## 10. Validation results

- `npm test` — **51 files, 562 tests passed**.
- `npx tsc -b` — clean.
- `npm run lint` — clean.
- `npm run build` — clean; visitor entry `index-*.js` 393 kB contains **no** TipTap/ProseMirror
  symbols; the owner chunk `BlogOwnerPanel-*.js` (~436 kB) is separate and lazy.
- `npm run format:check` — clean (blog-scope files formatted).
- `git diff --check` — clean.
- Live read-only interop check — see the companion validation report.
- Flake note: one full run under heavy load reported a single non-reproducible failure (only the
  summary was retained, so the test identity was not captured). Three subsequent full runs passed
  562/562, and the Blog files passed 29/29 five times in a row under stress. The flake is not in the
  Blog tests and is recorded here rather than hidden.

## 11. Adversarial self-audit — findings and remediation

All in-scope BLOCKER/HIGH findings below were remediated during this session.

1. **List rendering fidelity (MEDIUM→fixed).** Multi-paragraph / nested list items lost their
   continuation indentation in the derived Markdown, which would flatten SubWire's rendering. Fixed;
   nested lists no longer double-indent.
2. **Inline-code double escaping (LOW→fixed).** Code spans had Markdown escapes applied, so a
   downstream renderer would show backslashes. Fixed: code spans are literal.
3. **Index failure reasons dropped (MEDIUM→fixed).** A `failed` (not `partial`) index-stage attempt
   reported an empty `failures[]`, losing the per-resource reason. Fixed to report both.
4. **Non-WebP cover published (HIGH→fixed).** The image pipeline only *warns* if the browser encodes
   a different type; SubWire renders the cover as literally `data:image/webp`, so a non-WebP cover
   would appear broken. The publication now fails closed with a truthful `cover-processing` error.
5. **Quitter collapse hid the article link (MEDIUM→fixed).** Quitter truncates a post's displayed
   text at `MAX_TEXT_LENGTH = 280`; with the excerpt before the URLs the article reference could be
   hidden. The prefilled text now puts both article references immediately after the title (mirroring
   SubWire's own share shape) and the excerpt after.
6. **Dead/duplicated cover policy (LOW→fixed).** `blogMedia.ts` was unused and the policy inlined
   elsewhere; it is now the single source used by the service and modal.
7. **Lint error in the editor (LOW→fixed).** `BlogEditor`'s link toolbar synced state in an effect;
   it now subscribes to the editor's own selection/transaction events.
8. **Chunking warning (LOW→fixed).** `subwireArticleContract` was both statically and dynamically
   imported; the dynamic import was removed.

Verified as correct (no change needed): the identifier math is byte-exact (the live search using our
computed prefix returns real SubWire articles); Core metadata values stay within Core's
`MAX_TITLE_LENGTH=80` / `MAX_DESCRIPTION_LENGTH=240` / `MAX_TAG_LENGTH=20` / `MAX_TAGS_COUNT=5`; the
derived artifact cap (4 MiB) stays under qapp-core's `>= 5 MiB` discovery drop; `catalogIdIsTaken`
prevents id reuse; the deep-link form follows the project's verified Phase 1A convention
(`encodeURIComponent(appName)`), matching SubWire's own encoded-name convention.

## 12. Residual risks / not tested

- **SubWire's global first page.** SubWire discovers with `limit: 20, reverse: true` and no name
  filter; a publication can be pushed off the first page by newer SubWire articles (SubWire's own
  pagination behaviour, not controllable from Shadow Archives).
- **Per-node propagation lag.** Fresh resources can return `404 Data unavailable` on one node while
  another serves them (observed live). Verification reports `present: false` truthfully rather than
  claiming success.
- **No live publication was performed** (out of authorization). The single owner live-host
  validation remains pending; it is the authoritative gate.
- **Browser WebP encoding** is required for the cover; a browser unable to encode WebP now fails
  closed rather than publishing a broken SubWire cover.
- **Quitter long-title collapse** remains a display property of Quitter for very long titles.
