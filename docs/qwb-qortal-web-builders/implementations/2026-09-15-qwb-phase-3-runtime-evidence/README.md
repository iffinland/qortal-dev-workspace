# QWB Phase 3 runtime evidence (browser harness, fake QDN node)

Produced 2026-09-15 by the **DeepSeek** agent as part of the Phase 3 implementation task
(`qwb-phase-3`). This is **client-side evidence only**: it proves that the shipped bundle
performs the documented QDN read/write sequence, verifies what the node serves before it
claims success, and leaves the visitor DOM unchanged. It does **not** prove owner-runtime
behaviour in a real Qortal host — that is the Phase 4 staging run.

## What was run

1. `npm run build` in `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`
   (`dist/assets/index-CLC6fuj3.js`, 126.57 kB).
2. `python3 qwb-phase-3-harness.py` — copies `dist/` to a scratch directory and produces two
   pages from the same `index.html`:
   - `owner.html`: the real app with a scripted QDN node injected as `window.qortalRequest`
     plus `_qdnName = 'Qortal Web Builders'`, seeded from the shipped seed bundle (the site
     singleton in `JSON`, articles in `DOCUMENT`), and a report script that drives the owner UI;
   - `visitor.html` / `visitor-report.html`: the same page **without** any bridge or `_qdn*`
     globals, i.e. a plain visitor.
3. `bash qwb-phase-3-run.sh` — serves the scratch directory on `127.0.0.1:8913` and dumps the
   DOM / takes full-page screenshots with headless Chrome.
4. `dump-seed-fixture.mjs` regenerates the fake node's seed fixture from the shipped seed
   (`npx vite-node dump-seed-fixture.mjs > /tmp/qwb-p3-seed.json`) so this evidence is
   reproducible without the app repository's test suite.

## What the evidence shows

`harness-report.json` (extracted from the owner page):

- owner mode is derived automatically — bar meta `WEBSITE · verified by name ownership`,
  17 inline controls, bar buttons `Hide owner tools / Publishing status / Reload content /
  Check last write / Re-check owner mode`;
- read path: `FETCH_QDN_RESOURCE` for `qwb_site_v1`, then one `SEARCH_QDN_RESOURCES` per kind
  with `prefix: true`, `mode: 'ALL'`, `exactMatchNames: true` and the kind's own service
  (`JSON` for five kinds, `DOCUMENT` for `qwb_post_`);
- highlight edit (kind `highlight`, service `JSON`): one publish carrying
  `name: "Qortal Web Builders"`, then a read-back; toast
  `"Harness published headline" was published and verified as revision 2`; the home page
  re-renders the new headline; the status dialog shows
  `Submitted to the host (availability: verified)` (no self-contradicting wording);
- article edit (kind `article`, service `DOCUMENT`): one publish with `service: DOCUMENT`,
  a read-back `FETCH_QDN_RESOURCE` with `service: DOCUMENT`, the form closed on verification
  and the posts index re-rendered the new title `Harness article headline`;
- `errors: []` — the app raised no unhandled error in either cycle.

`visitor-report.json` (plain visitor): `ownerBar: false`, `ownerControls: 0`,
`ownerClasses: 0`, `modalHost: false`, `toastHost: false`, `appHtmlLength: 23603`,
`appHtmlHash: -264186793` — byte-identical to the accepted Phase 2 baseline, and
`visitor-home-1440.png` has the same SHA-256 as the Phase 2 screenshot.

## Files

| File | What it is |
| --- | --- |
| `harness-report.json` | the owner page's structured report (read, highlight edit, article edit phases) |
| `visitor-report.json` | the visitor page's DOM identity report |
| `owner-dom.html` / `visitor-dom.html` | dumped DOM of both pages |
| `owner-home-1440.png` / `visitor-home-1440.png` | full-page screenshots at 1440 px |
| `qwb-phase-3-harness.py` / `qwb-phase-3-run.sh` | the harness and runner that produced the above |
| `dump-seed-fixture.mjs` | regenerates the fake node's fixture from the shipped seed |
| `SHA256SUMS.txt` | digests of every file above |

## Limits

- The "node" is a script, so this cannot show real network lag, real approval dialogs, real
  publish fees or real node-side validation. It also cannot show that another node serves the
  same revision.
- The visitor page has no bridge, so it exercises the documented "no bridge" seed fallback,
  not a published-content read.
