# Shadow Archives — Q-Tube Video Contract, Live Read-Only Validation

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
**Agent identity correction (2026-09-13):** this task was executed by **DeepSeek**
(the autonomous implementation agent). The earlier `Codex` attribution was
incorrect — it was inferred from the orchestration role/CLI profile rather than
from the actual executor — and is corrected above. This work must not be
attributed to Codex.
**Application:** `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
**Project context:** `projects/shadow-archives-webportal.md`
**Related implementation report:**
`docs/shadow-archives-webportal/implementation/2026-09-13-video-owner-publishing-implementation-report.md`

**Authorization scope:** read-only inspection of owner-controlled Qortal nodes,
read-only inspection of public QDN resources, read-only reference-clone
inspection. Nothing in this document published, overwrote or transacted
anything.

---

## 1. Environment

| Item | Value |
| --- | --- |
| Node A | `http://127.0.0.1:24991` |
| Node B | `http://127.0.0.1:24992` |
| `/admin/status` (both) | `isSynchronizing: false`, `syncPercent: 100`, `height: 2722895` |
| Core build (node A `/admin/info`) | `qortal-6.1.9-108bf19` |
| Core commit pin (reference clone) | `108bf191d42d710ec617f535af30cfd82fc03c87` |

```
$ curl -s http://127.0.0.1:24991/admin/info
{"currentTimestamp":1789311036195,"uptime":12179521,"buildVersion":"qortal-6.1.9-108bf19",
 "buildTimestamp":1783541043,"nodeId":"NgrZWCr5ZUFZz768gsfBcStPqJErWUekTS","isTestNet":false,"type":"full"}
```

Reference revisions re-checked as the current upstream heads on 2026-09-13
(`git ls-remote <repo> refs/heads/<branch>`):

| Repo | Revision |
| --- | --- |
| `Qortal/q-tube` `main` | `68c3ea706c4ab110ffa44a7f55f8e09bdf7e85ff` |
| `Qortal/Subwire` `master` | `a933a6c44d60db19cd219408e36c747aebcce994` |
| `Qortal/Qortal-Hub` | `12a573b27246e8a626b24794830c6bc432d1b05d` |
| `Qortal/qapp-core` (published 1.0.79) | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` |
| `Qortal/qortal` (Core 6.1.9) | `108bf191d42d710ec617f535af30cfd82fc03c87` |

---

## 2. Q-Tube discovery query against real QDN data

The exact request the Shadow Archives adapter issues for
`verifyVideoDiscovery` (`QTUBE_VIDEO_DISCOVERY_REQUEST` plus the publisher name):

```
$ curl -s "http://127.0.0.1:24991/arbitrary/resources/search?service=DOCUMENT\
&identifier=qtube_vid_&mode=ALL&reverse=true&limit=20&offset=0"
results: 20
 - The Freeze Dried Business  qtube_vid_where-is-freeze-drying-headed-_y8clcufet98_metadata
 - Professor Dave Explains    qtube_vid_everything-is-crumbling-for-de_lcesbwebno_metadata
 - decenter                   qtube_vid_9-11-predicted-in-the-media_9uye3r_metadata
 - Crypto Casey               qtube_vid_bitcoin-bull-market-confirmed-_ldc6lhyazmu_metadata
 - Qortal-News-Network        qtube_vid_tousi-tv-breaking-civil-war-in_NjmXS3_metadata
 ...
```

Identifier semantics proved empirically on the same node:

| Query | Result |
| --- | --- |
| `identifier=qtube_vid_` + `mode=ALL` | all of the publisher's videos (20 with multi-video publishers) |
| `identifier=qtube_vid_` + `mode=LATEST` | one (latest) video per publisher — Core `LATEST` groups per `(name, service)` |
| `identifier=qtube_vid_` + `mode=ALL` + `name=decenter` + `exactmatchnames=true` | 20 (only that publisher) |
| `identifier=qtube_vid_` + `mode=LATEST` + `name=decenter` + `exactmatchnames=true` | 1 |
| `identifier=qtube_vid_` + `mode=ALL` + `description=category:9;` | the category-filtered set (Q-Tube's category tab) |

Consequences for the adapter: `mode: 'ALL'` is mandatory for full discovery, no
`prefix` flag is set by Q-Tube (so the identifier match is a *substring* match),
and the category filter is a Core `description` substring search — which is why
the Core metadata description must keep the
`**category:<id>;subcategory:<sub>;code:<code>**` marker.

Node B returns the same publication set (ordering differs between nodes and
between queries — the adapter checks membership, never position).

---

## 3. A real Q-Tube publication payload

Fetched read-only from node A:

```
$ curl -s -o /tmp/sa-live/qtube-live-metadata.json -w "http=%{http_code} bytes=%{size_download}\n" \
  http://127.0.0.1:24991/arbitrary/DOCUMENT/decenter/qtube_vid_9-11-predicted-in-the-media_9uye3r_metadata
http=200 bytes=157268
```

Field summary (matches the adapter's `QtubeVideoMetadata` model field for field):

```
keys:            category, code, commentsId, duration, extracts, fileSize, filename,
                 fullDescription, htmlDescription, subcategory, title, version,
                 videoImage, videoReference, videoType
title:           "9-11 Predicted in the Media"
version:         1
category:        9                (number in this publication; Q-Tube's TS type is `string`)
subcategory:     ""
code:            "tyiok"
videoType:       video/mp4
filename:        "911_Predicted_.mp4"
fileSize:        165861683
duration:        3349.71
videoReference:  {name: "decenter", identifier: "qtube_vid_9-11-predicted-in-the-media_9uye3r", service: "VIDEO"}
videoImage:      "data:image/webp;base64,UklGRrSOAABXRUJQV..." (48,743 chars)
extracts:        4 data-URL frames (first: "data:image/webp;base64,UklGRlpIA")
commentsId:      "qtube_vid__cm_9uye3r"
```

The referenced media exists as a single `VIDEO` resource at the metadata
identifier minus `_metadata`:

```
$ curl -s "http://127.0.0.1:24991/arbitrary/resources/search?service=VIDEO\
&identifier=qtube_vid_9-11-predicted-in-the-media_9uye3r&mode=ALL&exactmatchnames=true&limit=5"
[('decenter', 'qtube_vid_9-11-predicted-in-the-media_9uye3r', None, 162438432)]
```

Core-level metadata of a Q-Tube metadata resource (the discoverability mirror):

```
$ curl -s ".../search?service=DOCUMENT&identifier=qtube_vid_&mode=ALL&reverse=true&limit=1&includemetadata=true"
title:       "Ask the Mates anything | MOONSHOTS AMA  #289"      (50-char slice)
description: "**category:12;subcategory:;code:nkzo0**The mates sit down ..."  (150-char slice)
```

---

## 4. Shadow Archives adapter vs. live data (parity proof)

Unit tests mirror Q-Tube's gate; the live payload was additionally run through
the adapter itself (read-only, `npx vite-node`, no writes):

```
adapter validity gate on LIVE payload: true
live videoReference: {"name":"decenter","identifier":"qtube_vid_9-11-predicted-in-the-media_9uye3r","service":"VIDEO"}
live metadata identifier is a Shadow Archives artifact? null      ← foreign ids are never claimed
discovery request the adapter verifies with: {"service":"DOCUMENT","identifier":"qtube_vid_","mode":"ALL","reverse":true,"limit":20,"offset":0}
derived media identifier: qtube_vid_9-11-predicted-in-the-media_9uye3r
```

The third line matters as much as the first: the Shadow Archives parser refuses
to interpret a native Q-Tube identifier as one of its own.

---

## 5. No Shadow Archives video was published by this work

```
$ curl -s ".../search?service=DOCUMENT&identifier=saw_vid_&mode=ALL&reverse=true&limit=10"
saw_vid_ DOCUMENT hits: 0 []
```

The only Shadow Archives publications visible on the node are the earlier
Gallery ones, which also prove the app's own metadata transport:

```
$ curl -s ".../search?service=DOCUMENT&identifier=saw_img_&mode=ALL&reverse=true&limit=3&includemetadata=true"
 - Shadow Archives  saw_img_askdqb7749wh  tags=['logos', 'shadow archives logo']
 - Shadow Archives  saw_img_zud9a5dwv350  tags=None
```

---

## 6. Source-confirmed transport facts (no live write required)

Read from the pinned Qortal Hub revision `12a573b2`:

- `src/qortal/get.ts` `publishMultipleQDNResources` → per resource:
  `result['tag'+i+1] = tags[i] || resource['tag'+i+1]`, so the app's
  `tags: ['qtube_vid_']` becomes Core `tag1`.
- per resource: `if (resource.file) { ... rawData = await fileToBase64(resource.file) }`
  then `publishData({ data64: rawData, ... })` → a `File` is accepted per
  resource in a grouped publish and encoded host-side.
- every resource's `name` must belong to the connected account, and the grouped
  fee is `fee × resources.length` (one approval dialog).
- per-resource failures are returned as `unsuccessfulPublishes` (genuine partial
  success, never a rollback) — the shape the Shadow Archives partial-result
  handling is built on.
- `identifier == null` is silently mapped to `'default'`; Shadow Archives always
  sets an explicit identifier.

Read from the pinned `Qortal/q-tube` revision `68c3ea70`:

- `src/utils/checkStructure.ts` `isValidVideoMetadata` — required `title`,
  `videoReference` (non-empty `name`/`identifier`/`service` in the Qortal
  service set) and `filename`; `duration`/`fileSize` optional.
- `src/pages/Home/Components/VideoList.tsx` drops any discovered payload that
  fails that gate (unless the connected user owns it), so the gate is the real
  display condition.
- `src/pages/Home/Components/VideoCardImageContainer.tsx` receives
  `frameImages={video?.extracts || []}` and does
  `frameIndex = (frameIndex + 1) % frameImages.length`: a metadata payload with
  an **empty** `extracts` array blanks the card image on hover, while a
  single-element array is safe. This is why the adapter seeds `extracts` with the
  poster frame instead of publishing an empty list.

---

## 7. What this evidence does and does not prove

**Proved read-only:** the discovery query shape, the identifier family and
substring semantics, the metadata field contract, the gate Q-Tube applies, the
`videoReference`/media-identifier convention, the Core-level metadata mirror
shape, the Hub's `tags`/`file` transport handling, and that no Shadow Archives
video has been published.

**Not proved (requires the owner's authorized live publication):** an actual
write through the real host bridge — specifically that a `File` survives
`parent.postMessage` into the host and is published, that the host's approval
dialog accepts the two-resource media group, and that a freshly published
metadata resource is returned by a live node's search index.
