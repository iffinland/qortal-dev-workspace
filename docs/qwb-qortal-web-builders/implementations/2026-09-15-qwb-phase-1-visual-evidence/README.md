# QWB Phase 1 visual evidence — qwb-qortal-web-builders/phase-0-1-20260915

Executing agent (producer of this evidence): **DeepSeek**
Report/handoff writer: same (`DeepSeek`)

Application revision under test: `agent/qwb/phase-0-1` (and `main`) @
`18d760d011e956829714e7489432949829fa1840`, built with `npm run build` (Vite 8.3.0).
Golden master (read-only, never modified):
`/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/-PUBLISHED-versioon`.

## How the images were produced

1. The golden master was **copied** to `/tmp/qwb-baseline/golden-src/`; the original was never served,
   built, formatted or written.
2. Both sites were captured through one identical harness (`/tmp/qwb-baseline/harness.html`): the
   target page is loaded in a same-origin iframe of a fixed pixel width, sweep-scrolled so every image
   is fetched and painted, returned to the top, then photographed with headless Chrome
   (`google-chrome --headless --window-size=<w>,<h> --virtual-time-budget=15000 --screenshot`).
   Golden master: `python3 -m http.server 4180`. New build: `vite preview` on 4173.
3. Region crops were taken from the full-page captures; the non-default tab panes were reached with a
   click harness (`index-tab2.html` in the golden copy, a selector-driven click page for the new build)
   because the golden master's tab strip relies on its un-initialised jQuery plugin.
4. Every comparison image is **golden master on the left, new build on the right**, separated by a
   10 px magenta rule. Nothing else was retouched; no image was cropped to hide a difference.

Full-page images (`01`, `07`, `08`, `09`) are uniformly downscaled for readability; the region crops
(`02`–`06`, `10`) are full-resolution pixels.

## Contents

| File | Compares |
| --- | --- |
| `01-home-desktop-full-1440.png` | home, full page, 1440 px |
| `02-navbar-and-hero-1440.png` | navbar lock-up + four links + gradient hero |
| `03-featured-pair-1440.png` | featured 4/6 pair straddling the gradient/band edge |
| `04-tab-strip-and-steps-1440.png` | centred tab strip, numbered step pills, illustration cards |
| `05-pricing-1440.png` | two-box pricing, emoji bullets, green order CTA |
| `06-contact-and-footer-1440.png` | alice-blue contact band, footer brand line, diagonal corner motif |
| `07-home-mobile-390.png` | home, full page, 390 px (authored mobile layout; the golden's own mobile
state could not engage in a real phone because the published pages have no `viewport` meta) |
| `08-works-desktop-full-1440.png` | completed-works page, full page, 1440 px |
| `09-article-detail-1440.png` | article detail, full page, 1440 px |
| `10-article-header-1440.png` | article page-header band at full resolution |
| `11-tab2-pane-new-only-1440.png` | new build, second tab pane (no faithful golden equivalent) |
| `12-article-index-new-only-1440.png` | new build article index (the published site had no listing page) |

`SHA256SUMS.txt` records the digest of every file in this directory.

Deviations visible in these images are the intentional ones listed in §5 of
`../2026-09-15-qwb-phase-0-1-implementation.md` (body type restored to 20 px sentence case,
self-hosted fonts, viewport meta, native tab/navbar behaviour, contrast corrections, new copy).
