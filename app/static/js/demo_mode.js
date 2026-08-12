/**
 * Demo mode for module pages:
 *  - Selecting text auto-copies to the clipboard (live demo / terminal paste).
 *  - Code blocks get a copy control for the whole fence.
 *  - Floating toolbar to exit demo or return to teach mode.
 */
(function () {
  let active = false;
  let article = null;
  let enterBtn = null;
  let toastEl = null;
  let toolbar = null;
  let lastCopied = "";
  let copyTimer = null;

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function buildToolbar() {
    const bar = document.createElement("div");
    bar.className = "demo-toolbar";
    bar.setAttribute("role", "toolbar");
    bar.setAttribute("aria-label", "Demo mode controls");
    bar.innerHTML = [
      '<span class="demo-toolbar-label">Demo</span>',
      '<button type="button" data-action="teach" title="Return to teach mode at this section (T)">Teach</button>',
      '<button type="button" data-action="exit" title="Exit demo mode (Esc)">Exit demo</button>',
      '<span class="teach-hint">Select to copy · T teach · Esc exit</span>',
    ].join("");

    bar.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-action]");
      if (!btn || !active) return;
      const action = btn.getAttribute("data-action");
      if (action === "exit") exitDemoMode();
      else if (action === "teach") switchToTeach();
    });

    document.body.appendChild(bar);
    return bar;
  }

  function switchToTeach() {
    if (!active) return;
    exitDemoMode();
    // Teach mode listens and opens at the section currently in view.
    document.dispatchEvent(new CustomEvent("ciss:enter-teach"));
  }

  function ensureToast() {
    if (toastEl) return toastEl;
    toastEl = document.createElement("div");
    toastEl.className = "demo-toast";
    toastEl.setAttribute("role", "status");
    toastEl.setAttribute("aria-live", "polite");
    document.body.appendChild(toastEl);
    return toastEl;
  }

  function showToast(msg) {
    const el = ensureToast();
    el.textContent = msg;
    el.classList.add("is-visible");
    clearTimeout(copyTimer);
    copyTimer = setTimeout(() => {
      el.classList.remove("is-visible");
    }, 1400);
  }

  async function writeClipboard(text) {
    if (!text) return false;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        return true;
      }
    } catch (_) {
      /* fall through */
    }
    try {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand("copy");
      ta.remove();
      return ok;
    } catch (_) {
      return false;
    }
  }

  function selectionInArticle(sel) {
    if (!sel || sel.isCollapsed || !article) return false;
    const node = sel.anchorNode;
    if (!node) return false;
    const el = node.nodeType === 1 ? node : node.parentElement;
    return !!(el && article.contains(el));
  }

  async function copySelection() {
    if (!active) return;
    const sel = window.getSelection();
    if (!selectionInArticle(sel)) return;
    const text = sel.toString();
    // Ignore empty / whitespace-only drags
    if (!text || !text.trim()) return;
    // Avoid re-copying the exact same string repeatedly while mouse is held
    if (text === lastCopied) return;
    const ok = await writeClipboard(text);
    if (ok) {
      lastCopied = text;
      const preview =
        text.trim().length > 48 ? text.trim().slice(0, 48) + "…" : text.trim();
      showToast("Copied: " + preview);
    } else {
      showToast("Copy failed — allow clipboard access");
    }
  }

  function onMouseUp() {
    if (!active) return;
    // Defer so the selection is finalized
    setTimeout(copySelection, 0);
  }

  function onKeyUp(e) {
    if (!active) return;
    // Shift+arrows / keyboard selection
    if (e.key === "Shift" || e.key.startsWith("Arrow")) {
      setTimeout(copySelection, 0);
    }
  }

  function onKeydown(e) {
    if (!active) return;
    const tag = (e.target && e.target.tagName) || "";
    if (tag === "INPUT" || tag === "TEXTAREA" || e.target.isContentEditable) return;
    if (e.key === "Escape") {
      e.preventDefault();
      exitDemoMode();
      return;
    }
    if (e.key === "t" || e.key === "T") {
      e.preventDefault();
      switchToTeach();
    }
  }

  /** Wrap fenced code blocks with a copy button (skip mermaid sources). */
  function enhanceCodeBlocks(root) {
    if (!root) return;
    const pres = root.querySelectorAll("pre");
    pres.forEach((pre) => {
      if (pre.classList.contains("mermaid")) return;
      if (pre.closest(".code-block-wrap")) return;
      // Skip empty
      if (!(pre.textContent || "").trim()) return;

      const wrap = document.createElement("div");
      wrap.className = "code-block-wrap";
      pre.parentNode.insertBefore(wrap, pre);
      wrap.appendChild(pre);

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "code-copy-btn";
      btn.title = "Copy code block";
      btn.setAttribute("aria-label", "Copy code block");
      btn.innerHTML =
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span>';

      btn.addEventListener("click", async (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        const code = pre.querySelector("code");
        const text = (code || pre).innerText.replace(/\n$/, "");
        const ok = await writeClipboard(text);
        const label = btn.querySelector("span");
        if (ok) {
          if (label) label.textContent = "Copied";
          btn.classList.add("is-copied");
          showToast("Code block copied");
          setTimeout(() => {
            if (label) label.textContent = "Copy";
            btn.classList.remove("is-copied");
          }, 1500);
        } else {
          if (label) label.textContent = "Failed";
          showToast("Copy failed — allow clipboard access");
          setTimeout(() => {
            if (label) label.textContent = "Copy";
          }, 1500);
        }
      });

      wrap.appendChild(btn);
    });
  }

  function enterDemoMode() {
    if (active || !article) return;

    // If teach mode is up, ask it to exit (keeps scroll) then re-enter demo.
    if (document.body.classList.contains("teach-mode-active")) {
      document.dispatchEvent(new CustomEvent("ciss:request-demo-from-teach"));
      return;
    }

    active = true;
    lastCopied = "";
    document.body.classList.add("demo-mode-active");
    article.classList.add("demo-root");

    if (enterBtn) {
      enterBtn.setAttribute("aria-pressed", "true");
      enterBtn.textContent = "Demo on";
      enterBtn.classList.add("is-demo-on");
    }

    showToast("Demo mode — select text to copy");
  }

  function exitDemoMode() {
    if (!active) return;
    active = false;
    lastCopied = "";
    document.body.classList.remove("demo-mode-active");
    if (article) article.classList.remove("demo-root");

    if (enterBtn) {
      enterBtn.setAttribute("aria-pressed", "false");
      enterBtn.textContent = "Demo mode";
      enterBtn.classList.remove("is-demo-on");
    }

    if (toastEl) toastEl.classList.remove("is-visible");
  }

  function init() {
    article = qs("#module-article");
    enterBtn = qs("#demo-mode-enter");
    if (!article) return;

    // Code copy buttons are always useful on module pages
    enhanceCodeBlocks(article);

    toolbar = buildToolbar();

    if (enterBtn) {
      enterBtn.addEventListener("click", () => {
        if (active) exitDemoMode();
        else enterDemoMode();
      });
    }

    document.addEventListener("mouseup", onMouseUp);
    document.addEventListener("keyup", onKeyUp);
    document.addEventListener("keydown", onKeydown);

    document.addEventListener("ciss:enter-demo", () => enterDemoMode());
    document.addEventListener("ciss:exit-demo", () => exitDemoMode());
  }

  onReady(init);
})();
