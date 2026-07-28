#!/usr/bin/env python3
"""Build pbgf/receipts/graph-moat-measurement-1/{index,light}.html from the receipt source.

The framework paper cites this measurement by filename and commit hash. A hash in a private
repository has the form of a verifiable citation without the substance: it cannot be fetched.
Publishing the receipt makes the citation act like one — URL for retrieval, hash for
provenance, neither sufficient alone.

PERMANENCE. This URL is a promise. It does not move, and the document is never silently
edited: corrections are appended with a date, exactly as the correction of 2026-07-27 was. A
second measurement would be published at `-2`, never as a replacement for this one — a
corrected paper points here, and a pointer that can be quietly rewritten is worth nothing.
"""
import os
import re

import markdown

SRC = os.path.expanduser("~/dotfiles/docs/mori-planning/graph-moat-measurement-1.md")
HERE = os.path.expanduser("~/moriapp.dev")
BUILDER = os.path.join(HERE, "build_pbgf_cs.py")

md = open(SRC, encoding="utf-8").read()
# Drop the H1 and the date line — both are rendered in the hero instead.
md = md[md.index("## Setup"):]
body = markdown.markdown(md, extensions=['extra', 'smarty', 'sane_lists', 'toc'],
                         extension_configs={'toc': {'permalink': False}})

# Reuse the specification page's styling by extraction rather than duplication.
_src = open(BUILDER, encoding="utf-8").read()
LAYOUT = _src[_src.index('LAYOUT = """') + len('LAYOUT = """'):_src.index('"""\n\nTHEMES')]
BANNER = _src[_src.index("BANNER = '") + len("BANNER = '"):_src.index("'\n\nfor fname")]

THEMES = {
 "pbgf/receipts/graph-moat-measurement-1/index.html": ("DARK", "/pbgf/receipts/graph-moat-measurement-1/light", "See light version →", "#0d1117", "header-dark.svg",
   "--bg:#0d1117;--surface:#161b22;--border:#21262d;--text:#e6edf3;--text-muted:#8b949e;--text-faint:#6e7681;--green:#52b788;--green-deep:#1b4332;--green-faint:rgba(82,183,136,.3);--green-wash:rgba(27,67,50,.12);--row-hover:rgba(255,255,255,.02);"),
 "pbgf/receipts/graph-moat-measurement-1/light.html": ("LIGHT", "/pbgf/receipts/graph-moat-measurement-1", "See dark version →", "#fbfbf9", "header.svg",
   "--bg:#fbfbf9;--surface:#f0f0ec;--border:#e3e3dd;--text:#14241a;--text-muted:#46514c;--text-faint:#8a8f8a;--green:#2d6a4f;--green-deep:#1b4332;--green-faint:rgba(45,106,79,.3);--green-wash:rgba(45,106,79,.06);--row-hover:rgba(0,0,0,.02);"),
}

for fname, (label, toggle_href, toggle_text, themecolor, banner, root) in THEMES.items():
    css = f":root{{{root}}}" + LAYOUT + BANNER
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Receipt — code-graph moat, Measurement #1 — mori (森)</title>
<meta name="description" content="The Go/No-Go yield measurement cited by the PBGF framework as receipt #6, published in full with its dated correction. A null result: on this corpus nothing became enforceable machinery.">
<meta property="og:title" content="Receipt — code-graph moat, Measurement #1 (NULL)">
<meta property="og:description" content="16 conventions, 9 emitted checks, 3 engine-valid, measured Tier-1 zero. Published with the dated correction that established it.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://moriapp.dev/pbgf/receipts/graph-moat-measurement-1">
<meta name="author" content="Fred Wood">
<meta name="theme-color" content="{themecolor}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='28'>森</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="wp-banner"><a href="/"><img src="/assets/{banner}" alt="mori (森) — a governed shared memory layer for AI coding agents"></a></div>
<div class="topbar"><div class="wrap"><a href="/pbgf">← back to the framework</a><a href="{toggle_href}">{toggle_text}</a></div></div>
<div class="wrap">
<header class="hero">
  <div class="kicker">Receipt #6 · Measured 2026-06-25 · Corrected 2026-07-27</div>
  <h1>Code-graph moat — Measurement #1</h1>
  <p class="byline"><strong>A null result.</strong> On this corpus, with this compiler, nothing became enforceable machinery.</p>
  <p class="sub">The Go/No-Go yield measurement the framework cites as receipt #6, published in full — including the correction that withdrew its headline figure a month after it was written.</p>
  <p class="draft-note">This page is a fixed address. It does not move, and it is never silently edited: corrections are appended and dated, and a second measurement would be published separately rather than replacing this one. The paper points here, and a pointer that can be quietly rewritten is worth nothing.</p>
</header>
<article>
{body}
</article>
<footer class="site">
  <p>Cited by the <a href="/pbgf">PBGF framework</a> as receipt #6. Source: <code>graph-moat-measurement-1.md</code>, committed <code>53203a4</code>, 2026-06-25.</p>
  <p>Feedback: <a href="mailto:fredjwood@proton.me">fredjwood@proton.me</a></p>
</footer>
</div>
</body>
</html>
"""
    outpath = os.path.join(HERE, fname)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    open(outpath, "w", encoding="utf-8").write(html)
    print(f"wrote {fname} ({len(html):,} bytes) — {label}")
