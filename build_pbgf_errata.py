#!/usr/bin/env python3
"""Build pbgf/errata/{index,light}.html from Part A of the PBGF errata
(~/dotfiles/docs/mori-planning/pbgf-reval/02-ERRATA-draft.md), styled to match moriapp.dev.

Only Part A (the public text) is published; Part B (the internal evidence trail) never leaves the machine
(board publication rules, 2026-10-20). Board ruling 2026-10-24: publish the errata so the correction has its own page.
Part A is used verbatim, except that E8 is moved before E9 so the items read in number order. A dated changelog
is appended: corrections to this page are added and dated, never made silently.
"""
import os

import markdown

SRC = os.path.expanduser("~/dotfiles/docs/mori-planning/pbgf-reval/02-ERRATA-draft.md")
HERE = os.path.expanduser("~/moriapp.dev")
BUILDER = os.path.join(HERE, "build_pbgf_cs.py")

md = open(SRC, encoding="utf-8").read()
# Strip the title block — H1, version line and opening HR; body starts at the first section.
start = md.index("## Part A: proposed public text\n") + len("## Part A: proposed public text\n")
md = md[start:md.index("\n---\n\n## Part B")].strip() + "\n"
# E8 sits after E10 in the source; move it before E9 so the items read in number order.
e8 = md[md.index("**E8:"):]
md = md[:md.index("**E8:")]
md = md.replace("**E9 (checked", e8.rstrip() + "\n\n**E9 (checked", 1)
assert "Part B" not in md and "~/" not in md
# Python-Markdown needs a blank line before a list and 4-space indents for nesting; the source uses 2.
_out = []
for _l in md.split("\n"):
    _ind = len(_l) - len(_l.lstrip(" "))
    _l = " " * (_ind * 2) + _l.lstrip(" ") if _ind else _l
    if _l.startswith("- ") and _out and _out[-1].strip() and not _out[-1].lstrip().startswith("- ") and not _out[-1].startswith(" "):
        _out.append("")
    _out.append(_l)
md = "\n".join(_out)
md += """
**Changelog**

- 2026-10-24: first published.
"""
body = markdown.markdown(md, extensions=['extra', 'smarty', 'sane_lists', 'toc'],
                         extension_configs={'toc': {'permalink': False}})

# Reuse the specification page's LAYOUT/BANNER verbatim rather than copying the rules,
# so the two pages cannot drift apart visually.
_src = open(BUILDER, encoding="utf-8").read()
LAYOUT = _src[_src.index('LAYOUT = """') + len('LAYOUT = """'):_src.index('"""\n\nTHEMES')]
BANNER = _src[_src.index("BANNER = '") + len("BANNER = '"):_src.index("'\n\nfor fname")]

THEMES = {
 "pbgf/errata/index.html": ("DARK", "/pbgf/errata/light", "See light version →", "#0d1117", "header-dark.svg",
   "--bg:#0d1117;--surface:#161b22;--border:#21262d;--text:#e6edf3;--text-muted:#8b949e;--text-faint:#6e7681;--green:#52b788;--green-deep:#1b4332;--green-faint:rgba(82,183,136,.3);--green-wash:rgba(27,67,50,.12);--row-hover:rgba(255,255,255,.02);"),
 "pbgf/errata/light.html": ("LIGHT", "/pbgf/errata", "See dark version →", "#fbfbf9", "header.svg",
   "--bg:#fbfbf9;--surface:#f0f0ec;--border:#e3e3dd;--text:#14241a;--text-muted:#46514c;--text-faint:#8a8f8a;--green:#2d6a4f;--green-deep:#1b4332;--green-faint:rgba(45,106,79,.3);--green-wash:rgba(45,106,79,.06);--row-hover:rgba(0,0,0,.02);"),
}

for fname, (label, toggle_href, toggle_text, themecolor, banner, root) in THEMES.items():
    css = f":root{{{root}}}" + LAYOUT + BANNER
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PBGF errata — mori (森)</title>
<meta name="description" content="Corrections to the published paper, each checked against the primary run records.">
<meta property="og:title" content="PBGF errata">
<meta property="og:description" content="Corrections to the published paper, each checked against the primary run records.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://moriapp.dev/pbgf/errata">
<meta property="article:author" content="Fred Wood">
<meta name="author" content="Fred Wood">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="PBGF errata">
<meta name="twitter:description" content="Corrections to the published paper, each checked against the primary run records.">
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
  <div class="kicker">Framework · Errata</div>
  <h1>PBGF: errata</h1>
  <p class="byline"><strong>Fred Wood</strong> · October 2026</p>
  <p class="sub">Corrections to the published paper, each checked against the primary run records.</p>
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
