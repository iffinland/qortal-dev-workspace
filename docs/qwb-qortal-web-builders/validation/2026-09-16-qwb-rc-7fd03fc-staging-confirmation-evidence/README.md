# QWB release candidate `7fd03fc` — bounded staging confirmation evidence (2026-09-16)

Artefacts from the **final bounded staging confirmation** of release candidate
`7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a`. The run published that build to the staging
resource `WEBSITE / Q-Website / default` and confirmed only the production-bootstrap fix
(`e7bf357`) introduced after the Phase 4 owner-runtime `PASS`. The full Phase 4 §14 owner-runtime
suite was **not** repeated.

Report: `../2026-09-16-qwb-rc-7fd03fc-staging-confirmation.md`.

## Result

**PASS.** Staging revision `WEBSITE / Q-Website / default` now serves the release candidate
byte-for-byte; the already published synthetic entities still render, the untouched shipped items
render beside them with their owner inline controls, a hard reload preserves both, and no
tombstoned item is resurrected.

`WEBSITE / Qortal Web Builders / default` was **not** written (metadata identical to the Phase 4
record).

## Publish

| Item | Value |
| --- | --- |
| Resource | `WEBSITE / Q-Website / default` |
| Signature (new revision) | `2egexP3JFzX5pkyVKkPrt9Pidcv9QWvcrvYoxCb8KDtmZa1iY76TUjd4CxLG128xUszoJV2rxKCmyza1gDFJ9sLd` |
| Previous signature | `5qU9BKTpZycWToRwuZrkjoJDahNwvRLf2Uq2uSYLZH8Tra2ovQSKPg3TGRJX6Cg12gLh1KKamHQx61YYwN4cgb4i` |
| Resource size | 880 368 B (`properties` 1 210 698 B, 3 chunks, `READY`) |
| Signer | `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` (owner of the `Q-Website` name) |
| Transaction | `ARBITRARY`, block 2 725 989, fee 0.01000000 QORT |

## File map

| File | Proves |
| --- | --- |
| `publish-invocation.json`, `publish-transaction.json` | exactly how the publish was issued from the Hub, the rejected first attempt, and the confirmed on-chain transaction |
| `staging-status-before.json`, `staging-properties-before.json`, `staging-metadata-before.json`, `staging-resource-search-after.json` | the revision the run started from (build `741754b`) and the revision it ended on |
| `staging-status-after.json`, `staging-properties-after.json`, `staging-metadata-after.json` | the resource is `READY` and its file list now names `assets/index-Cc7rTXmF.js` |
| `served-index-after.html`, `served-js-after.js`, `served-js-before.js` | the served bytes from the node, before and after the publish |
| `served-files-verify-after.json` | all 19 published files fetched back from `/render/` and hashed against the local `dist/` |
| `staging-json-listing-before.json` | the `JSON` identifiers that discovery can see under `Q-Website` |
| `staging-entity-state-after.json` | every synthetic entity still has the Phase 4 revision, order and state (no entity was disturbed) |
| `runtime-before-fix-measure.json`, `runtime-before-fix-console.json` | the **defect reproduced on staging**: build `741754b` renders 0 highlights, 0 featured works, 0 prices, 2 services and 1 step — the shipped items are hidden |
| `runtime-after-fix-measure.json`, `runtime-after-fix-hard-reload.json`, `runtime-checklist-after-fix.json` | the five confirmation checks after the publish, and the same checks repeated after a hard reload |
| `shipped-seed-identifiers.txt` | the 23 shipped seed identifiers plus the 404 probe showing none of them is published |
| `production-status-before.json`, `production-resource-search-after.json` | `WEBSITE / Qortal Web Builders / default` untouched |
| `screen-before-fix-staging-741754b.png` | staging rendering the pre-fix build |
| `screen-after-fix-top.png` | staging rendering the release candidate |
| `screen-after-fix-steps-seed-beside-qdn.png` | the synthetic step (with its thumbnail) beside shipped steps that carry ✎ 🗑 ↑ ↓ |
| `screen-after-fix-seed-highlight-with-controls.png` | a shipped highlight card carrying ✎ 🗑 ↑ ↓ and the `+ Add featured card` control |

## Verification

Every file in this directory is covered by `SHA256SUMS.txt` (`sha256sum -c`).
