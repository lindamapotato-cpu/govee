#!/usr/bin/env python3
"""Generate HTML exports from the US Govee partial-refund invoice PRD markdown."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD_FILE = ROOT / "us-govee-部分退款发票更新-PRD-v0.2.md"
ASSETS_OUT = ROOT / "assets" / "us-govee-部分退款发票更新-PRD-展示页.html"
DOCS_PRD_OUT = ROOT / "docs" / "us-govee-部分退款发票更新-PRD.html"
DOCS_INDEX_OUT = ROOT / "docs" / "index.html"

PRD_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>us.govee.com 部分退款发票更新 PRD v0.5</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    :root {
      --bg: #f6f8fb;
      --card: #ffffff;
      --text: #1a2332;
      --muted: #5c6b7a;
      --border: #e2e8f0;
      --accent: #2563eb;
      --code-bg: #f1f5f9;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "PingFang SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
    }
    .page-header {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
      color: #e2e8f0;
      padding: 32px 24px;
      text-align: center;
    }
    .page-header h1 { margin: 0 0 8px; font-size: 1.6rem; font-weight: 700; }
    .page-header p { margin: 0; color: #94a3b8; font-size: 0.95rem; }
    .container {
      max-width: 920px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }
    .markdown-body {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 40px 48px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .markdown-body h1 { font-size: 1.75rem; border-bottom: 2px solid var(--border); padding-bottom: 0.4em; margin-top: 0; }
    .markdown-body h2 { font-size: 1.35rem; margin-top: 2em; border-bottom: 1px solid var(--border); padding-bottom: 0.3em; }
    .markdown-body h3 { font-size: 1.1rem; margin-top: 1.5em; }
    .markdown-body table { width: 100%; border-collapse: collapse; margin: 1em 0; font-size: 0.92rem; }
    .markdown-body th, .markdown-body td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
    .markdown-body th { background: var(--code-bg); font-weight: 600; }
    .markdown-body code { background: var(--code-bg); padding: 0.15em 0.4em; border-radius: 4px; font-size: 0.9em; }
    .markdown-body pre { background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; }
    .markdown-body pre code { background: none; padding: 0; color: inherit; }
    .markdown-body blockquote { border-left: 4px solid var(--accent); margin: 1em 0; padding: 0.5em 1em; background: #eff6ff; color: var(--muted); }
    .markdown-body hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }
    .mermaid { margin: 1.5em 0; text-align: center; }
    .footer { text-align: center; color: var(--muted); font-size: 0.85rem; margin-top: 24px; }
    @media (max-width: 640px) {
      .markdown-body { padding: 24px 18px; }
    }
  </style>
</head>
<body>
  <header class="page-header">
    <h1>us.govee.com 部分退款发票更新 PRD</h1>
    <p>v0.5 · ERP 驱动退款流程 · 美国站不含税定价</p>
  </header>
  <main class="container">
    <article id="content" class="markdown-body"></article>
    <p class="footer">Generated from <a href="__MD_LINK__">us-govee-部分退款发票更新-PRD-v0.2.md</a></p>
  </main>
  <script>
    const rawMd = __MD_ESCAPED__;
    mermaid.initialize({ startOnLoad: false, theme: "default", securityLevel: "loose" });

    const renderer = new marked.Renderer();
    renderer.code = function(code, infostring) {
      const lang = (infostring || "").trim().toLowerCase();
      if (lang === "mermaid") {
        return '<div class="mermaid">' + code + "</div>";
      }
      const escaped = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return "<pre><code>" + escaped + "</code></pre>";
    };

    marked.setOptions({ renderer: renderer, gfm: true, breaks: false });
    document.getElementById("content").innerHTML = marked.parse(rawMd);

    document.querySelectorAll(".mermaid").forEach(function(el, i) {
      const src = el.textContent;
      const id = "mermaid-" + i;
      mermaid.render(id, src).then(function(result) {
        el.innerHTML = result.svg;
      }).catch(function(err) {
        el.innerHTML = "<pre>Mermaid error: " + err.message + "</pre>";
      });
    });
  </script>
</body>
</html>
"""

DOCS_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Govee US 文档</title>
  <style>
    body {
      font-family: "PingFang SC", "Microsoft YaHei", -apple-system, BlinkMacSystemFont, sans-serif;
      max-width: 720px;
      margin: 48px auto;
      padding: 0 24px;
      line-height: 1.6;
      color: #1a2332;
    }
    h1 { font-size: 1.5rem; }
    ul { padding-left: 1.2em; }
    a { color: #2563eb; }
    .meta { color: #64748b; font-size: 0.9rem; }
  </style>
</head>
<body>
  <h1>Govee US 项目文档</h1>
  <p class="meta">GitHub Pages · mashulin05/govee-Risk-control-system</p>
  <h2>产品需求文档</h2>
  <ul>
    <li><a href="us-govee-部分退款发票更新-PRD.html">us.govee.com 部分退款发票更新 PRD v0.5</a></li>
  </ul>
</body>
</html>
"""


def read_markdown() -> str:
    if not MD_FILE.is_file():
        raise FileNotFoundError(f"Markdown source not found: {MD_FILE}")
    return MD_FILE.read_text(encoding="utf-8")


def build_prd_html(md_text: str) -> str:
  escaped = json.dumps(md_text, ensure_ascii=False)
  md_link = html.escape(MD_FILE.name)
  return (
    PRD_PAGE_TEMPLATE.replace("__MD_ESCAPED__", escaped).replace("__MD_LINK__", md_link)
  )


def write_outputs() -> None:
    md_text = read_markdown()
    prd_html = build_prd_html(md_text)

    ASSETS_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOCS_PRD_OUT.parent.mkdir(parents=True, exist_ok=True)

    ASSETS_OUT.write_text(prd_html, encoding="utf-8")
    DOCS_PRD_OUT.write_text(prd_html, encoding="utf-8")
    DOCS_INDEX_OUT.write_text(DOCS_INDEX_TEMPLATE, encoding="utf-8")

    print(f"Wrote {ASSETS_OUT}")
    print(f"Wrote {DOCS_PRD_OUT}")
    print(f"Wrote {DOCS_INDEX_OUT}")


if __name__ == "__main__":
    write_outputs()
