/**
 * Module teaching mode: section highlight, next/prev, freehand pen overlay, zoom.
 * Activates only on pages with #module-article and #teach-mode-enter.
 */
(function () {
  const PEN_COLOR = "#fbbf24";
  const PEN_WIDTH = 3.5;
  const MIN_ZOOM = 0.7;
  const MAX_ZOOM = 2.5;
  const ZOOM_STEP = 0.1;
  const ZOOM_STORAGE_KEY = "ciss.teach.zoom";

  let active = false;
  let penOn = true;
  let sectionIndex = 0;
  let sections = [];
  let strokes = [];
  let currentStroke = null;
  let drawing = false;
  let zoom = 1;
  /** Last zoom the instructor chose; restored on every teach-mode enter. */
  let savedZoom = null;

  let article = null;
  let canvas = null;
  let ctx = null;
  let toolbar = null;
  let sectionLabel = null;
  let zoomLabel = null;
  let btnPrev = null;
  let btnNext = null;
  let btnPen = null;
  let btnZoomOut = null;
  let btnZoomIn = null;
  let enterBtn = null;

  let resizeObserver = null;
  let originalChildren = null;

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
    bar.className = "teach-toolbar";
    bar.setAttribute("role", "toolbar");
    bar.setAttribute("aria-label", "Teach mode controls");
    bar.innerHTML = [
      '<button type="button" data-action="exit" title="Exit (Esc) — stay on this section">Exit</button>',
      '<button type="button" data-action="demo" title="Leave teach mode and enter demo mode (auto-copy)">Demo</button>',
      '<button type="button" data-action="prev" title="Previous section (←)">← Prev</button>',
      '<span class="teach-section-label" data-role="section-label">1 / 1</span>',
      '<button type="button" data-action="next" title="Next section (→)">Next →</button>',
      '<button type="button" data-action="zoom-out" title="Zoom out (−)">−</button>',
      '<span class="teach-section-label" data-role="zoom-label">100%</span>',
      '<button type="button" data-action="zoom-in" title="Zoom in (+)">+</button>',
      '<button type="button" data-action="fit" title="Fit content to window width (F)">Fit</button>',
      '<button type="button" data-action="pen" title="Toggle pen" class="is-on">Pen</button>',
      '<button type="button" data-action="clear" title="Clear drawings (C)">Clear</button>',
      '<span class="teach-hint">← → · +/− · F fit · Esc stay put</span>',
    ].join("");

    bar.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-action]");
      if (!btn || !active) return;
      const action = btn.getAttribute("data-action");
      if (action === "exit") exitTeachMode();
      else if (action === "demo") exitTeachMode({ enterDemo: true });
      else if (action === "prev") goSection(-1);
      else if (action === "next") goSection(1);
      else if (action === "clear") clearStrokes();
      else if (action === "pen") setPenOn(!penOn);
      else if (action === "zoom-in") nudgeZoom(ZOOM_STEP);
      else if (action === "zoom-out") nudgeZoom(-ZOOM_STEP);
      else if (action === "fit") fitToWidth();
    });

    document.body.appendChild(bar);
    return bar;
  }

  function clampZoom(z) {
    return Math.round(Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, z)) * 100) / 100;
  }

  function loadSavedZoom() {
    try {
      const raw = localStorage.getItem(ZOOM_STORAGE_KEY);
      if (raw == null || raw === "") return null;
      const n = parseFloat(raw);
      if (!Number.isFinite(n)) return null;
      return clampZoom(n);
    } catch (_) {
      return null;
    }
  }

  function persistZoom(z) {
    savedZoom = clampZoom(z);
    try {
      localStorage.setItem(ZOOM_STORAGE_KEY, String(savedZoom));
    } catch (_) {
      /* private mode / quota — keep in-memory only */
    }
  }

  function updateZoomUi() {
    if (zoomLabel) zoomLabel.textContent = Math.round(zoom * 100) + "%";
    if (btnZoomOut) btnZoomOut.disabled = zoom <= MIN_ZOOM;
    if (btnZoomIn) btnZoomIn.disabled = zoom >= MAX_ZOOM;
  }

  function applyZoomStyle() {
    if (!article) return;
    // CSS zoom scales layout + hit-testing in Chromium/Edge (classroom browsers).
    article.style.zoom = String(zoom);
  }

  function setZoom(z, opts) {
    const options = opts || {};
    const next = clampZoom(z);
    if (next === zoom && article && article.style.zoom === String(next)) {
      updateZoomUi();
      if (!options.skipPersist) persistZoom(next);
      return;
    }
    zoom = next;
    applyZoomStyle();
    updateZoomUi();
    if (!options.skipPersist) persistZoom(next);
    // Strokes are in pre-zoom canvas space; clear so annotations stay honest.
    if (!options.keepStrokes) clearStrokes();
    requestAnimationFrame(() => {
      resizeCanvas(true);
      const target = sections[sectionIndex];
      if (target && !options.skipScroll) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  }

  function nudgeZoom(delta) {
    setZoom(zoom + delta);
  }

  function fitToWidth() {
    if (!article || !active) return;
    // Measure unzoomed width against the viewport, then scale to fill.
    const prev = zoom;
    article.style.zoom = "1";
    // Force layout read at zoom=1
    const sidePad = 24; // matches main horizontal padding * 2-ish
    const available = Math.max(320, window.innerWidth - sidePad);
    const natural = Math.max(1, article.getBoundingClientRect().width);
    const next = clampZoom(available / natural);
    // Force setZoom to re-apply even when the numeric zoom is unchanged
    zoom = prev === next ? next - 0.001 : prev;
    setZoom(next);
  }

  /** Apply remembered zoom, or Fit once on first use. */
  function applyPreferredZoom() {
    if (savedZoom != null) {
      zoom = 1; // force style re-apply
      setZoom(savedZoom, { skipScroll: false });
      return;
    }
    fitToWidth();
  }

  function partitionSections(root) {
    const kids = Array.from(root.children).filter(
      (el) => !el.classList.contains("teach-canvas")
    );
    if (!kids.length) return [];

    // Snapshot originals so we can restore on exit
    originalChildren = kids.slice();

    const groups = [];
    let bucket = [];

    function flush() {
      if (!bucket.length) return;
      groups.push(bucket);
      bucket = [];
    }

    for (const el of kids) {
      if (el.tagName === "H2" && bucket.length) {
        flush();
      }
      bucket.push(el);
    }
    flush();

    // If no H2s, one section is the whole article
    const wrappers = groups.map((nodes, i) => {
      const wrap = document.createElement("div");
      wrap.className = "teach-section";
      wrap.dataset.teachIndex = String(i);
      for (const n of nodes) wrap.appendChild(n);
      return wrap;
    });

    // Remove leftover non-canvas nodes, keep canvas if any
    for (const el of Array.from(root.children)) {
      if (!el.classList.contains("teach-canvas")) el.remove();
    }
    for (const w of wrappers) root.appendChild(w);
    return wrappers;
  }

  function restoreArticle() {
    if (!article || !originalChildren) return;
    // Remove section wrappers and canvas
    Array.from(article.children).forEach((el) => el.remove());
    for (const el of originalChildren) article.appendChild(el);
    originalChildren = null;
    sections = [];
  }

  function ensureCanvas() {
    if (canvas && canvas.parentNode === article) return;
    canvas = document.createElement("canvas");
    canvas.className = "teach-canvas";
    canvas.setAttribute("aria-hidden", "true");
    article.appendChild(canvas);
    ctx = canvas.getContext("2d");
    bindCanvasEvents();
  }

  function contentSize() {
    // Full article content size (includes padding)
    return {
      w: Math.max(article.scrollWidth, article.clientWidth),
      h: Math.max(article.scrollHeight, article.clientHeight),
    };
  }

  function resizeCanvas(force) {
    if (!canvas || !article) return;
    const dpr = window.devicePixelRatio || 1;
    const { w, h } = contentSize();
    const cssW = Math.ceil(w);
    const cssH = Math.ceil(h);
    const nextW = Math.ceil(cssW * dpr);
    const nextH = Math.ceil(cssH * dpr);
    if (!force && canvas.width === nextW && canvas.height === nextH) {
      canvas.style.width = cssW + "px";
      canvas.style.height = cssH + "px";
      return;
    }
    canvas.width = nextW;
    canvas.height = nextH;
    canvas.style.width = cssW + "px";
    canvas.style.height = cssH + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    redrawStrokes();
  }

  function eventToCanvasPoint(e) {
    const rect = canvas.getBoundingClientRect();
    // clientWidth is layout (pre-zoom) size; rect is visual — maps screen → canvas.
    const scaleX = (canvas.clientWidth || rect.width) / (rect.width || 1);
    const scaleY = (canvas.clientHeight || rect.height) / (rect.height || 1);
    const clientX = e.clientX ?? (e.touches && e.touches[0] && e.touches[0].clientX);
    const clientY = e.clientY ?? (e.touches && e.touches[0] && e.touches[0].clientY);
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY,
    };
  }

  function redrawStrokes() {
    if (!ctx || !canvas) return;
    const dpr = window.devicePixelRatio || 1;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    for (const stroke of strokes) {
      drawStroke(stroke);
    }
    if (currentStroke) drawStroke(currentStroke);
  }

  function drawStroke(stroke) {
    if (!ctx || !stroke.points.length) return;
    ctx.save();
    ctx.strokeStyle = stroke.color;
    ctx.lineWidth = stroke.width;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.beginPath();
    const pts = stroke.points;
    ctx.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < pts.length; i++) {
      ctx.lineTo(pts[i].x, pts[i].y);
    }
    ctx.stroke();
    ctx.restore();
  }

  function clearStrokes() {
    strokes = [];
    currentStroke = null;
    drawing = false;
    redrawStrokes();
  }

  function setPenOn(on) {
    penOn = !!on;
    if (btnPen) btnPen.classList.toggle("is-on", penOn);
    if (canvas) canvas.classList.toggle("is-drawing", penOn && active);
  }

  function applySectionHighlight() {
    sections.forEach((sec, i) => {
      sec.classList.toggle("is-active", i === sectionIndex);
      sec.classList.toggle("is-dimmed", i !== sectionIndex);
    });
    if (sectionLabel) {
      sectionLabel.textContent =
        sections.length === 0
          ? "0 / 0"
          : sectionIndex + 1 + " / " + sections.length;
    }
    if (btnPrev) btnPrev.disabled = sectionIndex <= 0;
    if (btnNext) btnNext.disabled = sectionIndex >= sections.length - 1;
  }

  function goSection(delta) {
    if (!sections.length) return;
    const next = Math.min(
      sections.length - 1,
      Math.max(0, sectionIndex + delta)
    );
    if (next === sectionIndex) return;
    sectionIndex = next;
    clearStrokes();
    applySectionHighlight();
    const target = sections[sectionIndex];
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    // Canvas may need resize after layout settles
    requestAnimationFrame(() => {
      resizeCanvas();
    });
  }

  function bindCanvasEvents() {
    if (!canvas || canvas.dataset.bound === "1") return;
    canvas.dataset.bound = "1";

    const start = (e) => {
      if (!active || !penOn) return;
      e.preventDefault();
      drawing = true;
      const p = eventToCanvasPoint(e);
      currentStroke = { color: PEN_COLOR, width: PEN_WIDTH, points: [p] };
    };

    const move = (e) => {
      if (!drawing || !currentStroke) return;
      e.preventDefault();
      const p = eventToCanvasPoint(e);
      currentStroke.points.push(p);
      // incremental draw of last segment
      if (ctx && currentStroke.points.length >= 2) {
        const pts = currentStroke.points;
        const a = pts[pts.length - 2];
        const b = pts[pts.length - 1];
        ctx.save();
        ctx.strokeStyle = currentStroke.color;
        ctx.lineWidth = currentStroke.width;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
        ctx.restore();
      }
    };

    const end = (e) => {
      if (!drawing) return;
      if (e) e.preventDefault();
      drawing = false;
      if (currentStroke && currentStroke.points.length > 1) {
        strokes.push(currentStroke);
      }
      currentStroke = null;
    };

    canvas.addEventListener("mousedown", start);
    canvas.addEventListener("mousemove", move);
    window.addEventListener("mouseup", end);

    canvas.addEventListener("touchstart", start, { passive: false });
    canvas.addEventListener("touchmove", move, { passive: false });
    canvas.addEventListener("touchend", end, { passive: false });
    canvas.addEventListener("touchcancel", end, { passive: false });
  }

  function isTypingTarget(el) {
    if (!el) return false;
    const tag = el.tagName || "";
    return tag === "INPUT" || tag === "TEXTAREA" || el.isContentEditable;
  }

  function onKeydown(e) {
    if (isTypingTarget(e.target)) return;

    // Idle (not teach, not demo): enter modes from anywhere on the page
    if (!active && !document.body.classList.contains("demo-mode-active")) {
      if (e.key === "t" || e.key === "T") {
        e.preventDefault();
        enterTeachMode();
        return;
      }
      if (e.key === "d" || e.key === "D") {
        e.preventDefault();
        document.dispatchEvent(new CustomEvent("ciss:enter-demo"));
        return;
      }
      return;
    }

    if (!active) return;

    if (e.key === "Escape") {
      e.preventDefault();
      exitTeachMode();
      return;
    }
    if (e.key === "ArrowRight" || e.key === "PageDown" || (e.key === " " && !penOn)) {
      e.preventDefault();
      goSection(1);
      return;
    }
    if (e.key === "ArrowLeft" || e.key === "PageUp") {
      e.preventDefault();
      goSection(-1);
      return;
    }
    if (e.key === "c" || e.key === "C") {
      e.preventDefault();
      clearStrokes();
      return;
    }
    if (e.key === "p" || e.key === "P") {
      e.preventDefault();
      setPenOn(!penOn);
      return;
    }
    if (e.key === "+" || e.key === "=") {
      e.preventDefault();
      nudgeZoom(ZOOM_STEP);
      return;
    }
    if (e.key === "-" || e.key === "_") {
      e.preventDefault();
      nudgeZoom(-ZOOM_STEP);
      return;
    }
    if (e.key === "f" || e.key === "F") {
      e.preventDefault();
      fitToWidth();
    }
  }

  /** Always-visible controls when not in teach/demo (scroll-independent). */
  function buildModeDock() {
    const dock = document.createElement("div");
    dock.className = "module-mode-dock";
    dock.setAttribute("role", "toolbar");
    dock.setAttribute("aria-label", "Presentation modes");
    dock.innerHTML = [
      '<button type="button" data-action="teach" title="Teach mode (T) — starts at the section in view">Teach</button>',
      '<button type="button" data-action="demo" title="Demo mode (D) — select text to copy">Demo</button>',
      '<span class="teach-hint">T teach · D demo</span>',
    ].join("");

    dock.addEventListener("click", (e) => {
      const btn = e.target.closest("button[data-action]");
      if (!btn) return;
      if (document.body.classList.contains("teach-mode-active")) return;
      if (document.body.classList.contains("demo-mode-active")) return;
      const action = btn.getAttribute("data-action");
      if (action === "teach") enterTeachMode();
      else if (action === "demo") {
        document.dispatchEvent(new CustomEvent("ciss:enter-demo"));
      }
    });

    document.body.appendChild(dock);
    return dock;
  }

  async function requestFs() {
    try {
      if (document.fullscreenElement) return;
      const el = document.documentElement;
      if (el.requestFullscreen) await el.requestFullscreen();
    } catch (_) {
      /* browser may block; CSS shell still works */
    }
  }

  async function exitFs() {
    try {
      if (document.fullscreenElement && document.exitFullscreen) {
        await document.exitFullscreen();
      }
    } catch (_) {
      /* ignore */
    }
  }

  function onFullscreenChange() {
    // If user exits browser fullscreen with Esc, keep teach mode unless Esc also handled.
    // Esc is handled by keydown first for teach exit; fullscreen exit alone is fine.
  }

  /** Pick the section nearest the current viewport (for re-entering from demo). */
  function sectionIndexNearViewport() {
    if (!sections.length) return 0;
    const mark = window.innerHeight * 0.28;
    let idx = 0;
    sections.forEach((sec, i) => {
      const top = sec.getBoundingClientRect().top;
      if (top <= mark) idx = i;
    });
    return idx;
  }

  async function enterTeachMode() {
    if (active || !article) return;

    // Demo mode conflicts with pen overlay / section shell
    document.dispatchEvent(new CustomEvent("ciss:exit-demo"));

    sections = partitionSections(article);
    if (!sections.length) {
      return;
    }

    active = true;
    sectionIndex = sectionIndexNearViewport();
    zoom = savedZoom != null ? savedZoom : 1;
    document.body.classList.add("teach-mode-active");
    article.classList.add("teach-root");
    applyZoomStyle();
    updateZoomUi();

    ensureCanvas();
    setPenOn(true);
    clearStrokes();
    applySectionHighlight();

    if (resizeObserver) resizeObserver.disconnect();
    resizeObserver = new ResizeObserver(() => resizeCanvas());
    resizeObserver.observe(article);
    window.addEventListener("resize", onWindowResize);

    if (enterBtn) {
      enterBtn.setAttribute("aria-pressed", "true");
      enterBtn.textContent = "Teaching…";
    }

    await requestFs();

    requestAnimationFrame(() => {
      applyPreferredZoom();
      // Re-resolve after zoom/layout so we stay on the viewed section
      sectionIndex = sectionIndexNearViewport();
      applySectionHighlight();
      const target = sections[sectionIndex];
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  function onWindowResize() {
    if (!active) return;
    resizeCanvas(true);
  }

  /**
   * Exit teach mode but keep the reader on the current section.
   * @param {{ enterDemo?: boolean }} [opts]
   */
  async function exitTeachMode(opts) {
    if (!active) return;
    const options = opts || {};

    // Anchor is an original content node (survives restoreArticle).
    const activeSec = sections[sectionIndex];
    const anchorEl =
      (activeSec &&
        (activeSec.querySelector("h2, h3, h1") || activeSec.firstElementChild)) ||
      null;
    const anchorOffset = anchorEl
      ? anchorEl.getBoundingClientRect().top
      : null;

    // Remember zoom before teardown so the next enter restores it
    if (Number.isFinite(zoom)) persistZoom(zoom);

    active = false;
    drawing = false;
    currentStroke = null;
    strokes = [];
    zoom = 1;

    document.body.classList.remove("teach-mode-active");
    setPenOn(false);

    if (canvas) {
      canvas.remove();
      canvas = null;
      ctx = null;
    }

    if (resizeObserver) {
      resizeObserver.disconnect();
      resizeObserver = null;
    }
    window.removeEventListener("resize", onWindowResize);

    restoreArticle();
    article.classList.remove("teach-root");
    article.style.zoom = "";

    if (enterBtn) {
      enterBtn.setAttribute("aria-pressed", "false");
      enterBtn.textContent = "Teach mode";
    }

    await exitFs();

    // Restore viewport so Exit/Esc does not jump to the top of the module.
    const restoreScroll = () => {
      if (!anchorEl || !document.contains(anchorEl)) return;
      if (anchorOffset == null) {
        anchorEl.scrollIntoView({ block: "start", behavior: "instant" });
        return;
      }
      const now = anchorEl.getBoundingClientRect().top;
      window.scrollBy({ top: now - anchorOffset, left: 0, behavior: "instant" });
    };
    restoreScroll();
    requestAnimationFrame(restoreScroll);

    if (options.enterDemo) {
      document.dispatchEvent(new CustomEvent("ciss:enter-demo"));
    }
  }

  function init() {
    article = qs("#module-article");
    enterBtn = qs("#teach-mode-enter");
    if (!article) return;

    savedZoom = loadSavedZoom();

    toolbar = buildToolbar();
    buildModeDock();
    sectionLabel = qs("[data-role='section-label']", toolbar);
    zoomLabel = qs("[data-role='zoom-label']", toolbar);
    btnPrev = qs('[data-action="prev"]', toolbar);
    btnNext = qs('[data-action="next"]', toolbar);
    btnPen = qs('[data-action="pen"]', toolbar);
    btnZoomOut = qs('[data-action="zoom-out"]', toolbar);
    btnZoomIn = qs('[data-action="zoom-in"]', toolbar);

    if (enterBtn) {
      enterBtn.addEventListener("click", () => {
        if (active) exitTeachMode();
        else enterTeachMode();
      });
    }

    document.addEventListener("keydown", onKeydown);
    document.addEventListener("fullscreenchange", onFullscreenChange);

    // Demo mode may ask teach mode to stop and hand off (without jumping).
    document.addEventListener("ciss:exit-teach", () => {
      if (active) exitTeachMode();
    });
    document.addEventListener("ciss:request-demo-from-teach", () => {
      if (active) exitTeachMode({ enterDemo: true });
      else document.dispatchEvent(new CustomEvent("ciss:enter-demo"));
    });
    // Demo toolbar "Teach" / header / dock / shortcut
    document.addEventListener("ciss:enter-teach", () => {
      if (!active) enterTeachMode();
    });
  }

  onReady(init);
})();
