# HomePage loading-skeleton test maintenance — qortal/shadow-archives-webportal

Executing agent (registered role of the agent that actually produced this work): Codex
Report/handoff writer (if different from the executing agent): Codex
Executing-agent evidence (how the real executor was established): This report records the source investigation, patch, and local validation executed in this Codex task.
Report type: maintenance handoff
Exact application repository / branch / SHA: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`, `agent/shadow-archives-webportal/homepage-test-maintenance-20260915`, `980c5ad2517675b3da23209579bd9130e0fac6e9`
Canonical report path / SHA-256 / authorized remote evidence: this file; SHA-256 not required for this Git-tracked report; application branch push remote-verified at the SHA above.

## Objective and exit criterion

Resolve the persistent `HomePage.data.test.tsx` loading-skeleton failure without changing accepted runtime behavior. The exit criterion was five focused passing runs, a clean full automated suite, typecheck, lint, format check, build, and `git diff --check`.

## Evidence by layer (command/action, environment, timestamp, result)

- Focused Vitest file in the isolated application worktree: five consecutive runs of `npm test -- src/features/home/HomePage.data.test.tsx --reporter=dot` passed, 6/6 tests each.
- Full automated suite in the same worktree: `npm test` passed, 57 files and 632 tests.
- Static/build checks in the same worktree: `npm run typecheck`, `npm run lint`, `npm run format:check`, `npm run build`, and `git diff --check` all passed.

## Root cause and smallest correction

The published-render test awaited the `Latest Posts` region, but that region is intentionally rendered immediately with the loading skeleton. It then synchronously queried the loaded `Redaction notes` link before the injected asynchronous archive loader had settled. This was a racy test assertion, not an application async-settlement bug, shared-state leak, fixture lifecycle issue, or runtime regression.

The correction changes that one query to Testing Library's asynchronous `findByRole`, retaining the exact content assertion and removing no coverage. It does not alter application code, loader behavior, fixtures, timeouts, accepted Gallery/Video/Blog/Contact behavior, or Qortal runtime behavior.

## Files changed

- Application: `src/features/home/HomePage.data.test.tsx` — one assertion synchronized with the existing asynchronous content state.
- This canonical handoff report only.

## Checks not executed and why

- No new owner/Hub/QDN runtime validation was run: the correction is test-only and does not modify runtime behavior. Existing accepted feature/runtime workflows remain separate OWNER-RUNTIME PASS evidence.

## Adversarial self-audit

- Confirmed the failure state contained the expected region and loading skeleton, proving the assertion raced the content transition.
- Rejected timeout inflation and assertion weakening.
- Reviewed the complete application diff: one insertion and one deletion in the focused test only.
- Confirmed no generated build output or dependency artifacts remain in the application worktree.

## External actions (commit/push/tag/release/deploy/QDN write/transaction)

- Application commit and authorized branch push performed: `980c5ad2517675b3da23209579bd9130e0fac6e9`; remote branch SHA matched exactly.
- No main merge, tag, release, deployment, QDN publication, transaction, or runtime message action occurred.

## Remaining risks and follow-up

The automated gate is fully clean at this application revision. This task neither refreshes nor replaces existing owner-runtime acceptance; none is needed for a test-only synchronization correction.

## Report saved

- Absolute path: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-15-homepage-loading-test-maintenance-handoff.md`
- SHA-256 (optional): not recorded; the Git commit below is the durable integrity reference.
