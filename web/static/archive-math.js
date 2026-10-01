/* Local KaTeX 0.16.22. Keep every original formula accessible as source. */
(function () {
  "use strict";
  function render() {
    if (!window.katex) return;
    document.querySelectorAll("pre.math-source").forEach(function (source) {
      var tex = source.textContent.trim();
      if (!tex || tex.includes("尚未")) return;
      if ((tex.startsWith("$$") && tex.endsWith("$$")) ||
          (tex.startsWith("\\[") && tex.endsWith("\\]"))) tex = tex.slice(2, -2);
      var display = document.createElement("div");
      display.className = "math-rendered";
      try {
        window.katex.render(tex, display, {displayMode: true, throwOnError: true, trust: false, strict: "warn"});
        var details = document.createElement("details");
        var summary = document.createElement("summary");
        summary.className = "math-fallback";
        summary.textContent = "查看原始 LaTeX";
        source.before(display, details);
        details.append(summary, source);
      } catch (_) {
        // Unsupported commands and extraction errors stay visible as source.
        source.setAttribute("aria-label", "公式源码；自动排版未成功");
      }
    });
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [
          {left: "$$", right: "$$", display: true},
          {left: "\\[", right: "\\]", display: true},
          {left: "$", right: "$", display: false},
          {left: "\\(", right: "\\)", display: false}
        ],
        throwOnError: false, trust: false,
        ignoredClasses: ["lean-source", "math-rendered", "katex"]
      });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", render);
  else render();
})();
