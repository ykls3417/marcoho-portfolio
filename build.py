"""Build a dependency-free static portfolio. Edit content.json, then run python3 build.py."""
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent

def e(value):
    return escape(str(value), quote=True)

def link(url, label, css=''):
    if not url:
        return ''
    parsed = urlsplit(url)
    if parsed.scheme not in ('https', 'http', 'mailto') and (parsed.scheme or url.startswith('//')):
        raise ValueError('Use an https URL, mailto address, or relative file path.')
    return f'<a class="{e(css)}" href="{e(url)}">{e(label)} <span aria-hidden="true">↗</span></a>'

def render(c):
    projects = []
    for i, p in enumerate(c['projects'], 1):
        if not p['name']:
            if c['show_empty_project']:
                projects.append(f'<article class="project empty"><span class="number">{i:02}</span><div><p class="eyebrow">An open slot</p><h3>Next experiment<span class="accent">_</span></h3><p>Room for whatever comes next.</p></div><span class="empty-symbol" aria-hidden="true">[ + ]</span></article>')
            continue
        tags = ''.join(f'<li>{e(t)}</li>' for t in p['tags'])
        note = f'<p class="project-note">{e(p["note"])}</p>' if p['note'] else ''
        projects.append(f'<article class="project"><span class="number">{i:02}</span><div><p class="eyebrow">{e(p["category"])}</p><h3>{e(p["name"])}</h3><p>{e(p["description"])}</p>{note}<ul class="tags" aria-label="Technologies">{tags}</ul></div>{link(p["url"], "View project", "project-link")}</article>')
    jobs = ''.join(f'<article class="job"><p class="dates">{e(j["dates"])}</p><div><h3>{e(j["role"])}</h3><p class="company">{e(j["company"])}</p><p>{e(j["description"])}</p></div></article>' for j in c['experience'])
    contacts = ''.join([link('mailto:' + c['email'] if c['email'] else '', 'Email', 'button primary'), link(c['github'], 'GitHub', 'button'), link(c['linkedin'], 'LinkedIn', 'button'), link(c['resume_url'], 'Résumé', 'button')])
    contact = f'<section id="contact" class="contact"><p class="eyebrow">04 / Contact</p><h2>{e(c["contact_heading"])}</h2><p>{e(c["contact_text"])}</p><div class="actions">{contacts}</div></section>' if contacts else ''
    contact_nav = '<a href="#contact">Contact</a>' if contacts else ''
    skills = ''.join(f'<li>{e(s)}</li>' for s in c['skills'])
    headline = '<br>'.join(e(c['headline']).split('\n'))
    note = f'<p class="personal-note">{e(c["personal_note"])}</p>' if c['personal_note'] else ''
    terminal_data = json.dumps(c, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c['name'])} — {e(c['role'])}</title><meta name="description" content="{e(c['intro'])}">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="theme.css">
<script src="theme.js" defer></script><script src="terminal.js" defer></script></head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="shell"><header><a class="brand" href="#" aria-label="{e(c['name'])} home"><span class="accent" aria-hidden="true">&gt;_</span> {e(c['handle'])}</a><nav aria-label="Main navigation"><a href="#work">Work</a><a href="#about">About</a>{contact_nav}<button id="theme" hidden aria-pressed="false">Light mode</button></nav></header>
<main id="main"><section class="hero"><div><p class="eyebrow accent">{e(c['role'])} / {e(c['location'])}</p><h1>{headline}<span class="cursor" aria-hidden="true">_</span></h1><p class="intro">{e(c['intro'])}</p>{note}<div class="actions"><a class="button primary" href="#work">Explore my work <span aria-hidden="true">↓</span></a><a class="text-link" href="#about">A little about me <span aria-hidden="true">↗</span></a></div></div>
<aside class="terminal" aria-label="Interactive portfolio terminal"><div class="terminal-bar"><span aria-hidden="true">● ● ●</span><span>{e(c['handle'])}@portfolio</span></div><div class="terminal-body"><div id="terminal-log" role="log" aria-live="polite" aria-relevant="additions" tabindex="0" aria-label="Command output"><p class="terminal-name">{e(c['name'])}</p><p>{e(c['role'])} · {e(c['location'])}</p><p class="terminal-welcome">{e(c['terminal_welcome'])}</p></div><form id="terminal-form" hidden><label for="terminal-input" class="terminal-label">{e(c['handle'])}@portfolio <span class="muted">~ $</span></label><div class="terminal-entry"><input id="terminal-input" name="command" aria-describedby="terminal-hint" autocomplete="off" autocapitalize="off" spellcheck="false" maxlength="160" placeholder="help"><button type="submit">Run</button></div></form><div id="terminal-shortcuts" hidden><button type="button" data-command="help">help</button><button type="button" data-command="projects">projects</button><button type="button" data-command="interests">interests</button><button type="button" data-command="clear">clear</button></div><p id="terminal-hint" hidden>↑ ↓ history · Tab complete · Portfolio commands only</p><noscript><p>Enable JavaScript for terminal commands. All portfolio sections are readable below.</p></noscript></div></aside><script id="terminal-data" type="application/json">{terminal_data}</script></section>
<section id="work"><div class="section-title"><h2><span>01 /</span> Selected work</h2><span class="section-command" aria-hidden="true">ls ./projects</span></div>{''.join(projects)}</section>
<section id="about" class="about"><div><h2><span>02 /</span> Behind the keyboard</h2><p>{e(c['about'])}</p><h3 class="interests-heading">What keeps me interested</h3><p>{e(c['interests'])}</p><p class="education">{e(c['education'])}</p></div><div class="toolkit"><p class="eyebrow">Tools I reach for</p><ul class="tags">{skills}</ul></div></section>
<section id="experience"><div class="section-title"><h2><span>03 /</span> Along the way</h2><span class="section-command" aria-hidden="true">cat experience.log</span></div>{jobs}</section>{contact}
</main><footer><span><span class="accent" aria-hidden="true">&gt;_</span> {e(c['name'])}</span><span>{e(c['footer'])}</span><a href="#">Back to top ↑</a></footer></div></body></html>'''

if __name__ == '__main__':
    content = json.loads((ROOT / 'content.json').read_text())
    (ROOT / 'site' / 'index.html').write_text(render(content))
    print('Built site/index.html')
