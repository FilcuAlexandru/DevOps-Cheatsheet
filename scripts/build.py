################################################################
# build.py                                                     #
#                                                              #
# Generates the static HTML cheatsheet site from the           #
# markdown source files in each topic folder.                  #
#                                                              #
# Author: Filcu Alexandru                                      #
################################################################

import re, os, html, json, markdown

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# ---- SITE STRUCTURE ----

TOPICS = [
    ('linux', 'Linux', [
        ('bash', 'Bash'),
        ('networking', 'Networking'),
        ('logs', 'Logs'),
        ('systemd', 'Systemd'),
        ('performance', 'Performance'),
    ]),
    ('docker', 'Docker', []),
    ('kubernetes', 'Kubernetes', [
        ('helm', 'Helm'),
        ('openshift', 'OpenShift'),
        ('argocd', 'ArgoCD'),
    ]),
    ('ansible', 'Ansible', []),
    ('vault', 'Vault', []),
    ('oracle-db', 'Oracle Database', []),
    ('postgresql', 'PostgreSQL', []),
    ('weblogic', 'WebLogic', []),
    ('prometheus', 'Prometheus', []),
    ('grafana', 'Grafana', []),
    ('checkmk', 'Check_MK', []),
    ('python', 'Python', []),
    ('powershell', 'PowerShell', []),
    ('git', 'Git', []),
    ('data-formats', 'YAML / JSON / JQ', []),
    ('troubleshooting', 'Troubleshooting', []),
    ('production-safety', 'Production Safety', []),
    ('quick-reference', 'Quick References', []),
]

GROUPS = [
    ('OS & Shell', ['linux']),
    ('Containers & Orchestration', ['docker', 'kubernetes']),
    ('Automation & Secrets', ['ansible', 'vault']),
    ('Databases', ['oracle-db', 'postgresql']),
    ('Application Servers', ['weblogic']),
    ('Monitoring', ['prometheus', 'grafana', 'checkmk']),
    ('Languages', ['python', 'powershell']),
    ('Version Control', ['git']),
    ('Data Formats', ['data-formats']),
    ('Reference', ['troubleshooting', 'production-safety', 'quick-reference']),
]

# ---- FOLDERS THAT MERGE SEVERAL .MD FILES INTO ONE PAGE ----
MULTI_FILE_FOLDERS = {'linux', 'linux/bash', 'linux/networking'}

TOPIC_LOOKUP = {slug: (title, children) for slug, title, children in TOPICS}

SEARCH_INDEX = []  # list of {cmd, tip, section, page, topic}

# ---- PAGE TEMPLATE ----

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — DevOps Cheatsheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_path}">
</head>
<body>
<div class="topbar">
  <span class="brand">~/devops-cheatsheet</span>
  <button id="search-trigger" class="search-btn" data-prefix="{prefix}">Search <span class="kbd">/</span></button>
  {topnav}
</div>
<div id="search-overlay" class="search-overlay" hidden>
  <div class="search-panel">
    <input id="search-input" type="text" placeholder="Search commands…" autocomplete="off">
    <div id="search-results" class="search-results"></div>
  </div>
</div>
<div class="layout">
  <div class="sidebar">
    <div class="label">ON THIS PAGE</div>
    <ul>
      {sidenav}
    </ul>
  </div>
  <main>
    {breadcrumb}
    <div class="title-frame">
      <h1>{title}</h1>
      <div class="subtitle-readout">{readout}</div>
    </div>
    {children_grid}
    {body}
  </main>
</div>
<script src="{prefix}assets/search-index.js"></script>
<script src="{prefix}assets/search.js"></script>
<script src="{prefix}assets/tooltip.js"></script>
</body>
</html>
"""

# ---- MARKDOWN -> HTML HELPERS ----

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def wrap_smart_blocks(text):
    blocks = text.split('\n\n')
    out = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b.lstrip().startswith('**Enhanced'):
            m = re.match(r'\*\*(Enhanced[^*]*?)\*\*:?\s*\n?(.*)', b.strip(), re.DOTALL)
            if m:
                heading_text = m.group(1).rstrip(':').strip()
                remainder = m.group(2).strip()
            else:
                heading_text = 'Enhanced'
                remainder = ''
            group = [heading_text]
            i += 1
            if remainder:
                group.append(remainder)
            elif i < len(blocks) and blocks[i].lstrip().startswith('```'):
                group.append(blocks[i])
                i += 1
            summary = group[0]
            rest = '\n\n'.join(group[1:])
            out.append(f'<details class="enhanced-block" open markdown="1"><summary class="enhanced-heading">{summary}</summary>\n\n{rest}\n\n</details>')
        else:
            out.append(b)
            i += 1
    return '\n\n'.join(out)

def make_tip(comment):
    tip = comment.strip().strip('-').strip()
    if not tip:
        return None
    tip = tip[0].upper() + tip[1:]
    if not tip.endswith(('.', ')', ':')):
        tip += '.'
    return tip

PLACEHOLDER_RULES = [
    ('password', '••••••••'), ('pass', '••••••••'),
    ('username', 'myuser'), ('user', 'myuser'),
    ('hostname', 'myserver'), ('host', 'myserver'),
    ('port', '8080'),
    ('serial#', '101'), ('pid', '12345'), ('sid', '1'),
    ('namespace', 'mynamespace'), ('project', 'myproject'),
    ('database', 'mydb'), ('table', 'mytable'),
    ('key', 'mykey'), ('value', 'myvalue'),
    ('path', 'mypath'), ('file', 'myfile.yml'),
    ('app_name', 'myapp'), ('release_name', 'myapp'), ('chart', 'mychart'),
    ('service_name', 'myservice'), ('server_name', 'myserver'), ('service_account', 'mysa'),
    ('cluster', 'mycluster'), ('context', 'mycontext'),
    ('node_name', 'mynode'), ('policy_name', 'mypolicy'), ('policy_file', 'mypolicy.hcl'),
    ('role_name', 'myrole'), ('revision', '2'), ('history_id', '2'),
    ('tag_name', 'mytag'), ('task_name', 'mytask'),
    ('inventory_file', 'myinventory.ini'), ('host_or_group', 'mygroup'),
    ('route_name', 'myroute'), ('tns_alias', 'MYDB'),
    ('keystore', 'mykeystore.jks'), ('alias', 'myalias'), ('cert', 'mycert.pem'),
    ('api_key', 'mykey'), ('uid', 'myuid'),
    ('dashboard_name', 'mydashboard'), ('unseal_key', 'mykey'),
    ('tablespace', 'MYTABLESPACE'), ('command', 'mycommand'),
    ('sql', "SELECT 1;"), ('query', "SELECT 1;"),
]

def example_for_token(token):
    t = token.lower().strip()
    for needle, val in PLACEHOLDER_RULES:
        if needle in t:
            return val
    return 'example'

def substitute_placeholders(cmd_text):
    return re.sub(r'&lt;([^&<>]+)&gt;', lambda m: example_for_token(m.group(1)), cmd_text)

# ---- TOOLTIP CONTENT (what/example/use case) ----

def enrich_tooltips(body_html, topic_title):
    pattern = re.compile(
        r'<h[12] id="[^"]+">(?P<htext>.*?)</h[12]>'
        r'|<span class="cmdline"(?: tabindex="0")? data-tip="(?P<tip>[^"]*)">(?P<cmd>.*?)</span>'
    )
    current_section = topic_title
    out = []
    last_end = 0
    for m in pattern.finditer(body_html):
        out.append(body_html[last_end:m.start()])
        if m.group('htext') is not None:
            sect = strip_tags(m.group('htext'))
            sect = re.sub(r'^.+? — ', '', sect)
            current_section = sect
            out.append(m.group(0))
        else:
            old_tip = html.unescape(m.group('tip'))
            cmd = m.group('cmd')
            cmd_plain = strip_tags(cmd)
            example = substitute_placeholders(cmd)
            example = html.unescape(example)
            parts = [old_tip]
            parts.append('Example: ' + example)
            usecase = current_section if current_section != topic_title else topic_title
            parts.append('Use case: ' + usecase)
            new_tip = '\n'.join(parts)
            new_tip_esc = html.escape(new_tip, quote=True)
            out.append(f'<span class="cmdline" tabindex="0" data-tip="{new_tip_esc}">{cmd}</span>')
        last_end = m.end()
    out.append(body_html[last_end:])
    return ''.join(out)

def strip_tags(s):
    return re.sub('<[^<]+?>', '', s)

def tooltipify_code(html_text):
    comment_pat = re.compile(r'^(.*?)(\s{2,}(?:--|#)\s?)(.*)$')

    def repl_code(m):
        open_tag, code, close_tag = m.group(1), m.group(2), m.group(3)
        is_sql = 'language-sql' in open_tag
        marker = '--' if is_sql else '#'

        # group lines into logical commands — a line that starts
        # indented continues the previous one (SQL clause wrapping);
        # anything flush-left starts a new command
        groups, buf = [], []
        for line in code.split('\n'):
            if line.strip() == '':
                if buf:
                    groups.append(buf)
                    buf = []
                continue
            if buf and line[0] in (' ', '\t'):
                buf.append(line)
            else:
                if buf:
                    groups.append(buf)
                buf = [line]
        if buf:
            groups.append(buf)

        boxes = []
        for group in groups:
            comment, cleaned = None, []
            for gl in group:
                cm = comment_pat.match(gl)
                if cm and comment is None:
                    cleaned.append(cm.group(1))
                    comment = cm.group(3)
                else:
                    cleaned.append(gl)
            cmd_full = '\n'.join(cleaned)
            tip = make_tip(comment) if comment else None
            if tip:
                tip_esc = html.escape(tip, quote=True)
                comment_esc = html.escape(comment.strip())
                boxes.append(
                    f'<div class="cmd-box"><span class="c">{marker} {comment_esc}</span>'
                    f'<span class="cmdline" tabindex="0" data-tip="{tip_esc}">{cmd_full}</span></div>'
                )
            else:
                boxes.append(f'<div class="cmd-box"><span class="cmdline">{cmd_full}</span></div>')
        return open_tag + ''.join(boxes) + close_tag
    return re.sub(r'(<pre><code[^>]*>)(.*?)(</code></pre>)', repl_code, html_text, flags=re.DOTALL)

def md_to_html(md_text):
    pre = wrap_smart_blocks(md_text)
    body = markdown.markdown(pre, extensions=['fenced_code', 'tables', 'md_in_html', 'toc'])
    body = tooltipify_code(body)
    return body

# ---- PAGE ASSEMBLY ----

def gather_content(rel_folder):
    path = os.path.join(root, rel_folder)
    if rel_folder in MULTI_FILE_FOLDERS:
        readme = open(os.path.join(path, 'README.md')).read()
        file_order = re.findall(r'\(\./(.+?)\.md\)', readme)
        parts = []
        for fname in file_order:
            fpath = os.path.join(path, fname + '.md')
            if os.path.exists(fpath):
                parts.append(open(fpath).read())
        return '\n\n'.join(parts)
    else:
        content = open(os.path.join(path, 'README.md')).read()
        content = re.sub(r'^# .+\n+', '', content, count=1)
        return content

def build_sidenav(body_html):
    heads = re.findall(r'<h([12]) id="([^"]+)">(.*?)</h\1>', body_html)
    items = []
    for level, hid, text in heads:
        text = strip_tags(text)
        text = re.sub(r'^.+? — ', '', text)
        indent = ' style="padding-left:20px;font-size:12px;"' if level == '2' else ''
        items.append(f'<li><a href="#{hid}"{indent}>{text}</a></li>')
    return '\n      '.join(items) if items else '<li><span style="color:var(--text-dim);font-size:12px;">—</span></li>'

def build_topnav(current_top, prefix):
    links = [f'<a href="{prefix}index.html">index</a>']
    for slug, title, children in TOPICS:
        cls = ' class="active"' if slug == current_top else ''
        links.append(f'<a href="{prefix}{slug}/index.html"{cls}>{title.lower()}</a>')
    return '\n  '.join(links)

def index_page_commands(body_html, page_rel, topic_title, page_title):
    """Walk headings + cmdline spans in document order, attribute commands to nearest heading."""
    pattern = re.compile(
        r'<h[12] id="([^"]+)">(.*?)</h[12]>'
        r'|<span class="cmdline"(?: tabindex="0")? data-tip="([^"]*)">(.*?)</span>'
    )
    current_id, current_title = '', page_title
    for m in pattern.finditer(body_html):
        if m.group(1) is not None:
            current_id = m.group(1)
            current_title = strip_tags(m.group(2))
            current_title = re.sub(r'^.+? — ', '', current_title)
        else:
            tip = html.unescape(m.group(3))
            cmd = strip_tags(m.group(4))
            if not cmd.strip():
                continue
            SEARCH_INDEX.append({
                'cmd': cmd,
                'tip': tip,
                'section': current_title,
                'topic': topic_title,
                'page': page_rel,
                'anchor': current_id,
            })

def make_collapsible_sections(body_html):
    pattern = re.compile(r'(<h[12] id="[^"]+">.*?</h[12]>)')
    parts = pattern.split(body_html)
    if len(parts) < 2:
        return body_html
    out = [parts[0]]
    i = 1
    while i < len(parts):
        heading = parts[i]
        content = parts[i + 1] if i + 1 < len(parts) else ''
        out.append(f'<details class="section-block" open><summary>{heading}</summary>{content}</details>')
        i += 2
    return ''.join(out)

# ---- RENDER ----

def render_page(top_slug, top_title, sub_slug=None, sub_title=None, children=None):
    depth = 1 if sub_slug is None else 2
    prefix = '../' * depth
    rel_folder = top_slug if sub_slug is None else f'{top_slug}/{sub_slug}'
    folder_path = os.path.join(root, rel_folder)

    md_content = gather_content(rel_folder)
    empty = (not md_content.strip()) or ('to fill in' in md_content.lower())
    if empty:
        body_html = '<p style="color:var(--text-dim);">Not filled in yet — this section will be added as it comes up in practice.</p>'
    else:
        body_html = md_to_html(md_content)
        index_page_commands(body_html, f'{rel_folder}/index.html', top_title, sub_title or top_title)
        body_html = enrich_tooltips(body_html, sub_title or top_title)
        body_html = make_collapsible_sections(body_html)

    title = sub_title if sub_title else top_title
    breadcrumb = ''
    if sub_slug:
        breadcrumb = f'<div style="font-size:12px;margin-bottom:6px;"><a href="../index.html">{top_title}</a> <span style="color:var(--text-dim);">/</span> {sub_title}</div>'

    children_grid = ''
    if children:
        cards = []
        for cslug, ctitle in children:
            cards.append(f'<a class="card" href="./{cslug}/index.html">{ctitle}</a>')
        children_grid = f'<div class="label" style="margin:24px 0 8px;">SECTIONS</div><div class="grid" style="margin-top:0;">{"".join(cards)}</div>'

    sidenav = build_sidenav(body_html)
    topnav = build_topnav(top_slug, prefix)
    subtitle = f"Commands and notes for {title.lower()}."
    cmd_count = len(re.findall(r'class="cmdline"', body_html))
    readout = f"{cmd_count} COMMAND{'S' if cmd_count != 1 else ''} INDEXED" if cmd_count else "REFERENCE"

    html_out = TEMPLATE.format(
        title=title,
        css_path=f'{prefix}assets/style.css',
        prefix=prefix,
        topnav=topnav,
        sidenav=sidenav,
        breadcrumb=breadcrumb,
        children_grid=children_grid,
        body=body_html,
        subtitle=subtitle,
        readout=readout,
    )
    with open(os.path.join(folder_path, 'index.html'), 'w') as f:
        f.write(html_out)
    print(f"built {rel_folder}/index.html")

# ---- BUILD EVERY PAGE ----

for slug, title, children in TOPICS:
    render_page(slug, title, children=children)
    for cslug, ctitle in children:
        render_page(slug, title, sub_slug=cslug, sub_title=ctitle)

# ---- SEARCH INDEX FILE ----
with open(os.path.join(root, 'assets', 'search-index.js'), 'w') as f:
    f.write('window.SEARCH_INDEX = ' + json.dumps(SEARCH_INDEX, ensure_ascii=False) + ';\n')
print(f"indexed {len(SEARCH_INDEX)} commands")

# ---- ROOT LANDING PAGE ----
def topic_status(slug, children):
    if children:
        return False
    md_content = gather_content(slug)
    return (not md_content.strip()) or ('to fill in' in md_content.lower())

group_html = []
for gi, (group_name, slugs) in enumerate(GROUPS, start=1):
    cards = []
    for slug in slugs:
        title, children = TOPIC_LOOKUP[slug]
        empty = topic_status(slug, children)
        cls = 'card empty' if empty else 'card'
        cards.append(f'<a class="{cls}" href="./{slug}/index.html">{title}</a>')
    group_num = str(gi).zfill(2)
    group_html.append(f'<div class="label" style="margin:28px 0 8px;"><span class="group-num">{group_num}</span>{group_name.upper()}</div><div class="grid">{"".join(cards)}</div>')

root_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DevOps Cheatsheet</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/style.css">
</head>
<body>
<div class="topbar">
  <span class="brand">~/devops-cheatsheet</span>
  <button id="search-trigger" class="search-btn" data-prefix="./">Search <span class="kbd">/</span></button>
</div>
<div id="search-overlay" class="search-overlay" hidden>
  <div class="search-panel">
    <input id="search-input" type="text" placeholder="Search commands…" autocomplete="off">
    <div id="search-results" class="search-results"></div>
  </div>
</div>
<div style="max-width:1100px;margin:0 auto;padding:40px 36px 80px;">
  <div class="title-frame">
    <h1>DevOps Cheatsheet</h1>
    <div class="subtitle-readout">{len(SEARCH_INDEX)} COMMANDS INDEXED · {len(TOPICS)} MODULES</div>
  </div>
  <div class="subtitle">Personal command reference, organized by platform. Press / to search, or hover any command for what it does.</div>
  {''.join(group_html)}
</div>
<script src="./assets/search-index.js"></script>
<script src="./assets/search.js"></script>
<script src="./assets/tooltip.js"></script>
</body>
</html>
"""
with open(os.path.join(root, 'index.html'), 'w') as f:
    f.write(root_html)
print("built root index.html")
