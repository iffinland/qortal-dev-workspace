# Shadow Archives — Phase 1A Architecture Report

- Project: `shadow-archives-webportal-QORTAL`
- Phase: 1A (architecture, QDN contracts, performance baseline) — **no
  application code, no scaffold, no Git initialisation**
- Date: 2026-09-11
- Author: Codex (Phase 1A research)
- Primary task class: architecture, identity and data integrity, with
  publication/discovery/scaling and performance as secondary classes
- Status: **OWNER DECISIONS RECORDED (2026-09-11)** — the architecture package
  is complete, internally validated and **implementation-authoritative for
  Phase 1B**. The owner recorded final Phase 1A decisions **D1–D9** (see §14):
  **OWNER APPROVED** D1–D8; **DEFERRED** D9 (like wire representation);
  moderation **OWNER APPROVED** owner-only for alpha; video/Q-Tube
  interoperability **FUTURE / NOT VERIFIED**. No runtime/host validation was
  possible in Phase 1A; deferred and NOT VERIFIED items remain open.
- Related:
  [`./2026-09-11-qdn-data-contracts.md`](./2026-09-11-qdn-data-contracts.md),
  [`./2026-09-11-performance-reference-comparison.md`](./2026-09-11-performance-reference-comparison.md),
  [`./2026-09-11-responsive-appshell-and-design-tokens.md`](./2026-09-11-responsive-appshell-and-design-tokens.md),
  [`./2026-09-11-phase-1b-implementation-plan.md`](./2026-09-11-phase-1b-implementation-plan.md),
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md)

## 0. Scope, sources and fact labels

This report answers the 18 Phase 1A architecture questions. It does not
implement anything. Sources, revisions and measurement method are recorded in
the performance comparison; the fact labels used are the workspace standard's:
**VERIFIED**, **INFERENCE**, **UNKNOWN**, **OWNER DECISION**.

Re-verified on 2026-09-11: every pinned revision in the workspace standard is
still the repository `HEAD` (`qortal` v6.1.9, `Qortal-Hub` `12a573b2`,
`qapp-core` v1.0.79, `qapp-templates` `143cc7bf`, `q-tube` 2.1.0, `Subwire`,
`Quitter`, `q-mail` 3.2.1, `create-qortal-app`, plus the reference app).

Live read-only node evidence: `https://api.qortal.org`, queried 2026-09-11
(~11:40 UTC). Recorded in the performance comparison §6 and §14 below.

## 1. Application foundation

### 1.1 Verified current baseline

**VERIFIED** (`qapp-templates/react-default-template`, `143cc7bf`):

| Item | Value |
| ---- | ----- |
| React | `^19.0.0` |
| TypeScript | `~5.7.2` |
| Vite | `^6.3.5`, `base: ''` |
| Router | `react-router-dom` `^7.3.0` |
| Router construction | `createBrowserRouter(routes, { basename: window._qdnBase \|\| '' })` |
| Provider | `qapp-core` `GlobalProvider` with `appName`, `publicSalt`, `auth` |
| Styling | MUI 7 + emotion, custom theme provider |
| State | `jotai` |
| i18n | `i18next` / `react-i18next` |
| App config | `scripts/initialize.js` generates `src/qapp-config.ts` with a random `publicSalt` |

**VERIFIED** current app practice: `q-tube` (React 19.2, Vite 7.3.2,
`react-router-dom` 7, MUI 7), `Subwire` (React 19, Vite 6.3.5, MUI 7),
`Quitter` (React 19, Vite 6.3.5, MUI 7, `manualChunks`, `lazy`). All four
inspected apps (`q-tube`, `Subwire`, `Quitter`, `q-mail`) use
`createBrowserRouter` + `_qdnBase` (q-mail via modal routing on top of the same
pattern). **No current app uses `HashRouter`;** only the legacy reference app
does.

### 1.2 Recommendations

| Component | Recommendation | Why |
| --------- | -------------- | --- |
| React | **19.x** (`^19.2.0`) | current template and all current apps; no reason to diverge |
| TypeScript | **5.8+ with `strict`** | current apps; `strict` is required to keep contract parsing honest |
| Vite | **6.3.x** (starter parity) or **7.x** (q-tube precedent) | both current; pick 6.3.x for lowest scaffold risk, 7.x for newest app parity. Node ≥ 20.19 required for Vite 7 (satisfied) |
| Build output | `base: ''`, relative asset URLs | verified required for `/render/...` `<base href>` handling |
| Router | **`createBrowserRouter` + `RouterProvider`, `basename: _qdnBase`** | verified current pattern; `APP` resources auto-route unknown paths to `index.html`, so browser history works inside the iframe |
| `HashRouter` | **reject** | legacy reference only; breaks clean QDN URLs, shares the wrong links, and fights `_qdnBase` |
| `qapp-core` | **do not import the root entry in the shell** (see §2) | measured 596 kB gzip baseline for importing two small utilities |
| MUI | **do not use** (see §2) | measured cost + custom visual identity |
| Global state | one small in-repo store (Zustand or React context + reducers) | the app needs a handful of stores; `jotai` is optional, not required |
| i18n | not needed for Phase 1 (English only) | owner decision: application language is English. Keep strings in one module so i18n can be added later without a refactor |
| `publicSalt` | **not needed** under the recommended identifier scheme | the salt exists to namespace `qapp-core`'s hashed identifiers; a readable prefix scheme removes that coupling. If any hashing is used for internal cache keys, derive it from a fixed, published constant |

### 1.3 QDN basename handling (**VERIFIED**)

- Core injects `_qdnContext`, `_qdnTheme`, `_qdnLang`, `_qdnService`,
  `_qdnName`, `_qdnIdentifier`, `_qdnPath`, `_qdnBase`, `_qdnBaseWithPath`
  (`HTMLParser.addAdditionalHeaderTags`), plus `<base href=".../">`.
- `baseHref = usingCustomRouting ? _qdnBase : _qdnBaseWithPath` — for a route
  auto-served from `index.html`, `_qdnBase` is the correct router basename.
- `_qdnName` is percent-encoded for names containing spaces
  (`ArbitraryDataRenderer`: `resourceId.replace(" ", "%20")`). Therefore
  `Shadow Archives` arrives as `Shadow%20Archives` and must be decoded before
  comparison, re-encoded for `/names/{name}` lookups.
- In dev-proxy context `_qdnName`, `_qdnIdentifier` and `_qdnBase` are **empty**
  (`DevProxyServerResource` constructs `HTMLParser("", …)`), so owner logic
  cannot be exercised in the proxy and must be tested in a real host.

### 1.4 Provider structure

```text
<ErrorBoundary (root, branded)>
  <BridgeProvider>            // detect qortalRequest + read _qdn* once
    <AuthProvider>            // single-flight auth: account, name(s), ownership
      <CapabilityProvider>    // derived visitor / authenticated / owner
        <CacheProvider>       // IndexedDB + in-memory caches, TTLs
          <CatalogProvider>   // manifest + partitions, stale-while-revalidate
            <DesignTokensProvider>  // theme class + host theme/lang sync
              <RouterProvider router={…} />
```

Rules:

- UI components never touch `window.qortalRequest` directly; they call the
  typed wrapper.
- Providers must render the shell usefully when the bridge is absent, when auth
  is pending, and when auth is rejected. None of those states may throw.
- A lazy route's failure must not unmount the shell.

### 1.5 Error-boundary strategy

| Level | Catches | Renders |
| ----- | ------- | ------- |
| Root | render errors outside routes | branded full-page recovery panel with "reload" and the app's provenance line |
| Route | a single route's render/data failure | route-scoped panel inside the shell so navigation still works |
| Region/widget | engagement, media, editor widgets | an inline placeholder with retry; the page stays usable |
| Async data | fetch/malformed-payload failures | explicit state machine (`idle/loading/ready/empty/partial/unavailable/malformed/error`) |

Never render a blank screen. Never convert a bridge/parse failure into a valid
domain value (for example a `0` like count or an "empty" result).

## 2. UI / dependency strategy

### 2.1 Measured evidence (see the performance comparison for full tables)

| Configuration | Entry JS raw | gzip |
| ------------- | ------------ | ---- |
| React 19 + Router 7 only | 317.50 kB | 101.08 kB |
| + MUI 7 subset (6 components, 1 icon) | 435.35 kB | 139.67 kB |
| `qapp-core` root import (2 utilities only) | 1,908.62 kB | 596.00 kB |
| current starter (React + MUI + `qapp-core` + i18n, near-empty UI) | 1,882.85 kB | 590.74 kB |
| Quitter initial preloaded set | 2,071.75 kB | 634.28 kB |
| Subwire (single chunk) | 2,621.26 kB | 804.93 kB |
| q-tube (single chunk) | 3,389.48 kB | 1,015.14 kB |

**VERIFIED** additional facts:

- The published `qapp-core` ESM entry statically imports `video.js` (and its
  CSS), `zustand`, MUI, `react-idle-timer`, `react-hot-toast`, `dayjs`,
  `crypto-js`, `aes-js` and a vendored `nacl-fast`. Importing two small pure
  utilities still produced full video.js in the bundle (`vjs-` × 355).
- `qapp-core` declares no `sideEffects` field and exposes no deep import
  subpaths, so no consumer can import "just the small parts".
- MUI's own cost scales with components used: the subset above costs ≈+39 kB
  gzip, while Quitter's broad MUI surface is 380 kB raw / 110 kB gzip.
- Retained fonts are large: the starter emits four Inter weights (≈1,260 kB) and
  q-tube emits fourteen Roboto weights (≈2,050 kB).

### 2.2 Recommendation (`OWNER APPROVED — D6`)

**Do not use MUI.** Build on a semantic CSS-token layer (see the AppShell
specification) plus a small set of in-repo components: `Button`, `IconButton`,
`Card`, `Dialog`, `Tooltip`, `Tabs`, `Skeleton`, `Toast`, `Field`. Icons are
in-repo inline SVG components.

Justification against the owner's criteria:

- **Startup bundle size.** Measured: MUI plus `qapp-core` is the dominant cost;
  the custom path targets ≈100–150 kB gzip for the shell instead of ≈600 kB.
- **Maintainability.** MUI's theme system, emotion runtime and `sx` prop create
  a second styling language that fights a bespoke brand; a token layer has one.
- **Accessibility.** MUI provides good defaults, but they are not free: a
  hand-built `Dialog` must implement focus trap, `aria-modal`, escape handling
  and restore-focus. This is real, bounded work and must be explicitly tested.
  The recommendation accepts that cost in exchange for size and control.
- **Responsive behaviour.** The owner's layout (fixed 240px side panels,
  reserved 300–340px banner band, marquee panels, TV focus sizing) is easier to
  express in plain CSS than to bend MUI's grid/`sx` system around.
- **TV focus/navigation.** Focus rings and hit targets are simpler to guarantee
  with explicit CSS than through theme overrides.
- **Visual uniqueness.** The brand explicitly rejects generic blue dApp styling
  and glassmorphism; using the same MUI surface as `q-tube`/`Subwire`/`Quitter`
  would make Shadow Archives look like the ecosystem default.

**Rejected alternative (documented for completeness):** use MUI 7 with a heavy
custom theme. It is the fastest path to accessible primitives and matches every
current app, at a measured +110 kB gzip or more for the MUI surface alone (plus
the `qapp-core` decision in §3). The owner approved the no-MUI strategy (D6);
adding a generic UI framework to Phase 1B would require a new evidence-backed
reason and owner approval.

**Do not reject MUI without measurement** — the measurements above are the
basis for the recommendation, and the alternative remains documented.

## 3. Qortal integration layer and `qapp-core` decision

### 3.1 Problem

`qapp-core` is the current framework, but its published form is a single
monolithic entry. Any use of `GlobalProvider`, `useAuth`, `useResources` or even
`RequestQueueWithPromise` pays the full ~596 kB gzip cost including video.js,
MUI and the entire component set.

### 3.2 Recommendation (`OWNER APPROVED — D7`)

Create an in-repo layer `src/qortal/` that owns all platform interaction:

| Module | Responsibility |
| ------ | -------------- |
| `bridge.ts` | detect `qortalRequest`, typed wrapper, timeouts, error taxonomy, no raw global calls elsewhere |
| `actions.ts` | typed action/field contracts for the subset used (`SEARCH_QDN_RESOURCES`, `FETCH_QDN_RESOURCE`, `GET_NAME_DATA`, `GET_ACCOUNT_DATA`, `GET_ACCOUNT_NAMES`, `GET_PRIMARY_NAME`, `GET_USER_ACCOUNT`, `PUBLISH_*`, `LINK_TO_QDN_RESOURCE`) |
| `auth.ts` | single-flight account request, permission states, name resolution, ownership checks |
| `capability.ts` | owner/visitor derivation from `_qdnName` + ownership |
| `identifiers.ts` | the `saw_*` identifier codec (build/parse/validate) |
| `queue.ts` | bounded-concurrency request queue with cancellation |
| `cache.ts` | IndexedDB stores with explicit success/failure TTLs |
| `publish.ts` | publish/multi-publish wrappers, approval states, no automatic retry of ambiguous writes |
| `urls.ts` | QDN resource URL builders honouring `_qdnBase` and the CSP |

Behavioral reference for each module is the pinned current source
(`Qortal/qortal` `q-apps.js`, `Qortal-Hub` `src/qortal/*.ts`) — not memory and
not `qapp-core`'s type names.

**Rejected alternative (documented for completeness):** use `qapp-core`
`GlobalProvider` for auth, lists and identifiers and accept the measured
~600 kB gzip baseline. This reduces re-implementation risk and keeps the app
aligned with the ecosystem, at the cost of the owner's first-class performance
goal. The owner approved the in-repo `src/qortal/` integration layer (D7) based
on the Phase 1A measured bundle impact; importing `qapp-core` through its
published root entry in the application startup path remains rejected. Copy
`qapp-core` internals only where a contract genuinely requires it, and keep the
layer minimal and contract-focused.

## 4. Route architecture

| Route | Purpose | Split boundary | Access |
| ----- | ------- | -------------- | ------ |
| `/` | Home (Top Posts, Top Videos, Latest Posts, Latest Videos, gallery strip) | shell | public |
| `/blog?page=N` | paginated blog list | `blog-list` chunk | public |
| `/blog/:postRef` | blog detail + comments + engagement | `blog-detail` chunk | public |
| `/videos?page=N` | paginated video list | `video-list` chunk | public |
| `/videos/:videoRef` | video detail; player loaded on demand | `video-detail` chunk + `video-player` dynamic chunk | public |
| `/gallery` | albums + recent items | `gallery-list` chunk | public |
| `/gallery/album/:albumRef` | album contents | `gallery-album` chunk | public |
| `/gallery/item/:itemRef` | single item (lightbox/detail) | `gallery-item` chunk | public |
| `/about` | static/about content | `about` chunk | public |
| `/contact` | Q-Mail contact form | `contact` chunk (+ lazy rich-text composer if needed) | public |
| `/category/:slug` | cross-type category results | `taxonomy` chunk | public |
| `/tag/:slug` | cross-type tag results | `taxonomy` chunk | public |
| `/search?q=&type=` | deep search UI | `search` chunk (+ lazy local index bootstrap) | public |
| `/studio` | owner dashboard | one lazy `studio` chunk | owner only |
| `/studio/new/:type` | owner create | studio chunk | owner only |
| `/studio/edit/:type/:ref` | owner edit | studio chunk + lazy `editor` chunk | owner only |
| `/studio/moderation` | moderation overlay management | studio chunk | owner only |
| `/studio/settings` | site config, external app targets | studio chunk | owner only |
| `*` | not found | shell | public |

Rules:

- `:postRef`/`:videoRef`/`:galRef` are the entity's **stable short id**, not the
  full QDN identifier. Because the id is embedded in the identifier
  (`saw_post_<id12>`), a deep link resolves with **one** exact search under the
  publisher name even when the catalog is unavailable.
- Studio routes are gated by capability **and** by a lazy import boundary; the
  chunk must not be part of the initial graph. Gating is a UI/authorization
  boundary — writes still depend on the host's approval and current name
  ownership.
- A route-level `Suspense` fallback must be layout-stable (same reserved boxes
  as the loaded route).

## 5. Engagement, comments and moderation

**Owner decision status.** The like **identity** rule is **OWNER APPROVED**
(2026-09-11): one active like per acting registered Qortal name per content
item, never deduplicated across names of the same account/address. The exact
active/inactive/tombstone **wire representation is DEFERRED (D9)** pending a
controlled QDN overwrite/runtime test; Phase 1B may define the interface
boundary but must not claim an unverified wire format.

**Moderation (OWNER APPROVED for alpha).** No delegated moderators; moderation
authority is the current owner of the Shadow Archives publishing name. The
design stays extensible so delegated moderation can be added later without
rewriting content entities.

Full normative contracts are in
[`./2026-09-11-qdn-data-contracts.md`](./2026-09-11-qdn-data-contracts.md)
§5–§8. Summary of the design and its rationale:

- **Like identity.** `DOCUMENT` / `saw_lk_<targetType><targetId12>`, published
  under the **acting registered name**, with state inside the payload
  (`active`/`inactive`; exact wire representation **DEFERRED — D9**).
  `(name, service, identifier)` uniqueness gives exactly one like resource per
  acting name per target, so:
  - one name cannot create duplicate active likes (re-like overwrites);
  - two names of the same account produce two independent resources and are
    **never** deduplicated by address (owner decision preserved);
  - unlike updates the same identity.
- **The actor is not encoded in the identifier.** This is deliberate: it keeps
  identifiers short, prevents cross-name collisions, and lets one search return
  all likes for a target (including the caller's own, since results carry
  `name`).
- **Counting.** Never the raw resource count. **Candidate** fast path (D9
  wire representation is **DEFERRED**): publish a deterministic metadata tag
  (`saw_active` / `saw_inactive`) so one `SEARCH_QDN_RESOURCES` with
  `includemetadata=true` classifies all likes for a target. **NOT VERIFIED at
  runtime** — must be proven with one controlled owner publication before the
  wire format is chosen. Fallback: fetch payloads for that single target under
  a bounded queue; if any remain unclassifiable, report `>= N`.
  - This corrects the reference app's defect (`page.length` presented as a
    total) and the current apps' raw-count behaviour.
- **Card counts.** On listing pages, counts come from the catalog snapshot and
  are labelled as of `compiledAt`. Exact values resolve on the detail view.
- **Comments.** `COMMENT` / `saw_cmt_<targetType><targetId12>_<uid8>`; author
  name is authority; edit republishes the same identifier and sets `editedAt`;
  only the author may edit; target identity is validated exactly. One prefix
  search per target, paginated.
- **N+1 avoidance.** No per-card metadata/status/engagement queries. One search
  per target on detail views; catalog snapshot on listings; bounded queue;
  cached by identifier with TTL.
- **Moderation.** Owner-only overlay (`saw_mod_<target>`) plus one index
  resource (`saw_modindex`) so moderation applies with a single fetch. The
  overlay is applied last, after entity reduction. UI copy is
  "Hidden in Shadow Archives", never "deleted". It cannot affect the network,
  other apps, or the on-chain record.
- **Tips and share.** **NOT designed**; Qortal transport mechanisms for tips and
  shares were not verified. They must not be implemented as QDN publications
  until a current mechanism is confirmed.

## 5A. Video architecture and future Q-Tube interoperability (owner decision, 2026-09-11)

**OWNER APPROVED (new decision).** Shadow Archives will support publishing its
own video content to QDN.

The architecture **MUST ALSO** preserve a **future** capability whereby a video
published through Shadow Archives can participate in / appear through the
Q-Tube ecosystem using the appropriate QDN/Q-Tube publication/discovery
contract.

**FUTURE / NOT VERIFIED.** Do **not** implement Q-Tube interoperability now and
do **not** guess the exact Q-Tube metadata, identifier, indexing or publication
contract. The exact interoperability contract is **FUTURE / NOT VERIFIED** until
a dedicated Q-Tube source/runtime investigation is performed. Shadow Archives
must not import Q-Tube source code or depend directly on the Q-Tube
application.

The video domain is architected as separate layers so a future adapter does not
require an entity rewrite:

```text
Video entity
  -> Shadow Archives metadata        (this app's payload: title, taxonomy, ...)
  -> QDN media resource reference    (verified fields; not an opaque app-only ref)
  -> publication/discovery adapter   (FUTURE boundary; Q-Tube contract NOT VERIFIED)
```

The media reference must identify QDN media by verified fields —
`service`/`name`/`identifier` and `path` where applicable — rather than storing
an opaque Shadow-Archives-only blob reference, so a future Q-Tube
publication/discovery adapter can map it without re-publishing the entity. See
contracts §5.2.

## 6. Taxonomy decision

See contracts §5.8. Recommendation: **hybrid** — free-form app-managed
categories and tags carried in the entity payload and catalog (authoritative for
the app), with an optional mirror into Core metadata. **OWNER APPROVED — D2:**
Shadow Archives app-managed categories/tags are the canonical cross-content
taxonomy; Core category metadata may be mirrored where useful for QDN-ecosystem
discoverability, but the fixed Core enum must not limit the application's own
cross-type taxonomy.

Evidence:

- **VERIFIED.** Core `Category` is a fixed enum (~53 values), one per resource
  (`Category.java`).
- **VERIFIED.** Metadata is limited to title ≤ 80, description ≤ 240, tag ≤ 20,
  **max 5 tags** (`ArbitraryDataTransactionMetadata.java`).
- **VERIFIED.** Core search filters by `query`/`keywords`/`title`/`description`;
  there is no parameter that filters by metadata `tags`. `q-tube` works around
  this by encoding `**category:<id>;subcategory:<id>;**` into `description`.
- **INFERENCE.** Those limits make a Core-only taxonomy impossible for a shared
  cross-type taxonomy with autocomplete and cross-type pages.

Autocomplete comes from the catalog's taxonomy index (client-side, with
substring highlight); no QDN request per keystroke. **OWNER APPROVED (D2).**

## 7. Editor and stored rich-text model

### 7.1 Evidence

- **VERIFIED.** Current Qortal Hub uses TipTap 2.11.x (`@tiptap/react`,
  `@tiptap/starter-kit`, `extension-color`, `-highlight`, `-image`,
  `-mention`, `-placeholder`, `-text-style`, `-underline`) plus
  `dompurify` ^3.4.3 and a custom `configureDomPurify` hook that adds
  `rel="noopener noreferrer"` to `target="_blank"` links.
- **VERIFIED.** `q-tube`, `Subwire` and `Quitter` use `react-quill-new`
  (Quill 2) + DOMPurify. `q-mail` uses TipTap 2 + Slate + react-quill.
- **VERIFIED.** The reference app hand-rolls sanitization; the workspace
  standard forbids copying that.
- **MEASURED.** Quitter's editor chunk is 232.24 kB raw / 64.98 kB gzip for
  Quill + `quill-image-resize-module-react`; emoji picker 268.92 kB raw.

### 7.2 Recommendation (`OWNER APPROVED — D3/D4`)

- **Editor library: TipTap (ProseMirror).** Chosen over Quill and Lexical
  because current Hub already uses it (a live, maintained, in-ecosystem
  reference), the extension set maps directly onto the required presets
  (bold/italic/underline/bullet/ordered/colour/emoji/links/images), and its
  canonical output is a structured document (JSON), which is a better storage
  format than HTML for sanitization and migration. Lexical is a reasonable
  alternative but has no current Qortal precedent.
- **Comment preset:** bold, italic, underline, bullet list, ordered list,
  red/yellow/green/blue text colour, emoji. Implemented with a minimal TipTap
  extension set, lazy-loaded only when the composer is opened.
- **Owner editor:** the full extension set, lazy-loaded in the owner/studio
  chunk. Never in the shell.
- **Canonical stored representation:** structured document JSON
  (`{ format: "tiptap-json-v1", doc: … }`) plus a bounded plain-text extract
  (`bodyText`) for search. Render to HTML through **one** in-repo renderer that
  emits only allowlisted markup, with DOMPurify applied as defence in depth.
  Rationale: a single source of truth, no sanitizer drift between write and
  read, and schema migrations are data transforms rather than HTML surgery.
- **Sanitizer:** DOMPurify (maintained; used by Hub and every current app), with
  a strict allowlist, an explicit URL-scheme policy (`javascript:`, `data:`,
  `vbscript:` rejected for links; `data:`/`blob:` only where a media element
  requires it; all QDN media via same-origin URLs), and a post-sanitize hook
  that cannot reintroduce unsafe markup (mirroring Hub's `rel` hook).
- **Plain text** is escaped and rendered as text, never as HTML.
- **Migrations:** `schemaVersion` + `bodyFormat`; readers support the current
  and previous format and quarantine unknown ones.

**Rejected alternative (documented for completeness):** store sanitized HTML
(`{ format: "html-v1", html: … }`). Simpler to render and closer to the
current-app norm, but it stores a sanitizer artifact as the source of truth and
makes future sanitizer/format changes a migration hazard. The owner approved
the structured `tiptap-json-v1` model (D4).

## 8. Contact / Q-Mail

### 8.1 Verified Q-Mail convention (`q-mail` 3.2.1, `ddf3aa92`)

- Service: **`MAIL_PRIVATE`**; thread/notification resources use `MAIL`
  (group path). Payloads are encrypted to recipient public keys.
- Identifier: `_mail_qortal_qmail_<recipientName.slice(0,20)>_<recipientAddress.slice(-6)>_mail_<uid>`
  (or the alias form). Note the **20-character name truncation** — an app that
  intends Q-Mail interop must reproduce it exactly.
- Publication: `PUBLISH_MULTIPLE_QDN_RESOURCES` with `encrypt: true` and
  `publicKeys: [recipientPublicKey, …]`, published under the **sender's own
  name**.
- Payload (base64 JSON): `subject`, `createdAt`, `version: 1`,
  `attachments`, `textContentV2`, `generalData.thread`/`threadV2`,
  `recipient`.
- Recipient resolution in Q-Mail: `GET_NAME_DATA` → `owner`, then
  `GET_ACCOUNT_DATA` → `publicKey`.
- Discovery: `/arbitrary/resources/search?service=MAIL_PRIVATE&query=qortal_qmail_<name20>_<addrLast6>_mail_&includemetadata=true&reverse=true`.

**This is a community-app convention, not a Core API.** It must be re-verified
against the current Q-Mail release immediately before implementation.

### 8.2 Shadow Archives contact design

1. Recipient = the app's own publishing name (decoded from `_qdnName`), with an
   optional `contact.recipientName` override in `saw_cfg`.
2. Resolve name → owner address → account public key. Fail closed if any step is
   missing.
3. Require the sender to be authenticated **and** to own a registered name (writes
   are published under the sender's name).
4. Publish with the Q-Mail identifier convention (including the 20-character
   truncation) and Q-Mail's payload shape so the message is readable in Q-Mail.
5. Success feedback states what actually happened: submitted for approval,
   approved/published, or failed with a reason.

Failure conditions to handle explicitly: no bridge; no account; account
permission rejected; no registered name; recipient name not found; recipient
public key unavailable; publish rejected/timed out; node offline; identifier
length/encoding problem.

### 8.3 Recommended fallback (`OWNER APPROVED — D5`)

If verified Q-Mail delivery cannot be completed: **preserve the user's draft**
(keep it in the form and autosave it to IndexedDB), **clearly explain that
Q-Mail delivery is unavailable/failed**, and provide an explicit
**user-triggered Copy Message action** so the user can send it through Q-Mail
directly.

**Do not** silently substitute `SEND_CHAT_MESSAGE` or another transport.
`SEND_CHAT_MESSAGE` is a Qortal chat action, not Q-Mail; substituting it would
change the recipient experience and the message's discoverability without
telling the user.

## 9. Q-Tube / SubWire / Quitter links

### 9.1 Verified (LIVE read-only node, `https://api.qortal.org`, 2026-09-11)

| App | Registered name | Name owner (at query time) | APP resource |
| --- | --------------- | -------------------------- | ------------ |
| Q-Tube | `Q-Tube` (reduced `q-tube`) | `Qjd6bc36X9Aws45i3vgWqQfgsBu9LC68Mr` | present, 3,075,872 bytes |
| SubWire | `SubWire` (reduced `subwire`) | `QRntQARYCNT6M16VGR9zCcf1KvMPNTd5TA` | present, 2,488,912 bytes |
| Quitter | `Quitter` (reduced `quitter`) | `QfDv4Y1uKVFoAWABsZcwbX2yX7SaEw35s2` | present, 3,925,296 bytes |

The published names are `Q-Tube`, `SubWire`, `Quitter`; the GitHub repository
casing (`q-tube`, `Subwire`) is **not** the published identity.

### 9.2 Link mechanism (**VERIFIED**)

- `q-apps.js` `interceptClickEvent` intercepts `qortal://` anchors and issues
  `LINK_TO_QDN_RESOURCE`.
- `LINK_TO_QDN_RESOURCE` compares the target name with the current app's name
  and calls `openNewTab(...)` when they differ, waiting 200 ms for
  `SET_TAB_SUCCESS`, with a `window.location` fallback.
- The same handler calls `preventDefault()` on every `http(s)`/`//` anchor, so
  Web2 links cannot navigate from inside the app.

### 9.3 Recommendation

- Primary: a real anchor `href="qortal://APP/Q-Tube"` (and `SubWire`, `Quitter`)
  so the platform intercepts it and the item behaves like a link (middle-click,
  keyboard).
- Fallback: a programmatic `LINK_TO_QDN_RESOURCE` request if the anchor path is
  unavailable.
- The three names come from `saw_cfg.externalApps` with the verified values as
  defaults, so the owner can correct them without an app redeploy. They must
  never be treated as timeless constants.
- Web2 HTTPS links use copy-to-clipboard with visible feedback.

## 10. External-link (Web2) policy implementation notes

- **VERIFIED.** The platform blocks `http(s)` navigation from inside a Q-App, so
  copy-to-clipboard is both the owner's product decision and the only
  behaviour the platform permits.
- `_qdnName`/`_qdnIdentifier`-based external Web2 links open in a new tab only
  via the host; Shadow Archives does not attempt `window.open` for Web2 URLs.
- Clipboard access inside the iframe is **NOT VERIFIED**: `navigator.clipboard`
  may be restricted by permissions policy. Implement a cascade:
  `navigator.clipboard.writeText` → `document.execCommand('copy')` on a
  temporarily selected off-screen text node → reveal a selectable input with the
  URL and instructions. Always show explicit success/failure feedback (toast +
  inline state), never fail silently.
- Linkify: only explicit `http(s)` URLs in stored content become link affordances
  with the copy action; raw stored HTML never becomes a live external link.

## 11. Owner detection

### 11.1 Flow

```text
1. read _qdnService (expect APP) and _qdnName
2. decode %20 in _qdnName -> publisherName          (never re-encode for display)
3. if no bridge OR _qdnContext === "proxy"          -> capability "unknown"
4. single-flight AUTH request (host-mediated, approval-gated):
     GET_USER_ACCOUNT -> { address, publicKey }
     - pending            -> "resolving"
     - rejected/denied    -> "visitor"        (no automatic retry, no loop)
     - granted/no account -> "visitor"
5. if account:
     GET_NAME_DATA(publisherName) -> nameData.owner
     - nameData missing            -> "authenticated-non-owner" (app publisher not resolvable)
     - owner === account.address   -> "owner"
     - owner !== account.address   -> "authenticated-non-owner"
6. acting name for writes:
     GET_PRIMARY_NAME(address)      -> preferred acting name
     GET_ACCOUNT_NAMES(address)     -> all owned names (selectable)
     - none owned                  -> "authenticated-no-name" (cannot publish; say so)
7. revalidate ownership before any write (session-scoped, short TTL)
```

### 11.2 Capability states

| State | Meaning | Owner UI |
| ----- | ------- | -------- |
| `unknown` | bridge/context unresolved (proxy, plain browser, pending auth) | hidden |
| `visitor` | no account, or permission rejected | hidden |
| `authenticated-no-name` | account exists but owns no registered name | hidden (show "register a name to comment") |
| `authenticated-non-owner` | account does not own the app publisher name | hidden |
| `owner` | account address === current owner of the decoded app publisher name | visible |

### 11.3 Mandatory properties

- The owner identity is **derived at runtime** from `_qdnName` + current name
  ownership. No hardcoded name or address anywhere, including tests.
- Payload `publisher`/`author`/`owner` fields are never an authority test.
- **Avoid duplicate auth prompts:** a single shared in-flight auth promise; a
  rejection is cached for the session; no component may independently trigger
  `GET_USER_ACCOUNT`.
- **Name transfer:** ownership is re-resolved per session and immediately before
  writes; a transferred name loses/acquires controls on the next resolution.
- **No name:** publish/comment affordances are hidden or explain the
  requirement; the app must not fail with an opaque error.
- **Rejected permission:** the app remains fully usable read-only; never retry
  automatically.
- **Proxy/dev context:** owner controls cannot be validated there; the app shows
  an explicit dev notice instead of pretending to be the owner.

## 12. Responsive AppShell specification

See
[`./2026-09-11-responsive-appshell-and-design-tokens.md`](./2026-09-11-responsive-appshell-and-design-tokens.md)
for the full breakpoint table, header behaviour, auto-scroll rules, focus/hit
targets, skeleton strategy and the design-token proposal. Key constraints
restated here:

- Desktop/TV header: `240px | banner | 240px`, banner reserved in a 300–340px
  band; the 16:9 source image must not dictate header height.
- Main shell ≈90vw, clamped to a sensible maximum.
- Top Posts / Top Videos scroll vertically; the gallery strip scrolls
  horizontally; all auto-scroll pauses on hover, focus, interaction and
  `prefers-reduced-motion`, and content stays reachable with motion disabled.
- Video cards never load video bytes; gallery listings never load originals.
- Mobile is a genuine reflow, not squeezed columns.
- Skeletons reserve the final geometry to avoid layout shift.

## 13. Phase 1B plan

See
[`./2026-09-11-phase-1b-implementation-plan.md`](./2026-09-11-phase-1b-implementation-plan.md).

## 14. Final owner decision record (D1–D9)

**Status key:** `OWNER APPROVED` · `DEFERRED` · `NOT VERIFIED` ·
`FUTURE CAPABILITY`.

The owner recorded these final Phase 1A decisions on 2026-09-11. This is the
implementation-authoritative decision record for Phase 1B. The original
recommendation analysis is preserved in §14.2 for traceability; where a
recommendation and a decision differ, the decision wins.

| # | Decision | Final owner state | Approved / decided outcome |
| - | -------- | ----------------- | -------------------------- |
| D1 | Identifier namespace | **OWNER APPROVED** | Namespace prefix `saw_` (Shadow Archives Web). Conceptually `saw_post_<stable-id>`, `saw_vid_<stable-id>`, `saw_img_<stable-id>`, `saw_album_<stable-id>`, `saw_cmt_<target-or-stable-scope>_<comment-id>`, `saw_lk_<target-stable-id>`. The existing evidence-based stable-ID encoding is retained (`<id12>` base36, `<uid8>`). Schema evolution is represented by the payload `schemaVersion`, **not** by a namespace digit; **no `saw1_` migration** is required or defined. |
| D2 | Taxonomy | **OWNER APPROVED** | Hybrid taxonomy. Shadow Archives app-managed categories/tags are the canonical cross-content taxonomy; Core category metadata may be mirrored where useful for QDN-ecosystem discoverability, but the fixed Core enum must not limit the application's own cross-type taxonomy. |
| D3 | Editor | **OWNER APPROVED** | TipTap. The heavy owner editor must remain lazy-loaded and outside the visitor startup path. |
| D4 | Stored rich-text / rendering model | **OWNER APPROVED** | Canonical structured representation `tiptap-json-v1`; normalized/searchable `bodyText` alongside it where defined; DOMPurify-based sanitized rendering boundary; global canonical rendering-safety rules remain authoritative and must not be weakened. |
| D5 | Q-Mail failure UX | **OWNER APPROVED** | If verified Q-Mail delivery cannot be completed: preserve the user's draft; clearly explain delivery is unavailable/failed; provide an explicit user-triggered Copy Message action; do **not** silently substitute `SEND_CHAT_MESSAGE` or another transport. |
| D6 | UI dependency strategy | **OWNER APPROVED** | No MUI. Use semantic CSS design tokens, in-repository reusable components, inline/local SVG icons and accessible native semantics. No generic UI framework may be added to Phase 1B without a new evidence-backed reason and owner approval. |
| D7 | Qortal integration strategy | **OWNER APPROVED** | Do not import `qapp-core` through its published root entry in the application startup path. Use a small in-repository `src/qortal/` integration layer based on the verified current Qortal bridge/API contracts. Keep it minimal and contract-focused; do not copy `qapp-core` internals unnecessarily. |
| D8 | Catalog | **OWNER APPROVED** | Partitioned `DOCUMENT` catalog + manifest. Entity resources remain authoritative. Catalogs are derived, rebuildable, versioned, cacheable, permitted to be stale, and never evidence of publisher authority. Phase 1A recovery and partitioning rules are preserved. |
| D9 | Like-activeness wire representation | **DEFERRED** | The identity rule itself is **DECIDED**: one active like per acting registered Qortal name per content item. The exact active/inactive/tombstone wire representation must be selected after a controlled QDN overwrite/runtime test. Phase 1B may define an interface/type boundary but must not claim an unverified wire format. |

### 14.1 Supporting decisions (not owner D-numbered)

- **Comment service.** `COMMENT` (single file, 500 KB cap) over
  `BLOG_COMMENT`; a minor divergence from current apps. Not an owner decision;
  recorded here so the owner decision matrix stays D1–D9.
- **Moderation — OWNER APPROVED for alpha.** No delegated moderators;
  moderation authority is the current owner of the Shadow Archives publishing
  name. Keep the architecture extensible so delegated moderation can be added
  later without rewriting content entities.
- **Video + future Q-Tube interoperability — OWNER APPROVED.** Shadow Archives
  will publish its own video content to QDN and must preserve a **future**
  capability to participate in / appear through the Q-Tube ecosystem. The exact
  Q-Tube contract is **FUTURE / NOT VERIFIED**. See §5A.

### 14.2 Recommendation analysis (traceability)

| # | Decision | Recommended | Alternatives | Advantages | Cost / risk | Evidence | Blocks Phase 1B? |
| - | -------- | ----------- | ------------ | ---------- | ----------- | -------- | ---------------- |
| D1 | Identifier namespace | Owner-approved `saw_` namespace: `saw_<type>_<id12>`, `saw_cmt_<type><id12>_<uid8>`, `saw_lk_<type><id12>`; schema version carried by payload `schemaVersion` | (A) `qapp-core` hashed `buildIdentifier`; (C) fully random opaque ids | readable/greppable, prefix-searchable, ≤32 bytes, no salt coupling, deep-link resolvable without catalog | no cryptographic collision resistance (mitigated by 62-bit ids); new convention (not ecosystem-shared) | contracts §2; `Service`/`MAX_IDENTIFIER_LENGTH`; reference app's `ivm_*` prefixes | **yes** (identifiers are in the first published resource) |
| D2 | Taxonomy model | Hybrid: app categories + tags in payload/catalog; optional Core mirror | (A) Core enum only; (B) free-form only | works around 5-tag/20-char/240-char limits; cross-type pages; autocomplete | app owns normalization/migration; optional Core mirror adds publish complexity | contracts §5.8; `Category.java`; `ArbitraryDataTransactionMetadata.java`; q-tube `description` workaround | **yes** |
| D3 | Editor | TipTap; heavy owner editor lazy-loaded and outside the visitor startup path | Quill/react-quill-new + sanitized HTML; Lexical | hub precedent, preset coverage, structured output | TipTap bundle must be lazy; build/maintain the editor surface | Hub `package.json`; q-tube/Subwire/Quitter quill usage; contracts §7 | **no** for the shell; **yes** before any publishing feature |
| D4 | Stored rich-text / rendering model | Canonical `tiptap-json-v1` + `bodyText`; one allowlisting renderer + DOMPurify strict allowlist + URL-scheme policy | store sanitized HTML directly | structured storage, single sanitized render choke point, easier migration | build/maintain a renderer; sanitizer config must be tested with malicious fixtures | Hub `configureDomPurify.ts`; standard §6/§14; contracts §7 | **no** for the shell; **yes** before rendering stored content |
| D5 | Q-Mail fallback | Keep draft + explain unavailability + copy-message-to-clipboard | silent `SEND_CHAT_MESSAGE`; plain error | honest, no data loss, no wrong transport | contact is not delivered in-app when Q-Mail is unavailable | contracts/§8; q-mail 3.2.1 source | **no** (contact is a later route) |
| D6 | UI dependency strategy | No MUI: CSS tokens + in-repo components + SVG icons | MUI 7 + custom theme | measured ≈+39–110 kB gzip saved on MUI alone, plus design control | must build/test focus trap, tooltips, tabs, toasts; a11y is our responsibility | performance comparison §2–§4 | **yes** (shapes the shell) |
| D7 | `qapp-core` usage | In-repo `src/qortal/` layer (no root import) | `qapp-core` `GlobalProvider` (≈596 kB gzip baseline) | small first screen; full control of auth/identity; no video.js | re-implement bridge/auth/queue/caches; must track Core/Hub revisions | performance comparison §3; `qapp-core` `package.json`/`dist/index.mjs` | **yes** (shapes the scaffold) |
| D8 | Catalog service | `DOCUMENT` partitioned + manifest | `LIST`; `JSON` | no 25 KB cap; explicit `schemaVersion`; consistent envelope | new convention; self-imposed size ceiling is an inference | `Service.java` (JSON 25 KB, LIST/DOCUMENT uncapped); performance comparison §7 | **no** for the shell; before Blog/Video/Gallery listings |
| D9 | Like-activeness wire representation | **DEFERRED** — identity rule decided; proposed metadata tag fast path + payload fallback is a candidate only | payload fetch only | avoids per-like body fetches for counts **if verified** | **unverified at runtime**; needs one controlled publication to select the wire format | contracts §5.6; search metadata fields | **no** for the shell; before engagement |

## 15. Unresolved unknowns

- **DEFERRED (D9).** The like active/inactive/tombstone wire representation;
  metadata-tag engagement-state overwrite behaviour on republish must be proven
  with one controlled owner publication before the wire format is chosen.
- **FUTURE / NOT VERIFIED.** The exact Q-Tube publication/discovery/identifier
  contract for the future video-interoperability extension point (§5A). Do not
  implement or guess it now.
- **NOT VERIFIED.** Clipboard availability inside the iframe under the
  production and proxy CSP/permissions policy.
- **NOT VERIFIED.** `COMMENT` service behaviour with a base64 JSON envelope.
- **NOT VERIFIED.** Hub behaviour when publishing under a non-primary owned
  name.
- **NOT VERIFIED.** Real host/dev-proxy runtime timing, request counts and
  paint metrics; no browser performance numbers were fabricated.
- **RESOLVED (owner, 2026-09-11).** Delegated moderators: no delegated
  moderators for alpha; moderation authority is the publishing-name owner, with
  the design kept extensible for later delegation.
- **RESOLVED (owner, 2026-09-11).** Shadow Archives will publish its own video
  media to QDN and preserve a future Q-Tube participation capability; the exact
  Q-Tube contract remains FUTURE / NOT VERIFIED.
- **UNKNOWN.** The exact brand font/asset set; palette values are provisional.

## 16. Adversarial self-audit

Performed before handoff. Findings and disposition:

| ID | Finding | Class | Disposition |
| -- | ------- | ----- | ----------- |
| A1 | Legacy `HashRouter` could be inherited from the reference app | HIGH | **Fixed in design:** §1.2 explicitly rejects `HashRouter` and mandates `createBrowserRouter` + `_qdnBase`; reference app's router is documented as non-authoritative |
| A2 | Startup could accidentally include the owner editor / video.js / all comment bodies | BLOCKER | **Fixed in design:** §2/§3 ban `qapp-core` root import and MUI from the shell; editor and player are lazy chunks; policies stated in the appshell spec and Phase 1B plan |
| A3 | N+1 engagement discovery | BLOCKER | **Fixed in design:** contracts §8 + architecture §5: catalog snapshot on listings, one search per target on detail, bounded queue, cached, no per-card queries |
| A4 | Catalog treated as authority | HIGH | **Fixed:** contracts §6/§7 state the catalog is derived/rebuildable and never proves ownership; entity resources remain authoritative; recovery path defined |
| A5 | Payload `author` fields treated as identity | HIGH | **Fixed:** contracts §4/§6 and §11.3 forbid authority from payload fields; moderation/authority use resource `name` + ownership |
| A6 | Hardcoded owner or hardcoded external app targets | HIGH | **Fixed:** §11 derives owner at runtime from `_qdnName` + ownership; §9 puts app names in `saw_cfg` with verified defaults, explicitly "not timeless constants" |
| A7 | Invented Qortal bridge actions | HIGH | **Fixed:** §3/§14 restrict the action set to actions verified in `q-apps.js`/Hub; the index feature is marked as having no bridge action |
| A8 | Qortium behavior imported | HIGH | **Verified absent:** no Qortium trust/API reference anywhere in this package; rationale text mirrors the owner's non-import clause only |
| A9 | Q-Mail convention treated as a Core contract | MEDIUM | **Fixed:** §8.1 labels it a community-app convention at a pinned revision and requires re-verification before implementation |
| A10 | Unsafe rich-text assumptions | HIGH | **Fixed:** §7 + D3/D4 require structured storage, one allowlisting renderer, DOMPurify, URL-scheme policy and malicious fixtures in tests |
| A11 | Raw like-resource counting | HIGH | **Fixed:** contracts §5.6/§8: raw count is never the active count; state interpreted; unclassifiable ⇒ `>= N`; the reference app's capped-`page.length` defect is called out |
| A12 | Multi-name likes accidentally deduplicated by account | BLOCKER | **Fixed:** like identity is scoped by publishing **name**; identifier contains no actor; contracts §5.6 and §8.2 explicitly forbid address-level dedupe |
| A13 | Moderation described as network deletion | HIGH | **Fixed:** contracts §5.7 and architecture §5 use "Hidden in Shadow Archives" and state the on-chain record is untouched |
| A14 | Search requiring body fetches on every query | HIGH | **Fixed:** contracts §7.4 defines a local compiled index; explicit ban on QDN requests per keystroke |
| A15 | Unverified `qortal://` app targets hardcoded | HIGH | **Fixed:** §9 verifies the three names against a live read-only node on 2026-09-11 and moves them into owner-editable config |
| A16 | Mobile layout treated as squeezed desktop | MEDIUM | **Fixed:** appshell spec §2/§7: mobile is a reflow with snap scrollers and stacked sections |
| A17 | Auto-scroll ignoring reduced motion / accessibility | MEDIUM | **Fixed:** appshell spec §5: pause on hover/focus/interaction/hidden, disabled under `prefers-reduced-motion`, DOM order preserved, content reachable without motion |
| A18 | Performance claims without measurement | MEDIUM | **Fixed:** all numbers are labelled MEASURED/SOURCE-OBSERVED/INFERRED/NOT VERIFIED; no millisecond budgets invented |
| A19 | `qapp-core`'s Dexie DB is literally named `MyAppDB` (shared origin store) | MEDIUM | **Noted (design constraint):** if `qapp-core` is used, its persistent store is shared across apps on the same node origin. The recommended in-repo cache layer must use an app-namespaced IndexedDB database and version its stores. |
| A20 | `JSON` service mistaken as usable for catalogs/likes | MEDIUM | **Fixed:** contracts §3 rejects `JSON` for catalogs/likes because the app publishes base64 envelopes and `JSON` is capped at 25 KB and validated as JSON |
| A21 | App taxonomy assumed to be searchable via Core metadata tags | HIGH | **Fixed:** §6 records that Core search cannot filter metadata `tags`; taxonomy search is served from the catalog/search index |

No confirmed in-scope BLOCKER/HIGH finding remains unresolved.

## 17. Validation performed for this package

- Canonical workspace validation: `tools/validate-workspace.sh` (see the
  handoff summary for the exact result).
- Relative Markdown links and anchors: verified for this file and its siblings.
- Whitespace / conflict-marker checks: `git diff --check` and a
  conflict-marker scan.
- Target application directory: verified still empty and not a Git repository.
- No external writes: no commit, push, tag, PR, issue, publication, deployment
  or transaction was performed. Upstream repositories were not modified.
- Source claims: checked against the pinned revisions listed in the performance
  comparison §1; live claims checked against `https://api.qortal.org` on
  2026-09-11.
