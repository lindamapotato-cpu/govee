#!/usr/bin/env python3
"""Generate static HTML exports from the Adyen NTO checkout PRD markdown."""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
MD_FILE = ROOT / "Adyen-NTO卡支付一键复购-PRD.md"
DOCS_PRD_OUT = ROOT / "docs" / "Adyen-NTO卡支付一键复购-PRD.html"

PRD_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Adyen 卡支付 · 历史卡保存与一键复购 PRD</title>
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
    .nav {
      text-align: center;
      padding: 12px 24px;
      background: #fff;
      border-bottom: 1px solid var(--border);
      font-size: 0.9rem;
    }
    .nav a { color: var(--accent); margin: 0 12px; text-decoration: none; }
    .nav a:hover { text-decoration: underline; }
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
    <h1>Adyen 卡支付 · 历史卡保存与一键复购</h1>
    <p>v1.7 · NTO · APP 商城 · US / EU / UK / CA</p>
  </header>
  <nav class="nav">
    <a href="index.html">← 文档首页</a>
    <a href="Adyen-checkout-UI交互图.html">Checkout 交互原型</a>
  </nav>
  <main class="container">
    <article id="content" class="markdown-body">
__CONTENT_HTML__
    </article>
    <p class="footer">Generated from <a href="__MD_LINK__">Adyen-NTO卡支付一键复购-PRD.md</a></p>
  </main>
  <script>
    mermaid.initialize({ startOnLoad: false, theme: "default", securityLevel: "loose" });
    document.querySelectorAll(".mermaid").forEach(function(el, i) {
      const src = el.textContent.trim();
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

MERMAID_BLOCK = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)


def read_markdown() -> str:
    if not MD_FILE.is_file():
        raise FileNotFoundError(f"Markdown source not found: {MD_FILE}")
    return MD_FILE.read_text(encoding="utf-8")


def preprocess_mermaid(md_text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        body = match.group(1).strip()
        return f'<div class="mermaid">\n{body}\n</div>\n'

    return MERMAID_BLOCK.sub(repl, md_text)


def markdown_to_html(md_text: str) -> str:
    processed = preprocess_mermaid(md_text)
    return markdown.markdown(
        processed,
        extensions=["extra", "tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )


def build_prd_html(md_text: str) -> str:
    content_html = markdown_to_html(md_text)
    md_link = html.escape(MD_FILE.name)
    return (
        PRD_PAGE_TEMPLATE.replace("__CONTENT_HTML__", content_html).replace(
            "__MD_LINK__", md_link
        )
    )


def write_outputs() -> None:
    md_text = read_markdown()
    prd_html = build_prd_html(md_text)
    DOCS_PRD_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOCS_PRD_OUT.write_text(prd_html, encoding="utf-8")
    print(f"Wrote {DOCS_PRD_OUT}")


if __name__ == "__main__":
    write_outputs()
