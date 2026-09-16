# QWB Phase 4 staging owner-runtime validation — qwb-qortal-web-builders/phase-4-20260916

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): every artefact in this task — the
git baseline, the five gate runs, the read-only node probes, the pre-run QDN snapshots, the evidence
bundle and this report — was produced by the **DeepSeek** model executing through the local Codex CLI
profile. Per `AI-Orchestration/GIT-AND-HANDOFF.md` the CLI/orchestration profile is not the executor,
so the executing agent is recorded as DeepSeek. No third-party curating agent wrote or reviewed this
work.
Report type: **owner-runtime validation report (Phase 4) — outcome `blocked`; no PASS claimed**
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- branch `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` — the accepted Phase 3
  build; **unmodified, working tree clean, no new commit**
- remote-verified during this task: `git ls-remote origin refs/heads/agent/qwb/phase-3` →
  `911b44f3e57c39c46048c950274c89bdd04596f5`
Canonical report path:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md`
(SHA-256 recorded in "Report saved")
Companion evidence directory: `…/implementations/2026-09-16-qwb-phase-4-runtime-evidence/`
(18 files + `SHA256SUMS.txt`, all read-only or local-build artefacts)

---

## 1. Objective and result

**Objective.** Execute the single real-host validation procedure defined in the Phase 3 report §14
for the accepted build `911b44f`, against a staging resource
`WEBSITE / <owner-confirmed-staging-name> / default`, using only synthetic staging content, without
publishing or overwriting the live `WEBSITE / Qortal Web Builders / default`, and return real
persisted read-back and reload evidence for steps 1–13.

**Result: NOT EXECUTED — `blocked` before step 1. No runtime PASS is claimed.**

- Steps 1–13 of §14 are **all unexecuted**. There is no owner-recognition evidence, no visitor
  negative-control evidence, no add/edit/reorder/media/tombstone evidence, no read-back, no reload
  evidence, and no declined-write or account-switch evidence.
- **No QDN write was made.** No publish, overwrite, signature, transaction or deletion occurred. No
  `PUBLISH_QDN_RESOURCE` / `DELETE_*` request was issued. Consequently there is **no ambiguous write
  to resolve and nothing to conceal or retry.**
- Nothing in this report may be read as owner-runtime acceptance. Per the task's own rule, tests,
  gates and the scripted harness do **not** constitute PASS, and they are not offered as such here.

**One-line blocking condition.** The run is gated on owner-only inputs that are unavailable to this
agent in this environment — a *confirmed staging publishing name*, the owner's *signing account,
password and interactive host approvals* — and on the precondition that a Phase 3 build already be
published as a QDN `WEBSITE` resource (none is). Details in §4.

**Note on the staging target as received.** The task supplied the staging target as the literal
placeholder `WEBSITE / <OWNER-CONFIRMED-STAGING-NAME> / default`. No confirmed staging name exists in
the project documentation or on-chain (§4.1), so the target could not be resolved, and inventing one
would have been an unauthorized mainnet publication under the owner's identity.

## 2. What was verified instead (non-owner, autonomous)

Everything below re-verifies the **accepted** Phase 3 build and the **real node state**. None of it
is owner-runtime acceptance.

1. **Baseline**: branch `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5`, clean
   working tree, whitespace-clean diff, remote `refs/heads/agent/qwb/phase-3` equal to the local
   commit. `main` and `agent/qwb/phase-2` untouched.
2. **Gates re-run on this machine** (2026-09-16): `tsc --noEmit` exit 0; `eslint .` exit 0;
   `prettier --check .` clean; `vitest run` **24 files / 283 tests passed**; `npm run build`
   succeeded — identical counts to the Phase 3 report.
3. **Build reproducibility**: the freshly built `dist/` is **byte-identical** to the `dist/` already
   present before the build (`diff -r` clean), emitting
   `dist/assets/index-CLC6fuj3.js` (126.57 kB, gzip 37.56 kB) and
   `dist/assets/style-BgNavAWw.css` (215.35 kB) — the same artefacts the Phase 3 report recorded.
   19 files / 1 209 402 bytes; a `WEBSITE` archive of it is ≈ 879 kB.
4. **The bundle is QDN-path-safe** (a real staging prerequisite, not previously recorded):
   `vite.config.ts` sets `base: './'` and the built `dist/index.html` references only relative paths
   (`./assets/index-CLC6fuj3.js`, `favicon.svg`, `site.webmanifest`). No root-absolute URLs, so the
   archive will resolve correctly when served from a QDN resource path.
5. **Real-node evidence (read-only)**: both tunnelled nodes are Qortal **mainnet** full nodes,
   `qortal-6.1.9-108bf19`, `syncPercent` 100, `isSynchronizing` false, height 2725842 at capture.
6. **Pre-run QDN state (Phase 4 precondition 2)**: **zero** QWB app resources exist under any
   candidate publishing name — the `JSON` site singleton `qwb_site_v1` returns node error 1401
   ("Couldn't find PUT transaction") and `qwb_*` prefix searches under every candidate name return
   0 hits. The first add would therefore be unambiguous, exactly as precondition 2 requires.
7. **Live resource identified and NOT touched**: `WEBSITE / Qortal Web Builders / default` exists,
   `status: READY`, size 21 360 bytes, 2 files, latest signature `iFSzUWnU…Rjbb1`, created
   2024-12-24T17:00:59Z, last updated **2026-07-07T13:12:05Z**. It is **not** the Phase 3 build: it
   serves an 892-byte placeholder page (`index.html` + `img/sorry-event-is-canceled.avif`). The name
   `Qortal Web Builders` is owned by `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` (registered
   2024-12-24T12:50:27Z). No read or write was directed at this resource beyond the read-only
   inspection recorded in the evidence bundle.

## 3. Evidence by layer

| Layer | Command / action | Environment | Timestamp (UTC) | Result |
| --- | --- | --- | --- | --- |
| Git baseline | `git rev-parse HEAD`, `git status`, `git ls-remote origin refs/heads/agent/qwb/phase-3` | dev repo | 2026-09-16T02:28Z | `911b44f…`, clean, remote equal |
| Types | `npx tsc --noEmit` | dev repo | 2026-09-16T02:28Z | exit 0 |
| Lint | `npx eslint .` | dev repo | 2026-09-16T02:28Z | exit 0 |
| Format | `npx prettier --check .` | dev repo | 2026-09-16T02:28Z | clean |
| Tests | `npx vitest run` | dev repo | 2026-09-16T02:30Z | 24 files / 283 tests passed |
| Build | `npm run build` | dev repo | 2026-09-16T02:30Z | success; dist byte-identical to pre-build dist |
| Node A | `GET /admin/status`, `GET /admin/info` | `127.0.0.1:24991` → VPS loopback `12391` | 2026-09-16T02:28Z | `qortal-6.1.9-108bf19`, mainnet, height 2725842, sync 100 % |
| Node B | `GET /admin/status`, `GET /admin/info` | `127.0.0.1:24992` → VPS loopback `12391` | 2026-09-16T02:28Z | `qortal-6.1.9-108bf19`, mainnet, height 2725842, sync 100 % |
| Live resource | `GET /arbitrary/resources/search?service=WEBSITE`, `/arbitrary/metadata/…`, `/arbitrary/resource/status/…`, `?filepath=index.html` | node A | 2026-09-16T02:28Z | READY, 21 360 B, 2 files, placeholder content — read-only |
| Name ownership | `GET /names/Qortal%20Web%20Builders` | node A | 2026-09-16T02:28Z | owner `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` |
| Pre-run state | `GET /arbitrary/resources/search` (`JSON`/`DOCUMENT`, `qwb_` prefix, per name); `GET /arbitrary/JSON/<name>/qwb_site_v1` | node A | 2026-09-16T02:32Z | 0 QWB resources; singleton error 1401 → nothing published |
| **Owner-runtime steps 1–13** | **not executed** | — | — | **blocked** (§4) |

Raw captures, hashes and caveats: `2026-09-16-qwb-phase-4-runtime-evidence/` (+ `SHA256SUMS.txt`).

Incidental platform observation worth keeping (recorded in the evidence, not a defect of this app):
the node did **not** honour the `names=<...>&exactMatchNames=true` query form on
`/arbitrary/resources/search` — every name returned the same foreign `qwb_ix_*` rows — while the
singular `name=` form does filter. This corroborates the Phase 3 finding that server-side
name filtering cannot be relied upon and that the app's client-side re-filter on the exact
`(name, service, identifier)` is load-bearing.

## 4. Why the run could not be executed

### 4.1 B1 — No owner-confirmed staging name
The staging target was supplied as the unresolved placeholder
`WEBSITE / <OWNER-CONFIRMED-STAGING-NAME> / default`. No confirmed staging name is recorded anywhere:
the canonical project context still lists "staging target" under *"Not yet decided by the owner"*,
and the target-architecture proposal leaves it open in **D9** ("A needs a second publishing name …
that the owner controls"). The Hub's stored wallets own the names `iffi vaba mees`, `iffi olen`,
`vaba mees`, `free man`, `russian`, `AstuAeda`, `Shadow Archives`, `iffi forest life`; the live
`Qortal Web Builders` name is owned by a different account (§4.4). Selecting one of these, or any
other name, is an owner decision: it fixes the app's `_qdnName`, is permanently visible on mainnet,
and costs QORT. It was not made, and was not inferred.

### 4.2 B2 — Nothing is published to open in a real host
Phase 4 precondition 1 requires the build to be published/served as a QDN `WEBSITE` resource whose
`_qdnName` is the intended publishing name, because owner recognition needs `_qdnContext === 'render'`
and a non-empty injected `_qdnName`. **No such resource exists.** The only QWB `WEBSITE` resource is
the live one, and it serves a 892-byte placeholder (§2.7), not the Phase 3 bundle. There is therefore
no app that a host could open for steps 1–13.

### 4.3 B3 — Publishing requires the owner's signing authority
Creating the staging resource is a signed, fee-bearing mainnet transaction requiring the owner's
account, that account's password, and an interactive host approval. The agent holds no wallet
password and no unlocked account. Unlocking the local Qortal Hub and signing are inherently
owner-only actions.

### 4.4 B4 — The live name owner is not present in this Hub profile
`Qortal Web Builders` is owned by `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`. The local Hub's
`~/.config/qortal-hub/wallet-storage.json` holds five wallets with `address0` =
`QRTUysZHKgxrdqsATotaffNVfFrD4KPE2Q`, `QNLCcmfyoMBop4b9XP2hCrJxzjPcWDKw5T`,
`QRaCN6dYok5dqPP8rTQfUpAkwK8dreeVNt`, `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`,
`QdFtH8USoDvixChuG13dmaxU87fr84NcDL` — **not** the name owner. Even with the password, this profile
could not sign as the current owner of the live name without importing that account. (No wallet
material was read, decrypted or copied; only the public address list was inspected.)

### 4.5 B5 — Steps 1–3, 12 and 13 are interactive by construction
Step 3 requires approving the host's signature dialog; step 12 requires **declining** a dialog or
letting its timeout expire; step 13 requires switching/locking the Hub account mid-form. No host
event or API exposes these to an agent, and the Hub requires human interaction. They cannot be
simulated, and simulating them would not be real-host evidence.

### 4.6 B6 — Node API keys are not a substitute, and are not authorized
Read/admin API keys exist for the tunnelled VPS nodes, but publishing through the node API would
bypass the app's host-mediated `PUBLISH_QDN_RESOURCE` path, would not produce the `_qdnContext ===
'render'` conditions the validation exists to test, and would be an unauthorized mainnet write under
an account the owner has not designated. It was not attempted.

**No other path exists.** The Phase 2 and Phase 3 reports establish that owner mode cannot be
exercised in Hub Developer-Mode proxy (`_qdnName` is empty → `unavailable`) or through
gateway/domain-map serving; only a real host with a published resource can exercise it. There is no
local testnet node configured in this environment either.

## 5. Exact owner inputs required to unblock

The run becomes executable — in one sitting, by the owner, with an agent driving only what is
non-interactive — as soon as these four things exist:

1. **A confirmed staging publishing name** the owner's account owns (e.g. one of the names listed in
   §4.1, or any other) — this is the `<OWNER-CONFIRMED-STAGING-NAME>`.
2. **The staging resource published**: `npm run build` in the dev repo, then publish `dist/` as
   `WEBSITE / <staging-name> / default` (synthetic content only; ~879 kB archive; the build is
   `base: './'`-safe per §2.4). Record the WEBSITE resource revision/signature.
3. **The owner signed in, in a real Hub**, as the account that owns that staging name, with the
   permission dialog approved — for steps 1, 3–11, plus a second profile/account for the visitor
   control (step 2/11).
4. **Willingness to decline one approval dialog** (step 12) and to **switch/lock the account** while
   a form is open (step 13) — both destructive-free but interactive.

Afterwards the procedure is exactly Phase 3 §14 steps 1–13, recording node URL/height, the
identifiers and revisions of every `qwb_*` resource touched, the pre/post `SEARCH_QDN_RESOURCES`
results, console output and owner/visitor screenshots. Phase 4 precondition 2 is already satisfied
today (§2.6): the pre-run state is empty, so the first add is unambiguous.

## 6. Files changed

**Application repository: none.** No source, test, config, build-input or documentation file was
modified. `git status` is clean; no commit, amend, branch or worktree was created. Running
`npm run build` rewrote the gitignored `dist/` (allowed) and the result was verified byte-identical
to the pre-existing `dist/`.

**Documentation (this workspace):** two new additions under the untracked
`docs/qwb-qortal-web-builders/` path — this report and its companion evidence directory. The
canonical project context `projects/qwb-qortal-web-builders.md` was updated only in its status block,
to record the accepted Phase 3 revision and the Phase 4 `blocked` state.

**Orchestration repository:** unchanged. `handoff_sync = pending_authorization`.

## 7. Checks not executed and why

| Not executed | Reason |
| --- | --- |
| Every owner-runtime step 1–13 of Phase 3 §14 | `blocked` — §4 (no confirmed staging name, nothing published, no signing authority, interactive gates) |
| Publishing the staging (`WEBSITE / <staging-name> / default`) resource | Requires the owner's name, account, fee and approval; not authorized for a specific name |
| Owner-mode recognition / visitor negative control in a real host | Requires a published resource + host session |
| Real `PUBLISH_QDN_RESOURCE` round-trips (add/edit/reorder/media/tombstone) and read-back verification | Same; no QDN write made, deliberately |
| Declined-write and account-switch fail-closed behaviour | Requires interactive host dialogs |
| Any read of the live `WEBSITE / Qortal Web Builders / default` for validation | Deliberately avoided; only read-only identification was performed, and the resource was not modified |
| Negative control in a second browser profile | Requires the real host session first |

## 8. Adversarial self-audit

- **Did I fabricate or infer a PASS?** No. The report states `blocked` in the header, §1 and §12, and
  labels every non-owner check as such. The strongest evidence available (283 tests, byte-identical
  reproducible build, live-node reads) is explicitly *not* offered as owner-runtime acceptance.
- **Did I write to QDN to "make progress"?** No. Zero writes, zero signatures, zero transactions.
  The absence of any ambiguous write is the correct state given no authorization and no name.
- **Did I invent a staging name?** No. Publishing synthetic content under an unconfirmed registered
  name would be an unauthorized, publicly visible, fee-bearing mainnet write under the owner's
  identity; the decision is open in D9 and was left to the owner.
- **Did I touch the live resource?** No. It was read-only identified (`search`, `metadata`,
  `resource/status`, one `filepath=index.html` fetch) so that the "do not overwrite" constraint could
  be reported precisely. No write path was reachable anyway (no signing authority).
- **Did I overstate the node evidence?** No. Both nodes are identified as mainnet by their own
  `/admin/info` (`isTestNet: false`), and heights are given as single-point observations with the
  capture timestamp.
- **Did I overstate the pre-run state?** No. The claim is bounded to the candidate names checked and
  is supported by the site-singleton 1401 error; the evidence file records that a `names=` server-side
  filter was silently ignored, so that the reading cannot be mistaken for a stronger claim. A build
  published under a name not checked cannot be ruled out — but with no owner-confirmed name there is
  nothing to open, so the distinction does not change the outcome.
- **Is any gate claim unverified?** No. Each gate's raw output is in the evidence bundle and hashed in
  `SHA256SUMS.txt`, and the bundle verifies clean.
- **Could a defect have been masked by stopping?** No defect claim is made in either direction. The
  Phase 3 risks that only a real run can settle (real image encoding, DOCUMENT publish, verify
  budget, replication lag) remain **untested**, and are listed as such in §10.

## 9. External actions

- **No commit and no push** in the application repository or in `AI-Orchestration`. The accepted
  Phase 3 commit `911b44f…` is unchanged and still equals the remote branch.
- **No** QDN write, QDN publication, signature, transaction, tag, release, deployment, server change,
  or issue mutation. The live `WEBSITE / Qortal Web Builders / default` resource is untouched.
- Live-node access was **read-only** (`/admin/status`, `/admin/info`, `/names/*`,
  `/arbitrary/resources/search`, `/arbitrary/metadata/*`, `/arbitrary/resource/status/*`, one
  arbitrary file fetch).
- No wallet seed, private key, password or API key was read, decrypted, copied or transmitted; only
  the public address list in `wallet-storage.json` was inspected to establish §4.4.
- `handoff_sync = pending_authorization` (no authorization to write the orchestration repo was given).

## 10. Remaining risks and follow-up

Still un-retired from the Phase 3 risk table, because only a real owner run can retire them: real
image encoding (`createImageBitmap`/canvas → WebP) and the media-before-entity ordering; the first
real `DOCUMENT` publish for articles; the 4 × 5 s verify budget on a slow node; read-back proving
only the serving node; `rev` equality not being payload identity; reorder-renumber non-atomicity; and
the absence of an account-change host event. **None may be marked resolved from this report.**

New, task-level follow-ups:

- Record the owner's staging-name decision in the project context and in D9 when it is made.
- The live `WEBSITE / Qortal Web Builders / default` currently serves an empty "Event is canceled"
  placeholder (last updated 2026-07-07). Final publication will therefore replace a placeholder, not
  the marketing site — the owner may want to confirm that this is the intended target and timing.
- Add one line to the Phase 4 runbook: capture the published staging WEBSITE resource's revision
  before step 1, so the app's "never republishes the WEBSITE resource" property can be checked
  against a recorded value.

## 11. Capability harvest

**No skill was created or updated, and no candidate is promotable.** All pending candidates still
lack the owner-runtime evidence that would set a real maturity:

| Candidate | Status after this task |
| --- | --- |
| `qortal/qdn-content-crud` | **Not promotable** — still no live publish from this repository; no read-back was observed from a real host |
| `qortal/registered-name-owner-mode` | **Not promotable** — owner recognition has never run in a real host |
| `qortal/inline-owner-editing` | **Not promotable** — same |
| `shared/headless-browser-evidence-harness` | **Not promotable** — no third consumer, and its platform fakes remain unvalidated against a real host |

The harvest result for this task is therefore *explicitly blocked*: it produced useful verification
and a precise blocker, but no reusable capability with runtime evidence. Re-run the harvest after the
Phase 4 owner run.

## 12. Readiness for final production publication

**Not ready.** Production publication of the live `WEBSITE / Qortal Web Builders / default` is
correctly deferred, and per the task it must not happen yet. What is ready:

- the accepted build `911b44f…` is verified on this machine (gates clean, build byte-identical and
  reproducible) and is QDN-path-safe;
- the pre-run QDN state is empty, so a staging run starts from an unambiguous baseline;
- the exact single-run procedure already exists (Phase 3 §14) and the only missing inputs are the
  four owner items in §5.

What is missing: the entire owner-runtime acceptance layer (§1, §7). Until that run passes with real
persisted read-back and reload evidence, this project has **no owner-runtime acceptance** and must not
be published to production.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md`
- Companion evidence directory (18 files + `SHA256SUMS.txt`, verified clean):
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-runtime-evidence/`
- Application commit this report concerns:
  `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` (unchanged; remote-verified)
- Handoff synchronization: `handoff_sync = pending_authorization` — nothing was committed or pushed
  in `AI-Orchestration/` or in the `qortal-dev-workspace` working tree.
- SHA-256 of the report body (313 lines, measured immediately before this bullet was
  appended): `2360c60b2f7da3a1a5614722ada47e7971351307fbe122184f33631057dfdeff`
