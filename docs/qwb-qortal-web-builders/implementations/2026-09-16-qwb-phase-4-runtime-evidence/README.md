# QWB Phase 4 runtime evidence — 2026-09-16

Companion evidence for
`../2026-09-16-qwb-phase-4-owner-runtime-validation.md`.

**No owner-runtime evidence is present in this directory**, because the Phase 4 real-host run could
not be executed (see the report, §1 and §4). Everything here is either (a) re-verification of the
accepted Phase 3 build on the accepted commit, or (b) **read-only** observation of the live node and
of the existing QDN state. No QDN write, signature, transaction or publication was made, and no
`PUBLISH_*`/`DELETE_*` request was issued.

## Files

| File | What it is | Write? |
| --- | --- | --- |
| `run-timestamp-utc.txt` | UTC time of the evidence capture | read-only |
| `git-baseline.txt` | branch, HEAD, remote phase-3 ref, dirty state, whitespace check | read-only |
| `gate-typecheck.txt` | `npx tsc --noEmit` | read-only |
| `gate-lint.txt` | `npx eslint .` | read-only |
| `gate-format.txt` | `npx prettier --check .` | read-only |
| `gate-tests.txt` | `npx vitest run` | read-only |
| `gate-build.txt` | `npm run build` (reproducible build) | local build output only |
| `node-a-admin-status.json` | Qortal node A `/admin/status` | read-only |
| `node-b-admin-status.json` | Qortal node B `/admin/status` | read-only |
| `node-a-admin-info.json` | Qortal node A `/admin/info` (version, mainnet) | read-only |
| `node-b-admin-info.json` | Qortal node B `/admin/info` | read-only |
| `live-qwb-name-record.json` | `/names/Qortal Web Builders` — name ownership | read-only |
| `live-qwb-website-search.json` | `WEBSITE` search for the live resource | read-only |
| `live-qwb-website-metadata.json` | live resource file list + metadata | read-only |
| `live-qwb-website-status.json` | live resource readiness status | read-only |
| `live-qwb-website-index.html` | bytes the live `default` resource currently serves | read-only |
| `prerun-qdn-state.txt` | Phase 4 precondition-2 pre-run state of `qwb_*` content | read-only |

## Endpoints used

- node A `http://127.0.0.1:24991` (SSH tunnel → VPS loopback `12391`)
- node B `http://127.0.0.1:24992` (SSH tunnel → VPS loopback `12391`)

Both are Qortal **mainnet** full nodes. Reads only.
