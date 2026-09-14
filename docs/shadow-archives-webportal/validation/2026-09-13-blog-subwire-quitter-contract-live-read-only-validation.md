# Shadow Archives — Blog SubWire/Quitter Contract, Live Read-Only Validation

> **Subsequent owner acceptance — 2026-09-13: OWNER-RUNTIME PASS.** Gallery,
> Video/Q-Tube, Blog/SubWire and optional Quitter announcement are accepted.
> This supersedes earlier FUTURE / NOT VERIFIED or owner-validation-pending
> statements for those surfaces only. Original observations below remain a dated
> historical record; no new runtime test is claimed by this update.
> See [checkpoint and pinned evidence](../handoffs/2026-09-13-owner-runtime-checkpoint.md).
> Implementation executor: DeepSeek; acceptance: owner; update writer: Codex Local.


**Date:** 2026-09-13
**Type:** live read-only QDN validation (no publication, no transaction)
**Executing agent:** DeepSeek
**Agent identity evidence:** runtime `CODEX_HOME=/home/iffi/.codex-deepseek` with
`config.toml` `model = "deepseek-flash"`, `model_provider = "deepseek"`, `base_url =
https://api.deepseek.com/`, and `DEEPSEEK_API_KEY` set. The CLI harness is Codex
(`CODEX_VERSION=0.154.0`); the work is not attributed to Codex merely because of the harness.
**Application:** `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
**Related implementation report:**
`docs/shadow-archives-webportal/implementation/2026-09-13-blog-subwire-quitter-owner-publishing-implementation-report.md`

**Authorization scope:** read-only inspection of owner-controlled Qortal nodes, read-only inspection
of public QDN resources, read-only reference-clone inspection. Nothing in this document published,
overwrote or transacted anything.

---

## 1. Environment

| Item | Value |
| --- | --- |
| Node A | `http://127.0.0.1:24991` |
| Node B | `http://127.0.0.1:24992` |
| `/admin/status` (both) | `isSynchronizing: false`, `syncPercent: 100`, height `2723000` |
| Core build (`/admin/info`, node A) | `qortal-6.1.9-108bf19`, `isTestNet: false`, nodeId `NgrZWCr5ZUFZz768gsfBcStPqJErWUekTS` |

Raw capture: `docs/shadow-archives-webportal/live-evidence/2026-09-13-nodes-status.json`.
Raw interop capture: `docs/shadow-archives-webportal/live-evidence/2026-09-13-blog-subwire-quitter-live-read-only.json`.

Reference revisions re-checked as the current upstream heads on 2026-09-13:

| Repo | Branch | Revision |
| --- | --- | --- |
| `Qortal/Subwire` | `master` | `a933a6c44d60db19cd219408e36c747aebcce994` |
| `Qortal/Quitter` | `master` | `4e4246c3283bcbc8e05e683260692ed36144f862` |
| `Qortal/qapp-core` | `master` | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` |
| `Qortal/qortal` (Core 6.1.9) | `master` | `108bf191d42d710ec617f535af30cfd82fc03c87` |
| `Qortal/Qortal-Hub` | `develop` (default) | `12a573b27246e8a626b24794830c6bc432d1b05d` |

Reproduce:
```
npx vite-node scripts/live-blog-interop-check.ts \
  http://127.0.0.1:24991 http://127.0.0.1:24992
```

## 2. Identifier prefixes derived by the adapter, confirmed live

The prefixes were computed by `src/services/subwireArticleContract.ts` and
`src/services/quitterAnnouncementContract.ts` (mirrored qapp-core math), then used as `identifier`
with `prefix: true` in the exact search requests the two apps issue:

| App | Derived prefix | Live search result |
| --- | --- | --- |
| SubWire articles | `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-` | 20 DOCUMENT hits; 2 under `Shadow Archives` begin with this prefix |
| Quitter posts | `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-` | 20 DOCUMENT hits; 2 under `Shadow Archives` begin with this prefix |

That the derived prefix returns *real* SubWire/Quitter resources proves the mirrored
`hashWord`/`buildIdentifier` math is byte-exact against `qapp-core` `0f9d6ac`.

Search request issued (identical to the apps', with a name filter added only to prove the Shadow
Archives publication is found):
```
service=DOCUMENT&identifier=<prefix>&prefix=true&mode=ALL&reverse=true&limit=20&excludeBlocked=true&name=Shadow Archives
```

## 3. A real SubWire article (existing Shadow Archives publication)

Resource: `DOCUMENT` / `Shadow Archives` / `7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-J1KcSHZWmB52mwv-v1`

```
identifier           7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-J1KcSHZWmB52mwv-v1
served by            http://127.0.0.1:24992
gatePasses           true   (isSubwireRenderableArticle)
title                "Uncovering the past - exposing the truth"
type                 "essay"
published            true
contentChars         2321
coverBase64Chars     229236   (bare base64, NOT a data: URL)
```

This confirms live: `service = DOCUMENT`, bare-base64 WebP cover (rendered by SubWire as
`data:image/webp;base64,<src>`), and a payload that passes the same gate the adapter runs before
publishing. The second article hit under the same prefix
(`…-8fHVixazg6kxLOX-v1`) was **not served** by either node at the time of capture (`404 Data
unavailable`) — reported truthfully as `served: false`, not fabricated.

## 4. SubWire's own Quitter cross-post, read back

Resource: `DOCUMENT` / `Shadow Archives` / `MhNiRYdzkaP9dz-kX47dT-XrFXaYetyErMdF-OL35sQV20oxI6z0-v1`

```
gatePasses                true   (isQuitterRenderablePost)
textFirstLine             "New publication: Uncovering the past - exposing the truth"
referencesSubwireArticle  true
referencedIdentifiers     ["7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-J1KcSHZWmB52mwv-v1"]
imageCount                1
timestamp                 1789049960852
```

The full text is exactly SubWire's own share shape:
```
New publication: Uncovering the past - exposing the truth

qortal://APP/Subwire/article/Shadow%20Archives/7l1NGsWiY0SgPb-FJVWQM-T60ZadsfPsbLTh-J1KcSHZWmB52mwv-v1
```

This proves, against real data, that (a) the Quitter cross-post is a separate `DOCUMENT` in
Quitter's namespace whose text references the SubWire article identifier and attaches a WebP image,
and (b) Shadow Archives can reproduce the same write independently. The other Quitter hit
(`…-vGCdDrjPoqVCvbP-v1`) was not served by either node at capture time (`served: false`).

## 5. Deep-link resolution (Core source `108bf191`)

Verified in `qortal/src/main/resources/q-apps/q-apps.js`:

- `interceptClickEvent` (line ~717) intercepts anchors whose `href` starts with `qortal://`, calls
  `extractComponents`, and issues `LINK_TO_QDN_RESOURCE { service, name, identifier, path }`.
- `extractComponents` maps `qortal://APP/<appName>/<path...>` to `service = 'APP'`, `name = <appName>`,
  and treats the next segment as an identifier only when
  `/arbitrary/resource/status/APP/<appName>/<segment>` reports `totalChunkCount > 0`; otherwise the
  whole remainder is the in-app `path`.
- Consequently `qortal://APP/Subwire/article/Shadow%20Archives/<id>` resolves to SubWire's
  `article/:name/:identifier` route (name percent-encoded, as SubWire's own share text encodes it),
  and `qortal://APP/Shadow%20Archives/blog/<id>` resolves to Shadow Archives' `blog/:id` route
  (confirmed in `src/app/router/routes.tsx`).

The app-name encoding follows the project's already-verified Phase 1A navigation convention
(`src/qortal/navigation.ts#buildQortalAppUrl` uses `encodeURIComponent(appName)`), which is also what
SubWire's own cross-post text does for the author name.

## 6. What this validation does and does not prove

Proves: the adapter's derived SubWire/Quitter coordinates are real, discoverable, and correctly
shaped; the real SubWire article/Quitter cross-post pair exists on mainnet; the discovery requests
and the render gates match current source; the deep-link forms resolve.

Does **not** prove: a Shadow Archives article authored by this work being published and then found
by SubWire — that requires the owner's authorized live publication (no live write was permitted
here). It also does not prove SubWire's UI rendering pixel-for-pixel; the payload gate and format are
verified from source and data, not by driving the SubWire UI.
