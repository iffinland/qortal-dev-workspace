# QWB Phase 4 owner-runtime evidence — resumed run, 2026-09-16 (PASS)

This directory holds the artefacts of the **resumed** Phase 4 owner-runtime run
that executed the Phase 3 §14 procedure end to end against the staging resource
`WEBSITE / Q-Website / default` and returned **PASS** for steps 1–13.

The files in the parent directory (`…/2026-09-16-qwb-phase-4-runtime-evidence/`)
are the earlier `blocked` run and are deliberately left in place.

## Provenance

- App repo `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`,
  branch `agent/qwb/phase-4-runtime-fix` @ `741754becb79a131c699f2468fe096fdacd00c19`
  (accepted Phase 3 build `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5`).
- Served staging build: `dist/` of that revision, published as
  `WEBSITE / Q-Website / default`, signature `5qU9BKTp…cgb4i`.
- Nodes: mainnet `qortal-6.1.9-108bf19`, `127.0.0.1:24991` (A) and
  `127.0.0.1:24992` (B), `syncPercent` 100.
- Host: Qortal Hub 3.0.3 (Linux/Electron), owner account
  `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` (also owner of the `Q-Website` name).
- All content is synthetic. The production resource
  `WEBSITE / Qortal Web Builders / default` was read-only inspected and never
  written.

## File map

| File | Proves |
| --- | --- |
| `step1-reload.json`, `step1-hard-reload.json` | owner boot, owner bar, genuine reload (marker gone, `frameNavigated`) |
| `step3-*` | add -> revision 1, toast, node payload/status/search |
| `step4-edit.json` | edit -> revision 2 |
| `step5-reload.json`, `step5-hard-reload.json` | reload-surviving persistence of the edit |
| `step6-media.json`, `step6-net-capture.json`, `step6-fixed-reload.json`, `step6-thumb.webp` | media published before the entity; thumbnail served at the bare identifier path (3016 B WebP, `900x600` rendered) |
| `step7-reorder.json`, `step7-reload.json` | reorder = exactly one publish, order survives reload |
| `step8-delete.json`, `step8-tombstone.json`, `step8-reload-net.json` | tombstone `state:"deleted"`, row gone after reload, no node-admin delete |
| `step9-status-with-writes.txt`, `step9b-status-fresh-session.txt` | `Publishing status` lists state **and** availability, `Pending writes: 0` |
| `step10b-reload-content.txt` | `Reload content` -> `Content reloaded from this node.` |
| `step11-visitor.json/.png`, `step11-final-visitor.json/.png` | independent visitor browser: no owner UI, identical public content |
| `hub-dialog.png`, `hub-dialog-layout.png`, `step12-rejected-hub.png` | host approval dialog layout (Decline left, Accept right) and the rejected-draft state |
| `step12-probe.json` | diagnosis: a **trusted** pointer click landed on the `Accept` control |
| `step12-decline2.json`, `step12-timeout.json` | two attempted owner declines that were in fact approved (retained as evidence, not PASS) |
| `step12-declined.json`, `step12-rejected-ui.json`, `step12-attempt1-note.txt` | **step 12 PASS**: `Rejected by the host …`, draft preserved, nothing claimed, one dialog, no retry, node revision unchanged |
| `step13-refuse.json` | Hub **locked** does not change the account: app still asked the host; declined -> truthful rejection, node unchanged |
| `logout-watch.json`, `login-watch.json`, `restore-watch.json` | Hub log-out ends the session and destroys the render frame; signed-in non-owner and restore sequence |
| `step-final-reload.json` | hard reload after the final write: owner bar returns, revision survives, no exception |
| `step9-final-write.json` | final verified write (`rev 7`) |
| `served-index-now.html`, `served-js-now.js`, `thumb-now.webp` | served bytes hash-match the local accepted build and the local thumbnail |
| `final-state.json` | end-of-run node heights, name record, every staging resource with `rev`/`state`/`order`, and the untouched production resource metadata |

## Verification

`SHA256SUMS.txt` in the parent directory covers every file in this tree plus the
pre-existing `blocked`-run files.
