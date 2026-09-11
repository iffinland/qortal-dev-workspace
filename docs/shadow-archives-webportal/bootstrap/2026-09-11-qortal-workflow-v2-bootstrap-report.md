# Qortal Development Workflow v2 — Workspace Bootstrap Report

- Date: 2026-09-11
- Report type: bootstrap
- Project slug: `shadow-archives-webportal`
- Task: bootstrap the canonical Qortal Development Workflow v2 workspace and
  onboard the initial Shadow Archives project context.
- Agent: DeepSeek (primary local investigator/implementer)
- Status: **COMPLETE** (documentation/workflow bootstrap; see "Not verified")

## 1. Objective and exit criterion

**Objective.** Create the first complete Qortal-specific Workflow v2
development workspace, using `qortium-dev-workspace` as a structural and
methodological reference while replacing Qortium-specific platform assumptions
with verified Qortal-specific rules.

**Exit criterion.** The local `qortal-dev-workspace` contains a coherent,
internally consistent, Qortal-specific Workflow v2 system usable by ChatGPT,
DeepSeek and Codex, including initial project context for
`shadow-archives-webportal-QORTAL`, with all internal documentation references
validated and all platform claims either source-supported or explicitly marked
unknown.

**Result.** Met. No Shadow Archives application code was written.

## 2. Baseline

Captured before creating files:

- Repository: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`
- Remote: `https://github.com/iffinland/qortal-dev-workspace.git`
- Branch: `main`; **no commits yet**; `origin/main` gone; remote has no refs
  (`git ls-remote origin` empty; GitHub API `size: 0`).
- Local tree: only `.git` existed. Nothing to preserve; no owner changes.
- Application local path
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`:
  exists, empty, not a Git repository.
- Application remote `iffinland/shadow-archives-webportal-QORTAL`: exists,
  `size: 0`, no commits.
- Reference workspace `/home/iffi/VsCodec-Projects/Qortium/qortium-dev-workspace`:
  read-only inspection (7 project files, 14 guides, 3 workflows, 7 templates).

No `apply_patch` binary exists in this environment; files were created with
here-documents via the shell. This is an environment note, not a task result.

## 3. Qortal authority sources investigated

Read-only clones/reads on 2026-09-11. No external writes were made to any of
them.

| Source | Revision / observed date | What was read |
| ------ | ------------------------ | ------------- |
| `Qortal/qortal` (Core) | `108bf191d42d710ec617f535af30cfd82fc03c87`, v6.1.9, 2026-07-08 | `q-apps.js` bridge shim, `HTMLParser`, `RenderResource`, `DevProxyServerResource`, `DevProxyManager`, `ArbitraryDataRenderer`, `ArbitraryResource`, `NamesResource`, `Service`, `ArbitraryResourceStatus`, `Security`, `Settings`, `AppsResource`, `DeveloperResource` |
| `Qortal/Qortal-Hub` | `12a573b27246e8a626b24794830c6bc432d1b05d`, 2026-08-23 | `qortal-requests.ts` (request dispatch + action list), `get.ts` (publish, user account, delete hosted data, multi-publish), `AppViewer.tsx`, `apps` dev-mode UI, i18n dev-mode strings, package deps |
| `Qortal/qapp-core` | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df`, 1.0.79, 2026-05-25 | `global.ts` request types, `useAuth`, `useResources`, `useListData`, `usePublish`, request queues, caches |
| `Qortal/qapp-templates` | `143cc7bffd265f543f96ef25bf1b58ef7bb04472`, 2026-05-25 | `react-default-template` router/`GlobalProvider` pattern and dependency baseline |
| `Qortal/q-mail` | `ddf3aa928e0b51f89e2a6a7e86e5b44bdfd7b6d0`, 3.2.1, 2026-05-28 | `MAIL`/`MAIL_PRIVATE` usage, identifier convention, encrypted multi-publish |
| `Qortal/q-tube` | `68c3ea706c4ab110ffa44a7f55f8e09bdf7e85ff`, 2.1.0, 2026-07-15 | media services, router pattern, DOMPurify |
| `Qortal/Quitter` | `4e4246c3283bcbc8e05e683260692ed36144f862`, 2026-05-25 | like/engagement model, unlike by overwrite |
| `Qortal/Subwire` | `a933a6c44d60db19cd219408e36c747aebcce994`, 2026-06-27 | list/index resources, IndexedDB caches, search usage |
| `Qortal/create-qortal-app` | `ea9d720bb31fa42b777659aceccd69ad20393abb`, 2025-05-12 | scaffolding CLI |
| `Qortal/Q-Apps-Utils` | `67af8f38b2cb7f44434255a9ed1eb298822c8330`, 1.5.0, 2024-07-17 | legacy utility library (not current authority) |
| `Qortal/qortal-ui` | archived, 2025-06-14 | confirmed deprecated after Core 5.0 |
| `Qortal/chrome-extension` | not archived | confirmed current host family |
| `Qortal/qortal-mobile` | not archived | confirmed current host family |
| `iffinland/iffi-vaba-mees-QORTAL` | `64f55bf7b6f4a1a093f19413d3a985e61a9fad37`, 2026-06-11 | reference app patterns and anti-patterns |
| `https://qortal.dev/docs/q-apps` | fetched 2026-09-11 | services, routing, identifier guidance, link protocol |
| Qortal org repository inventory | GitHub API, 2026-09-11 | current vs archived repos |

## 4. Important platform conclusions

All below are VERIFIED against the sources above unless marked otherwise.

1. **No SSH tunnel.** Qortal local validation uses a local node plus Qortal Hub
   Developer Mode, which calls `POST /developer/proxy/start` to run a Core dev
   proxy that injects the bridge into a live dev server. SSH is not part of the
   model.
2. **Bridge injection is Core's job.** Core injects `/apps/q-apps.js` and the
   `_qdn*` variables (`_qdnContext`, `_qdnTheme`, `_qdnLang`, `_qdnService`,
   `_qdnName`, `_qdnIdentifier`, `_qdnPath`, `_qdnBase`, `_qdnBaseWithPath`)
   into rendered HTML.
3. **Q-Apps run in a host iframe** at the node's `/render/{service}/{name}`
   route; reads are same-origin node API calls handled by `q-apps.js`; writes
   are forwarded to the host for approval/signing.
4. **Documentation/source discrepancy.** The public API page documents only two
   `_qdn*` variables; source injects nine. Source wins.
5. **CSP constrains the design.** The render path sets
   `default-src 'self' 'unsafe-inline' 'unsafe-eval'; font-src 'self' data:;
   media-src 'self' data: blob: http://127.0.0.1:* http://localhost:*;
   img-src 'self' data: blob:; connect-src 'self' wss: blob:`. Third-party
   HTTPS APIs/image CDNs are not available by default.
6. **Node API defaults** are 12391 (mainnet) / 62391 (testnet), configurable.
7. **Identity is name ownership.** Resource ownership belongs to a registered
   name; `_qdnName` identifies the app's publisher name and is percent-encoded
   for spaces. `GET_USER_ACCOUNT` returns only address + public key.
8. **QDN has no on-chain delete.** `DELETE_HOSTED_DATA` removes only local
   hosted data and is refused on public/gateway nodes; current apps implement
   "unlike" as an overwrite/tombstone.
9. **Search cannot do body search.** `/arbitrary/resources/search` covers name,
   identifier, title and description metadata; body search needs an app index.
10. **N+1 discovery is the main scale risk.** Current mitigations:
    paginated search with `includestatus`/`includemetadata`, batched
    `POST /names/list`, `qapp-core` request queues, IndexedDB caches with TTLs,
    and `LIST`/`JSON` catalog resources.
11. **Current stack:** React 19 + TypeScript + Vite + `react-router-dom` 7 +
    `@mui/material` 7 + `qapp-core`, with `createBrowserRouter` using
    `window._qdnBase` as `basename` and Vite `base: ''`.
12. **Q-Mail interop is a convention, not Core API.** Mail is published as an
    encrypted `MAIL_PRIVATE` resource under the sender's name with a
    recipient-encoding identifier; recipients search
    `qortal_qmail_<name>_<addressLast6>_mail_`. `SEND_CHAT_MESSAGE` is chat, not
    mail. Must be re-verified against the current Q-Mail release.
13. **`Qortal/qortal-ui` is archived** and must not be treated as authority;
    `create-qortal-app` and `Q-App-Utils` are stale (2025-05-12 / 2024-07-17).

## 5. Workspace structure created

```text
qortal-dev-workspace/
├── README.md
├── AGENTS.md
├── agents/
│   ├── README.md
│   ├── 00-SESSION-START.md
│   ├── 01-TASK-CLASSIFICATION.md
│   ├── qortal-native-app-workflow.md
│   ├── qortal-architecture-and-data-integrity.md
│   ├── qortal-qdn-and-bridge.md
│   ├── qdn-publication-discovery-and-scaling.md
│   ├── runtime-diagnostics-and-performance.md
│   ├── live-qdn-validation.md
│   ├── issue-driven-audit-and-refactor.md
│   ├── app-release-and-provenance.md
│   ├── git-generated-files-and-hygiene.md
│   ├── final-report-and-owner-handoff.md
│   └── roles/{CHATGPT,DEEPSEEK,CODEX}.md
├── docs/
│   ├── architecture/qortal-dapp-development-standard.md
│   ├── governance/source-of-truth-and-lifecycle.md
│   ├── workflows/{workflow-v2,deepseek-primary-work-model,report-storage-policy}.md
│   └── shadow-archives-webportal/bootstrap/<this report>
├── projects/shadow-archives-webportal.md
├── templates/{TASK-CONTROLLER,PROJECT-CONTEXT,AUDIT-ISSUE,IMPLEMENTATION-ISSUE,OWNER-HANDOFF,DEEPSEEK-TASK,DEEPSEEK-REVIEW}.md
└── tools/validate-workspace.sh
```

Deliberate deviations from the target layout:

- `qavs-versioning-and-release.md` was **not** carried over (QAVS is a
  Qortium-specific artifact with no verified Qortal equivalent) and is replaced
  by `agents/app-release-and-provenance.md`.
- `qortium-home-and-bridge.md` is replaced by the Qortal-native
  `agents/qortal-qdn-and-bridge.md`.
- `agents/issue-driven-audit-and-refactor.md` was retained because it is a
  reusable Workflow v2 capability.
- `tools/validate-workspace.sh` was added; see §7.

## 6. Files created

All files are new; nothing was modified or deleted.

Root: `README.md`, `AGENTS.md`.

`agents/`: `README.md`, `00-SESSION-START.md`, `01-TASK-CLASSIFICATION.md`,
`qortal-native-app-workflow.md`, `qortal-architecture-and-data-integrity.md`,
`qortal-qdn-and-bridge.md`, `qdn-publication-discovery-and-scaling.md`,
`runtime-diagnostics-and-performance.md`, `live-qdn-validation.md`,
`issue-driven-audit-and-refactor.md`, `app-release-and-provenance.md`,
`git-generated-files-and-hygiene.md`, `final-report-and-owner-handoff.md`.

`agents/roles/`: `CHATGPT.md`, `DEEPSEEK.md`, `CODEX.md`.

`docs/architecture/`: `qortal-dapp-development-standard.md`.
`docs/governance/`: `source-of-truth-and-lifecycle.md`.
`docs/workflows/`: `workflow-v2.md`, `deepseek-primary-work-model.md`,
`report-storage-policy.md`.

`projects/`: `shadow-archives-webportal.md`.

`templates/`: `TASK-CONTROLLER.md`, `PROJECT-CONTEXT.md`, `AUDIT-ISSUE.md`,
`IMPLEMENTATION-ISSUE.md`, `OWNER-HANDOFF.md`, `DEEPSEEK-TASK.md`,
`DEEPSEEK-REVIEW.md`.

`tools/`: `validate-workspace.sh`.

This report:
`docs/shadow-archives-webportal/bootstrap/2026-09-11-qortal-workflow-v2-bootstrap-report.md`.

Total: 33 files (32 workspace files + this report). Markdown totals 4,315 lines
including this report; 4,444 lines including the validator script.

## 7. Validation performed

| Check | Command | Result |
| ----- | ------- | ------ |
| Required files present | `bash tools/validate-workspace.sh` | PASS |
| Relative Markdown links resolve | `bash tools/validate-workspace.sh` | PASS — 159 relative links across 32 files, 0 broken |
| Stale platform assumptions (hard-fail list: retired Qortium preview endpoint) | validator | PASS — none |
| Hygiene scan (Qortium/SSH/QAVS/ports/qortal-ui) | validator | PASS with 5 review warnings, all legitimate comparative statements |
| Trailing whitespace | `grep -rnE ' +$'` | none |
| Tabs | `grep -rnP '\t'` | none |
| CRLF | `grep -rlU $'\r'` | none |
| Conflict markers | `grep -rnE '^(<<<<<<<|=======\|>>>>>>>)'` | none |
| Git baseline | `git status`, `git ls-remote origin` | no commits; remote empty |
| Whitespace diff check | `git diff --check` | rc=0 (no tracked files yet) |
| Reusable-fact placement | manual | Q-Mail interop, identity, CSP, N+1 present in global guides |
| Project leakage | `grep -ri shadow` outside project scope | clean after remediation (see §8) |
| Bridge action names | compared all backticked ALL-CAPS tokens against Core `q-apps.js` + Hub request list | no invented actions |

Not run and reported as such:

- No Qortal node or Hub was available in this environment (no listener on
  12391/62391, no `~/.qortal`), so **no live node-API, Hub-host or QDN
  validation was performed**. This is a documentation/bootstrap task; no
  runtime claim is made.
- No `npm` install/build was run; no application source exists yet.
- `create-qortal-app` was not executed, so its current template resolution is
  unverified (recorded as UNKNOWN).

## 8. Adversarial self-audit

Performed after the first validation pass. Categories checked: copied Qortium
rules, obsolete `qortal-ui` assumptions, invented bridge actions, unsupported
QDN semantics, missing authority boundaries, duplicated governance, broken
links, contradictory role instructions, false live-validation claims, SSH
assumptions, hidden commit/push authority, and project leakage.

Findings and remediation:

| # | Severity | Finding | Remediation |
| - | -------- | ------- | ----------- |
| 1 | HIGH | Broken relative link from the architecture standard to `agents/runtime-diagnostics-and-performance.md` (`../agents/...` instead of `../../agents/...`). | Fixed; validator now passes with 0 broken links. |
| 2 | MEDIUM | Shadow Archives identifier example (`shadowarchives_`) appeared in two reusable global guides, leaking project naming into the standard. | Replaced with neutral `myapp_` in both guides. |
| 3 | MEDIUM | Reusable Q-Mail interop facts existed only in the project file, violating "reusable Qortal facts must not be project-only". | Added a reusable "Mail and messaging interop" section to `agents/qortal-qdn-and-bridge.md`. |
| 4 | MEDIUM | Owner-detection guidance omitted that Core percent-encodes spaces in `_qdnName` (`iffi vaba mees` → `iffi%20vaba%20mees`), a likely identity-comparison bug. | Added the verified detail to the bridge guide and the project file. |
| 5 | MEDIUM | The bridge guide listed an unverified `_qdnContext` value ("site-map"). | Corrected to the verified set: `render`, `proxy`, `gateway`, `domainMap`. |
| 6 | LOW | The bridge guide implied `_qdnService` is empty in proxy context; it is actually `APP`. | Corrected to name/identifier/base empty, service `APP`. |
| 7 | LOW | Potential ambiguity about whether SSH could ever be a project rule. | Explicitly scoped in workflow-v2: project-specific infrastructure is not a generic Qortal rule. |

Confirmed absent after remediation: copied Qortium platform rules presented as
Qortal truth; obsolete `qortal-ui` assumptions; invented bridge actions;
unsupported QDN semantics; missing authority boundaries; duplicated governance;
broken relative links; contradictory role instructions; false live-validation
claims; SSH requirements; hidden commit/push authority; Shadow Archives product
details in reusable standards.

No in-scope BLOCKER findings were identified. All confirmed HIGH/MEDIUM findings
were remediated, and validation was re-run afterwards.

## 9. Unresolved unknowns

- The app's Qortal publishing name, service (`APP` vs `WEBSITE`) and identifier
  prefix are undecided.
- `create-qortal-app` current template resolution is unverified (not executed).
- `Qortal/Q-Apps` (referenced by the old `Q-Apps-Utils` README) is not publicly
  resolvable; treat that reference as stale.
- Q-Mail's identifier/payload convention was verified only against Q-Mail 3.2.1;
  the current release may differ.
- Core default-branch HEAD was `108bf19` (2026-07-08) on 2026-09-11, but the
  repository had newer pushes on other branches; re-verify before
  platform-dependent work.
- Whether Core's `Category` enum or free-form tags (or both) will be used for
  shared taxonomy.
- Editor/sanitization choice for owner publishing.

## 10. Owner decisions still required

1. Publishing name, service and identifier prefix for Shadow Archives.
2. Whether owner controls extend beyond the publishing name (delegated
   moderators).
3. Taxonomy model: Core `Category` enum, free-form shared tags, or both.
4. Owner-publishing editor choice and stored rich-text schema.
5. Contact-form Q-Mail fallback behavior and user-facing success feedback.
6. Performance baseline targets after measurement.
7. Whether report files (`docs/<project-slug>/`) should be committed to this
   repository or kept untracked.
8. Verified `qortal://` targets (names/identifiers) for Q-Tube, SubWire and
   Quitter.

## 11. Git status, commit state, push state

Git status (2026-09-11):

```
On branch main

No commits yet

Untracked files:
	AGENTS.md
	README.md
	agents/
	docs/
	projects/
	templates/
	tools/
```

- Commit state: **not committed.** `main` has no commits.
- Push state: **not pushed.** `git ls-remote origin` returns no refs; the remote
  repository is empty.
- Tags/releases/publications: none.
- No QDN resource was published or mutated.
- No GitHub issue/PR/project was mutated.
- No destructive Git command was used.

## 12. Final status

**COMPLETE.** The Qortal-specific Workflow v2 workspace and the initial Shadow
Archives project context exist, are internally consistent, pass the workspace
validator, and contain no unresolved in-scope BLOCKER/HIGH finding.

Remaining work requires owner input (see §9–§10) before any Shadow Archives
application implementation begins. Per the task boundary, no application
implementation was started.

Report saved:
/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/bootstrap/2026-09-11-qortal-workflow-v2-bootstrap-report.md
