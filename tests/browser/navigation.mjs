// Browser check of the navigation's section toggles (used by tests/test_browser.py).
// Drives headless Chrome over the DevTools Protocol and prints one JSON object with what assistive
// technologies and keyboard users get. Usage: node navigation.mjs <page-url> <chrome> <profile-dir>
import { spawn } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";

const [url, chromeBin, profile] = process.argv.slice(2);
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
async function open() { const l = once("Page.loadEventFired"); await send("Page.navigate", { url }); await l; await sleep(300); }
async function press(key, code, keyCode, text) {
  await send("Input.dispatchKeyEvent", { type: "keyDown", key, code, windowsVirtualKeyCode: keyCode, text });
  await send("Input.dispatchKeyEvent", { type: "keyUp", key, code, windowsVirtualKeyCode: keyCode });
  await sleep(200);
}
const TOGGLE = `document.querySelector('label.md-nav__link[for^="__nav_"]')`;
async function ax() {
  // Accessibility tree as assistive technologies see it: the toggle and the list it controls.
  const { nodes } = (await send("Accessibility.getFullAXTree")).result;
  const doc = (await send("DOM.getDocument", { depth: 0 })).result.root.nodeId;
  const toggleId = (await send("DOM.querySelector", { nodeId: doc, selector: 'label.md-nav__link[for^="__nav_"]' })).result.nodeId;
  const listSel = await evaluate(`(() => { const l = ${TOGGLE}; const c = l.getAttribute('aria-controls'); return c ? '#' + c : 'nav[aria-labelledby="' + l.id + '"]'; })()`);
  const listId = (await send("DOM.querySelector", { nodeId: doc, selector: listSel })).result.nodeId;
  const backend = async (nodeId) => (await send("DOM.describeNode", { nodeId })).result.node.backendNodeId;
  const [tb, lb] = [await backend(toggleId), await backend(listId)];
  const find = (b) => nodes.find((n) => n.backendDOMNodeId === b) || {};
  const t = find(tb), l = find(lb);
  const prop = (n, name) => (n.properties || []).find((p) => p.name === name)?.value.value;
  const bool = (v) => (v === undefined ? null : v === true || v === "true");
  return { role: t.role?.value, name: t.name?.value || "", expanded: bool(prop(t, "expanded")), focusable: bool(prop(t, "focusable")),
           listRole: l.role?.value, listName: l.name?.value || "" };
}
const state = () => evaluate(`(() => { const l = ${TOGGLE}; return { checked: document.getElementById(l.htmlFor).checked, ariaExpandedAttribute: l.getAttribute('aria-expanded'), focused: document.activeElement === l, scrollY: window.scrollY }; })()`);

await send("Page.enable"); await send("Runtime.enable"); await send("Accessibility.enable"); await send("DOM.enable");
const result = {};
for (const view of [{ name: "desktop", width: 1280, height: 900, mobile: false }, { name: "phone", width: 390, height: 844, mobile: true }]) {
  await send("Emulation.setDeviceMetricsOverride", { width: view.width, height: view.height, deviceScaleFactor: 1, mobile: view.mobile });
  await open();
  const r = { initial: { ...(await ax()), ...(await state()) } };
  await evaluate(`${TOGGLE}.focus(), true`);
  await press(" ", "Space", 32, " ");
  r.afterSpace = { ...(await ax()), ...(await state()) };
  await press(" ", "Space", 32, " ");
  r.afterSecondSpace = { ...(await ax()), ...(await state()) };
  await press("Enter", "Enter", 13, "\r");
  r.afterEnter = { ...(await ax()), ...(await state()) };
  result[view.name] = r;
}
console.log(JSON.stringify(result));
ws.close(); chrome.kill(); process.exit(0);
