# Independent Workflow v2 pre-commit audit

Date: 2026-09-11. Auditor: Codex, independent of the bootstrap implementer.

**CHANGES REQUIRED BEFORE INITIAL COMMIT**

Repository: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`.

Primary class: governance/documentation audit, with platform-contract and security review. Risk level: LEVEL 3 independent audit. Objective: assess the first canonical commit, not implement Shadow Archives. Acceptance: complete repository review, independent critical-source checks, validator/Git/link/hygiene checks, and an evidence-based verdict. No application runtime is required to complete this documentation audit.

## Findings summary

| Severity | Count | Findings |
| --- | ---: | --- |
| BLOCKER | 0 | None |
| HIGH | 2 | H1 account approval/retries; H2 shared rich-text security boundary |
| MEDIUM | 7 | M1 publication revision evidence; M2 API field mapping; M3 ZIP support; M4 validator limitations; M5 engagement semantics; M6 owner-decision hierarchy; M7 project leakage |
| LOW | 1 | L1 archive-date provenance |
| INFO | 3 | I1 preserved baseline; I2 applicable validation; I3 report policy and references |

HIGH findings require a separate correction task before initial commit. No original file was edited. This report is the only workspace addition.

## HIGH findings

### H1 — Account authentication is incorrectly classified as approval-free and automatically retryable

**Location:** `agents/qortal-qdn-and-bridge.md:85-94`, particularly lines 87-90. Also reconcile its runtime-model blanket read/write split at lines 52-53 and the summaries in README/standard/bootstrap.

**Evidence:** The guide explicitly includes `GET_USER_ACCOUNT` among reads that need no approval and can be retried. At the independently verified current Hub revision, `src/qortal/get.ts:529-600` checks saved and session permissions, otherwise calls `getUserPermission`, and returns the address/public key only when accepted or previously permitted. Rejection is an error. Core `src/main/resources/q-apps/q-apps.js:795-805` gives this action an hour-long timeout specifically because the user may be deciding a popup. The standard itself already acknowledges remembered account permission at lines 135-138. `GET_PRIMARY_NAME` is also handled by Hub (`qortal-requests.ts:2723`), so “all reads handled locally” is not an accurate dispatch rule.

**Consequence:** A conforming wrapper could apply short background-read deadlines and automatic retries to an outstanding authentication dialog, or retry a deliberate denial. This is an actual privacy/consent and integration-boundary error, not a naming preference. It does not mean the host can be bypassed; the host still enforces approval.

**Minimal remediation:** Distinguish public node reads, permissioned host reads/authentication, and signed writes. Make account access an explicit, deduplicated authentication operation with permission-appropriate waiting and a denial state. Never automatically retry user rejection or an unresolved approval request. Reconcile the short summaries by referencing the authoritative classification. Retain bounded retries for genuinely idempotent public reads.

**Correction acceptance:** Source-linked action classification and wrapper guidance consistently describe first-time approval, remembered approval, rejection, and an unresolved request. No application implementation or live transaction is needed for this documentation correction.

### H2 — Shared security guidance omits the rich-text rendering boundary

**Location:** `agents/qortal-architecture-and-data-integrity.md:62-70` and its validation section; `docs/architecture/qortal-dapp-development-standard.md:152-179`. Relevant project-only text: `projects/shadow-archives-webportal.md:191-212`.

**Evidence:** Shared guidance marks payloads untrusted but prescribes schema validation only. Complete searches of `agents/`, `docs/architecture/`, and `templates/` found no sanitization/XSS/HTML-rendering rule. The project context mentions safe rendering and DOMPurify as observations, but does not establish a reusable cross-project security contract. Current Core `ArbitraryDataRenderer.java:183-191` permits inline script and eval in its CSP. A valid JSON payload with an HTML string can satisfy its schema while carrying executable event attributes or unsafe URLs. Current Q-Tube `src/components/common/TextEditor/DisplayHtml.tsx:15-33` explicitly sanitizes before its HTML sink, confirming this is a separate layer in the reference implementation.

**Consequence:** A future application can satisfy the documented shared schema/identity checks while rendering another publisher's executable rich text. Script running in the app can alter UI and invoke its bridge; host signing approval is not an HTML sanitization defense. This is a gap in the proposed canonical security authority, not a claim that the nonexistent Shadow Archives app currently has an exploit.

**Minimal remediation:** Add one shared, routed requirement for safe rendering: escape plain text; sanitize untrusted HTML with a maintained sanitizer or use a constrained safe document renderer; validate URL protocols and media/link transformations; ensure transformations do not reintroduce unsafe markup after sanitization. Apply it to comments, owner/imported content, previews, and stored/cached content. Add malicious HTML/URL fixtures to the relevant validation checklist. Reference that rule from project context; editor selection can remain undecided.

**Correction acceptance:** Shared guidance makes schema validation, publisher authority, and rendering safety distinct checks; explicitly covers script/event handlers and unsafe URL schemes. A framework/editor rewrite is neither required nor authorized.

## MEDIUM findings

### M1 — Publication checks can accept the old version of an updated resource

Locations: standard lines 144-145; `agents/live-qdn-validation.md:64-70`; publication guide §3. The standard singles out resource status; the detailed checklist requires schema and metadata correctness but not the submitted revision/content. Core `ArbitraryDataResource.java:90-145` reports availability/build status of the resource known to that node; `ArbitraryResourceStatus.java` has no submitted-transaction identity. An existing resource A can remain READY and schema-valid while update B is absent or unconfirmed. This counterexample follows from source; it was not exercised live.

Require comparison with the intended update (content hash, version/operation identifier or exact relevant content), and transaction confirmation when claiming confirmation. Keep availability, submission, confirmation and intended-content verification separate. The release guide already requires expected content, mitigating but not eliminating this conflict. Severity is MEDIUM because the fuller release process supplies part of the missing protection.

### M2 — Node query names are incorrectly presented as bridge argument names

Location: `agents/qdn-publication-discovery-and-scaling.md:79-84`; repeated camel/lowercase ambiguity in standard §9 and project scalability examples. The list explicitly covers both the node endpoint and `SEARCH_QDN_RESOURCES` but uses `includestatus`, `includemetadata`, `exactmatchnames`, `minlevel`, and `namefilter`, with `name` described as a list. Core `q-apps.js:498-555` reads `includeStatus`, `includeMetadata`, `exactMatchNames`, `minLevel`, `nameListFilter`, and `names` for a list (`name` is singular). Lowercase bridge fields are silently ignored. The bridge guide's own camelCase warning is correct but conflicts with the list.

Use a small API-to-bridge mapping, or label this list node-only and point to the bridge contract. Explain that search identifier matching is substring/prefix matching, not exact identity: Core `HSQLDBArbitraryRepository.java:1153-1158`. Filter returned service/name/identifier exactly when correctness depends on identity; distinguish null/default identifiers. This prevents incomplete metadata, accidental name matches and incorrect scoped counts.

### M3 — Current in-app multi-file ZIP publication is overlooked

Locations: `agents/qdn-publication-discovery-and-scaling.md:45-46`; `agents/app-release-and-provenance.md`, §5. Current Hub `src/qortal/get.ts:1646,1797-1809,2206,2288-2312` accepts `isMultiFileZip` in both single and multi-resource publication and selects `uploadType: 'zip'`. Thus the blanket statement that in-app multi-file publication is not generally available omits a supported current path.

Document this as source-supported for the inspected Hub revision, with host approval and ZIP/root-layout requirements. Keep actual successful publication unverified until an authorized runtime test. It remains reasonable to recommend Hub's publishing UI as a workflow choice; do not justify it with an obsolete platform limitation.

### M4 — Validator PASS is narrower than its advertised guarantees

Locations: `tools/validate-workspace.sh:68-99,103-126`; README “Workspace validation”. The script strips heading fragments, only recognizes inline links, and its only hard-failing stale-platform check is a literal retired-port token. SSH and legacy-host claims are warning-only regardless of meaning. It scans historical reports as if they were active guidance, so an honest quotation of that retired token would fail too.

Independent fixtures in a disposable copy, without modifying this repository:

| Fixture | Actual exit/result |
| --- | --- |
| Missing inline file target | 1 / FAIL, correctly |
| Existing file with nonexistent heading | 0 / PASS |
| Reference-style link to missing file | 0 / PASS |
| Explicit rule requiring an SSH tunnel and current legacy UI | 0 / PASS with review warnings |

Scratch fixture root: `/tmp/qortal-validator-audit-3cpr9dny` (not a canonical report location; test inputs only).

Scope the output/README to structural checks and explicitly require semantic review. Validate the link forms actually supported/allowed, including anchors; fail on checker execution errors. Separate active-guidance checks from historical evidence. Do not attempt to replace source review with increasingly broad word bans. Existing repository links independently pass; this is a checker-quality finding, not a claim of current broken links.

### M5 — Engagement guidance loses essential distinctions from its references

Locations: standard §10, particularly lines 257-268; architecture guide lines 74-81; project engagement rules.

The standard equates like count with the number of matching resources while also prescribing tombstone overwrites. Current Quitter `src/utils/postQdn.ts:1933-1980` delegates unlike to framework deletion; qapp-core `src/hooks/useResources.tsx:696-715` republishes a placeholder, and discovery at lines 275-277 and 390 filters its convention before counting. Raw search-resource count is therefore not active-like count. The project says one like per Qortal user; the global rule says per acting name, while one account can own multiple names. These are not equivalent. Also, a blanket “actor owns the target” check cannot apply to liking/commenting on another author's post; it must apply to the operation resource being edited, with separately validated parent linkage. Tips and shares should not universally be described as published QDN records: their transport is operation-specific.

Require explicit active/tombstone validation and exact target identity; keep the framework's size convention revision-scoped, not a Core rule. Record the name-versus-account product decision without silently changing the owner requirement. Clarify entity ownership versus operation ownership and avoid prescribing QDN publication for every interaction.

### M6 — Project-state truth is mixed with owner-decision authority

Location: `docs/governance/source-of-truth-and-lifecycle.md:35-46` and conflict handling. Source/Git history and project context outrank documented owner decisions under a combined “behavior and decisions” heading. This mirrors the methodological workspace, but source establishes implemented behavior, not desired behavior or permission. Read literally, an existing implementation can defeat an explicit product decision. Workflow v2's owner-retains-decisions rule mitigates this, hence MEDIUM.

Separate factual implementation-state precedence from product/authorization precedence. Owner decisions control intended behavior and authorized changes; conflicting code is evidence of a gap. Do not use this clarification to override platform facts.

### M7 — Shadow Archives external-link preference leaks into global guidance

Location: `agents/qortal-qdn-and-bridge.md:165-175`; compare project “Links” owner decisions. The global guide adopts copying HTTP(S) links as the workspace-wide working assumption. This is a product interaction choice, not a consequence of Core's asset/connect CSP or a general Qortal requirement.

Keep the copy-to-clipboard requirement in Shadow Archives context. Globally require an explicit project policy and verified host support. The permissionless-content safety requirements remain global.

## LOW finding

### L1 — Archive date is inaccurate in bootstrap provenance

The bootstrap source table associates qortal-ui's archived state with 2025-06-14. The current [GitHub repository banner](https://github.com/Qortal/qortal-ui) says archived July 5, 2025. Its README supports deprecation after Core 5.0. The substantive exclusion is correct. Record the date correction in the correction report rather than rewriting historical evidence as though originally verified correctly.

## Positive findings and scope coverage

- **I1 Git/independence:** Baseline is unborn `main`, no tracked/staged files, 33 untracked files (32 Markdown plus validator), 174,302 bytes. No symlinks, generated application output, ignored files, or recognizable private-key/token signatures were found in the inspected content. The secret scan is limited, not a guarantee. All original files were read. No commit, push, tag, release, deployment, publication, transaction, issue/PR mutation, or application edit occurred.
- **I2 Validation applicability:** Workflow v2 correctly distinguishes applicable validation layers, names unavailable required evidence and forbids substitution with mocks. No SSH requirement survives in active Qortal guidance. Documentation audit completion does not require a running node; actual application-runtime acceptance remains a later gate. The bootstrap was right not to invent node/host evidence.
- **I3 Structure/report policy:** All seven templates and routed files exist. Roles are thin and share the same guides. Source authority is subject-scoped to Core, Hub and framework; current apps are references, not Core contracts. The report root is coherent and explicitly authorized by this task. Whether reports enter the initial commit remains an owner choice, not an audit prerequisite.
- Independent source inspection supports bridge/context injection, render versus proxy identity differences, Core's render CSP, APP fallback routing versus WEBSITE handling, configurable mainnet/testnet defaults, local-node dev proxy and its POST-body TODO, registered-name update ownership, local-hosted deletion versus chain history, metadata-only Core search, batched name lookup, framework queues, template/router baseline, and current-app TTL examples.
- Q-Mail is properly marked an app convention requiring re-verification, not SEND_CHAT_MESSAGE. The inspected mail code has name truncation/normalization and alias variants; the summary is not a complete interoperability specification. Retain the explicit implementation-time verification gate.
- Shadow Archives source directory remains empty. Its publishing identity, taxonomy, editor, mail fallback and performance baseline are undecided and generally labeled appropriately. No schema or complete application architecture has been invented. M5 identifies the user/name choice that still needs clarification.
- No current Qortium Home APIs, QAVS mandate or fixed Qortium runtime endpoint was found masquerading as Qortal. Methodology reuse is appropriate; the owner-decision hierarchy and clipboard preference need the specific corrections above.

## Source provenance

All source inspection is static evidence, not live Qortal runtime validation. Existing source clones under `/tmp/qortal-investigation/` were read, not changed. Their Git trees were clean. Core and Hub remote HEADs were independently queried on this audit date and match these revisions:

| Repository | Inspected revision | Main source locations inspected |
| --- | --- | --- |
| Qortal/qortal | `108bf191d42d710ec617f535af30cfd82fc03c87` | q-apps.js; HTMLParser; ArbitraryDataRenderer; DevProxyServerResource; ArbitraryDataResource; ArbitraryResourceStatus; HSQLDBArbitraryRepository; Service; NamesResource; ArbitraryTransaction; Settings |
| Qortal/Qortal-Hub | `12a573b27246e8a626b24794830c6bc432d1b05d` | src/qortal/get.ts; qortal-requests.ts; AppsDevModeHome.tsx and dev-mode strings |
| Qortal/qapp-core | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` | useResources.tsx; useListData.tsx; queue/export/IndexManager references |
| Qortal/qapp-templates | `143cc7bffd265f543f96ef25bf1b58ef7bb04472` | react-default-template package and starter layout |
| Qortal/create-qortal-app | `ea9d720bb31fa42b777659aceccd69ad20393abb` | index.js: current template repository discovery and degit path |
| Qortal/Quitter | `4e4246c3283bcbc8e05e683260692ed36144f862` | useLikeCount; useHasLiked; postQdn unlike; Post consumer |
| Qortal/q-tube | `68c3ea706c4ab110ffa44a7f55f8e09bdf7e85ff` | DisplayHtml and video-content rendering |
| Qortal/Subwire | `a933a6c44d60db19cd219408e36c747aebcce994` | primaryNamesCache; profileCache; articleQdn list references |
| Qortal/q-mail | `ddf3aa928e0b51f89e2a6a7e86e5b44bdfd7b6d0` | Mail/AliasMail discovery; message rendering and textContentV2 references |

The legacy utility/reference-app clone revisions were checked for baseline provenance only, not relied on as present-day platform authority. Current qortal-ui archival/deprecation was checked on its public GitHub page. The Q-Apps documentation fetch timed out; it was not treated as freshly verified. Framework/app remote HEADs and deployed release parity were not independently refreshed.

Methodological reference inspected: Qortium workspace's workflow-v2.md, source-of-truth-and-lifecycle.md and report-storage-policy.md. Historical memory was used only to locate that methodology; current local documents supplied the comparison. All 33 Qortal workspace files, including bootstrap, every template and all role overlays, were read.

## Commands and checks

- `pwd`; `rg --files --hidden -g '!.git'`; complete file reads and targeted `rg`/`nl`/`sed` source tracing.
- `git status --short --branch`, `git status --porcelain=v1 --untracked-files=all`, `git status --ignored --short`, `git remote -v`, `git ls-files`, `git diff --stat`, `git diff --cached --stat`: unborn main, no tracked/staged content, all workspace content untracked.
- `git diff --check` and `git diff --cached --check`: pass, but vacuous for this untracked baseline. Independent per-file `git diff --no-index --check /dev/null <file>` covered all 33 original files: no whitespace errors.
- Python full-tree inventory, content hashes, trailing whitespace/conflict/CRLF checks, symlink scan and limited secret-signature scan: no findings. A source-inventory loop encountered the intentionally empty application clone's missing HEAD after successfully checking all 11 populated clones; this is not a source-check success for that empty clone.
- `bash -n tools/validate-workspace.sh`: pass. `bash tools/validate-workspace.sh`: PASS, 5 review warnings, 159 file-link checks across 32 Markdown files before this report. Warning categories manually reviewed.
- Independent inline-link and anchor check: 160 destinations, zero broken. Isolated validator fixtures produced the results in M4. No fixture was placed in the workspace.
- `git ls-remote` Core HEAD, Hub HEAD and workspace origin: initially failed sandbox DNS; approved read-only retry succeeded. Core/Hub hashes above; workspace origin returned zero refs.
- Public web reads: qortal-ui page succeeded; API commit URLs and large Hub source page were unavailable through the web tool. Local clean source plus successful remote HEAD checks supplied Core/Hub evidence instead.
- No npm install/build, node API, browser-host, QDN publication or owner application acceptance was attempted. They are not required for this audit's exit criterion.

## Disagreement with the bootstrap self-audit

The bootstrap's overall COMPLETE/internal-consistency/no-missing-boundaries conclusion is not supported. H1 is a direct source contradiction; H2 is a missing shared security gate. Its “unsupported QDN semantics absent” conclusion misses M1-M3 and M5; its no-project-leakage conclusion misses M7. Validator PASS does not resolve these. The reported successful structural checks, lack of application code, absence of external writes and honest unavailable-runtime disclosure are consistent with this independent inspection. A broken ordinary documentation link alone would not normally merit HIGH; this audit grades by consequence rather than copying the bootstrap's severity choices.

## Remaining unknowns and handoff

No deployed host/Core parity, real account interaction, runtime owner detection, live publication/update, or Q-Mail delivery has been proven here. No scaffold CLI was executed. The original full product brief was not supplied, so completeness of every recorded owner decision against that original brief cannot be independently certified. The publishing identity, editor, taxonomy, contact fallback, account-versus-name engagement semantics and measured performance baseline remain application-design inputs.

A separate DeepSeek documentation correction task should address H1/H2 and reconcile the concrete MEDIUM contradictions without implementing Shadow Archives or changing platform source. Then rerun structural checks and independently review the correction diff. Owner authorization is still required for any initial commit/push.

Final Git state: unborn `main`; origin `https://github.com/iffinland/qortal-dev-workspace.git`, zero advertised refs at audit time. All original 33 files remain untracked and unchanged; this untracked report brings the tree to 34 files. Nothing staged, committed or pushed.

Report saved: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/audits/2026-09-11-independent-workflow-v2-pre-commit-audit.md`.
