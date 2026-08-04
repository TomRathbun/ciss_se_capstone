/**
 * CISS dual-pane Markdown editor with live Mermaid, PlantUML, and KaTeX preview.
 * Inspired by the artifact registry (@uiw/react-md-editor + diagram code blocks).
 */
(function () {
  const ta = document.getElementById("md-source");
  const preview = document.getElementById("md-preview");
  const statusEl = document.getElementById("md-status");
  const fileInput = document.getElementById("md-image-file");
  if (!ta || !preview || typeof marked === "undefined") return;

  if (typeof mermaid !== "undefined") {
    mermaid.initialize({
      startOnLoad: false,
      theme: "dark",
      securityLevel: "loose",
      fontFamily: "Inter, system-ui, sans-serif",
    });
  }

  marked.setOptions({ gfm: true, breaks: false });

  let timer = null;
  let mermaidId = 0;
  const PLANTUML_SERVER = "https://www.plantuml.com/plantuml/svg/";

  function setStatus(msg, ok) {
    if (!statusEl) return;
    statusEl.textContent = msg;
    statusEl.className =
      "text-xs " +
      (ok === false ? "text-red-400" : ok === true ? "text-green-400" : "text-gray-500");
  }

  function unescapeHtml(code) {
    return code
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&amp;/g, "&")
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'");
  }

  function plantumlUrl(code) {
    if (typeof plantumlEncoder === "undefined") return null;
    let text = code.trim();
    if (!text.startsWith("@start")) {
      text = "@startuml\n" + text + "\n@enduml";
    }
    try {
      return PLANTUML_SERVER + plantumlEncoder.encode(text);
    } catch (e) {
      return null;
    }
  }

  async function renderPreview() {
    const src = ta.value || "";
    let html = marked.parse(src);

    // Mermaid fences → pre.mermaid
    html = html.replace(
      /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/gi,
      function (_, code) {
        return '<pre class="mermaid">' + unescapeHtml(code) + "</pre>";
      }
    );

    // PlantUML fences → img via plantuml.com
    html = html.replace(
      /<pre><code class="language-plantuml">([\s\S]*?)<\/code><\/pre>/gi,
      function (_, code) {
        const raw = unescapeHtml(code);
        const url = plantumlUrl(raw);
        if (!url) {
          return (
            '<pre class="plantuml-source text-xs text-amber-200">' +
            raw.replace(/</g, "&lt;") +
            "</pre>"
          );
        }
        return (
          '<div class="plantuml-render my-4">' +
          '<img src="' +
          url +
          '" alt="PlantUML diagram" class="max-w-full mx-auto bg-white rounded-lg p-2" loading="lazy" />' +
          "</div>"
        );
      }
    );

    // Math / latex / katex fences → display math
    html = html.replace(
      /<pre><code class="language-(?:math|latex|katex)">([\s\S]*?)<\/code><\/pre>/gi,
      function (_, code) {
        const raw = unescapeHtml(code).trim();
        return '<div class="math-display">\\[' + raw + "\\]</div>";
      }
    );

    preview.innerHTML = html;

    // Mermaid client render
    if (typeof mermaid !== "undefined") {
      const nodes = preview.querySelectorAll("pre.mermaid");
      for (const node of nodes) {
        const chart = node.textContent || "";
        const id = "mmd-" + Date.now() + "-" + mermaidId++;
        try {
          const { svg } = await mermaid.render(id, chart);
          const wrap = document.createElement("div");
          wrap.className = "mermaid-render my-4 overflow-x-auto";
          wrap.innerHTML = svg;
          node.replaceWith(wrap);
        } catch (err) {
          const errBox = document.createElement("div");
          errBox.className =
            "my-3 p-3 rounded-lg border border-red-500/30 bg-red-500/10 text-red-300 text-xs font-mono whitespace-pre-wrap";
          errBox.textContent = "Mermaid error: " + (err.message || String(err));
          node.replaceWith(errBox);
        }
      }
    }

    // KaTeX auto-render for $...$ $$...$$ and math-display
    if (typeof renderMathInElement === "function") {
      try {
        renderMathInElement(preview, {
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
    }
  }

  function schedulePreview() {
    setStatus("Preview updating…");
    clearTimeout(timer);
    timer = setTimeout(async () => {
      try {
        await renderPreview();
        setStatus("Preview up to date", true);
      } catch (e) {
        setStatus("Preview error", false);
      }
    }, 280);
  }

  function insertAround(before, after, placeholder) {
    const start = ta.selectionStart;
    const end = ta.selectionEnd;
    const selected = ta.value.slice(start, end) || placeholder || "";
    const next = ta.value.slice(0, start) + before + selected + after + ta.value.slice(end);
    ta.value = next;
    const cursor = start + before.length + selected.length;
    ta.focus();
    ta.setSelectionRange(start + before.length, cursor);
    schedulePreview();
  }

  function insertBlock(block) {
    const start = ta.selectionStart;
    const prefix = start > 0 && ta.value[start - 1] !== "\n" ? "\n\n" : "\n";
    const text = prefix + block + "\n";
    ta.value = ta.value.slice(0, start) + text + ta.value.slice(ta.selectionEnd);
    ta.focus();
    schedulePreview();
  }

  async function uploadImage(file) {
    if (!file) return;
    setStatus("Uploading image…");
    const fd = new FormData();
    fd.append("file", file);
    try {
      const res = await fetch("/instructor/upload-image", {
        method: "POST",
        body: fd,
        credentials: "same-origin",
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus(data.error || "Upload failed", false);
        return;
      }
      insertBlock(data.markdown);
      setStatus("Image uploaded", true);
    } catch (e) {
      setStatus("Upload error", false);
    }
  }

  const actions = {
    bold: () => insertAround("**", "**", "bold"),
    italic: () => insertAround("*", "*", "italic"),
    h2: () => insertAround("\n## ", "\n", "Heading"),
    h3: () => insertAround("\n### ", "\n", "Heading"),
    ul: () => insertAround("\n- ", "\n", "list item"),
    ol: () => insertAround("\n1. ", "\n", "list item"),
    quote: () => insertAround("\n> ", "\n", "quote"),
    code: () => insertAround("`", "`", "code"),
    table: () => insertBlock("| Col A | Col B |\n| --- | --- |\n| cell | cell |"),
    link: () => insertAround("[", "](https://)", "link text"),
    image: () => {
      if (fileInput) fileInput.click();
      else insertBlock("![alt text](/static/uploads/content/your-image.png)");
    },
    mermaidFlow: () =>
      insertBlock(
        "```mermaid\nflowchart TD\n    A[Start] --> B{Decision}\n    B -->|Yes| C[OK]\n    B -->|No| D[Retry]\n    D --> B\n```"
      ),
    mermaidSeq: () =>
      insertBlock(
        "```mermaid\nsequenceDiagram\n    actor User\n    participant System\n    User->>System: Request\n    System-->>User: Response\n```"
      ),
    mermaidState: () =>
      insertBlock(
        "```mermaid\nstateDiagram-v2\n    [*] --> Idle\n    Idle --> Active: start\n    Active --> Idle: stop\n```"
      ),
    plantuml: () =>
      insertBlock(
        "```plantuml\n@startuml\nactor Operator\nparticipant AOC\nparticipant VCS\n\nOperator -> AOC: Report track\nAOC -> VCS: Voice tasking\nVCS --> Operator: Acknowledge\n@enduml\n```"
      ),
    katexInline: () => insertAround("$", "$", "E=mc^2"),
    katexBlock: () =>
      insertBlock("```math\n\\sum_{i=1}^{n} x_i = \\frac{n(n+1)}{2}\n```"),
    ears: () =>
      insertBlock(
        "WHEN <trigger>, the <system> shall <response>.\n\n" +
          "WHILE <state>, the <system> shall <response>.\n\n" +
          "IF <unwanted condition> THEN the <system> shall <response>."
      ),
    need: () =>
      insertBlock("As <stakeholder>,\nwe need <the need>,\nso that <benefit>."),
  };

  document.querySelectorAll("[data-md-action]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const act = btn.getAttribute("data-md-action");
      if (actions[act]) actions[act]();
    });
  });

  if (fileInput) {
    fileInput.addEventListener("change", () => {
      const f = fileInput.files && fileInput.files[0];
      uploadImage(f);
      fileInput.value = "";
    });
  }

  // Paste image from clipboard
  ta.addEventListener("paste", (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (const item of items) {
      if (item.type && item.type.startsWith("image/")) {
        e.preventDefault();
        const blob = item.getAsFile();
        if (blob) uploadImage(blob);
        break;
      }
    }
  });

  ta.addEventListener("input", schedulePreview);
  ta.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "s") {
      e.preventDefault();
      const form = ta.closest("form");
      if (form) form.requestSubmit();
    }
  });

  schedulePreview();
})();
