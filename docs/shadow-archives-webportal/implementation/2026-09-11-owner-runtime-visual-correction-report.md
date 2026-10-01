# Shadow Archives Webportal — Owner-Runtime Visual Correction (not a phase)

**Date:** 2026-09-11
**Type:** owner-runtime correction (product/visual defect fix) — **not a new
development phase**
**Application:** `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
**Project context:** `projects/shadow-archives-webportal.md`
**Baseline:** `1b099c1` ("Prepare Shadow Archives first QDN app release"), clean
working tree
**Owner authorization:** CSS/design-token changes, footer component/layout,
affected tests, canonical project documentation, local build/test/browser
validation. **Not authorized** (and not performed): QDN publication,
transactions, commit, push, tag, next phase, content publishing,
Q-Tube/SubWire integration, engagement implementation.

---

## 1. Objective and exit criterion

**Objective.** Make the whole application visibly derived from and integrated
with the real Shadow Archives banner, and simplify the footer to a navigation-free,
external-link-free, repository-URL-free block.

**Exit criterion.** In a real browser, the banner, header panels, actions,
navigation, sections, cards and footer read as one warm archival composition;
major panels are visibly raised from the page background; the footer contains no
`a`/`Link`/`NavLink` elements and no repository URL; the main site navigation is
unchanged and functional; all declared checks pass.

---

## 2. Banner palette evidence (source of truth)

Asset: `src/assets/banner-shadow-archives.webp` (1202×683, WebP).
Read-only analysis with ImageMagick 6 and Pillow 11 (development-time only; no
runtime dependency added).

**Whole-image mean colour:** `#5d5040` — a warm brown, not a cold slate.

**Quantized dominant colours (16-colour median cut):**

| Colour | Share | Reading |
| --- | --- | --- |
| `#201d1a` | 8.1% | warm dark charcoal |
| `#1a1916` | 7.6% | warm near-black |
| `#c4ad89` | 7.5% | aged cream / parchment |
| `#9c7f5f` | 7.2% | faded paper grey-brown |
| `#13100e` | 6.7% | warm near-black |
| `#251e19` | 6.7% | warm dark charcoal |
| `#35261c` | 6.3% | warm brown mid |
| `#b99c76` | 6.2% | faded paper |
| `#513e2e` | 6.0% | dark rust brown |
| `#a89070` | 5.9% | faded paper |
| `#e4d9ba` | 5.5% | parchment / aged cream |
| `#0f0906` | 4.1% | deepest warm black |

**Red-dominant (dried-blood/oxide) pixels** (r≫g, g≈b): `#402018`, `#381810`,
`#482820`, `#503028`, `#503020` — muted, dark, desaturated; there is **no**
bright or pure red anywhere in the artwork.

**Warm-highlight pixels:** `#c0a070`, `#e0d0b0`, `#f0e0c0` — the banner's gold /
lit-paper tones.

**Region means:** left edge `#8e7354`, right edge `#927a5c`, top strip `#3f3127`,
bottom strip `#4b3e31`. Every region is warm.

**Conclusion used for the tokens:** the banner is a warm sepia/parchment
composition over warm black. The new palette samples its dark range (page,
surface, raised), its paper range (text, muted text), and its oxide-red range
(accent), plus the banner gold for focus. No dominant blue was introduced.

---

## 3. Semantic token changes (`src/styles/tokens.css`)

The raw-palette → semantic → elevation architecture is preserved. The provisional
cold palette was **replaced**, not nudged.

### 3.1 Raw palette

| Slot | Before | After |
| --- | --- | --- |
| deepest black | `#0e0f10` (charcoal-900) | `#080706` (ink-950) |
| page black | `#0e0f10` | `#0e0c09` (ink-900) |
| surface | `#14161a` | `#241d17` (ink-800) |
| raised | `#1b1e23` | `#33291b` (ink-700) |
| raised hover | — | `#3f3324` (ink-600) |
| document edge | `#2a2e35` (grey-600) | `#4a3d2d` (rust-700) |
| strong edge | `#3d434d` (grey-500) | `#6b563c` (rust-600) |
| text | `#f7f3e8` (cream-50) | `#e6dcc2` (parchment-200) |
| muted text | `#b9b2a3` | `#b3a184` (parchment-400) |
| accent | `#8f2b28` (red-600) | `#6e2f22` (oxide-600) |
| accent hover | `#ad3a35` (red-500) | `#8a3f2c` (oxide-500) |
| accent edge | — | `#4a2418` (oxide-700) |
| danger | `#ad3a35` | `#c96a52` (oxide-400, warm) |
| success | `#3f6b4a` | `#8fa877` (olive-500, warm-archival) |
| warning | `#b8862b` | `#d2a552` (amber-500) |
| info | `#2f5d7c` (**blue — removed**) | `#c2b492` (sand-400, warm neutral) |
| focus | `#e0c46a` | `#e6c982` (banner gold) |

Cold grey ramps (`charcoal-*`, `grey-*`) and the blue info token are gone.
`--sa-grey-500` was the only raw token referenced by a component; it was replaced
by the semantic `--sa-color-border-strong` in the skeleton shimmer.

### 3.2 Semantic layer

| Semantic token | Before | After |
| --- | --- | --- |
| `--sa-color-bg` | `#0e0f10` | `#0e0c09` |
| `--sa-color-surface` | `#14161a` | `#241d17` |
| `--sa-color-surface-raised` | `#1b1e23` | `#33291b` |
| `--sa-color-surface-raised-hover` | — (new) | `#3f3324` |
| `--sa-color-surface-sunken` | `#0b0c0e` | `#080706` |
| `--sa-color-border` | `#2a2e35` | `#4a3d2d` |
| `--sa-color-border-strong` | `#3d434d` | `#6b563c` |
| `--sa-color-text` | `#f7f3e8` | `#e6dcc2` |
| `--sa-color-text-muted` | `#b9b2a3` | `#b3a184` |
| `--sa-color-text-inverted` | `#14161a` | `#17120d` |
| `--sa-color-accent` | `#8f2b28` | `#6e2f22` |
| `--sa-color-accent-hover` | `#ad3a35` | `#8a3f2c` |
| `--sa-color-accent-strong` | — (new) | `#4a2418` |
| `--sa-color-accent-contrast` | `#f7f3e8` | `#f2e9d2` |
| `--sa-color-link` | `#e8e2d4` | `#e6dcc2` |
| `--sa-color-success` | `#3f6b4a` | `#8fa877` |
| `--sa-color-warning` | `#b8862b` | `#d2a552` |
| `--sa-color-danger` | `#ad3a35` | `#c96a52` |
| `--sa-color-info` | `#2f5d7c` (blue) | `#c2b492` (warm) |
| `--sa-color-focus` | `#e0c46a` | `#e6c982` |
| `--sa-color-overlay` | `rgb(0 0 0 / .6)` | `rgb(6 5 4 / .72)` (warm) |

Components consume only semantic tokens; after this change no raw-palette token
is referenced outside `tokens.css` (verified with `rg`).

---

## 4. Elevation / shadow changes

### 4.1 Shadow tokens

| Token | Before | After |
| --- | --- | --- |
| `--sa-shadow-1` | `0 1px 2px rgb(0 0 0/.35)` | `0 1px 2px rgb(3 2 1/.5), 0 2px 5px rgb(3 2 1/.35)` |
| `--sa-shadow-2` | `0 2px 6px rgb(0 0 0/.4)` | `0 3px 8px rgb(3 2 1/.55), 0 10px 22px rgb(3 2 1/.4)` |
| `--sa-shadow-3` | `0 6px 18px rgb(0 0 0/.45)` | `0 6px 16px rgb(3 2 1/.6), 0 18px 40px rgb(3 2 1/.45)` |
| `--sa-shadow-inset-paper` | `inset 0 0 0 1px rgb(232 226 212/.06)` | `inset 0 1px 0 rgb(242 233 210/.09), inset 0 0 0 1px rgb(242 233 210/.03)` |

Shadows are warm-toned (near-black `rgb(3 2 1)`) and layered, not a single large
blur. Because a drop shadow alone is nearly invisible on a near-black page, every
raised panel also carries `--sa-shadow-inset-paper`, which now produces a warm 1px
**top edge highlight** — the "paper lifted off a dark desk" read. Tonal contrast
between `bg / surface / raised` was also increased so separation survives without
the shadow (normal-mode luminance ratios: surface/bg 1.18, raised/surface 1.17,
raised/bg 1.37).

### 4.2 Panel assignments (`shell.css`, `content.css`)

| Region | Before | After |
| --- | --- | --- |
| site header container | shadow-2, border | **shadow-3**, border-strong |
| banner frame | inset only | **+ shadow-2** (framed plate) |
| Top Posts / Top Videos | shadow-1 | **shadow-2** |
| primary action row | shadow-2 | shadow-2, **border-strong** |
| main site nav | shadow-1 | **shadow-2**, **border-strong** |
| Latest Posts / Videos / Gallery sections | shadow-2 | shadow-2, **border-strong** |
| route / page panel | shadow-2 | **shadow-3**, border-strong |
| cards | shadow-1 | shadow-1 **+ inset-paper** |
| footer | shadow-2 | shadow-2, **border-strong** |

No glassmorphism (`backdrop-filter`) was introduced. No oversized SaaS blur.

---

## 5. Page background (`base.css`)

Replaced the generic blue-ish `#101113 → charcoal` gradient and the cold radial
with a banner-derived warm atmosphere: a faint parchment wash at the top
(`rgb(196 173 137 / .05)`), a faint oxide-red corner (`rgb(74 36 24 / .08)`), and
a warm-black vertical gradient `#17130f → #0e0c09 → #080706`. Quiet enough for
text; no blue/purple gradient, no neon, no synthetic radial glow.

---

## 6. Primary actions and navigation

- **Primary actions (Q-Tube / SubWire / Quitter / Search)** remain visually
  stronger than normal navigation: flat deep oxide-red pills, a darker stamped
  edge and a faint top light — deliberately not a shiny bright-red SaaS CTA.
  Destinations are unchanged (`qortal://APP/<name>`), search behaviour unchanged.
- **Main site navigation is unchanged and fully functional:**
  `HOME / BLOG / VIDEOS / GALLERY / ABOUT / CONTACT`. Only its styling moved to
  the corrected palette (border-strong, shadow-2, warm hover, oxide active
  underline). `NavLink` still sets `aria-current="page"`.

---

## 7. Footer change (`SiteFooter.tsx`)

**Before:** three-column footer with a "Sections" `<nav>` containing Home, Blog,
Videos, Gallery, About, Contact; a "Provenance" column with the QDN service,
build id, and the visible GitHub repository URL.

**After:** compact two-part footer, **text only**:

- brand: `SHADOW ARCHIVES` + short project description;
- meta: `Decentralized on Qortal` + `Build v0.1.0 · 1b099c1`.

No `<nav>`, no `Link`/`NavLink`/`<a>`, no Web2 URL, no repository URL, no
Q-Tube/SubWire/Quitter links. Desktop layout is `brand | meta` (meta right
aligned); mobile stacks. The `<footer>` landmark (contentinfo) is preserved.
`siteConfig.repositoryUrl` remains defined in config for provenance tooling but
is no longer rendered anywhere.

---

## 8. Verification

### 8.1 Automated (all green, application repo)

| Command | Result |
| --- | --- |
| `npm run lint` | PASS |
| `npm run typecheck` | PASS |
| `npm test` | PASS — 32 files / **301** tests |
| `npm run build` | PASS (vite 7.3.6, 145 modules) |
| `npm run format:check` | PASS |
| `git diff --check` | PASS (clean) |

New/updated tests in `src/components/layout/AppShell.test.tsx`:

- main SiteNav still contains Home/Blog/Videos/Gallery/About/Contact;
- footer has **zero** links, no `navigation` role, no `<a>`, no `github.com`, no
  `Sections`, and still shows `Decentralized on Qortal` + the build id.

`routes.test.tsx` (all 18 routes, including the legacy gallery redirect and
`/studio`) still passes — no routing regression.

### 8.2 Browser screenshots inspected

Production build served with `vite preview`; full-page PNG captured through the
Chrome DevTools Protocol (Chrome 153 headless) at exact widths.

After (this change): `/tmp/after-375.png` (375×2064), `/tmp/after-768.png`
(768×1769), `/tmp/after-1440.png` (1440×1331), `/tmp/after-1920.png`
(1920×1350), plus route panels `/tmp/route-blog-1440.png`,
`/tmp/route-contact-1440.png`, `/tmp/route-about-375.png`.

Before (HEAD `1b099c1`, built in a temporary detached worktree, same harness):
`/tmp/before-375.png`, `/tmp/before-768.png`, `/tmp/before-1440.png`,
`/tmp/before-1920.png`.

Inspected results:

- the banner now belongs to the page — the warm parchment/cream/oxide tones of
  the artwork are the same family as the header, surfaces, borders and background;
- in the **before** capture the shell read as cold blue-slate and the banner
  looked dropped into an unrelated dark template; the **after** capture is a
  single warm archival composition;
- Top Posts/Top Videos, the action row, the nav, Latest Posts/Videos/Gallery and
  the route panel are each visibly raised from the page background, with a warm
  edge highlight; cards/empty-state boxes read as lifted file cards;
- the footer is minimal, has no columns of links, and no repository URL;
- mobile (375) and tablet (768) stack correctly with no empty footer column.

These screenshots are local validation artifacts (not committed).

### 8.3 Accessibility

Contrast re-checked (WCAG relative luminance):

- body text `#e6dcc2` on surface `#241d17` = **12.4:1**; muted `#b3a184` = 6.7:1;
- accent button text `#f2e9d2` on accent `#6e2f22` = **8.3:1**;
- focus gold `#e6c982` on surface = 10.7:1;
- danger `#c96a52` = 4.65:1, warning `#d2a552` = 7.6:1, success `#8fa877` = 6.6:1,
  info `#c2b492` = 8.4:1.

All ≥44px hit targets, the visible `:focus-visible` outline, `prefers-reduced-motion`
handling, keyboard operation and the semantic `<footer>`/`<nav>` landmarks are
unchanged.

---

## 9. Bundle-size change

Measured production build, same toolchain (before = HEAD `1b099c1` rebuilt in a
temporary worktree; after = working tree):

| Asset | Before (raw / gzip) | After (raw / gzip) | Delta (raw / gzip) |
| --- | --- | --- | --- |
| CSS `index-*.css` | 25 243 B / 4 911 B | 25 580 B / 5 018 B | **+337 B / +107 B** |
| entry JS `index-*.js` | 383 959 B / 120 382 B | 383 082 B / 120 222 B | **−877 B / −160 B** |

Net gzip change ≈ **−53 B**. No dependency was added; no UI framework, no MUI,
no external font, no runtime colour-analysis package. The only JS change is the
smaller footer component.

---

## 10. Files changed

Application repo (`QORTAL`):

- `src/styles/tokens.css` — banner-derived raw palette, new semantic tokens
  (`surface-raised-hover`, `accent-strong`), stronger elevation tokens.
- `src/styles/base.css` — warm banner-derived page background.
- `src/styles/shell.css` — header/banner/panels/nav/action-row elevation,
  stamped archival action buttons, reworked link-free footer styling.
- `src/styles/content.css` — section/route/card elevation, warm skeleton shimmer.
- `src/components/layout/SiteFooter.tsx` — minimal, link-free footer.
- `src/components/layout/AppShell.test.tsx` — footer and navigation assertions.

Workspace repo (`qortal-dev-workspace`):

- `projects/shadow-archives-webportal.md` — recorded the two owner decisions and
  the owner-runtime status (see §11).

---

## 11. Workspace documentation change

`projects/shadow-archives-webportal.md` now records:

- **OWNER DECISION:** the visual palette is derived from the actual banner
  artwork, not from generic dark-app defaults;
- **OWNER DECISION:** major panels/sections must have clearly visible elevation
  from the page background;
- **OWNER DECISION:** the footer contains no navigation links, no external links
  and no repository URL; the primary site navigation is unchanged;
- the repository/HEAD baseline is corrected to `1b099c1`;
- a Current-state note that the owner reports the APP published and
  runtime-tested, plus the uncommitted visual-correction status.

---

## 12. Git status / commit / push state

- Application repo: branch `main`, HEAD `1b099c1`, **working tree modified** by
  the six files in §10; no untracked files; `dist/` remains ignored.
- **Not committed, not pushed, not tagged** (not authorized).
- **Not republished** (not authorized). The task is a local correction only.
- Temporary validation worktree `/tmp/sa-before` was removed; no stray worktrees
  remain (`git worktree list` shows only the main tree).

---

## 13. Self-audit (in-scope BLOCKER/HIGH)

| Check | Result |
| --- | --- |
| generic blue/slate palette still dominating | **No** — no blue token remains; `info` is warm |
| banner still visually disconnected from shell | **No** — verified in after-screenshots |
| raised surfaces indistinguishable from background | **No** — tonal contrast + border-strong + inset highlight + shadow |
| shadows invisible on dark background | **No** — layered shadows + paper edge highlight |
| excessive / shiny shadows | **No** — max blur 40px at 0.45, warm-toned |
| glassmorphism introduced | **No** — no `backdrop-filter` |
| action buttons look like generic red SaaS CTAs | **No** — flat oxide red with stamped edge |
| footer still contains `Link`/`NavLink`/`a` | **No** — asserted in tests |
| footer still contains repository URL | **No** — `github.com` absent; asserted in tests |
| main SiteNav removed or changed | **No** — six links intact; asserted in tests |
| text contrast degraded | **No** — all sampled pairs ≥ 4.5:1 |
| focus visibility degraded | **No** — gold outline, 10.7:1 |
| mobile footer has empty columns | **No** — two-part stack |
| route/read/auth regressions | **No** — 301 tests + all 18 routes pass |

No confirmed in-scope BLOCKER/HIGH finding remains.

---

## 14. Not done / not verified

- **Not verified in a real Qortal host:** the visual change is CSS-only and the
  owner has already runtime-tested the published build, but this specific
  correction was validated locally (preview server + headless Chrome), not on the
  real host. Owner re-publication/re-render is required before the corrected
  visuals appear in Qortal.
- No QDN write, transaction, publication, commit, push or tag was performed.
