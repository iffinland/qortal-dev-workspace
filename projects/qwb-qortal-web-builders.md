# Qortal Web Builders — qwb-qortal-web-builders

> Status: **PHASE 3 ACCEPTED (CODE-COMPLETE); PHASE 4 OWNER-RUNTIME VALIDATION `PASS`;
> RELEASE CANDIDATE `7fd03fc` CONFIRMED ON STAGING AND PRODUCTION-READY** (2026-09-16).
> Development repository `git@github.com:iffinland/QWB-Qortal-Web-Builders.git`: `main` @
> `18d760d011e956829714e7489432949829fa1840`; the accepted Phase 3 build is on `agent/qwb/phase-3` @
> `911b44f3e57c39c46048c950274c89bdd04596f5` (base `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`, the
> Phase 2 head), remote-verified and unchanged. Phase 2 supplied the owner layer: automatic owner
> recognition (`_qdnName` + `GET_USER_ACCOUNT` + `GET_ACCOUNT_NAMES` → case-folded membership), the
> owner/visitor state machine with re-verification, and the inline owner shell (compact bar,
> contextual `✎ / 🗑 / ↑ / ↓ / + Add …` controls, modal/sheet shells, dirty-state UX). Phase 3
> connected that same UI to QDN-backed CRUD: one resource per entity (`JSON` for
> site/highlight/service/step/work/price, `DOCUMENT` for articles; media as `THUMBNAIL`/`IMAGE`),
> logical tombstone deletion, sparse persistent ordering, the truthful
> submitted/rejected/ambiguous/failed × verified/superseded/not-yet-served write-result model, and
> client-side interlocks (one in-flight write per identifier, no automatic retry of any write,
> fail-closed owner re-verification immediately before every write).
> **Phase 4 owner-runtime validation is complete and PASSED.** The whole Phase 3 §14 procedure was
> executed end to end against the owner-approved staging resource `WEBSITE / Q-Website / default`,
> held by the expected owner wallet `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`, on mainnet
> `qortal-6.1.9-108bf19` with Qortal Hub 3.0.3, using synthetic content only. Steps 1–13 all returned
> real served read-back with reload-surviving persistence: automatic owner recognition, visitor and
> signed-in-non-owner negative controls with no owner UI, add/edit/hard-reload persistence, media
> replacement published **before** the entity and rendered from `/arbitrary/…`, persistent reorder,
> tombstone delete, the `Publishing status` surface with state **and** availability and
> `Pending writes: 0`, `Reload content`, a declined approval returning
> `Rejected by the host — nothing was published` with the draft preserved, **exactly one** approval
> dialog and **no automatic retry**, and an account lock/switch that leaves no owner UI.
> Two genuine real-host runtime defects were found and fixed at the root cause on the pushed branch
> `agent/qwb/phase-4-runtime-fix` @ `741754becb79a131c699f2468fe096fdacd00c19`
> (remote-verified): `8fd110b` — the injected `qortalRequest` is a **lexical** global and `_qdnName`
> arrives **percent-encoded**, so owner mode reported `no-bridge` on a real host; `741754b` — a
> single-file QDN image must be addressed at the **bare identifier path** (appending the stored
> filename 404s, and `?filepath=` is the multi-file lookup). After the last source change: `tsc
> --noEmit`, `eslint .`, `prettier --check .` clean, **291 tests in 25 files pass**, `npm run build`
> emits `dist/assets/index-BKwnLHC3.js`; the served staging bytes hash-match that build exactly. No
> source changed during the resumed runtime run, so the gate was not re-run for ceremony.
> **Phase 4 checkpoint (2026-09-16):** two further commits closed the checkpoint on the same
> branch — `e7bf3578d8772330f313b468bc808d5c57c8bf22` (a per-entity, self-terminating
> pre-publication bootstrap baseline; read path only) and
> `7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a` (project documentation). The release candidate is
> therefore `agent/qwb/phase-4-runtime-fix` @ `7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a`, and its
> gate is `tsc --noEmit` / `eslint .` / `prettier --check .` clean, **294 tests in 25 files pass**,
> and a successful `npm run build`. No write, owner-mode or inline-editing contract changed, and
> the checkpoint made no QDN write.
> **Final bounded staging confirmation (2026-09-16, `PASS`):** the release candidate build was
> published to the staging resource `WEBSITE / Q-Website / default` (signature
> `2egexP3JFzX5pkyVKkPrt9Pidcv9QWvcrvYoxCb8KDtmZa1iY76TUjd4CxLG128xUszoJV2rxKCmyza1gDFJ9sLd`,
> 880 368 B, `READY`, confirmed in block 2 725 989 by `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`), and
> the production-bootstrap fix was confirmed in the real Hub: the already published synthetic
> entities still render, the untouched shipped items render beside them **with** their owner
> inline controls, a hard reload preserves both, and no tombstoned item is resurrected. The
> release candidate `7fd03fc` is **production-ready**. Production was still not published. The
> staging run also reproduced the pre-fix defect live (build `741754b` rendered 0 highlights,
> 0 featured works, 0 prices, 2 services, 1 step).
> **The production resource `WEBSITE / Qortal Web Builders / default` was NOT published and NOT
> written** — it remains the 2026-07-07 placeholder (21 360 B, 2 files; name owner
> `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`). No write used a node API key; every write was signed by the
> owner through a Hub approval dialog.
> Explicitly unverified / documented limitations: the §14 step 6 failure half (image failure must
> block the entity publish) was not exercised; and in Hub 3.0.3 a mid-session account switch tears the
> render frame down, so step 13's literal in-form refusal notice is unreachable — the equivalent
> guarantees (fail-closed decision, zero owner UI for a signed-in non-owner, host-gated writes) were
> verified instead.
> Reports: `docs/qwb-qortal-web-builders/implementations/2026-09-16-qwb-phase-4-owner-runtime-validation.md`
> (evidence in `…/implementations/2026-09-16-qwb-phase-4-runtime-evidence/`, resumed-run artefacts under
> `run-2026-09-16-resumed/`; the prior `blocked` run is archived as
> `…/2026-09-16-qwb-phase-4-owner-runtime-validation-blocked-run-archive.md`),
> `…/implementations/2026-09-15-qwb-phase-3-implementation.md` (evidence in
> `…/implementations/2026-09-15-qwb-phase-3-runtime-evidence/`),
> `…/implementations/2026-09-15-qwb-phase-2-implementation.md`
> (evidence in `…/implementations/2026-09-15-qwb-phase-2-visual-evidence/`) and
> `…/implementations/2026-09-15-qwb-phase-0-1-implementation.md`
> (visual evidence in `…/implementations/2026-09-15-qwb-phase-1-visual-evidence/`),
> `…/implementations/2026-09-16-qwb-phase-4-checkpoint.md` (evidence in
> `…/implementations/2026-09-16-qwb-phase-4-checkpoint-evidence/`) and
> `…/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation.md` (evidence in
> `…/validation/2026-09-16-qwb-rc-7fd03fc-staging-confirmation-evidence/`).
> **Owner decisions D1–D9 are approved (2026-09-16)** — the entry conditions recorded as open above
> are closed, and the remaining external step is the owner-authorized production publication itself.
> The approved production identity is **`WEBSITE / Qortal Web Builders / default`** (service
> `WEBSITE`, publishing name `Qortal Web Builders`, identifier `default`), the resource the site
> already addresses; staging was **`WEBSITE / Q-Website / default`**, where the Phase 4 owner-runtime
> validation passed and where the release candidate `7fd03fc` was subsequently confirmed on
> 2026-09-16. QDN CRUD, owner mode and inline editing are implemented and runtime-verified —
> the `qwb_*` resource model is the shipped model, no longer a proposal.

## Project identity

- Project ID: `qortal/qwb-qortal-web-builders`
- Product name: **Qortal Web Builders** (QWB) — a service business offering individually designed
  Qortal websites and applications (custom visual identity, layout, functions and client-specific
  behaviour), not a generic block/website builder.
- Refreshed site goal: communicate premium custom development while clearly descending from the
  existing QWB visual identity.

## Repository and local path

| Role | Path / remote |
| --- | --- |
| Immutable visual golden master (**READ-ONLY**) | `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/-PUBLISHED-versioon` |
| Development repository | `/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders` — `main` @ `18d760d011e956829714e7489432949829fa1840` (Phase 1 baseline, **not merged**); `agent/qwb/phase-2` @ `b53edc1aa57b89037cd4b86a6fa5173e5bd5934c`; `agent/qwb/phase-3` @ `911b44f3e57c39c46048c950274c89bdd04596f5` (accepted Phase 3 build); `agent/qwb/phase-4-runtime-fix` @ `7fd03fc5b2d39d80b20ccaa9c7a07355d85dc94a` (release candidate, Phase 4 checkpoint closed) |
| GitHub remote | `git@github.com:iffinland/QWB-Qortal-Web-Builders.git` (`https://github.com/iffinland/QWB-Qortal-Web-Builders`) |
| Canonical report root | `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/` |

The golden master has no Git metadata and must never be used as a Git working tree, remote,
submodule or worktree. Its SHA-256 manifest is recorded in this workspace's validation directory.

## Product purpose

Service-oriented Qortal website/app for QWB's own marketing and portfolio: custom websites, custom
Qortal applications, visually unique designs, client-specific functionality.

## The currently served resource (verified 2026-09-15)

This describes the **published** resource being replaced; it is not the state of the development
repository (see the status header and the Phase 0–4 baseline below).

- The published site is a **six-page static Bootstrap 5.2.2 site** (home, completed works, four
  article pages) with a bespoke theme CSS, vendored jQuery 2.2.3 + plugins, no build tooling, no
  data layer, and Qortal integration only via `qortal://` deep links.
- No owner editing, no QDN reads/writes, no dynamic content.
- 50 files / 8,897,400 bytes. Full forensics:
  `docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-static-site-forensics.md`.
- Reference owner-editing application audited (not to be cloned):
  `iffinland/iffi-vaba-mees-QORTAL` — see the owner-pattern audit report.
- The audit's open questions — QDN service/URL strategy, typography, asset strategy, stock-photo
  licensing, publishing identity, dev-override policy, article kind, commerce/contact touchpoints
  and staging target (§15 of the architecture proposal) — were all **answered by the owner on
  2026-09-16 as D1–D9** (below). Nothing in that list is still undecided.

### Development baseline (Phase 0–1 snapshot extended through the Phase 4 checkpoint)

- **Stack:** Vite 8.3.0 + TypeScript 6.0.3 (strict) + vanilla DOM modules. Runtime dependencies are
  `bootstrap` (CSS only), `@fontsource/montserrat`, `@fontsource/open-sans` — no React, no MUI, no
  `qapp-core`, no jQuery, no Bootstrap JS bundle.
- **Structure:** `src/content`, `src/styles`, `src/ui`, `src/views`, `public/` for brand/structural assets,
  `docs/` for durable project documentation (`architecture.md`, `attribution.md`,
  `third-party-licences.md`); `tests/` holds **294 Vitest tests in 25 files** at the Phase 4
  checkpoint (Phase 1 47/5 → Phase 2 174/17 → Phase 3 283/24 → Phase 4 runtime fixes 291/25 →
  Phase 4 checkpoint 294/25).
- **Views implemented:** home (hero, featured pair, tabbed Browse Topics strip, steps, pricing,
  contact), completed works, article index, article detail, not-found. Hash routes `#/`, `#/works`,
  `#/posts`, `#/post/<slug>`; the published `#section_1/2/3/5` anchors still resolve as
  "home + scroll"; `#main-content` is reserved for the skip link.
- **Content seam:** typed seed content behind a `ContentSource` interface
  (`createSeedSource()` in Phase 1, `createQdnSource()` from Phase 3), with the common entity
  envelope (`schema`/`rev`/`state`/`deletedAt`/`order`) and the `qwb_*` identifier policy enforced
  on both paths.
- **QDN layer (Phase 3, `agent/qwb/phase-3`):** `src/qortal/read.ts` (bounded, prefix-filtered
  `SEARCH_QDN_RESOURCES` with exact name/service/prefix re-filtering) and `src/qortal/publish.ts`
  (media → entity ordering, served-revision verification) behind `src/content/qdn-source.ts`. Every
  kind is discovered and hydrated per entity; tombstones are filtered on every read path.
- **QDN network calls exist from Phase 3 onwards** — this supersedes the Phase 0–1 statement that no
  QDN call existed anywhere in the code.
- **Owner layer (Phase 2, `agent/qwb/phase-2`):** `src/qortal/` (`context.ts` injected globals,
  `bridge.ts` the single `qortalRequest` wrapper, `identity.ts` owner recognition, `write.ts` truthful
  write vocabulary + served-revision gate) and `src/owner/` (session, targets, controls, bar, shell,
  flows, fields/forms, drafts, phase gate) plus `src/ui/modal.ts`, `src/ui/toast.ts` and
  `src/styles/owner.css`. Statuses are `owner | visitor | unavailable | inconclusive`; only `owner`
  mounts owner UI, every flow re-verifies via `assertOwner()`, and nothing about ownership is
  persisted. Owner mode is structurally `unavailable` in the Hub dev-proxy (empty `_qdnName`) and in
  gateway/domain-map serving.
- **Preserved identity:** golden-master `:root` tokens verbatim, the 15° `#13547a → #80d0c7`
  gradient, aquamarine fills with 100 px rounded section bottoms, alice-blue contact band, 10 px
  footer border with the diagonal corner motif, 20 px card radius, featured 4/6 asymmetry, centred tab
  strip, step pills, green stat pill, two-box pricing and the transparent navbar lock-up.
- **Known open item:** white navbar links on the gradient measure 2.10:1 — measured identical to the
  golden master. Phase 4 did not change it: it is a design choice, not a regression against the
  currently published site, and it stays an owner decision.
- **Owner input requested:** (a) the licence position of the three bundled unDraw illustrations
  (recorded as *unDraw-assumed*, not proven from the files); (b) the navbar contrast decision above.
  Neither one blocks the accepted implementation; both were carried into the Phase 4 checkpoint.

## Owner decisions (D1–D9, approved 2026-09-16)

The owner approved the D1–D9 package of
`docs/qwb-qortal-web-builders/audits/2026-09-15-qwb-target-architecture-proposal.md`; the accepted
state below is the approved choice as actually implemented (verifiable in the application source and
in the Phase 4 runtime evidence, none of it a proposal any more).

| # | Decision | Accepted (implemented / decided) state |
| --- | --- | --- |
| D1 | Service and URL strategy | `WEBSITE`, single-entry build, dynamic views in the hash (no `APP` routing change, so existing `qortal://WEBSITE/…` links stay valid) |
| D2 | Typography | self-hosted Montserrat + Open Sans (latin subset, woff2) with the intended body scale restored |
| D3 | Asset strategy | brand/structural assets bundled in the build; content images are QDN-managed (`bundled` / `qdn` / `placeholder` reference kinds) |
| D4 | Stock photography | unknown-provenance stock photography dropped (app `docs/attribution.md`); the three unDraw illustrations remain, with the licence assumption recorded |
| D5 | Publishing identity | `Qortal Web Builders` — the existing registered name, which is therefore also `_qdnName` and the only owner |
| D6 | Local owner-editing development | no dev-only owner override; owner mode comes only from a real host `_qdnName` + name ownership |
| D7 | Article pages | the article kind is kept (`qwb_post_*`, service `DOCUMENT`) |
| D8 | Commerce / contact | the existing Q-Shop, Q-Mail and group touchpoints are kept and carried in the editable content |
| D9 | First publication target | staging first (`WEBSITE / Q-Website / default`, where Phase 4 passed and the release candidate `7fd03fc` was confirmed on 2026-09-16), production only at the final owner-authorized step |

## QDN identities and services

- **Production identity (approved, not yet written):** `WEBSITE / Qortal Web Builders / default` —
  the registered name `Qortal Web Builders` (also referenced in the site footer as
  `qortal://WEBSITE/Qortal%20Web%20Builders`). It still serves the 2026-07-07 placeholder; no write
  has been made to it.
- **Staging identity (used for Phase 4 and the release-candidate confirmation):**
  `WEBSITE / Q-Website / default`, owned by `QNwV9VV82UUZmMkDZZbEMAKPpCx7otnnsi`, where all §14
  steps passed and where the release candidate `7fd03fc` now serves (three publishes in total:
  the `8fd110b` build, the `741754b` build, and the `7fd03fc` confirmation revision).
- Related existing QDN touchpoints referenced by the site: `APP/Q-Shop/Qortal Web Builders/q-store-general-qortal-web-builders`,
  `APP/Q-Mail/to/Qortal20Web%20Builders`, group `745`, several portfolio `WEBSITE` resources.
- Identifier prefix family, implemented and runtime-verified under the staging name: `qwb_*`
  (`qwb_site_v1`, `qwb_hl_`, `qwb_svc_`, `qwb_step_`, `qwb_work_`, `qwb_price_`, `qwb_post_`).

## Entity and operation model

Implemented and owner-runtime-verified: singleton `site` JSON plus per-entity `highlight`, `service`,
`step`, `work`, `price` and optional `article` resources; media in `THUMBNAIL`/`IMAGE`; `rev`-verified
updates by re-publishing the same `(name, service, identifier)`; **logical deletion via tombstones**
because no app-accessible QDN delete exists. Discovery is bounded `SEARCH_QDN_RESOURCES` by
identifier prefix with post-filtering; **no derived index in v1**. One read-path rule is
QWB-specific and was added at the Phase 4 checkpoint: while the owner is still replacing the shipped
seed content (the approved §6.4 flow), a kind keeps the shipped items that discovery did not
report at all — a published identifier is never replaced by its shipped default, and a failed or
page-budget-truncated discovery contributes no default. The baseline is per entity and
self-terminating: publishing or tombstoning every shipped identifier ends it. Details: §6–§8 of the
architecture proposal; read contract in the application `docs/architecture.md` §3.4.

## Authority and trust boundaries

- Owner mode must be derived, never hardcoded: `_qdnName` (the app's publishing name) must be a
  member of the current account's name list from `GET_ACCOUNT_NAMES`, resolved after
  `GET_USER_ACCOUNT`; fail closed on any error, and never persist `owner=true`.
- Every read path must discard resources whose publishing `name` is not `_qdnName`; every write
  path must re-verify owner mode immediately before publishing.
- The real boundary remains the Qortal ledger + host signing approval; in-app checks are defence in
  depth only.
- Gateway context is read-only and must disable editing (Core's gateway shim resolves interactive
  actions with an `{error}` object instead of rejecting).
- Rendering safety is a separate gate: any owner-authored rich text must be sanitised with a vetted
  allowlist sanitizer before `innerHTML`, with malicious HTML/URL fixtures in tests.

## Qortal platform dependencies (pinned for the audit; re-verify per task)

| Reference | Revision |
| --- | --- |
| Qortal Core `master` | `108bf191d42d710ec617f535af30cfd82fc03c87` (6.1.9) |
| Qortal Hub `develop` | `12a573b27246e8a626b24794830c6bc432d1b05d` |
| qapp-core `master` | `0f9d6ac5134ef2f82c1444a74e78471ddc7eb7df` (1.0.79) |
| qapp-templates `main` | `143cc7bffd265f543f96ef25bf1b58ef7bb04472` |
| Reference app `iffinland/iffi-vaba-mees-QORTAL` `main` | `64f55bf7b6f4a1a093f19413d3a985e61a9fad37` |

## Key commands

Development repository (`/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders`):

```bash
npm ci                 # then:
npm run dev            # vite dev server
npm run typecheck      # tsc --noEmit
npm run lint           # eslint .
npm run format:check   # prettier --check .
npm test               # vitest run
npm run build          # tsc --noEmit && vite build
npm run preview        # serve dist/
```

The read-only integrity check for the golden master is:

```bash
cd /home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders
find ./-PUBLISHED-versioon -type f | LC_ALL=C sort | xargs sha256sum \
  | sed 's#\./-PUBLISHED-versioon/#./#' \
  | diff - <(grep -E '^[0-9a-f]{64}  ' \
      /home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/qwb-qortal-web-builders/validation/2026-09-15-qwb-golden-master-sha256.txt)
```

## Validation

- Local development must use a local node + Hub Developer Mode (dev proxy), **but owner mode cannot
  be exercised there** because `_qdnName` is empty in proxy context (the app now reports
  `unavailable` with that reason instead of guessing). Owner mode also cannot be exercised through
  gateway or domain-mapped serving: only Core's `render` context attaches a Hub that answers
  host-mediated requests.
- Required layers per phase: unit tests (identity derivation, write-result classification, schema
  validation, identifier generation, tombstone filtering), production build, bounded live read-only
  node validation, and **owner real-host acceptance in Qortal Hub** for any editing/write claim.
- No QDN write is authorized without explicit owner approval (see D9 in the architecture proposal).

## Known limitations

- No app-accessible QDN delete exists (only node-local, API-key admin deletion) — deletion is
  logical and the UI must say so truthfully.
- Publishing returns submission, not availability; the served revision must be verified by re-read.
- No host event reports an account switch, so owner mode is re-verified on demand (before every
  privileged action and on visibility regain; automatic re-checks are rate-limited to 15 s).
- Owner-mode status is therefore only ever accepted from a real host run; the Phase 2 headless-browser
  evidence is structural, not host validation. **Satisfied for the current build on 2026-09-16**: the
  Phase 4 owner-runtime run in Qortal Hub 3.0.3 returned `PASS` for §14 steps 1–13 against staging
  `WEBSITE / Q-Website / default`. Any future owner-mode claim still needs a fresh real-host run.
- `GET_ACCOUNT_NAMES` ignores `limit`/`offset`/`reverse` in the bridge.
- External `http(s)` links are blocked inside a Qortal host.

## Current reference revisions

See the table above; all were confirmed clean and equal to upstream on 2026-09-15 12:51 UTC and
re-verified unchanged at 2026-09-15 14:20 UTC during the Phase 0–1 implementation (no delta to the
audit).

## Mandatory project rules

1. `-PUBLISHED-versioon` is read-only; never build, format, edit or initialise Git inside it.
2. No static-content migration/import script (confirmed: not recommended).
3. Owner content management happens in context on the public page; no general admin dashboard.
4. Never hardcode the owner's name or address; derive owner mode from `_qdnName` + current name
   ownership.
5. No QDN write, deployment, commit or push without explicit task-scoped owner authorization.
6. Do not clone the reference application's architecture; reuse only the patterns classified in the
   owner-pattern audit report.
