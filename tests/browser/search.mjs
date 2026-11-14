// Browser check of the site search (Zensical's search dialog), used by tests/test_browser.py.
// For each query: open the page, open search from the keyboard (Enter on the "Search" button),
// type the query, read the results, then press Enter and record where the browser went.
// Usage: node search.mjs <base-url> <chrome> <profile-dir> '<json [{"page": "/", "query": "..."}]>'
// Prints one JSON object: {desktop: [...], phone: [...]}.
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";

const [base, chromeBin, profile, spec] = process.argv.slice(2);
const queries = JSON.parse(spec);
const port = 9200 + Math.floor(Math.random() * 700);
const chrome = spawn(chromeBin, ["--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`, "about:blank"], { stdio: "ignore" });
async function json(path, method = "GET") {
  for (let i = 0; i < 100; i++) {
    try { return await (await fetch(`http://127.0.0.1:${port}${path}`, { method })).json(); } catch { await sleep(100); }
  }
  throw new Error("Chrome DevTools endpoint not reachable");
}
const target = await json("/json/new?about:blank", "PUT");
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let seq = 0; const pending = new Map(); const waiters = [];
ws.addEventListener("message", ({ data }) => {
  const msg = JSON.parse(data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  if (msg.method) waiters.filter((w) => w.method === msg.method).forEach((w) => w.resolve(msg));
});
const send = (method, params = {}) => new Promise((r) => { const id = ++seq; pending.set(id, r); ws.send(JSON.stringify({ id, method, params })); });
const once = (method) => new Promise((r) => { const w = { method, resolve: (m) => { waiters.splice(waiters.indexOf(w), 1); r(m); } }; waiters.push(w); });
const evaluate = async (e) => (await send("Runtime.evaluate", { expression: e, returnByValue: true, awaitPromise: true })).result.result.value;
async function open(path) {
  const l = once("Page.loadEventFired"); await send("Page.navigate", { url: base + path }); await l; await sleep(300);
}
async function press(key, code, keyCode, text) {
  await send("Input.dispatchKeyEvent", { type: "keyDown", key, code, windowsVirtualKeyCode: keyCode, text });
  await send("Input.dispatchKeyEvent", { type: "keyUp", key, code, windowsVirtualKeyCode: keyCode });
}
// The dialog lives in an open shadow root of an element appended to <body>.
const RESULTS = `(() => {
  const host = [...document.body.children].find(e => e.shadowRoot && e.shadowRoot.querySelector('dialog'));
  const root = host && host.shadowRoot;
  if (!root) return null;
  const input = root.querySelector('input[role=combobox]');
  const options = [...root.querySelectorAll('[role=listbox] [role=option]')];
  return { focused: root.activeElement === input, inputLabel: input && input.getAttribute('aria-label'),
           status: (root.querySelector('[role=status]') || {}).textContent || '',
           results: options.map(o => { const u = new URL(o.href); return u.pathname + u.hash; }),
           selected: options.findIndex(o => o.getAttribute('aria-selected') === 'true') };
})()`;

await send("Page.enable"); await send("Runtime.enable");
const out = {};
for (const view of [{ name: "desktop", width: 1280, height: 900, mobile: false }, { name: "phone", width: 390, height: 844, mobile: true }]) {
  await send("Emulation.setDeviceMetricsOverride", { width: view.width, height: view.height, deviceScaleFactor: 1, mobile: view.mobile });
  out[view.name] = [];
  for (const q of queries) {
    await open(q.page);
    // Keyboard only: focus the search button as Tab would, then Enter.
    const button = await evaluate(`(() => { const b = [...document.querySelectorAll('.md-search__button, label[for="__search"]')].find(e => e.getClientRects().length); if (!b) return null; b.focus(); return b.tagName + ':' + (b.getAttribute('aria-label') || b.textContent.trim()); })()`);
    await press("Enter", "Enter", 13, "\r");
    await sleep(400);
    await send("Input.insertText", { text: q.query });
    let state = null;
    for (let i = 0; i < 30; i++) {
      await sleep(150);
      state = await evaluate(RESULTS);
      if (state && /\d/.test(state.status)) break;
    }
    let opened = null;
    if (state && state.results.length) {
      const loaded = once("Page.loadEventFired");
      await press("Enter", "Enter", 13, "\r");
      await Promise.race([loaded, sleep(3000)]);
      await sleep(300);
      opened = await evaluate("location.pathname + location.hash");
    }
    out[view.name].push({ ...q, button, ...(state || { results: [] }), opened });
  }
}
console.log(JSON.stringify(out));
ws.close(); chrome.kill(); process.exit(0);
