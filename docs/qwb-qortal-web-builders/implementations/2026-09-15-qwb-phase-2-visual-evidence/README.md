# QWB Phase 2 visual + structural evidence — qwb-qortal-web-builders/phase-2-20260915

Executing agent (producer of this evidence): **DeepSeek**
Report/handoff writer: same (`DeepSeek`)

Application revision under test: `agent/qwb/phase-2` @
`b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`, built with `npm run build` (Vite 8.3.0).

## What this evidence is, and what it is not

These images and reports come from a **headless-Chrome harness over the built `dist/`**, not from
Qortal Hub/Home. The harness loads the production bundle with the Core-injected globals
(`_qdnContext`, `_qdnService`, `_qdnName`, `_qdnIdentifier`, `_qdnTheme`, `_qdnLang`) and a stub
`window.qortalRequest` that answers `GET_USER_ACCOUNT` and `GET_ACCOUNT_NAMES` with two names
(`Q-Website`, `Qortal Web Builders`) in the audit-verified order. It proves the **client-side**
contract — owner recognition from the audited three-input model, the inline owner shell, the truthful
no-write wording, and visitor cleanliness — and it does **not** prove host behaviour. Owner-mode PASS
still requires the owner run described in `../2026-09-15-qwb-phase-2-implementation.md` §9.

## How the images and reports were produced

1. `npm run build` → `dist/` copied to `/tmp/qwb-check-3/`.
2. Harness pages generated from the built `index.html`:
   - `owner.html` — injects the render-context globals above plus the stub bridge (before the module
     script, exactly as Core injects them) and, at 700 ms, writes a JSON report into
     `<pre id="harness-report">`. `?form=1` clicks the first inline `✎`, `?sheet=1` clicks the owner-bar
     toggle, `?toast=1` clicks `Re-check owner mode`.
   - `visitor.html` — the built page with **no** Qortal globals and no injection at all.
   - `visitor-report.html` — as `visitor.html`, plus a structural report in
     `<pre id="visitor-report">`.
3. `python3 -m http.server 8913` and headless Chrome 153
   (`--headless=new --disable-gpu --no-sandbox --hide-scrollbars --force-device-scale-factor=1`,
   `--window-size=<w>,<h> --virtual-time-budget=8000 --screenshot`, `--dump-dom` for the reports).
4. No image was retouched, cropped or downscaled; screenshots are full-resolution viewport captures
   (1440×3200 and 390×2400) taken at the top of the page.

## Contents

| File | Shows |
| --- | --- |
| `01-owner-home-desktop-expanded-1440.png` | owner view at 1440 px: owner bar **expanded** (badge, name, `WEBSITE · verified by name ownership`, publishing status, unsaved-change line, `Publishing status`, `Re-check owner mode`, `Hide owner tools`), 17 inline control groups, 5 `+ Add …` rows, `+ Add pricing tier` on its own 68 px line instead of stretched to the pricing-box height |
| `02-owner-home-phone-collapsed-390.png` | owner view at 390 px: the bar is collapsed to its badge (mobile `§9.5`) |
| `03-owner-sheet-390.png` | the same bar after the badge toggle: the actions open as a sheet, actions ≥44 px |
| `04-owner-edit-modal-1440.png` | inline `✎` → pre-filled form from the seed model, `Save & publish` **disabled**, `Not saved (Phase 3 adds publishing)`, Phase-2 notice, `Validate draft` as the only enabled action |
| `05-visitor-home-1440.png` | visitor view at 1440 px — **byte-identical** (SHA-256 `28bc7fb7…4b62`, zero-pixel diff) to the same capture taken earlier on this branch, so the review fixes in §6 of the implementation report changed no visitor pixel. (The stronger claim that the owner layer adds *nothing* to a visitor is made in code by `tests/phase-2-visitor-baseline.test.ts`, which compares the live `#app` markup against the Phase 1 render output byte-for-byte.) |
| `06-visitor-home-390.png` | visitor view at 390 px |
| `harness-owner-1440.json` | owner structure report: `ownerBarExpanded: true`, `controls: 17`, `editButtons: 17`, `moveButtons: 28`, `deleteButtons: 14`, `addRows: 5`, `pricingAddRow` height 68 px / `flex-basis: 100%` / `align-self: flex-start` against a 634 px pricing box, `bridgeCalls: [GET_USER_ACCOUNT, GET_ACCOUNT_NAMES]`, `writeActions: []`, `documentTextHasClaim: false` |
| `harness-owner-1440-toast.json` | `Re-check owner mode` → toast `Owner mode confirmed: the current account owns "Qortal Web Builders".` and `toastClearsBar: true` (toast bottom 2888 ≤ bar top 2900) |
| `harness-owner-1440-edit-modal.json` | modal open, title `Edit featured card`, `saveDisabled: true`, Phase-2 notice text, no `PUBLISH_*` call |
| `harness-owner-390.json` / `…-sheet.json` | `ownerBarExpanded: false`, toggle `Show owner tools`, and `sheetOpenAfterClick: true` |
| `harness-visitor-1440.json` | `ownerBar: false`, `ownerControls: 0`, `ownerClasses: 0`, `modalHost: false`, `toastHost: false` |

`SHA256SUMS.txt` records the digest of every file in this directory.
