# Project — shadow-archives-webportal-QORTAL

## Purpose and scope

Canonical project-specific context for the first onboarded Qortal Workflow v2
application. Read it after
[`../agents/00-SESSION-START.md`](../agents/00-SESSION-START.md). Shared rules
remain in the canonical workspace guides.

This file records product direction and owner decisions. It does **not**
authorize implementation: a phase label in this file is not authorization for
new work. Factual implementation status is recorded under "Current state"
below.

## Project identity

- Development name: `shadow-archives-webportal-QORTAL`
- Repository: `https://github.com/iffinland/shadow-archives-webportal-QORTAL`
- Local path:
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Application language: English
- Target platform: Qortal/QDN Q-App/webportal
- Frontend: Vite + React + TypeScript (implemented)

## Repository and local path

- Remote repository: `https://github.com/iffinland/shadow-archives-webportal-QORTAL`
  (branch `main`); `origin/main` and local `HEAD` are at commit `6354c88`
  ("Checkpoint Shadow Archives parchment visual baseline", 2026-09-11), which
  records the owner-approved parchment visual correction on top of the
  Phase 2C-A publication-provenance work (`1b099c1`).
- Local path: a Git working tree on branch `main` — baseline `6354c88` plus the
  uncommitted Phase 2C-B `/studio` host-context diagnostics block (2026-09-12).
- Canonical report root:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/`

## Phase 1A architecture package (2026-09-11)

The Phase 1A architecture, QDN data-contract, performance-baseline and Phase 1B
planning artifacts are under
[`../docs/shadow-archives-webportal/architecture/`](../docs/shadow-archives-webportal/architecture/).
They now record the owner-approved Phase 1A decision baseline, which is
implementation-authoritative for Phase 1B; they still do **not** by themselves
authorize scaffolding, which requires explicit owner go-ahead.

- Architecture report:
  [`2026-09-11-phase-1a-architecture-report.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-phase-1a-architecture-report.md)
- QDN data contracts:
  [`2026-09-11-qdn-data-contracts.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-qdn-data-contracts.md)
- Performance / reference comparison:
  [`2026-09-11-performance-reference-comparison.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-performance-reference-comparison.md)
- Responsive AppShell spec and design tokens:
  [`2026-09-11-responsive-appshell-and-design-tokens.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-responsive-appshell-and-design-tokens.md)
- Phase 1B implementation plan:
  [`2026-09-11-phase-1b-implementation-plan.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-phase-1b-implementation-plan.md)

**OWNER DECISIONS (final, 2026-09-11).** The owner recorded the final Phase 1A
decisions below; where the earlier Phase 1A package made a recommendation, the
decision is authoritative. Status labels: `OWNER APPROVED`, `DEFERRED`,
`NOT VERIFIED`, `FUTURE CAPABILITY`.

- **D1 Identifier namespace — OWNER APPROVED.** Prefix `saw_` (Shadow Archives
  Web). Conceptually `saw_post_<stable-id>`, `saw_vid_<stable-id>`,
  `saw_img_<stable-id>`, `saw_album_<stable-id>`,
  `saw_cmt_<target-or-stable-scope>_<comment-id>`, `saw_lk_<target-stable-id>`.
  The existing evidence-based stable-ID encoding is retained. Schema evolution
  is carried by payload `schemaVersion`, not by a namespace digit; no `saw1_`
  migration is defined.
- **D2 Taxonomy — OWNER APPROVED.** Hybrid. App-managed categories/tags are the
  canonical cross-content taxonomy; Core category metadata may be mirrored for
  QDN-ecosystem discoverability, but the fixed Core enum must not limit the
  application's own cross-type taxonomy.
- **D3 Editor — OWNER APPROVED.** TipTap. The heavy owner editor is
  lazy-loaded and outside the visitor startup path.
- **D4 Stored rich-text / rendering model — OWNER APPROVED.** Canonical
  structured representation `tiptap-json-v1` with normalized/searchable
  `bodyText` alongside it; DOMPurify-based sanitized rendering boundary; the
  global canonical rendering-safety rules remain authoritative.
- **D5 Q-Mail failure UX — OWNER APPROVED.** Preserve the draft, explain that
  Q-Mail delivery is unavailable/failed, provide an explicit user-triggered
  Copy Message action, and do **not** silently substitute
  `SEND_CHAT_MESSAGE` or another transport.
- **D6 UI dependency strategy — OWNER APPROVED.** No MUI. Semantic CSS design
  tokens, in-repository reusable components, inline/local SVG icons and
  accessible native semantics. No generic UI framework may be added to Phase 1B
  without a new evidence-backed reason and owner approval.
- **D7 Qortal integration strategy — OWNER APPROVED.** Do not import
  `qapp-core` through its published root entry in the application startup path.
  Use a small in-repository `src/qortal/` integration layer on the verified
  current Qortal bridge/API contracts; keep it minimal and contract-focused.
- **D8 Catalog — OWNER APPROVED.** Partitioned `DOCUMENT` catalog + manifest.
  Entity resources remain authoritative; catalogs are derived, rebuildable,
  versioned, cacheable, permitted to be stale, and never evidence of publisher
  authority.
- **D9 Like-activeness wire representation — DEFERRED.** The identity rule is
  decided (one active like per acting registered Qortal name per content item);
  the exact active/inactive/tombstone wire representation must be selected
  after a controlled QDN overwrite/runtime test. Phase 1B may define an
  interface/type boundary but must not claim an unverified wire format.
- **Moderation — OWNER APPROVED for alpha.** No delegated moderators;
  moderation authority is the current owner of the Shadow Archives publishing
  name. Keep the design extensible for later delegated moderation without
  rewriting content entities.
- **Video + future Q-Tube interoperability — OWNER APPROVED / FUTURE.** See
  "Video architecture" below.
- **Publishing interoperability first — OWNER APPROVED (2026-09-11).** The final
  Video and Blog publish modals MUST be preceded by dedicated research into the
  then-current ecosystem contracts. See "Publishing interoperability first"
  below.

Individual like/comment identity records are scoped by the publishing **name**,
not the account address.

**VERIFIED (2026-09-11).** The published external app names are `Q-Tube`,
`SubWire` and `Quitter` (read-only node `https://api.qortal.org`); a
`qortal://APP/<name>` anchor is intercepted by `q-apps.js` and opened as a new
tab by the host. These values still belong in owner-editable configuration and
must not be treated as timeless constants.

## QDN publishing identity (owner decisions, 2026-09-11)

- **Publishing name:** `Shadow Archives` — the human-readable canonical
  publishing name.
- **QDN service:** `APP`.
- **Identifier / prefix:** **`saw_`** (owner decision D1). The namespace is
  fixed; schema evolution is carried by payload `schemaVersion`, not by a
  namespace digit. `saw_` is the **content** namespace (for example
  `saw_post_*`); it is **not** the APP resource identifier.
- Deployed APP resource URI (Phase 2C-A recommendation, owner confirmation
  pending): **default identifier** at
  `qortal://APP/Shadow Archives` → `(service=APP, name="Shadow Archives",
  identifier=default)`.

The canonical identity is the human-readable `Shadow Archives`. Account for
platform encoding (for example percent-encoding of spaces) only where
technically required; do not redefine the product identity as the
percent-encoded string.

## Development model

- Workflow: Qortal Development Workflow v2.
- Primary implementation agent: DeepSeek.
- Independent auditor: Codex.
- Architecture / task planning / review: ChatGPT.

## Ownership and permission model (owner decisions)

- The application MUST detect the site owner automatically at runtime.
- The owner sees publishing/edit controls.
- Normal users may comment.
- Users may edit their own comments.
- Normal users MUST NOT get owner publishing controls.

**Mandatory implementation constraint.** Owner detection MUST be derived from
the app's published identity (`_qdnName`) and current name ownership, verified
against the connected account. Note that Core percent-encodes spaces in
`_qdnName` (`iffi vaba mees` becomes `iffi%20vaba%20mees`), so decode before
comparing and re-encode when calling `/names/{name}`. It MUST NOT be a hardcoded name or address, and
it MUST NOT trust a payload `author`/`owner` field. See
[`../agents/qortal-qdn-and-bridge.md`](../agents/qortal-qdn-and-bridge.md) and
[`../agents/qortal-architecture-and-data-integrity.md`](../agents/qortal-architecture-and-data-integrity.md).

**OWNER APPROVED (2026-09-11).** For alpha there are no delegated moderators:
owner/moderation authority is the current owner of the Shadow Archives
publishing name. Keep the architecture extensible so delegated moderation can
be added later without rewriting content entities.

## Responsive targets (owner decisions)

- mobile
- tablet
- desktop
- large desktop
- TV
- desktop/TV main layout approximately 90% viewport width
- avoid uncontrolled extreme width on very large screens

## Home layout (owner decisions)

### Header

- left panel: TOP POSTS, approximately 240px on desktop
- center: Shadow Archives banner
- right panel: TOP VIDEOS, approximately 240px on desktop

### Top Posts and Top Videos

- top content by likes
- maximum 10 visible/listed items
- no thumbnails
- vertical automatic scrolling behavior
- clickable items

### Banner

- use the supplied Shadow Archives brand image later from application assets
- do not allow the full 16:9 source image to make the desktop header
  excessively tall
- expected desktop presentation approximately 300–340px high, or another
  evidence-based responsive equivalent
- preserve the important central SHADOW ARCHIVES branding

### Primary action row

- Q-Tube
- SubWire
- Quitter
- Search icon/button
- approximately 70% page width
- actions visually stronger than standard navigation

**UNKNOWN / verify before implementing.** The verified Qortal mechanism for
opening another Q-App is a `qortal://APP/{name}` link intercepted by the host
(`q-apps.js`), which opens a new tab when the target app differs. The exact
published names/identifiers for Q-Tube, SubWire and Quitter MUST be verified
before hardcoding any link target, and no such target MUST be treated as a
timeless constant.

### Navigation

- Home
- Blog
- Videos
- Gallery
- About
- Contact

### Home body

- two primary columns on suitable desktop widths
- Latest Posts on left
- Latest Videos on right
- content cards are clickable
- posts include thumbnail and short description
- videos use suitable video cards

### Gallery strip

- `LATEST FROM THE GALLERY`
- horizontal media strip
- automatically scrolling horizontally
- responsive and accessible

### Footer

- visually elevated from the site background consistently with other major
  panels
- **OWNER DECISION (owner-runtime correction, 2026-09-11):** the footer contains
  **no navigation links, no external/Web2 links and no repository URL**. The
  `HOME / BLOG / VIDEOS / GALLERY / ABOUT / CONTACT` links live only in the main
  site navigation. Footer content is limited to the brand, a short description,
  `Decentralized on Qortal` and the text-only build provenance
  (`Build vX · commit`).

## Visual identity (owner decisions)

- NOT generic blue dApp styling
- use the Shadow Archives brand direction
- charcoal / black
- parchment / faded cream
- classified-document greys
- muted dark red accent
- light beige/cream text where suitable
- restrained shadows/borders/elevation
- avoid generic heavy glassmorphism

**OWNER DECISION (owner-runtime correction, 2026-09-11):** The Shadow Archives
visual palette is **derived from the actual banner artwork**
(`src/assets/banner-shadow-archives.webp`), not from generic dark-app defaults.
The warm banner tones are the source of truth: warm near-black, warm dark
charcoal, aged parchment/cream, faded paper grey, and muted/dried-blood
oxidative red. No dominant blue/slate SaaS tone and no heavy glassmorphism; the
earlier provisional palette is superseded.

**OWNER DECISION (owner-runtime correction, 2026-09-11):** Major
panels/sections must have **clearly visible elevation** from the page
background — stronger tonal contrast, warm borders, a useful shadow and a
subtle inset highlight. No oversized SaaS shadows and no glassmorphism.

**OWNER DECISION (owner-runtime visual correction follow-up, 2026-09-11):** The
application uses a **parchment / paper-led** palette derived directly from the
banner, replacing the still-too-dark archive look:

- general page background follows the lighter beige glow around the central
  figure (warm aged light beige, never pure white or bright cream);
- large section containers (site header outer, primary actions, site
  navigation, Latest Posts, Latest Videos, Latest from the Gallery, route main
  panels, footer) follow the paper-sheet tones on the left/right sides of the
  banner;
- inner content boxes and empty states also use light parchment tones derived
  from the lighter beige around the central figure — the previous dark inner
  boxes are removed;
- heading strips such as TOP POSTS / TOP VIDEOS use a slightly darker beige so
  they still separate from their panels;
- borders use a darker archival brown-beige so surfaces separate clearly;
- text moves to dark archival ink (primary), faded brown-grey (muted) and a
  readable dark oxide (links); the accent/action controls keep the stamped
  muted dark-red family;
- elevation is preserved with tonal separation, darker borders, restrained
  warm shadows and a subtle inset paper edge — no glassmorphism and no large
  dark shadows;
- the footer remains link-free (no navigation, external links or repository
  URL), and the main `HOME / BLOG / VIDEOS / GALLERY / ABOUT / CONTACT`
  navigation remains present and functional.

## Interaction and engagement (owner decisions)

- visible button click feedback
- like action uses a thumbs-up icon and count
- successful like may emit a short upward floating/bubbling thumbs animation
- respect `prefers-reduced-motion`

### Shared engagement component

- Like
- Comments + count
- Share
- Send Tip

Rules:

- **OWNER DECISION (2026-09-11).** One active like is allowed per acting
  registered Qortal name per content item;
- likes MUST NOT be deduplicated across multiple registered names owned by the
  same Qortal account/address; each registered name has its own interaction
  identity;
- unlike and re-like MUST operate on the same name-scoped interaction identity
  rather than creating duplicate active like resources;
- Example: registered name `Alice` can have one active like on content X, and
  another registered name `AliceAlt` can independently have one active like on
  X even if both names belong to the same underlying account; `Alice` cannot
  create multiple simultaneous active likes on X;
- Rationale (conceptual only): Shadow Archives does not attempt to define one
  wallet/account as one human identity; a future Qortal trust/reputation system
  may provide better semantics for weighting or interpreting engagement. This
  rationale does not import, depend on or reference Qortium trust, APIs or
  contracts, and no trust system is implemented in Shadow Archives;
- publisher identity MUST NOT be trusted only from arbitrary payload text;
- plan for owner-side moderation presentation without pretending QDN data was
  deleted if it cannot actually be deleted;
- engagement discovery MUST NOT create an N+1 request pattern.

**VERIFIED constraint (revision-scoped framework convention).** QDN has no
on-chain delete. The inspected current Qortal apps implement "unlike" by
overwriting the like resource with a placeholder payload and filtering it on
read; local hosted-data deletion does not remove the on-chain record. This is a
framework convention, not a timeless Core rule. See
[`../agents/qortal-architecture-and-data-integrity.md`](../agents/qortal-architecture-and-data-integrity.md).

## Comments (owner decisions)

- users can add comments;
- users can edit only their own comments;
- publisher identity must not be trusted only from arbitrary payload text;
- plan for owner-side moderation presentation without pretending QDN data was
  deleted if it cannot actually be deleted.

## Rich text (owner decisions)

### Comments

- bold, italic, underline
- bullet list, numbered list
- red, yellow, green, blue
- emoji

### Owner publishing

- full editor
- use `iffi-vaba-mees-QORTAL` UX/functionality as a reference
- do not blindly reuse deprecated browser editing APIs
- investigate a modern maintainable editor architecture

**OWNER APPROVED (D3/D4, 2026-09-11).** The editor is **TipTap**. The canonical
stored representation is `tiptap-json-v1` plus a normalized/searchable
`bodyText` extract where defined by the architecture; rendering goes through a
single allowlisting renderer with a **DOMPurify-based sanitized rendering
boundary**. The heavy owner editor MUST remain lazy-loaded and outside the
visitor startup path.

**Reference observations (non-authoritative).** The `iffi-vaba-mees-QORTAL`
reference uses a hand-rolled sanitizer rather than DOMPurify; current Qortal
apps use DOMPurify (`q-tube`, `Subwire`, `q-mail`) and Qortal Hub uses TipTap.
The decision is evidence-based and must keep rendering safe and the stored
schema parseable and validatable. Do not weaken the XSS/rendering-safety
requirements.

**Global security rule (reference only).** All Shadow Archives content —
plain text, rich text, imported, stored, cached and preview — MUST comply with
[`../agents/qortal-architecture-and-data-integrity.md`](../agents/qortal-architecture-and-data-integrity.md)
§11. Schema validation, publisher/authority validation and rendering safety
remain separate gates through that global rule; this project does not restate or
extend it, and the approved editor/rendering decision does not weaken it.

## Content model (owner decisions)

Content types: Blog, Videos, Gallery.

### Pagination

- blog: 10 posts per page
- video: 20 videos per page

### Cards

- similar useful content-card concept to `iffi-vaba-mees-QORTAL`
- quick engagement actions at card bottom

## Video architecture (owner decision, 2026-09-11)

- Shadow Archives **will publish its own video content to QDN** (owner
  approved).
- The architecture MUST ALSO preserve a **future** capability whereby a video
  published through Shadow Archives can participate in / appear through the
  Q-Tube ecosystem using the appropriate QDN/Q-Tube publication/discovery
  contract.
- **Do not** implement Q-Tube interoperability now and **do not** guess the
  exact Q-Tube metadata, identifier, indexing or publication contract. Mark the
  exact interoperability contract **FUTURE / NOT VERIFIED** until a dedicated
  Q-Tube source/runtime investigation is performed.
- Do not import Q-Tube source code or make Shadow Archives depend directly on
  the Q-Tube application.
- Architect the video domain with separated layers so future interoperability
  does not require a rewrite:

  ```text
  Video entity
    -> Shadow Archives metadata
    -> QDN media resource reference
    -> publication/discovery adapter boundary
  ```

- The media reference must identify QDN media by verified fields such as
  `service`/`name`/`identifier`/`path` where applicable instead of storing an
  opaque Shadow-Archives-only blob reference.

## Publishing interoperability first (owner decision, 2026-09-11)

Code is the contract here: the publication format has to match what the
ecosystem actually reads, and that can only be established from current source.

- **Before implementing the final Video Publish modal:** inspect the
  then-current Q-Tube source and the relevant QDN/runtime behaviour, determine
  the actual current Q-Tube publication/discovery contract, and build the Shadow
  Archives video publication flow around that verified compatible QDN model
  where appropriate.
  Goal: a video published through Shadow Archives is later capable of native
  Q-Tube ecosystem discovery/participation **without the Video domain being
  rewritten**.
- **Before implementing the final Blog Publish modal:** inspect the then-current
  Subwire source and QDN publication contract, investigate its then-current
  Quitter cross-post/publication integration, and build the Shadow Archives blog
  publication flow around the verified ecosystem contract where appropriate.
- This is a **future implementation rule**. It is **not** Phase 1B work and must
  not be started early. A small read-only check is permitted only where needed
  to avoid an architectural mistake.
- **Do NOT** claim Q-Tube/Subwire/Quitter interoperability is verified by any
  earlier task. The contracts remain FUTURE / NOT VERIFIED until that dedicated
  research is executed and recorded.
- **Do NOT** copy their UIs merely for visual similarity. The purpose is
  protocol/resource interoperability, not cloning applications.

## Taxonomy (owner decisions)

- shared categories and tags across blog/video/gallery
- category/tag click shows related content across content types
- creation forms suggest previously used categories/tags
- matching text should be visually highlighted

**OWNER APPROVED (D2).** Hybrid taxonomy. Shadow Archives app-managed
categories/tags are the canonical cross-content taxonomy; Core category
metadata may be mirrored where useful for QDN-ecosystem discoverability, but
the fixed Core enum must not limit the application's own cross-type taxonomy.

## Search (owner decisions)

- expandable search field activated by compact search icon/button
- deep search across the application: titles, descriptions, body/content text
  where practical, categories, tags, relevant video/gallery metadata
- search architecture must scale
- must not issue wasteful QDN requests on every keystroke

**VERIFIED constraint.** QDN search (`query`) covers name, identifier, title and
description metadata only — not body content. Deep/body search requires an
app-maintained index/catalog. See
[`../agents/qdn-publication-discovery-and-scaling.md`](../agents/qdn-publication-discovery-and-scaling.md).

## Contact (owner decisions)

- simple contact form
- goal: send a message to the owner through Q-Mail
- verify the CURRENT Qortal/Q-Mail integration contract
- do not assume `SEND_CHAT_MESSAGE` is automatically equivalent to Q-Mail

**VERIFIED (against `Qortal/q-mail` 3.2.1, revision recorded in the standard).**
Q-Mail interop is a **convention**, not a Core API:

- mail messages are published under the sender's own name with service
  `MAIL_PRIVATE`;
- the identifier follows the sender's chosen convention
  (`_mail_qortal_qmail_<recipientName>_<recipientAddressLast6>_mail_<id>` in the
  current source, or an alias value);
- the message is encrypted to the recipient's public key using
  `PUBLISH_MULTIPLE_QDN_RESOURCES` with `encrypt: true` and `publicKeys`;
- recipients discover mail by searching `MAIL_PRIVATE` resources with a query of
  the form `qortal_qmail_<name>_<addressLast6>_mail_`;
- the payload is a base64-encoded JSON object with `subject`, `createdAt`,
  `version`, `attachments`, `textContentV2` and thread references.

**UNKNOWN / MUST RE-VERIFY.** This convention was read from the current Q-Mail
source but MUST be re-verified against the current Q-Mail release before
implementation, because it is a community-app convention and may change.
`SEND_CHAT_MESSAGE` sends a Qortal chat message and is **not** Q-Mail.

**OWNER APPROVED (D5).** If verified Q-Mail delivery cannot be completed:
preserve the user's draft; clearly explain that Q-Mail delivery is
unavailable/failed; provide an explicit **user-triggered Copy Message action**;
and do **not** silently substitute `SEND_CHAT_MESSAGE` or another transport.
Success feedback must state what actually happened (submitted for approval,
published, or failed with a reason). The exact Q-Mail convention above remains
**MUST RE-VERIFY** before implementation.

## Links (owner decisions)

- internal Shadow Archives navigation stays in the current application
- Qortal internal links to other Q-Apps open through the appropriate Qortal
  mechanism / new-tab behavior supported by the current platform
- Web2 HTTPS links should be copied to the clipboard rather than navigating away
- user-visible success feedback / badges / tooltips required

This is the project-specific external-link policy required by
[`../agents/qortal-qdn-and-bridge.md`](../agents/qortal-qdn-and-bridge.md) §8;
copy-to-clipboard is a Shadow Archives interaction decision, not a global Qortal
rule.

**VERIFIED.** `q-apps.js` intercepts `qortal://` links and asks the host to open
a new tab when the target app differs. Clipboard access inside the iframe may be
restricted; a supported path with fallback and visible feedback is required.

## Performance (first-class product requirement)

Users should see a useful application shell quickly rather than waiting for all
QDN/media content.

Before finalizing the performance architecture, benchmark and inspect current
Qortal applications and determine appropriate patterns for:

- route-level code splitting
- dynamic imports
- lazy media loading
- application shell
- QDN discovery
- request batching
- catalog/index strategy
- IndexedDB/cache
- background refresh
- route/content prefetching
- avoiding unnecessary video/media download
- loading skeletons
- repeat-visit performance

Do not establish arbitrary performance budgets without evidence. First collect a
Qortal-relevant baseline.

## Scalability rules (owner decisions)

The application MUST NOT use designs such as:

```text
20 cards
x separate like query
x separate comment query
x separate metadata query
```

- N+1 QDN discovery is a documented architecture risk.
- Investigate bulk discovery, aggregation, caching and catalog/index resources.

**VERIFIED** mitigations available from current Qortal sources:

- one paginated `SEARCH_QDN_RESOURCES` with the bridge fields
  `includeMetadata`/`includeStatus`;
- `POST /names/list` for batched primary-name resolution;
- `qapp-core` request queues (`RequestQueueWithPromise`) for bounded concurrency;
- IndexedDB caches with TTLs (current apps cache primary names 24h, profiles
  5m);
- derived catalog resources rebuildable from entity resources (D8: partitioned
  `DOCUMENT` catalog + manifest; `LIST`/`JSON` are not used).

## Accepted future product ideas

Recorded as accepted roadmap candidates, **not** Phase 0 implementation work:

- Featured Archive
- Related Content
- Draft + Preview
- IndexedDB draft autosave
- Owner Toolbar
- publishing/upload progress
- skeleton loading and partial loading
- offline/repeat-visit caching
- breadcrumbs
- previous/next navigation
- QDN payload schema versioning
- owner moderation layer
- central site configuration
- proper empty/error/retry states
- user capability detection
- archive statistics/footer metadata
- scalable QDN content catalog/index
- batched engagement discovery to avoid N+1 queries

Do not implement these in the bootstrap task.

## Current state

**Phase 2C-B real Qortal host validation (2026-09-12, read-only; no write).**
The published `APP` resource `(service=APP, name="Shadow Archives",
identifier=default)` was verified read-only from two public nodes
(`https://api.qortal.org`, `https://api.qortal.link`; mainnet, heights
2721342/2721343). Chain evidence: the latest publish is ARBITRARY transaction
`5fVoqGEc…`, block `2720709`, timestamp 2026-09-11T18:32:23Z, creator
`QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA` (the current `Shadow Archives` name owner),
`size` 459360. The served revision is the **2026-09-11 artifact**
(`release/shadow-archives-app-0.1.0-20260911.zip`, built from `1b099c1` with
`dirty: true`), identified by its chain-anchored 24-file metadata list, which
matches that artifact exactly and differs from the `6354c88` artifact in 19 of
24 files; the two artifacts are byte-identical in every served file after
normalizing Vite chunk names and the embedded build identity, so the app
currently displays the build label `1b099c1`. Served revision vs. committed
baseline: **MISMATCH by revision identity, EQUIVALENT by served content**. The
2C-A publication-readiness report and the earlier text of this file quote
SHA-256 `697aa966…` for that artifact; the artifact on disk (unchanged during
this task) and its own manifest record `354065b9…` — the quoted value is stale,
not evidence of tampering.

Public-node data-plane finding: both nodes can serve the resource *metadata*
but report the resource *data* as `DOWNLOADING` 1 of 2 chunks (50%) /
`MISSING_DATA` with `peerCount: 0`; every file fetch 404s and
`/render/APP/Shadow%20Archives/` returns 503. The published APP data is
currently not retrievable from the public network tested. Served-byte hash
verification is therefore `NOT VERIFIED`. This is a hosting/availability
condition, not an application defect.

A bounded, non-secret, read-only **Host context diagnostics** block was added to
`/studio` only (uncommitted): it displays `_qdnService`, `_qdnName`,
`_qdnIdentifier`, `_qdnContext`, `_qdnBase` and `_qdnBaseWithPath`, issues no
host request and shows no account data. It is **not** in the currently published
build, so exact live `_qdn*` values remain `NOT VERIFIED` until a future
owner-authorized publication; a partial check is already available in the
published build because `/studio` quotes the decoded `_qdnName`. Owner
observations (layout, navigation, action buttons, route pages) are recorded at
owner-runtime level only. No QDN write, transaction, content write, commit,
push or tag occurred. Report:
[`../docs/shadow-archives-webportal/validation/2026-09-12-real-qortal-host-validation-report.md`](../docs/shadow-archives-webportal/validation/2026-09-12-real-qortal-host-validation-report.md)

**Owner-reported runtime status (2026-09-11, owner-confirmed).** The owner has
published and runtime-tested the APP in Qortal: layout passes, the main
navigation works, the primary action buttons work, and pages/routes open
correctly. This supersedes the Phase 2C-A "not published" statement below for
the runtime-publication question; the owner supplied this status directly.

**Uncommitted owner-runtime visual correction (2026-09-11, not a phase).** A
CSS/design-token and footer correction is applied on top of `1b099c1`: the
semantic palette is re-derived from the banner artwork, panel elevation is
strengthened, and the footer is reduced to link-free brand/provenance text. No
architecture, routing, QDN-read, auth, capability or content-contract change.
Report:
[`../docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md`](../docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md)

**Uncommitted owner-runtime visual correction follow-up (2026-09-11, not a
phase).** The owner reviewed the first correction and directed a further shift
from a dark archive to a parchment/archive-paper visual language: light warm
beige page background, paper-sheet section panels, light inner content boxes,
slightly darker beige heading strips, darker archival borders, dark-ink text
and the retained muted dark-red action controls. This is a
CSS/design-token-only change (plus one provider comment), with no architecture,
routing, QDN-read, auth, capability or content-contract change. Report:
[`../docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-followup-report.md`](../docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-followup-report.md)

**Verified 2026-09-11 — Phase 2C-A first APP publication readiness prepared
(current factual state):**

- The current multi-file `APP` publication contract was re-verified against the
  pinned Core `108bf191` (v6.1.9) and Hub `12a573b2` sources (both still
  upstream `HEAD`): `PUBLISH_QDN_RESOURCE` with `service: 'APP'`,
  `isMultiFileZip: true` (Hub maps this to `uploadType: 'zip'` → Core
  `isZip=true` → `ZipUtils.unzip`), `identifier` omitted (Hub substitutes
  `'default'`; Core treats `null`/`''`/`'default'` as the default resource),
  metadata via `title`/`description`/`category`/`tags`. Hub's own app-publish UI
  uses the same ZIP/no-identifier convention.
- `index.html` must be at the resource root; `Service.APP` auto-routes
  unhandled paths to it. A single enclosing directory in the ZIP is flattened
  by Core, but the artifact is built with `index.html` at the ZIP root.
- Recommended canonical identity (**owner confirmation pending**): the
  **default identifier**, so the canonical URL is `qortal://APP/Shadow
  Archives`. `saw_` is the content namespace and is **not** used as the APP
  identifier. Alternative explicit identifiers are technically viable but would
  break the direct `qortal://APP/Shadow Archives` address and trigger
  `HTMLParser` relative-asset query rewriting.
- Production artifact produced and structurally verified:
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL/release/shadow-archives-app-0.1.0-20260911.zip`
  — 24 files, 774964 bytes uncompressed, 458078 bytes compressed, SHA-256
  `697aa9664a03fac0e1a1ea90d7631a899a4b27ea6f273aa56bf1dccde2a46c96`,
  `index.html` at the ZIP root, all lazy route chunks and the banner present, no
  source maps / `node_modules` / `.env` / source files, all asset URLs relative.
  Packaging is deterministic (sorted entries, normalized mtimes, `zip -X -D`);
  `SOURCE_DATE_EPOCH` is supported. The artifact is **not** committed
  (`/release/` is ignored).
- Build/revision provenance added: `__BUILD_INFO__` (`version` + git `commit`)
  is injected at build time; `dist/build.json` records
  `version`/`commit`/`commitShort`/`builtAt`/`dirty`; the footer and `/studio`
  show the served build id. Intended-revision verification compares the served
  non-HTML asset SHA-256 and `build.json` against the manifest, because
  `index.html` is rewritten at render time and `READY` alone does not prove the
  intended revision.
- Exact owner live-publish procedure and the exact post-publication real-host
  validation checklist are recorded in the Phase 2C-A report. **No publication,
  transaction or QDN write occurred**; the `APP` resource remains
  `NOT_PUBLISHED`, so no genuine `_qdnName` render context exists yet and
  real-host validation remains `NOT VERIFIED` / owner-authorized.
- Tests: 32 files / 299 tests passing; `lint`, `typecheck`, `format:check`,
  `build`, `git diff --check`, `bash -n tools/validate-workspace.sh` and
  `bash tools/validate-workspace.sh` (PASS) all green.
- Phase 2C-A report:
  [`../docs/shadow-archives-webportal/release/2026-09-11-first-app-publication-readiness-report.md`](../docs/shadow-archives-webportal/release/2026-09-11-first-app-publication-readiness-report.md)

**Verified 2026-09-11 — Phase 2B owner-capability boundary implemented
(current factual state):**

- The owner authority model is the **current owner of the registered Qortal name
  under which the app is published**: `publisherName` is derived from the
  injected `_qdnName` (percent-decoded), never from a hardcoded string, a
  configured address, payload `owner`/`author`/`publisher` fields, catalog data
  or browser storage.
- Capability states: `unknown`, `requesting-permission`, `resolving-ownership`,
  `permission-denied`, `error`, `visitor`, `authenticated-no-name`,
  `authenticated-non-owner`, `owner`. Owner is reported only after positively
  verifying that the connected account address equals the node-reported current
  owner of the publishing name; every other path fails closed. A name transfer
  revokes/grants capability on the next explicit resolution.
- Ordinary browsing remains permission-free: `GET_USER_ACCOUNT` is issued only
  from an explicit action on the lazy `/studio` route ("Enter owner mode").
  Automated tests assert zero `GET_USER_ACCOUNT` on startup and on all public
  routes, and the local browser smoke confirms zero on load and Home.
- Session behaviour: single-flight account request shared by consumers; a
  decline/failure is cached for the session and never auto-retried; an explicit
  "Try again" retries; "Cancel" returns to read-only. Only the in-memory session
  `{address, publicKey}` is held; no secrets are logged or persisted; no custom
  login system.
- Registered names: `GET_ACCOUNT_NAMES` is parsed as the verified
  `NameSummary[]` (`[{name, owner}]`) shape and all names are retained
  individually; `authenticated-no-name` is distinguished from
  `authenticated-non-owner`.
- Studio/Owner Mode is a capability/status shell only — no publish form, no
  editor, no upload, no moderation write, no button that implies a write.
- Verified current auth/name contracts (Core `108bf191` v6.1.9, Hub `12a573b`):
  `GET_USER_ACCOUNT` → `{address, publicKey}` (host-mediated, approval-gated);
  `GET_ACCOUNT_NAMES` → `NameSummary[]`; `GET_NAME_DATA` → `NameData.owner`;
  `GET_PRIMARY_NAME` → name string. The Phase 1B/2A assumption that
  `GET_ACCOUNT_NAMES` returned bare strings was a real contract mismatch and is
  fixed. Hub wraps a declined dialog in a generic error, so a real decline may
  surface as the fail-closed `error` state rather than `permission-denied`; the
  app never auto-retries and never treats it as non-owner.
- Tests: 31 files / 295 tests passing; `lint`, `typecheck`, `format:check`,
  `build`, `git diff --check` and `tools/validate-workspace.sh` (PASS) all green.
  Production entry chunk 383.72 kB raw / 120.51 kB gzip (+0.26 kB gzip over
  Phase 2A); the capability UI ships in a 5.68 kB / 1.86 kB-gzip lazy
  `StudioPage` chunk.
- **REAL HOST VALIDATION NOT VERIFIED (OWNER VALIDATION REQUIRED):** no local
  Qortal node (no process, no data dir, no node API port) and no usable Hub
  Developer Mode session exist in this environment; Developer Mode requires the
  local Core node. The `Shadow Archives` name is registered and owned by
  `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`, but the `APP` resource is
  `NOT_PUBLISHED` (live read-only status), so no real render context can inject
  `_qdnName` yet. `_qdnBase` routing, live bridge behaviour, host CSP,
  `qortal://` interception and in-iframe clipboard remain unvalidated at
  runtime; see the Phase 2B report for the manual checklist.
- **First-publication bootstrap.** A genuine chicken-and-egg exists: the app has
  no authoritative deployed identity until its `APP` resource is first published,
  which is a write action and is out of scope for Phase 2B. The development
  proxy is explicitly modelled as "development / identity not authoritative" and
  has no owner bypass.
- No QDN write path, transaction, publication, like/comment/tip, moderation or
  editor code was added. Nothing was committed or pushed for Phase 2B.
- Phase 2B report:
  [`../docs/shadow-archives-webportal/implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md`](../docs/shadow-archives-webportal/implementation/2026-09-11-phase-2b-owner-capability-host-validation-report.md)

**Phase 2A snapshot (2026-09-11, historical, superseded above): read-only QDN
content pipeline.**

- Centralized read-only QDN layer: `src/qortal/qdn.ts` wraps the verified
  bridge actions (`SEARCH_QDN_RESOURCES`, `FETCH_QDN_RESOURCE`,
  `GET_QDN_RESOURCE_STATUS`, `GET_QDN_RESOURCE_URL`) with the exact camelCase
  bridge field names; `src/services/` owns Shadow Archives content semantics.
  No UI component issues a raw `qortalRequest`.
- Runtime-validated domain models for Blog, Video, Gallery item and Gallery
  album, plus the partitioned catalog manifest/partition/entry contract
  (`schemaVersion: 1`). Every untrusted payload passes an explicit validator
  before entering the trusted layer; a malformed entry is isolated.
- Catalog consumer (manifest -> bounded partition fetches -> validated entries)
  with a bounded `mode: 'ALL'` prefix-discovery fallback. Archive state
  distinguishes loading / ready / empty / partial / stale / unavailable / error;
  failure is never rendered as "empty".
- Authoritative detail fetch on `/blog/:id`, `/videos/:id`,
  `/gallery/item/:id` and `/gallery/album/:id` (bare stable id canonical; the
  full `saw_*` identifier accepted as an alias). Legacy `/gallery/:id` resolves
  to the item route.
- Blog detail renders `tiptap-json-v1` through an allowlisting read-only
  renderer plus a DOMPurify boundary; stored content is never injected as raw
  HTML, and stored web links copy instead of navigating the Q-App away.
- Listings use catalog/thumbnail metadata only. Headless-browser validation
  against a simulated host bridge: home issued 8 bridge reads with 3 entries and
  still 8 with 30, so discovery is not N+1 and no listing body/media is fetched.
- Reads never authenticate: `GET_USER_ACCOUNT` is not requested at startup or
  for browsing.
- Added dependency: `dompurify`, kept out of the entry bundle (lazy blog-detail
  chunk only). No MUI, no `qapp-core` root entry, no TipTap editor, no video
  player. Production entry chunk 382.32 kB raw / 120.25 kB gzip (+10.89 kB gzip
  over the Phase 1B baseline); DOMPurify sits in the 36.49 kB / 14.15 kB-gzip
  lazy blog-detail chunk.
- Tests: 29 files / 258 tests passing; `lint`, `typecheck`, `format:check` and
  the production build pass.
- **NOT VERIFIED (OWNER VALIDATION REQUIRED):** real Qortal host / Hub Developer
  Mode — `_qdnBase` routing, injected `_qdnName`, live `SEARCH_QDN_RESOURCES`,
  QDN media `<img>` serving, and clipboard inside the Q-App iframe.
- No QDN write path, transaction, publication, like/comment/tip, moderation or
  editor code was added. Nothing was committed or pushed for Phase 2A.

**Phase 1B foundation snapshot (2026-09-11, historical, superseded above):**

- The repository was cloned into the canonical local path (branch `main`,
  `origin` = the GitHub remote, no commits yet). At Phase 1A closure the remote
  was empty and the local path was not a Git repository.
- Application foundation: Vite 7.3.6, React 19.3.0, TypeScript 5.9.3
  (`strict`), `react-router-dom` 7.18.3, `createBrowserRouter` with
  `window._qdnBase` basename handling.
- Implemented: domain-oriented source tree, the `src/qortal/` integration
  boundary, semantic CSS design tokens, the responsive AppShell (top panels,
  real brand banner, primary action row, site navigation, footer),
  loading/empty/error states, route-level lazy boundaries and Vitest tests
  (9 files, 59 tests passing).
- Dependency footprint is deliberately small: no MUI/emotion, no `qapp-core`
  root entry, no video player, no TipTap. DOMPurify is deferred until the first
  feature that actually renders stored rich text.
- Commands: `npm run dev`, `npm run build` (`tsc -b && vite build`),
  `npm run preview`, `npm run lint`, `npm run typecheck`, `npm test`,
  `npm run format:check`.
- Measured production build (Node 20.19.2, 2026-09-11): entry chunk
  345.07 kB raw / 109.36 kB gzip; stylesheet 21.06 kB / 4.34 kB gzip; bundled
  banner WebP 202.89 kB; each lazy route a separate 0.3–1.7 kB chunk. That is
  the Phase 1A React+Router-only baseline (317.50 kB raw / 101.08 kB gzip) plus
  the shell/home code, and far below the `qapp-core`/MUI floor (~596 kB gzip).
- Headless-Chrome smoke test against the production build (320–2560 px, no
  horizontal overflow, ≥44 px interactive targets, visible focus, keyboard
  search disclosure, zero external network requests): **PASS**.
- **NOT VERIFIED:** real Qortal host and node dev-proxy rendering. No local
  Qortal node was available, so `_qdnName`-based owner detection, injected
  bridge behaviour and QDN CSP behaviour remain unvalidated at runtime.
- No QDN resource has been published, and nothing has been committed or pushed.
- Still not implemented: owner authentication, publishing, comments, likes,
  tips, moderation, deep search, catalogs and any QDN discovery. No Qortal/QDN
  API is called at all in this build.

### Phase 1A baseline snapshot (2026-09-11, historical)

Kept for traceability; re-verify before platform-dependent work.

- Remote repository existed and was empty; the local path existed, was empty,
  and was not yet a Git repository (both superseded — see above).
- No application source, package manifest or schema existed (superseded).
- Every Qortal source revision pinned in the workspace standard was re-verified
  as the repository `HEAD` on 2026-09-11 (`qortal` v6.1.9, `Qortal-Hub`
  `12a573b2`, `qapp-core` v1.0.79, `qapp-templates` `143cc7bf`, `q-tube` 2.1.0,
  `Subwire`, `Quitter`, `q-mail` 3.2.1, `create-qortal-app`).
- Measured production build baselines (Node 20.19.2, scratch clones): React 19
  + Router 7 only 317.50 kB raw / 101.08 kB gzip; `react-default-template`
  1,882.85 kB raw / 590.74 kB gzip; `q-tube` 3,389.48 kB raw / 1,015.14 kB
  gzip. Importing two small utilities from `qapp-core` yields 1,908.62 kB raw /
  596.00 kB gzip because the published entry statically imports `video.js` and
  the framework component set.
- Live read-only node evidence (`https://api.qortal.org`) confirms `APP`
  resources for `Q-Tube` (3,075,872 B), `SubWire` (2,488,912 B) and `Quitter`
  (3,925,296 B).

## Recommended next steps (not authorized by this document)

1. The Phase 1A decision matrix D1–D9 is now recorded (see the owner decisions
   above): D1–D8 are OWNER APPROVED, D9's wire representation is DEFERRED, and
   future Q-Tube interoperability is FUTURE / NOT VERIFIED. Publishing name and
   service are decided: `Shadow Archives` under `APP`. Like scope is decided:
   one active like per acting registered Qortal name per content item.
2. Phase 1B foundation scaffold — **DONE (2026-09-11)** per the bounded plan in
   [`../docs/shadow-archives-webportal/architecture/2026-09-11-phase-1b-implementation-plan.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-phase-1b-implementation-plan.md);
   see
   [`../docs/shadow-archives-webportal/implementation/`](../docs/shadow-archives-webportal/implementation/)
   for the implementation report. The in-repo `src/qortal/` layer and semantic
   CSS tokens are in place; no `qapp-core` root entry and no MUI (D6/D7).
3. **First publication — DONE (owner, 2026-09-11 18:32 UTC).** The owner
   published the Phase 2C-A artifact
   `release/shadow-archives-app-0.1.0-20260911.zip` under name `Shadow Archives`
   / service `APP` with the default identifier, establishing the real render
   context `qortal://APP/Shadow Archives`; Phase 2C-B then verified that served
   revision read-only (`PUBLIC-NODE VERIFIED`). **Next owner-authorized step:**
   run the remaining real-host checks listed in the Phase 2C-B report §22 (exact
   `_qdn*` values need a build containing the `/studio` diagnostics block, i.e.
   a later publication; deep-route hard reload; owner-capability click flow;
   live read pipeline). Owner detection is implemented and tested against the
   verified contracts; host confirmation is still outstanding. An owner decision
   is also open on whether `/studio` should be discoverable from public
   navigation (Phase 1A keeps it unlinked), and on whether to re-publish the
   `6354c88` artifact now that its content equivalence to the served build has
   been established.
4. Set a concrete performance budget from a real measured baseline in the dev
   proxy and a real host; the Phase 1A numbers are build-output comparisons, not
   runtime timings.
5. Implement one bounded issue at a time through Workflow v2.

## Mandatory project rules

- Never hardcode the owner name or address; resolve it at runtime.
- Never treat payload `author`/`owner` fields as authority.
- Never claim QDN data was deleted.
- Respect `prefers-reduced-motion`.
- Design for the QDN CSP; do not rely on third-party origins.
- Do not publish, deploy, transact or release without explicit owner
  authorization.
- Save reports only under the canonical report root above.
- Do not promote Shadow Archives product details into global workspace guides.
