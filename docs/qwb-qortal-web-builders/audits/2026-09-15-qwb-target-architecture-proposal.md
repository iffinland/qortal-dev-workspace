# QWB target architecture proposal — qwb-qortal-web-builders/architecture-audit-20260915

Executing agent (registered role of the agent that actually produced this work): `DeepSeek`
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence: the design analysis was produced by the DeepSeek model through the local
Codex CLI profile (the profile is not the executor).
Report type: architecture proposal (audit output; **no implementation performed or authorized**)

**STATUS: PROPOSAL ONLY. Do not start implementation until the owner has reviewed this document.**
No application was scaffolded, no repository was initialized, no content was published, no QDN
write was executed, no skill was created.

Companion evidence: `2026-09-15-qwb-static-site-forensics.md`,
`2026-09-15-qwb-visual-preservation-map.md`,
`2026-09-15-qwb-iffi-vaba-mees-owner-pattern-audit.md`,
`2026-09-15-qwb-qortal-platform-compatibility-and-write-contract.md`.

---

## 4. Stack decision

### 4.1 What the site actually is

Evidence from the audit: 6 static pages, one bespoke ~1,300-line theme CSS layer over Bootstrap
5.2.2, 12 distinct visual components, ~8 editable content kinds with single-digit-to-low-double-digit
item counts (3 steps, 8 works, 2 price tiers, a handful of articles), one owner-editor, no
multi-user, no real-time collaboration, no routing complexity beyond a handful of views, and an
explicit requirement to *descend visually* from the existing design.

### 4.2 Options compared

| Criterion | A. Vite + TypeScript + vanilla DOM components | B. React + Vite + TypeScript |
| --- | --- | --- |
| Visual preservation | **Best.** The existing HTML/CSS maps almost 1:1 onto TypeScript render functions with the same class names; the golden-master CSS can be reused nearly verbatim, so "did the design survive" is verifiable by screenshot diff | Requires porting all markup to JSX; every port is a chance to drift; the team is also tempted to re-style |
| Existing HTML/CSS reuse | ~90 % of the theme CSS reused unchanged; Bootstrap 5.2.2 CSS kept as substrate | Same CSS can be kept, but the markup must be rewritten; Bootstrap's JS components must be replaced by React state |
| Inline editing complexity | Low. Owner controls are DOM insertions into known containers; form state is a plain object per modal; ~300–500 LOC of shared UI plumbing (modal, toast, confirm, field rendering) covers everything | Low too, but the same plumbing is React components; slightly less code for lists/modals, more code for markup fidelity |
| Modal / state management | Hand-rolled but small and auditable (one modal manager, one store) | Idiomatic `useState`/context |
| Content lists, add/edit/delete | Simple array render + sort by `order`; re-render one section after a write | Same, tidier with keys/lists |
| Future growth | Comfortable up to roughly a dozen views and a few hundred entities | Safer if the app becomes a large multi-view SPA with complex nested editors |
| Testability | Plain functions + JSDOM: easy unit tests for reducers, validators, identifier generation, write-result classification; Playwright for flows | Equivalent with testing-library |
| Bundle / startup cost | No framework runtime: ~15–25 KB gzip of app code + Bootstrap CSS/JS + small utilities. The QDN render path is an iframe on a possibly slow node, so start-up cost is a real product concern | React 19 + react-dom ≈ 45–55 KB gzip before app code; qapp-core would add MUI + Emotion (hundreds of KB) |
| `qapp-core` reuse | Not usable — it is a React + MUI library (`react`, `@emotion/*`, `@mui/*`, zustand, dexie, video.js). Its genuinely useful primitives for this app (a request queue, a sanitizer, small caches) are each <150 LOC to reimplement | Would let us import `RequestQueueWithPromise`, `GlobalProvider`, `ListLoader`, `IndexManager`, `ImagePicker`, `MultiPublishDialog`, `VirtualizedList` — but drags a full MUI design system into a site whose identity is bespoke Bootstrap |
| Maintainability | One small codebase, few dependencies, nothing to upgrade but Vite/TS/Bootstrap | Framework churn + MUI coupling, but familiar to React developers |

### 4.3 Recommendation: **Option A — Vite + TypeScript + vanilla DOM component modules**

Reason: this is a *presentation-preserving* project with *bounded* interactivity. The decisive
factors are (1) the visual-fidelity requirement is best served by keeping the existing HTML/CSS
structure, (2) the content model is small and single-owner, so the framework's state management
advantage is marginal, and (3) start-up cost inside a QDN iframe is a real constraint, while
`qapp-core` — the one strong React argument — would import an MUI design system that actively
conflicts with the preserved visual identity.

Non-negotiable structure so that A does not degrade into spaghetti:

```text
src/
  main.ts                 boot: read _qdn* context, detect bridge, load content, render, wire owner mode
  qortal/
    context.ts            typed read of _qdn* + bridge presence + context classification
    bridge.ts             THE single qortalRequest wrapper (typed, per-action result classification)
    identity.ts           current account + names -> owner decision (see §5)
    qdn.ts                resource identity, fetch/search with normalization + post-filter
    write.ts              publish/verify pipeline, in-flight guards, truthful result classification
    media.ts              image downscale/encode + media publish
  content/
    schema.ts             typed entity schemas + validators + revision/state fields
    repository.ts         load all content kinds (read-time reconciliation, partiality reporting)
    seed.ts               mock/seed content used before the owner edits anything
  views/                  one module per section (hero, highlights, steps, works, pricing, contact, footer)
    <section>.ts          render(data) -> HTML string + mount(el, ctx) -> wires events & owner controls
  ui/
    modal.ts              modal manager (focus trap, Escape, dirty-state guard, aria wiring)
    forms.ts              field renderer driven by a small field schema
    toast.ts, confirm.ts  feedback + destructive confirmation
  owner/
    controls.ts           per-section/per-item owner affordances
    flows.ts              edit/create/delete/reorder/publish flows
  styles/
    tokens.css theme.css components.css owner.css    (theme derived from the golden master)
```

A single immutable store per content kind (`{ items, status: 'ready'|'partial'|'error', diagnostics }`),
explicit `render(section)` functions, and no framework — with pure functions for validators,
identifier generation and write-result classification so they are unit-testable.

**Reconsideration triggers (decide again if any becomes true):** the app grows past ~12 distinct
views; the owner asks for a rich visual/drag-drop editor with live preview, or multi-user
collaboration; or reuse of `qapp-core` components becomes an explicit product requirement. Any of
those makes Option B the better trade.

## 5. Owner recognition architecture

Requirements: automatic, no in-app login, no hardcoded owner address, authority derived from the
app's own publishing identity + current name ownership, fails closed, re-verifies, never persists
`owner=true`, and visitors never see owner controls.

### 5.1 Model

```text
injected context            host-mediated read          derivation                 decision
_qdnService, _qdnName   ->  GET_USER_ACCOUNT       ->  normalise + compare   ->  owner | visitor
(and _qdnContext)           GET_ACCOUNT_NAMES           membership test
```

1. **App identity (authoritative, free, no permission needed):** read `_qdnService` and `_qdnName`
   from the injected globals (Core `HTMLParser.java:72`). `_qdnName` is the registered name that
   published this resource — the only correct basis for "which identity owns this app".
   `_qdnContext` tells us whether owner mode is even possible (`gateway` is read-only, `proxy` has
   an empty `_qdnName`).
2. **Current account (host-mediated, user-approved once):** `{ action: 'GET_USER_ACCOUNT' }`.
   The Hub opens a permission dialog the first time and remembers the answer per app name (with an
   "always authenticate" checkbox), plus a session permission afterwards. Returns
   `{ address, publicKey }`. A rejection or a gateway `{error}` response yields no address.
3. **Ownership resolution (public read):** `{ action: 'GET_ACCOUNT_NAMES', address }`
   — the bridge maps this to `GET /names/address/{address}` and **ignores** `limit`/`offset`/
   `reverse`. Treat the result as the complete current name list for that address (entries may be
   strings or `{ name, … }` objects; normalise both).
4. **Decision:**
   `isOwner = _qdnName !== '' && names.map(normalize).includes(normalize(_qdnName))`
   — case-insensitive, trimmed membership; never `names[0]`; never a literal owner name in source.
5. **Fail closed:** no bridge, gateway context, empty `_qdnName`, permission rejection, malformed
   response, non-array names, timeout, or any thrown error ⇒ **visitor mode**, silently (no error
   toast for visitors; log a single diagnostic).
6. **No persistence of authority:** owner mode lives in memory for the page session only. Nothing
   about ownership is written to `localStorage`/IndexedDB. A reload re-derives it. (Optionally cache
   only the *permission was granted* fact is NOT stored — the host already owns that.)
7. **Re-verification:** because the host sends **no account-changed event**, re-run steps 2–4
   (a) before every write flow starts, (b) when the document becomes visible again after being
   hidden, and (c) on an explicit owner-bar "re-check" action. If the re-check fails, immediately
   drop owner controls without destroying an open draft — show "owner mode ended: account changed"
   and keep the draft in the modal for the user to copy.
8. **Defence in depth (not the boundary):** every write path re-checks `isOwner` immediately before
   calling the bridge, and every read path discards entities whose publishing `name` is not
   `_qdnName` (the reference app's best pattern). The real security boundary remains the Qortal
   ledger: only the owner of the name can publish under it, and the host gates signing.

### 5.2 Exact calls to implement (current revisions)

| Purpose | Call | Notes |
| --- | --- | --- |
| App identity | `_qdnService`, `_qdnName`, `_qdnContext` (+ `_qdnTheme`, `_qdnLang`) | injected globals, no bridge call |
| Bridge presence | `typeof window.qortalRequest === 'function'` (own window only) | do not probe `window.parent`/`top` |
| Current account | `GET_USER_ACCOUNT` | host-mediated, 60-minute timeout budget, permission dialog possible |
| Owned names | `GET_ACCOUNT_NAMES { address }` | public read; parameters ignored by the bridge |
| (Optional hardening) name owner | `GET_NAME_DATA { name: _qdnName }` → `.owner` | redundant if `_qdnName ∈ names`; use only to display diagnostics |
| Host theme/language | `THEME_CHANGED`, `LANGUAGE_CHANGED` messages | optional; last value wins, never let an older injected value overwrite a newer event |

`GET_NAME_DATA` is deliberately *not* required: comparing the account's own current name list
against `_qdnName` is already current-ownership evidence, and adding a second source would create
two authorities for the same fact.

### 5.3 Explicit non-goals / rejected shapes

- No hardcoded owner name or address in source (rejected from the reference app).
- No `owner=true` flag, no "owner token", no client-side "logged in as" screen.
- No dev-proxy owner mode: under Hub Developer Mode `_qdnName` is empty by construction, so owner
  mode is **unavailable in local dev** and must be validated in a published-app context. Do not
  work around this with a hardcoded name; optionally allow a **development-only** override that is
  compiled out of production builds and clearly labelled if the owner wants to iterate on the
  editing UI locally (owner decision D6).

## 6. Content architecture

Principles: entity = authority; singletons stay single; one bad write damages one entity; no
general CMS; every entity carries schema/revision/state; media referenced explicitly and resolved
absolutely at render time.

### 6.1 Editable content kinds

| # | Kind | QDN service | Identifier | Singleton? | Editable fields |
| --- | --- | --- | --- | --- | --- |
| 1 | `site` | `JSON` (≤25 KB) | `qwb_site_v1` (fixed) | yes | brand name/tagline, nav labels, hero (heading, subtitle, optional background image ref, optional CTA label/target), highlight-card text, contact block (Q-mail link, group link/ID, note), footer credit lines, section order/visibility |
| 2 | `highlight` | `JSON` | `qwb_hl_<slug>-<ts36>-<rand>` | no | title, body (small rich text), bullet lines, primary/secondary variant (`plain`/`overlay`), CTA label+target, `order` |
| 3 | `service` | `JSON` | `qwb_svc_<slug>-<ts36>-<rand>` | no | title, summary, bullet lines, icon (emoji or bundled icon name), image ref, CTA, `order` |
| 4 | `step` | `JSON` | `qwb_step_<slug>-<ts36>-<rand>` | no | title, description, illustration ref, `order` |
| 5 | `work` | `JSON` | `qwb_work_<slug>-<ts36>-<rand>` | no | title, build kind label, summary, external/QDN links[], cover ref, featured flag, `order` |
| 6 | `price` | `JSON` | `qwb_price_<slug>-<ts36>-<rand>` | no | title, emoji+line items[], CTA label/target, `order` |
| 7 | `article` (only if the 4 prose pages survive) | `DOCUMENT` | `qwb_post_<slug>-<ts36>-<rand>` | no | title, slug, summary, body HTML (sanitised), hero image ref, tags[], `state`, timestamps |
| 8 | media | `THUMBNAIL` (≤500 KB) / `IMAGE` (≤10 MB) | same identifier as the owning entity for its primary image; `<entity id>_<n>` for extras | — | binary; the entity stores an explicit reference, never a path |

Everything is published under the app's publishing name (`_qdnName`). Identifier policy: lowercase
`[a-z0-9-]`, ≤60 characters, kind-prefixed, timestamp-suffixed, **never reused** (an identifier
is the entity's permanent identity; Core has no rename and re-publishing under a new identifier
orphans the old bytes).

### 6.2 Entity schema (common envelope)

```jsonc
{
  "schema": 1,                 // payload-format version; reject unknown versions with a diagnostic
  "id": "qwb_work_kaubamaja-2f19x7-k3",   // = the QDN identifier, duplicated inside the payload
  "kind": "work",
  "rev": 3,                    // monotonically increasing per entity; used to verify a write
  "state": "active",           // "active" | "deleted"
  "createdAt": 1757900000000,
  "updatedAt": 1757950000000,
  "deletedAt": null,
  "order": 20,                 // sparse ordering (10, 20, 30 …); reorder = republish one entity
  "title": "…",
  "payload": { /* kind-specific fields */ }
}
```

`rev` is the write-verification handle: after publishing, re-read the entity and compare `rev`
(and `updatedAt`) with what was sent; only then is the change presented as applied. Unknown
`schema` values are shown as "update the app to read this item", never silently dropped or rendered.

### 6.3 Media references

```jsonc
"image": { "service": "THUMBNAIL", "name": "<publishing name>", "identifier": "<entity id>",
           "filename": "cover.jpg", "width": 1200, "height": 675 }
```

- The reference is explicit; the display URL is derived at render time as an **absolute**
  `/arbitrary/<service>/<name>/<identifier>` path. Never persist or render a relative media path
  (it resolves under the frame's `<base href>` and the node returns the app shell HTML).
- Publishing order is always **media → entity**: a card must never reference an image that does
  not exist yet. For updates, publish a changed image before the entity that points at it.
- Bundle assets (logo, favicons, theme CSS, self-hosted fonts, static illustrations) stay inside
  the published app archive; only *content* images become QDN resources. This is owner decision D3.

### 6.4 Seed content

The new app ships with clean mock/seed content (typed, in `src/content/seed.ts`) that reproduces the
golden master's structure with rewritten copy and placeholder-but-valid media. The owner then
replaces it through the inline editor. There is **no import of the old content** (§12).

## 7. Index / discovery decision

**Expected volume (single publisher, bounded):** ≤10 services, ≤6 steps, ≤4 price tiers, ≤40 works,
≤30 articles — i.e. roughly 40–90 entities total, 1–2 search pages per kind at a page size of 50.

**Decision: no derived index initially. Use bounded direct discovery.**

```text
per kind:
  SEARCH_QDN_RESOURCES {
    service:        <kind service>,
    identifier:     "qwb_work_",       // kind prefix
    prefix:         true,
    mode:           "ALL",
    includeStatus:  true,
    includeMetadata:true,
    excludeBlocked: true,
    limit:          50,
    offset:         0,                 // paginate while page is full, up to a hard budget
    reverse:        true              // newest first for stable paging
  }
  -> post-filter: exact name === _qdnName AND identifier startsWith prefix AND service matches
  -> fetch payloads with bounded concurrency (queue, e.g. 4–6 in flight)
  -> sort in the app: order ASC, createdAt ASC, identifier ASC (fully deterministic)
  -> report status: ready | partial (some payloads unavailable) | error, with diagnostics
```

Rules that make this acceptable: results are one publisher's resources (not a global scan), the
budget is bounded (explicit page cap), unavailable payloads are reported as unavailable rather than
as "no content", and `query` is never used for body-text search (it only covers
name/identifier/title/description).

**Add a derived index only when a trigger fires:** (a) any kind consistently exceeds two search
pages, (b) a listing needs a sort/filter on a field that is not in the resource metadata and is not
cheap to fetch, or (c) measured listing latency exceeds the agreed budget. If added, it must follow
the verified `qdn-derived-index-coherence` contract: entity = authority, index = derived
acceleration, bounded read-time reconciliation, fallback discovery when the index is unreadable,
never rebuild an unreadable index from a partial view, and never re-add a tombstoned entity as
active.

## 8. Update / delete strategy

The full platform contract is in the companion report §6–§8. Design consequences:

### 8.1 Update

- Publish the same `(name, service, identifier)`; Core keeps the newest transaction, preserves
  `created`, and sets `updated`. There is no compare-and-swap, so the app must serialise writes per
  entity: one in-flight write per identifier, and a second edit disabled until the first resolves.
- Every write increments `rev` and sets `updatedAt` in the payload. Verification = re-read the
  entity + compare `rev`. Only then is the change shown as applied.
- Write lifecycle shown to the owner:
  `draft → submitting → accepted (submitted, unverified) → verified` with explicit failure states
  `rejected` (user declined the host dialog), `failed`, `ambiguous` (timeout), `gateway-blocked`.
- Media-first ordering: image (if changed) → entity → (optional index).
- No auto-retry on any write. A retry is always an explicit, clearly labelled user action, because
  publishing is not idempotent from the user's perspective (a second submit can produce a second
  transaction).

### 8.2 Delete — logical tombstones (recommended)

Because there is **no app-accessible QDN delete** in current Qortal (§7 of the platform report):

1. `Delete` republishes the entity with `state: "deleted"`, `deletedAt`, a `rev` increment and a
   minimal retained payload (keep `id`, `kind`, timestamps, `order` — drop heavy fields).
2. Every read path filters `state !== "active"`: listing, detail lookup, search, and any index
   rebuild. A tombstone is never resurrected as active content.
3. Media for a tombstoned entity may also be tombstoned (publish an empty/placeholder THUMBNAIL or
   simply stop referencing it). Deleting media is optional and never required for correctness.
4. The confirmation dialog must tell the truth: the item disappears from the site; the previously
   published bytes cannot be erased from the QDN. Suggested wording is part of §9.
5. Alternative considered and rejected as the *only* mechanism: "hide" (a boolean flag) — it keeps
   the item listable forever and forces every read path to filter a permanent graveyard; a tombstone
   is the same cost with an honest semantic.
6. Physical purge (admin API-key, node-local) is **out of scope** and must not be presented as an
   app feature.

### 8.3 Ambiguous writes

| Situation | UX |
| --- | --- |
| Host dialog declined | "Update cancelled — you declined the Qortal permission prompt." Draft kept. |
| Bridge throws before signing | "Update failed before signing." Draft kept, retry offered. |
| Timeout (up to 60 min budget for publish) | "Still in flight / could not confirm." Show `[ Check status ]` (re-read + `rev` compare). Never auto-retry. |
| Gateway `{error}` response | "Interactive editing isn't available in gateway view — open this site in Qortal Hub." Owner controls may be hidden entirely when `_qdnContext === 'gateway'`. |
| Publish accepted, resource not yet served | "Submitted. Not yet visible on this node." After verification succeeds, refresh the entity in place. |

## 9. Inline editing UX design

### 9.1 Placement of owner controls (concrete, for the audited page)

```text
Navbar                      [ owner indicator •  re-check ]                         (only when owner)
Hero (section_1)            [ ✎ Edit hero ]
Featured pair               [ ✎ Edit ] [ 🗑 ]  per card        + Add highlight
Browse Topics
  ├ Website Building Steps  [ ✎ Edit ] [ 🗑 ]  per step card   + Add step    [ ↑ ↓ ]
  ├ Completed Works         [ ✎ Edit ] [ 🗑 ]  per work card   + Add project [ ↑ ↓ ]
  └ Template Gallery        [ ✎ Edit ]  (single block)         + Add bullet line
Pricing (section_3)         [ ✎ Edit ] [ 🗑 ]  per tier        + Add tier
Contact (section_5)         [ ✎ Edit contact ]
Footer                      [ ✎ Edit footer ]
Article page (if kept)      [ ✎ Edit ] [ 🗑 ]  in the header row; [+ New article] on the index
Media inside a form         [ Choose image ] [ Replace ] [ Remove ]
```

Rules: controls appear only in owner mode; they are **always visible** (not hover-gated) so touch
devices work; destructive actions are visually distinct; every control has an `aria-label` naming
the entity ("Edit hero", "Delete work: Kaubamaja"); the main content stays byte-identical for
visitors — no placeholder editing widgets leak into visitor markup.

### 9.2 Modal types

1. **Entity form modal** (the workhorse) — schema-driven fields (text, textarea, rich-lite text,
   emoji/icon picker, list-of-strings, repeatable rows, link rows, select), inline validation,
   save/cancel, error region, `aria-modal` + `aria-labelledby`, focus trap, Escape = cancel.
2. **Media picker modal** — file input + drag-drop, client-side downscale preview, target service
   shown (`THUMBNAIL` ≤500 KB vs `IMAGE` ≤10 MB), size/format validation before publishing.
3. **Delete confirmation modal** — entity name in the title, honest QDN wording, destructive button
   requires an explicit click (no default focus on the destructive action), and for works with
   external links a reminder listing what will disappear.
4. **Publish status modal / tray** — staged progress (preparing → waiting for host approval →
   submitting → confirming → done) with a per-write result, and a "Check status" action for
   ambiguous outcomes. This is where truthfulness lives: never show a green check before `rev`
   verification succeeds.
5. **Reorder affordance** — inline ↑/↓ buttons (keeps it operable on touch/keyboard); optional
   drag-and-drop later. A reorder changes `order` on the moved entity (and possibly its neighbour)
   and publishes only those.

### 9.3 Flows

- **Create:** `+ Add …` → entity form modal (empty, seed defaults) → client validation → media
  publish if an image was chosen → entity publish with a fresh identifier → verify by re-read →
  insert into the section in `order` position → toast with the truthful outcome.
- **Edit:** `✎ Edit` → form pre-filled from the loaded entity (including its `rev`) → validation →
  media first if changed → entity publish with `rev + 1` → verify → replace in place.
- **Delete:** `🗑` → confirmation modal → tombstone publish (`state: 'deleted'`) → verify → remove
  from the section → toast; the tombstone stays filtered on every future load.
- **Dirty state:** closing a dirty modal (Escape, backdrop, cancel, or a re-check that ends owner
  mode) asks "Discard changes?"; the draft survives an ambiguous write.
- **In-flight guard:** while a write for an entity is in flight, its controls are disabled and the
  status tray shows the stage; a second submit is impossible, and no write is ever retried
  automatically.

### 9.4 Quick actions and the owner bar

A single compact owner bar (page top edge or a floating pill) carries global, non-cascading
information: owner mode status + name, in-flight/pending write count, `Reload content`,
`Check last write`, and `Re-check owner mode`. It is deliberately *not* a CMS dashboard — the
sections remain the primary editing surface.

### 9.5 Mobile owner UX

Owner editing on a phone is a real scenario (the site runs inside the mobile Hub), so: modals become
full-height sheets with a sticky action bar; touch targets ≥44 px; the owner bar collapses to a
single badge that opens a sheet; destructive confirmations require an explicit tap on a distinctly
coloured button; media picking uses the native file/photo picker; reorder uses ↑/↓ rather than drag.

## 10. Development directory

**Reserved path: `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`**

Rationale: it is a sibling of `-PUBLISHED-versioon`, so the read-only golden master stays visible
and untouched while the new project keeps the same repository name as the GitHub repo
(`QWB-Qortal-Web-Builders`), and it does not collide with the existing out-of-scope siblings
(`QWB-Web-Builders-kola/`, `QWB-favicon/`, `portal-HTML-templates/`, the two loose template HTML
files). The directory is created empty by this audit purely to reserve the name; **no application
scaffold, no `git init`, no `package.json` was created.**

Layout after implementation begins:

```text
/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/
├── -PUBLISHED-versioon/          READ-ONLY golden master (never a Git working tree)
└── qortal-web-builders/          new development repository (Git → GitHub)
```

Explicit rule for the implementation phase: the golden master is **never** added as a Git remote,
submodule, worktree or "reference" directory inside the new repo. Selected assets are *copied* into
the new repo with written source mapping (§11).

## 11. GitHub bootstrap plan

**Verified remote (2026-09-15, `gh repo view`):**

| Property | Value |
| --- | --- |
| Owner / account | `iffinland` (the account authenticated for `gh` and the Git identity in use) |
| Repository | `QWB-Qortal-Web-Builders` |
| URL | `https://github.com/iffinland/QWB-Qortal-Web-Builders` |
| SSH | `git@github.com:iffinland/QWB-Qortal-Web-Builders.git` |
| Visibility | PUBLIC |
| State | **empty** — `isEmpty: true`, no commits, no default branch |
| Created | 2026-09-15T12:24:30Z |

Bootstrap sequence (only after the owner approves this architecture and explicitly authorizes
commits/pushes — no push has been performed by this audit):

```text
1. cd /home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders
   git init -b main
   git remote add origin git@github.com:iffinland/QWB-Qortal-Web-Builders.git
2. Commit 1 — scaffold only: Vite + TypeScript, eslint/prettier, vitest (+ JSDOM),
   .gitignore, README (project identity + reference pins), LICENSE/attribution decision,
   docs/attribution.md (asset source mapping). No site content yet.
3. Commit 2 — visual baseline: theme CSS derived from the golden master + the public page
   structure reproduced with SEED content. No owner mode, no QDN writes. Screenshot-compared
   against the golden master. This is the "descent" checkpoint.
4. Branch per phase: agent/qwb-<phase> (feature branches, small, coherent verticals), merged to
   main only after the phase acceptance evidence exists.
5. Push order: application branch first, verify the remote SHA, then handoff artifacts
   (orchestration task record) with that exact SHA.
```

Asset handling rules:

- **Never** push `-PUBLISHED-versioon` wholesale, and never add it as a subtree.
- During Phase 1, copy only the assets actually used, into `src/assets/` and `public/`, and record
  each one in `docs/attribution.md` with: source path inside the golden master, its SHA-256 (already
  produced in this audit's manifest), the file's origin/licence (Bootstrap 5.2.2 MIT, Bootstrap
  Icons MIT, unDraw illustrations, template-provided stock photos = unknown), and a "replaced or
  retained" decision.
- Vendored third-party CSS/fonts keep their upstream licence notices; MIT licence texts for
  Bootstrap/Bootstrap Icons are added to `docs/third-party-licences.md`.
- Unknown-provenance stock photos are flagged for replacement (owner decision D4).

## 12. No migration script — confirmed

**No static-content migration, import or scraping script is recommended, and none was written.**

Reasons, from the audit evidence: the brand and much of the copy are being rewritten; the old
content is entangled in markup with no data layer, so any extractor would encode today's mistakes
(the capitalised body-text artefact, "Builded To HTML Template" copy, dead external links, stale
prices); the owner will edit content through the new inline editor; and the engineering budget is
better spent on the durable owner-editing architecture. The old site's role is limited to visual
structure, asset reuse and evidence of the previous identity. Seed content is typed mock data
(§6.4); a human may copy individual sentences by hand where useful.

## 13. Implementation phase plan

Each phase ends with the owner-visible artifact named in "exit" — no phase claims runtime success
without the corresponding evidence layer.

**Phase 0 — repository, tooling, references, visual baseline prep**
- create the development repo at §10, `git init -b main`, tooling (Vite + TS + eslint + vitest),
  `.gitignore`, README with the pinned references below, `docs/attribution.md`.
- re-run the freshness gate and pin: Core `108bf191`, Hub `12a573b2`, qapp-core `0f9d6ac5`,
  qapp-templates `143cc7b`, reference app `64f55bf7`.
- copy the preserved theme assets with source mapping.
- exit: `npm run build`, `npm run lint`, `npm test` green on an empty scaffold; remote verified.

**Phase 1 — public visual site, seed content, no editing**
- reproduce the golden master's public pages in the chosen stack: token layer, gradient bands,
  rounded section, cards, tab strip, pricing, contact, footer, responsive behaviour **with a real
  viewport meta**; delete the obsolete techniques (jQuery, sticky/timeline code, malformed style
  blocks, capitalisation leak); self-host the intended webfonts (owner decision D2).
- render from `src/content/seed.ts` through typed section modules.
- exit: desktop + mobile screenshots compared against the golden-master screenshots; documented
  intentional differences; no owner controls, no bridge calls.

**Phase 2 — owner recognition + owner UI shell**
- implement `qortal/context.ts`, `qortal/bridge.ts`, `qortal/identity.ts` per §5 and the single
  `qortalRequest` wrapper with per-action result classification (including the gateway `{error}` and
  host-rejection paths).
- owner bar, owner-only control rendering, modal/confirm/toast plumbing, dirty-state guard.
- exit: unit tests for identity derivation (owner/visitor/gateway/no-bridge/rejection/malformed) and
  for the write-result classifier; **real published-app check that owner mode appears exactly for
  the publishing name's owner and never for a visitor** (this cannot be proven in dev proxy).

**Phase 3 — QDN-backed CRUD + media + truthful outcomes**
- `content/repository.ts` bounded discovery + reconciliation + partiality diagnostics; `schema.ts`
  validators; `write.ts` publish/verify pipeline with `rev` verification; `media.ts` downscale and
  publish; create/edit/delete(tombstone)/reorder for every editable kind; per-entity in-flight locks.
- exit: unit tests for schema validation, identifier generation, tombstone filtering, revision
  verification, ambiguous-write classification; a bounded live read-only validation of the search +
  fetch path against a node; **no write without explicit owner authorization**.

**Phase 4 — owner-runtime validation, visual regression, documentation**
- owner publishes real content in the real host (Hub) on a real account: create → verify → reload;
  edit → verify; reorder; delete → tombstone stays hidden after reload; visitor view shows no owner
  controls; failure paths (declined approval, gateway view, offline node) behave truthfully.
- visual regression pass against the Phase 1 baseline; contrast/accessibility/focus checks;
  documentation of the data model, identifier policy and recovery actions.
- exit: owner acceptance recorded, plus the capability-harvest decision (§14).

Deferred by default (explicitly not in Phases 0–4): a derived index, rich-text formatting beyond
sanitised basics, comment/engagement features, visitor accounts, i18n, offline caching, and any
admin dashboard.

## 14. Future skill harvest candidates (no skill was created or promoted in this audit)

| Candidate skill | Platform | Why it is reusable | Evidence needed before promotion |
| --- | --- | --- | --- |
| `qortal/registered-name-owner-mode` | `qortal` | Deriving owner mode from `_qdnName` + `GET_USER_ACCOUNT` + `GET_ACCOUNT_NAMES` with fail-closed semantics, gateway/dev-proxy caveats and re-verification rules is a general Q-App need | owner-runtime PASS in a real host (this app) + Core/Hub pins |
| `qortal/inline-owner-editing` | `qortal` | Owner-in-context controls, modal/form plumbing, dirty-state, in-flight guards, truthful write status | same, after Phase 4 |
| `qortal/qdn-content-crud` | `qortal` | Create/update/**logical delete** without any delete bridge action: revision verification, tombstone semantics, media-first ordering, ambiguous-write rules | same, plus a live read-back verification of a real tombstone |
| `qortal/qdn-app-asset-strategy` *(optional)* | `qortal` | Which assets belong in the published archive vs QDN-managed media, under the render CSP and `<base href>` rules | could also be folded into an existing skill |

Explicitly **not** proposed: a `static-site-to-managed-qapp` skill. The starting point being static
does not create reusable methodology here (no migration tooling is wanted, and the visual
preservation work is project-specific). If Phases 1–4 produce a genuinely reusable methodology
(e.g. "reproduce a static QDN site in a managed stack while preserving its identity"), it can be
reconsidered then with real evidence.

## 15. Decisions for the owner

Only decisions the audit cannot settle from source evidence are listed.

> **Later record (2026-09-16): the owner approved the D1–D9 package.** This section is kept
> unedited as the audit's evidence and its recommendations stand as the approved choices; the
> accepted, implemented state and the approved production identity
> (`WEBSITE / Qortal Web Builders / default`) are recorded in
> [`projects/qwb-qortal-web-builders.md`](../../../projects/qwb-qortal-web-builders.md) and in
> `implementations/2026-09-16-qwb-phase-4-checkpoint.md`.

**D1 — QDN service and URL strategy.** Publish the refreshed app as … 
- A: `WEBSITE` under the existing name `Qortal Web Builders`, single-entry build with hash routes
  for dynamic content. Keeps every existing `qortal://WEBSITE/Qortal%20Web%20Builders` link valid;
  no client-routing fallback needed because dynamic views live in the hash.
- B: `APP` under the same name with history routing (Core forwards unknown paths to `index.html`),
  giving cleaner URLs but a **new** address; the old `WEBSITE` resource stays published and would
  have to be updated separately or left stale.
- Recommendation: **A** (link continuity, least surprise, no migration of existing references).
  Consequence: dynamic detail views are addressed by hash (`…/index.html#/works/…`).

**D2 — Typography.** The site declares Montserrat + Open Sans but renders system sans-serif, and the
body copy is currently 15 px capitalised because of the CSS leak.
- A: self-host Montserrat + Open Sans locally (CSP-safe, SIL OFL) and restore the intended body
  scale. Looks closer to the original design intent, but **will visibly differ from today's render**.
- B: keep the system-sans fallback deliberately (what visitors see now) and only fix the
  capitalisation artefact.
- Recommendation: **A**, with the correction treated as an intentional modernisation.

**D3 — Asset strategy.** Which images live in the published app bundle vs QDN-managed media.
- A (recommended): bundle brand/structural assets (logo, favicons, theme, self-hosted fonts,
  generic illustrations); QDN-manage all content images (portfolio covers, hero/about images,
  per-service images). Content images become editable without republishing the app.
- B: bundle everything, including portfolio previews.
- Consequence of A: each content image is a separate published resource (more writes, but they are
  exactly the images the owner will change).

**D4 — Stock photography.** Four JPEGs ship with unknown provenance/licence.
- A (recommended): replace them with owner-provided or clearly licensed images during Phase 1.
- B: keep them as-is and accept the licensing uncertainty.
- Consequence: A needs 3–4 replacement images (or a generated/illustrated alternative).

**D5 — Publishing identity.** `_qdnName` defines owner mode, so one name must be chosen.
- A (recommended): keep `Qortal Web Builders` as the publishing name.
- B: publish under a different owner name and retire the current resource.
- Consequence: changing the name changes the app URL **and** who counts as owner.

**D6 — Local owner-editing development.** Owner mode cannot work through Hub Developer Mode
(`_qdnName` is empty).
- A: accept that editing UI work is validated only against a published build (slower iteration, but
  no divergence).
- B: add a development-only owner override compiled out of production builds (fast iteration, small
  risk of accidentally shipping it).
- Recommendation: **A** for Phases 2–3, with B only if iteration cost becomes painful; if B, the
  override must be dead-code-eliminated in production and covered by a build assertion.

**D7 — Article pages.** The 4 article pages plus the out-of-golden-master blog listing/detail
templates.
- A (recommended): keep a small article kind (`qwb_post_*`, §6.1) so the site can grow editorially
  without a rebuild.
- B: drop articles in v1 and ship a one-page service site; add them later.
- Consequence: A adds one content kind and a detail view; B reduces Phase 1–3 scope.

**D8 — Existing commerce/contact touchpoints.** Keep the `Q-Shop` order links, the Q-Mail/group
contact block, and the `qortal://` portfolio links?
- A (recommended): keep them (they are working Qortal touchpoints) and make their labels/URLs
  editable fields.
- B: replace ordering/contact with a private-chat contact form (reuse
  `skills/qortal/private-chat-contact-form`) or plain instructions.
- Consequence: A preserves current revenue/contact paths; B changes how customers reach the owner.

**D9 — Approved first publication target.** Any real QDN write requires explicit authorization.
- A (recommended): during Phases 2–4, publish to a **separate staging name/identifier** and publish
  to the live `Qortal Web Builders` resource only at the final acceptance step.
- B: develop and publish directly against the live resource (faster, but the public site changes
  mid-development).
- Consequence: A needs a second publishing name (or at least a distinct resource) that the owner
  controls.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-target-architecture-proposal.md`
