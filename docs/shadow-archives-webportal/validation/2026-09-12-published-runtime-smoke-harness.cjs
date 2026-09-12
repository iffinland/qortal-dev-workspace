/* Shadow Archives production smoke test: plain browser, render-without-bridge,
 * and render-with-emulated-bridge. Serves dist/ the way Core's render path does
 * (inject <base> + _qdn* + a classic-script bridge) and drives headless Chrome
 * over CDP. No repo dependency is added. */
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { spawn } = require('node:child_process');
const WebSocket = require('/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL/node_modules/ws');

const DIST = '/home/iffi/VsCodec-Projects/shadow-archives/shadow-archives-webportal/QORTAL/dist';
const PREFIX = '/render/APP/Shadow%20Archives';
const CHROME = '/usr/bin/google-chrome';

const QDN_VARS = (ctx) => `<script>var _qdnContext="${ctx.context}"; var _qdnTheme="dark"; var _qdnLang="en"; var _qdnService="${ctx.service}"; var _qdnName="${ctx.name}"; var _qdnIdentifier=""; var _qdnPath="/"; var _qdnBase="${ctx.base}"; var _qdnBaseWithPath="${ctx.base}";</script>`;
// Byte-for-byte the declaration style Core v6.1.9 uses in /apps/q-apps.js:
// a top-level `const` in a classic script (NOT a window property).
const BRIDGE_SHIM = `<script>
const qortalRequest = (request) => {
  window.__bridgeCalls = (window.__bridgeCalls || []).concat([request.action]);
  switch (request.action) {
    case 'SEARCH_QDN_RESOURCES': return Promise.resolve([]);
    case 'GET_USER_ACCOUNT': return Promise.resolve({ address: 'QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA', publicKey: 'K' });
    case 'GET_ACCOUNT_NAMES': return Promise.resolve([{ name: 'Shadow Archives', owner: 'QPw4vnk5CBDWkgdXB4vUXCc4DXGEjHVxCA' }]);
    case 'GET_NAME_DATA': return Promise.resolve({ name: 'Shadow Archives', owner: 'QPw4vnk5CBDwkgdXB4vUXCc4DXGEjHVxCA' });
    default: return Promise.resolve([]);
  }
};
</script>`;

const servers = new Map(); // variant -> {server, port, arbitraryHits, base}

function buildVariant(name, html) {
  return new Promise((resolve) => {
    const state = { arbitraryHits: [], server: null, port: 0, base: '' };
    const server = http.createServer((req, res) => {
      const url = new URL(req.url, 'http://127.0.0.1');
      let pathname = decodeURIComponent(url.pathname);
      if (pathname.startsWith('/arbitrary/')) {
        state.arbitraryHits.push(url.pathname + url.search);
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end('[]');
        return;
      }
      const variant = pathname.startsWith('/render/APP/Shadow Archives')
        ? pathname.slice('/render/APP/Shadow Archives'.length)
        : pathname;
      const rel = variant.replace(/^\/+/, '');
      if (rel.length > 0 && path.extname(rel) !== '') {
        const file = path.join(DIST, rel);
        if (fs.existsSync(file) && fs.statSync(file).isFile()) {
          const ext = path.extname(file);
          const type = ext === '.js' ? 'text/javascript' : ext === '.css' ? 'text/css' : ext === '.webp' ? 'image/webp' : 'application/octet-stream';
          res.writeHead(200, { 'content-type': type });
          res.end(fs.readFileSync(file));
          return;
        }
      }
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      res.end(html);
    });
    server.listen(0, '127.0.0.1', () => {
      state.server = server;
      state.port = server.address().port;
      state.base = `http://127.0.0.1:${state.port}`;
      servers.set(name, state);
      resolve(state);
    });
  });
}

function indexHtml(variant) {
  const raw = fs.readFileSync(path.join(DIST, 'index.html'), 'utf8');
  if (variant === 'plain') return raw;
  const ctx = { context: 'render', service: 'APP', name: 'Shadow%20Archives', base: PREFIX };
  const injected = `<base href="${PREFIX}/">` + QDN_VARS(ctx) + (variant === 'bridge' ? BRIDGE_SHIM : '');
  return raw.replace('<head>', `<head>${injected}`);
}

/* ---------------- minimal CDP client ---------------- */
class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.events = [];
    ws.on('message', (data) => {
      const msg = JSON.parse(data.toString());
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
      } else if (msg.method) {
        this.events.push(msg);
      }
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify(sessionId ? { id, method, params, sessionId } : { id, method, params }));
    });
  }
}

async function connect(port) {
  const list = await fetch(`http://127.0.0.1:${port}/json/version`).then((r) => r.json());
  const ws = new WebSocket(list.webSocketDebuggerUrl, { maxPayload: 256 * 1024 * 1024 });
  await new Promise((resolve, reject) => {
    ws.once('open', resolve);
    ws.once('error', reject);
  });
  return new Cdp(ws);
}

async function evaluate(cdp, sessionId, expression) {
  const result = await cdp.send(
    'Runtime.evaluate',
    { expression, returnByValue: true, awaitPromise: true },
    sessionId,
  );
  if (result.exceptionDetails) {
    throw new Error('evaluate failed: ' + JSON.stringify(result.exceptionDetails.exception));
  }
  return result.result.value;
}

async function visit(cdp, url, marker) {
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  await cdp.send('Page.enable', {}, sessionId);
  await cdp.send('Page.navigate', { url }, sessionId);
  // Wait for the requested route content, not just the shared app shell.
  const deadline = Date.now() + 25000;
  let text = '';
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 250));
    text = await evaluate(cdp, sessionId, 'document.body ? document.body.textContent : ""');
    if (text.includes(marker)) break;
  }
  await new Promise((r) => setTimeout(r, 500));
  text = await evaluate(cdp, sessionId, 'document.body ? document.body.textContent : ""');
  return { sessionId, text, close: () => cdp.send('Target.closeTarget', { targetId }) };
}

const results = [];
function check(name, pass, detail) {
  results.push({ name, pass, detail });
}

(async () => {
  const plain = await buildVariant('plain', indexHtml('plain'));
  const readonly = await buildVariant('readonly', indexHtml('readonly'));
  const bridge = await buildVariant('bridge', indexHtml('bridge'));

  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'sa-chrome-'));
  const port = 9333;
  const chrome = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--no-first-run',
    '--disable-extensions', '--disable-dev-shm-usage',
    `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    'about:blank',
  ], { stdio: 'ignore' });

  let cdp;
  for (let i = 0; i < 60 && !cdp; i++) {
    try { cdp = await connect(port); } catch { await new Promise((r) => setTimeout(r, 500)); }
  }
  if (!cdp) { console.error('could not connect to chrome'); process.exit(1); }

  try {
    // ---- A. plain browser -------------------------------------------------
    const pStudio = await visit(cdp, `${plain.base}/studio`, 'Owner studio');
    check('A plain browser /studio says plain-browser state',
      pStudio.text.includes('Plain browser — no Qortal context'),
      pStudio.text.slice(0, 160).replace(/\n/g, ' | '));
    check('A plain browser /studio is not mislabelled as published',
      !pStudio.text.includes('Published in a Qortal render context'),
      '');
    const pGallery = await visit(cdp, `${plain.base}/gallery`, 'Gallery');
    check('A plain browser /gallery does not claim a missing publisher identity',
      !pGallery.text.includes('No production Qortal publisher identity'),
      '');
    await pStudio.close(); await pGallery.close();

    // ---- B. render context, no bridge ------------------------------------
    const rStudio = await visit(cdp, `${readonly.base}${PREFIX}/studio`, 'Published in a Qortal render context');
    check('B render-no-bridge /studio reports published read-only context',
      rStudio.text.includes('Published in a Qortal render context — read-only'),
      rStudio.text.slice(0, 200).replace(/\n/g, ' | '));
    check('B render-no-bridge /studio detects the publishing identity from _qdnName',
      rStudio.text.includes('Shadow Archives'),
      '');
    check('B render-no-bridge /studio never says plain browser',
      !rStudio.text.includes('Plain browser — no Qortal context') &&
      !rStudio.text.includes('Not running in a Qortal host'),
      '');
    const rStudioDiag = rStudio.text.split('Host context diagnostics')[1] || '';
    check('B diagnostics still report no bridge truthfully',
      /Bridge available\s*\n?no/.test(rStudioDiag),
      rStudioDiag.replace(/\n/g, ' | ').slice(0, 140));

    const rGallery = await visit(cdp, `${readonly.base}${PREFIX}/gallery`, 'Gallery');
    check('B render-no-bridge /gallery does not claim a missing publisher identity',
      !rGallery.text.includes('No production Qortal publisher identity'),
      rGallery.text.slice(0, 200).replace(/\n/g, ' | '));
    check('B render-no-bridge /gallery renders a real route heading',
      rGallery.text.includes('Gallery'),
      '');
    await new Promise((r) => setTimeout(r, 500));
    check('B read fallback used same-origin GET /arbitrary/... in the browser',
      readonly.arbitraryHits.some((h) => h.startsWith('/arbitrary/resources/search')),
      JSON.stringify(readonly.arbitraryHits.slice(0, 3)));
    check('B no bridge call was possible (window.qortalRequest is undefined)',
      await evaluate(cdp, rGallery.sessionId, 'window.qortalRequest === undefined'),
      '');
    await rStudio.close(); await rGallery.close();

    // ---- C. render context with the emulated bridge -----------------------
    const bStudio = await visit(cdp, `${bridge.base}${PREFIX}/studio`, 'Enter owner mode');
    check('C render-with-bridge /studio keeps the owner flow',
      bStudio.text.includes('Owner mode') &&
      bStudio.text.includes('Enter owner mode'),
      bStudio.text.slice(0, 200).replace(/\n/g, ' | '));
    const bDiag = bStudio.text.split('Host context diagnostics')[1] || '';
    check('C diagnostics report the bridge as available (global-binding detection)',
      /Bridge available\s*\n?yes/.test(bDiag),
      bDiag.replace(/\n/g, ' | ').slice(0, 140));
    check('C the shim is a global binding, not a window property (Core semantics)',
      (await evaluate(cdp, bStudio.sessionId, 'typeof qortalRequest')) === 'function' &&
      (await evaluate(cdp, bStudio.sessionId, 'window.qortalRequest === undefined')),
      '');
    const bGallery = await visit(cdp, `${bridge.base}${PREFIX}/gallery`, 'Gallery');
    check('C bridge-host /gallery reads through the bridge, not direct HTTP',
      bridge.arbitraryHits.length === 0,
      'arbitrary hits: ' + JSON.stringify(bridge.arbitraryHits.slice(0, 3)));
    check('C bridge-host /gallery does not ask for an account',
      !(await evaluate(cdp, bStudio.sessionId, '(window.__bridgeCalls||[]).includes("GET_USER_ACCOUNT")')),
      '');
    await bStudio.close(); await bGallery.close();
  } finally {
    try { cdp.ws.close(); } catch {}
    chrome.kill('SIGKILL');
    for (const s of servers.values()) s.server.close();
  }

  let failed = 0;
  for (const r of results) {
    if (!r.pass) failed++;
    console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}${r.detail ? `\n        ${r.detail}` : ''}`);
  }
  console.log(`\n${results.length - failed}/${results.length} smoke checks passed`);
  process.exit(failed === 0 ? 0 : 1);
})().catch((e) => { console.error('smoke error:', e); process.exit(2); });
