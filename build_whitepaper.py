#!/usr/bin/env python3
"""Build whitepaper.html (dark) + whitepaper-light.html (light) from DRAFT.md, styled to match moriapp.dev."""
import re, markdown, os

SRC = os.path.expanduser("~/dotfiles/docs/mori-planning/whitepaper/DRAFT.md")
HERE = os.path.expanduser("~/moriapp.dev")

md = open(SRC, encoding="utf-8").read()
md = md[md.index("**Mori is open source"):]                       # strip internal title + voice note
md = re.sub(r'^> \*\[Figure[^\n]*\]\*\s*$', '', md, flags=re.MULTILINE)  # strip scaffold figure markers
body = markdown.markdown(md, extensions=['extra', 'smarty', 'sane_lists', 'toc'],
                         extension_configs={'toc': {'permalink': False}})

FIGS = {
    "You cannot pick": ('figure-13-the-arc.svg',
        'The five-step spine: Memory → Curation → Governance → Insurance → Unpredictability.', None),
    "Caution is not": ('figure-11-governed-playbooks-flow.svg',
        'A governed playbook run, step by step.',
        'Architecture — built and benchmarked, not a shipped product surface.'),
    "Where Mori sits": ('figure-10-governed-playbooks-spectrum.svg',
        'The governance spectrum: blast-radius × machine-checkability; the authority↔advisor dial.',
        'Architecture — built and benchmarked, not a shipped product surface.'),
}
DAY = ('figure-12-day-in-the-life.svg', 'A day with Mori — the layers in use.',
       'Scenario figures (~80% / ~3h) are illustrative, not cited.')

def fig_html(fname, alt, guard):
    cap = f'<figcaption>{alt}' + (f' <span class="guard">{guard}</span>' if guard else '') + '</figcaption>'
    return f'<figure class="wp-fig"><img src="/assets/{fname}" alt="{alt}" loading="lazy">{cap}</figure>'

for key, (fname, alt, guard) in FIGS.items():
    pat = re.compile(r'(<h2[^>]*>[^<]*' + re.escape(key) + r'[^<]*</h2>)')
    body = pat.sub(lambda m: m.group(1) + fig_html(fname, alt, guard), body, count=1)
body = body.replace(fig_html(*FIGS["Where Mori sits"]),
                    fig_html(*FIGS["Where Mori sits"]) + fig_html(*DAY), 1)

LAYOUT = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{background:var(--bg);color:var(--text-muted);font-family:'DM Sans',system-ui,sans-serif;font-size:16px;line-height:1.8;font-weight:300;-webkit-font-smoothing:antialiased;}
.wrap{max-width:760px;margin:0 auto;padding:0 1.5rem;}
.topbar{border-bottom:1px solid var(--border);padding:1.1rem 0;display:flex;}
.topbar .wrap{display:flex;justify-content:space-between;width:100%;}
.topbar a{color:var(--text-muted);text-decoration:none;font-size:.9rem;}
.topbar a:hover{color:var(--green);}
header.hero{padding:4.5rem 0 2.5rem;border-bottom:1px solid var(--border);margin-bottom:3rem;}
header.hero .kicker{font-family:'JetBrains Mono',monospace;font-size:.8rem;letter-spacing:.12em;color:var(--green);text-transform:uppercase;margin-bottom:1.25rem;}
header.hero h1{font-family:'Fraunces',Georgia,serif;font-weight:300;font-size:clamp(2rem,5vw,3.1rem);line-height:1.1;letter-spacing:-.02em;color:var(--text);margin-bottom:1rem;}
header.hero .sub{font-size:1.1rem;color:var(--text-muted);max-width:36em;}
h2{font-family:'Fraunces',Georgia,serif;font-weight:400;font-size:clamp(1.5rem,3vw,2rem);letter-spacing:-.02em;line-height:1.25;color:var(--text);margin:3.5rem 0 1.25rem;padding-top:1rem;border-top:1px solid var(--border);}
article > h2:first-of-type{border-top:none;}
h3{font-family:'Fraunces',Georgia,serif;font-weight:400;font-size:1.25rem;color:var(--text);margin:2rem 0 .75rem;}
p{margin-bottom:1.25rem;}
strong{color:var(--text);font-weight:500;}
em{color:var(--text);font-style:italic;}
a{color:var(--green);text-decoration:none;border-bottom:1px solid var(--green-faint);}
a:hover{border-bottom-color:var(--green);}
code{font-family:'JetBrains Mono',monospace;font-size:.82em;background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:.1em .35em;color:var(--text-muted);}
blockquote{border-left:2px solid var(--green-deep);background:var(--green-wash);padding:1rem 1.25rem;margin:1.5rem 0;border-radius:0 4px 4px 0;}
blockquote p{margin:0;}
blockquote strong{color:var(--green);}
hr{border:none;border-top:1px solid var(--border);margin:3rem 0;}
table{width:100%;border-collapse:collapse;margin:1.75rem 0;font-size:.9rem;}
th,td{text-align:left;padding:.6rem .8rem;border-bottom:1px solid var(--border);vertical-align:top;}
th{color:var(--text);font-weight:500;border-bottom:1px solid var(--green-deep);}
tbody tr:hover{background:var(--row-hover);}
ul,ol{margin:0 0 1.25rem 1.4rem;}
li{margin-bottom:.5rem;}
.wp-fig{margin:2.5rem 0;text-align:center;}
.wp-fig img{max-width:100%;height:auto;border:1px solid var(--border);border-radius:8px;background:#fff;}
.wp-fig figcaption{font-size:.85rem;color:var(--text-faint);margin-top:.75rem;font-style:italic;}
.wp-fig .guard{color:var(--green);font-style:normal;display:block;margin-top:.25rem;font-size:.8rem;}
sup a,.footnote-ref a{border:none;font-size:.75em;}
.footnote{font-size:.88rem;border-top:1px solid var(--border);margin-top:3rem;padding-top:1.5rem;color:var(--text-faint);}
.footnote ol{margin-left:1.2rem;}
footer.site{border-top:1px solid var(--border);margin-top:4rem;padding:2.5rem 0 4rem;font-size:.9rem;color:var(--text-faint);}
footer.site a{color:var(--text-muted);}
"""

THEMES = {
 "whitepaper/index.html": ("DARK",  "/whitepaper/light", "See light version →", "#0d1117", "header-dark.svg",
   "--bg:#0d1117;--surface:#161b22;--border:#21262d;--text:#e6edf3;--text-muted:#8b949e;--text-faint:#6e7681;--green:#52b788;--green-deep:#1b4332;--green-faint:rgba(82,183,136,.3);--green-wash:rgba(27,67,50,.12);--row-hover:rgba(255,255,255,.02);"),
 "whitepaper/light.html": ("LIGHT", "/whitepaper",       "See dark version →",  "#fbfbf9", "header.svg",
   "--bg:#fbfbf9;--surface:#f0f0ec;--border:#e3e3dd;--text:#14241a;--text-muted:#46514c;--text-faint:#8a8f8a;--green:#2d6a4f;--green-deep:#1b4332;--green-faint:rgba(45,106,79,.3);--green-wash:rgba(45,106,79,.06);--row-hover:rgba(0,0,0,.02);"),
}
# each theme uses its matching banner (it carries its own background), shown as a centred card.
BANNER = '.wp-banner{padding:2.25rem 0 1.5rem;text-align:center;}.wp-banner img{height:84px;width:auto;max-width:92%;border-radius:10px;}'

for fname, (label, toggle_href, toggle_text, themecolor, banner, root) in THEMES.items():
    css = f":root{{{root}}}" + LAYOUT + BANNER
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Deterministic Boundaries for Non-Deterministic Agents — mori (森)</title>
<meta name="description" content="A pre-registered benchmark of AI coding agents: why information doesn't bind behaviour, what does, and every result that didn't survive.">
<meta property="og:title" content="Deterministic Boundaries for Non-Deterministic Agents">
<meta property="og:description" content="Seven model families, three independent harnesses, every result checked against the code — including the nulls and every retraction.">
<meta property="og:type" content="article">
<meta property="og:url" content="https://moriapp.dev/whitepaper">
<meta name="theme-color" content="{themecolor}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='26' font-size='28'>森</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<div class="wp-banner"><a href="/"><img src="/assets/{banner}" alt="mori (森) — a governed shared memory layer for AI coding agents"></a></div>
<div class="topbar"><div class="wrap"><a href="/">← back to moriapp.dev</a><a href="{toggle_href}">{toggle_text}</a></div></div>
<div class="wrap">
<header class="hero">
  <div class="kicker">Whitepaper</div>
  <h1>Deterministic Boundaries for Non-Deterministic Agents</h1>
  <p class="sub">Why information doesn't bind AI coding-agent behaviour — and what does. A pre-registered
  benchmark, every result checked against the code, including the ones that didn't survive.</p>
</header>
<article>
{body}
</article>
<footer class="site">
  <p>mori (森) — a governed memory layer for AI coding agents.
  <a href="/">moriapp.dev</a> · <a href="https://github.com/fjwood69/mori">github.com/fjwood69/mori</a> (AGPL-3.0)</p>
</footer>
</div>
</body>
</html>
"""
    outpath = os.path.join(HERE, fname)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    open(outpath, "w", encoding="utf-8").write(html)
    print(f"wrote {fname} ({len(html)} bytes) — {label} + banner, "
          f"figs={sum(f'assets/{f}' in html for f in ['figure-13-the-arc.svg','figure-11-governed-playbooks-flow.svg','figure-10-governed-playbooks-spectrum.svg','figure-12-day-in-the-life.svg'])}/4, "
          f"tables={html.count('<table>')}")
