# Staging resources and revisions touched (2026-09-16 Phase 4 run)

All writes below are synthetic, were signed by the owner account
`QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` through Qortal Hub approvals, and were
published under the owner-approved staging name `Q-Website`. No write used a node
API key. The production resource `WEBSITE / Qortal Web Builders / default` was
never written (read-only metadata inspection only).

Node authority: mainnet `qortal-6.1.9-108bf19`, `127.0.0.1:24991` / `:24992`.

| # | Service / name / identifier | Revisions written | Final state | Signature (final revision) |
| --- | --- | --- | --- | --- |
| 1 | `WEBSITE / Q-Website / default` | 2 publishes (build `8fd110b`, then build `741754b`) | `READY`, 880 160 B, multi-file | `5qU9BKTpZycWToRwuZrkjoJDahNwvRLf2Uq2uSYLZH8Tra2ovQSKPg3TGRJX6Cg12gLh1KKamHQx61YYwN4cgb4i` |
| 2 | `JSON / Q-Website / qwb_svc_build-service-mu3jfqw1-i5hb` | rev 1 create, rev 2 edit, rev 3 edit, rev 4 edit, rev 5 edit, rev 6 edit, rev 7 edit (final) | active, order 50, title `Synthetic staging service (Phase 4, verified)` | `3D6TqkhSPrgQMSPfqWrWtmo6v5uMksLnL4D5p1sPLwhQM6bMfTQRTA74WiqnNxroLErmQHUK53TjPdvqJynCLKPw` |
| 3 | `JSON / Q-Website / qwb_step_process-step-mu3jj436-ynaz` | rev 1 create (with media reference) | active, order 10, title `Synthetic staging step (Phase 4)` | `jsMhMn1RoHR4rhMKdxRb3xCSCCxMQfmttvZivgZ7LFUD54qvsZfmU4VBYYA6LJLiuQiofGdRjAnGc37FbT9dj6c` |
| 4 | `THUMBNAIL / Q-Website / qwb_step_process-step-mu3jj436-ynaz` | 1 publish, issued **before** entity #3 | `READY`, 3 016 B WebP, served at the bare identifier path | (single publish; see `final-state.json`) |
| 5 | `JSON / Q-Website / qwb_step_process-step-mu3jjvhv-o74n` | rev 1 create, rev 2 reorder (order 0), rev 3 tombstone | `state:"deleted"`, `payload:null`, order 0 | `4XujAJodE5PErXdvsWRHnHZKEKthGwN7G8pSoBXYx7cerqyFhKRzAbfpSZJN3ugKnzTHLwf4wU8JwDgprAHAqNrg` |
| 6 | `JSON / Q-Website / qwb_svc_build-service-mu3jylnd-xmv8` | rev 1 create | active, order 60, title `In-session service A (Phase 4)` | `2geCFs6QJvVSTLj6Z3t5D9PSxYCFUgDFfg6d3dQqLaxeHpgfJdmHs8uBUne46z6AewqwdLCzcrzkT8EgV3MSEMf4` |
| 7 | `JSON / Q-Website / qwb_svc_build-service-mu3jyvwn-99dq` | rev 1 create, rev 2 reorder (order 55), rev 3 tombstone | `state:"deleted"`, `payload:null`, order 55 | `28pujKsF1ujhMPnF6Mhi8FhAgb5jay9DD1kSdmqutotYmN3d5xYiCttuoTg6DFmwN1XJzyN7jgcNZQXXmkkjDTnN` |

Notes:

- Rows 6 and 7 are the in-session pair created purely to give the `Publishing
  status` surface a session containing add + reorder + delete; row 7 was
  tombstoned so it does not render.
- The four intermediate edits of row 2 (rev 3–6) were produced by the step-12
  decline attempts, which were **approved by the operator instead of declined**
  and are recorded as evidence of a second and third confirmation of the success
  path, not as a step-12 declination. The genuine decline was then performed at
  rev 6 -> the write was refused and the node stayed at rev 6; rev 7 is the final
  verified write.
- Media replacement used `media-a.png` / `media-b.png` (900x600 synthetic).
- No staging resource was deleted from the network: Qortal exposes no
  app-accessible delete, so deletion is a tombstone republish to the same
  identifier.
