# Owner handoff — Contact private-chat live validation (ONE procedure)

Executing agent: `DeepSeek` (implementer; evidence in the implementation report)
Report type: owner handoff / live-host validation procedure
Exact application repository / branch / SHA:
`/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`, branch
`agent/shadow-archives-webportal/owner-runtime-checkpoint-20260913`, base `c9ce071` **plus the
uncommitted Contact feature changes** (nothing was committed or pushed; see the implementation report §15)
Canonical report path:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-14-contact-private-chat-owner-live-validation-handoff.md`
State: `owner_validation_pending` — the feature is complete but **not** runtime-verified.

## What is being validated

One visitor-facing flow, end to end, in a real Qortal host with a real account:

```text
Contact page -> write message -> resolve current owner -> host approval -> SEND_CHAT_MESSAGE
  -> truthful result -> owner sees the message in current Qortal chat -> no duplicate -> clean state
```

This is the only remaining gate. Unit tests, typecheck, lint, the production build and read-only node
evidence are already green (implementation report §8), but they cannot prove host approval, relay or
owner receipt.

## Preconditions

1. The Contact changes are present in the build/deployment under test — either run them locally
   (`npm run dev` behind the Hub dev proxy is not sufficient for sending; use a real host) or ask for
   an explicitly authorized commit/deploy first. Nothing has been committed.
2. A Qortal Hub (desktop or browser extension) with an account that holds at least **4 QORT**
   (`MIN_REQUIRED_QORTS`) and is **not** already at the node's pending-chat limit
   (`maxRecentChatMessagesPerAccount`, 250 on the owner nodes).
3. The app is open as the published `APP` resource for the `Shadow Archives` name, and the owner
   account (the account that will receive the message) is available in a second Qortal client for
   verification. The current on-chain owner is `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA`; the app resolves
   it at runtime and does not need it to be configured.
4. Use a synthetic test message. Do not type anything private: the message body is transmitted and
   relayed by the node, and this validation is about the mechanism, not the content.

## Procedure

1. **Open Contact.** Navigate to `/contact` in the published app. Expected: the recipient panel shows
   the publishing name (`Shadow Archives`), never an address or public key; the retention notice names
   the verified period ("about 24 hours in the current Qortal Core chain configuration … the exact
   period depends on the network and node settings") and points at Q-Mail for durable contact.
   Capture: Hub version, node `buildVersion`, a screenshot of the notice.
2. **Verify the field is usable immediately.** Start typing as soon as the page appears. Expected: no
   keystrokes are lost while the owner is still being resolved (this was a fixed defect).
3. **Send.** Press `Send private message` once with e.g. `validation test <date> <time>`.
   Expected: the button changes to `Sending…` and is disabled; the Qortal host shows the approval
   dialog naming the recipient address and a preview of the message.
4. **Approve once** (do not tick "always allow" for this test; the dialog must be observed). Expected
   results, in order of likelihood:
   - `Message sent.` with "present in the private chat relay" — the node's own chat list already
     returned the returned signature (this node, not proof of owner receipt);
   - `Message submitted, delivery unconfirmed.` — the host acknowledged but the read-back did not
     confirm within ~3 s. This is *not* a failure; do not resend.
   Either is acceptable for validation. Record the exact text, and the signature + timestamp from
   `Technical details`.
5. **Check for duplicates.** Expected: exactly one message. Do not press Send again at any point
   during this procedure; if the result was ambiguous, stop and report instead of resending.
6. **Verify owner receipt.** In the owner's Qortal client, open current Qortal chat (private chat, not
   Q-Mail) for the visitor account. Expected: the message text is present once, in the visitor ->
   owner direction. Capture: time, whether it appeared, and the client's node/version.
7. **Verify reload/navigation state.** Reload the Contact page and also navigate away and back.
   Expected: a clean page with an empty message field and no stale success/failure panel; the owner
   name resolves again.
8. **Record failures truthfully.** If any step fails (no dialog, host error, "Cannot send an encrypted
   message…", insufficient-balance message, timeout, empty field after typing), capture the exact
   visible text plus the technical-details values if present. Report it as a failure; do not retry
   repeatedly, because a chat message is not idempotent.

## Evidence to return

- Hub version + host node `buildVersion`; date/time with timezone.
- Whether the approval dialog appeared, and the result text verbatim.
- The chat signature and signed-at timestamp, if shown.
- The owner-side observation (present / not present / how long it took).
- Confirmation that the message appeared exactly once and that the reloaded page was clean.
- Anything unexpected, verbatim.

## Out of scope for this validation

Q-Mail sending, public chat, group chat, attachments, group membership, retention configuration
changes, node/Hub changes, QDN publication, and any commit/push/deploy. None of those are part of this
feature, and none are authorized by this handoff.

## After a successful validation

1. Promote the harvest candidate to a reusable skill (`skills/qortal/private-chat-contact-form`,
   maturity `candidate` -> `verified-runtime`) under a separate skill-promotion authorization; see the
   implementation report §14.
2. Authorize an application commit/branch and (separately) a deploy if the accepted baseline should
   include the Contact feature.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-14-contact-private-chat-owner-live-validation-handoff.md`

## Superseding accepted owner result (2026-09-15)

The owner completed this procedure and accepted the Contact/private-chat flow as **OWNER-RUNTIME
PASS**. The observed outcome was a host-approved message arriving successfully in the owner’s current
Qortal private chat, with no duplicate-send issue; reload/navigation returned the page to a clean
state. This records owner evidence only. It does not establish a deployed artifact hash, a release,
or a new runtime test run by DeepSeek or the report writer.

The accepted product decision remains: use Qortal private chat for simple Contact; retain the
limited-retention/Q-Mail-for-durable-contact notice; do not implement direct Q-Mail sending or any
silent fallback. The normal-chat approximately 24-hour figure remains tied to Core `108bf191` current
chain config. Reticulum DM’s approximately one-month store is separate Hub storage and unavailable
through the Q-App bridge.
