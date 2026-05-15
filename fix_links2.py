import glob, re

def update_href(html, keyword, new_href):
    # Find all <a> tags
    a_tags = re.finditer(r'<a\b[^>]*>.*?</a>', html, flags=re.DOTALL)
    for match in a_tags:
        a_text = match.group(0)
        if keyword in a_text:
            # Check if it has an href
            if 'href=' in a_text:
                new_a_text = re.sub(r'href="[^"]*"', f'href="{new_href}"', a_text)
                html = html.replace(a_text, new_a_text)
    return html

for file in glob.glob('frontend/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    content = update_href(content, 'Hyperparameters', 'hyperparameters.html')
    content = update_href(content, 'Query Terminal', 'terminal.html')
    content = update_href(content, 'System Health', 'system-health.html')
    # Terminal text alone might match Query Terminal, so let's be careful.
    content = update_href(content, 'Terminal v4.0', 'terminal.html')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

