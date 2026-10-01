"""Phase 3 browser harness: build a scripted-QDN page and a plain visitor page."""
import json, pathlib, shutil

ROOT = pathlib.Path('/tmp/qwb-p3-check')
DIST = pathlib.Path('/home/iffi/VsCodec-Projects/QWB-Qortal-Web-Builders/qortal-web-builders/dist')
if ROOT.exists():
    shutil.rmtree(ROOT)
shutil.copytree(DIST, ROOT)
index = (ROOT / 'index.html').read_text()
assert '<script type="module"' in index

SEED = json.loads(pathlib.Path('/tmp/qwb-p3-seed.json').read_text())
QDN_TITLE = 'QDN-served featured headline (harness)'

FAKE_NODE = """
window.__qwbCalls = [];
window.__qwbPublishes = [];
window.__qwbNode = (function () {
  var SEED = %(seed)s;
  var NAME = 'Qortal Web Builders';
  var QDN_TITLE = %(title)s;
  var store = {};
  SEED.forEach(function (entity) {
    var copy = JSON.parse(JSON.stringify(entity));
    if (copy.kind === 'highlight' && entity.id === SEED.filter(function (e) { return e.kind === 'highlight'; })[0].id) {
      copy.title = QDN_TITLE;
    }
    store[copy.id] = { service: copy.kind === 'article' ? 'DOCUMENT' : 'JSON', payload: copy, created: 1700000000000 };
  });
  function summaryFor(entry) {
    return {
      name: NAME, service: entry.service, identifier: entry.payload.id,
      size: JSON.stringify(entry.payload).length, created: entry.created, updated: entry.created,
      latestSignature: 'sig-' + entry.payload.id,
      status: { status: 'READY', id: 'READY' }
    };
  }
  function toBase64(text) {
    var bytes = new TextEncoder().encode(text);
    var binary = '';
    for (var i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
  }
  function fromBase64(value) {
    var binary = atob(value);
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }
  return {
    handle: function (request) {
      window.__qwbCalls.push(request);
      switch (request.action) {
        case 'GET_USER_ACCOUNT':
          return Promise.resolve({ address: 'QHarnessFakeAddress', publicKey: 'pk' });
        case 'GET_ACCOUNT_NAMES':
          return Promise.resolve([{ name: 'Q-Website' }, { name: NAME }]);
        case 'SEARCH_QDN_RESOURCES': {
          var prefix = typeof request.identifier === 'string' ? request.identifier : '';
          var service = String(request.service);
          var names = request.names || [];
          var matches = Object.keys(store).map(function (key) { return store[key]; }).filter(function (entry) {
            return entry.service === service && entry.payload.id.indexOf(prefix) === 0 && names.indexOf(NAME) !== -1;
          });
          matches.sort(function (a, b) { return b.created - a.created; });
          if (request.reverse !== true) matches.reverse();
          var offset = typeof request.offset === 'number' ? request.offset : 0;
          var limit = typeof request.limit === 'number' ? request.limit : 50;
          return Promise.resolve(matches.slice(offset, offset + limit).map(summaryFor));
        }
        case 'FETCH_QDN_RESOURCE': {
          var entry = store[request.identifier];
          if (!entry) {
            return Promise.reject({ error: 1401, message: "Couldn't find PUT transaction for name " + request.name + ", service " + request.service + " and identifier " + request.identifier });
          }
          if (request.encoding === 'base64') return Promise.resolve(entry.data64 || '');
          return Promise.resolve(JSON.parse(JSON.stringify(entry.payload)));
        }
        case 'GET_QDN_RESOURCE_STATUS': {
          var known = store[request.identifier];
          if (!known) return Promise.reject({ error: 1401, message: "Couldn't find PUT transaction" });
          return Promise.resolve({ status: 'READY', id: 'READY' });
        }
        case 'PUBLISH_QDN_RESOURCE': {
          window.__qwbPublishes.push({
            service: request.service, name: request.name, identifier: request.identifier,
            byteLength: typeof request.data64 === 'string' ? request.data64.length : 0
          });
          if (typeof request.data64 !== 'string' || request.data64 === '') {
            return Promise.reject({ error: 'harness: no data64' });
          }
          if (String(request.service) === 'JSON' || String(request.service) === 'DOCUMENT') {
            var payload = JSON.parse(fromBase64(request.data64));
            store[request.identifier] = { service: String(request.service), payload: payload, created: Date.now() };
          } else {
            store[request.identifier] = { service: String(request.service), payload: { id: request.identifier }, created: Date.now(), data64: request.data64 };
          }
          return Promise.resolve({ signature: 'harness-signature-' + window.__qwbPublishes.length, type: 'ARBITRARY' });
        }
        default:
          return Promise.reject(new Error('harness: unexpected action ' + request.action));
      }
    },
    store: store
  };
})();
window._qdnContext = 'render';
window._qdnService = 'WEBSITE';
window._qdnName = 'Qortal Web Builders';
window._qdnIdentifier = 'default';
window._qdnTheme = 'light';
window._qdnLang = 'en';
window.qortalRequest = function (request) { return window.__qwbNode.handle(request); };
""" % {'seed': json.dumps(SEED), 'title': json.dumps(QDN_TITLE)}

REPORT = """
(function () {
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  function headlines() {
    return Array.prototype.map.call(
      document.querySelectorAll('#section_featured article.custom-block h5 a'),
      function (a) { return a.textContent.trim(); }
    );
  }
  function barButtons() {
    var bar = document.getElementById('qwb-owner-bar');
    if (!bar) return [];
    return Array.prototype.map.call(bar.querySelectorAll('button'), function (b) { return b.textContent.trim(); });
  }
  function btn(label) {
    return Array.prototype.slice.call(document.querySelectorAll('button')).filter(function (b) {
      return b.textContent.trim() === label;
    })[0] || null;
  }
  function priceOrder() {
    return Array.prototype.map.call(
      document.querySelectorAll('#section_3 article.pricing-box .card-title, #section_3 article.pricing-box h5'),
      function (n) { return n.textContent.trim(); }
    );
  }
  async function run() {
    var report = { phases: {}, errors: [] };
    try {
      for (var i = 0; i < 60; i++) {
        if (document.querySelectorAll('#section_featured article.custom-block').length > 0) break;
        await sleep(250);
      }
      report.phases.read = {
        headlines: headlines(),
        bridgeCalls: Array.from(new Set(window.__qwbCalls.map(function (c) { return c.action; }))),
        searchModes: window.__qwbCalls.filter(function (c) { return c.action === 'SEARCH_QDN_RESOURCES'; })
          .map(function (c) { return { service: c.service, identifier: c.identifier, prefix: c.prefix, mode: c.mode, exactMatchNames: c.exactMatchNames, names: c.names }; }).slice(0, 2),
        ownerBar: document.getElementById('qwb-owner-bar') !== null,
        barButtons: barButtons(),
        controls: document.querySelectorAll('[data-qwb-owner="controls"]').length,
        ownerBarMeta: (document.querySelector('.qwb-owner-meta') || {}).textContent || null,
        bodyClaims: (function () {
          var clone = document.body.cloneNode(true);
          Array.prototype.forEach.call(clone.querySelectorAll('script, pre'), function (n) { n.remove(); });
          return /published successfully|saved successfully/i.test(clone.textContent);
        })()
      };

      // Phase 2 - edit the first featured card through the real form.
      var edit = document.querySelector('[aria-label^="Edit highlights:"]');
      report.phases.edit = { editFound: edit !== null };
      if (edit) {
        edit.click();
        for (var i = 0; i < 40; i++) {
          if (document.querySelector('[data-qwb-form]')) break;
          await sleep(100);
        }
        var form = document.querySelector('[data-qwb-form]');
        var submit = document.querySelector('[data-qwb-form-submit]');
        var status = document.querySelector('[data-qwb-form-status]');
        var notice = document.querySelector('.qwb-notice');
        var titleInput = form ? form.elements.namedItem('title') : null;
        report.phases.edit.formOpen = form !== null;
        report.phases.edit.titleValue = titleInput ? titleInput.value : null;
        report.phases.edit.saveDisabled = submit ? submit.disabled : null;
        report.phases.edit.saveLabel = submit ? submit.textContent.trim() : null;
        report.phases.edit.notice = notice ? notice.textContent.trim().slice(0, 160) : null;
        report.phases.edit.verifyNote = (document.querySelector('.qwb-form-note') || {}).textContent || null;
        report.phases.edit.statusHidden = status ? status.hasAttribute('hidden') : null;
        report.phases.edit.blockEditor = document.querySelectorAll('textarea.qwb-input-blocks').length;

        if (titleInput) {
          titleInput.value = 'Harness published headline';
          titleInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
        if (submit) submit.click();
        for (var i = 0; i < 80; i++) {
          await sleep(250);
          var openForm = document.querySelector('[data-qwb-form]');
          if (!openForm) break;
          var statusEl = document.querySelector('[data-qwb-form-status]');
          if (statusEl && !statusEl.hasAttribute('hidden') && /Not retryable|not verified|Failed|Rejected|Outcome/.test(statusEl.textContent)) break;
        }
        var afterStatus = document.querySelector('[data-qwb-form-status]');
        report.phases.edit.afterSubmit = {
          modalOpen: document.querySelectorAll('.qwb-modal').length,
          formStatus: afterStatus && !afterStatus.hasAttribute('hidden') ? afterStatus.textContent.trim().slice(0, 200) : null,
          saveDisabled: submit ? submit.disabled : null,
          saveLabel: submit ? submit.textContent.trim() : null,
          toast: (document.querySelector('.qwb-toast') || {}).textContent ? document.querySelector('.qwb-toast').textContent.trim().slice(0, 200) : null,
          publishes: window.__qwbPublishes.slice()
        };
        // The write must have been re-read from the node and re-rendered.
        report.phases.edit.renderedAfterWrite = headlines();
        report.phases.edit.publishStatusEntry = (function () {
          var statusBtn = btn('Publishing status');
          if (!statusBtn) return null;
          statusBtn.click();
          var list = document.querySelector('.qwb-status-list');
          var text = list ? list.textContent.replace(/\\s+/g, ' ').trim().slice(0, 240) : null;
          var close = btn('Close') || document.querySelector('[data-qwb-modal-cancel]');
          if (close) close.click();
          return text;
        })();
      }
      // Phase 3 - edit the first article, whose kind lives in the DOCUMENT service.
      window.__qwbCalls.length = 0;
      window.__qwbPublishes.length = 0;
      window.location.hash = '#/posts';
      report.phases.post = { editFound: false };
      for (var i = 0; i < 60; i++) {
        if (document.querySelector('[aria-label^="Edit articles:"]')) break;
        await sleep(100);
      }
      var postEdit = document.querySelector('[aria-label^="Edit articles:"]');
      report.phases.post.editFound = postEdit !== null;
      report.phases.post.editLabel = postEdit ? postEdit.getAttribute('aria-label') : null;
      if (postEdit) {
        postEdit.click();
        for (var i = 0; i < 40; i++) {
          if (document.querySelector('[data-qwb-form]')) break;
          await sleep(100);
        }
        var pform = document.querySelector('[data-qwb-form]');
        var psubmit = document.querySelector('[data-qwb-form-submit]');
        var ptitle = pform ? pform.elements.namedItem('title') : null;
        report.phases.post.formOpen = pform !== null;
        report.phases.post.titleValue = ptitle ? ptitle.value : null;
        report.phases.post.blocksEditor = document.querySelectorAll('textarea.qwb-input-blocks').length;
        if (ptitle) {
          ptitle.value = 'Harness article headline';
          ptitle.dispatchEvent(new Event('input', { bubbles: true }));
        }
        if (psubmit) psubmit.click();
        for (var i = 0; i < 80; i++) {
          await sleep(250);
          var openForm2 = document.querySelector('[data-qwb-form]');
          if (!openForm2) break;
          var statusEl2 = document.querySelector('[data-qwb-form-status]');
          if (statusEl2 && !statusEl2.hasAttribute('hidden') && /Not retryable|not verified|Failed|Rejected|Outcome/.test(statusEl2.textContent)) break;
        }
        var after2 = document.querySelector('[data-qwb-form-status]');
        report.phases.post.afterSubmit = {
          modalOpen: document.querySelectorAll('.qwb-modal').length,
          formStatus: after2 && !after2.hasAttribute('hidden') ? after2.textContent.trim().slice(0, 220) : null,
          toast: (document.querySelector('.qwb-toast') || {}).textContent ? document.querySelector('.qwb-toast').textContent.trim().slice(0, 220) : null,
          publishes: window.__qwbPublishes.slice()
        };
        report.phases.post.bridgeCalls = window.__qwbCalls.map(function (c) {
          return { action: c.action, service: c.service, identifier: c.identifier };
        });
        var postsApp = document.getElementById('app');
        report.phases.post.renderedAfterWrite = postsApp ? postsApp.textContent.replace(/\s+/g, ' ').slice(0, 240) : null;
      }
    } catch (error) {
      report.errors.push(String(error && error.stack ? error.stack : error));
    }
    var pre = document.createElement('pre');
    pre.id = 'harness-report';
    pre.textContent = JSON.stringify(report, null, 1);
    document.body.appendChild(pre);
  }
  window.__qwbPhase3 = run;
})();
"""

owner = index.replace('    <script type="module"', '    <script>' + FAKE_NODE + '</script>\n    <script type="module"', 1)
owner = owner.replace('</body>', '    <script>' + REPORT + '</script>\n    <script>setTimeout(function () { window.__qwbPhase3(); }, 600);</script>\n  </body>')
(ROOT / 'owner.html').write_text(owner)

(ROOT / 'visitor.html').write_text(index)

VISITOR_REPORT = """    <script>
      window.__qwbVisitorReport = function () {
        var app = document.getElementById('app');
        var report = {
          ownerBar: document.getElementById('qwb-owner-bar') !== null,
          ownerControls: app ? app.querySelectorAll('[data-qwb-owner]').length : -1,
          ownerClasses: app ? app.querySelectorAll('.qwb-ctl, .qwb-owner-add-row').length : -1,
          modalHost: document.getElementById('qwb-modal-host') !== null,
          toastHost: document.getElementById('qwb-toast-host') !== null,
          appHtmlLength: app ? app.innerHTML.length : -1,
          appHtmlHash: 0
        };
        if (app) {
          var hash = 0;
          var html = app.innerHTML;
          for (var i = 0; i < html.length; i++) { hash = (hash * 31 + html.charCodeAt(i)) | 0; }
          report.appHtmlHash = hash;
        }
        var pre = document.createElement('pre');
        pre.id = 'visitor-report';
        pre.textContent = JSON.stringify(report, null, 1);
        document.body.appendChild(pre);
      };
    </script>
    <script>setTimeout(function () { window.__qwbVisitorReport(); }, 900);</script>
"""
(ROOT / 'visitor-report.html').write_text(index.replace('</body>', VISITOR_REPORT + '  </body>'))
print('harness written:', sorted(p.name for p in ROOT.iterdir() if p.is_file()))
