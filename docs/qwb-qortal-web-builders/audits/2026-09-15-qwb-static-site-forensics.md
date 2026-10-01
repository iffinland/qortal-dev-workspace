# QWB static site forensics + architecture audit — qwb-qortal-web-builders/architecture-audit-20260915

Executing agent (registered role of the agent that actually produced this work): `DeepSeek`
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): the analysis, source
inspection and validation commands in this task were produced by the DeepSeek model running
through the local Codex CLI profile. Per `AI-Orchestration/GIT-AND-HANDOFF.md`, work executed
through a Codex/`codex` CLI profile is authored by the model that performed it, and the
orchestration profile is not the executor. No other agent contributed evidence.
Report type: forensic audit + architecture proposal (read-only; no implementation)
Exact application repository / branch / SHA: **no application repository exists yet**;
the audited artifact is the immutable static golden master
`/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/-PUBLISHED-versioon` (no Git metadata).
Reference application: `iffinland/iffi-vaba-mees-QORTAL` branch `main`
`64f55bf7b6f4a1a093f19413d3a985e61a9fad37`.
Canonical report path: this file (see "Report saved" at the end).

Status: **READ-ONLY AUDIT COMPLETE — IMPLEMENTATION NOT STARTED AND NOT AUTHORIZED**

---

## 0. Objective and exit criterion

Objective: produce a decision-ready forensic and architectural audit of the published
Qortal Web Builders static site plus the owner-editing reference application, so the owner
can approve one architecture before any implementation starts.

Exit criterion: every audit objective (1–15) in the task controller answered from source or
runtime evidence, with an explicit golden-master integrity proof, and no implementation,
QDN write, deployment or skill promotion performed.

## 1. Baseline, scope and safety

| Item | Value |
| --- | --- |
| Golden master (read-only) | `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/-PUBLISHED-versioon` |
| Golden master Git metadata | **none** (no `.git` in the directory or in its parent) |
| Owner work touched | none — nothing was written, renamed, formatted or deleted anywhere under the golden master |
| Reference clone created for this audit | `/home/iffi/VsCodec-Projects/github-clones/Qortal/iffi-vaba-mees-QORTAL` (new clean clone, `main` @ `64f55bf7`) |
| Out-of-scope siblings (not the published site) | `KÕIK-POSTID-topics-listing-BLOG-PAGE.html`, `MALLIKS-topics-detail.html`, `QWB-Web-Builders-kola/`, `QWB-favicon/`, `portal-HTML-templates/`, `favicont-512x512-removebg-preview.png` |
| Explicitly excluded as reference | the Shadow Archives Studio owner-auth architecture (owner UX and owner recognition); only its validated Qortal contracts were treated as reusable knowledge |

Read before analysis: `AI-Orchestration/AGENTS.md`, `WORKFLOW.md`, `skills/README.md`,
`PROJECT-REGISTRY.md`, `ENVIRONMENT.md`, `GIT-AND-HANDOFF.md`,
`Qortal/qortal-dev-workspace/AGENTS.md`, `docs/workflows/report-storage-policy.md`,
`agents/00-SESSION-START.md`, `agents/qortal-qdn-and-bridge.md`,
`agents/qdn-publication-discovery-and-scaling.md`,
`docs/architecture/qortal-dapp-development-standard.md`,
`skills/qortal/qdn-derived-index-coherence`, `skills/qortal/bridge-fetch-qdn-resource-normalization`.

No audit report existed for this project before this task; the project was unregistered in
`PROJECT-REGISTRY.md` and has been registered as part of this task.

## 2. Golden-master integrity result

- Inventory: **50 files**, **8,897,400 bytes**, 7 subdirectories (`css/`, `fonts/`,
  `images/`, `images/icons/`, `images/topics/`, `images/web-preview/`, plus root).
- SHA-256 manifest (50/50 files):
  `docs/qwb-qortal-web-builders/validation/2026-09-15-qwb-golden-master-sha256.txt`
- Integrity result: **PASS — byte-identical before and after the audit.** Proof is recorded
  in `validation/2026-09-15-qwb-golden-master-integrity.txt`.
- All writes produced by this audit live under
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/`
  and `/home/iffi/VsCodec-Projects/AI-Orchestration/tasks/`, plus temporary files in `/tmp`.

## 3. Directory structure and file inventory

```text
-PUBLISHED-versioon/
├── index.html                              (28,157 B)  home: hero, cards, 3 tabs, pricing, contact, footer
├── completed-works.html                    (14,781 B)  portfolio gallery, 8 project cards
├── order-reception-and-planning.html       (10,715 B)  article: process "step by step"
├── why-do-you-need-a-own-website.html      ( 8,712 B)  article
├── valuing-your-time.html                  ( 8,183 B)  article
├── what-information-do-we-want-first.html  (10,794 B)  article: checklist
├── css/
│   ├── bootstrap.min.css                   (194,901 B) Bootstrap 5.2.2 (MIT), vendored
│   ├── bootstrap-icons.css                 ( 88,587 B) vendored, local @font-face
│   └── templatemo-topic-listing.css        ( 26,711 B) bespoke template CSS (theme layer)
├── fonts/
│   ├── bootstrap-icons.woff                (150,592 B)
│   └── bootstrap-icons.woff2               (112,440 B)
├── js/
│   ├── jquery.min.js                       ( 85,658 B) jQuery v2.2.3 (2016)
│   ├── bootstrap.bundle.min.js             ( 80,496 B) Bootstrap 5.2.2 (Popper bundled)
│   ├── jquery.sticky.js                    (  7,301 B) Sticky Plugin v1.0.3 (2015)
│   ├── click-scroll.js                     (  1,267 B) in-page scroll + scroll-spy
│   └── custom.js                           (  1,631 B) navbar collapse + smooth scroll + dead timeline code
└── images/
    ├── favicon.ico / favicon.svg / favicon-96x96.png / apple-touch-icon.png
    ├── qwb-icon-trans-192x192.png          brand mark used in navbar + footer
    ├── web-app-manifest-192x192.png / -512x512.png / site.webmanifest
    ├── businesswoman-using-tablet-analysis.jpg, colleagues-working-cozy-office-medium-shot.jpg,
    │   faq_graphic.jpg, rear-view-young-college-student.jpg          (stock photos, provenance unknown)
    ├── icons/q-mail-centered-350x250.png
    ├── topics/  (11 PNG: 10 unDraw illustrations + 1 photo crop)
    └── web-preview/ (8 PNG, 1920×1080 screenshots of built sites, 0.4–1.3 MB each)
```

Per-extension counts: 6 HTML, 3 CSS, 5 JS, 2 WOFF, 17 PNG, 4 JPG, 1 SVG, 1 ICO, 1 JSON.
Largest single asset: `images/web-preview/asot-web-preview.png` = 1,332,263 B.

## 4. HTML / page structure

**It is a multi-page static site, not an SPA.** Six real `.html` files with relative links
between them; no client-side router, no templating, no partials. Every page duplicates the
complete `<head>`, the navbar, the footer and an inline `<style>` block.

| Page | Role | Top-level anchors | Notable structure |
| --- | --- | --- | --- |
| `index.html` | home | `#section_1`…`#section_5` (no `section_4`) | hero, 2 featured cards, tabbed "Browse Topics" (3 panes), pricing, contact, footer |
| `completed-works.html` | portfolio | breadcrumb only | gradient header + 8 project cards in a 3-column grid |
| `order-reception-and-planning.html` | article | breadcrumb only | process list + quote block |
| `why-do-you-need-a-own-website.html` | article | breadcrumb only | short argumentative copy |
| `valuing-your-time.html` | article | breadcrumb only | short argumentative copy |
| `what-information-do-we-want-first.html` | article | breadcrumb only | intake checklist |

Navigation: a transparent Bootstrap 5 navbar (`navbar navbar-expand-lg`) with the QWB logo
(70×70), wordmark, and four links: Home, Browse Topics → `index.html#section_2`, Prices →
`index.html#section_3`, Contact → `index.html#section_5`. Article pages keep the same navbar
but their links point back to `index.html` anchors.

Markup defects confirmed in source: a duplicated empty `<li class="nav-item">` in the navbar;
`<li>` elements used directly inside `<div>`/`<p>` (no `<ul>`); invalid `<p><h6>…</h6></p>`
nesting; two deprecated `<center>` wrappers; `<h1>` used only on the home hero (article pages
start at `<h2>`); all images with content meaning have empty `alt=""` except the logo.

## 5. CSS organization (and how much of it is actually applied)

Three stylesheets plus a per-page inline `<style>` block:

1. `bootstrap.min.css` — Bootstrap 5.2.2 framework layer (unmodified).
2. `bootstrap-icons.css` — icon font with a **local** `@font-face` (`../fonts/…`); this is the
   only webfont that genuinely loads.
3. `templatemo-topic-listing.css` — the bespoke theme layer. Design tokens in `:root`,
   component classes, two breakpoints (991 px, 480 px), then a **corrupted appended block**
   (lines ≈1150–1320) containing an external `@import url('https://fonts.googleapis.com/css?family=Poppins')`,
   SCSS variables (`$bgcolor`, `$btncolor`, `$headingbg`) and nested SCSS syntax (`&:hover{}`,
   nested `li{}`) that a browser cannot parse.

Design tokens (unchanged in the published build):

```text
--primary-color #13547a   --secondary-color #80d0c7   --section-bg-color #f0f8ff
--border-color #7fffd4    --p-color #717275           --custom-btn-bg-color #80d0c7
--body-font-family 'Open Sans'    --title-font-family 'Montserrat'   (neither is loaded anywhere)
h1 58 h2 46 h3 32 h4 28 h5 24 h6 22 p 20 (px)   radius 100 / 20 / 10 px
```

Runtime-verified reality versus declared intent (headless Chrome 153.0.8010.36, `file://`,
2026-09-15) — this is what a visitor actually sees today, and therefore what must be
preserved if "preserve the current character" is taken literally:

| Computed property | Value | Cause |
| --- | --- | --- |
| `body` font-family | `Poppins, sans-serif` (Poppins **not** loaded → generic sans) | last `body{}` rule in the theme file; `@import` is blocked/unavailable |
| `body` font-size / padding / text-align | `16px` / `0px` / `start` | the inline `<style>` `body{}` override is **dropped** by malformed comment markers |
| `p` color / size / weight / transform | `rgb(39,38,37)` / `15px` / 600 / **capitalize** | global leak from the corrupted SCSS tail |
| `h1` | `#fff`, 58 px | theme layer |
| `.hero-section` padding-top | 150 px | theme layer |
| `.featured-section` bottom radius | 100 px | theme layer |
| `.custom-block` radius / shadow | 20 px / `rgba(0,0,0,.176) 0 16px 48px` | theme layer |
| `.custom-block-image` height | 200 px, `object-fit: cover` | theme layer |
| `.pricing-box` border / radius / bg | `2px solid #ddd` / 10 px / `#f9f9f9` | malformed inline block (rules survived, `body{}` did not) |
| `.order-btn` bg | `#28a745` | malformed inline block |
| `.site-footer` border-bottom | `10px solid #80d0c7` | theme layer |
| `.navbar` background | transparent (gradient shows through) | theme layer |

Consequences worth flagging: the **entire body copy of the site renders capitalised 15 px
dark text** because of a global `p{}` leak, and the inline `Arial`/`20px`/centred-body
overrides never applied. Any "pixel-faithful" preservation must copy the *rendered* result,
not the declared tokens.

## 6. JavaScript behaviour

Load order on every page: `jquery.min.js` → `bootstrap.bundle.min.js` → `jquery.sticky.js` →
`click-scroll.js` → `custom.js`, plus a per-page inline copy of the "scroll to top" script.

| Script | Actual behaviour today |
| --- | --- |
| `bootstrap.bundle.min.js` | navbar collapse (mobile toggler) and the three "Browse Topics" tab panes — the only interactive behaviour a visitor reliably uses |
| `click-scroll.js` | smooth-scroll anchors + scroll-spy for `#section_1..5` |
| `custom.js` | closes the mobile menu on nav click; the rest of its scroll handler targets `#vertical-scrollable-timeline`, which **does not exist on any page** (dead template code, harmless no-op) |
| `jquery.sticky.js` | loaded on every page but **no element is ever initialised as sticky** — `.sticky-wrapper.is-sticky` is never created, so the plugin is dead weight |
| inline "Top" button script | duplicates the same ~20 lines on all six pages; adds a fixed red scroll-to-top button |

Runtime-verified defect: `click-scroll.js` iterates `section_1..section_5`, but the home page
has **no `#section_4`**. Because `document.querySelector`-style lookup returns an empty
jQuery set, `.offset()` returns `undefined` and `.top` throws:

- programmatic click on the **Contact** nav link → `Uncaught TypeError: Cannot read properties
  of undefined (reading 'top')` at `click-scroll.js:24`, with `location.hash` becoming
  `#section_5` (the exception fires *before* `preventDefault()`, so the browser's native
  fragment jump is what actually happens — no smooth scroll);
- dispatching a `document` scroll event → same TypeError at `click-scroll.js:9` (the
  scroll-spy handler for the missing section throws on every scroll event).

No console errors occur from missing assets; all 8 home-page images load
(`images=8 ok=8`).

## 7. Assets, fonts and images

- **Icons**: Bootstrap Icons via local WOFF/WOFF2 — CSP-compatible, keep.
- **Declared-but-absent fonts**: `'Open Sans'` and `'Montserrat'` are referenced by the
  tokens but no `@font-face` or `<link>` loads them; `Poppins` is referenced only through an
  external `@import` that cannot load under the production render CSP
  (`font-src 'self' data:`). Typography today is therefore default sans-serif.
- **Photography**: 4 stock JPEGs of unknown provenance/licence shipped with the template
  (`businesswoman…`, `colleagues…`, `faq_graphic.jpg`, `rear-view…`). Flagged as an owner
  decision (§15 of the architecture proposal).
- **Illustrations**: 10 `undraw_*` PNGs (open illustration set) plus one photo crop in
  `images/topics/`.
- **Portfolio previews**: 8 large PNG screenshots (0.4–1.3 MB each, 1920×1080) — over 6.6 MB,
  74 % of the payload. These are exactly the assets that belong in QDN-managed content rather
  than baked into the app bundle.
- **PWA bug (verified in source)**: `images/site.webmanifest` references its icons as
  `/web-app-manifest-192x192.png` and `/web-app-manifest-512x512.png` — root-absolute paths,
  while the files live in `images/`. Inside a QDN render frame these resolve to the node root
  and 404.

## 8. Responsive strategy

- Bootstrap 5 grid plus two hand-written breakpoints: `max-width: 991px` (type scale down,
  `.section-padding` 100→50 px, navbar background becomes `--secondary-color`,
  `.featured-section` radius 100→80 px) and `max-width: 480px` (h1 58→36 px…).
- **`<meta name="viewport">` is absent on all six pages** (source-level fact, confirmed at
  runtime: `viewportMeta=ABSENT`). On real phones the layout viewport therefore falls back to
  ~980 px and the page renders as a zoomed-out desktop layout; the two mobile breakpoints are
  effectively unreachable as designed. Headless desktop window-width tests do show the
  breakpoints working (hamburger appears, cards stack), but that is not what a phone does.
- Observed mobile-width defects at 390 px: the navbar wordmark overflows the viewport, and the
  tab strip wraps to two lines.
- `completed-works.html` uses Bootstrap columns only; `index.html` uses the "pull the card row
  up over the coloured band" technique (`.featured-section .row { bottom: 100px; margin-bottom: -100px }`).

## 9. Recurring visual components and repeated content patterns

Reusable component vocabulary extracted from the rendered pages:

1. **Gradient band** — `linear-gradient(15deg, #13547a 0%, #80d0c7 100%)` used by
   `.hero-section` (150 px vertical padding) and `.site-header` (article/gallery pages,
   breadcrumb + `<h2>` + illustration).
2. **Rounded coloured section** — `.featured-section` with `border-radius: 0 0 100px 100px`
   (80 px at ≤991 px) carrying the "stand out / why do you need a website" cards.
3. **Content card** — `.custom-block` (20 px radius, 30 px padding, `shadow-lg`, hover lift
   `translateY(-3px)` + background turns `--secondary-color`), with `.custom-block-image`
   (full width, 200 px, `object-fit: cover`) and an optional numbered pill badge.
4. **Overlay card** — `.custom-block-overlay` (min-height 350 px, absolutely positioned text
   at z-index 2 over a gradient `.section-overlay` at 85 % opacity).
5. **Tab strip** — centred `nav-tabs` with an active underline; three panes ("Website Building
   Steps", "Completed Works", "Template Gallery").
6. **Pill button** — `.custom-btn` / `.custom-border-btn` (secondary-colour fill, 100 px radius,
   hover → primary colour) and the dark green `.order-btn` (#28a745, 5 px radius) used by the
   pricing boxes.
7. **Pricing box** — `.pricing-box` (max 400 px, 2 px #ddd border, 10 px radius, #f9f9f9, soft
   shadow) with emoji-icon bullet lines.
8. **Footer** — brand block, a 10 px secondary-colour bottom border, and a **diagonal corner
   motif** drawn with `::after { border-width: 0 0 200px 200px; border-color: transparent
   transparent #80d0c7 transparent; }`, plus a one-line legal/host note.
9. **Statistic button** — `.statcompleted` (#54CA8B) / `.statprogress` (#FAC20A) rounded pills
   ("Completed websites - 8").

Repeated content patterns (hard-coded, page by page, no data layer):

| Pattern | Repetition |
| --- | --- |
| Process step card (title + description + numbered badge + illustration) | 3 cards in the first tab of `index.html`, expanded to 8 items in `order-reception-and-planning.html` |
| Portfolio card (preview image + title + "Builded To/Using … CMS" + `Watch live website` button + QDN link) | 8 items in `completed-works.html`, 2–3 mirrored in the home tabs |
| Pricing box (5 emoji bullet lines + Q order button) | 2 boxes |
| Article block (breadcrumb, gradient header, `<h3>`, list/paragraphs, quote box) | 4 article pages |
| Navbar + footer + inline `<style>` + inline "Top" script | 6 copies each (no shared partials) |

## 10. Existing Qortal / QDN integration

The published site already integrates with Qortal by **deep links only** — no bridge calls, no
`qortalRequest`, no `_qdn*` usage, no dynamic read of QDN data:

| QDN / Qortal target | Occurrences |
| --- | --- |
| `qortal://WEBSITE/Qortal%20Web%20Builders` (self, footer "Design:" credit) | 7 |
| `qortal://WEBSITE/HTML-web` (template gallery) | 6 |
| `qortal://use-group/action-join/groupid-745` (community group) | 3 |
| `qortal://WEBSITE/ASOT%20-%20A%20State%20Of%20Trance` | 3 |
| `qortal://WEBSITE/iffi%20vaba%20mees`, `.../Suomi%20-%20Finland`, `.../Eestlased%20Qortalis` | 2 each |
| `qortal://APP/Q-Shop/Qortal%20Web%20Builders/q-store-general-qortal-web-builders` (ordering) | 2 |
| `qortal://APP/Q-Mail/to/Qortal20Web%20Builders` (contact) | 1 |
| `qortal://WEBSITE/iffi%20forest%20life`, `.../suomen%20vapaiden%20ihmisten%20kommuuni` | 1 each |
| external `https://qortal.org` (footer) | 6 |

Two integration facts matter for the rebuild:

- `qortal://` links are handled by Core's injected `q-apps.js` click interceptor
  (`LINK_TO_QDN_RESOURCE`) — this is the supported in-app navigation mechanism and must be kept.
- The **same interceptor calls `preventDefault()` for every `http://`, `https://` and `//` link**
  ("Block external links"), so the footer's `https://qortal.org` link is dead inside a Qortal
  host. Source-verified in `qortal` @ `108bf191`, `src/main/resources/q-apps/q-apps.js`
  (click interception block); not runtime-tested in a real host during this audit.

## 11. Build tooling, dependencies and separation of content and presentation

- **No build tooling at all**: no `package.json`, no bundler, no minifier, no linter, no tests,
  no CI. Hand-authored HTML/CSS/JS served as-is.
- Vendored dependencies: Bootstrap 5.2.2 (CSS+JS), Bootstrap Icons (font+CSS), jQuery 2.2.3,
  Sticky 1.0.3. Two framework generations are mixed (jQuery 2.x from 2016 with Bootstrap 5 from
  2022).
- **Content and presentation are fully entangled**: every string, price, project entry and
  contact detail is inline markup; there is no data file, no JSON, no template, no includes.
  Changing one price means editing `index.html`; the same project list exists twice
  (`index.html` tabs and `completed-works.html`) and the process list exists twice with
  different lengths.
- There is no `.gitignore`/`.git` and no release/version marker inside the published directory
  (the footer says "since 2025" and credits template `QWBT-1`).

## 12. Brittle, obsolete and accessibility findings

**Brittle / obsolete (all source-verified, several runtime-confirmed):**

1. Malformed CSS comment markers (`<!important -- … -->`, `<!-- … start -->`) inside the inline
   `<style>` blocks silently drop the rules that follow them (body font/padding/alignment),
   while later selectors in the same block survive — non-obvious and hard to maintain.
2. An entire SCSS file is pasted into the end of the shipped CSS: external Google Fonts
   `@import`, `$variables`, nested rules. It cannot be maintained as-is and its `p{}` and
   `h4{}` rules **leak globally**, changing body copy on every page.
3. Missing `<meta name="viewport">` on all pages (mobile layout broken by default).
4. `#section_4` does not exist while `click-scroll.js` iterates 1–5: an uncaught TypeError on
   the Contact nav click and on document scroll.
5. jQuery 2.2.3 (2016, EOL) loaded for ~3 KB of bespoke behaviour; `jquery.sticky.js` is never
   initialised; `custom.js`'s scroll code targets an element that exists on no page.
6. Duplicated navbar/footer/head/inline-style/inline-script across six files — a content or
   brand change must be repeated six times.
7. `.webmanifest` uses root-absolute icon paths that cannot resolve inside a QDN render frame.
8. External `https://` links are silently dead inside the Qortal host (bridge blocks them).
9. Inline `style="…"` attributes scattered through markup (footer credits, pricing heading)
   plus `Arial` fallbacks declared per page.
10. Invalid/nested markup (`<p><h6>`, `<li>` outside lists, `<center>`) that the browser
    repairs silently, making "preserve exactly" ambiguous.

**Accessibility concerns:**

- No `viewport` meta (above) — the single largest mobile accessibility defect.
- Decorative illustrations carry empty `alt` (acceptable), but content-bearing preview images
  also carry empty `alt` — no text alternative for the portfolio.
- Tabs rely on Bootstrap's data API and are labelled, but the markup duplicates
  `role="presentation"`/`aria-controls` inconsistently across panes.
- The scroll-to-top button is a bare `<button>` with no `aria-label` and red-only affordance.
- Emoji used as the only semantic marker for pricing bullet meaning (screen readers announce
  them literally).
- `.custom-block:hover` changes background to the secondary colour, but white text on
  `--secondary-color` (`.text-white` inside `.custom-block-overlay`) is the only
  contrast-checked combination; `.statcompleted` (white on #54CA8B) is borderline.
- Colour alone is not used for the stat pills' meaning, but their labels are still cryptic
  ("Completed websites - 8" is fine; the yellow pill has no label).
- Heading order: article pages have no `<h1>`; `<h3>`/`<h5>` are used as visual sizes rather
  than document structure.

## 13. Per-part classification

| Part | Classification | Note |
| --- | --- | --- |
| Overall composition, section order, rhythm | **preserve** | home: hero → featured pair → tabbed topics → pricing → contact → footer |
| Colour system (`#13547a`/`#80d0c7`/`#f0f8ff`/`#7fffd4`) and 15° gradient | **preserve** | the strongest identity signal; carry over as tokens verbatim |
| Typography *intent* (Montserrat/Open Sans) | **preserve with modernization** | self-host under CSP, or knowingly accept the current system-sans reality |
| Typography *reality* (capitalised 15 px body text from the CSS leak) | **replace** | an artefact, not a design decision — do not preserve |
| Radii/shadow tokens (100/20/10 px, soft shadow, hover lift) | **preserve** | |
| Diagonal footer corner motif + 10 px footer border | **preserve** | distinctive and cheap |
| Cards, overlay card, tab strip, pill buttons, pricing boxes, stat pills | **preserve with modernization** | same look, rebuilt as real components with state |
| Hero structure (white h1 + `h6` subtitle on gradient, 150 px padding) | **preserve** | becomes the "edit hero" surface |
| Navbar (transparent, logo + wordmark, 4 links) | **preserve with modernization** | add viewport meta, real anchor targets, accessible toggler |
| Bootstrap 5.2.2 CSS layer | **preserve with modernization** | keep as layout substrate, or lift used utilities into owned CSS |
| Bootstrap Icons + local font | **preserve** | CSP-safe |
| jQuery + jQuery plugins + inline scripts | **replace** | no reason to carry jQuery into a built app |
| Inline `<style>`/malformed comment blocks | **replace** | fold surviving rules into the owned theme file |
| `templatemo-topic-listing.css` theme layer | **preserve with modernization** | keep the design tokens/components, delete the corrupted tail, fix the global `p{}` leak |
| Copy/text, prices, project list, contact details | **content-only reference** | to be rewritten; seed the new app with mock content |
| 6 static HTML pages | **content-only reference** | layout evidence; not to be migrated mechanically |
| Portfolio preview PNGs | **content-only reference** | become QDN-managed media |
| Stock photos of unknown provenance | **content-only reference** | licensing decision (§15) |
| QDN deep links (`qortal://…`) | **preserve** | still the correct in-app link mechanism |
| `https://qortal.org` external link | **replace** | dead inside the host; use a QDN-valid target or plain text |
| Dead template JS/CSS (sticky, timeline, SCSS tail) | **replace** | delete |

## 14. Evidence by layer

| Layer | Action | Environment | Result |
| --- | --- | --- | --- |
| Static inventory | `find`/`file`/`du`/`sha256sum` | local, 2026-09-15 | 50 files, 8,897,400 B, types + hashes recorded |
| Static source read | `sed`/`grep` over HTML/CSS/JS | local | structure, tokens, links, defects recorded |
| Rendered visual | headless Chrome 153.0.8010.36 screenshots | local `file://` | home full page, completed works, article, 390 px width, secondary tab |
| Rendered behaviour | headless Chrome DOM probes of the real page in an iframe | local `file://` | computed styles table, viewport-meta absence, jQuery 2.2.3, 8/8 images, `click-scroll.js` TypeErrors, Contact click behaviour |
| Platform contract | source inspection of Qortal Core/Hub at pinned SHAs | clean clones | see the platform compatibility report |
| Real Qortal host | **not executed** | — | no owner-runtime validation claimed by this audit |
| Live QDN read/write | **not executed** | — | no QDN write of any kind was performed |

## 15. Checks not executed and why

- No real Hub/host rendering test: the owner's runtime validation belongs to the implementation
  and acceptance phase, and this task explicitly forbids publication.
- No QDN read or write; no node queries were needed, since the audit's platform claims come
  from pinned source.
- No automated HTML validation (no validator installed) — structural findings were read
  manually from source and confirmed where possible in the browser.
- The dev-proxy context was not exercised, because owner mode cannot be exercised there at all
  (see the platform compatibility report, §10).

## 16. Adversarial self-audit

- Initially I assumed the inline `body{font-family:Arial}` override applied; the computed-style
  probe disproved it (body renders `Poppins, sans-serif`, padding `0px`, `text-align:start`).
  The report states the verified rendered behaviour, not the source intent, and flags the
  difference explicitly.
- I initially suspected `custom.js` also threw on scroll; closer reading showed its throwing
  line lives inside a per-item callback that never runs (no timeline items), so it is dead code,
  not an error. Corrected in §6.
- The Contact-link defect was verified by a programmatic click, and its user-visible outcome
  (native fragment navigation instead of smooth scroll, because the exception precedes
  `preventDefault()`) is stated rather than the stronger claim "the link is broken".
- Framework/font claims are limited to what was measured; no claim is made about rendering on a
  real phone (the missing viewport meta is a source fact, and its consequence is reasoned).
- No external write of any kind was performed during this audit.

## Related reports

- Visual preservation map: `audits/2026-09-15-qwb-visual-preservation-map.md`
- Reference owner/editing audit: `audits/2026-09-15-qwb-iffi-vaba-mees-owner-pattern-audit.md`
- Platform compatibility + write contract: `audits/2026-09-15-qwb-qortal-platform-compatibility-and-write-contract.md`
- Target architecture proposal (stack, owner mode, content, index, inline UX, phases, decisions):
  `audits/2026-09-15-qwb-target-architecture-proposal.md`
- Integrity proof: `validation/2026-09-15-qwb-golden-master-integrity.txt`

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-static-site-forensics.md`
