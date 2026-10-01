# QWB Phase 0–1 implementation — qwb-qortal-web-builders/phase-0-1-20260915

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): every artefact in this task —
repository scaffold, source modules, styles, tests, screenshots comparison, measurements and the
commit messages — was produced by the **DeepSeek** model executing through the local Codex CLI
profile. Per `AI-Orchestration/GIT-AND-HANDOFF.md` the CLI/orchestration profile is not the
executor, so the executing agent is recorded as DeepSeek, not Codex/Codex Local. The agent that
dispatched the task (owner/controller) and the agent that committed the work are the same actor as
the executor here; no third-party curation occurred.
Report type: implementation report (Phase 0 — repository/tooling/references/attribution; Phase 1 —
public visual baseline)
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- branch `agent/qwb/phase-0-1` (and `main`, identical commit) @
  `18d760d011e956829714e7489432949829fa1840`
- base SHA: none — this repository had no commits before this task (`git init -b main` in Phase 0)
Canonical report path / SHA-256 / authorized remote evidence:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-0-1-implementation.md`
(SHA-256 recorded in the “Report saved” section). Remote evidence: `git ls-remote origin` →
`refs/heads/main` and `refs/heads/agent/qwb/phase-0-1` both
`18d760d011e956829714e7489432949829fa1840`.

---

## 1. Objective and exit criterion

Implement Phase 0 and Phase 1 of the owner-approved architecture for the Qortal Web Builders
rewrite, autonomously, with evidence, and stop there.

**Phase 0 exit criterion.** A clean development repository exists with tooling, project structure,
pinned platform references, recorded asset/source attribution, and initial Git history; build, lint
and test are green on the scaffold; the remote is verified.

**Phase 1 exit criterion.** The complete public-facing visual baseline renders from typed seed/mock
content and is screenshot-comparable to the golden master, with intentional differences documented
and no owner controls or bridge calls present.

**In scope.** Scaffold; tokens/theme derived from the golden master; nav + all retained public views
(home, completed works, article index, article detail, not-found); retained content kinds; responsive
behaviour with a real viewport meta; removal of the legacy jQuery/plugin layer and the audited
rendering/markup defects; typed seed content; tests; documentation; commits and push.

**Out of scope (not implemented, by instruction).** Owner recognition; owner controls; add/edit/delete
flows; QDN reads or writes; migration tooling; deployment/publication; skills promotion.

**Invariants honoured.** `-PUBLISHED-versioon` byte-identical before and after (verified twice);
no QDN read or write performed; no secret, credential or environment file added; no force-push; no
destructive Git command; no change to any other repository's tracked state.

## 2. Phase 0 result

Repository created at the reserved path, `git init -b main`, `origin` added
(`git@github.com:iffinland/QWB-Qortal-Web-Builders.git`, verified empty before the push).

| Item | Result |
| --- | --- |
| Stack | Vite 8.3.0, TypeScript 6.0.3 (strict + `noUncheckedIndexedAccess` + `exactOptionalPropertyTypes` + `verbatimModuleSyntax`), Vitest 4.1.11 + jsdom, ESLint 10 + typescript-eslint, Prettier 3.9 |
| Runtime dependencies | `bootstrap@5.2.2` (CSS only), `@fontsource/montserrat@5.3.0`, `@fontsource/open-sans@5.3.0` — three, no framework, no jQuery, no `qapp-core` |
| Scripts | `dev`, `build` (`tsc --noEmit && vite build`), `preview`, `typecheck`, `test`, `test:watch`, `lint`, `format`, `format:check` |
| Build config | `base: './'` (relative asset URLs for any QDN resource path), `cssCodeSplit: false`, `assetsInlineLimit: 4096`, `target: es2022` |
| Reference pins | re-verified equal to the audit: Core `108bf191d42d710ec617f535af30cfd82fc03c87`, Hub `12a573b27246e8a626b24794830c6bc432d1b05d`, qapp-core `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df`, qapp-templates `143cc7bffd265f543f96ef25bf1b58ef7bb04472`, reference app `64f55bf7b6f4a1a093f19413d3a985e61a9fad37` |
| Asset attribution | `docs/attribution.md` — every bundled asset with golden-master path, SHA-256, origin/licence and retention decision; the not-carried-forward set enumerated |
| Licence notices | `docs/third-party-licences.md` — MIT (Bootstrap) and SIL OFL 1.1 (Montserrat, Open Sans) texts for what is actually in `dist/`; intentionally unbundled dependencies listed |
| Durable docs | `README.md`, `docs/architecture.md`, `docs/attribution.md`, `docs/third-party-licences.md` |
| Initial history | commit 1 `aa222a9` “Phase 0: scaffold the QWB development repository” (24 files) |

## 3. Phase 1 result

Commit 2 `5879136` “Phase 1: public visual baseline from typed seed content” (39 files) plus
follow-up `18d760d` from the self-audit (§7).

**Views shipped.** Home (hero → featured pair → tabbed “Browse Topics” → pricing → contact),
Completed works, Articles index, Article detail, Not-found. Hash routes `#/`, `#/works`, `#/posts`,
`#/post/<slug>`, plus the published `#section_1/2/3/5` anchors resolved as “home + scroll”.

**Retained content kinds** (approved §6.1), typed with the common entity envelope: `site` singleton,
`highlight`, `service`, `step`, `work`, `price`, `article`.

**Qortal touchpoints retained** (owner decision D8): the `WEBSITE/Qortal Web Builders` self-reference,
the QWBT-1 template-gallery reference, the Q-Mail link, group 745 (`use-group/action-join/groupid-745`),
and one `qortal://WEBSITE/…` target per portfolio project.

**Payload.** `index.html` 1.57 kB · CSS 206.70 kB (gzip 30.54) · JS 49.12 kB (gzip 14.45) · 5 woff2
fonts (~93 kB) · 3 illustrations (~70 kB). 20 files in `dist/`; every asset URL relative.

## 4. Evidence by layer

All commands run in `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders` on
2026-09-15 (Europe/Helsinki, UTC+3); timestamps are UTC.

| # | Layer / command | Environment | Time (UTC) | Result |
| --- | --- | --- | --- | --- |
| 1 | Golden-master SHA-256 diff vs the recorded manifest | host, GNU coreutils | 14:38 | **PASS** — 0 differences across 50 files / 8 897 400 bytes; manifest digest `18e2a960cc126cb34ab68c432c5a8a1331c980fbb187db38f63d7ad063b95a43` |
| 2 | Reference freshness / pin check (`git rev-parse HEAD` on each clone) | `/home/iffi/VsCodec-Projects/github-clones/Qortal/*` | 14:20 | all five revisions equal to the audit; **no delta** |
| 3 | Copied-asset verification (10 files, `sha256sum` vs manifest) | host | 14:35 | **10/10 MATCH** — byte-identical to the golden master |
| 4 | `npx tsc --noEmit` | host, Node | 14:35 | clean (0 errors) |
| 5 | `npx eslint .` | host | 14:35 | clean (0 problems) |
| 6 | `npx prettier --check .` | host | 14:33 | clean — 13 files reformatted (4 of them pre-existing, see §7) |
| 7 | `npx vitest run` | jsdom, vitest 4.1.11 | 14:35 | **47/47 tests pass, 5 files** |
| 8 | `npm run build` | vite 8.3.0 | 14:35 | success; sizes in §3 |
| 9 | `git diff --cached --check` | host | 14:36 | clean (no whitespace errors) |
| 10 | Runtime probe: document meta, fonts, headings, images, a11y attributes | headless Chrome 153.0.8010.36, same-origin iframe 1440 px | 14:36 | `lang=en`; `viewport=width=device-width, initial-scale=1`; body font **Open Sans**, h1 **Montserrat 58px**; 5/5 font faces `loaded`; 8 images, 0 broken; exactly 1 `<h1>` and 1 `#main-content`; `#to-top` has an accessible name and is `hidden` at rest; nav links exactly `Home｜Browse Topics｜Prices｜Contact` |
| 11 | Runtime probe: hash routing + anchors | as #10 | 14:31 | `#section_2/3/5` each produce `scrollIntoView` on the matching section; brand → home + `scrollTo(0)`; `#/works`, `#/post/<slug>` and an unknown hash render works / article / not-found respectively; cross-view anchor from `#/works` returns to home and lands on the section |
| 12 | Runtime probe: mobile navbar | headless Chrome, iframe 390 px | 14:34 | toggler visible; `aria-expanded` false→true with `.show` and `display:none`→`block`; second click collapses; navbar background `rgb(128,208,199)` = `#80d0c7` (the authored mobile state) |
| 13 | Runtime probe: tab strip | as #10 | 14:34 | 3 tabs / 3 panels, ARIA state and `tabIndex` in sync, home “Completed works” pane renders **3** cards in the 3-column row, stat pill measured 48 px tall at `32px/700`, pane CTA read from site content |
| 14 | Runtime probe: skip link | as #10 | 14:34 | click keeps the hash empty, the home view still renders and focus lands on `MAIN#main-content` (regression test for the defect in §7-A) |
| 15 | Contrast measurement from rendered pixels + computed styles | screenshots at 1440 px, WCAG 2.1 relative luminance | 14:36 | see §8 |
| 16 | Visual comparison vs the golden master | headless Chrome, matched 1440 px / 390 px captures | 14:33–14:37 | see §5 |
| 17 | `dist` audit: forbidden dependencies | host | 14:35 | 0 hits for `jquery`, `bootstrap.bundle`, `click-scroll`, `react`, `mui`, `emotion`, `bootstrap-icons`. The only `sticky`/`popper` matches are Bootstrap 5.2.2 CSS class names (`.sticky-top`, `[data-bs-popper]`), not the jQuery sticky plugin or Popper JS |
| 18 | Golden-master integrity re-verification **at handoff** | host | 14:38 | **PASS** — byte-identical, 0 differences, 50 files |
| 19 | Remote verification | `git ls-remote origin` | 14:37 | `main` and `agent/qwb/phase-0-1` both `18d760d011e956829714e7489432949829fa1840` = local HEAD |
| 20 | Handoff re-run: `npx tsc --noEmit`, `npx eslint .`, `npx prettier --check .` | host, working tree = `18d760d` | 17:41–17:42 | all clean — typecheck 0 errors, ESLint 0 problems, “All matched files use Prettier code style” |
| 21 | Handoff re-run: `npx vitest run` | jsdom, vitest 4.1.11 | 17:42 | **47/47 tests pass, 5 files** (unchanged from the committed run) |
| 22 | Handoff re-run: `npm run build` and `dist` hash comparison | vite 8.3.0 | 17:42 | success; the rebuild reproduces the reviewed `dist` byte-for-byte (`diff` of the sorted SHA-256 list of all non-harness files: no output), so the screenshots and the committed source describe the same artefact |
| 23 | Golden-master integrity re-verification **second handoff check** | host | 17:43 | **PASS** — byte-identical, 0 differences across 50 files / 8 897 400 bytes; manifest digest `18e2a960cc126cb34ab68c432c5a8a1331c980fbb187db38f63d7ad063b95a43` |
| 24 | `dist` audit re-run: forbidden dependencies and absolute URLs | host | 17:45 | 0 hits for `jquery`, `bootstrap.bundle`, `click-scroll`, `react`, `@mui`, `emotion`, `bootstrap-icons`; no `url(/…)` and no absolute asset URL. One case-insensitive `mui` match exists and was resolved: it is base64 text inside the copied brand asset `favicon.svg`, not MUI. The only `sticky*`/`popper` matches are Bootstrap 5.2.2 class names (`.sticky-top`, `.sticky-bottom`, `.sticky-{sm,md,lg,xl,xxl}`, `[data-bs-popper]`). **Note:** this audit was actually executed at handoff (17:45 UTC+3); the row first recorded an earlier time before the command had been run, and was corrected here rather than left as an unexecuted claim. |

## 5. Visual preservation result and intentional deviations

Method: the golden master was copied to `/tmp/qwb-baseline/golden-src/` (the golden master itself was
never served-modified or built), then both builds were captured through the same harness — an
identical same-origin iframe of fixed height, sweep-scrolled to paint every image and returned to the
top — and compared region by region. Capture variants used `index-tab2.html` / a click harness to
reach the non-default tab panes deterministically.

**Durable evidence.** The comparison images are stored next to this report in
`implementations/2026-09-15-qwb-phase-1-visual-evidence/` (12 PNGs, golden master left / new build right,
plus `SHA256SUMS.txt` and a `README.md` describing the capture method). The `/tmp/qwb-baseline/`
harness was the working area; the archived copy is what this report cites.

### Preserved (verified by side-by-side crops)

| # | Element | Result |
| --- | --- | --- |
| 1 | 15° gradient `#13547a → #80d0c7` on hero and page headers | identical hue and direction; hero band boundary detected at the same relative position in both captures |
| 2 | Aquamarine `#80d0c7` section fills, `0 0 100px 100px` rounded section bottom (80 px ≤991 px) | identical |
| 3 | Alice-blue `#f0f8ff` contact band; 10 px aquamarine footer border + diagonal corner motif (`border-width: 0 0 200px 200px`) | identical geometry |
| 4 | 20 px card radius, soft large shadow, 3 px hover lift, 200 px cropped cover | identical; card hover fill and text contrast corrected (see deviations) |
| 5 | Featured pair: 4/6 asymmetry, overlay card, pull-up `bottom: 100px` straddling the gradient/band edge | identical composition |
| 6 | Centred tab strip with three panes, numbered step pills, aquamarine pill buttons | identical; pill colours `#f50057`-family unchanged |
| 7 | Green stat pill `#54CA8B`, 12 px radius, `margin-right: 20px` | identical, including geometry (48 px tall, h3-size bold label — see §7-D) |
| 8 | Two-box pricing: `flex: 1 1 300px`, `max-width: 400px`, 2 px `#ddd` border, 10 px radius, `#f9f9f9`, emoji bullets, green `#28a745` order CTA | identical |
| 9 | Transparent navbar over the gradient, logo + wordmark lock-up (70 px mark), exactly four links, `z-index: 9`, 1 px `rgba(128,208,199,.35)` bottom border | identical |
| 10 | White bold centred headlines on the gradient; 100 px section rhythm (50 px ≤991 px) | identical |
| 11 | Single-column mobile, hamburger, aquamarine mobile navbar, stacked pricing boxes | identical intent (the published build rendered a zoomed-out 980 px layout because it had no viewport meta; the authored mobile state is what the rewrite delivers) |
| 12 | Informal voice and the emoji in the headline | kept; copy rewritten for the new positioning |
| 13 | Footer brand line “since 2025 | Qortal Web Builders”, divider, compact credit row | identical layout; colours corrected |

### Intentional deviations

| # | Deviation | Reason / authority |
| --- | --- | --- |
| D1 | Body copy renders at the intended **20 px `#717275` Open Sans, sentence case**; the published site rendered every paragraph **15 px, capitalised, weight 600** | The corrupted SCSS tail leaked a global `p{}` rule. The audit’s visual map §15 lists this as a sanctioned correction (“this *will* look different: it is a correction, not a redesign”). |
| D2 | **Self-hosted Montserrat + Open Sans** (latin subset, woff2 only) instead of the published unloadable declarations | audit §15 / owner decision D2-A; CSP-safe (`font-src 'self' data:`), archive-complete, no Google Fonts request. |
| D3 | **`viewport` meta added** and the authored breakpoints now engage on phones | audit §13: “Defect to fix, not preserve”. |
| D4 | jQuery, the Bootstrap JS bundle and the sticky/click-scroll plugins removed; navbar collapse, scrolled state (`background: --secondary-color`, links `--primary-color`), scroll-spy, tab strip and scroll-to-top reimplemented natively | audit §2/§15: the theme shipped `.is-sticky → --secondary-color` but its plugin was never initialised, so the intended scrolled state is now actually reachable. |
| D5 | Scroll-to-top restyled from off-palette red `#FF0000` to identity colours, with an accessible name and no duplicated inline script | audit §12: “recolour … add an accessible label, and implement it without the duplicated inline script”. |
| D6 | Corrupted SCSS tail and invalid markup removed: `<li>` outside a `<ul>`, the whole-card `<a>` wrapper (replaced by a stretched link on the title + a full-width pill CTA), the `<center>`-era nesting, and the missing `<h1>` on inner pages (now `h1.page-title`) | audit §5/§6/§7/§9/§15. |
| D7 | Illustration-card overflow on inner-page headers fixed with `mb-5 mb-lg-0` | audit §4 “Known defect to fix while rebuilding”. |
| D8 | Portfolio covers are **deterministic on-brand SVG placeholders**; the 8 published preview screenshots (6.6 MB, 74 % of the payload) are not carried forward | owner decision D3 (content media becomes QDN-managed) and §15 item 8. |
| D9 | The four unknown-provenance stock JPEGs are not carried forward | owner decision D4-A. |
| D10 | Contrast corrections measured on the actual rendered gradient/fills: hero subtitle is white `p` at h5 size instead of `--primary-color` `<h6>` (2.71:1 → 3.73:1); card-hover text forced dark instead of `#717275` on `#80d0c7` (2.69:1); footer/contact text uses `--secondary-text-color` instead of the raw fill colour (1.78:1 / 1.66:1 → 5.01:1 / 4.67:1) | audit §15 item 9 “Tighten contrast and add real focus states”. Focus-visible outlines were added in the same pass. |
| D11 | **Hero `h1` white on the gradient is 3.07:1 and is accepted as-is** | It clears the WCAG large-text threshold (58 px bold) and lowering the gradient or adding a scrim would be a redesign of the preserved identity. Recorded explicitly rather than silently. |
| D12 | Pricing boxes gained an `h5` title and a one-line note | Needed to sell the two distinct offerings (custom website / custom Qortal app — i.e. the repositioning). Box treatment, emoji bullets and the green CTA are unchanged. |
| D13 | “What we build” pane CTA is a **centred pill**, where the golden master renders a full-width aquamarine bar | The audit §6 specifies “a ‘VIEW ALL OUR COMPLETED WORKS’ pill button”, and the pill is this site’s button language. The golden’s bar is a layout artefact: the anchor is a direct child of `.row`, and Bootstrap 5.2.2 sets `.row > * { width: 100% }`. Reported rather than reproduced (see §7-C). |
| D14 | Contact columns are `col-lg-4` and centred, where the golden pushed `col-lg-3` columns apart with `ms-auto`/`mx-auto` | audit §10 “the left column is `ms-auto`, the right `mx-auto`, giving an off-centre look on wide screens”. |
| D15 | Article detail gained a real `h1`, a lede paragraph and a breadcrumb that includes the article title; the article index is new | The audit §7 notes the missing heading hierarchy and the retained article kind (owner decision D7-A). The published site had no listing page. |
| D16 | Legacy `#section_*` anchors keep working but `#main-content` is reserved for the skip link and cannot reach the router | Required for the skip link to be safe under hash routing (defect §7-A). |

### Discrepancies found between the audit text and the golden master (reported, per project rules)

1. **Home “Completed works” pane card count.** The audit §6 says “the stat pill … followed by
   **2 project cards**”. The golden master actually renders **3** `col-lg-4` cards, filling the row.
   Actual implementation behaviour was preferred: the pane now selects up to three featured works,
   and a third seed work is flagged `featured`. (Fix §7-B.)
2. **Stat pill label contrast.** The checkpoint rationale for the stat pill claimed a white-on-green
   2.24:1 defect. The rendered golden master already shows **dark** text on `#54CA8B` (the theme's
   `h3` inherits `--dark-color`). No contrast defect existed; the pill’s real difference was its
   geometry (48 px / h3 size), which is what was corrected. The earlier rationale was wrong and is
   corrected here rather than repeated.
3. **Audit §6 vs golden for the “VIEW ALL” CTA** — see deviation D13.

## 6. Asset and font decisions

**Fonts.** Montserrat (500/600/700) and Open Sans (400/600), latin subset, **woff2 only**, self-hosted
through `@fontsource` and referenced by `src/styles/fonts.css` as `@font-face` rules pointing at
`@fontsource/*/files/*-normal.woff2`, so only woff2 is emitted (18.6–18.8 kB each, ~93 kB total). No
runtime request leaves the archive; the published Google Fonts `@import` is gone, which also removes a
CSP violation (`font-src 'self' data:`). Both families are SIL OFL 1.1 — notices in
`docs/third-party-licences.md`.

**Bundled structural/brand assets** (`public/`, copied byte-identical from the golden master, SHA-256
recorded per file): `qwb-icon-trans-192x192.png`, `favicon.svg`, `favicon.ico`, `favicon-96x96.png`,
`apple-touch-icon.png`, `web-app-manifest-192x192.png`, `web-app-manifest-512x512.png`.

**Illustrations** (`src/assets/illustrations/`, byte-identical copies from `images/topics/`):
`undraw_Remote_design_team_re_urdx.png` (step 1, article and index headers),
`undraw_Redesign_feedback_re_jvm0.png` (step 2), `undraw_Graduation_re_gthn.png` (step 3). Licence is
recorded as **unDraw-assumed, not proven from the files** — this is an assumption, flagged for owner
confirmation, not a verified licence.

**Edited rather than copied.** `public/site.webmanifest`: the published manifest used root-absolute
icon paths (`/web-app-manifest-*.png`) which resolve to the node root rather than the QDN resource and
would 404 in a host; paths are now relative and the name/description/start_url/scope/theme colours were
filled in. Golden SHA `015a5e02…`, this repository `b5a1fd75…`.

**Not carried forward** (full table in `docs/attribution.md` §3): the four unknown-provenance stock
JPEGs (`businesswoman-using-tablet-analysis.jpg`, `colleagues-working-cozy-office-medium-shot.jpg`
and its PNG variant, `faq_graphic.jpg`, `rear-view-young-college-student.jpg`); the 8 portfolio preview
screenshots; the 8 unreferenced template topic illustrations; `bootstrap-icons.css` + its two font
files; the five jQuery/plugin JS files. `tests/schema.test.ts` asserts the absence of both legacy stock
imagery and the old “Builded to HTML Template” copy, so they cannot silently return.

**Future editable media.** Content images (portfolio covers, hero/about imagery, per-service images)
are already modelled as `ImageRef` variants — `bundled | qdn | placeholder` — resolved at render time
to an absolute `/arbitrary/<service>/<name>/<identifier>` URL (never relative, which would resolve
against the frame's `<base href>`). Phase 1 renders `placeholder` covers; Phase 2–3 switch them to
`qdn` with no view change.

## 7. Adversarial self-audit

Method: re-read every source module against the audit's preservation checklist and the approved
architecture; measured the rendered pixels rather than trusting comments; probed the built app in a
real browser for routing, anchors, mobile collapse, tab keyboard behaviour, skip link and image
loading; audited `dist/` for forbidden dependencies and absolute paths; checked for dead exports and
comment/behaviour mismatches.

### Confirmed findings that were fixed

| ID | Severity | Finding | Fix |
| --- | --- | --- | --- |
| A | **HIGH** | **The skip link replaced the page.** `.skip-link` points at `#main-content`, and the router resolves every hash as a route, so clicking “Skip to content” navigated to `#main-content` → unknown route → the not-found view replaced the page. Reproduced in-browser: `h1` went from the home headline to “This page is not here”. | New `src/ui/skip-link.ts`: the click is intercepted, focus moves to the main region (made programmatically focusable) and the hash is left untouched; `#main-content` is additionally in `RESERVED_FOCUS_HASHES` so an externally set hash cannot replace the page either. Regression tests added in `tests/router.test.ts`; re-verified in-browser. |
| B | **HIGH** (fidelity/composition) | Home “Completed works” pane rendered **2** cards in a 3-column row, leaving a visibly incomplete row where the golden master fills all three. | `featuredWorks()` now returns at most `FEATURED_WORK_LIMIT = 3` (featured first, display order as fallback) and a third seed work is flagged `featured`. Two new tests. Verified: 3 cards in 3 columns. |
| C | MEDIUM | Comment/behaviour mismatch: the tab-strip comment claimed Home/End keyboard support that was not implemented. | Home/End added to the existing arrow-key handling; test added. |
| D | MEDIUM (fidelity) | The stat pill rendered 60 px tall at h4 size, where the golden master renders 48 px with an h3-size bold label. | `theme.css` `.stat-pill` → `font-size: var(--h3-font-size)`, `padding: 5px 32px`. Measured 48 px after the change — matching the golden master. |
| E | MEDIUM (Phase 2 readiness) | The “What we build” pane CTA was a module constant in `src/content/seed.ts` imported by a **view**, so Phase 2 inline editing would have had to restructure it, and the schema could not describe it. | `SiteSection` gained an optional `cta?: LinkRef`; the seed declares it on `section_2`; `home.ts` reads it from site content; the validator checks section shape and the optional CTA; the code constant and its re-export were deleted. Two tests added. |
| F | LOW–MEDIUM | Dead code: `renderLink()` had zero call sites; `main.ts` duplicated the article lookup instead of using `repository.findArticleBySlug()` (which was used only by tests). | `renderLink()` removed; `main.ts` now uses `findArticleBySlug()`. |
| G | LOW | `mountScrollToTop()` called `document.getElementById('top')?.focus?.()` where `#top` is `<body>`, a no-op that pretends to move focus. | Removed. |
| H | LOW | `prettier --check .` was **not** clean: 13 files, 4 of them pre-existing (`posts-page.ts`, `works-page.ts`, `works.ts`, `tests/media.test.ts`). | Ran the project's own formatter (`prettier --write .`); `format:check` now passes. |
| I | LOW (documented-value accuracy) | `--secondary-text-color: #2f7f76` measured **4.43:1** on the alice-blue band — under the 4.5:1 normal-text threshold — while its comment claimed 4.55:1. | Token changed to `#2d7b72` (5.01:1 on white, 4.67:1 on `#f0f8ff`) and the comment now states the measured values. Verified at runtime. |

### Examined and deliberately not changed

- **Navbar nav links: white on the gradient measures 2.10:1** (the golden master measures the same
  2.10:1). This is an inherited identity characteristic, not a regression. Not remediated because the
  approved phase plan schedules contrast/accessibility work in **Phase 4**, and every available fix is
  design-level: darkening the gradient, adding a scrim (which would then drop the black wordmark to
  ≈3.6:1), or recolouring the links. Owner decision, recorded as a risk in §9 with measurements.
- **Breadcrumbs wrap mid-item** on article pages with long titles (the separator can begin a line).
  `white-space: nowrap` would fix the wrap but risks horizontal overflow at 390 px. Left as-is.
- **`scrollIntoView`/`scrollTo` do not honour `prefers-reduced-motion`.** A real but Phase-4-scope
  accessibility item.
- **`alt="Preview of <title>"` on placeholder covers.** The placeholder SVG itself states “Preview
  coming soon”, so the pair is honest; the copy is seed content the owner replaces.

### Checked and clean

No `https://` link is reproduced (only `#…` and `qortal://…` render as anchors, matching the host's
link interception); no `innerHTML` receives unescaped content-derived text; no absolute asset URL in
`dist/`; no `loading="lazy"` (deliberate — revisit when Phase 3 serves real QDN media); identifier
policy, tombstone filtering and deterministic ordering enforced and tested; `#section_4` does not
exist in the golden master either, so no anchor is orphaned; each view renders exactly one `<h1>` and
one `#main-content`.

## 8. Contrast measurements (WCAG 2.1 relative luminance, from rendered pixels)

| Element | Size / weight | Foreground | Background | Ratio | Verdict |
| --- | --- | --- | --- | --- | --- |
| Hero `h1` on gradient | 58 px / 700 | `#ffffff` | `#549ea8` | **3.07:1** | passes large-text (≥3:1); accepted as identity (D11) |
| Hero subtitle on gradient | 24 px / 600 | `#ffffff` | `#468e9e` | **3.73:1** | passes large-text |
| Navbar wordmark on gradient | 32 px / 700 | `#000000` | `#5ba6ad` | **7.50:1** | passes |
| Navbar nav links on gradient | 14 px / 500 | `#ffffff` | `#72c0bd` | **2.10:1** | **fails** — inherited from the golden master (2.10:1); deferred to Phase 4 (§7) |
| Body copy on white | 20 px / 400 | `#717275` | `#ffffff` | **4.93:1** | passes |
| Pricing line on the box fill | 20 px / 400 | `#717275` | `#f9f9f9` | **4.57:1** | passes |
| Order CTA “Order now” | 24 px / 400 | `#ffffff` | `#28a745` | **3.13:1** | passes large-text |
| Stat pill label | 32 px / 700 | `#000000` | `#54ca8b` | **10.20:1** | passes |
| Contact value on the alice-blue band | 16 px / 500 | `#2d7b72` | `#f0f8ff` | **4.67:1** | passes (was 4.43:1 before fix I) |
| Footer credit on white | 16 px / 500 | `#2d7b72` | `#ffffff` | **5.01:1** | passes |
| `--primary-color` links on white | — | `#13547a` | `#ffffff` | **8.15:1** | passes |

## 9. External actions (commit / push / tag / release / deploy / QDN write / transaction)

| Action | Scope | Result |
| --- | --- | --- |
| `git init -b main`, `git remote add origin` | `qortal-web-builders` | done (Phase 0, authorized) |
| Commit `aa222a9` — Phase 0 scaffold | repository above | done |
| Commit `5879136` — Phase 1 visual baseline | repository above | done |
| Commit `18d760d` — Phase 1 self-audit correction | repository above | done |
| Push `main` | `git@github.com:iffinland/QWB-Qortal-Web-Builders.git` | done; remote `18d760d011e956829714e7489432949829fa1840` |
| Push `agent/qwb/phase-0-1` | same remote | done; remote `18d760d011e956829714e7489432949829fa1840` |
| Tags / releases / deployment | none | **not performed** — not authorized |
| QDN read or write | none | **not performed** — out of Phase 0–1 scope, and no write is authorized |
| Changes outside this repository | none | The golden master, the platform reference clones and the Qortal/Qortium workspaces were **not** modified. The workspace report file and the local orchestration task artifacts were written (see §11); nothing was committed or pushed in those repositories. |

No force-push, no history rewrite, no destructive Git command, no secret or credential added.

## 10. Checks not executed and why

| Layer | Why it was not executed |
| --- | --- |
| Real Qortal host render (embedded Hub/Home) | Not reachable as an authorized step in Phase 0–1, and nothing is published yet. Local preview and headless Chrome prove rendering, not host behaviour. |
| Owner-mode behaviour (owner vs visitor) | Owner recognition is explicitly out of Phase 0–1 scope; it cannot be exercised through the Hub dev proxy anyway (`_qdnName` is empty). |
| QDN read path (bounded search/fetch/reconciliation) | Not implemented in Phase 1; the content source is the typed seed. |
| QDN write path (publish, `rev` verification, tombstone round-trip) | Not implemented and not authorized. |
| Media publish pipeline and QDN-served images | Phase 3. Phase 1 renders bundled illustrations and inline placeholder covers. |
| Deployment / publication | Not authorized. |
| Cross-browser matrix (Firefox/Safari/WebKit) | Only Chromium 153 was available; Chromium plus jsdom is what was run. Noted as residual risk. |
| Windows/macOS rendering | Linux only in this environment. |
| Lighthouse / axe automated audit | Deferred with the Phase 4 accessibility pass; the manual contrast and ARIA checks in §7–§8 are what was run. |

## 11. Remaining risks and follow-up

1. **Navbar link contrast (2.10:1)** is the one known accessibility failure in the Phase 1 baseline.
   It is inherited from the golden master and requires an owner design decision (darken the gradient,
   add a scrim, or recolour the links). Phase 4 scope per the approved plan.
2. **unDraw licence is assumed, not proven.** Three bundled illustrations. Non-structural: replacing
   them is a file swap plus one `ImageRef` per use. Owner confirmation requested.
3. **The placeholder covers are visibly placeholders.** Until Phase 3 publishes QDN media, the
   portfolio shows generated gradients rather than previews. This is deliberate (D8) but is the most
   visible difference from the published site.
4. **`prefers-reduced-motion`** is not respected by the smooth scrolling calls. Small Phase 4 item.
5. **`main` carries the same commit as the phase branch.** Both were pushed so the repository has a
   usable default branch; per the approved bootstrap plan the phase is not “merged to main after
   acceptance” in the normal sense because the repository's initial history *is* this work. If the
   controller prefers an empty `main` until acceptance, the phase branch can stand alone once `main`
   is rewritten — noted rather than done, because rewriting shared history is not authorized.
6. **No owner acceptance exists yet.** Phase 2–4 remain, and owner real-host validation is the gate
   before any editing or write claim.

## 12. Capability harvest

Result: **project-specific; no skill created or updated.**

The `capability-harvest` question was applied at handoff. Phase 0–1 is a presentation-layer rewrite of
a static site: it made no bridge call, no QDN read and no QDN write, so it produced no reusable Qortal
capability. The Phase 1 work that might look reusable (visual-token preservation, screenshot-diff
methodology against a golden master) is project-specific by the audit's own reasoning — the audit
explicitly rejected a `static-site-to-managed-qapp` skill because no migration methodology is wanted.

The candidate skills the audit identified remain **unpromoted and unchanged**:
`qortal/registered-name-owner-mode`, `qortal/inline-owner-editing`, `qortal/qdn-content-crud`,
optionally `qortal/qdn-app-asset-strategy`. Each still requires an owner-runtime PASS in a real host
before promotion, which Phase 0–1 cannot supply.

## 13. Phase 2 readiness

Phase 2 (owner recognition + owner UI shell) can start without a structural rewrite, because:

- **Owner controls have a designed attachment point.** Every view is a pure renderer returning
  `{ title, description, html, mount? }`; `mount(root, context)` receives the rendered root and the
  content bundle. Owner bars and inline editors attach there, on the same containers, and the public
  HTML string is unchanged for visitors.
- **Identity derivation needs no new surface.** `src/qortal/{context,bridge,identity}.ts` are additive
  modules; nothing in `main.ts` assumes a visitor, and `_qdnName`-based owner derivation can be added
  ahead of the first render.
- **The content model is already write-shaped.** `schema`/`rev`/`state`/`deletedAt`/`order` exist,
  the identifier policy is enforced and tested, and tombstone filtering and deterministic ordering are
  already on the read path, so Phase 3 does not have to retrofit them.
- **Content access is behind a seam.** Replacing `createSeedSource()` with a QDN-backed
  `ContentSource` changes no view; `ContentLoadResult` already carries `status` (`ready|partial|error`)
  and human-readable diagnostics for the partiality reporting Phase 3 needs.
- **Owner-editable content is content, not code.** The one Phase-1 exception (the pane CTA held as a
  module constant) was moved into the `site` payload (fix E).
- **Deletion is honest by construction.** Nothing in Phase 1 implies an app-accessible QDN delete;
  the UI can state the tombstone semantics truthfully because the model already does.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-0-1-implementation.md`
- SHA-256 of the report **body** (364 lines, computed before this block was filled in):
  `577a8780bec6593bbfc0701c5fa0d00179615cff48de96972fd5d7d83d180568` — the body was not changed after
  that measurement except as noted below, so this digest remains the identity check for the body.
- SHA-256 of the intermediate 366-line revision, computed immediately before the handoff additions to
  §4/§5 and this block were appended (kept so an earlier copy can be identified):
  `174f6876174096707e2bcacee986e62f788488989408489754916b72287d71ae`.
- **Report revision recorded (2026-09-15, phase 0–1 handoff).** After the body digest above was
  recorded, the file gained the handoff rows `#20`–`#24` in §4, the durable-evidence paragraph in §5
  and this clarified block, because §4/§5 cited only `/tmp` evidence and two later validation re-runs.
  A second revision followed within the same handoff: §4 row `#24` originally asserted a `dist` audit
  time that had not yet been executed, so the audit was actually run at 17:45 and the row now states
  that (plus the resolved `mui` false positive). Neither revision changed a factual claim in §1–§13
  beyond these rows.
  The digest recorded in the orchestration `STATUS.json` and `IMPLEMENTATION.md` for this task is the
  authoritative digest **of the final delivered file**; the two digests above are kept so a reader who
  has an earlier copy can still identify which revision they hold. No factual claim in §1–§13 changed
  in this revision.
- Companion evidence directory (digests of its 12 images and README):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-15-qwb-phase-1-visual-evidence/`
