# QWB release candidate `7fd03fc` — final bounded staging confirmation

Executing agent (registered role of the agent that actually produced this work): **DeepSeek**
Report/handoff writer (if different from the executing agent): same (`DeepSeek`)
Executing-agent evidence (how the real executor was established): the Hub driving, the staging publish,
the runtime confirmation, the node read-backs and this report were produced by the **DeepSeek** model
executing through the local Codex CLI profile (`CODEX_HOME=/home/iffi/.codex-deepseek`,
`model = "deepseek-flash"`, `model_provider = "deepseek"`). Per `AI-Orchestration/GIT-AND-HANDOFF.md`
the CLI/orchestration profile is not the executor.
Report type: **validation report (live-host / live-QDN confirmation)**
Exact application repository / branch / SHA:
- repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`
  (local `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`)
- **release candidate** `agent/qwb/phase-4-runtime-fix` @ `7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a`
- `main` @ `18d760d011e956829714e7489432949829fa1840` — untouched, **not merged**
Canonical report path:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation.md`
Companion evidence directory:
`…/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation-evidence/`
Entry reports: `…/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md` (Phase 4 `PASS`)
and `…/implementations/2026-09-16-qwb-phase-4-checkpoint.md` (checkpoint closure).

---

## 1. Objective and result

**Objective.** Publish the current release candidate to the staging resource
`WEBSITE / Q-Website / default` and confirm **only** the production-bootstrap fix introduced after the
Phase 4 owner-runtime `PASS` (`e7bf357`): the already published synthetic entities still render, the
untouched shipped seed items render beside them, those items still expose the owner inline controls, a
hard reload preserves both, and no tombstoned shipped item is resurrected.

**Result: PASS.** The release candidate `7fd03fc` is now the served staging revision and all five
checks pass on the real Hub. `7fd03fc` is **production-ready**. Production was **not** published and
`WEBSITE / Qortal Web Builders / default` was **not** touched.

| Check | Result |
| --- | --- |
| Publication to staging | done — `2egexP3J…gDFJ9sLd`, 880 368 B, `READY`, block 2 725 989 |
| 1. existing synthetic QDN entities still render | **PASS** |
| 2. untouched shipped seed items render beside them | **PASS** |
| 3. those items still expose the owner inline controls | **PASS** |
| 4. hard reload preserves both | **PASS** |
| 5. no tombstoned item is resurrected | **PASS** |
| Full Phase 4 §14 owner-runtime suite | **not repeated** (by instruction) |
| Automated gates | **not re-run** — no source changed since `7fd03fc` |

## 2. The publish

Published with the Hub's own QDN publish implementation, called from the Hub 3.0.3 renderer
(`window.sendMessage('publishOnQDN', …)` → `src/encryption/encryption.ts` →
`src/qdn/publish/publish.ts::publishData` with `uploadType: 'zip'`). That is the same implementation
that backs the Hub's own **Apps → My apps → Publish site** flow; the transaction is signed by the Hub
wallet and **no node API key was present or used**. Payload: the `dist/` of `7fd03fc` packed from the
clean worktree (19 files, 879 170 B, sha256 `43244c21…67984cf7`), verified in-page before sending.

| Item | Value |
| --- | --- |
| Resource | `WEBSITE / Q-Website / default` |
| Previous revision | `5qU9BKTp…cgb4i`, 880 160 B (build `741754b`) |
| New revision | `2egexP3JFzX5pkyVKkPrt9Pidcv9QWvcrvYoxCb8KDtmZa1iY76TUjd4CxLG128xUszoJV2rxKCmyza1gDFJ9sLd` |
| New size | 880 368 B (`properties` 1 210 698 B, 3 chunks, `READY`) |
| Signer / creator | `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi` |
| Transaction | `ARBITRARY`, block 2 725 989, fee 0.01000000 QORT (balance 9.85 → 9.84) |

One intermediate attempt was rejected by the node (`Finalize failed: Bad parameter "category"`) because
the payload carried `category: 'other'`; it was retried without a category, matching the previous
staging publish. Both attempts are recorded in
`…-evidence/publish-invocation.json`.

**Served bytes.** All 19 published files were fetched back through `/render/` and hashed against the
local `dist/` of `7fd03fc`: 18 are byte-identical, and `index.html` differs only by the node's
`/render/` shell (injected `<base href>`, the `_qdn*` variables, `q-apps.js`, an extra
`<meta charset="UTF-8">`) plus the node's HTML re-serialisation. The served application chunk is
`assets/index-Cc7rTXmF.js`, sha256 `19c6ff71…0fcd6084` — identical to the local build
(`served-files-verify-after.json`).

## 3. The defect as it was still observable on staging

Staging was confirmed to be serving the pre-fix build before the publish (served `assets/index-BKwnLHC3.js`,
sha256 `9e1ce7a1…863db27f`, identical to the Phase 4 evidence `served-js-now.js`), so the bounded run
captured the defect **live**, not just from source:

| Group | `741754b` (pre-fix) | `7fd03fc` (release candidate) | QDN truth |
| --- | --- | --- | --- |
| highlights | **0** | 2 | 0 published |
| steps | **1** | 4 | 1 active |
| featured works | **0** | 3 | 0 published |
| services | **2** | 6 | 2 active |
| prices | **0** | 2 | 0 published |
| owner item control rows | **3** | 17 | 3 QDN + 14 shipped |
| owner add controls | 4 (no `Add featured card`) | 5 | — |

The pre-fix build hid every shipped item of a kind as soon as that kind had any QDN content, and once
the last item of a kind was gone its **only** control (`+ Add …`) went with it — the owner could not
bootstrap the site one entity at a time. The release candidate renders the shipped items again.

## 4. The five confirmation checks

Executed in Qortal Hub 3.0.3 (Linux/Electron) against the real staging resource, owner mode active via
`_qdnName` + name ownership on `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`. Hard reload = the Hub's own
`refreshApp` (document-level reload of the app iframe with a fresh `time=` cache-buster); three reloads
were performed in this run.

**1. The published synthetic entities still render — PASS.** All three active synthetic entities are
present and carry their owner controls: `Synthetic staging service (Phase 4, verified)` (rev 7),
`In-session service A (Phase 4)` (rev 1) and `Synthetic staging step (Phase 4)` (rev 1, with its
3 016 B `THUMBNAIL` rendering inside the card). The synthetic step is visible **beside** the shipped
steps in `screen-after-fix-steps-seed-beside-qdn.png`.

**2. The untouched shipped seed items render beside them — PASS.** 14 shipped items render although
**none** of the 23 shipped identifiers is published (probe: all 404 on the node). The counts are exactly
seed + QDN: services 6 = 4 shipped + 2 published, steps 4 = 3 shipped + 1 published. Since the QDN
reads returned nothing for highlights, featured works and prices, the 2 / 3 / 2 items rendered there can
only come from the shipped baseline.

**3. Those items still expose the owner inline controls — PASS.** 17 item control rows, of which **14
are shipped items**, each with the full `✎ / 🗑 / ↑ / ↓` set (`qwb-ctl-edit`, `qwb-ctl-delete`,
`qwb-ctl-move` ×2), plus 5 add controls including `Add featured card`, which the pre-fix build could not
mount. See `screen-after-fix-seed-highlight-with-controls.png`. The site singletons (Hero, Contact,
Footer) keep their `✎` controls.

**4. Hard reload preserves both — PASS.** After the Hub reload the counts, the 17 item rows, the
console and every tombstone/entity assertion are identical to the pre-reload state
(`runtime-after-fix-hard-reload.json`, `runtime-checklist-after-fix.json`).

**5. No tombstoned shipped item is resurrected — PASS.** The two tombstoned identifiers on this node
(`qwb_step_process-step-mu3jjvhv-o74n` rev 3 `deleted`, `qwb_svc_build-service-mu3jyvwn-99dq` rev 3
`deleted`) render nowhere: their titles are absent from the whole document text **and** from every
control label, while the two `tombstones: …` are reported as filtered. Honest scope note: **no shipped
identifier is tombstoned on this node**, so this run confirms the general rule (a reported tombstone is
never rendered and is never replaced by its shipped default) rather than a shipped-tombstone instance.
The shipped-tombstone case itself is covered by the transition tests in `tests/qdn-source.test.ts`
introduced with `e7bf357`; re-running the write path that would create one was out of scope by
instruction.

Also confirmed unchanged: every synthetic entity still holds its Phase 4 revision, order and state
(rev 7/1/3/1/3; order 50/10/0/60/55; active/active/deleted/active/deleted) and the `THUMBNAIL` still
serves 3 016 B — the bounded run disturbed no entity.

### 4.1 A correction to the checkpoint's expected evidence

The checkpoint plan expected a `console.info('[qwb owner] bootstrap-defaults: …')` line at boot. That
expectation was wrong: `bootstrap-defaults` is a diagnostic of the **QDN source load result**
(`src/content/qdn-source.ts`), and the console logging in `src/owner/shell.ts` only reports the
**control-mount** diagnostics. The source diagnostics are rendered only when the load *fails*, and are
returned to callers otherwise. The baseline is therefore confirmed from the rendered content (checks
1–3) and the 404 probe of the shipped identifiers, not from a console line. The one `[qwb owner]`
console line the run did capture belongs to the pre-fix build
(`owner add control skipped for "add-highlight": container not found`) and is retained as evidence of
the pre-fix state.

## 5. What was deliberately not done

- The full Phase 4 §14 owner-runtime suite was **not** repeated, and no write/owner-mode/inline-editing
  contract was re-exercised. This run executed **no entity write at all**; its only QDN write was the
  staging `WEBSITE` bundle publish.
- Automated gates were **not** re-run: no source changed between `7fd03fc` and this run (`git status`
  clean, HEAD unmoved), so the recorded `tsc --noEmit` / `eslint .` / `prettier --check .` and
  **294 tests in 25 files** still describe this exact tree.
- No unrelated feature work, no importer, no migration, and no merge of `main`.
- `WEBSITE / Qortal Web Builders / default` was read-only inspected (metadata identical to the Phase 4
  record) and never written.

## 6. Production publication readiness

**The release candidate `7fd03fc` is production-ready.** The last non-technical item recorded by the
Phase 4 checkpoint — a bounded owner confirmation that the release-candidate build behaves as intended
on staging — is now closed with runtime evidence.

Remaining before an owner-authorized production publication, none of which is a source defect:

1. **Owner authorization to publish** `WEBSITE / Qortal Web Builders / default`. This is the only
   external step left (D9: staging first, production last). Production currently serves the 2026-07-07
   placeholder (21 360 B, 2 files) and is byte-identical to its recorded state.
2. **Two owner decisions carried over unchanged** from the Phase 4 report, neither blocking: the
   licence position of the three bundled unDraw illustrations, and the inherited white-on-gradient
   navbar contrast (2.10:1, identical to the currently published site).
3. **Explicitly unverified, unchanged from the Phase 4 report:** the §14 step 6 failure half (image
   failure must block the entity publish) was not exercised, and step 13's literal in-form refusal
   notice is unreachable in Hub 3.0.3 because an account switch tears the render frame down. The
   equivalent guarantees were verified instead.

Note for the publication step: a published production entity switches that production resource away
from the shipped seed bundle exactly as staging did, which is why the production publication should
carry this release candidate (`7fd03fc`) and not the `741754b` build that hid the shipped items.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation.md`
- Companion evidence directory:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation-evidence/`
