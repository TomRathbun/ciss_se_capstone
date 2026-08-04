/**
 * Render Mermaid + KaTeX on public curriculum pages.
 * PlantUML is already emitted as <img> server-side.
 */
(function () {
  async function renderMermaid() {
    if (typeof mermaid === "undefined") return;
    mermaid.initialize({
      startOnLoad: false,
      theme: "dark",
      securityLevel: "loose",
      fontFamily: "Inter, system-ui, sans-serif",
    });
    const nodes = document.querySelectorAll("pre.mermaid");
    let i = 0;
    for (const node of nodes) {
      if (node.dataset.processed === "1") continue;
      const chart = node.textContent || "";
      const id = "view-mmd-" + Date.now() + "-" + i++;
      try {
        const { svg } = await mermaid.render(id, chart);
        const wrap = document.createElement("div");
        wrap.className =
          "mermaid-render my-6 overflow-x-auto rounded-xl border border-white/10 bg-surface-900/50 p-4";
        wrap.innerHTML = svg;
        node.replaceWith(wrap);
      } catch (err) {
        node.classList.add("text-red-300", "text-xs");
        node.setAttribute("title", err.message || String(err));
      }
    }
  }

  function renderKatex() {
    if (typeof renderMathInElement !== "function") return;
    const roots = document.querySelectorAll(".prose-course, .math-root");
    roots.forEach((el) => {
      try {
        renderMathInElement(el, {
          delimiters: [
            { left: "\\[", right: "\\]", display: true },
            { left: "$$", right: "$$", display: true },
            { left: "\\(", right: "\\)", display: false },
            { left: "$", right: "$", display: false },
          ],
          throwOnError: false,
        });
      } catch (e) {
        /* ignore */
      }
    });
  }

  async function run() {
    await renderMermaid();
    renderKatex();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
