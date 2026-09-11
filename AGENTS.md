# Qortal Development Orchestration

This repository is the canonical shared control and knowledge repository for
Qortal development. It contains documentation and workflows, not project source
code or secrets.

## Mandatory operating contract

The canonical standard is the detailed source of truth; this is the minimum.

- Current Qortal Core, current Qortal Hub, and the current Q-App framework are
  the reference truth. Do not design platform behavior from memory.
- Do not assume a Qortium, legacy `qortal-ui`, or generic-web behavior applies
  to current Qortal. `Qortal/qortal-ui` is archived.
- There is no SSH tunnel in the supported Qortal validation model and none is
  required. Do not add one.
- Autonomous implementation must end with an adversarial self-audit and
  remediation of confirmed BLOCKER/HIGH findings.
- A green automated suite is not enough. Owner product/runtime validation in a
  real Qortal host is a separate gate before completion.
- Platform-boundary defects must be traced to the first confirmed mismatch and
  classified before any dApp workaround.
- Full-access execution does not imply commit/push/tag/release/publish/deploy/
  issue-closure authority; explicit owner authorization remains required.
- Reports are handoff artifacts and must follow the canonical report-storage
  policy. The final response MUST state the exact absolute saved report path.
- Task prompts are compact deltas with one primary objective and exit criterion;
  shared governance and project truth are referenced, not recopied.
- Agents must challenge unsupported premises or materially inferior requested
  methods with evidence and recommend the better bounded alternative.

Every substantial task MUST begin with
[`agents/00-SESSION-START.md`](agents/00-SESSION-START.md), then be classified
using
[`agents/01-TASK-CLASSIFICATION.md`](agents/01-TASK-CLASSIFICATION.md).
Execution follows
[`docs/workflows/workflow-v2.md`](docs/workflows/workflow-v2.md).
All Qortal dApp work MUST follow the shared
[`docs/architecture/qortal-dapp-development-standard.md`](docs/architecture/qortal-dapp-development-standard.md)
standard.
After classification, read:

1. the matching root-level `projects/<project>.md`;
2. only the relevant routed global guides; and
3. the acting agent's thin role overlay under `agents/roles/`, when applicable.

Global guides are shared and MUST NOT be duplicated per agent. Project-specific
facts belong only under `projects/`.

Keep verified facts, inference, unknowns, and owner decisions clearly separated.
Source ownership and conflict resolution follow
[`docs/governance/source-of-truth-and-lifecycle.md`](docs/governance/source-of-truth-and-lifecycle.md).

Agent selection and escalation follow
[`docs/workflows/deepseek-primary-work-model.md`](docs/workflows/deepseek-primary-work-model.md).

All AI-generated investigation, audit, implementation, review, runtime,
validation, comparison and owner-handoff reports MUST follow
[`docs/workflows/report-storage-policy.md`](docs/workflows/report-storage-policy.md).
The final response MUST state the exact absolute saved report path.
Agents MUST NOT invent an alternative report location.

## Legacy Qortal guidance

Legacy Qortal agent material was found in
`iffinland/iffi-vaba-mees-QORTAL/agents/` (`master-workflow.md`,
`qapp-framework-essentials.md`, `qortal-runtime-performance-rules.md`, and
others). It is **migration evidence only**. It is not routed to, not
authoritative, and MUST NOT be copied forward. Its reusable content is recorded
in [`agents/README.md`](agents/README.md); everything else is superseded by this
workspace.
