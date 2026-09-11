# Shadow Archives — Phase 1B Implementation Plan (bounded scaffold)

- Project: `shadow-archives-webportal-QORTAL`
- Phase: 1B planning artifact produced during Phase 1A. **Not executed.**
- Date: 2026-09-11
- Author: Codex (Phase 1A research)
- Precondition: the owner recorded the Phase 1A decisions **D1–D9** on
  2026-09-11 (see
  [`./2026-09-11-phase-1a-architecture-report.md`](./2026-09-11-phase-1a-architecture-report.md)
  §14). D1, D2, D6 and D7 (the decisions that shape the scaffold) are
  **OWNER APPROVED**; **D9's wire representation is DEFERRED** and Phase 1B
  must only define its interface boundary. Q-Tube interoperability stays
  **FUTURE / NOT VERIFIED** and is out of scope.
- Related: [`./2026-09-11-phase-1a-architecture-report.md`](./2026-09-11-phase-1a-architecture-report.md),
  [`./2026-09-11-qdn-data-contracts.md`](./2026-09-11-qdn-data-contracts.md),
  [`./2026-09-11-performance-reference-comparison.md`](./2026-09-11-performance-reference-comparison.md),
  [`./2026-09-11-responsive-appshell-and-design-tokens.md`](./2026-09-11-responsive-appshell-and-design-tokens.md)

## 1. Objective and exit criterion

**Objective.** Stand up a minimal, Qortal-compatible Shadow Archives shell in
the target repository: project toolchain, providers, routing boundaries, design
tokens, the responsive home AppShell with skeleton regions, and owner-capability
plumbing **without live writes**.

**Exit criterion.** The shell builds, typechecks, lints and renders the approved
home layout at every target breakpoint with placeholder/skeleton data, all
lazy-route boundaries in place, owner capability detection reporting a truthful
state (including `unknown` outside a host), and **no** Blog/Video/Gallery
feature, publishing editor or QDN write path implemented.

**Explicit non-goals for Phase 1B.** No QDN publication, no catalog publishing,
no like/comment writes, no moderation writes, no editor integration, no video
player, no Q-Mail send, **no Q-Tube interoperability**, no Git initialisation
without separate authorization, no deployment, no release.

## 2. Authorized scope for Phase 1B

- Create the application source tree in
  `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`.
- Initialize Git **only if** the owner authorizes it as part of Phase 1B.
- Install only the approved baseline dependencies (see §4).
- Implement the shell, tokens, routing skeleton, provider stubs and tests.
- Run local automated validation.
- Run local dev-proxy validation if a local Qortal node is available.

Out of scope: any network write, any QDN resource publication, and any
implementation of the content contracts' write paths.

## 3. Sequence

### Step 1 — Initialize the project (D6/D7 dependent)

1. Create a Vite + React + TypeScript project in the target directory with
   `base: ''`.
2. Do **not** run `create-qortal-app` blindly: it has not been updated since
   2025-05-12. Either use it and then verify/replace the generated files, or
   reproduce the verified starter shape manually (React 19, TS 5.8+, Vite 6.3.x
   or 7.x, `react-router-dom` 7).
3. If D7 chooses the in-repo integration layer, remove `qapp-core` and MUI from
   `package.json` before the first build and confirm the entry bundle stays
   small (target: comparable to the 317 kB raw / 101 kB gzip React + Router
   baseline, plus app shell code).
4. Configure: `strict` TypeScript, ESLint + Prettier matching current app style,
   `tsc -b && vite build`, `vite preview`.
5. Add the test runner decided in Step 7 (Vitest is the current-app precedent:
   Quitter uses Vitest + jsdom + `fake-indexeddb`).

**Verification for this step.** `npm run build`, `npm run lint`, `tsc` all pass;
the build report shows a single small entry chunk and no video.js/MUI markers.

### Step 2 — Providers and router skeleton

1. `src/qortal/bridge.ts`: bridge detection (`typeof` guard), typed
   `request()` wrapper, timeout handling per action, error taxonomy
   (`unavailable`, `malformed`, `timeout`, `rejected`, `error`). No other module
   may call `window.qortalRequest`.
2. Read `_qdn*` once into a typed context object; decode `%20` in `_qdnName`
   into `publisherName`; keep the raw value too.
3. `src/qortal/auth.ts`: single-flight account request, permission states
   (`idle | pending | granted | rejected | unavailable`), name resolution
   (`GET_PRIMARY_NAME`, `GET_ACCOUNT_NAMES`), ownership check via
   `GET_NAME_DATA` on the decoded publisher name.
4. `src/qortal/capability.ts`: expose the capability states from the
   architecture report §11.2. **No write paths.**
5. Providers in the order from architecture report §1.4.
6. `createBrowserRouter` with `basename: window._qdnBase || ''` and the full
   route table from architecture report §4, each element behind `React.lazy`
   except the home route's shell.
7. Root + route + region error boundaries with branded fallbacks.

**Verification.** Unit tests for: bridge absent, malformed response, timeout,
rejected permission, no registered name, non-owner account, proxy/empty
`_qdnName`. A test asserting no duplicate `GET_USER_ACCOUNT` calls under
concurrent mounts.

### Step 3 — Design tokens and global styles

1. Implement the token block from the appshell specification §9 as CSS custom
   properties, with the semantic names unchanged.
2. Global reset, focus-visible styles, `prefers-reduced-motion` overrides,
   container/shell width rules, typography scale (two font families maximum).
3. A minimal in-repo component set: `Button`, `IconButton`, `Card`, `Dialog`
   (focus trap, `aria-modal`, escape, restore focus), `Tooltip`, `Tabs`,
   `Skeleton`, `Toast`, `Field`, `VisuallyHidden`.
4. Inline SVG icon module (thumb-up, comment, search, external-link, copy,
   close, chevron, menu, play).

**Verification.** Axe/automated accessibility check where practical, plus manual
keyboard checks: tab order, focus trap in dialog, escape, skip link.

### Step 4 — Responsive AppShell

1. Header with the three panels, reserved heights and skeleton states.
2. Primary action row (Q-Tube / SubWire / Quitter anchors + search control) and
   the site navigation row.
3. Auto-scroll marquee component (vertical + horizontal variants) with the pause
   rules and reduced-motion behaviour from the appshell specification §5, with
   placeholder items in Phase 1B.
4. Home body placeholder regions: `Latest Posts`, `Latest Videos`, gallery
   strip, footer.
5. Skeleton components that exactly match the final geometry.

**Verification.** Render at 320/375/768/1024/1440/1920/2560px; assert no
horizontal page scroll, reserved header band, no layout shift on
skeleton→content swap, auto-scroll pauses on hover/focus/reduced motion, all
targets ≥44px (≥48px TV) and visible focus rings.

### Step 5 — Cache and catalog plumbing (read-only)

1. `src/qortal/cache.ts`: app-namespaced IndexedDB database (distinct name per
   app), explicit success/failure TTLs, stale-while-revalidate, versioned
   stores. Do **not** reuse `qapp-core`'s `MyAppDB`.
2. `src/qortal/queue.ts`: bounded-concurrency queue (start at 4–6) with
   cancellation and generation tokens so stale responses cannot overwrite newer
   state.
3. `src/catalog/`: manifest + partition type definitions from the data
   contracts §7, a reader that validates `schemaVersion`, and a degraded mode
   when the catalog is absent. **Read-only: no publisher.**
4. A `useCatalogStatus()` hook exposing `idle | loading | fresh | stale |
   partial | unavailable | malformed`.

**Verification.** Unit tests with in-memory fake IndexedDB: TTL expiry, failure
TTL, malformed partition quarantine, stale-served-with-flag, generation-token
race.

### Step 6 — Owner capability plumbing stub

1. Wire `capability` into the shell: the studio navigation entry and owner
   toolbar render only for `owner`, and only as an inert placeholder that links
   to a `studio` lazy route containing an explanatory "not implemented in this
   phase" panel.
2. No publish, like, comment or moderation write call may exist in Phase 1B.
   Publishing helpers may be typed declarations only, and must not be imported
   by any route.

**Verification.** A test asserting that no module reachable from a public route
imports the studio chunk, and a test asserting zero `PUBLISH_*` invocations
during a full shell render.

### Step 7 — Automated validation

- `npm run lint`
- `tsc --noEmit` (or `tsc -b`)
- `npm run test` (Vitest) with the Phase 1B tests above
- `npm run build` and a recorded build-output report (chunk sizes) compared
  against the Phase 1A baselines
- `npx vite preview` smoke render (plain browser; **not** proof of Qortal
  compatibility)

### Step 8 — Local Qortal dev-proxy validation (when a local node is available)

- Start the dev server, register the dev app in Hub Developer Mode, and start
  the node dev proxy (`POST /developer/proxy/start`).
- Confirm the shell renders under the proxy context and that the app reports
  capability `unknown` (because `_qdnName` is empty in proxy context) rather
  than pretending to be the owner.
- Record the node/port and proxy context used.
- **Not** proof of published-app behavior.

### Step 9 — Handoff and adversarial self-audit

- Run the Workflow v2 self-audit checklist against the actual implementation.
- Record what was verified, what was not, and the exact files changed.
- Produce the report under the canonical report root.

## 4. Approved baseline dependencies (owner-approved D6/D7)

Under the owner-approved D6 (no MUI) and D7 (in-repo integration layer):

**Runtime**

- `react`, `react-dom` (19.x)
- `react-router-dom` (7.x)
- a small state library if needed (`zustand`) — optional
- `dompurify` (only when stored rich text is first rendered; can be lazy-loaded
  with the content-render chunk)
- TipTap packages — **not installed in Phase 1B**; deferred to the editor phase
- no MUI, no emotion, no `qapp-core`, no video library, no icon package

**Dev**

- `typescript`, `vite`, `@vitejs/plugin-react`, `eslint` +
  `typescript-eslint` + `eslint-plugin-react-hooks` + `eslint-plugin-react-refresh`,
  `prettier`, `vitest`, `jsdom`, `fake-indexeddb`,
  `@testing-library/react`, `@testing-library/user-event`

**Rejected alternative (documented for traceability).** Using `qapp-core`
`GlobalProvider` would add `qapp-core`, `@mui/material`, `@mui/icons-material`,
`@mui/system`, `@emotion/react` and `@emotion/styled`, and record a ~596 kB
gzip baseline floor. The owner rejected this (D7); do not add it to Phase 1B
without a new evidence-backed reason and owner approval.

## 5. Phase 1B acceptance checklist

- [ ] Build, typecheck and lint pass with zero errors.
- [ ] Entry chunk contains no video player, no editor, no studio code.
- [ ] Every public route is a lazy boundary; studio is unreachable from a public
      route import graph.
- [ ] Home AppShell matches the owner layout at every breakpoint.
- [ ] Auto-scroll pauses correctly and is disabled under reduced motion.
- [ ] Owner capability states are correct for: no bridge, proxy, no account,
      rejected permission, no name, non-owner, owner.
- [ ] No write path exists; no `PUBLISH_*` call is reachable.
- [ ] Catalog is read-only and degrades honestly when absent.
- [ ] No layout shift on skeleton→content swap.
- [ ] Target repository contains no secrets and no environment files.
- [ ] Report saved under the canonical root with the absolute path disclosed.

## 6. Risks and mitigations

| Risk | Mitigation |
| ---- | ---------- |
| Re-implementing bridge/auth incorrectly | pin Core/Hub revisions; mirror `q-apps.js`/Hub behavior; unit-test negative cases; verify in a real host before claiming success |
| Accessibility regressions from hand-built primitives | explicit focus-trap/dialog tests; automated a11y checks; manual keyboard pass |
| Identifier scheme needs revision after first publish | the scheme is fully specified in Phase 1A (`saw_` namespace, stable-ID encoding) so the first publish is already consistent; schema evolution is carried by payload `schemaVersion`, not by the namespace |
| Catalog size ceiling is an inference | measure a real partition publish in the catalog phase before committing to partition sizes |
| No runtime measurement available locally | treat all Phase 1B numbers as build-output evidence only; a real host measurement is a separate, owner-run gate |
