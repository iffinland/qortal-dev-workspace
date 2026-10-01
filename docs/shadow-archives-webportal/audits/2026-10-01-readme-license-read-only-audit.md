# Shadow Archives — README and licence read-only audit

Executing agent (registered role of the agent that actually produced this work): **Codex**
Report/handoff writer (if different from the executing agent): **Codex**
Executing-agent evidence (how the real executor was established): This audit was performed directly in the current Codex session.
Report type: Read-only repository documentation and licence audit
Exact application repository / branch / SHA: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`; `agent/shadow-archives/blog-publish-partial-outcome-20261001`; `adfb91f841f10c796b462e045fc6520f6682b126`
Canonical report path / authorized remote evidence: Local report only; no source, licence, commit, push, or release action is part of this audit.

## Finding 1 — README is materially stale

`README.md:6-8` says the project is only a Phase 1B responsive shell and has no content discovery, publishing, or QDN-loaded data. That conflicts with the same README's later Blog/Video/Gallery publishing sections and with the current owner-runtime evidence: the published APP served the fixed `d8967d7` build and QDN now contains canonical Blog entity `saw_post_lr6vjv48uo4u`.

The public default branch `main` is `fab9fdbded2e8f687587ff5a122fcb4070fa67c1`; the remediation branch is `adfb91f…`. Both the local current branch and `main` lack a tracked licence file, and the stale Phase 1B summary appears in the current README.

Recommended bounded documentation correction:

- Replace the opening status block with the current implemented scope: QDN content discovery; owner-gated Blog, Video, and Gallery publishing; SubWire/Q-Tube interoperability; optional Quitter announcement; direct private-chat Contact.
- Keep non-implemented items explicit: comments, likes, tips, moderation, advanced/deep search, and any unverified interoperability path.
- Replace historical “all tests/build pass” claims with dated evidence or a concise pointer to the canonical Qortal handoff/audit report.

## Finding 2 — no project licence is present

No tracked `LICENSE`, `COPYING`, or `NOTICE` file exists in either `main` or the current remediation branch. Absent a licence grant, outside users do not receive a clear permission to copy, modify, or redistribute the repository code.

## Licence decision

The owner's stated desired result is: allow use, copying, and modification while preserving original attribution and asking people to contact the owner when appropriate.

**Recommended licence: GNU GPL v3.0 or later (`GPL-3.0-or-later`).** It permits those activities, requires preservation of copyright/licence notices, and requires distributed modified whole works to remain under GPL with corresponding source available. This is stronger than an attribution-only licence: downstream distribution is copyleft, not permissive/proprietary.

Do not modify the official GPL text. Add the unmodified FSF GPLv3 text as root `LICENSE`, with a project copyright notice. Place the courteous contact request in `NOTICE` and/or README as a non-binding request, for example: “If you use, adapt, or publish a derivative of Shadow Archives, please retain the copyright and licence notices and consider contacting the original author at <owner-provided contact method>.” A mandatory “must contact” term needs legal review before being presented as a GPL condition; it may be an additional restriction rather than a simple attribution notice.

If the owner instead wants only attribution and no obligation to open-source distributed derivatives, GPL-3.0-or-later is the wrong choice; use a permissive licence such as Apache-2.0 with `NOTICE` instead.

## Checks not executed and why

- No source or documentation edits: the owner requested inspection first.
- No licence was added: the exact copyright holder/year and public contact method remain owner-provided legal/product choices.
- No commit, push, release, or QDN publication.

## Report saved

- Absolute path: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/audits/2026-10-01-readme-license-read-only-audit.md`
