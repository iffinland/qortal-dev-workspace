# Phase 4 checkpoint evidence — 2026-09-16

Companion evidence for
`../2026-09-16-qwb-phase-4-checkpoint.md` (Phase 4 checkpoint report).

Executing agent: **DeepSeek** (local Codex CLI profile; the CLI/orchestration
profile is not the executor).

## Files

| File | What it is |
| --- | --- |
| `bootstrap-transition-prefix-failure.txt` | Pre-fix reproduction of the production-bootstrap defect. The test cases from the fix commit were copied into a detached worktree of the release candidate `741754becb79a131c699f2468fe096fdacd00c19`; **no application source was modified**. Two of the three cases fail there: after the first published entity only 1 of the 2 shipped highlights renders, and a tombstoned shipped item is immediately resurrected. |
| `bootstrap-transition-test.txt` | The same three cases at the checkpoint HEAD `7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a`: zero content → first write → reload → second write, tombstone non-resurrection, baseline self-termination. All pass. |
| `gates.txt` | First full gate capture at HEAD `7fd03fc…` (typecheck, eslint, prettier, vitest, build). |
| `gates-checkpoint.txt` | Authoritative re-run of the full gate on the same HEAD during checkpoint closure: typecheck/eslint/prettier clean, **294 tests in 25 files pass**, `npm run build` emits `dist/assets/index-Cc7rTXmF.js`. |
| `git-state.txt` | Branch, HEAD, clean `git status`, `git diff --check` over the checkpoint range, and `git ls-remote` confirmation that the branch is pushed and `main` / `agent/qwb/phase-3` are untouched. |
| `application-commits.patch` | `git format-patch` of the two checkpoint commits (`e7bf357`, `7fd03fc`) on top of `741754b`. |
| `SHA256SUMS.txt` | Digests of the files above (excluding itself). |

## Notes

- No QDN write of any kind was made by this checkpoint. The production resource
  `WEBSITE / Qortal Web Builders / default` was not touched.
- The runtime layers (Hub 3.0.3 owner-runtime run) were **not** re-executed: the
  checkpoint changes the read/merge path only, and no write, owner-mode or
  inline-editing contract changed.
