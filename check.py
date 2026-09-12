"""Small regression check: escaping, optional blanks, links, and static assets."""
import json
from build import ROOT, render, link

c = json.loads((ROOT / 'content.json').read_text())
page = render(c)
assert '<h1>' in page and 'Charamelt' in page
assert 'id="contact"' not in page if not any(c[k] for k in ('email', 'github', 'linkedin', 'resume_url')) else 'id="contact"' in page
c['name'] = '<script>alert("x")</script>'
c['interests'] = '</script><img src=x onerror=alert(1)>'
c['show_empty_project'] = False
c['github'] = 'https://github.com/example'
page = render(c)
assert '<script>alert' not in page and '&lt;script&gt;' in page
assert 'An open slot' not in page and 'id="contact"' in page
assert 'href="https://github.com/example"' in page
for bad in ('javascript:alert(1)', '//example.com', 'data:text/html,test'):
    try:
        link(bad, 'Unsafe')
        raise AssertionError('Unsafe URL accepted')
    except ValueError:
        pass
for file in ('theme.css', 'theme.js', 'favicon.svg'):
    assert (ROOT / 'site' / file).is_file()
print('Checks passed: escaping, empty fields, contact links, URL validation, assets.')

assert "</script><img" not in page
assert "marcoho@portfolio" in page and ".dev</span>" not in page
assert "terminal-form" in page
