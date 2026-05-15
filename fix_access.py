import glob

files = glob.glob('frontend/*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Fix inline version (admin-command.html, admin-command-3.html)
    content = content.replace(
        'href="#"><span class="material-symbols-outlined text-[20px]">admin_panel_settings</span>Access Control and Logs</a>',
        'href="admin-command-2.html"><span class="material-symbols-outlined text-[20px]">admin_panel_settings</span>Access Control and Logs</a>'
    )
    
    # Fix multiline version (hyperparameters.html)
    old = '''href="#">
<span class="material-symbols-outlined text-[20px]">admin_panel_settings</span>
                    Access Control and Logs
                </a>'''
    new = '''href="admin-command-2.html">
<span class="material-symbols-outlined text-[20px]">admin_panel_settings</span>
                    Access Control and Logs
                </a>'''
    content = content.replace(old, new)

    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(content)

print('Done')
