# QWB visual golden-master map — qwb-qortal-web-builders/architecture-audit-20260915

Executing agent (registered role of the agent that actually produced this work): `DeepSeek`
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence: analysis, measurements and rendering were produced by the DeepSeek
model through the local Codex CLI profile (the profile is not the executor).
Report type: visual preservation map (implementation input; read-only audit)
Source of truth: `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/-PUBLISHED-versioon`
(immutable, verified byte-identical after the audit)
Rendered with: headless Chrome 153.0.8010.36, 1440 px and 390 px windows, `file://`
Screenshots used for this map live outside the repository: `/tmp/qwb-audit-shots/`
(`index-full-1440.png`, `index-1440.png`, `index-mobile-390.png`, `completed-works.png`,
`order-reception-and-planning.png`, `tab-completed-works.png`)

**Purpose.** Give the implementation agent a specification detailed enough to rebuild the site
in a new stack without re-deriving the design, while distinguishing what must survive from
what may legitimately change. This is a *map*, not a pixel lock.

---

## 1. Global design system

```css
/* Identity tokens — preserve verbatim */
--primary-color:            #13547a;   /* deep teal-blue: headings accents, buttons hover, h6 */
--secondary-color:          #80d0c7;   /* aquamarine: section fills, buttons, footer accent   */
--section-bg-color:         #f0f8ff;   /* alice blue: alternating section background          */
--custom-btn-bg-color:      #80d0c7;
--custom-btn-bg-hover-color:#13547a;
--border-color:             #7fffd4;   /* aquamarine accent border                            */
--p-color:                  #717275;   /* intended body text grey                             */
--dark-color:               #000000;
/* accent colours actually used by badges/buttons */
#28a745 order button · #54CA8B stat-completed · #FAC20A stat-progress · #00B0FF/#00BFA6/#F50057/#536DFE/#F9A826 category badges
/* geometry */
--border-radius-large: 100px;  --border-radius-medium: 20px;  --border-radius-small: 10px;
/* the signature gradient (15 degrees, primary -> secondary) */
background-image: linear-gradient(15deg, #13547a 0%, #80d0c7 100%);
```

Type scale (desktop → ≤991 px → ≤480 px): `h1 58/48/36`, `h2 46/36/28`, `h3 32/32/26`,
`h4 28/28/22`, `h5 24/20/20`, `h6 22/18/-`, `p 20`, menu 14, button 18, copyright 16.
Intended families: titles `'Montserrat'`, body `'Open Sans'` (neither loaded today).

Layout substrate: Bootstrap 5.2.2 grid (`container`, `row`, `col-lg-*`), max content width
1140 px at `lg`; `.section-padding` = 100 px vertical (50 px ≤991 px).

Vertical rhythm of the home page: hero (150 px padding each side) → featured band (pull-up
row) → white section with 100 px padding → pricing (100 px) → alice-blue contact section
(100 px) → footer.

## 2. Navbar (all pages)

- Transparent background; 1 px bottom border `rgba(128,208,199,.35)`; `z-index: 9`; sits on top
  of the gradient band so the gradient continues behind it.
- Left: brand = logo image 70×70 (`images/qwb-icon-trans-192x192.png`, transparent PNG of the
  circular "QWB" mark) + wordmark text at `h3` size (32 px) in bold.
- Right: 4 links (14 px, `Montserrat`, 500) — Home, Browse Topics, Prices, Contact.
- ≤991 px: background becomes `--secondary-color`; a burger toggler appears; the collapse
  panel shows the links stacked.
- Scroll-spy adds `.active`/`.inactive` classes to nav links as sections pass.
- Sticky behaviour: the theme ships `.sticky-wrapper.is-sticky .navbar { background:
  var(--secondary-color) }` — in the published build the plugin is never initialised, so the
  navbar is effectively static.
- **Must survive**: transparency over the gradient, the logo+wordmark lock-up, 4-link set,
  aquamarine mobile background.
- **May modernize**: sticky behaviour with a proper scrolled state (this is what the theme
  clearly intended), real anchor targets, accessible toggler, wordmark wrapping on small screens.

## 3. Hero (`index.html` `#section_1`)

- `.hero-section`: 15° gradient background, 150 px top and bottom padding, `overflow: hidden`,
  flex-centred content.
- Content column `col-lg-8` centred: `<h1>` white, bold, centred, 58 px ("Welcome to Qortal Web
  Builders website 🤗"), then `<h6>` centred in `--primary-color`, 22 px, max ~2 lines
  ("We craft unique websites that fuse modern design with a nostalgic twist…").
- No buttons, no image, no overlay — pure typographic hero on gradient.
- ≤991 px: h1 48 px, h6 18 px; ≤480 px: h1 36 px; 150 px padding retained.
- **Must survive**: full-width gradient band, white centred h1, coloured subtitle, generous
  vertical space, emoji as part of the headline (a genuine brand quirk — keep or deliberately
  drop, owner's call).
- **May modernize**: an optional background texture/illustration layer behind the gradient
  (the current build has none); a CTA row would change the character, so treat as a
  brand decision, not a default.
- **Becomes**: the `[ Edit hero ]` owner surface (heading, subtitle, optional background image).

## 4. Page header band (articles + `completed-works.html`)

- `.site-header`: same 15° gradient, `padding-top: 150px`, `padding-bottom: 80px`
  (`.topics-listing-page .site-header` → 65 px).
- Left column: white breadcrumb ("Homepage / Order reception and planning", 14 px), then
  `<h2>` white bold ("Website building / step by step", with an explicit `<br>`), then optional
  body copy in white.
- Right column (`col-lg-5`, gallery page): an illustration inside a white rounded card
  (20 px radius) that visually overhangs the gradient band; on the article pages a browser
  illustration (`undraw_Remote_design_team_re_urdx.png`) sits in a white card.
- Known defect to fix while rebuilding: the illustration card overflows the gradient band on
  article pages (the band's padding is shorter than the image column), producing a visible
  seam where the card overlaps white space.
- **Must survive**: gradient band + breadcrumb + white h2 + adjacent illustration card.
- **May modernize**: equalise band height so the card never overflows; allow taller headlines.

## 5. Featured pair (`index.html`, `.featured-section`)

- Band: `background-color: var(--secondary-color)` with `border-radius: 0 0 100px 100px`
  (80 px ≤991 px), `padding-bottom: 100px`.
- The `row` inside is pulled **up 100 px** over the band (`position: relative; bottom: 100px;
  margin-bottom: -100px`) so the cards straddle the gradient/band boundary — this overlap is a
  defining part of the composition.
- Card A (left, `col-lg-4`): white `.custom-block.shadow-lg`, 20 px radius, 30 px padding,
  `<h5>` black title with sparkle emoji, a two-item bullet list, a `<h6>` sub-question, then a
  centred aquamarine pill button "Learn More". Whole card is wrapped in an `<a>`.
- Card B (right, `col-lg-6`): `.custom-block.custom-block-overlay` (min-height 350 px, no
  padding) containing a white `<h5>`, three white bullet lines and a pill button, all
  absolutely positioned over a `.section-overlay` gradient at 85 % opacity, 20 px radius.
- Hover: cards lift 3 px and adopt the secondary-colour background.
- **Must survive**: the two-card asymmetry (4/6 columns), the pull-up overlap, the overlay card,
  the pill buttons.
- **May modernize**: replace `<li>`-outside-`<ul>` markup with real lists; make the whole-card
  link accessible (it currently swallows text selection and has no focus ring); keep hover
  effects but ensure contrast when the background swaps to `--secondary-color`.

## 6. Tab strip + three panes (`index.html` `#section_2`)

- White section, 100 px vertical padding (`section-padding`), centred `<h2>` "Browse Topics"
  (46 px, bold) with `mb-4`.
- Centred `nav-tabs`: three labels at 18 px (`Montserrat`, 500), 15×25 px padding, 1 px
  `#ecf3f2` bottom border on the strip, active tab indicated by a coloured underline/border.
  ≤991 px: labels shrink to 16 px, 10 px padding, and wrap on narrow screens.
- Panes:
  1. **Website Building Steps** — 3 white cards (`col-lg-4`), each: `<h5>` title, one-sentence
     description, a numbered pill (1/2/3) pinned right, and a full-width 200 px illustration
     (`object-fit: cover`) below.
  2. **Completed Works** — a stats pill ("Completed websites - 8", `.statcompleted` #54CA8B,
     12 px radius, `margin-right: 20px`) followed by 2 project cards (same card anatomy as §8)
     plus a "VIEW ALL OUR COMPLETED WORKS" pill button linking to `completed-works.html`.
  3. **Template Gallery** — one wide white card: `<h5>` title, a 4-item bullet list, and a
     centred pill button "CHECK OUT THE TEMPLATE GALLERIES" linking to `qortal://WEBSITE/HTML-web`.
- **Must survive**: centred tab strip, three-pane structure, card anatomy, the numbered pills,
  the aquamarine pill buttons.
- **May modernize**: tab semantics/ARIA; make the strip scrollable rather than wrapping on
  phones; treat each pane as a real content collection (steps / works / gallery) backed by data.

## 7. Process / step content (`order-reception-and-planning.html`)

- Gradient band + breadcrumb (see §4), then a white `section-padding` article column
  (`col-lg-8` centred): `<h3>` ("Order Reception and Planning", 32 px), a centred boxed intro
  (`blockquote` styling: alice-blue background, 10 px radius, `Montserrat` 28 px bold, 30–40 px
  padding), an 8-item bullet list of process steps with links to the Qortal group/Q-Mail, then a
  large centred quote box containing a white/amber highlighted call to action.
- **Must survive**: centred reading column, boxed intro, quote block, step list with inline
  Qortal links.
- **May modernize**: convert the two "boxed" blocks into explicit, reusable callout components;
  fix heading hierarchy (no `h1` today); real link styling for the amber CTA.

## 8. Portfolio / completed works (`.completed-works.html` and the second tab)

- Grid: `col-lg-4 col-md-6 col-12`, 8 cards, 3 columns on desktop, 2 at `md`, 1 on mobile.
- Card anatomy: white `.custom-block.shadow-lg`, 20 px radius, 30 px padding; `<h5>` project
  title (24 px, may wrap to 2 lines), a small `<p>` provenance line
  ("Builded To HTML Template" / "Builted Using Publii CMS" — sic, to be rewritten), a
  full-width 200 px preview image with `object-fit: cover` and `margin-top: 35px`, then a
  full-width aquamarine pill button "Watch live website" that links to the live
  `qortal://WEBSITE/...` resource. Some cards wrap everything in an `<a>` to the target, others
  put the button outside the anchor.
- Home tab variant of the same card adds the numbered/stat pill and uses the same image slot.
- **Must survive**: 3/2/1 responsive grid, card anatomy, preview image ratio treatment
  (full-width, cropped to 200 px), aquamarine pill CTA, one QDN target per project.
- **May modernize**: unify the two card variants into one component with optional badge; make
  the image ratio consistent (`object-fit: cover` at a fixed aspect-ratio box rather than a
  fixed 200 px height); move previews to QDN-managed media (they are 74 % of today's payload).

## 9. Pricing (`index.html` `#section_3`)

- White section, `section-padding`, centred `<h2>` (46 px) "The Perfect Web Solution for Your &
  Business!" (inline `style="text-align:center"`).
- `.pricing-container`: flex, wrap, centred, 20 px gap.
- `.pricing-box`: `flex: 1 1 300px`, `max-width: 400px`, 2 px `#ddd` border, 10 px radius,
  `#f9f9f9` background, soft `2px 2px 10px rgba(0,0,0,.1)` shadow, 20 px padding.
- Box contents: 5 lines, each an emoji `<span class="icon">` (18 px, 8 px right margin) plus
  text (15 px, capitalised due to the CSS leak), then a green `.order-btn`
  (#28a745, 5 px radius, 10/20 px padding, white 1.2em text) linking to
  `qortal://APP/Q-Shop/Qortal%20Web%20Builders/q-store-general-qortal-web-builders`.
- **Must survive**: two-box pricing row, light boxed treatment with thin border + soft shadow,
  emoji-icon bullet lines, single green order CTA per box.
- **Must modernize**: the boxes are currently flat `<div>`s inside a `<section>` that is nested
  incorrectly (an extra `</section>`), the buttons are unstyled anchors with no hover/focus
  state, and the capitalisation artefact must not be carried forward — restore sentence case.
- **Design note**: this is the clearest place where the *service* positioning must change:
  the copy today sells "HTML template + 123 QORT", the refreshed site must sell custom
  design/development. The layout can stay; the message must not.

## 10. Contact (`index.html` `#section_5`)

- `section-padding section-bg` → alice-blue `#f0f8ff` background, centred `<h2>` "Get in touch"
  (46 px) with `mb-5`.
- Two `col-lg-3` blocks (pushed apart by `ms-auto`/`mx-auto`), each a small heading, a `<hr>`,
  then label/value rows: "Let's chat! / Q-Mail → click to open apps" (link
  `qortal://APP/Q-Mail/to/Qortal20Web%20Builders`), "PM to → qortal web builders" (group link),
  and "Join the LIVE Chat & Forum / Group name / Group ID 745" with group links. Values are
  aquamarine (`--secondary-color`, 16 px).
- **Must survive**: quiet two-column info layout on the alice-blue band, aquamarine link values,
  `qortal://` deep links as the contact mechanism.
- **May modernize**: keep the layout but back it with editable content fields; make the two
  columns visually balanced (the left column is `ms-auto`, the right `mx-auto`, giving an
  off-centre look on wide screens); consider a real contact form later only if the owner
  accepts Qortal private-chat submission semantics (out of scope here).

## 11. Footer (all pages)

- `.site-footer`: `section-padding` (100/50 px) with `border-bottom: 10px solid
  var(--secondary-color)` and a **diagonal corner ornament** drawn with a zero-size `::after`
  element (`border-width: 0 0 200px 200px`, aquamarine) at the bottom-right of the page.
- Left column: logo (70×70) + "since 2025 | Qortal Web Builders" wordmark; an `<hr>`; then a
  single 14 px line in `#71D8CE` noting censorship-free QDN hosting, "does not use cookies",
  the design credit (self-referencing `qortal://WEBSITE/Qortal%20Web%20Builders`) and the
  template credit (`qortal://WEBSITE/HTML-web`, "QWBT-1").
- `.site-footer-link` values are aquamarine 16 px, `Montserrat` 500.
- **Must survive**: the 10 px aquamarine bottom border, the diagonal corner motif, the compact
  single-line credit row, the brand mark + "since …" line.
- **May modernize**: rewrite/reduce the credit line (the external `https://qortal.org` link is
  dead inside a Qortal host), replace `<span style="…">` with a styled element, and keep the
  motif as an SVG/CSS pseudo-element rather than a 200 px border hack if convenient.

## 12. Fixed scroll-to-top button

- `#myBtn`: red (#FF0000) block, fixed at bottom-right (20 px / 30 px), 15 px padding, 4 px
  radius, 18 px white text, `#555` on hover, hidden until `scrollTop > 20`.
- **Must survive**: the affordance exists today, so removing it would be a visible regression.
- **May modernize**: recolour to the identity (red is the only off-palette element on the page),
  add an accessible label, and implement it without the duplicated inline script.

## 13. Responsive character

| Breakpoint | Behaviour |
| --- | --- |
| ≥992 px | 3-column card grids; navbar links horizontal on a transparent bar; hero 58 px h1; section padding 100 px |
| 768–991 px | 2-column card grids; navbar turns aquamarine with a burger toggler; type scale reduced one step; `.section-padding` 50 px; featured band radius 80 px; tabs shrink |
| <768 px | single column; tabs wrap; pricing boxes stack (`flex: 1 1 300px`); card images keep 200 px height |
| <480 px | h1 36 px, h2 28 px, h3 26 px, h4 22 px |

**Defect to fix, not preserve**: no `viewport` meta on any page, so phones render the 980 px
layout zoomed out; the two breakpoints above never engage as authored on a real device. The
mobile *character* to preserve is: single column, hamburger navbar on aquamarine, stacked
pricing boxes, hero type reduced — not the zoomed-out desktop rendering.

## 14. Asset treatment and continuity cues

- The circular QWB mark (transparent PNG, 192×192) appears in navbar + footer at 70×70; the
  favicon set derives from the same mark (`favicon.svg`, `favicon.ico`, `favicon-96x96.png`,
  `apple-touch-icon.png`, plus 192/512 PWA icons).
- Illustrations are flat-colour unDraw PNGs; project previews are full-page screenshots with a
  consistent 16:9 framing.
- Continuity cues that make the site recognisable as *this* site: 15° teal gradient, aquamarine
  section fills and pill buttons, 100 px rounded section bottoms, 20 px rounded cards with soft
  shadows, alice-blue alternating band, white bold Montserrat-ish headlines, the diagonal
  footer corner, and the emoji-laden, informal Estonian-influenced English voice.
- **Brand-voice caution**: the copy is part of the current identity but the product positioning
  changes from "cheap HTML template" to "custom design/development". Preserve the *visual*
  language and the informal warmth; rewrite the message.

## 15. Preservation checklist for the implementation agent

Must survive (checkable on a screenshot diff):
1. 15° gradient `#13547a → #80d0c7` on hero and page headers.
2. Aquamarine `#80d0c7` section fills and 100 px rounded section bottom.
3. Alice-blue `#f0f8ff` contact band and the 10 px aquamarine footer border + diagonal corner.
4. 20 px card radius, soft large shadow, 3 px hover lift, 200 px cropped card image.
5. Centred tab strip with three content panes.
6. Two-box pricing row with emoji bullets and green order CTA.
7. Transparent navbar with logo + wordmark and four links.
8. Aquamarine pill buttons with primary-colour hover.
9. White bold centred headlines on gradient; generous 100 px section rhythm.
10. Single-column mobile with hamburger navigation.

May change (justified modernisation):
1. Self-hosted Montserrat/Open Sans (or deliberate system-sans) instead of unloadable webfonts.
2. Remove the global capitalisation/15 px body-text artefact → restore the intended 20 px,
   `#717275` body copy (this *will* look different: it is a correction, not a redesign).
3. Add `viewport` meta and make the existing breakpoints actually work on phones.
4. Replace jQuery/plugins with framework-native behaviour; delete dead sticky/timeline code.
5. Rebuild duplicated markup as shared components; single source of truth for nav/footer.
6. Recolour or restyle the red scroll-to-top button to fit the palette.
7. Fix the article-header illustration overflow and the invalid heading/markup nesting.
8. Replace unknown-provenance stock photos and the template preview screenshots with
   owner-provided or QDN-managed media.
9. Tighten contrast and add real focus states; keep the informal voice with rewritten copy.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-visual-preservation-map.md`
