# Contact private chat — live read-only validation (development nodes)

Executing agent: `DeepSeek` (same session/profile evidence as the implementation report)
Report type: validation — read-only runtime evidence; **no write, no chat send, no QDN publication**
Exact application repository / branch / SHA: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
on `agent/shadow-archives-webportal/owner-runtime-checkpoint-20260913` at base `c9ce071`
(+ uncommitted Contact feature changes; application code is not exercised by this read-only evidence)
Canonical report path:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/validation/2026-09-14-contact-private-chat-live-read-only-validation.md`

## Scope

Establish, from read-only runtime evidence, the parts of the Contact feature that cannot be settled by
unit tests: which node/Core revision is actually running, whether the owner/recipient identity the app
resolves matches the live chain, whether the chat read endpoint behaves as the source says, and what
retention-related configuration the node exposes read-only.

Raw capture: `docs/shadow-archives-webportal/live-evidence/2026-09-14-contact-private-chat-read-only.json`.
Environment: owner-controlled local nodes `http://127.0.0.1:24991` and `http://127.0.0.1:24992`.
No credentials, keys or private message content are recorded here or in the JSON.

## Method

`curl` GET requests only. The chat read probe was deliberately chosen to return zero elements for an
address pair whose messages are not of interest to anyone, and the capture records **only** the
response shape (`is_array`, element count, key names). No `POST /transactions/process`, no
`SEND_CHAT_MESSAGE`, no wallet/unlock endpoint and no admin-authenticated call was made. The
`/admin/settings` response is recorded as a chat-relevant subset only (the full document contains
local filesystem paths that do not belong in a report).

## Results

### Node identity

| Node | `buildVersion` | `isTestNet` | `type` |
| --- | --- | --- | --- |
| `:24991` | `qortal-6.1.9-108bf19` | `false` | `full` |
| `:24992` | `qortal-6.1.9-108bf19` | `false` | `full` |

Both nodes therefore run Core `108bf191` (v6.1.9), the exact revision the contract was read from.

### Owner / recipient identity (matches the app's resolution inputs, not hardcoded in the app)

- `GET /names/Shadow%20Archives` → owner `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA` (identical on both nodes;
  not for sale).
- `GET /names/address/{owner}` → the owner's only name is `Shadow Archives`.
- `GET /addresses/{owner}` → `publicKey 2q9PKM4yBmqiZhx6q54wEFGJHUvfmddpbBQ8J6UXfDfv`,
  `defaultGroupId 746`, `level 4`.

This is the identity the app derives at runtime from the injected `_qdnName`; nothing in the bundle
contains it.

### Chat read endpoint (`SEARCH_CHAT_MESSAGES` → `GET /chat/messages`)

| Probe | Result |
| --- | --- |
| no criteria | HTTP 400 `{"error":125,"message":"invalid search criteria"}` |
| one `involving` address | HTTP 400 `{"error":125,"message":"invalid search criteria"}` |
| one invalid address + one valid | HTTP 400 `{"error":102,"message":"invalid address"}` |
| two valid `involving` addresses | HTTP 200, JSON array (shape probe: 0 elements for the probed pair) |

This confirms live the `ChatResource.searchChat` contract the app relies on for its signature-only
read-back: exactly two addresses, both validated, array response.

### Retention-related configuration exposed read-only

`GET /admin/settings` (readable without an API key on these nodes; `apiRestricted: false`,
`apiWhitelist: ["::1","127.0.0.1"]`) reports the chat-relevant subset:

```json
{ "maxUnconfirmedPerAccount": 25, "maxRecentChatMessagesPerAccount": 250,
  "recentChatMessagesMaxAge": 3600000, "wipeUnconfirmedOnStart": false }
```

Interpretation (source-verified in the implementation report): `maxRecentChatMessagesPerAccount` /
`recentChatMessagesMaxAge` are the per-account **rate limit** on pending unconfirmed CHAT
transactions (`ChatTransaction.isValid` → `TOO_MANY_UNCONFIRMED`), and `maxUnconfirmedPerAccount` is
the node-wide unconfirmed cap. **None of them is message retention.** Message retention is the
chain-wide `transactionExpiryPeriod` (`86400000` ms = 24 h in `blockchain.json` at `108bf191`), which
no read-only endpoint exposes; that value is therefore packaged-source evidence at the revision both
nodes report, not node-API evidence.

## What this evidence does and does not prove

- Proves: the running Core revision; the live current owner and owner public key the app must resolve;
  the chat read endpoint's live validation/response behaviour; the node-side chat settings that shape
  failure copy (rate limit) as distinct from retention.
- Does not prove: that `SEND_CHAT_MESSAGE` succeeds in a real host, that the Hub approval dialog
  behaves as documented, that the transaction is relayed to the owner's node, that the owner sees the
  message in current Qortal chat, or anything about Electron/gateway host restrictions.

Those remain in the single owner live-host validation procedure:
`docs/shadow-archives-webportal/handoffs/2026-09-14-contact-private-chat-owner-live-validation-handoff.md`.

## Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/validation/2026-09-14-contact-private-chat-live-read-only-validation.md`
- Raw evidence JSON:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/live-evidence/2026-09-14-contact-private-chat-read-only.json`

## Superseding owner-runtime acceptance (2026-09-15)

The owner subsequently completed the real-host procedure with **FULL PASS**: the approved message
arrived once in the owner's current private chat and the Contact flow reloaded cleanly. This report
remains read-only evidence only; it does not claim to have performed the send. Retention remains
source-scoped to Core `108bf191` rather than a timeless node guarantee.
