# Project — shadow-archives-webportal-QORTAL

## Purpose and scope

Canonical project-specific context for the first onboarded Qortal Workflow v2
application. Read it after
[`../agents/00-SESSION-START.md`](../agents/00-SESSION-START.md). Shared rules
remain in the canonical workspace guides.

This file records product direction and owner decisions. It does **not**
authorize implementation. No Shadow Archives application code exists yet.

## Project identity

- Development name: `shadow-archives-webportal-QORTAL`
- Repository: `https://github.com/iffinland/shadow-archives-webportal-QORTAL`
- Local path:
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Application language: English
- Target platform: Qortal/QDN Q-App/webportal
- Planned frontend: Vite + React + TypeScript

## Repository and local path

- Remote repository: exists, empty (no commits as of 2026-09-11).
- Local path: exists, empty, and is **not** a Git repository as of 2026-09-11.
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
  namespace digit.
- Deployed resource URI: not yet established.

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

Verified 2026-09-11:

- Remote repository exists and is empty.
- Local path exists and is empty; not yet a Git repository.
- No application source, package manifest or schema exists.
- The identifier namespace is approved (`saw_`, D1), but no QDN resource for
  this application has been published under the decided publishing name/service
  by this workspace.
- Every Qortal source revision pinned in the workspace standard was re-verified
  as the repository `HEAD` on 2026-09-11 (`qortal` v6.1.9, `Qortal-Hub`
  `12a573b2`, `qapp-core` v1.0.79, `qapp-templates` `143cc7bf`, `q-tube` 2.1.0,
  `Subwire`, `Quitter`, `q-mail` 3.2.1, `create-qortal-app`).
- Measured production build baselines (Node 20.19.2, scratch clones): React 19
  + Router 7 only 317.50 kB raw / 101.08 kB gzip; current
  `react-default-template` 1,882.85 kB raw / 590.74 kB gzip; `q-tube`
  3,389.48 kB raw / 1,015.14 kB gzip. Importing two small utilities from
  `qapp-core` still yields 1,908.62 kB raw / 596.00 kB gzip because the
  published entry statically imports `video.js` and the framework component set.
- Live read-only node evidence (`https://api.qortal.org`) confirms `APP`
  resources for `Q-Tube` (3,075,872 B), `SubWire` (2,488,912 B) and `Quitter`
  (3,925,296 B).

This is a dated snapshot. Establish a fresh baseline before editing.

## Recommended next steps (not authorized by this document)

1. The Phase 1A decision matrix D1–D9 is now recorded (see the owner decisions
   above): D1–D8 are OWNER APPROVED, D9's wire representation is DEFERRED, and
   future Q-Tube interoperability is FUTURE / NOT VERIFIED. Publishing name and
   service are decided: `Shadow Archives` under `APP`. Like scope is decided:
   one active like per acting registered Qortal name per content item.
2. Scaffold the bounded Phase 1B foundation (shell, providers, routing
   boundaries, design tokens, capability plumbing, no writes) per
   [`../docs/shadow-archives-webportal/architecture/2026-09-11-phase-1b-implementation-plan.md`](../docs/shadow-archives-webportal/architecture/2026-09-11-phase-1b-implementation-plan.md).
   The scaffold does not use `qapp-core`'s published root entry or MUI
   (D6/D7 approved); use the in-repo `src/qortal/` layer and semantic CSS
   tokens.
3. Implement identity/owner detection first (it gates every write path).
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
