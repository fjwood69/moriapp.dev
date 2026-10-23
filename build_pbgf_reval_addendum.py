#!/usr/bin/env python3
"""Build pbgf/addendum/{index,light}.html from the board-approved PBGF re-validation addendum
(~/dotfiles/docs/mori-planning/pbgf-reval/04-ADDENDUM-draft.md, final text), styled to match moriapp.dev.

A separate page, like the PBGF-CS governance page: the first release is the addendum alone (board ruling
2026-10-23). The H1 and the internal status block are dropped; everything from "Provenance" on is the approved
text verbatim. The page chrome (kicker, title, byline, one-line sub) adds no claim: the sub is section 1's opening
sentence.
"""
import os

import markdown

SRC = os.path.expanduser("~/dotfiles/docs/mori-planning/pbgf-reval/04-ADDENDUM-draft.md")
HERE = os.path.expanduser("~/moriapp.dev")
BUILDER = os.path.join(HERE, "build_pbgf_cs.py")

md = open(SRC, encoding="utf-8").read()
# Strip the title block — H1, version line and opening HR; body starts at the first section.
md = md[md.index("**Provenance**"):]  # drop the H1 and the internal status block; the approved text follows verbatim
body = markdown.markdown(md, extensions=['extra', 'smarty', 'sane_lists', 'toc'],
                         extension_configs={'toc': {'permalink': False}})

# Reuse the specification page's LAYOUT/BANNER verbatim rather than copying the rules,
# so the two pages cannot drift apart visually.
_src = open(BUILDER, encoding="utf-8").read()
LAYOUT = _src[_src.index('LAYOUT = """') + len('LAYOUT = """'):_src.index('"""\n\nTHEMES')]
BANNER = _src[_src.index("BANNER = '") + len("BANNER = '"):_src.index("'\n\nfor fname")]

THEMES = {
 "pbgf/addendum/index.html": ("DARK", "/pbgf/addendum/light", "See light version →", "#0d1117", "header-dark.svg",
   "--bg:#0d1117;--surface:#161b22;--border:#21262d;--text:#e6edf3;--text-muted:#8b949e;--text-faint:#6e7681;--green:#52b788;--green-deep:#1b4332;--green-faint:rgba(82,183,136,.3);--green-wash:rgba(27,67,50,.12);--row-hover:rgba(255,255,255,.02);"),
 "pbgf/addendum/light.html": ("LIGHT", "/pbgf/addendum", "See dark version →", "#fbfbf9", "header.svg",
   "--bg:#fbfbf9;--surface:#f0f0ec;--border:#e3e3dd;--text:#14241a;--text-muted:#46514c;--text-faint:#8a8f8a;--green:#2d6a4f;--green-deep:#1b4332;--green-faint:rgba(45,106,79,.3);--green-wash:rgba(45,106,79,.06);--row-hover:rgba(0,0,0,.02);"),
}

for fname, (label, toggle_href, toggle_text, themecolor, banner, root) in THEMES.items():
    css = f":root{{{root}}}" + LAYOUT + BANNER
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PBGF re-validation addendum — mori (森)</title>
<meta name="description" content="The published paper’s five claims, re-run on current agents in a sealed harness.">
<meta property="og:title" content="PBGF re-validation addendum">
<meta property="og:description" content="The published paper’s five claims, re-run on current agents in a sealed harness.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://moriapp.dev/pbgf/addendum">
<meta property="article:author" content="Fred Wood">
<meta name="author" content="Fred Wood">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="PBGF re-validation addendum">
<meta name="twitter:description" content="The published paper’s five claims, re-run on current agents in a sealed harness.">
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
  <div class="kicker">Framework · Re-validation addendum</div>
  <h1>PBGF: re-validation addendum</h1>
  <p class="byline"><strong>Fred Wood</strong> · October 2026</p>
  <p class="sub">The published paper’s five claims, re-run on current agents in a sealed harness.</p>
</header>
<article>
{body}
</article>
<footer class="site">
  <p>Framework: <a href="/pbgf">moriapp.dev/pbgf</a> · Specification: <a href="/pbgf-cs">moriapp.dev/pbgf-cs</a> · Feedback: <a href="mailto:fredjwood@proton.me">fredjwood@proton.me</a></p>
</footer>
</div>
</body>
</html>
"""
    outpath = os.path.join(HERE, fname)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    open(outpath, "w", encoding="utf-8").write(html)
    print(f"wrote {fname} ({len(html):,} bytes) — {label}")
