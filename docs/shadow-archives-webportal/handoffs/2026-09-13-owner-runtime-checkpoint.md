# Shadow Archives — accepted owner-runtime checkpoint, 2026-09-13

Executing agent (accepted feature implementation): **DeepSeek** through the local Codex CLI harness.
Report/handoff writer and checkpoint/documentation executor: **Codex Local**.
Executing-agent evidence: explicit owner instruction in this checkpoint task; the Video reports
already carry the Codex → DeepSeek correction; Blog reports record the DeepSeek provider/runtime.
Owner runtime validator: **owner**. Report type: durable checkpoint and documentation handoff.
Application branch: `agent/shadow-archives-webportal/owner-runtime-checkpoint-20260913`.
Application SHA: `c9ce0716f87c4d083c01601678d0354102f455ac`.

## Objective and exit criterion

Checkpoint the accepted Gallery + Video/Q-Tube + Blog/SubWire/Quitter implementation and update
Qortal status documentation. Complete when authorized branches are committed, pushed and their
remote SHAs verified, the four owner-PASS workflows are recorded, and owner files are preserved.
Primary class: Git checkpoint/documentation hygiene; no new feature or release work.

## Owner-runtime acceptance

Explicit owner acceptance recorded on **2026-09-13**, from this task's accepted-results statement
and referenced conversation `6aa3be65-44f8-83ed-bcf3-f9f1a423f501` (Shadow-Archives-webportal).
This is owner-reported real-host acceptance; this writer did not repeat publication or signing.

| Surface | Accepted owner workflow | Result |
| --- | --- | --- |
| Gallery | End-to-end publish → authoritative read → index convergence → thumbnails/item/album render → reload persistence | OWNER-RUNTIME PASS |
| Video + Q-Tube | Publish in Shadow Archives → Shadow Archives discovery/detail/playback → native Q-Tube discovery/playback | OWNER-RUNTIME PASS |
| Blog + SubWire | Publish in Shadow Archives → Shadow Archives discovery/detail/render → native SubWire discovery/render | OWNER-RUNTIME PASS |
| Optional Quitter | Explicit Blog announcement with separate approval → Quitter discovery/render, article link and cover | OWNER-RUNTIME PASS |

The owner accepts the current app worktree as the completed work to checkpoint. Its exact bytes
are retained (except the README status addition). This does **not** establish a byte-for-byte
comparison with the owner-tested deployed APP ZIP: that ZIP hash, exact test timestamps, new
publication coordinates and deployed consumer revisions were not supplied with acceptance.
No invented screenshots, transactions or exact build equivalence are used to fill those gaps.
Gallery PASS is carried forward from its closure; no claim of a new Gallery run after the later
shared-code changes is made. Regression support is recorded separately below.

## Dated contract evidence and limits

Source/read-only evidence captured by DeepSeek on 2026-09-13:

| Reference | Branch | Inspected source revision |
| --- | --- | --- |
| Qortal/q-tube | main | `68c3ea706c4ab110ffa44a7f55f8e09bdf7e85ff` |
| Qortal/Subwire | master | `a933a6c44d60db19cd219408e36c747aebcce994` |
| Qortal/Quitter | master | `4e4246c3283bcbc8e05e683260692ed36144f862` |
| Qortal/qortal | master | `108bf191d42d710ec617f535af30cfd82fc03c87` |
| Qortal/Qortal-Hub | develop | `12a573b27246e8a626b24794830c6bc432d1b05d` |
| Qortal/qapp-core | master | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` |

Live read-only environment in those reports: Qortal mainnet via local forwards
`127.0.0.1:24991` and `:24992`, Core `qortal-6.1.9-108bf19`.
The node-status capture is at height 2722989; later interop searches report 2723000.
These are separate observations, not simultaneous snapshots.
This task does not refresh platform sources or turn source revisions into deployed-runtime pins.
On future reuse, check current donor source and the affected runtime workflow; community-app
schemas/discovery/renderers are not timeless platform guarantees.

Evidence:

- [Gallery closure](2026-09-13-gallery-closure-checkpoint.md).
- [Gallery index coherence](2026-09-13-gallery-owner-workflow-index-coherence-owner-handoff.md).
- [Gallery bridge/media](../runtime/2026-09-13-gallery-host-read-contract-and-media-rendering-report.md).
- [Video implementation](../implementation/2026-09-13-video-owner-publishing-implementation-report.md).
- [Q-Tube source/live reads](../validation/2026-09-13-video-qtube-contract-live-read-only-validation.md).
- [Blog implementation](../implementation/2026-09-13-blog-subwire-quitter-owner-publishing-implementation-report.md).
- [SubWire/Quitter source/live reads](../validation/2026-09-13-blog-subwire-quitter-contract-live-read-only-validation.md).
- [Original Blog owner procedure](2026-09-13-blog-subwire-quitter-owner-live-validation-handoff.md).

Historical pending/not-published/no-commit statements remain scoped to their original runs.
Dated supersession notices now prevent them from being mistaken for current project status.
Older donor article/cross-post captures prove consumer contracts, not the later owner publication.

## Workflow measurements

| Work | Executor | Recorded measurement |
| --- | --- | --- |
| Gallery coherence | DeepSeek | 43 minutes (previous closure record) |
| Gallery bridge/media follow-up | DeepSeek | 37 minutes (previous closure record) |
| Video/Q-Tube autonomous vertical | DeepSeek | 46 files / 502 tests in implementation report; final owner PASS |
| Blog/SubWire/Quitter autonomous vertical | DeepSeek | 51 files / 562 tests in implementation report; final owner PASS |

Video/Blog elapsed runtime, tokens and API cost were not captured in the supplied durable evidence;
no estimates are substituted. The owner considers the two latest autonomous verticals successful.
Previous reports note a non-reproducible full-suite flake under load; that history is retained.

## Identity audit

Accepted Video implementation/validation already have explicit corrections of earlier `Codex`
attribution to **DeepSeek**. Blog implementation/validation/handoff already name **DeepSeek**.
Gallery implementation attribution was corrected in its prior closure. No blanket replacement of
`Codex` is appropriate: the harness and actual checkpoint writer legitimately retain that name.
The unrelated 2026-09-11 untracked visual-correction report remains untouched and uncommitted.

## Candidate knowledge promotions — next task only

No skills are created, edited or promoted here, by explicit owner scope (overrides automatic
capability-harvest promotion). The shared harvest decision test was used only to select candidates.

1. **Update existing Qortal cross-app video publishing skill**, currently `candidate` at
   `AI-Orchestration/skills/qortal/cross-app-video-publishing/SKILL.md`. Evidence: Video/Q-Tube
   reports + owner PASS; adapter `src/services/qtubeVideoContract.ts`. Capture single VIDEO bytes,
   derived DOCUMENT metadata and actual discovery/render gates. Do not extend to engagement,
   edit/delete or untested large-file limits.
2. **SubWire-compatible article publishing.** Evidence: Blog reports + owner PASS;
   `src/services/subwireArticleContract.ts`, `src/domain/richTextMarkdown.ts`. DOCUMENT prefix,
   GFM conversion, bare WebP cover, safe derived rendering, bounded discovery; not a new editor.
3. **Optional Quitter announcement.** Evidence: Blog/Quitter reports + owner PASS;
   `src/services/quitterAnnouncementContract.ts`. Separate opt-in/approval, exact namespace and
   payload, independent outcome; not a general social API or automatic retry.
4. **Derived-index recovery/coherence from authoritative QDN entities.** Evidence: Gallery
   coherence/closure + Video/Blog acceptance; `catalogPublishSupport.ts`, `catalogWriter.ts`,
   `galleryPublishService.ts`, `contentRepository.ts`. Keep unreadable indexes intact, preserve
   entity authority and bounded discovery. Do not claim every failure injection was owner-tested.
5. **FETCH_QDN_RESOURCE parsed-JSON normalization.** Evidence: Gallery bridge/media report + PASS;
   `src/qortal/qdn.ts`. Normalize the observed object/string response at the bridge boundary with
   validation, not global assumptions about every action or Qortium behavior.

All candidates must retain these dated pins and define freshness/invalidation checks when promoted.
The only loaded skill was shared `capability-harvest` (`verified-runtime`, last checked 2026-09-13);
its procedure was inspected locally. The existing video skill was inventoried read-only as a
candidate destination, not applied as authority for implementation.

## Baselines and preserved owner state

### app

Repository: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`.
Initial branch: `agent/shadow-archives-webportal/video-qtube-publishing`; HEAD `472f244bd8cbb8f6ef11d60d7ee1baaaac6c0c83`.
One linked worktree (the listed repository); no worktree moved.

Initial status:

```text
 M README.md
 M package-lock.json
 M package.json
 M src/domain/catalog.ts
 M src/domain/identifiers.ts
 M src/domain/index.ts
 M src/features/blog/BlogPage.tsx
 M src/features/gallery/owner/GalleryAlbumModal.tsx
 M src/features/gallery/owner/GalleryImageModal.tsx
 M src/features/gallery/owner/GalleryOwnerPanel.tsx
 M src/features/owner/StudioPage.tsx
RM src/features/gallery/owner/TaxonomyInput.tsx -> src/features/owner/TaxonomyInput.tsx
RM src/features/gallery/owner/owner.css -> src/features/owner/owner.css
 M src/features/videos/VideoDetailPage.tsx
 M src/features/videos/VideosPage.tsx
 M src/qortal/publish.ts
 M src/services/catalogWriter.ts
 M src/services/contentRepository.test.ts
 M src/services/contentRepository.ts
 M src/services/galleryPublishService.test.ts
 M src/services/galleryPublishService.ts
 M src/services/imageProcessing.ts
 M src/styles/content.css
?? AGENTS.md
?? scripts/live-blog-interop-check.ts
?? src/domain/blogMedia.ts
?? src/domain/richTextMarkdown.test.ts
?? src/domain/richTextMarkdown.ts
?? src/domain/videoMedia.ts
?? src/features/blog/owner/
?? src/features/videos/VideoDetailPage.test.tsx
?? src/features/videos/owner/
?? src/services/blogPublishService.test.ts
?? src/services/blogPublishService.ts
?? src/services/catalogPublishSupport.ts
?? src/services/ownerAuthority.ts
?? src/services/qappIdentifierContract.ts
?? src/services/qtubeVideoContract.test.ts
?? src/services/qtubeVideoContract.ts
?? src/services/quitterAnnouncementContract.test.ts
?? src/services/quitterAnnouncementContract.ts
?? src/services/subwireArticleContract.test.ts
?? src/services/subwireArticleContract.ts
?? src/services/videoMetadataProbe.test.ts
?? src/services/videoMetadataProbe.ts
?? src/services/videoPublishService.test.ts
?? src/services/videoPublishService.ts
```

### workspace

Repository: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`.
Initial branch: `main`; HEAD `b8fd2f6fbfcff88c0ab9bc8fd116d5548679d2d2`.
One linked worktree (the listed repository); no worktree moved.

Initial status:

```text
?? docs/shadow-archives-webportal/handoffs/2026-09-13-blog-subwire-quitter-owner-live-validation-handoff.md
?? docs/shadow-archives-webportal/implementation/2026-09-11-owner-runtime-visual-correction-report.md
?? docs/shadow-archives-webportal/implementation/2026-09-13-blog-subwire-quitter-owner-publishing-implementation-report.md
?? docs/shadow-archives-webportal/implementation/2026-09-13-video-owner-publishing-implementation-report.md
?? docs/shadow-archives-webportal/live-evidence/
?? docs/shadow-archives-webportal/validation/2026-09-13-blog-subwire-quitter-contract-live-read-only-validation.md
?? docs/shadow-archives-webportal/validation/2026-09-13-video-qtube-contract-live-read-only-validation.md
```

### orchestration

Repository: `/home/iffi/VsCodec-Projects/AI-Orchestration`.
Initial branch: `agent/orchestration/bootstrap`; HEAD `c52e04841adfde062e579463a39bf0463609c8d5`.
One linked worktree (the listed repository); no worktree moved.

Initial status:

```text
 M AGENTS.md
 M GIT-AND-HANDOFF.md
 M WORKFLOW.md
?? templates/REPORT.md
```

## Checkpoint structure and files

Application checkpoint retains Gallery commits `b247ccd` and `472f244` as ancestors and records
all accepted Video/Blog implementation in one coherent commit. No synthetic separation of their
shared owner/catalog changes and no history rewrite. Both TaxonomyInput and owner.css moves are
preserved as Git-detected renames. App source/lockfile bytes match the starting worktree.
The only new application edit by this task is the README acceptance section.

Workspace changes:

- `projects/shadow-archives-webportal.md`
- `docs/shadow-archives-webportal/handoffs/2026-09-11-shadow-archives-phase-1a-handoff.md`
- `docs/shadow-archives-webportal/handoffs/2026-09-13-gallery-closure-checkpoint.md`
- `docs/shadow-archives-webportal/handoffs/2026-09-13-blog-subwire-quitter-owner-live-validation-handoff.md`
- `docs/shadow-archives-webportal/architecture/2026-09-11-qdn-data-contracts.md`
- `docs/shadow-archives-webportal/architecture/2026-09-11-phase-1a-architecture-report.md`
- `docs/shadow-archives-webportal/architecture/2026-09-11-phase-1b-implementation-plan.md`
- `docs/shadow-archives-webportal/implementation/2026-09-13-blog-subwire-quitter-owner-publishing-implementation-report.md`
- `docs/shadow-archives-webportal/implementation/2026-09-13-video-owner-publishing-implementation-report.md`
- `docs/shadow-archives-webportal/validation/2026-09-13-blog-subwire-quitter-contract-live-read-only-validation.md`
- `docs/shadow-archives-webportal/validation/2026-09-13-video-qtube-contract-live-read-only-validation.md`
- This checkpoint report.
- Previously untracked accepted Video/Blog reports and `live-evidence/*.json` are included.

Orchestration changes are limited to task-specific TASK.md, STATUS.json, IMPLEMENTATION.md and
AUDIT.md under `tasks/shadow-archives-webportal/owner-runtime-checkpoint-20260913/`.
The pre-existing modified AGENTS.md, GIT-AND-HANDOFF.md, WORKFLOW.md and untracked
templates/REPORT.md remain byte-identical and outside the commit; skills remain unchanged.

## Checks and adversarial self-audit

- Application checks on the checkpoint worktree: `npm run lint`, `npm run build`
  and `npm run format:check` passed. The full `npm test` run finished with
  **561/562 passed**: `HomePage.data.test.tsx` did not settle from its loading
  skeleton before its assertion for the `Redaction notes` link. A focused rerun
  of that file reproduced the same failure (**5/6 passed**). This is therefore
  an unresolved regression-test failure in the checkpointed revision, not a
  passing flake. It affects the test's async-settlement assertion only; the
  owner has separately accepted the real-host workflows. Fixing it is outside
  this checkpoint/documentation scope and must be the first follow-up before a
  release-quality automated gate is claimed.
- Workspace documentation check: `bash tools/validate-workspace.sh` passed
  (five existing human-review warnings).
- Application and workspace `git diff --check` passed before commit.

Scope review: file inventory and implementation reports match accepted verticals; no new source
implementation. Owner file hashes and all application source bytes are compared to the initial
baseline. No generated dist/release/node_modules files are tracked. Credential/private-key and
conflict-marker checks cover the staged text. Identity, pending-status supersession, source-vs-
runtime claims and exact remote branch hashes are checked separately. This is a bounded
checkpoint/documentation review, not a new independent feature/security audit.

A pre-existing Studio status sentence still calls Blog publishing a roadmap item
(`src/features/owner/StudioPage.tsx:248`). This is stale product copy, not a
failure of the accepted Blog workflow. It is recorded for later correction;
application source edits are outside this checkpoint task.

The existing project context links an unrelated untracked visual-correction report. It remains
locally resolvable but is not durable in this branch; it predates this task and was deliberately
excluded from accepted-feature staging. No new link depends on it.

## External actions and final state

APP_PUSH

Workspace branch: `agent/shadow-archives-webportal/owner-runtime-docs-20260913`.
Its exact commit is recorded in the orchestration STATUS.json and final handoff after push,
avoiding a self-referential commit SHA in this report.
Orchestration branch: `agent/shadow-archives-webportal/owner-runtime-handoff-20260913`.
No main merge/push, tag, release, deploy, QDN publication, transaction or feature change.

Report saved:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-13-owner-runtime-checkpoint.md`.
