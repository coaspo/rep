const api = globalThis.browser ?? chrome;

const CONFIG = {
  windowWidth: "80vw",
  windowHeight: "75vh",
  aiLinksPage: "τν-σύνδεσμοi.html",
  a: { file: "Συντάγματα.txt", keyPrefix: "param_a_item_" },
  b: { file: "Δοκιμές.txt", keyPrefix: "param_b_item_" },
  c: { file: "Στυλ.txt", keyPrefix: "param_c_item_" },
  d: { file: "Προχείρο.txt", keyPrefix: "param_d_item_" }
};

let targetField = null;
let popupEl = null;

const keyFor = (param, index) => `${param.keyPrefix}${index}`;
const isEditable = (el) =>
  Boolean(el && (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.isContentEditable));

function parseBlocks(rawText) {
  return rawText.replace(/\r\n/g, "\n").split("#--").map((b) => b.trim()).filter(Boolean);
}

async function fetchFileBlocks(fileName) {
  console.log("====", fileName)
  const res = await fetch(api.runtime.getURL(fileName));
  if (!res.ok) throw new Error(`Failed to load ${fileName}: ${res.status}`);
  return parseBlocks(await res.text());
}

function getStoredValues(keys) {
  return new Promise((resolve) => {
    api.storage.local.get(keys, (data) => resolve(api.runtime.lastError ? {} : (data ?? {})));
  });
}

async function loadParamPrompts(param) {
  const defaults = await fetchFileBlocks(param.file);
  const stored = await getStoredValues(defaults.map((_, i) => keyFor(param, i)));
  return { defaults, snippets: defaults.map((d, i) => stored[keyFor(param, i)] ?? d) };
}

const saveSnippet = (param, index, text) =>
  api.storage.local.set({ [keyFor(param, index)]: text });

const closePopup = () => {
  popupEl?.remove();
  popupEl = null;
};

function insertAtCursor(el, text) {
  if (!isEditable(el)) return;
  if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
    el.value = text + el.value;
    el.selectionStart = el.selectionEnd = el.value.length;
  } else {
    el.prepend(document.createTextNode(text));
  }
  el.focus();
  el.dispatchEvent(new Event("input", { bubbles: true }));
}

function makeButton(label, bgColor, onClick) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.textContent = label;
  Object.assign(btn.style, {
    whiteSpace: "nowrap", height: "30px", alignSelf: "center",
    fontSize: "1.2em", backgroundColor: bgColor, color: "#faf6ee", cursor: "pointer"
  });
  btn.addEventListener("click", onClick);
  return btn;
}

function makeHeader(fileName, box) {
  const bar = document.createElement("div");
  bar.textContent = fileName.replace(/\.[^.]+$/, "");
  Object.assign(bar.style, {
    gridColumn: "1 / -1", cursor: "move", userSelect: "none",
    padding: "4px 8px", backgroundColor: "#dfd5c0"
  });
  bar.addEventListener("mousedown", (e) => {
    if (e.button !== 0) return;
    const r = box.getBoundingClientRect();
    const dx = e.clientX - r.left, dy = e.clientY - r.top;
    box.style.transform = "none";
    box.style.left = `${r.left}px`;
    box.style.top = `${r.top}px`;
    const move = (ev) => {
      box.style.left = `${Math.max(0, Math.min(ev.clientX - dx, innerWidth - box.offsetWidth))}px`;
      box.style.top = `${Math.max(0, Math.min(ev.clientY - dy, innerHeight - box.offsetHeight))}px`;
    };
    const up = () => { removeEventListener("mousemove", move); removeEventListener("mouseup", up); };
    addEventListener("mousemove", move);
    addEventListener("mouseup", up);
  });
  return bar;
}

function buildRow(param, initialText, defaultText, index) {
  const textarea = document.createElement("textarea");
  textarea.value = initialText;
  Object.assign(textarea.style, {
    width: "100%", height: "100%", minHeight: "64px", boxSizing: "border-box", resize: "none"
  });
  textarea.addEventListener("input", () => saveSnippet(param, index, textarea.value));

  const insertBtn = makeButton("Εισαγωγή", "#3f6251", () => {
    saveSnippet(param, index, textarea.value);
    insertAtCursor(targetField, `${textarea.value}\n`);
    closePopup();
  });

  const resetBtn = makeButton("Επαναφορά", "#b86b4b", () => {
    textarea.value = defaultText;
    saveSnippet(param, index, textarea.value);
  });

  return [textarea, insertBtn, resetBtn];
}

async function openPopupForParam(paramId) {
  const param = CONFIG[paramId];
  if (!param) return;

  try {
    const { defaults, snippets } = await loadParamPrompts(param);
    closePopup();

    const rows = Math.max(1, snippets.length);
    const box = document.createElement("div");
    Object.assign(box.style, {
      position: "fixed", top: "50%", left: "50%", transform: "translate(-50%, -50%)",
      zIndex: "2147483647", width: CONFIG.windowWidth, height: CONFIG.windowHeight,
      maxWidth: "95vw", maxHeight: "95vh", overflowY: "auto", boxSizing: "border-box",
      border: "2px solid #1e241f", backgroundColor: "#efe8d8", padding: "8px",
      display: "grid", gridTemplateColumns: "minmax(0, 1fr) auto auto",
      gridTemplateRows: `auto repeat(${rows}, minmax(64px, 1fr)) auto`, gap: "8px"
    });

    box.append(makeHeader(param.file, box));
    for (let i = 0; i < snippets.length; i++) {
      box.append(...buildRow(param, snippets[i], defaults[i] ?? "", i));
    }

    const hint = Object.assign(document.createElement("span"), {
      textContent: "Alt-Shift-Q  W  E  R  /  Συντάγματα  Δοκιμές  Στυλ  Προχείρο"
    });
    hint.style.cssText = "grid-column: 1; align-self: center; color: #2b4c3f; white-space: pre;";

    const link = Object.assign(document.createElement("button"), {
      type: "button", textContent: "σύνδεσμοi TN"
    });
    link.style.cssText = "grid-column: 3; justify-self: end; align-self: center; background: none; border: none; color: #2b4c3f; text-decoration: underline; cursor: pointer;";
    link.addEventListener("click", async () => {
      const win = window.open("", "_blank");
      if (!win) return;
      const html = await (await fetch(api.runtime.getURL(CONFIG.aiLinksPage))).text();
      win.document.open();
      win.document.write(html);
      win.document.close();
    });

    box.append(hint, link);

    document.body.append(box);
    popupEl = box;
  } catch (err) {
    console.error("Failed to open snippet popup:", err);
  }
}

function matchedParamId(e) {
  if (!e.shiftKey || !e.altKey || e.ctrlKey || e.metaKey) return null;
  console.log("====", e.key)
  if (e.key === 'Q') return "a";
  if (e.key === 'W') return "b";
  if (e.key === 'E') return "c";
  if (e.key === 'R') return "d";
  return null;
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && popupEl) return closePopup();
  const paramId = matchedParamId(event);
  if (!paramId) return;
  event.preventDefault();
  if (isEditable(document.activeElement) && !popupEl?.contains(document.activeElement)) {
    targetField = document.activeElement;
  }
  openPopupForParam(paramId);
});
