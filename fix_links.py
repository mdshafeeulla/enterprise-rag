import glob, re

for file in glob.glob('frontend/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert nested <a> tags
    content = content.replace('<a href="hyperparameters.html" style="color:inherit;text-decoration:none;">Hyperparameters</a>', 'Hyperparameters')
    content = content.replace('<a href="terminal.html" style="color:inherit;text-decoration:none;">Terminal</a>', 'Terminal')
    content = content.replace('<a href="system-health.html" style="color:inherit;text-decoration:none;">System Health</a>', 'System Health')

    # Now correctly replace href="#" with the proper links
    content = re.sub(r'<a([^>]*)href="#"([^>]*)>(.*?)Hyperparameters(.*?)</a>', r'<a\1href="hyperparameters.html"\2>\3Hyperparameters\4</a>', content, flags=re.DOTALL)
    
    # In the sidebar, Query Terminal uses href="#"
    content = re.sub(r'<a([^>]*)href="#"([^>]*)>(.*?)Query\s+Terminal(.*?)</a>', r'<a\1href="terminal.html"\2>\3Query Terminal\4</a>', content, flags=re.DOTALL)
    
    content = re.sub(r'<a([^>]*)href="#"([^>]*)>(.*?)System\s+Health(.*?)</a>', r'<a\1href="system-health.html"\2>\3System Health\4</a>', content, flags=re.DOTALL)
    
    # Same for other navigation links
    content = re.sub(r'<a([^>]*)href="#"([^>]*)>(.*?)Terminal(.*?)</a>', r'<a\1href="terminal.html"\2>\3Terminal\4</a>', content, flags=re.DOTALL)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
