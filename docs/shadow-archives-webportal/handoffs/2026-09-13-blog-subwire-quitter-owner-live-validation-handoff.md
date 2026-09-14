# Shadow Archives — Owner Blog Publishing + SubWire Interop (+ optional Quitter): Owner Handoff

> **Subsequent owner acceptance — 2026-09-13: OWNER-RUNTIME PASS.** Gallery,
> Video/Q-Tube, Blog/SubWire and optional Quitter announcement are accepted.
> This supersedes earlier FUTURE / NOT VERIFIED or owner-validation-pending
> statements for those surfaces only. Original observations below remain a dated
> historical record; no new runtime test is claimed by this update.
> See [checkpoint and pinned evidence](2026-09-13-owner-runtime-checkpoint.md).
> Implementation executor: DeepSeek; acceptance: owner; update writer: Codex Local.


**Date:** 2026-09-13
**Executing agent:** DeepSeek (runtime evidence: `CODEX_HOME=/home/iffi/.codex-deepseek`,
`model = "deepseek-flash"`, provider `deepseek`; CLI harness Codex `0.154.0` — not attributed to Codex).
**Status:** internally complete and ready for **one** owner live-host publication validation.
**Verdict:** Blog + SubWire interoperability **PASS by source + read-only live evidence**; final
owner live publication **PENDING** (not authorized in this session). Quitter announcement
**implemented** (contract proven; no SubWire/Quitter change required).

**Reports:**
- Implementation: `docs/shadow-archives-webportal/implementation/2026-09-13-blog-subwire-quitter-owner-publishing-implementation-report.md`
- Live validation: `docs/shadow-archives-webportal/validation/2026-09-13-blog-subwire-quitter-contract-live-read-only-validation.md`
- Live evidence: `docs/shadow-archives-webportal/live-evidence/2026-09-13-blog-subwire-quitter-live-read-only.json`, `…/2026-09-13-nodes-status.json`

**Git state:** branch `agent/shadow-archives-webportal/video-qtube-publishing`, HEAD
`472f244bd8cbb8f6ef11d60d7ee1baaaac6c0c83` (`Fix Gallery bridge reads and media hydration`). All Blog
work is uncommitted on top of the pre-existing dirty Video/Q-Tube vertical; nothing was committed,
staged, stashed, reset or pushed. `git diff --check` clean.

---

## 1. Verified SubWire publication/discovery contract

Source `Qortal/Subwire` `master` `a933a6c44d60db19cd219408e36c747aebcce994`, `qapp-core` `master`
`0f9d6ac`; live-confirmed on both nodes.

- Identity: `qapp-core` `hashWord(word, strength, salt) = safeBase64(sha256(salt + word)).slice(0, strength)`
  with `+`→`.`, `/`→`~`, `_`→`!`, `=` stripped; `buildIdentifier` =
  `${appHash}-${entityPrefix}-${parentRef}-${uid}-v1`. SubWire: `appName 'subwire'`,
  salt `0drEPfUciLNhQZF9NFBg6RLnwcff/g3Ic7mm3VrIJKw=`, entity `SUBWIRE_ARTICLE`, parent `SUBWIRE_ROOT`.
- **Article prefix (live-verified):** `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-`.
- Resource: `DOCUMENT`, `name = <publisher>`, `data64 = base64(JSON)`; Core `title` ≤75 B,
  `description` ≤180 B.
- Payload: `{ title, subtitle?, content (GFM Markdown), coverImage { name, src }, timestamp, name,
  type: 'essay'|'episode', published: true }`; `coverImage.src` is **bare WebP base64** (SubWire
  renders `data:image/webp;base64,<src>`).
- Discovery: `SEARCH_QDN_RESOURCES { service: 'DOCUMENT', identifier: <prefix>, prefix: true,
  mode: 'ALL', reverse: true, limit: 20, excludeBlocked: true }`; no index/list resource required.
  qapp-core drops hits with `size === 32` or `>= 5 MiB`.
- Deep link: `qortal://APP/Subwire/article/<percentEncodedName>/<identifier>`.

## 2. Verified SubWire → Quitter cross-post contract

Source `SubWire/src/utils/quitterQdn.ts`; live-confirmed.

- A separate `DOCUMENT` in **Quitter's** namespace: `appName 'quitter'`, salt
  `6hMqDBxky6j1G2wZEHgIiOeApj3x3CP8LQwg0Ok0RVc=`, entity `POST`, parent `ROOT`.
- **Post prefix (live-verified):** `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-`.
- Payload: `{ text, timestamp, name, images?: [{ src: <bare base64> }] }`, max 2 images; Quitter
  sniffs image magic bytes.
- Text: `New publication: <title>` + `qortal://APP/Subwire/article/<name>/<identifier>`.
- Separate, optional, own approval (`publishMultipleResources`). Independently reproducible.
- Live: SubWire's cross-post for the existing `Shadow Archives` article was read back — text
  references the article identifier, one WebP image attached, `isQuitterRenderablePost === true`.

## 3. Was Quitter implemented? Yes

The contract is proven implementable from Shadow Archives with **no** SubWire or Quitter change, so
the optional Quitter announcement is implemented: an explicit opt-in checkbox, a prefilled
owner-editable text (references immediately after the title, mirroring SubWire, excerpt after — so
Quitter's 280-char collapse still shows the article link), and its own approval and outcome
(`announced` / `ambiguous` / `failed`, or declined). Its failure never changes the article outcome and
an ambiguous submission is never auto-retried.

## 4. Architecture

```
Blog entity (canonical tiptap-json-v1 + bodyText)
  -> Shadow Archives catalog/listing/detail (authoritative; DOMPurify boundary)
  -> shared QDN resources (saw_post_<id>, saw_post_thumb_<id>)
  -> services/subwireArticleContract.ts   (derived SubWire article)
  -> services/quitterAnnouncementContract.ts (optional separate Quitter write)
```

Adapters only; no SubWire/Quitter source imported or bundled; no runtime dependency on either UI.
The whole write path is inside the lazy `BlogOwnerPanel` boundary (owner-only), so TipTap and the
adapters stay out of the visitor startup graph (proven by build chunking).

## 5. Exact QDN resource / identifier model (`<id12>` = Shadow Archives stable id)

| Resource | Service | Identifier |
| --- | --- | --- |
| Shadow Archives entity (authoritative, `tiptap-json-v1`) | `DOCUMENT` | `saw_post_<id>` |
| Cover | `THUMBNAIL` | `saw_post_thumb_<id>` |
| SubWire-compatible article (derived) | `DOCUMENT` | `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-<id>-v1` |
| Derived Blog index | `DOCUMENT` | `saw_cat_post_p###` + `saw_cat_manifest` |
| Optional Quitter announcement | `DOCUMENT` | `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-<id>-v1` |

Quitter action model: one `DOCUMENT` write, `service = DOCUMENT`, `name = <publisher>`, `data64 =
base64({ text, timestamp, name, images? })`, cover as bare WebP base64, deterministic identifier so an
explicit retry overwrites instead of duplicating.

## 6. Outcome model

`published` · `index-incomplete` (article authoritative) · `partial` (points at the authoritative
entity + Verify) · `ambiguous` (timeout, never auto-retried) · `failed`; Quitter separately
`announced` / `ambiguous` / `failed` / declined. The whole operation is never reported failed while
the authoritative article exists; exact resource identities, the entity payload and the cover are
preserved in the result for Verify/recovery.

## 7. Files changed (Blog vertical)

New: `src/domain/blogMedia.ts`; `src/domain/richTextMarkdown.ts` (+test);
`src/services/qappIdentifierContract.ts`; `src/services/subwireArticleContract.ts` (+test);
`src/services/quitterAnnouncementContract.ts` (+test); `src/services/blogPublishService.ts` (+test);
`src/features/blog/owner/{BlogEditor,BlogPublishModal,BlogOwnerPanel,blogPublishFeedback}.tsx`,
`blogOwner.css`, `BlogPublishModal.test.tsx`; `scripts/live-blog-interop-check.ts`.
Modified: `src/domain/identifiers.ts`, `src/domain/catalog.ts`, `src/domain/index.ts`,
`src/services/catalogWriter.ts`, `src/services/contentRepository.ts`,
`src/features/blog/BlogPage.tsx`, `package.json`, `package-lock.json`, `README.md`.

Pre-existing uncommitted Video/Q-Tube work and shared refactors were preserved untouched.

## 8. Live read-only evidence (nodes `127.0.0.1:24991`, `:24992`; mainnet height 2723000)

- Derived prefixes returned real resources: SubWire `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-` (2 Shadow
  Archives articles), Quitter `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-` (2 Shadow Archives posts).
- SubWire article `…-J1KcSHZWmB52mwv-v1`: `isSubwireRenderableArticle === true`, title
  "Uncovering the past - exposing the truth", cover 229 236 bare-base64 chars.
- Quitter cross-post `…-OL35sQV20oxI6z0-v1`: `isQuitterRenderablePost === true`, text
  "New publication: Uncovering the past - exposing the truth", references `…-J1KcSHZWmB52mwv-v1`, 1 image.
- One resource returned `404 Data unavailable` on both nodes at capture time (propagation lag);
  recorded truthfully as not served.
- Reproduce: `npx vite-node scripts/live-blog-interop-check.ts http://127.0.0.1:24991 http://127.0.0.1:24992`.

## 9. Tests / build

`npm test` 51 files / 562 tests passed · `npx tsc -b` clean · `npm run lint` clean ·
`npm run build` clean (visitor `index-*.js` 393 kB, no TipTap/ProseMirror; separate lazy
`BlogOwnerPanel-*.js` ~436 kB) · `npm run format:check` clean · `git diff --check` clean.
One full run under heavy load showed a single non-reproducible failure (identity not captured —
only the summary was retained); three further full runs passed 562/562 and the Blog files passed
29/29 five times under stress.

## 10. Adversarial self-audit

Remediated: list continuation indentation; inline-code double escaping; index-stage failure reasons
dropped; **non-WebP cover would have broken SubWire (now fails closed)**; Quitter collapse hiding the
article link (references moved before the excerpt); dead cover-policy module wired in; editor
setState-in-effect lint; static+dynamic import chunking warning. Verified correct: byte-exact
identifier math, Core metadata limits, 4 MiB artifact cap under qapp-core's 5 MiB drop, id reuse,
deep-link convention.

## 11. Unresolved risks

- SubWire's global `limit: 20` first page can push a publication off-page (SubWire's own pagination).
- Per-node index/chunk propagation lag can briefly show `missing` on a strict Verify.
- No live publication performed; browser WebP encoding is required for the cover (fails closed).
- Quitter's 280-char display collapse still truncates very long titles.

## 12. ONE owner live-host validation procedure

1. Open the published Shadow Archives Q-App in a Qortal host as the verified owner; open **Blog**.
2. Click **Write a post**; compose title, body (TipTap), excerpt, cover, categories, tags, language.
3. Leave the Quitter opt-in **off** for the first pass; click **Publish article**; approve each Qortal
   step (cover, article, index).
4. Record the three exact identifiers shown (entity `saw_post_*`, thumbnail, SubWire-compatible).
5. Confirm the Shadow Archives **Blog** listing shows the post, open its detail, reload and confirm it
   persists.
6. Open **SubWire** in the host and confirm the same article appears in its discovery feed and renders
   (title, cover, body) — proving native SubWire discovery of the same QDN article.
7. (Optional) Return to the result, tick the Quitter opt-in / open the Quitter step, click **Post
   announcement to Quitter**, approve, and confirm Quitter shows the announcement with the article
   link and cover. Decline is a valid outcome; the article is unaffected.
8. If a step times out, do **not** resubmit blindly: use **Verify** first (it reuses the same
   identities, so a retry cannot duplicate).

## 13. Authorization boundary reminder

Not authorized / not performed here: live QDN publication, any transaction, modifying SubWire or
Quitter, deploy/release, commit, branch change, push, tag, merge.
