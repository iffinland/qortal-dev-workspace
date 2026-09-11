# Shadow Archives Webportal — Owner-Runtime Visual Correction Follow-Up (not a phase)

**Date:** 2026-09-11
**Type:** owner-runtime visual correction follow-up — **not a new development
phase**
**Application:**
`/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
**Project context:** `projects/shadow-archives-webportal.md`
**Baseline:** `1b099c1` ("Prepare Shadow Archives first QDN app release") plus
the earlier uncommitted owner-runtime visual correction.
**Owner authorization:** CSS/design-token adjustment, header/HTML colour-scheme
alignment, one provider comment, canonical project documentation, local
build/test/browser validation.
**Not authorized / not performed:** QDN publication, transactions, commit,
push, tag, next phase, content publishing, Q-Tube/SubWire integration,
engagement implementation, routing/QDN-read/auth/capability changes.

---

## 1. Objective and exit criterion

**Objective.** Move the UI from the still-too-dark archive look to a
parchment / archive-paper visual language led by the real banner artwork, while
keeping the muted dark-red action identity, the layout, the main navigation and
all behaviour unchanged.

**Exit criterion.** In a browser at 375 / 768 / 1440 / 1920 px the page reads as
one warm parchment document: light beige page, paper-sheet section panels,
light inner boxes, slightly darker beige heading strips, darker archival
borders, dark-ink readable text, stamped red action controls, link-free footer
and the six-link main navigation. All declared checks pass.

---

## 2. Banner palette evidence (source of truth)

Asset: `src/assets/banner-shadow-archives.webp` (1202×683, WebP). Read-only
ImageMagick/Pillow analysis at development time only; **no** runtime colour
dependency was added.

The owner's screenshot (`~/Pictures/sa-templates.png`) was used only as a
before/current-state reference. The banner is the brand source of truth.

**Light paper / glow range** (the new lead tones):

| Region | mean | median | p90 (lit paper) |
| --- | --- | --- | --- |
| central glow band around the figure | `#7b705a` | `#85755a` | `#f0e2bb` |
| central figure area | `#3f3c34` | `#141310` | `#efebcb` |
| left paper sheet | `#967d5e` | `#ac8f6c` | `#c7ad87` |
| right paper sheet | `#988162` | `#b89d76` | `#d1b994` |

**Supporting samples:** light beige glow beside the figure `#dac8a2`; side-paper
highlights `#b59a74` / `#b49c77`; sheet shadows / torn edges `#7a5e42` /
`#8c7355`; dark archival ink around the central bar `#4a433c`; whole-image mean
`#5e4f3e`.

**How the tokens are derived:** the page and inner-paper tones are drawn from
the lit paper range (`#c7ad87` → `#f0e2bb`), aging slightly toward the sheet
mean; the deeper tan comes from the sheet shadows and torn edges; text uses the
banner's dark ink; the accent keeps the dried-blood oxide reds
(`#4a2418` / `#6e2f22` / `#8a3f2c`). No blue/slate tone remains.

---

## 3. Token rework (`src/styles/tokens.css`)

The raw-palette → semantic → elevation architecture is preserved; the palette is
replaced, not nudged. New raw ramps: `--sa-paper-50…700` (aged paper, light →
deep tan), `--sa-rust-600/700/800` (archival edges), `--sa-ink-900…600` (dark
archival ink), `--sa-oxide-800…500` (stamped red), and warm status tones
(`--sa-olive-600`, `--sa-amber-700`, `--sa-sand-700`, `--sa-danger-600`).

| Semantic token | Before (dark) | After (parchment) |
| --- | --- | --- |
| `--sa-color-bg` | `#0e0c09` | `#d8c59c` (paper-400, page glow) |
| `--sa-color-surface` | `#241d17` | `#e2d2ab` (paper-300, paper sheet) |
| `--sa-color-surface-strip` (new) | — | `#cfb88c` (paper-500, heading strip) |
| `--sa-color-surface-sunken` | `#080706` | `#ece0c0` (paper-200, light inner box) |
| `--sa-color-surface-raised` | `#33291b` | `#f3ead4` (paper-100, raised card) |
| `--sa-color-surface-raised-hover` | `#3f3324` | `#f9f3e3` (paper-50) |
| `--sa-color-border` | `#4a3d2d` | `#66502f` (rust-700) |
| `--sa-color-border-strong` | `#6b563c` | `#52401f` (rust-800) |
| `--sa-color-text` | `#e6dcc2` | `#1f160b` (dark archival ink) |
| `--sa-color-text-muted` | `#b3a184` | `#4f3d20` (faded brown-grey) |
| `--sa-color-text-inverted` | `#17120d` | `#f3ead4` (light on dark overlay) |
| `--sa-color-accent` | `#6e2f22` | `#6e2f22` (unchanged oxide family) |
| `--sa-color-link` | `#e6dcc2` | `#6e2f22` (readable dark oxide) |
| `--sa-color-success` | `#8fa877` | `#3a4f24` |
| `--sa-color-warning` | `#d2a552` | `#6b4a0b` |
| `--sa-color-danger` | `#c96a52` | `#8c2c18` |
| `--sa-color-info` | `#c2b492` | `#564832` |
| `--sa-color-focus` | `#e6c982` | `#5a2415` (dark oxide, visible on paper) |
| `--sa-color-overlay` | `rgb(6 5 4 / .72)` | `rgb(31 22 11 / .72)` |
| shadows | dark, blur to 40px | warm brown, restrained (`rgb(74 52 26 / …)`) |
| `--sa-shadow-inset-paper` | dark top highlight | lit paper edge `rgb(255 251 240 / .65)` |

`--sa-color-surface-strip` is new; the removed cold/dark raw tokens
(`charcoal-*`, `grey-*`, `red-*`, `cream-*`, `blue-*`, `parchment-*`, old
`oxide-400`, `olive-500`, `amber-500`, `sand-400`) are gone. No undefined token
remains (verified by a defined-vs-used sweep).

---

## 4. Page background / section / inner-box changes

- **Page (`base.css`):** `color-scheme` is now `light`; the body background is a
  warm lit-beige glow resolving into deeper paper tan — no near-black and no
  pure white.
- **Large sections (`shell.css`, `content.css`):** header outer container,
  primary actions, site navigation, Latest Posts / Latest Videos / Latest from
  the Gallery, route panels and the footer all sit on `--sa-color-surface`
  (paper sheet) with `--sa-color-border-strong` and restrained warm elevation.
- **Inner boxes (`content.css`):** `.sa-empty` / `.sa-error` (including the
  "No ranked posts/videos yet" boxes and the Latest Posts / Latest Videos /
  Gallery empty states) are now solid `--sa-color-surface-sunken`
  (light parchment) with the dashed archival border; the studio panel is the
  same light paper. Cards, media frames, gallery fallbacks and rich-text
  containers use the same light family.
- **Heading strips:** `.sa-top-list__title` (TOP POSTS / TOP VIDEOS) uses
  `--sa-color-surface-strip` (slightly darker beige) with dark ink text.
  `.sa-section__header` (LATEST POSTS / LATEST VIDEOS / LATEST FROM THE
  GALLERY) received the same strip treatment for family consistency.
- **Cards / badges:** the media duration badge now uses
  `--sa-color-text-inverted` so light text stays readable on the dark overlay;
  skeleton shimmer now runs raised → strip → raised (no dark mid-band).

---

## 5. Borders / elevation / text contrast

- Borders use darker archival brown-beige: border `#66502f` and border-strong
  `#52401f`; contrast vs the light surfaces is ~3.5–8:1, so boxes separate
  clearly.
- Elevation stays visible via tonal steps (page `#d8c59c` → panel `#e2d2ab` →
  inner box `#ece0c0` → raised card `#f3ead4`), darker borders, restrained warm
  shadows and the subtle inset lit-paper edge. No glassmorphism, no large dark
  shadows.
- Text contrast (WCAG relative luminance, sampled pairs):

| Pair | Ratio |
| --- | --- |
| ink `#1f160b` on page / panel / strip | 10.5 / 11.9 / 8.7 |
| muted `#4f3d20` on page / panel / inner / raised | 6.1 / 7.0 / 7.9 / 8.7 |
| link/accent `#6e2f22` on page / panel | 5.9 / 6.9 |
| accent text `#f3ead4` on accent `#6e2f22` / hover `#8a3f2c` | 8.4 / 6.2 |
| success / warning / danger on inner paper | 5.9 / 6.1 / 6.4 |
| focus `#5a2415` on page / panel | ≥ 8 |

All sampled pairs meet or exceed 4.5:1 for text; the focus outline (with 2px
offset) is high-contrast on every light surface.

---

## 6. Action buttons / navigation / footer

- **Action buttons** (Q-Tube / SubWire / Quitter / Search) are functionally
  unchanged and remain the strongest controls: flat stamped oxide red with a
  darker edge, plus a light raised Search button. They read as stamped archival
  red controls on the lighter paper UI.
- **Main navigation** remains the six working links `HOME / BLOG / VIDEOS /
  GALLERY / ABOUT / CONTACT` (`SiteNav`, `aria-label="Site sections"`),
  restyled for the paper palette; the active link keeps its dark-red underline.
- **Footer** keeps the previous owner decision: `<footer>` only, no `a` /
  `Link` / `NavLink`, no `nav`, no external link, no repository URL. Content is
  the brand, a short description, `Decentralized on Qortal` and the text-only
  build provenance. Restyled onto the paper surface.

---

## 7. Visual validation (screenshots)

Built app served with `vite preview`; captured full-document at the required
widths through Chrome DevTools Protocol (viewport sized to the document,
explicit `img.decode()` wait, `captureBeyondViewport: false`). Local artifacts
(not committed): `/tmp/final-375.png`, `/tmp/final-768.png`,
`/tmp/final-1440.png`, `/tmp/final-1920.png` (document heights 2090 / 1804 /
1357 / 1376 px).

| Check | 375 | 768 | 1440 | 1920 |
| --- | --- | --- | --- | --- |
| page clearly belongs to the banner | ✅ | ✅ | ✅ | ✅ |
| main sections use paper-sheet tones | ✅ | ✅ | ✅ | ✅ |
| inner boxes no longer dark | ✅ | ✅ | ✅ | ✅ |
| TOP POSTS / TOP VIDEOS strips slightly darker beige | ✅ | ✅ | ✅ | ✅ |
| borders clearly separate surfaces | ✅ | ✅ | ✅ | ✅ |
| text readable (dark ink / muted / links) | ✅ | ✅ | ✅ | ✅ |
| footer link-free | ✅ | ✅ | ✅ | ✅ |
| main nav present with all six links | ✅ (wraps) | ✅ | ✅ | ✅ |

Internal routes `/videos`, `/gallery`, `/about`, `/blog` were also captured:
route panels render as paper panels with dark-ink headings and light empty
boxes. (Headless full-page capture intermittently drops decoded bitmaps; the
final captures were taken viewport-sized to the document with an explicit
decode wait, and all four report `banner-ready`.)

---

## 8. Test / regression results

| Command | Result |
| --- | --- |
| `npm run lint` | PASS |
| `npm run typecheck` | PASS |
| `npm test` | PASS — 32 files, 301 tests |
| `npm run build` | PASS (`tsc -b && vite build`); CSS 25.76 kB / gzip 5.01 kB |
| `npm run format:check` | PASS — all files match Prettier |
| `git diff --check` | clean |

Confirmed by the suite and by inspection: the main `SiteNav` exists with the
same six route links; the footer has no links; all 18 routes render; no
route/auth/read/capability logic was touched. No test needed changing for this
follow-up (the earlier correction's footer/nav assertions already cover the
unchanged expectations).

---

## 9. Files changed

Application repo (`QORTAL`) — this follow-up:

- `src/styles/tokens.css` — parchment/paper raw palette, revised semantic
  tokens (incl. new `--sa-color-surface-strip`), warm restrained elevation.
- `src/styles/base.css` — `color-scheme: light`, warm parchment page gradient.
- `src/styles/shell.css` — heading-strip token on TOP POSTS / TOP VIDEOS,
  button hover, dark-ink strip text.
- `src/styles/content.css` — section heading strips, light solid inner boxes,
  light studio panel, badge text fix, warm skeleton shimmer.
- `index.html` — `color-scheme` meta `dark` → `light`.
- `src/app/providers/DesignTokensProvider.tsx` — comment updated to describe the
  single parchment-led theme (no behaviour change).

Pre-existing uncommitted changes from the earlier correction (untouched by this
follow-up, still present): `src/components/layout/SiteFooter.tsx`,
`src/components/layout/AppShell.test.tsx`.

Workspace repo (`qortal-dev-workspace`):

- `projects/shadow-archives-webportal.md` — recorded the clarified
  parchment/paper-led owner visual decision and the follow-up status.
- `docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-followup-report.md`
  — this report.

No UI framework, MUI, external font or runtime colour-extraction dependency was
added. CSS/design-token adjustment only.

---

## 10. Git status / commit / push state

- Application repo: branch `main`, HEAD `1b099c1`, **working tree modified** by
  the files in §9; no untracked files (a stray development-only ImageMagick
  probe artifact was removed).
- Workspace repo: `projects/shadow-archives-webportal.md` modified plus the
  untracked report files.
- **Not committed, not pushed, not tagged, not republished** (not authorized).

---

## 11. Self-audit (in-scope BLOCKER/HIGH)

| Check | Result |
| --- | --- |
| app still reads as a generic dark UI | **No** — page is light parchment |
| page background still too dark | **No** — `#d8c59c` warm lit beige |
| large section containers still too dark | **No** — paper-sheet tones |
| inner content boxes still dark | **No** — light parchment `#ece0c0` |
| text too light on light surfaces | **No** — dark archival ink, ≥4.5:1 |
| borders too weak to separate surfaces | **No** — darker archival borders |
| action buttons disconnected from the palette | **No** — stamped oxide red |
| footer still contains links | **No** — asserted by tests |
| main nav removed accidentally | **No** — six links asserted |
| readability degraded | **No** — contrast re-checked |
| route/auth/read logic regressed | **No** — 301 tests, routes render |
| glassmorphism / heavy shadows introduced | **No** |

No confirmed in-scope BLOCKER/HIGH finding remains.

---

## 12. Not done / not verified

- **Not verified in a real Qortal host.** The change is CSS-only and was
  validated locally (production build + headless Chrome at 375/768/1440/1920).
  Owner re-render/re-publication is required before the corrected visuals appear
  in Qortal; nothing was published.
- No QDN write, transaction, publication, commit, push or tag was performed.
- Screenshot capture note: headless full-page raster can drop the decoded banner
  bitmap; captures were taken viewport-sized to the document after an explicit
  `img.decode()` wait.
