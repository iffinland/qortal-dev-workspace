# Shadow Archives — Responsive AppShell Specification and Design Tokens (Phase 1A)

- Project: `shadow-archives-webportal-QORTAL`
- Phase: 1A (specification only — **no CSS or components are built here**)
- Date: 2026-09-11
- Author: Codex (Phase 1A research)
- Status: implementation-ready specification derived from the owner layout
  decisions in
  [`../../../projects/shadow-archives-webportal.md`](../../../projects/shadow-archives-webportal.md).
  The UI dependency strategy — **no MUI; semantic CSS design tokens + in-repo
  components + inline SVG** — is **OWNER APPROVED (D6, 2026-09-11)**.
  Individual visual values (palette, motion durations, exact sizes) remain
  proposals.
- Related: [`./2026-09-11-phase-1a-architecture-report.md`](./2026-09-11-phase-1a-architecture-report.md),
  [`./2026-09-11-phase-1b-implementation-plan.md`](./2026-09-11-phase-1b-implementation-plan.md)

## 1. Approved home layout (owner decisions)

Desktop / large desktop / TV:

```text
┌───────────────────────────────────────────────────────────────────┐
│  TOP POSTS (~240px)   │  SHADOW ARCHIVES BANNER  │  TOP VIDEOS (~240px) │
├───────────────────────────────────────────────────────────────────┤
│        Q-TUBE   SUBWIRE   QUITTER   SEARCH   (~70% width)          │
├───────────────────────────────────────────────────────────────────┤
│        HOME   BLOG   VIDEOS   GALLERY   ABOUT   CONTACT            │
├───────────────────────────────────────────────────────────────────┤
│        LATEST POSTS (left)        │        LATEST VIDEOS (right)   │
├───────────────────────────────────────────────────────────────────┤
│        LATEST FROM THE GALLERY  — horizontal auto-scroll           │
├───────────────────────────────────────────────────────────────────┤
│        FOOTER (elevated from the page background)                  │
└───────────────────────────────────────────────────────────────────┘
```

`TOP POSTS` and `TOP VIDEOS` are ordered by like count, maximum 10 listed
items, no thumbnails, vertically auto-scrolling, each item clickable.

## 2. Breakpoints

| Token | Range | Class | Notes |
| ----- | ----- | ----- | ----- |
| `bp.xs` | < 480px | small phone (portrait) | single column |
| `bp.sm` | 480–767px | phone landscape / small tablet | single column, wider cards |
| `bp.md` | 768–1023px | tablet | single column with 2-up card grids |
| `bp.lg` | 1024–1439px | laptop / small desktop | 3-panel header becomes viable |
| `bp.xl` | 1440–1919px | large desktop | target desktop layout, content ≈90vw |
| `bp.xxl` | ≥ 1920px | TV / very large display | max content width clamps, larger type/focus |

Content width rule (owner decision): main shell is **≈90vw** with a sensible
maximum.

| Token | Value (proposal) | Rationale |
| ----- | ---------------- | --------- |
| `layout.shellMax` | `1760px` | prevents uncontrolled width on ultrawide/TV while keeping ≈90vw on a 1440–1920 display |
| `layout.shellInline` | `5vw` (i.e. 90vw content) | owner decision |
| `layout.gutter` | 16 / 20 / 24 / 32px by breakpoint | rhythm |

**INFERENCE.** At 1440px, 90vw = 1296px, below the 1760px clamp, so `90vw`
dominates; above ~1955px the clamp takes over. This is the intended behaviour
(90vw on normal desktops, bounded on very large displays) and should be
confirmed visually in Phase 1B.

## 3. Shell structure (DOM order and semantics)

1. `header.site-header`
   - `section.top-posts` — `aria-label="Top posts by likes"`, `<nav>` list of up
     to 10 links.
   - `a.site-banner` — brand link to `/`; contains the brand image and the
     `SHADOW ARCHIVES` wordmark.
   - `section.top-videos` — `aria-label="Top videos by likes"`, same shape.
2. `nav.primary-actions` — Q-Tube, SubWire, Quitter (external Qortal apps) plus
   the Search control. Visually stronger than standard navigation.
3. `nav.site-nav` — Home, Blog, Videos, Gallery, About, Contact. Current route
   marked `aria-current="page"`.
4. `main` — route outlet; each route owns its own regions and skeletons.
5. `section.gallery-strip` — `LATEST FROM THE GALLERY`, horizontal auto-scroll.
6. `footer.site-footer` — elevated surface; archive metadata, link groups,
   provenance/version line.

Only the header, primary actions, site navigation and footer are part of the
persistent shell. `Latest Posts`, `Latest Videos` and the gallery strip are
home-route regions, not shell regions, so other routes are not forced to pay for
them.

## 4. Header behaviour by breakpoint

| Breakpoint | Behaviour |
| ---------- | --------- |
| `xl`, `xxl` | 3-panel: `240px | flexible banner | 240px`; banner height 300–340px; top panels auto-scroll vertically |
| `lg` | 3-panel retained; side panels 200px; banner 260–300px |
| `md` | banner first (200–260px); Top Posts and Top Videos become two side-by-side compact lists under the banner |
| `sm`, `xs` | banner first (clamped, ≈16:6 crop, target ≤200px); Top Posts and Top Videos become horizontal snap scrollers (one card per view), or compact 5-item lists |

Rules:

- The banner must **not** grow with the 16:9 source image. Use a fixed
  `aspect-ratio`-bounded box with `object-fit: cover` and a max height so the
  desktop header stays in the 300–340px band. `INFERENCE`: 300–340px is large
  but owner-approved; it is the reserve height for a 240px side-panel column
  plus padding.
- The banner region reserves its height before the image loads (fixed height or
  `aspect-ratio`) so there is no layout shift.
- On all breakpoints the brand wordmark stays legible; if the image fails to
  load, the textual `SHADOW ARCHIVES` mark is the fallback (never an empty box).

## 5. Auto-scroll behaviour (Top Posts, Top Videos, Gallery strip)

Implementation shape: a list rendered twice (original + `aria-hidden="true"`
duplicate) inside a clipped track, translated by a CSS animation; the duplicate
is removed from the accessibility tree and from tab order.

Pause rules (all must stop the animation, not merely slow it):

- `:hover` on the track;
- `:focus-within` on the track (keyboard users);
- user interaction: pointer/touch/scroll/wheel on the track pauses for a
  cooldown period (proposal: 3 s);
- document hidden (`document.visibilitychange`);
- **`prefers-reduced-motion: reduce` → animation disabled entirely**, replaced
  by a static, natively scrollable list;
- a user-visible pause control is not required by the owner, but if the item
  count exceeds the visible area the component must expose the full list via
  native scrolling so nothing is unreachable.

Accessibility rules:

- Items are real `<a>` elements in DOM order; auto-scroll never moves focus.
- Pausing must not require a mouse: focus alone pauses.
- The vertical panels must be keyboard-scrollable when reduced motion is set.
- The gallery strip sets `overflow-x: auto`, `scroll-snap-type: x proximity`,
  and visible scroll affordances; auto-scroll is an enhancement.
- No content may be reachable only through the animation.

Motion tokens (proposals): vertical panel duration 24–40 s per loop depending
on item count; gallery 45–70 s per loop; linear easing; no easing bounce.

## 6. Focus and hit-target rules (TV / D-pad)

- Minimum interactive target: 44 × 44 CSS px (`bp.xs`–`bp.lg`).
- TV (`bp.xxl`, and any TV-detected context): minimum 48 × 48 CSS px and a
  minimum 3px visible focus indicator with ≥3:1 contrast against both the
  surface and the accent.
- Focus indicator token: `2–3px` `outline` in `color.focus` plus a 2px offset;
  never `outline: none` without a replacement.
- Focus order follows DOM order: banner → primary actions → site navigation →
  main content → gallery strip → footer. The auto-scrolling panels are placed
  before the banner in DOM order and are fully keyboard traversable.
- Avoid hover-only affordances; every hover action has a focus equivalent.
- `:focus-visible` used for pointer-vs-keyboard differentiation.
- Skip link: "Skip to content" as the first focusable element.

## 7. Home body regions

- `Latest Posts` (left) / `Latest Videos` (right) on `lg`+ as a two-column
  layout; each column has an ordered list of clickable cards; posts show a
  thumbnail and short description; videos use video cards with a duration badge.
- `md` and below: sections stack vertically; cards become 1-up (`xs`/`sm`) or
  2-up (`md`) grids. **Mobile must not squeeze desktop columns.**
- `LATEST FROM THE GALLERY`: full-width horizontal strip of thumbnails; each
  tile is a fixed aspect-ratio box; clicking opens the gallery item.
- Card media: `loading="lazy"`, `decoding="async"`, explicit width/height or
  `aspect-ratio`, and an LQIP/solid placeholder. Video cards never request video
  bytes — poster/thumbnail only.

## 8. Loading skeletons and layout stability

- Skeleton components mirror the final box geometry:
  - Top Posts / Top Videos items: fixed row height (proposal 40–48px).
  - Banner: exactly the reserved header height for the breakpoint.
  - Post/video cards: reserved image box + 2 text lines + action row.
  - Gallery tiles: fixed aspect-ratio boxes.
- Skeletons render text-free but keep an accessible label
  (`aria-busy="true"`, `aria-label="Loading ..."`).
- Skeleton → content swap must not change container height (no jump).
- Empty, partial, unavailable and error states reuse the same reserved layout so
  they do not shift the page either.
- Target: no cumulative layout shift caused by media or counts arriving; any
  count that changes after load must update in place with a reserved width.

## 9. Visual design tokens (proposal)

Implemented as CSS custom properties on `:root` (and a future light variant if
the owner ever wants one; the brand direction is dark). Names are semantic; raw
palette values live behind them.

```css
:root {
  /* ---- palette (raw, not used directly in components) ---- */
  --sa-charcoal-900: #0e0f10;
  --sa-charcoal-800: #14161a;
  --sa-charcoal-700: #1b1e23;
  --sa-grey-600:    #2a2e35;
  --sa-grey-500:    #3d434d;
  --sa-grey-400:    #6b7280;
  --sa-parchment-200: #e8e2d4;
  --sa-parchment-100: #f2ede1;
  --sa-cream-50:    #f7f3e8;
  --sa-red-600:     #8f2b28;
  --sa-red-500:     #a63a34;
  --sa-green-600:   #3f6b4a;
  --sa-amber-500:   #b8862b;
  --sa-blue-600:    #2f5d7c;

  /* ---- semantic colour tokens ---- */
  --sa-color-bg:              var(--sa-charcoal-900);
  --sa-color-surface:         var(--sa-charcoal-800);
  --sa-color-surface-raised:  var(--sa-charcoal-700);
  --sa-color-surface-sunken:  var(--sa-charcoal-900);
  --sa-color-border:          var(--sa-grey-600);
  --sa-color-border-strong:   var(--sa-grey-500);
  --sa-color-text:            var(--sa-cream-50);
  --sa-color-text-muted:      #b9b2a3;
  --sa-color-text-inverted:   #14161a;
  --sa-color-accent:          var(--sa-red-600);
  --sa-color-accent-hover:    var(--sa-red-500);
  --sa-color-accent-contrast: var(--sa-cream-50);
  --sa-color-link:            var(--sa-parchment-200);
  --sa-color-success:         var(--sa-green-600);
  --sa-color-warning:         var(--sa-amber-500);
  --sa-color-danger:          var(--sa-red-500);
  --sa-color-info:            var(--sa-blue-600);
  --sa-color-focus:           #e0c46a;   /* high-contrast focus ring */
  --sa-color-overlay:         rgb(0 0 0 / 0.6);

  /* ---- elevation (restrained; borders do most of the work) ---- */
  --sa-shadow-0: none;
  --sa-shadow-1: 0 1px 2px rgb(0 0 0 / 0.35);
  --sa-shadow-2: 0 2px 6px rgb(0 0 0 / 0.40);
  --sa-shadow-3: 0 6px 18px rgb(0 0 0 / 0.45);
  --sa-shadow-inset-paper: inset 0 0 0 1px rgb(232 226 212 / 0.06);

  /* ---- radii ---- */
  --sa-radius-xs: 2px;
  --sa-radius-sm: 4px;
  --sa-radius-md: 6px;
  --sa-radius-lg: 10px;
  --sa-radius-pill: 999px;

  /* ---- spacing (4px base) ---- */
  --sa-space-1: 4px;   --sa-space-2: 8px;   --sa-space-3: 12px;
  --sa-space-4: 16px;  --sa-space-5: 20px;  --sa-space-6: 24px;
  --sa-space-8: 32px;  --sa-space-10: 40px; --sa-space-12: 48px;

  /* ---- typography ---- */
  --sa-font-display: "Shadow Archives Display", Georgia, "Times New Roman", serif;
  --sa-font-body: "Shadow Archives Text", system-ui, -apple-system, "Segoe UI", sans-serif;
  --sa-font-mono: ui-monospace, SFMono-Regular, Menlo, monospace;
  --sa-text-xs: 0.75rem;  --sa-text-sm: 0.875rem; --sa-text-base: 1rem;
  --sa-text-lg: 1.125rem; --sa-text-xl: 1.25rem;  --sa-text-2xl: 1.5rem;
  --sa-text-3xl: 1.875rem; --sa-text-display: clamp(1.75rem, 4vw, 3rem);
  --sa-leading-tight: 1.2; --sa-leading-normal: 1.5; --sa-leading-relaxed: 1.7;

  /* ---- layout ---- */
  --sa-shell-inline: 5vw;
  --sa-shell-max: 1760px;
  --sa-header-side: 240px;
  --sa-header-side-lg: 200px;
  --sa-header-height-xl: 320px;  /* inside the owner-approved 300–340px band */
  --sa-header-height-lg: 280px;
  --sa-header-height-md: 240px;
  --sa-header-height-sm: 190px;
  --sa-gallery-tile: 220px;

  /* ---- motion ---- */
  --sa-motion-fast: 120ms;
  --sa-motion-base: 200ms;
  --sa-motion-slow: 320ms;
  --sa-motion-easing: cubic-bezier(0.2, 0.7, 0.2, 1);
  --sa-marquee-vertical: 32s;
  --sa-marquee-gallery: 60s;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --sa-motion-fast: 0ms;
    --sa-motion-base: 0ms;
    --sa-motion-slow: 0ms;
    --sa-marquee-vertical: 0s;
    --sa-marquee-gallery: 0s;
  }
}
```

Notes on intent:

- Charcoal/black backgrounds, parchment/cream text, classified-document grey
  borders, one muted dark-red accent. No blue primary, no glassmorphism.
- Elevation is deliberately restrained: prefer a 1px border plus
  `--sa-shadow-1`/`--sa-shadow-inset-paper` over large blurred shadows.
- Focus colour is a warm parchment-gold, distinct from the red accent, so the
  focus ring never reads as a "danger" state.
- Danger and accent share the red family but remain distinct tokens; do not
  collapse them.
- Exact palette values are proposals and are expected to change once the owner's
  supplied brand image and typography are available. The **token names and
  semantic structure** are the durable part of this specification.

## 10. Typography and font loading

- Two families maximum: one display/serif-ish face for the banner and headings,
  one text face for body. Optional mono for metadata/provenance lines.
- Self-host fonts (CSP allows only `'self'` and `data:`). Subset to the Latin
  range used; ship at most two weights per family.
- `font-display: swap`; preload only the single face used above the fold
  (banner wordmark).
- **Do not** inherit the template's four Inter weights or q-tube's fourteen
  Roboto weights (see the performance comparison).

## 11. Responsive acceptance checks for Phase 1B

- 320px, 375px, 768px, 1024px, 1440px, 1920px, 2560px widths render without
  horizontal page scroll (except intentional galleries).
- Header height stays inside its reserved band at every breakpoint.
- Auto-scroll pauses on hover, focus, interaction and reduced motion; content is
  fully reachable with the animation disabled.
- All interactive targets meet 44px (48px TV) and show a visible focus ring.
- Skeleton → content produces no measurable layout shift.
- Mobile layout is a genuine reflow (stacked/scroll-snapped), not compressed
  desktop columns.
