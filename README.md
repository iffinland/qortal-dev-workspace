# Qortal Development Workspace

This repository is the canonical shared control and operational knowledge base
for AI-assisted Qortal development. It centralizes task routing, verified
global development rules, project context, reusable issue and handoff
templates, and thin agent role overlays.

It is the Qortal-specific successor to the earlier Qortium workspace. It was
built by studying `qortium-dev-workspace` as a structural and methodological
reference, then re-deriving every platform claim from current Qortal sources.
It is **not** a rename of that repository.

The durable cross-project rules are summarized in the
[Qortal dApp Development Standard](docs/architecture/qortal-dapp-development-standard.md).
Task execution follows
[Qortal Development Workflow v2](docs/workflows/workflow-v2.md), and source
ownership follows
[Source of Truth and Documentation Lifecycle](docs/governance/source-of-truth-and-lifecycle.md).

## Knowledge model

ChatGPT, DeepSeek and Codex share one global guide set under `agents/`; they do
not maintain separate copies. ChatGPT scopes, plans and reviews. DeepSeek is
the default cost-efficient local implementation agent: it investigates,
implements, validates locally and hands off. Codex is reserved for independent
audit, high-risk architecture and data-integrity review, repeated failure, and
final release-critical verification. GitHub provides durable collaboration
history, while local workspaces hold checked-out project and Qortal platform
repositories.

The canonical hierarchy is:

1. current checked-out Qortal Core (`Qortal/qortal`) rendered behavior and the
   current application host (Qortal Hub) for platform behavior;
2. each project's own source and durable documentation for implementation state;
3. root-level `projects/<project>.md` for shared project context;
4. global guides under `agents/` for reusable workflows; and
5. thin `agents/roles/` overlays for agent-specific operating constraints.

Facts must be labelled as verified, inferred, unknown, or requiring an owner
decision. Project-specific facts must not be promoted into global guidance.

## Qortal-specific platform model (summary)

These are the conclusions that make this workspace differ from a mechanical
Qortium port. Full evidence is in
[`agents/qortal-qdn-and-bridge.md`](agents/qortal-qdn-and-bridge.md) and the
[development standard](docs/architecture/qortal-dapp-development-standard.md).

- There is **no SSH tunnel** in the supported Qortal validation model, and none
  is required. Do not encode one.
- Q-Apps are JavaScript apps published to QDN under the `APP` (or `WEBSITE`)
  service and run **inside an iframe rendered by a host** (Qortal Hub or a
  gateway node). Qortal Core injects the `qortalRequest()` bridge and the
  `_qdn*` context variables into the rendered HTML.
- Qortal Core's node API is the same origin as the running Q-App in the normal
  case, so relative requests such as `/arbitrary/...` and `/names/...` are the
  verified read path.
- Actions are not simply "reads vs writes". Public/idempotent node reads are
  handled by `q-apps.js`; `GET_USER_ACCOUNT` and other account/authentication
  actions are **host-mediated and permissioned** (saved, session, or a user
  dialog that can be rejected); write actions are signed with host approval.
  See [`agents/qortal-qdn-and-bridge.md`](agents/qortal-qdn-and-bridge.md).
- Local development uses **Qortal Hub Developer Mode against a local Qortal
  node**, which starts a Core dev proxy (`POST /developer/proxy/start`) that
  injects the same bridge into a live Vite/other dev server.
- The production render path sets a restrictive CSP. Third-party origins are
  not generally available, and this constrains images, media and network
  design.
- `Qortal/qortal-ui` is archived and MUST NOT be treated as current authority.
- `Qortal/create-qortal-app` and `Qortal/qapp-core` are the current scaffolding
  and framework path, even though `create-qortal-app` has not been updated
  recently; verify their behavior against source rather than memory.

## Structure

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
│   └── roles/
│       ├── CHATGPT.md
│       ├── DEEPSEEK.md
│       └── CODEX.md
├── docs/
│   ├── architecture/
│   │   └── qortal-dapp-development-standard.md
│   ├── governance/
│   │   └── source-of-truth-and-lifecycle.md
│   ├── workflows/
│   │   ├── workflow-v2.md
│   │   ├── deepseek-primary-work-model.md
│   │   └── report-storage-policy.md
│   └── <project-slug>/          # canonical report root, created on demand
├── projects/
│   └── shadow-archives-webportal.md
├── templates/
│   ├── TASK-CONTROLLER.md
│   ├── PROJECT-CONTEXT.md
│   ├── AUDIT-ISSUE.md
│   ├── IMPLEMENTATION-ISSUE.md
│   ├── OWNER-HANDOFF.md
│   ├── DEEPSEEK-TASK.md
│   └── DEEPSEEK-REVIEW.md
└── tools/
    └── validate-workspace.sh
```

Two files are deliberately **not** copied from the Qortium reference:
`qavs-versioning-and-release.md` (QAVS is a Qortium-specific artifact with no
verified Qortal equivalent) is replaced by
[`agents/app-release-and-provenance.md`](agents/app-release-and-provenance.md),
and `qortium-home-and-bridge.md` is replaced by the Qortal-native
[`agents/qortal-qdn-and-bridge.md`](agents/qortal-qdn-and-bridge.md).

## Default agent workflow

```
ChatGPT scopes and reviews
→ DeepSeek investigates, implements and self-audits locally
→ owner/runtime validation in a real Qortal host
→ GitHub
→ Codex escalation when required
```

The full agent operating model, risk levels, and escalation rules are defined in
[`docs/workflows/deepseek-primary-work-model.md`](docs/workflows/deepseek-primary-work-model.md).

## Onboarding a project

Keep the project's source code and detailed implementation documentation in its
own repository. Create one root-level project context file from
[`templates/PROJECT-CONTEXT.md`](templates/PROJECT-CONTEXT.md), record verified
identity, architecture, dependencies, commands and validation requirements,
then route work through
[`agents/00-SESSION-START.md`](agents/00-SESSION-START.md). Add or change global
guidance only when a rule is reusable across Qortal projects.

## Report storage

AI-generated work reports (audits, investigations, implementations, reviews,
runtime diagnostics, validations, comparisons and owner handoffs) MUST be stored
under the canonical workspace report root:

```
<workspace-root>/docs/<project-slug>/
```

Application repository `docs/` directories are reserved for durable
source-controlled project documentation (architecture, user guides, API docs,
release instructions, migration specs).

See [`docs/workflows/report-storage-policy.md`](docs/workflows/report-storage-policy.md)
for the full policy, including directory layout, filename rules, and required
final report path disclosure.

## Workspace validation

Run:

```bash
bash tools/validate-workspace.sh
```

The checker is a **structural** gate. It verifies that the required workspace
files exist, that supported relative Markdown link forms resolve (inline links,
reference-style definitions and local heading anchors), and that a small,
hard-coded stale-platform marker is absent from active guidance. It exits
non-zero on a failed check or a checker execution error.

Passing it is **not** semantic proof. It does not prove that platform claims,
bridge contracts, authority rules or security guidance are correct. Semantic
review against current Qortal Core/Hub/framework source — and, where a claim
depends on it, live host evidence — remains a separate mandatory gate.
Historical reports under `docs/<project-slug>/` are treated as historical
evidence rather than active guidance by the stale-marker check.

## Public-repository boundary

Never store project source code, generated release artifacts, user data, or
confidential operational material here. Secrets, credentials, private keys,
wallet seeds, API keys, server credentials, and private infrastructure details
MUST NEVER be committed. Project source remains in its own repository.
