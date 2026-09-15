# Shadow Archives Contact workflow on Qortal private chat — implementation report

Executing agent (registered role of the agent that actually produced this work): `DeepSeek`
Report/handoff writer (if different from the executing agent): same agent
Executing-agent evidence: the working session ran inside the Codex CLI tool profile with
`CODEX_HOME=/home/iffi/.codex-deepseek` and `CODEX_SESSION_ID=01a09f65-8b44-7c02-8501-062175464ffe`;
that profile's `config.toml` declares `model = "deepseek-flash"`, `model_provider = "deepseek"`.
The CLI/harness profile is recorded as the tool, not as the author.
Report type: implementation (autonomous feature vertical; research → design → implementation → validation → self-audit)
Exact application repository / branch / SHA:
`/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL` on
`agent/shadow-archives-webportal/owner-runtime-checkpoint-20260913` at base `c9ce071`
(`c9ce0716f87c4d083c01601678d0354102f455ac`), with the uncommitted feature changes listed in §8.
Canonical report path / SHA-256 / authorized remote evidence:
`/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/implementation/2026-09-14-contact-private-chat-implementation-report.md`
(SHA-256 in §17); no remote evidence — nothing was committed or pushed.

## 1. Objective and exit criterion

Deliver one completed feature vertical: a visitor opens Contact, writes a private message, the app
resolves the CURRENT Shadow Archives owner from the app's own publishing name, sends the message
through **current Qortal private chat** (`SEND_CHAT_MESSAGE`), and reports the outcome truthfully —
preserving the draft whenever the result is not an acknowledged submission. Direct Q-Mail sending is
out of scope; retention copy must reflect verified current behaviour, not the unverified "one month".

Exit criterion (not yet met, by design): the feature is complete and ready for exactly ONE owner
live-host validation, where the owner performs the authorized private-message send and confirms the
message arrives in current Qortal chat. Automated evidence cannot substitute for that step, and this
report does **not** claim runtime PASS.

## 2. Confirmed current private-chat contract

All revisions below were re-verified on 2026-09-14 by reading the clean reference clones under
`/home/iffi/VsCodec-Projects/github-clones/Qortal/` (`git status --porcelain` empty for every clone):

| Repository | Revision | Notes |
| --- | --- | --- |
| `qortal` (Qortal Core) | `108bf191` | "Bump version to 6.1.9" |
| `Qortal-Hub` | `12a573b2` | branch `develop`; same revision pinned by the project standard |
| `qapp-core` | `0f9d6ac` | request interfaces |
| `Quitter` / `Subwire` / `q-tube` / `qapp-templates` | `4e4246c` / `a933a6c` / `68c3ea7` / `143cc7b` | donor apps, read-only |

Both owner-controlled development nodes report `buildVersion: "qortal-6.1.9-108bf19"` (i.e. the same
Core revision) and `isTestNet: false`.

### 2.1 Which bridge action actually sends a private message

`SEND_CHAT_MESSAGE` is the correct action, and it is **host-mediated, not frame-handled**:

- Core `108bf191` `src/main/resources/q-apps/q-apps.js` has no `case "SEND_CHAT_MESSAGE"` in the
  request switch, so the request falls into `default:` which sets
  `event.data.requestedHandler = "UI"` and `parent.postMessage(event.data, "*", [event.ports[0]])`.
  The app window therefore cannot send a chat message by itself; the host must.
- The same file's `getDefaultTimeout()` has an explicit `case "SEND_CHAT_MESSAGE": return 60 * 1000`
  ("Chat messages rely on PoW computations, so allow extra time").
- Core `Q-Apps.md` documents `SEND_CHAT_MESSAGE` with `destinationAddress` + `message` and marks it
  as requiring user approval. `SEARCH_CHAT_MESSAGES` is documented separately and *is* handled
  in-frame.

### 2.2 Exact request shape (application → bridge)

The app sends exactly three fields, and no others:

```json
{ "action": "SEND_CHAT_MESSAGE", "destinationAddress": "<recipient address>", "message": "<plain text body>" }
```

Justification, from Hub `12a573b2` `src/qortal/get.ts` `sendChatMessage`:

- recipient: `data.destinationAddress || data.recipient` — the documented `destinationAddress` is
  used; `recipient` is an accepted alias in `qapp-core` `0f9d6ac`
  `src/types/qortalRequests/interfaces.ts`.
- body: `data.message` (a bare string). The host wraps it into the legacy TipTap envelope
  `{messageText: {type:'doc',content:[{type:'paragraph',content:[{type:'text',text:<body>}]}]}, images: [], repliedTo: '', version: 3}`.
- `data.groupId === undefined` selects the direct (recipient) branch. The app never sends `groupId`,
  so a group message is structurally impossible from this feature.
- **No subject, no recipient public key, no encryption flag, no message id** is sent. The host owns
  all of those; inventing them would be ignored at best.

### 2.3 Host handling and approval semantics

- Permission: `getPermission('qAPPSendChatMessage-<appName>')`, otherwise `getUserPermission({text1:
  "…permission to send this chat message", text2: "…to <recipient>", text3: <first 25 chars of the
  message>, checkbox1: "always allow chat messages from this app"})`. The visitor sees the recipient
  address and the message preview in the dialog. A previously granted "always allow" skips it.
- Declining throws the Hub error `question:message.generic.user_declined_send_message`
  ("user declined to send message"), which the app classifies as `rejected`.
- Balance gate: `MIN_REQUIRED_QORTS = 4` (`src/constants/constants.ts`); below it the Hub throws the
  localized `qortals_required` error before any signing.
- Recipient encryptability gate: for a direct message the Hub fetches
  `/addresses/publickey/{recipient}` and throws "Cannot send an encrypted message to this user since
  they do not have their publickey on chain." when the recipient has no key on chain.
- Signing/relay: the host builds transaction type 18, sets `isEncrypted: 1`, `isText: 1`, performs
  proof-of-work (`difficulty = 8` in the Hub) and POSTs the signed transaction as
  base58 to `/transactions/process?apiVersion=2`.

### 2.4 Exact response shape (bridge → application)

`signChatFunc` returns whatever `processTransactionVersion2Chat` parsed: the HTTP body of
`POST /transactions/process?apiVersion=2` parsed with `response.json()` (falling back to text). Core
`TransactionsResource.processTransaction` marshals the **`ChatTransactionData`** for CHAT and returns
it as `text/plain` JSON, so the app receives the marshalled transaction data:

```json
{
  "type": "CHAT", "timestamp": <ms>, "reference": "<base58>", "fee": "<QORT>",
  "signature": "<base58>", "txGroupId": 0, "recipient": "<owner address>",
  "blockHeight": null, "blockSequence": null, "approvalStatus": "NOT_REQUIRED",
  "creatorAddress": "<sender address>"
}
```

Two source facts matter here and one of them was a real defect found by self-audit (§11):

- `creatorAddress` is the sender. It is produced by
  `TransactionData.getCreatorAddress()` (`Crypto.toAddress(creatorPublicKey)`, annotated
  `@XmlElement(name = "creatorAddress")`); `creatorPublicKey` itself is `@XmlTransient`. There is no
  `sender` field on this object.
- `signature` is a **submission identifier**, not a delivery receipt. `ChatTransaction.isConfirmable()`
  returns `false` (Core `src/main/java/org/qortal/transaction/ChatTransaction.java`), so a CHAT
  transaction can never enter a block. Nothing in Core can ever "confirm" a chat message.

### 2.5 Privacy and where encryption happens

Encryption is done entirely by the host: ed2curve + `nacl.secretbox`, `isEncrypted: 1`, `isText: 1`,
addressed to the recipient's on-chain public key. The app never sees, sends or stores a private key,
and it never sees the ciphertext or the plaintext of any other message. Direct (recipient) messages
are always encrypted; only the Hub's group branch uses `isEncrypted: 0`, which this feature cannot
reach. The app must not be given (and does not send) the recipient public key.

### 2.6 Read-back for independent verification

`SEARCH_CHAT_MESSAGES` **is** handled in-frame by `q-apps.js` (→ `GET /chat/messages`) and maps
`involving`, `encoding`, `limit`, `offset`, `reverse`, `before`, `after`, `txGroupId`,
`reference`, `chatreference`, `haschatreference`. Constraints verified from Core
`src/main/java/org/qortal/api/resource/ChatResource.java`:

- exactly two `involving` addresses (or `txGroupId` alone); otherwise `ApiError.INVALID_CRITERIA`
  (live: HTTP 400, `{"error":125,"message":"invalid search criteria"}`);
- each address must be a valid address, else `ApiError.INVALID_ADDRESS` (error 102);
- matching is done over `ChatTransactionDelegate`'s in-memory **validated chats**, keeping messages
  where both supplied addresses are the sender or the recipient — so a just-sent direct message is
  visible to its own sender+recipient pair;
- the returned `ChatMessage` includes `signature` (and encrypted `data`, which this app never reads).

This proves only that **this node's** chat store holds the message. It is not proof that the owner
received or read it, and the UI says so.

### 2.7 Size and payload limits

- Core `ChatTransaction.MAX_DATA_SIZE = 4000` bytes applies to the **encrypted** blob.
- `nacl.secretbox` adds a 16-byte authenticator, so the JSON envelope the host encrypts must fit in
  3984 bytes. The app rebuilds the host envelope locally and refuses an oversized body *before* an
  approval prompt is raised (`CHAT_ENVELOPE_MAX_BYTES = 3984`, product limit 2000 characters).
- The sender may not have more than `maxRecentChatMessagesPerAccount` unconfirmed CHAT transactions
  inside `recentChatMessagesMaxAge`; the node then rejects with `TOO_MANY_UNCONFIRMED`
  ("account has too many unconfirmed transactions pending"), surfaced by the API as
  `ApiError.TRANSACTION_INVALID` (312). Both are node settings, so the copy names no number.

### 2.8 Fees, PoW and who pays

There is no fee payment from the app and no fee field in the request. The relay cost is the host's
proof-of-work (difficulty 8 above 4000 QORT confirmed balance, 18 below) plus the Hub's
`MIN_REQUIRED_QORTS = 4` balance precondition. The app neither constructs nor inspects the
transaction.

### 2.9 Timeout and ambiguous-send behaviour

The shim's own action timeout for `SEND_CHAT_MESSAGE` is 60 s and is applied around the host call, so
a timeout can occur **after** the user approved and after the transaction may already have been
relayed. The app therefore treats a timeout as `ambiguous` and never as success or failure.

### 2.10 Duplicate-send risk and retry policy

A CHAT transaction is not idempotent: the host supplies a fresh random reference and timestamp per
call, and CHAT is never block-confirmed, so there is no natural dedup key. Consequences implemented:

- no automatic retry anywhere in the feature, for any outcome;
- a double-click/submit-repeat guard plus a disabled button while in flight;
- after an ambiguous result the button relabels to "Send again (may duplicate)" with a title
  explaining the risk, and the draft is preserved so the visitor decides.

### 2.11 Host/runtime restrictions

- Sending requires an Electron Hub or extension host that routes `SEND_CHAT_MESSAGE`; the gateway
  build refuses interactive features. A published read-only frame with `_qdn*` injected but no
  reachable host bridge is a valid read-only runtime and must fail closed (it does, with its own
  explanation), not be reported as a browser.
- Electron main/browser context restrictions (wallet unlock, host version) surface as host errors and
  are reported as failures; they are not re-classified as success.

## 3. Retention: verified behaviour (correction to the brief)

**The brief's "about one month" is not the retention of a `SEND_CHAT_MESSAGE` message.** Verified
from source:

- A chat message is an unconfirmed `CHAT` transaction; `ChatTransaction.isConfirmable()` is `false`.
- Nodes drop unconfirmed transactions once `now >= timestamp + BlockChain.getTransactionExpiryPeriod()`
  (`Transaction.getDeadline()`), by `Controller.deleteExpiredTransactions()` which runs every
  `DELETE_EXPIRED_INTERVAL = 5 * 60 * 1000` ms.
- `ChatTransactionDelegate.cleanup()` (scheduled every 1 hour) prunes validated chats older than the
  same period; `HSQLDBChatRepository` queries and `ChatTransactionDelegate.isValid()` use it too
  (older messages are even rejected as `TIMESTAMP_TOO_OLD`).
- `transactionExpiryPeriod` is `86400000` ms (**24 hours**) in `qortal` `108bf191`
  `src/main/resources/blockchain.json` (and `testchain.json`). It is chain configuration, validated
  only as "positive" (`BlockChain.java`), so it is not a universal constant.

Read-only runtime evidence (`docs/shadow-archives-webportal/live-evidence/2026-09-14-contact-private-chat-read-only.json`):
`GET /admin/settings` is readable on both owner nodes and reports
`maxRecentChatMessagesPerAccount: 250`, `recentChatMessagesMaxAge: 3600000` (1 h) and
`maxUnconfirmedPerAccount: 25`. These are the **per-account rate limit** for pending unconfirmed chat
transactions, *not* message retention; reading them as retention would be wrong. No read-only endpoint
exposes the chain configuration, so the 24 h figure rests on the packaged `blockchain.json` at the
revision both nodes report.

Where the one-month figure does come from: the Hub's separate Reticulum DM store
(`Qortal-Hub` `12a573b2` `electron/src/reticulum-chat-db.ts`, `RETICULUM_DM_DEFAULT_EXPIRY_MS = 30 ×
24 h`; i18n `group.dm.expiry_notice` = "DMs expire after 1 month by default", user-adjustable). A
Q-App cannot reach that transport: the injected bridge exposes no Reticulum action.

Product decision taken from that evidence: the notice names the verified window, states that the
exact period is network/node dependent, and does not promise a reply deadline.

## 4. Recipient (current owner) resolution

- No owner name, address or public key is hardcoded anywhere in the app; the identity comes from the
  `_qdnName` the host injects for the published `APP` resource, decoded to `publisherName`
  ("Shadow Archives").
- `GET_NAME_DATA` (`/names/{name}`) gives the **current** owner; `GET_ACCOUNT_DATA`
  (`/addresses/{address}`) confirms the owner has an on-chain public key.
- Resolution runs on mount *and again immediately before every send*, so a name transfer between page
  load and send cannot silently message the previous owner.
- Failure closes the flow before any approval prompt, with distinct truthful reasons:
  `proxy-context`, `not-a-qortal-frame`, `no-host-bridge` (published read-only frame), `no-publisher-name`,
  `name-unresolved`, `recipient-not-encryptable`.
- Read-only runtime confirmation: `/names/Shadow%20Archives` → owner
  `QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA` (identical on both nodes); `/addresses/{owner}` → publicKey
  `2q9PKM4yBmqiZhx6q54wEFGJHUvfmddpbBQ8J6UXfDfv`. The owner address/public key are used only for the
  send and the read-back; they are never rendered in the visitor UI.
- The app does not send the public key: the host resolves it itself. The key is checked only to fail
  closed *before* the visitor is asked to approve a doomed send.

## 5. Architecture

```text
ContactPage (React, visitor UI, lazy route chunk)
  -> services/contactMessage        validation + envelope/byte budget
  -> services/contactService        orchestration + outcome model + verification policy
       -> services/contactRecipient owner resolution (fail-closed codes)
       -> qortal/chat               the ONLY module that speaks the chat bridge
            -> qortal/bridge        the only module that touches the injected global
```

- `qortal/chat.ts` is deliberately **not** re-exported from `qortal/index.ts`; the entry chunk
  contains only the shared action-name constants (§8 build evidence).
- `qortal/actions.ts` documents `SEND_CHAT_MESSAGE` as a non-idempotent, approval-gated write and
  `SEARCH_CHAT_MESSAGES`/`GET_ACCOUNT_DATA` as public idempotent reads.
- No Q-Mail code, package or runtime dependency: the only Q-Mail occurrences are retention copy and
  test/comment text.
- The draft lives only in component state; nothing is persisted and the message body is never logged.

## 6. Send-result and ambiguity model

| Outcome | Trigger | UI | Draft |
| --- | --- | --- | --- |
| `sent` / `delivery: "confirmed"` | host returned a submission **and** the node's own chat list already contains the returned signature | "Message sent." + node-scoped wording | cleared (only if unchanged) |
| `sent` / `delivery: "submitted"` | host acknowledged but the read-back did not (yet) show it | "Message submitted, delivery unconfirmed." + warning not to retry immediately | preserved |
| `ambiguous` | bridge timeout (possibly after approval) | "Send result unknown." + warning; button becomes "Send again (may duplicate)" | preserved |
| `rejected` | visitor declined the host dialog (or host refused before signing) | "Not sent." + reason | preserved |
| `failed` | anything before signing: no bridge, insufficient balance, recipient without public key, node chat limit, other host error | "Not sent." + classified, actionable copy | preserved |

Never: an optimistic success, an automatic retry, a fabricated delivery confirmation, or a silent
fallback to public chat / QDN / Q-Mail. `Technical details` shows only the chat signature and the
signed-at time — never the body, recipient address or public key.

## 7. Files changed

Modified (tracked):

- `src/features/contact/ContactPage.tsx` — the Contact page (was a `RoutePlaceholder` stub).
- `src/qortal/actions.ts` — `GET_ACCOUNT_DATA` + `SEARCH_CHAT_MESSAGES` added to
  `PUBLIC_READ_ACTIONS`; `SEND_CHAT_MESSAGE` added to `WRITE_ACTIONS`; contract comment re-verified
  against Core `108bf191` / Hub `12a573b2` / `qapp-core` `0f9d6ac`.

Added:

- `src/qortal/chat.ts` — private-chat transport (`SEND_CHAT_MESSAGE`, `SEARCH_CHAT_MESSAGES`),
  timeouts, submission/attempt taxonomy. Not re-exported from the barrel.
- `src/services/contactMessage.ts` — envelope + byte budget + draft validation.
- `src/services/contactRecipient.ts` — owner resolution and failure codes.
- `src/services/contactRetention.ts` — verified retention policy + notice text.
- `src/services/contactService.ts` — orchestration, outcome model, bounded read-back, error
  classification.
- `src/features/contact/contact.css` — Contact-only layout (shared form primitives stay in
  `owner.css`, which the page imports, matching the existing owner-panel pattern).
- Tests: `src/qortal/chat.test.ts`, `src/services/contactMessage.test.ts`,
  `src/services/contactRecipient.test.ts`, `src/services/contactService.test.ts`,
  `src/features/contact/ContactPage.test.tsx`,
  `src/features/contact/contactBridgeFlow.test.tsx` (production-wiring test with **no** injected
  dependencies over a fake injected bridge).

Nothing in `qortal-core`, `Qortal-Hub`, other clones or any other project was modified.

## 8. Evidence by layer

Static / automated (2026-09-14, Node per project defaults, repo at `c9ce071` + these uncommitted changes):

- `npm run typecheck` (`tsc -b`) — clean.
- `npm run lint` (`eslint .`) — clean (it initially failed on a real
  `react-hooks/set-state-in-effect` violation in the mount effect, see §11).
- `npm run format:check` (Prettier) — clean.
- `npm test` (`vitest run`) — **57 files / 632 tests passed**, including the 6 Contact-focused files
  (70 tests): `ContactPage.test.tsx` 16, `contactBridgeFlow.test.tsx` 4, `chat.test.ts` 13,
  `contactRecipient.test.ts` 13, `contactService.test.ts` 15, `contactMessage.test.ts` 9.
  The Contact files were additionally run 5× in a row to check for flakiness after the fix in §11.
- `npm run build` (`tsc -b && vite build`) — built in ~16 s, 244 modules. Entry chunk
  `index-*.js` 393.69 kB raw / 123.67 kB gzip; Contact route chunk `ContactPage-*.js` 13.76 kB raw /
  4.88 kB gzip plus `ContactPage-*.css` 1.59 kB.
- Startup-graph boundary verified against the emitted bundle: `destinationAddress`, `involving`,
  `creatorAddress` and `BASE64` appear **only** in the `ContactPage` chunk (count 0 in the entry
  chunk); the entry chunk contains only the shared `SEND_CHAT_MESSAGE`/`SEARCH_CHAT_MESSAGES` action
  *name constants* from `qortal/actions.ts`. A unit test asserts `qortal/chat` is not re-exported
  from the barrel.

Runtime (read-only, no writes): see
`docs/shadow-archives-webportal/validation/2026-09-14-contact-private-chat-live-read-only-validation.md`
and `live-evidence/2026-09-14-contact-private-chat-read-only.json`. Summary: both nodes
`qortal-6.1.9-108bf19` mainnet; name owner and owner public key reproduced; `/chat/messages`
returns a JSON array for a valid two-address pair (probe pair deliberately chosen to return zero
elements, and message content was deliberately not recorded); the same endpoint reports
`{"error":125,"message":"invalid search criteria"}` for missing/one-sided criteria and error 102 for
an invalid address.

Real host / owner acceptance: **not executed** — see §13. This is the only remaining gate and it
requires the owner to authorize and perform one live private-message send.

## 9. Checks not executed and why

- Live `SEND_CHAT_MESSAGE` send: not authorized during implementation; it is the single owner
  validation step in §13.
- Any write to Core/Hub/QDN: outside authorization.
- Real Electron-Hub rendering of the finished page: not available in this environment; the
  production-wiring test uses the real bridge paths against a fake injected `qortalRequest`, and the
  read-only node evidence covers the node-side contract. Only the owner's host run proves the
  end-to-end path.
- A node-API confirmation of `transactionExpiryPeriod`: no read-only endpoint exposes it, so the 24 h
  value is source/packaged-config evidence at the revision both nodes report.

## 10. Adversarial self-audit

Performed after the suite was green. Findings and dispositions:

1. **BLOCKER (fixed) — the confirmation path was unreachable.** `chat.ts` read the sender from
   `record.sender`, but the marshalled `/transactions/process` response exposes it as
   `creatorAddress`. Every send would have been reported "submitted, unconfirmed", permanently
   weakening the truthful outcome and making the read-back dead code. Fixed by reading
   `creatorAddress` (with `sender` kept as a fallback), documented against
   `TransactionData.getCreatorAddress()`, and covered by tests using the real response shape.
2. **HIGH (fixed) — user input was silently discarded.** The message field was
   `disabled={recipient === null || pending}`, so a visitor who began typing before the ~200 ms node
   lookup, or while the host was working, lost everything they typed. Found by a flaky test, then
   fixed at the root: the field stays writable; only Send is gated on a resolved recipient, and the
   recipient is re-resolved at send time regardless. A draft typed during an in-flight send is now
   also preserved instead of being cleared with the submitted text.
3. **HIGH (fixed) — lint violation of React's effect rules.** `setResolution({status:'resolving'})`
   inside the mount effect (`react-hooks/set-state-in-effect`). Replaced by a render-derived
   resolution keyed to the dependency graph, which also removes a cascading render.
4. **MEDIUM (fixed) — misleading copy.** The retention notice implied a reply-window
   ("if you have not received a reply by then"), which does not follow from a 24 h relay window;
   reworded to describe relay retention and to advise Q-Mail for anything durable. The pending
   message text also named only the host while the app was already waiting on the node read-back.
5. **MEDIUM (fixed) — retention-misreading risk.** `recentChatMessagesMaxAge` (1 h) is a rate-limit
   window, not retention. Documented in the policy module and in this report so a later agent does
   not advertise "1 hour" retention.
6. **LOW (fixed) — rate-limit failure was unclassified.** `TOO_MANY_UNCONFIRMED` now maps to a
   distinct, actionable `too-many-pending` message instead of a raw host string.
7. **LOW (fixed) — style/consistency.** Restored the page JSDoc to the component, used a JSX comment
   for the in-JSX rationale, and used the shared `components/common` barrel for `Skeleton`.
8. **Reviewed, no change:** `maxLength` on the field is 2× the product limit so an over-long paste is
   *shown* as over-long (counter) and refused by the shared validator rather than silently truncated;
   the owner address/public key are never rendered; the draft is never persisted; the sender line
   shows the visitor's own address only when the session already knows it (no permission prompt is
   triggered by visiting Contact).
9. **Reviewed, no change:** no Q-Mail, public-chat, QDN or group-chat path exists in the code; an
   assertion pins the write-action vocabulary so a future transport must be a deliberate addition.

## 11. External actions

None. No commit, push, branch, tag, release, deploy, QDN publication, signing, transaction or issue
mutation was performed, and no live private-message send was executed. The only network activity was
read-only HTTP against the two owner-controlled local nodes and read-only inspection of the local
reference clones.

## 12. Remaining risks and follow-up

- **Owner acceptance is pending** (§13); automated evidence cannot prove that the owner receives the
  message in current Qortal chat.
- **Retention is chain-configurable**: if a future chain config or a node's config changes
  `transactionExpiryPeriod`, the notice's "about 24 hours" becomes stale. Freshness trigger: any Core
  chain-config change, or a Hub notice that disagrees.
- **`creatorAddress` is the app's only sender source.** If a future Hub/extension host returns a
  different shape, the read-back silently degrades to `submitted` rather than lying — acceptable, but
  worth re-checking on any Hub bump (`sendChatMessage` / `signChatFunc`).
- **`/chat/messages` visibility is node-local and short-lived**; the read-back can legitimately miss a
  message the node has already pruned or has not indexed, which is why the unconfirmed state exists.
- **No `subject`, attachments or rich text** by design; the current contract has no subject, and the
  host's legacy envelope supports images only for hosts that send `fullMessageObject`, which this
  feature deliberately does not.
- **Host approval copy is host-owned** (recipient address and message preview appear in the Hub
  dialog); the app cannot change it.
- Follow-up if the owner wants durable contact: a Q-Mail navigation link would be a separate,
  separately approved change; the brief explicitly kept Q-Mail sending out of scope.

## 13. Owner live-host validation (the one required procedure)

Full step-by-step procedure:
`docs/shadow-archives-webportal/handoffs/2026-09-14-contact-private-chat-owner-live-validation-handoff.md`.
Summary: open the published app in the Qortal Hub, open Contact, confirm the recipient shows the
current publishing name and the retention notice names the verified period, send one short synthetic
message, approve the host dialog once, confirm the truthful result (and the signature under
"Technical details"), then confirm the message appears in current Qortal chat for the owner account
from the visitor account, confirm no duplicate message exists, and finally reload/navigate away and
back to confirm the Contact page returns to a clean, sensible state. Evidence to capture: node
build version, Hub version, timestamps, the visible result text, the signature, whether the approval
dialog appeared, and the chat-store observation. Until that is done this feature is
`owner_validation_pending`, not PASS.

## 14. Skill-harvest candidate

Candidate (do **not** create in this task):
`skills/qortal/private-chat-contact-form` — platform `qortal`, maturity `candidate` until the owner
live send passes, then promotable. Reusable content: the current `SEND_CHAT_MESSAGE` action and its
host-mediated/`requestedHandler: "UI"` nature and 60 s shim timeout; the exact request shape
(`destinationAddress` + bare `message`, never a public key/groupId/subject); the marshalled
`creatorAddress` sender field and the absence of any block confirmation; recipient resolution from
the publishing name with a freshness rule; encryption/approval/fee/PoW semantics; the 4000-byte
encrypted cap and 3984-byte envelope budget; the ambiguous-send, duplicate-risk and no-automatic-retry
rules; the read-back `SEARCH_CHAT_MESSAGES` two-address contract and its node-local limit; the
verified 24 h retention with the 1 h rate-limit caveat; and the truthful UX boundary (submitted ≠
delivered). Freshness/invalidation triggers: Core chain-config change, Hub `sendChatMessage`/
`signChatFunc` change, `q-apps.js` action/timeout change, or an API change to
`/transactions/process` or `/chat/messages`. No skill file was created or modified by this task.

## 15. Git state

- Repository: `/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL`
- Branch: `agent/shadow-archives-webportal/owner-runtime-checkpoint-20260913`, base HEAD `c9ce071`
- Tracked modifications: `src/features/contact/ContactPage.tsx`, `src/qortal/actions.ts`
  (`git diff --stat`: 2 files, +389/−12)
- Untracked additions: `src/qortal/chat.ts`, `src/qortal/chat.test.ts`,
  `src/services/contactMessage.ts`, `src/services/contactMessage.test.ts`,
  `src/services/contactRecipient.ts`, `src/services/contactRecipient.test.ts`,
  `src/services/contactRetention.ts`, `src/services/contactService.ts`,
  `src/services/contactService.test.ts`, `src/features/contact/ContactPage.test.tsx`,
  `src/features/contact/contact.css`, `src/features/contact/contactBridgeFlow.test.tsx`
- Pre-existing user-owned untracked `AGENTS.md` left untouched.
- `git diff --check`: clean. **No commit, no push, no merge.** `handoff_sync = pending_authorization`.

Report repository (this workspace):

- Repository: `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace`
- Branch: `agent/shadow-archives-webportal/owner-runtime-docs-20260913`, HEAD `6eccf6d`
- This report and its three companions are new untracked files; nothing was committed or pushed.
  A pre-existing untracked report (`implementation/2026-09-11-owner-runtime-visual-correction-report.md`)
  was left untouched.

## 16. Report saved

- Absolute path:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/implementation/2026-09-14-contact-private-chat-implementation-report.md`
- Companion files:
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/validation/2026-09-14-contact-private-chat-live-read-only-validation.md`,
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/handoffs/2026-09-14-contact-private-chat-owner-live-validation-handoff.md`,
  `/home/iffi/VsCodec-Projects/Qortal/qortal-dev-workspace/docs/shadow-archives-webportal/live-evidence/2026-09-14-contact-private-chat-read-only.json`
- SHA-256: recorded in §17.

## 17. Report hashes

```
40e3f882b22c9a57fdce7193cc2e8ddec1fff385a742dbda2f4b189b548dfd8f  validation/2026-09-14-contact-private-chat-live-read-only-validation.md
e460e5b7de3742517d5cb7e990ee0bd998c5198d722cea2372e179a2af2dff74  handoffs/2026-09-14-contact-private-chat-owner-live-validation-handoff.md
8fa8cbcdf6e64126b86f95d7a8a99c9124568beabff817374d5ca0ccdf584183  live-evidence/2026-09-14-contact-private-chat-read-only.json
```

This file's own digest is intentionally not recorded here (any self-referential digest would be stale
the moment it is written); verify the current file with `sha256sum` if an exact digest is needed.
Paths above are relative to `docs/shadow-archives-webportal/`.

## 18. Superseding owner-runtime acceptance (2026-09-15)

Owner result: **FULL PASS** for the accepted Contact/private-chat workflow in a real Qortal host.
The owner confirmed current registered-name recipient resolution, one host-approved send, successful
arrival in the owner's current private chat, no duplicate-send issue, and a clean Contact page after
reload/navigation. This is owner evidence, not a second send or runtime test by the report writer.

The product decision is unchanged: keep current Qortal private chat, retain the limited-retention /
Q-Mail-for-durable-contact notice, and do not redesign this feature as Q-Mail. The approximately
24-hour value remains scoped to Core `108bf191` and its current chain configuration; Reticulum DM's
approximately one-month storage is a separate Hub transport unavailable to Q-Apps through the
verified bridge. The reusable contract was promoted separately as
`AI-Orchestration/skills/qortal/private-chat-contact-form/SKILL.md` with maturity
`verified-runtime`.
