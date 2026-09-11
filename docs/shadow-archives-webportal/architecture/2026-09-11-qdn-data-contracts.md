# Shadow Archives — QDN Data-Contract Specification (Phase 1A, owner-approved baseline)

- Project: `shadow-archives-webportal-QORTAL`
- Phase: 1A (architecture / contract design)
- Date: 2026-09-11
- Author: Codex (Phase 1A research)
- Status: **owner-approved contract baseline for Phase 1B, not yet implemented
  or published.** The owner recorded final Phase 1A decisions (D1–D9) on
  2026-09-11; identity, taxonomy, editor/rendering, Q-Mail fallback, UI
  dependency, Qortal integration, catalog, like-activeness and moderation
  states are marked inline. **D9's wire representation is DEFERRED**, and
  Q-Tube interoperability is **FUTURE / NOT VERIFIED**. Nothing here is
  published; every `NOT VERIFIED` item still requires runtime proof.
- Related: [`./2026-09-11-phase-1a-architecture-report.md`](./2026-09-11-phase-1a-architecture-report.md),
  [`./2026-09-11-performance-reference-comparison.md`](./2026-09-11-performance-reference-comparison.md),
  [`../../../agents/qortal-architecture-and-data-integrity.md`](../../../agents/qortal-architecture-and-data-integrity.md),
  [`../../../agents/qdn-publication-discovery-and-scaling.md`](../../../agents/qdn-publication-discovery-and-scaling.md)

## 1. Platform facts these contracts depend on

All VERIFIED (source-observed) against `Qortal/qortal` `108bf191` (v6.1.9) and
`Qortal/Qortal-Hub` `12a573b2`; live values re-checked against
`https://api.qortal.org` on 2026-09-11.

| Fact | Source |
| ---- | ------ |
| A resource is addressed by `(name, service, identifier)`; republishing the same triple overwrites it | architecture guide §2 |
| Publishing/overwriting requires **current ownership of `name`** at publish time | `ArbitraryTransaction.isValid()` (`INVALID_NAME_OWNER`) |
| Identifier max length is **64 UTF-8 bytes** (enforced at deserialisation) | `ArbitraryTransaction.MAX_IDENTIFIER_LENGTH` |
| `default`/empty identifier is normalised to `null` | `ArbitraryDataTransactionBuilder`, `ArbitraryDataFile` |
| Search `query` matches **name, identifier, title, description** only — never body | `ArbitraryResource.searchResources` |
| Identifier search is substring unless `prefix: true` | architecture/scaling guide §4 |
| `limit` applies only when `> 0`; `limit=0` = unbounded | `HSQLDBRepository.limitOffsetSql` |
| Search can return `tags`/`description`/`category` metadata via `includemetadata=true` | `ArbitraryResourceData`/`ArbitraryResourceMetadata` |
| Metadata limits: title ≤ 80, description ≤ 240, tag ≤ 20, max 5 tags | `ArbitraryDataTransactionMetadata` |
| Core `Category` is a fixed enum (~53 entries), one per resource | `org.qortal.arbitrary.misc.Category` |
| There is no on-chain delete; the framework "unlike/delete" convention is an overwrite | architecture guide §8 |
| Payload `author`/`owner` fields are untrusted | architecture guide §3 |
| `PUBLISH_QDN_RESOURCE` accepts `name`, `service`, `identifier`, `data64`/`base64`/`file`, `filename`, `title`, `description`, `category`, `tags[]`, `isMultiFileZip`, `encrypt`, `publicKeys` | Hub `src/qortal/get.ts` |
| `PUBLISH_MULTIPLE_QDN_RESOURCES` takes `resources[]` plus group-level `encrypt`/`publicKeys`; independent transactions, partial success possible | Hub `src/qortal/get.ts` |
| Production CSP blocks third-party origins | `ArbitraryDataRenderer` |

**Identifier content (INFERRED, low risk).** Core does not validate identifier
characters beyond the 64-byte cap, but the identifier is used as a URL path
segment and is percent-encoded by the host. Restrict Shadow Archives
identifiers to `[a-z0-9_]` so no encoding ambiguity can arise.

## 2. Identifier namespace

### 2.1 Candidate schemes

**Scheme A — `qapp-core` hashed identifiers.**
`buildIdentifier(appName, publicSalt, entityType, parentId)` →
`<appHash14>-<entityHash6>-<parentHash14>-<uid15>` (≈52 chars), using
`safeBase64` characters `.`, `~`, `!` and `-`.
Pros: framework-consistent, collision-resistant, parent-scoped, already used by
Subwire.
Cons: opaque (cannot grep or reason about an identifier); depends on a
`publicSalt` that must never change or every derived identifier breaks; sits
close to the 64-byte cap; uses non-alphanumeric characters; the published
`qapp-core` root import that provides it costs ~596 kB gzip (see the
performance comparison).

**Scheme B — readable app-prefixed, type-partitioned identifiers
(owner-approved namespace `saw_`).**
`saw_<type>_<id>` e.g. `saw_post_2f8k3qz1m4`.
Pros: readable, greppable, debuggable; prefix-search-friendly; deterministic;
far below the 64-byte cap; content-type partitioned; no salt dependency; deep
links can be resolved without the catalog when the stable id is embedded. The
`saw_` namespace is fixed (owner decision D1); schema evolution is carried by
the payload `schemaVersion`, not by a version digit in the namespace.
Cons: no cryptographic collision resistance (mitigated by id entropy: 12 chars
base36 ≈ 62 bits, publisher-scoped so cross-name collisions are irrelevant).

**Scheme C — hybrid: readable app prefix + type + target hash + uid.**
`saw_cmt_<targetType><targetId12>_<uid8>`.
Pros: enumerates a target's children with one prefix search; readable.
Cons: longer; still needs a random suffix for per-item uniqueness.

### 2.2 Recommendation (`OWNER APPROVED — D1`)

Use **Scheme B for top-level entities** and the Scheme C shape for
**target-scoped children** (comments, likes), i.e. one readable,
type-partitioned family under the approved `saw_` namespace:

| Entity | Identifier shape | Notes |
| ------ | ---------------- | ----- |
| Blog post | `saw_post_<id12>` | `id12` = 12-char base36 stable id |
| Video entry | `saw_vid_<id12>` | |
| Gallery item | `saw_img_<id12>` | |
| Gallery album | `saw_album_<id12>` | |
| Comment | `saw_cmt_<targetType><targetId12>_<uid8>` | one prefix search per target |
| Like state | `saw_lk_<targetType><targetId12>` | **no actor in the identifier**; scoped by publishing name |
| Moderation entry | `saw_mod_<targetType><targetId12>` | owner-published overlay |
| Moderation index | `saw_modindex` | single resource, avoids N+1 |
| Catalog partition | `saw_cat_<type>_p<NNN>` | |
| Catalog manifest | `saw_cat_manifest` | |
| Search-index partition | `saw_idx_<NNN>` | |
| Site config | `saw_cfg` | singleton |

`targetType` is a short token (`post`/`vid`/`img`/`album`/`cmt`). Longest realistic
identifier: `saw_cmt_vid<id12>_<uid8>` = 4+4+3+12+1+8 = 32 bytes — well inside
the 64-byte cap, leaving room for future additions.

Prefix searches this enables (all `prefix: true`, one query each):

- all posts: `saw_post_`
- all comments of one target: `saw_cmt_vid<id12>_`
- all likes of one target: `saw_lk_vid<id12>` (substring-safe because the tail is
  exactly `<id12>` with no further segment)
- all moderation entries: `saw_mod_`

## 3. Services

| Purpose | Service | Why |
| ------- | ------- | --- |
| Blog post, video entry, gallery item/album, catalog, search index | `DOCUMENT` | no Core size cap, current-app norm, accepts base64 JSON envelopes |
| Comment | `COMMENT` | purpose-built: single file, 500 KB cap, validated. Alternative: `BLOG_COMMENT` (matches q-tube/Quitter precedent) |
| Like state | `DOCUMENT` | tiny payload; must not use `JSON` because Shadow Archives publishes base64 envelopes, and `JSON` validates the decoded payload as JSON |
| Media (gallery/video) | `IMAGE`, `VIDEO`, `THUMBNAIL` | native services |
| Site config, moderation index | `DOCUMENT` (base64 JSON envelope) | consistency; `JSON`'s 25 KB cap is a hazard |
| Index resources (if adopted) | `DOCUMENT` | `JSON`'s 25 KB cap forbids real index partitions |

**NOT chosen.** `JSON` for catalogs/indexes (25 KB cap, validated only). `LIST`
is technically acceptable for the catalog (single file, no size cap) but no
inspected current app publishes a `LIST` catalog with defined semantics, so the
team would be inventing the format anyway; a `DOCUMENT` envelope with an
explicit `schemaVersion` is the lower-risk choice. `OWNER-neutral`.

## 4. Common envelope

Every Shadow Archives entity payload is a JSON object, UTF-8 encoded, then
base64-encoded into the host's `data64` field.

```jsonc
{
  "schemaVersion": 1,          // integer, required
  "kind": "blog-post",         // short discriminator, required
  "id": "2f8k3qz1m4",          // stable id, required, matches identifier
  "publisher": "Shadow Archives", // informational display hint ONLY
  "createdAt": 1767225600000,  // publisher clock (ms), untrusted for ordering
  "updatedAt": 1767225600000,  // publisher clock (ms)
  "state": "active",           // active | inactive | withdrawn
  "data": { }                  // kind-specific
}
```

Rules:

- `publisher` is a display hint and is **never** an authority test. Authority is
  the resource's `name` plus current name ownership.
- `createdAt`/`updatedAt` are content metadata. Ordering uses node-reported
  `created`/`updated` from search results, with the stable `id` as a
  deterministic tie-breaker.
- An unknown `schemaVersion` or `kind` is quarantined (not rendered), never
  guessed.
- Maximum envelope bytes: enforce a client-side cap per kind (recommended
  ≤ 256 KB for entities, ≤ 1 MB only for the catalog) and reject oversized
  payloads. Rationale: `DOCUMENT` has no Core cap, so the app must impose one.

## 5. Entities

### 5.1 Blog post

- **Purpose.** Owner-authored article with an optional thumbnail.
- **Authoritative publisher.** The Shadow Archives publishing name (current
  owner at publish time).
- **Service / identifier.** `DOCUMENT` / `saw_post_<id12>`.
- **Schema version.** 1.
- **Stable id.** `id` (12-char base36), embedded in the identifier.
- **Parent/target.** none.
- **Timestamps.** `createdAt`/`updatedAt` (publisher), node `created`/`updated`
  (ordering).
- **Mutability.** Mutable by the owner (republish the same identifier keeps the
  stable id and URL).
- **Deletion / tombstone.** `state: "withdrawn"` + `withdrawnAt`. Never a
  network delete. Removed from listings; the detail route renders an honest
  "withdrawn by the publisher" state.
- **Discovery.** Direct `name=<publisher>` + `identifier=saw_post_<id12>` for a
  known item; catalog for listings.
- **Authority validation.** Resource `name` must be the current app publisher
  name; payload must satisfy schema; identifier must match `saw_post_` + `id`.
- **Catalog representation.** One catalog entry (see §7).

```jsonc
"data": {
  "title": "string (<= 200)",
  "slug": "string (lowercase, [a-z0-9-])",
  "excerpt": "string (<= 300)",
  "body": { "format": "tiptap-json-v1", "doc": { /* ProseMirror doc */ } },
  "bodyText": "string (plain-text extract for search/index, <= 8 KB)",
  "thumbnail": { "service": "THUMBNAIL", "name": "<publisher>", "identifier": "<media id>" } | null,
  "categories": ["history"],
  "tags": ["archive", "declassified"],
  "language": "en"
}
```

### 5.2 Video entry

- **Purpose.** Metadata record for a video hosted on QDN (own video or a
  reference to another Qortal video app's resource).
- **Owner decision (2026-09-11).** Shadow Archives will publish its own video
  content to QDN. The architecture must also preserve a **future** capability
  for a Shadow Archives video to appear through the Q-Tube ecosystem. The exact
  Q-Tube publication/discovery/identifier contract is **FUTURE / NOT VERIFIED**
  and must not be treated as a current platform contract; Shadow Archives must
  not import Q-Tube source or depend on the Q-Tube application. The media
  reference intentionally uses verified QDN fields
  (`service`/`name`/`identifier`, plus `path` where applicable) so a future
  publication/discovery adapter can be added without rewriting the entity.
- **Publisher.** The Shadow Archives publishing name.
- **Service / identifier.** `DOCUMENT` / `saw_vid_<id12>`.
- **Parent/target.** `media` may reference an external `(service, name,
  identifier)`; a referenced resource is validated by exact identity and is
  **not** treated as owned by the publisher.
- **Mutability.** Mutable (metadata only; media replacement yields a new media
  identifier referenced in place).
- **Deletion/tombstone.** `state: "withdrawn"`.
- **Discovery.** Catalog; direct identifier for deep links.
- **Catalog representation.** One catalog entry with `durationSeconds` and
  thumbnail ref for card rendering.

```jsonc
"data": {
  "title": "string (<= 200)",
  "slug": "string",
  "description": "string (<= 2000)",
  "media": { "service": "VIDEO", "name": "<publisher>", "identifier": "<media id>", "mimeType": "video/mp4" },
  "externalMedia": { "service": "VIDEO", "name": "<other name>", "identifier": "<id>" } | null,
  "thumbnail": { "service": "THUMBNAIL", "name": "<publisher>", "identifier": "<id>" } | null,
  "durationSeconds": 0,
  "categories": [], "tags": [], "language": "en"
}
```

### 5.3 Gallery item

- **Purpose.** A single image (or short video) with metadata.
- **Service / identifier.** `DOCUMENT` / `saw_img_<id12>`; the binary media is a
  separate `IMAGE`/`VIDEO`/`THUMBNAIL` resource.
- **Parent/target.** Optional `albumId` linking to `saw_album_<id12>`.
- **Mutability.** Mutable metadata; media change yields a new media identifier.
- **Deletion/tombstone.** `state: "withdrawn"`.
- **Catalog representation.** One catalog entry with a thumbnail ref; originals
  are never included in the catalog or downloaded for listings.

```jsonc
"data": {
  "title": "string (<= 200)",
  "description": "string (<= 2000)",
  "albumId": "string | null",
  "media": { "service": "IMAGE", "name": "<publisher>", "identifier": "<id>", "mimeType": "image/webp" },
  "thumbnail": { "service": "THUMBNAIL", "name": "<publisher>", "identifier": "<id>" },
  "width": 0, "height": 0,
  "categories": [], "tags": [], "language": "en"
}
```

### 5.4 Gallery album

- **Justified?** Yes — the owner requires albums ("Gallery item/album where
  appropriate"), and album grouping must survive without the catalog.
- **Service / identifier.** `DOCUMENT` / `saw_album_<id12>`.
- **Deletion/tombstone.** `state: "withdrawn"`; items reference the album by id
  and are hidden if the album is withdrawn.
- **Catalog representation.** One catalog entry plus a derived `itemCount`.

```jsonc
"data": {
  "title": "string (<= 200)",
  "description": "string (<= 2000)",
  "coverThumbnail": { "service": "THUMBNAIL", "name": "<publisher>", "identifier": "<id>" } | null,
  "categories": [], "tags": [], "language": "en"
}
```

### 5.5 Comment

- **Purpose.** User-authored comment on any content entity.
- **Authoritative publisher.** **The acting registered Qortal name** (not the
  site owner). A comment's `name` is its authority.
- **Service / identifier.** `COMMENT` / `saw_cmt_<targetType><targetId12>_<uid8>`.
- **Stable identity.** The identifier. Editing republishes the same identifier
  under the same name.
- **Parent/target.** Explicit `target` object **and** optional
  `parentCommentRef`. The target is validated by exact
  `(service, name, identifier)`; a forged/mismatched target is rejected and
  quarantined.
- **Timestamps.** `createdAt` (payload) and `editedAt` (payload, absent until
  edited); node `created`/`updated` for ordering.
- **Mutability.** Only the authoring name may edit its own comment. Edit =
  republish same `(name, service, identifier)` with `editedAt` set and
  `editCount` incremented. Last write wins; the app must display "edited".
- **Deletion/tombstone.** The author may set `state: "inactive"` (rendered as
  "deleted by the author" placeholder, not removed). The owner's moderation
  overlay may hide a comment in-app only.
- **Discovery.** One prefix search per target
  (`identifier=saw_cmt_<targetType><targetId12>_`, `prefix: true`), paginated
  with `limit`/`offset`, `includemetadata=true`. Never one query per comment.
- **Authority validation.** Resource `name` is the author; the payload may
  contain an informational `displayName`, which is **never** authoritative.
- **Catalog representation.** Comment counts are a catalog snapshot only; the
  authoritative list is the per-target search.

```jsonc
"data": {
  "target": { "service": "DOCUMENT", "name": "<publisher>", "identifier": "saw_post_<id12>" },
  "parentCommentRef": "saw_cmt_..._<uid8>" | null,
  "body": { "format": "tiptap-json-v1", "doc": { } },
  "bodyText": "string (<= 4 KB plain text)",
  "displayName": "informational hint only"
}
```

### 5.6 Like state

- **Purpose.** The record of one acting name's like state for one target.
- **Owner decision status (D9).** The identity rule is **DECIDED**: one active
  like per acting registered Qortal name per content item. The exact
  active/inactive/tombstone **wire representation** is **DEFERRED** until a
  controlled QDN overwrite/runtime test selects it. Phase 1B may define an
  interface/type boundary but must not claim an unverified wire format; the
  `state` and metadata-tag shapes below are the proposed candidates only.
- **Authoritative publisher.** **The acting registered Qortal name.**
- **Service / identifier.** `DOCUMENT` / `saw_lk_<targetType><targetId12>`.
- **Uniqueness rule (owner decision, 2026-09-11).** Because `(name, service,
  identifier)` is unique, exactly one resource exists per acting name per
  target. The **actor is never encoded in the identifier**, so:
  - one name cannot create duplicate simultaneous active likes (re-like
    overwrites the same triple);
  - two different registered names, even of the same account, produce two
    different resources and are **never** deduplicated by address;
  - unlike and re-like update the same name-scoped identity.
- **Activeness.** `state: "active" | "inactive"` in the payload. Unlike
  republishes the same identifier with `state: "inactive"` and
  `inactiveAt`. **Raw resource count is never used as the active-like count.**
- **Metadata fast path (proposed; runtime verification required).** When
  publishing, also set a deterministic metadata tag: `saw_active` on like and
  `saw_inactive` on unlike, so a single `SEARCH_QDN_RESOURCES` with
  `includemetadata=true` can classify all of a target's likes without fetching
  each payload. Source-observed that search returns resource `tags`, and that a
  republish carries new metadata; the overwrite-behaviour must still be proven
  with one controlled publication.
- **Fallback.** If metadata state is missing/unreadable for a resource, fetch
  that payload (bounded, queued) before counting. If any resource remains
  unclassifiable, report `>= N` / "count partially available" — never a
  truncated total.
- **Discovery.**
  - count for one target: one search on `saw_lk_<targetType><targetId12>` with
    `prefix: true`, `includemetadata: true`;
  - the current user's own state: the same search already contains the caller's
    resource because results include `name`; no second query;
  - listing-card counts: from the catalog snapshot, labelled as of
    `compiledAt`, with exact values resolved on the detail view.
- **Catalog representation.** `likeCount` snapshot + `compiledAt`.

```jsonc
"data": {
  "target": { "service": "DOCUMENT", "name": "<publisher>", "identifier": "saw_post_<id12>" },
  "state": "active",
  "inactiveAt": null
}
```

### 5.7 Moderation overlay

- **Purpose.** Owner-controlled presentation filter. It hides content **in this
  application only**. It is not a network delete and must never be described as
  one.
- **Authoritative publisher.** The Shadow Archives publishing name (current
  owner).
- **Service / identifier.** `DOCUMENT` / `saw_mod_<targetType><targetId12>` for a
  single record, plus one index resource `saw_modindex` listing all hidden
  targets so the client applies moderation with **one** fetch.
- **Schema version.** 1.
- **Target identity.** `(service, name, identifier)` of the hidden resource, or
  a comment identifier. Validated exactly.
- **Mutability.** Owner mutates `action: "hide" | "unhide"` on the same
  identifier.
- **Timestamps.** `createdAt`, `updatedAt`.
- **Discovery.** Index resource first; individual records for detail.
- **UI semantics.** "Hidden in Shadow Archives" / "Removed from this site's
  listings", with an owner-only view that still shows the underlying state.
- **Limits.** Cannot affect other apps, other QDN readers, or the on-chain
  record.

```jsonc
{ "schemaVersion": 1, "kind": "moderation", "actions": [
  { "target": { "service": "DOCUMENT", "name": "Shadow Archives", "identifier": "saw_post_ab12cd34ef56" },
    "action": "hide", "reason": "duplicate", "createdAt": 1767225600000 }
] }
```

### 5.8 Taxonomy

- **Purpose.** Shared categories and tags across Blog, Videos and Gallery, with
  autocomplete in creation forms and cross-type category/tag pages.
- **Representation.** Taxonomy lives in the entity payload
  (`data.categories[]`, `data.tags[]`) and in the catalog/search index. It is
  **not** stored only in Core metadata, because Core tags are capped at 5 × 20
  chars, `description` is capped at 240 chars, and Core search cannot filter by
  metadata `tags` (only `query`/`keywords`/`description`).
- **Normalisation.** `slug = lowercase(trim(value))` with spaces/underscores →
  `-`, `[^a-z0-9-]` removed, collapsed dashes; display label preserved in the
  payload/catalog.
- **Registry.** No separate taxonomy resource is required initially: the catalog
  carries the used labels/slugs, which is exactly what the autocomplete needs.
  Optional later: `saw_tax` registry resource. If added, it is derived and
  non-authoritative.
- **Autocomplete + highlight.** Client-side over the cached catalog taxonomy
  index; substring highlight; no QDN request per keystroke.
- **Recommended model.** Hybrid: free-form app categories + tags (authoritative
  for the app), optionally mirrored into up to five Core metadata tags plus a
  compact string in `description` for cross-app discoverability. The Core
  `Category` enum may be set as a coarse classification but must not drive the
  UX. **OWNER APPROVED (D2).** Shadow Archives app-managed categories/tags are
  the canonical cross-content taxonomy; Core category metadata may be mirrored
  for QDN-ecosystem discoverability but the fixed Core enum must not limit the
  application's own cross-type taxonomy.

### 5.9 Catalog

See §7.

### 5.10 Site configuration

- **Justified?** Yes: the app needs an owner-editable place for the external
  app-link targets (Q-Tube/SubWire/Quitter names), the contact recipient, the
  brand/version, and the taxonomy seed. Hardcoding these would violate the
  "verify before hardcoding / not a timeless constant" requirement.
- **Service / identifier.** `DOCUMENT` / `saw_cfg`.
- **Publisher.** Owner name; the app treats the config as **non-authoritative
  presentation data** (never as an authority test) and falls back to built-in
  defaults when absent or invalid.

```jsonc
{ "schemaVersion": 1, "kind": "site-config",
  "externalApps": { "qtube": "Q-Tube", "subwire": "SubWire", "quitter": "Quitter" },
  "contact": { "recipientName": "Shadow Archives" },
  "search": { "indexPartitions": 1 },
  "brand": { "tagline": "..." } }
```

## 6. Authority and validation pipeline

```text
discovery (bounded, paginated)
-> trusted metadata check (name/service/identifier/created/updated)
-> schema + schemaVersion validation (quarantine unknown)
-> identity validation (resource name == claimed publisher; identifier matches kind + id)
-> target validation for children (exact service/name/identifier of the parent)
-> deterministic ordering (node created, then id)
-> entity reduction
-> operation reduction (likes/comments/moderation applied last)
-> derived index/catalog generation
-> diagnostics for quarantined records
```

Fail-closed rules:

- Authority-sensitive paths (owner controls, moderation, publish) fail closed.
- Partial discovery never grants authority and is reported as partial.
- Catalogs, indexes, counts and search hints are derived and never establish
  ownership or content authority.
- Payload `publisher`/`displayName`/`author` fields never grant authority.

## 7. Catalog and search-index contracts

### 7.1 Catalog purpose

A rebuildable, non-authoritative index so home, pagination, taxonomy and search
do not require fetching every entity document.

### 7.2 Shape

Partitioned documents plus a manifest. Entity resources stay authoritative; the
catalog only carries **locators + display summaries**.

```jsonc
// saw_cat_manifest (DOCUMENT)
{
  "schemaVersion": 1,
  "kind": "catalog-manifest",
  "catalogVersion": 1,
  "compiledAt": 1767225600000,
  "publisherName": "Shadow Archives",
  "partitions": [
    { "identifier": "saw_cat_post_p000", "type": "blog-post", "count": 180, "maxUpdated": 1767225000000, "checksum": "sha256:..." },
    { "identifier": "saw_cat_vid_p000",  "type": "video",     "count": 640, "maxUpdated": 1767224000000, "checksum": "sha256:..." }
  ],
  "taxonomy": { "categories": ["history"], "tags": ["archive"] }
}

// saw_cat_post_p000 (DOCUMENT)
{
  "schemaVersion": 1, "kind": "catalog-partition", "type": "blog-post", "partition": 0,
  "compiledAt": 1767225600000,
  "entries": [
    { "id": "2f8k3qz1m4", "service": "DOCUMENT", "identifier": "saw_post_2f8k3qz1m4",
      "title": "...", "slug": "...", "excerpt": "...", "createdAt": 0, "updatedAt": 0,
      "categories": ["history"], "tags": ["archive"],
      "thumbnail": { "service": "THUMBNAIL", "name": "Shadow Archives", "identifier": "..." },
      "state": "active", "contentHash": "sha256:...",
      "likeCount": 12, "commentCount": 3, "countsCompiledAt": 1767225600000 }
  ]
}
```

### 7.3 Decisions

- **Service.** `DOCUMENT` (see §3). Not `JSON` (25 KB cap). `LIST` acceptable
  but unnecessary.
- **One catalog vs partitioned.** Partitioned from day one: one partition per
  content type, split further when a partition exceeds the size cap.
- **Maximum practical resource size (INFERENCE).** Keep a partition
  ≤ ~200 entries and ≤ ~256 KB raw so a single partition stays a cheap download
  and a cheap publish. `DOCUMENT` has no Core cap; this is a self-imposed
  engineering limit to be confirmed by measurement in Phase 1B.
- **Entry metadata.** As in the shape above. Body text is **not** in the
  catalog; only a bounded excerpt.
- **Rebuildability.** Rebuild any partition from entity prefix searches
  (`saw_post_`, `saw_vid_`, ...) — the catalog is fully derived.
- **Stale behaviour.** IndexedDB stale-while-revalidate. Display
  `compiledAt`/staleness. Never block first render on a catalog refresh.
- **Versioning.** `schemaVersion` + `catalogVersion`; a newer `catalogVersion`
  is preferred; unknown versions are ignored and the app falls back to direct
  search.
- **Updates.** On owner publish, the affected entity resource is written first,
  then the affected partition + manifest are republished. Readers merge by
  `updatedAt`/`contentHash`.
- **Removed/hidden/withdrawn.** Entry `state` plus the moderation overlay.
  Hidden entries are filtered at render time; the entry itself may remain in the
  catalog (with `state`) or be removed on the next compile — either way the
  entity resource is untouched.
- **Recovery.** Missing/corrupt/stale catalog → direct prefix search over entity
  identifiers, paginated, with a visible "index unavailable; showing live search
  results" notice. Never present catalog absence as "no content".
- **Authority.** The catalog must never be used to prove ownership, existence
  beyond a locator, or counts except as a labelled snapshot.

### 7.4 Deep search design

Requirements: titles, descriptions, body text, categories, tags, video and
gallery metadata; no QDN request per keystroke; scale; ranking; type filtering;
highlighting; offline/stale behaviour.

**Recommended: hybrid local index.**

1. **Index partitions** (`saw_idx_<NNN>`, `DOCUMENT`) carry normalized tokens
   per entity: `{ id, type, tokens: [...], title, excerpt, taxonomy: [...],
   updatedAt }` plus a bounded plain-text extract. Body text is **not** shipped
   in full; the extract is capped (recommended ≤ 1 KB per entity) so an index
   partition stays comparable to a catalog partition.
2. **Client compile.** On first load (or when a partition changes), download the
   missing partitions once, merge into an in-memory inverted index, and persist
   to IndexedDB. Matching runs locally with no network calls.
3. **Ranking.** Field-weighted: title > taxonomy > excerpt > extract >
   recency/engagement tie-breakers. Deterministic and documented.
4. **Type filtering.** `type` is part of every index entry; filters applied
   locally.
5. **Highlighting.** Client-side substring highlighting on title/excerpt; never
   inject index text as HTML.
6. **Stale/offline.** Serve the cached index with a "results may be out of date"
   indicator; a manual refresh re-fetches only changed partitions
   (`updatedAt`/checksum compare).
7. **Full-body search honesty.** Search covers the indexed extract only. If the
   owner later wants true full-body search, the entity body must be fetched —
   offer it as an explicit, bounded, queued action, not a default.
8. **Mobile.** Cap local index size; move tokenization to a Web Worker if
   measurement shows main-thread cost.
9. **Never** search Core `query` per keystroke; Core search is used only to
   rebuild partitions or to resolve a single deep link.
10. **Rejected alternatives.** (a) Catalog-supplied text only — insufficient for
    body search and bloats the catalog. (b) A separate per-content-type index
    without local compilation — still requires network matching per query.
    (c) Client-only indexing of fetched entities — does not scale to a large
    archive.

## 8. Engagement rules (normative for Phase 1B)

The like **identity** rule (rule 1 below) is **DECIDED by the owner
(2026-09-11)**. The exact active/inactive/tombstone **wire representation**
remains **DEFERRED (D9)** pending a controlled QDN overwrite/runtime test;
Phase 1B may define the interface boundary but must not assert an unverified
wire format.

1. One active like per **acting registered Qortal name** per content item.
2. Likes are **never** deduplicated across different registered names of the
   same account/address.
3. Unlike/re-like operate on the same name-scoped identity; no duplicate active
   likes are ever created.
4. Raw count of matching QDN resources is **not** the active-like count.
5. Inactive/tombstoned state is interpreted before counting; unclassifiable
   resources produce a partial/`>= N` presentation.
6. Exact target identity (`service`, `name`, `identifier`) is validated before a
   like or comment is accepted.
7. Comments: publisher name is authority; a user may edit only their own
   comment; stable comment identity; `editedAt` state; parent target validated.
8. Engagement discovery never uses N+1 patterns: counts come from the catalog
   snapshot on listings; one search per target on a detail view; bounded
   concurrency; cached with TTL.
9. Tips and share transport are **NOT designed here**. Their Qortal mechanisms
   are unverified; they must not be implemented or described as QDN
   publications until a current mechanism is verified.
   `NOT VERIFIED — mechanism unknown`.

## 9. Versioning and migration

- Every payload carries `schemaVersion`. The owner-approved `saw_` identifier
  namespace is fixed and does **not** encode a schema version; schema evolution
  is represented by `schemaVersion`, not by a namespace digit. No `saw1_`
  migration is required or defined.
- Readers support the current and previous schema versions for a bounded period
  and quarantine everything else with a diagnostic code.
- A migration publishes new resources with a new `schemaVersion` alongside the
  old ones; history is never mutated and nothing is described as deleted.
- Indexes/catalogs are rebuilt, not migrated.

## 10. Open items requiring verification before implementation

- `DEFERRED (D9)` — the exact like active/inactive/tombstone **wire
  representation**; the identity rule is decided, but the representation must be
  selected after a controlled QDN overwrite/runtime test (one controlled owner
  publication required). The metadata-tag fast path below is a candidate, not a
  verified contract.
- `FUTURE / NOT VERIFIED` — the exact Q-Tube publication/discovery/identifier
  contract for the future video-interoperability extension point. Do **not**
  implement Q-Tube interoperability now and do not guess the contract; a
  dedicated Q-Tube source/runtime investigation is required first.
- `NOT VERIFIED` — metadata-tag engagement state surviving a republish
  (one controlled owner publication required).
- `NOT VERIFIED` — whether publishing a base64 envelope to the `COMMENT` service
  passes Core validation in the same way `DOCUMENT` does (single-file +
  encrypted-prefix checks apply).
- `NOT VERIFIED` — exact size at which a `DOCUMENT` catalog partition becomes
  slow to publish through a real host (memory cost of in-browser base64).
- `NOT VERIFIED` — hub behaviour when the app publishes under a non-primary
  owned name (`auth.name` is the primary name; the acting name must be
  selectable).
