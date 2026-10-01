# Shadow Archives — blog publication read-only audit

Executing agent (registered role of the agent that actually produced this work): **Codex**
Report/handoff writer (if different from the executing agent): **Codex**
Executing-agent evidence (how the real executor was established): This audit was performed directly in the current Codex session.
Report type: Read-only platform-integration and runtime audit
Exact application repository / branch / SHA: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`; initial baseline `agent/shadow-archives-webportal/owner-runtime-checkpoint-20260913` at `d8967d735f5621a13aa302e4ce977464258fac03`; remediation branch `agent/shadow-archives/blog-publish-partial-outcome-20261001` at `adfb91f841f10c796b462e045fc6520f6682b126`.
Canonical report path / SHA-256 / authorized remote evidence: This local, uncommitted report is at the path below. No commit, push, or other external mutation is authorized or performed.

## Objective and exit criterion

Determine, without changing application, QDN, Git, or server state, why a Shadow Archives blog-post creation can fail.  Separate source evidence, current read-only node evidence, and unproven hypotheses.

Primary task class: platform integration / runtime diagnostic.  The exact failure state of the owner's most recent Hub interaction was not supplied and no Qortal Hub window was available, so this audit can confirm a narrow source defect but cannot attribute a particular failed click to it.

## Workflow and authority model used

- The local `qortal-dev-workspace` is the Qortal workflow authority; current Core/Hub/framework source outranks application documentation, and observed runtime only proves its recorded environment.
- The application source is authoritative for its implemented behavior.  Owner instructions control product intent and authorization; no QDN write, signature, commit, push, publication, deployment, or server change is implied by this audit.
- The tunnel at `http://127.0.0.1:24992` is read-only Qortal-node evidence.  It cannot prove the Hub bridge, permission dialog, selected wallet, or the UI result of a new write.

## Baseline and preserved owner work

- Application worktree had the pre-existing untracked `AGENTS.md`; it was not read as authority, altered, moved, staged, or removed.
- Workspace worktree already had untracked `docs/qwb-qortal-web-builders/`, `docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md`, and `projects/qwb-qortal-web-builders.md`; these are owner work and remain untouched.
- Application remote branch equals local `d8967d7`; the published APP bundle identifies itself as its parent feature checkpoint `c9ce071`, whose Blog publication code is the same accepted Blog vertical.  The later local commit is a Contact checkpoint, not evidence of a Blog-code divergence.

## Source evidence — confirmed defect

**Finding: `PUBLISH_MULTIPLE_QDN_RESOURCES` partial failure is incorrectly classified as success.**

Severity: **HIGH** for truthful blog-write outcome and recovery; scope is only grouped publish outcomes.

1. A Blog post's authoritative entity and derived SubWire article are submitted together through `publishResources` (`src/services/blogPublishService.ts:715-725`).  This is the load-bearing creation stage.
2. The publish port accepts any resolved response as `submitted` (`src/qortal/publish.ts:196-212`).  It reads only an array/non-array shape and never checks the resolved `error.unsuccessfulPublishes` payload.
3. The same module recognizes `unsuccessfulPublishes` only in its `catch` path (`src/qortal/publish.ts:213-248`).
4. Both the pinned Hub source and current upstream `develop` source return, rather than throw, an object shaped as `{ message, error: { unsuccessfulPublishes } }` after a grouped partial failure (`Qortal-Hub/src/qortal/get.ts:2499-2519` in the pinned checkout; current upstream checked read-only at revision `d1ac4adb3b070a257954829c1d7258c2837b027a`).

Consequence: if either resource in the article pair is refused, the app can proceed as though the pair was submitted.  The entity can be absent while the modal proceeds to confirmation/index handling, or the entity can exist while the required SubWire resource is absent.  This is a concrete mismatch between the app's failure parser and Hub's actual successful-promise partial-failure contract.

This is the smallest confirmed technical cause that can explain an attempted post not appearing despite the client flow moving beyond the approval step.  It does **not** prove that every failed blog attempt has this cause.

## Live evidence — read-only node `qortal-node-b`

Timestamp: 2026-10-01, endpoint `http://127.0.0.1:24992`.

- `/admin/status` reported Qortal mainnet `syncPercent: 100`, `isSynchronizing: false`, height `2744355`.
- `/names/Shadow%20Archives` reports owner `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`, matching the application's expected publisher identity.
- `APP / Shadow Archives / default` is `READY`; its served main bundle embeds build commit `c9ce0716f87c4d083c01601678d0354102f455ac`.
- `DOCUMENT` discovery for `saw_post_` found two authoritative blog entities: `saw_post_7fowyzlvgg24` and `saw_post_80n480fypyvw`. Both fetch as schema-valid `blog-post` payloads. Their node timestamps are respectively `2026-09-13 20:56:24 EEST` and `2026-09-14 10:27:32 EEST`; they are not dated 2026-10-01. No newer `saw_post_` resource was returned by this read-only query.

Interpretation: the node is reachable and synchronized, the app identity exists, and Blog publishing succeeded twice earlier for this deployed build lineage. Therefore the evidence rules out a universal node outage, missing publisher name, or a permanently nonfunctional Blog implementation. It does not prove a current Hub approval or a new post's transaction outcome; the absent newer resource is consistent with the owner-reported unsuccessful publication.

## Hypotheses and blockers

- **Most likely bounded cause when a post does not materialize after the grouped approval:** the confirmed partial-result parsing defect above.  To prove it for a particular attempt, capture the modal's exact error/outcome and read the three relevant resource coordinates after that attempt.  Do not repeat an ambiguous write automatically.
- **Unknown:** a refusal affecting all resources (for example Hub rejection, fee/balance condition, or owner-mode/permission failure) cannot be diagnosed from the node alone.  The application normally exposes the returned error, but no error text or Hub trace was provided.
- **Unknown:** the current installed Hub version was not available for inspection.  Upstream Hub has moved from the locally pinned `12a573b` to `d1ac4ad`; the relevant resolved partial-failure return shape remains present upstream, but this is not proof of the owner's installed Hub version.
- **Not a cause:** QDN write authority is not inferred from the node owner record.  The real host must still establish owner mode and ask for each approval.

## Remediation applied

Applied only in the application worktree; no commit or publication was made.

- `src/qortal/publish.ts` now normalizes a resolved grouped-publish response containing `error.unsuccessfulPublishes` into the existing `partial`/`failed` taxonomy before generic success handling.
- The same normalization is shared by thrown and resolved partial responses, preserving the resource identities that did land and never retrying an ambiguous or partial write.
- Added `src/qortal/publish.test.ts`, with one Hub-shaped resolved partial response and one all-failed response.
- Focused verification passed: `npm test -- src/qortal/publish.test.ts src/services/blogPublishService.test.ts` — 2 files, 26 tests passed; targeted ESLint and Prettier checks passed; `git diff --check` passed; `npm run typecheck` completed without diagnostics.

No redesign of Blog, catalog, SubWire, owner mode, or publishing workflow was made.

## Owner-runtime confirmation after remediation

Owner reported that, after building and publishing the changed APP, a new post published successfully in Shadow Archives. Fresh read-only node evidence at `http://127.0.0.1:24992` confirms:

- `APP / Shadow Archives / default` is `READY`, with latest signature `cKwTKz3nnk6KxUCZu3LLSu5wAFjj8wkMM3vvFqoQxGZByBVdxRZgP6PP3hhee93DGBCzCbpLyWXzhkzMRiZf22N`.
- The served bundle contains application build identity `d8967d735f5621a13aa302e4ce977464258fac03`; it was built from the dirty local source that contained this fix before it was committed as `adfb91f`.
- New authoritative entity `DOCUMENT / Shadow Archives / saw_post_lr6vjv48uo4u` exists, with signature `6wQFYfAtvNuhVSX9knFQWRXXutMw5ePXdCE9ZNvzibUm7qKNBJMEP5vctgL7bMJ1WtbuZ4UnfVSZ44Cmfz8aSbU` and the owner's supplied post title.

This proves this app's canonical post entity published and is discoverable on the node. The owner did not test the optional derived SubWire publication in this run, so SubWire consumer discovery/rendering for this specific new post remains **NOT VERIFIED**.

The remaining acceptance workflow for this narrowly scoped patch is:

1. focused publish-port and Blog-service regression tests;
2. publish the changed APP bytes, then a real Hub owner attempt, observing the actual outcome without retrying; and
3. read-only verification of the exact entity/SubWire/index coordinates produced by that attempt.

## Checks not executed and why

- No full automated suite or build was run: the focused tests cover the changed protocol boundary; a full suite/build cannot prove a real Hub promise shape or a signed write.
- No real Hub interaction was run: no Qortal Hub process/window was available to this session. The node tunnel is intentionally not a signing substitute.
- No QDN write, APP publication, test-post transaction, commit, push, deployment, server change, or issue mutation was performed.

## Adversarial self-audit

- I did not claim that the confirmed parsing defect caused a specific owner attempt; it is a confirmed narrow defect and a supported explanation only.
- I did not treat node availability, an existing APP, or historical successful posts as evidence that a current Hub write works.
- I did not infer that the node-recorded name owner is the selected Hub account.
- No unrelated Contact, Video, Gallery, documentation-cleanup, or transport work was added.

## Report saved

- Absolute path: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/audits/2026-10-01-blog-publication-read-only-audit.md`
- SHA-256: omitted because embedding a file's own digest would change it; calculate only for an external handoff snapshot.
