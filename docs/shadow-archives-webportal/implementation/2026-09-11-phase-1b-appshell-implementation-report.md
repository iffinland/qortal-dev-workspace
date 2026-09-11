# Shadow Archives Phase 1B — Qortal APP bootstrap and responsive AppShell (implementation report)

- Project: `shadow-archives-webportal-QORTAL`
- Phase / task: Phase 1B — bootstrap the Qortal `APP` and implement the responsive
  AppShell
- Date: 2026-09-11
- Author: Codex (implementation agent)
- Task class: product/feature + UI work (new Q-App foundation), with a
  platform-integration boundary defined but **not** exercised at runtime
- Related:
  [`../architecture/2026-09-11-phase-1a-architecture-report.md`](../architecture/2026-09-11-phase-1a-architecture-report.md),
  [`../architecture/2026-09-11-phase-1b-implementation-plan.md`](../architecture/2026-09-11-phase-1b-implementation-plan.md),
  [`../architecture/2026-09-11-responsive-appshell-and-design-tokens.md`](../architecture/2026-09-11-responsive-appshell-and-design-tokens.md),
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md)

## 1. Status

**PASS WITH OWNER VALIDATION REQUIRED.**

The Phase 1B objective and exit criterion are met at the static, automated and
local-browser layers: the shell builds, typechecks, lints, tests and renders the
approved home layout with honest placeholder/skeleton states, route-level lazy
boundaries and permission-free capability reporting. No QDN write path, editor,
video player or interoperability work exists.

A named owner/real-host check remains: **no real Qortal host or node dev-proxy
validation was possible** (no local Qortal node was running and no host session
was available). All Qortal bridge/`_qdn*` behaviour is therefore
**NOT VERIFIED at runtime**.

## 2. Baseline and preserved changes

- Canonical workspace `qortal-dev-workspace`: branch `main`, HEAD `2f208c4`
  ("Define Shadow Archives Phase 1A architecture"). No user changes were
  overwritten, reverted, restored or deleted.
- Target repository
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`:
  the directory was empty and not a Git repository at Phase 1A closure. Before
  writing anything it was verified empty, the remote was verified empty
  (`git ls-remote` returned no refs), and the repository was then cloned into
  the canonical path (`git clone`, branch `main`, `origin` set). Nothing
  unexpected existed, so nothing had to be preserved.
- Environment: Linux, Node v20.19.2, npm 10.8.2, Google Chrome available for
  headless rendering. No local Qortal node reachable on 12391/62391/12392.
- Report root (canonical):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/`.

## 3. Objective and exit criterion

**Objective.** Create the first working Shadow Archives Qortal `APP` foundation
and responsive AppShell per the owner-approved Phase 1A architecture
(application foundation, routing, design system, responsive layout,
loading/empty states, performance boundaries).

**Exit criterion.** Shell builds/typechecks/lints/tests; the approved home layout
renders at every target breakpoint with placeholder/empty states; lazy route
boundaries are in place; capability reporting is truthful (never claiming owner);
and **no** Blog/Video/Gallery feature, publishing editor or QDN write path is
implemented. — **Met** (see §6).

## 4. What was built

### 4.1 Owner decision recorded

The owner's new **"PUBLISHING INTEROPERABILITY FIRST"** decision was added to
canonical project context
([`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md),
§"Publishing interoperability first", plus the D-matrix). It is recorded as a
**future implementation rule**: the final Video publish modal must be preceded by
then-current Q-Tube source/QDN contract research, and the final Blog publish
modal by then-current Subwire (and its Quitter cross-post) research, so the
publication model is interoperable without a later rewrite.

No Q-Tube/Subwire/Quitter code, contract or interoperability was implemented,
investigated or claimed in Phase 1B, and no UI was copied from those apps.

### 4.2 Technology and dependency decisions (as implemented)

Runtime: `react` 19.3.0, `react-dom` 19.3.0, `react-router-dom` 7.18.3.
Build: `vite` 7.3.6, `@vitejs/plugin-react` 5.2.0, `typescript` 5.9.3 (`strict`).
Test: `vitest` 3.2.7, `jsdom` 26.1.0, `@testing-library/react` 16.3.3,
`@testing-library/user-event` 14.6.7, `@testing-library/jest-dom` 6.9.1.
Lint/format: `eslint` 10.10.0 (flat config), `typescript-eslint` 8.70.0,
`eslint-plugin-react-hooks` 7.1.1, `eslint-plugin-react-refresh` 0.5.6,
`prettier` 3.9.6.

Deliberately absent (verified by grep over `package.json`, `src/` and built
chunks): MUI/emotion, `qapp-core`, `video.js`/`hls.js`/`plyr`, TipTap, DOMPurify,
`HashRouter`, icon packages, web-font/CDN dependencies. 187 packages total.

### 4.3 Router

`createBrowserRouter(appRoutes, { basename: getRouterBasename() })` where
`getRouterBasename()` reads `window._qdnBase` (empty outside a host). `HashRouter`
is not used. Routes: `/`, `/blog`, `/blog/:id`, `/videos`, `/videos/:id`,
`/gallery`, `/gallery/:id`, `/about`, `/contact`, `/category/:slug`,
`/tag/:slug`, `/search`, `*`, plus an unlinked lazy `/studio` placeholder.

The home route ships in the startup graph; **every other route is a
`React.lazy` dynamic import**, so each is a separate chunk. The route outlet sits
inside a layout-stable `Suspense` fallback and a route-level `errorElement`, so a
failing or loading route never unmounts the shell.

### 4.4 Qortal integration boundary (`src/qortal/`)

- `environment.ts` — reads the injected `_qdn*` context once into a frozen typed
  object; decodes `_qdnName` (`Shadow%20Archives` → `Shadow Archives`); exposes
  `getRouterBasename()`.
- `bridge.ts` — the only module that calls `window.qortalRequest`, with
  per-action timeouts and the error taxonomy
  `unavailable | malformed | timeout | rejected | error`.
- `auth.ts` — single-flight `GET_USER_ACCOUNT` with a session-cached rejection
  and no automatic retry. **Not called on startup**; only an explicit future
  owner flow may call it.
- `capability.ts` — pure derivation of
  `unknown | visitor | authenticated-no-name | authenticated-non-owner | owner`;
  returns `unknown` for no bridge, dev proxy, or unresolved auth/ownership and
  never reports `owner` optimistically.
- `navigation.ts` — builds the verified `qortal://APP/<name>` links and
  classifies `qortal://` vs Web2 URLs.
- `actions.ts` — typed action-name declarations for the subset used; write
  actions exist only as type names.

No Qortal/QDN request is issued by this build at any point (verified in the
browser: 8 requests total, all same-origin static assets).

### 4.5 AppShell and home

`AppShell` = skip link → `header` (Top Posts | banner | Top Videos) → primary
action row (Q-Tube, SubWire, Quitter, Search) → site navigation → `main`
(route outlet) → footer. Config (`src/app/config/siteConfig.ts`) owns the
revision-scoped published app names (`Q-Tube`, `SubWire`, `Quitter`, verified
2026-09-11) and the ≤10-item top-list cap; no component hardcodes them.

External apps render as real anchors (`qortal://APP/...`) so the host's
`q-apps.js` interception, middle-click and keyboard behaviour all work. Search is
a compact icon that expands into a labelled input, focuses it, supports Escape,
and navigates to `/search?q=…` on submit.

Home regions: `Latest Posts` / `Latest Videos` (two columns at ≥1024px),
`Latest from the Gallery` strip, all rendering honest empty states with reserved
geometry. Top panels render the loading skeleton path and the empty state; the
auto-scroll duplicate is only created when real content overflows. No engagement
counts or content are fabricated, and `ContentCard`'s engagement footer is
rendered `aria-hidden` because it holds no working control yet.

### 4.6 Design system

Semantic CSS custom properties in `src/styles/tokens.css` (charcoal/near-black
backgrounds, dark document surfaces, parchment/cream text, classified greys, one
muted dark-red accent, warm parchment-gold focus ring, restrained borders +
small shadows + inner paper highlight instead of glassmorphism).
`base.css`, `shell.css`, `content.css` consume only the semantic layer. No web
fonts are loaded (CSP `font-src 'self' data:`; no font files supplied), so
display/body stacks use local families only.

### 4.7 Accessibility and motion

Skip link as first focusable element; `:focus-visible` 3px parchment-gold outline
with 2px offset; semantic landmarks; one `h1` per route; labelled icon buttons;
`aria-current="page"` navigation; `aria-expanded`/`aria-controls` search
disclosure; ≥44px targets (≥48px at ≥1920px); no hover-only affordances.
`AutoScrollTrack` pauses on hover, `:focus-within`, pointer/wheel/touch
(3s cooldown) and document-hidden, is disabled entirely under
`prefers-reduced-motion`, never duplicates into the accessibility tree
(`aria-hidden` + `inert`), and falls back to a natively scrollable list so no
content is reachable only through animation.

### 4.8 Performance boundaries

Route-level splitting for all non-home routes; no video/player/editor/media code
in the startup path; the banner is the only startup image (WebP, explicit
dimensions, `fetchPriority="high"`); other images would be `loading="lazy"` with
reserved aspect ratios; skeletons reserve final geometry.

**Production build (Node 20.19.2, `npm run build`):**

| Artifact | Raw | Gzip |
| -------- | --- | ---- |
| `index-*.js` (entry: React + Router + shell + home) | 345.07 kB | 109.36 kB |
| `index-*.css` | 21.06 kB | 4.34 kB |
| `banner-shadow-archives-*.webp` | 202.89 kB | (already compressed) |
| Lazy route chunks (13 files) | 0.3–1.7 kB each | 0.29–0.83 kB each |

Reference: the Phase 1A React+Router-only baseline measured 317.50 kB raw /
101.08 kB gzip, and importing `qapp-core` costs ≈596 kB gzip. The entry chunk is
therefore ≈+27.6 kB raw / +8.3 kB gzip over the minimal baseline and ≈0.18× the
`qapp-core` floor. No millisecond runtime budget is invented; these are
build-output byte measurements only.

## 5. Files

### 5.1 Application repository (created; 97 files before `dist/`)

No pre-existing files were modified — the repository had no commits and no
content. Full inventory:

Root: `package.json`, `package-lock.json`, `index.html`, `vite.config.ts`,
`eslint.config.js`, `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`,
`.gitignore`, `.prettierrc.json`, `.prettierignore`, `README.md`.

`public/`: `sa-avatar.png` (owner-supplied avatar, used as the app icon).

`src/assets/`: `banner-shadow-archives.webp`.

`src/app/`: `router/{router.tsx,routes.tsx,routes.test.tsx}`,
`providers/{AppProviders,AuthProvider,BridgeProvider,CapabilityProvider,DesignTokensProvider,index}`,
`config/{siteConfig.ts,navigation.ts}`.

`src/components/common/`: `AutoScrollTrack.tsx` (+ test), `Button.tsx`,
`MediaFrame.tsx`, `Skeleton.tsx`, `icons.tsx`, `index.ts`.
`src/components/layout/`: `AppShell.tsx` (+ test), `PrimaryActions.tsx`,
`SearchDisclosure.tsx` (+ test), `SiteBanner.tsx`, `SiteFooter.tsx`,
`SiteHeader.tsx`, `SiteNav.tsx`, `TopListPanel.tsx`, `index.ts`.
`src/components/feedback/`: `EmptyState.tsx`, `ErrorState.tsx`,
`RootErrorBoundary.tsx`, `RouteErrorBoundary.tsx`, `RouteLoading.tsx`,
`index.ts`.

`src/features/`: `home/{HomePage.tsx,HomePage.test.tsx,homeContent.ts,components/{ContentCard,GalleryStrip,LatestPostsSection,LatestVideosSection,SectionHeader}.tsx}`,
`engagement/topContent.ts`, `shared/RoutePlaceholder.tsx`,
`blog/{BlogPage,BlogPostPage}.tsx`, `videos/{VideosPage,VideoDetailPage}.tsx`,
`gallery/{GalleryPage,GalleryDetailPage}.tsx`, `search/SearchPage.tsx`,
`about/AboutPage.tsx`, `contact/ContactPage.tsx`,
`taxonomy/{CategoryPage,TagPage}.tsx`, `owner/StudioPage.tsx` (+ test),
`not-found/NotFoundPage.tsx`.

`src/qortal/`: `environment.ts` (+ test), `bridge.ts`, `auth.ts`,
`capability.ts` (+ test), `navigation.ts` (+ test), `actions.ts`, `types.ts`,
`index.ts`.

`src/styles/`: `tokens.css`, `base.css`, `shell.css`, `content.css`.
`src/types/`: `content.ts`, `global.d.ts`. `src/utils/`: `motion.ts`,
`overflow.ts`. `src/test/`: `setup.ts`, `utils.tsx`, `environment.ts`.
`src/main.tsx`, `src/vite-env.d.ts`.

### 5.2 Canonical workspace (modified)

- `projects/shadow-archives-webportal.md` — recorded the new owner decision
  ("Publishing interoperability first"), updated "Current state" with the
  factual Phase 1B state (clone, dependency versions, commands, build sizes,
  validation state, NOT VERIFIED items), kept the Phase 1A snapshot as a clearly
  marked historical subsection, and marked the Phase 1B scaffold step DONE.
- This report (new file). No other workspace file was changed.

## 6. Validation executed

| Layer / command | Environment | Result |
| --------------- | ----------- | ------ |
| `npm install` | Node 20.19.2, npm 10.8.2 | 187 packages, no engine warnings after pinning `jest-dom` 6.9.1 and eslint 10 |
| `npm run lint` (eslint 10 flat) | local | **PASS**, 0 errors / 0 warnings |
| `npm run typecheck` (`tsc -b`, strict) | local | **PASS**, 0 errors |
| `npm test` (vitest, jsdom) | local | **PASS** — 9 files, 59 tests |
| `npm run build` (`tsc -b && vite build`) | local | **PASS** — chunks as in §4.8 |
| `npm run format:check` | local | **PASS** (after `prettier --write`) |
| Headless-Chrome smoke test vs `vite preview` (production build) | Chrome, 320/375/768/1024/1440/1920/2560 px | **PASS** (details below) |
| Same-origin network audit | Chrome | **PASS** — 8 requests, 0 external; no console/page errors |
| Workspace structural validator `bash tools/validate-workspace.sh` | local | **PASS** (0 errors, 5 pre-existing warnings for human review) |

Tests (59) cover: route resolution for all 14 paths; shell landmarks and
`aria-current`; no bridge call during shell render; no studio link for visitors;
search disclosure expand/focus/Escape/submit/empty-guard; `isTrackOverflowing`
axis logic; auto-scroll disabled without overflow, with insufficient content and
under reduced motion; the duplicate copy being `aria-hidden` + `inert` and
pointer-pause; home empty states with no fabricated engagement data; card
geometry from a synthetic (test-only) state; studio page inertness and
zero bridge calls; `_qdnName` decoding and environment/proxy detection;
capability derivation for all six states; `qortal://` navigation helpers.

Headless-browser measurements (production build):

- No horizontal overflow at any width (320 → 2560; `documentElement.scrollWidth`
  equals the viewport at every breakpoint).
- Shell width = 90vw (288/375/691/922/1296/1728/1760 px) and clamps at 1760 px
  (0.688 of 2560), confirming the owner's 90vw + max-width rule.
- Banner height 180 (mobile) → 240 (768) → 280 (1024) → 320 px (≥1440), i.e.
  inside the approved 300–340 px desktop band; header height 306–346 px.
- Header panels: stacked on mobile, two-up at 768 px, three-panel
  (`240 | banner | 240`) from 1024 px; DOM order `posts, banner, videos`.
- Primary action row width ratio 0.70 at 1024–1920 px (≈70% page width).
- Minimum interactive height 44 px (48 px at ≥1920 px).
- One `h1` per page; one image (the banner) and it loads and decodes
  (`naturalWidth` 1202); 5 empty states on `/`.
- Keyboard: first Tab focuses the skip link with a visible 3 px solid
  `rgb(224,196,106)` outline; search expands, focuses the input, Escape returns
  focus to the toggle; submit reaches `/search?q=redaction` with the query
  rendered.
- Navigation Blog → Videos keeps the shell mounted and sets `aria-current`.
- Reduced-motion emulation: `prefers-reduced-motion` matches, skeleton animation
  is `none`, no auto-scroll instances exist (no content) and no duplicate copies.
- Console/page errors: none.

Screenshots were captured for 375/768/1440/1920 px (`/tmp/sa-browser/`) and
inspected; the desktop render matches the approved layout with the real banner
artwork, muted-red primary actions and no generic-blue styling.

## 7. Not verified (honest gaps)

- **Real Qortal host and node dev-proxy rendering: NOT VERIFIED.** No local
  Qortal node was running (12391/62391/12392 unreachable) and no Hub Developer
  Mode session was available. Consequence: injected `_qdn*` context, the
  `qortal://APP/...` anchor interception, host `GET_USER_ACCOUNT` behaviour,
  owner detection against real name ownership, and QDN CSP/render behaviour are
  all unvalidated. Local Vite preview is explicitly **not** proof of Qortal
  compatibility.
- Bridge/authorization behaviour is covered only by unit tests with synthetic
  environments, not by a real host.
- No QDN read, publish, milestone-status or engagement behaviour was exercised,
  because none is implemented in this phase.
- Auto-scroll motion could not be exercised in the browser (no content exists in
  Phase 1B, so no `AutoScrollTrack` instance is rendered); the motion/pause/
  duplicate rules are verified by jsdom unit tests and CSS review only.
- No runtime timing measurements (paint, request count, memory) were taken; §4.8
  numbers are build-output bytes.

## 8. Adversarial self-audit (findings and remediation)

Checklist item → finding → classification → action:

- HashRouter accidentally used → none (only an explanatory comment) → — → none.
- MUI dependency / `qapp-core` root import / video.js in startup / TipTap in
  startup → none in `package.json`, `src/` or `dist/` → — → none.
- Owner authentication requested on load → none; test asserts zero bridge calls
  during shell render, and `/studio` also issues none → — → none.
- Fake QDN behaviour presented as real → none; every region reports
  `unavailable` with an explicit explanation and no fake counts → — → none.
- Hardcoded owner authority / hardcoded Qortal address → none (grep clean); the
  only URL literal is the public repository URL in config → — → none.
- Hardcoded external APP targets scattered through components → none; names live
  in `siteConfig.externalApps` with a `verifiedOn` date → — → none.
- Generic blue styling / heavy glassmorphism → none; muted-red accent + charcoal
  + parchment tokens, restrained elevation → LOW (palette values remain
  provisional until the owner supplies the final brand set) → documented.
- Excessive banner height → desktop 320 px inside the approved 300–340 px band;
  the 16:9 source does not drive header height (fixed box + `object-fit: cover`)
  → — → none.
- Desktop layout squeezed onto mobile → mobile is a genuine reflow: banner first,
  then compact top lists, full-width action/nav rows; no horizontal overflow at
  320 px → LOW (mobile header total height 523–565 px at 320–375 px because the
  two compact panels stack; the spec permits compact lists) → documented for the
  owner's visual review.
- Interactive targets below 44 px → **HIGH, found by browser measurement**:
  the "All posts"/"All media" section links measured 22 px tall → fixed
  (`inline-flex`, `min-height: var(--sa-hit-target)`); re-measured minimum 44 px
  (48 px at ≥1920 px).
- Primary action row not ~70% page width → **MEDIUM, found by browser
  measurement**: it was 70% of the shell (≈48% of a 2560 px viewport) → fixed to
  `min(70vw, 100%)`; re-measured 0.70 at 1024–1920 px.
- Inaccessible auto-scroll / missing reduced motion → auto-scroll is opt-in,
  keyboard-pausable, duplicate is `aria-hidden` + `inert`, disabled under
  reduced motion, natively scrollable otherwise; covered by tests → — → none.
- Layout shifts from unreserved media → banner height reserved per breakpoint,
  cards/gallery/skeletons reserve geometry with explicit aspect ratios → LOW
  (not measured with CLS tooling; verified by review and stable
  widths/heights across breakpoint captures) → documented.
- Q-Tube/Subwire publication work accidentally started → none; publishing
  interoperability recorded as a future rule only → — → none.
- Qortium code/API imported → none → — → none.
- Dependency/tooling drift found during setup → **MEDIUM (fixed)**:
  `@testing-library/jest-dom@7` requires Node ≥22 and `eslint@9` is EOL; pinned
  `jest-dom` 6.9.1 and moved to `eslint` 10 + `@eslint/js` 10, both supported by
  the installed plugins. All commands pass with no engine warnings.
- `react-refresh/only-export-components` false positives (barrels, provider+hook
  modules, the lazy route table) → LOW → rule scoped off for those paths with a
  written rationale; all `react-hooks` correctness rules remain enabled.
- `react-hooks/set-state-in-effect` in the reduced-motion hook and an unused
  `eslint-disable` → LOW → both fixed.
- Phase 1A spec §3 puts the auto-scroll panels before the banner in DOM order
  while the mobile layout shows the banner first → LOW → desktop DOM order
  matches the spec exactly; the banner-first mobile order is achieved with CSS
  `order` at ≤767 px (documented trade-off between DOM order and mobile visual
  preference).
- Banner asset: the real owner-supplied PNG (1202×683, 1.46 MB) was found in the
  workspace and converted locally with ImageMagick to WebP q90 (202.89 kB, no
  crop, identical dimensions) to keep the bundle honest; the original PNG remains
  the owner's master → LOW → documented for owner confirmation.
- First desktop screenshot showed a black banner box → investigated
  (`img.decode()`, element screenshot) → **capture-timing artifact, not an app
  defect**; the image loads, decodes and paints correctly → no change.
- Route table uses `/gallery/:id` as the task prompt requires, while the Phase 1A
  route table later refines gallery to `/gallery/album/:albumRef` and
  `/gallery/item/:itemRef` → LOW (future refinement; recorded below) → documented.

No in-scope BLOCKER or HIGH finding remains open.

## 9. Remaining risks and follow-up

1. **Owner/real-host validation is the outstanding gate** for anything
   platform-dependent: injected context, basename behaviour under `/render/...`,
   `qortal://APP` interception, permission prompt behaviour and CSP.
2. Gallery route refinement (`/gallery/:id` → album/item refs) before the gallery
   feature phase, per the Phase 1A route table.
3. Banner derivative (WebP q90) should be confirmed or replaced by the owner's
   preferred export; final palette/typography remain provisional until the brand
   set is supplied.
4. Mobile header height (523–565 px at 320–375 px) may want a horizontal
   snap-scroller variant later; the spec allows the current compact-list form.
5. The like/comment/tip affordances are geometry only; they must stay inert until
   the engagement phase implements them with real data.
6. Search is shell interaction only; the local compiled index and catalog phases
   are unimplemented.

## 10. Unresolved unknowns and owner decisions

- Real host/dev-proxy rendering of this shell — **UNKNOWN / NOT VERIFIED**.
- Whether a QDN write path from this app can publish within the current host
  approval/CSP model — **NOT VERIFIED** (not attempted).
- Whether `navigator.clipboard` works inside the production iframe — **NOT
  VERIFIED** (the footer currently shows the repository URL as text only).

## 11. External actions, Git and commit state

- **Commit: NO.** **Push: NO.** **Tag/release/deploy: NO.** **QDN publication:
  NO.** **Qortal transaction: NO.** **Issue/PR/project mutation: NO.**
- Application repository
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`:
  branch `main`, **no commits yet**; `git status` shows 14 top-level untracked
  entries (97 files with `--untracked-files=all`, `dist/` and `node_modules/`
  ignored). `origin` = `https://github.com/iffinland/shadow-archives-webportal-QORTAL`.
- Canonical workspace repository: branch `main`, HEAD `2f208c4`,
  `git status` shows `M projects/shadow-archives-webportal.md` plus the new
  untracked `docs/shadow-archives-webportal/implementation/` report directory.
  Nothing else was modified and no user work was touched.
- No secrets, credentials or environment files were created or added; `.env*` is
  git-ignored.
- The temporary `vite preview` server and headless Chrome were stopped after the
  checks; `playwright-core` was installed only under `/tmp/sa-browser/`, outside
  the application repository.

## 12. Owner next actions

1. Run the built app in a real Qortal host (Hub/dev mode) and confirm the shell
   renders, `_qdnBase` routing works, and the `qortal://APP/...` links behave.
2. Confirm or replace the banner WebP derivative and supply the final palette /
   typography set.
3. Authorize the next bounded issue (identity/owner detection against a validated
   host boundary) when ready.
4. Decide whether to commit the Phase 1B work (explicit authorization required).

## 13. Saved report

- Report type: implementation (Phase 1B)
- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/implementation/2026-09-11-phase-1b-appshell-implementation-report.md`
- File created: yes
