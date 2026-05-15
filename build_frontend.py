"""
build_frontend.py
Cross-references E:\Dummy\rag folders 1-12 and assembles a fully wired frontend
with correct navigation links matching the design screenshots.
"""
import shutil, re, os

SRC = r"E:\Dummy\rag"
DST = r"e:\project\enterprise-rag\frontend"

# Mapping: folder number -> destination filename
MAPPING = {
    1:  "index.html",
    2:  "admin-login.html",
    3:  "admin-login-error.html",
    4:  "sectors.html",
    5:  "secure-login.html",
    6:  "secure-login-error.html",
    7:  "admin-command.html",
    8:  "system-health.html",
    9:  "access-control.html",
    10: "source-vault.html",
    11: "hyperparameters.html",
    12: "terminal.html",
}

# Sidebar nav links for admin pages (7,8,9,10,11)
ADMIN_NAV = {
    "hyperparameters": "hyperparameters.html",
    "query terminal":  "terminal.html",
    "source vault":    "source-vault.html",
    "system health":   "system-health.html",
    "access control":  "access-control.html",
}

# ── Step 1: copy raw source files ──────────────────────────────────────────
# ── Step 0: Clean all existing HTML files in frontend ─────────────────────
os.makedirs(DST, exist_ok=True)
for old_file in os.listdir(DST):
    if old_file.endswith(".html"):
        os.remove(os.path.join(DST, old_file))
        print(f"  Removed old file: {old_file}")
print("  Frontend directory cleaned.")
for num, fname in MAPPING.items():
    src_file = os.path.join(SRC, str(num), "code.html")
    dst_file = os.path.join(DST, fname)
    shutil.copy2(src_file, dst_file)
    print(f"  Copied {num}/code.html -> {fname}")

# ── Step 2: patch navigation links ────────────────────────────────────────
def patch(filepath, replacements):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    for old, new in replacements:
        html = html.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

# ── index.html (folder 1) ─────────────────────────────────────────────────
# Landing page has two clickable cards; folder 1 has href="#" for both.
# We need to wire Enterprise User -> sectors.html and System Administrator -> admin-login.html
patch(os.path.join(DST, "index.html"), [
    # The two cards in the landing page point to href="#"
    # Card 1 (Enterprise User) - first occurrence
    ('href="#"\n', 'href="#"\n', ),   # placeholder - use regex below
])
with open(os.path.join(DST, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()
# Replace first href="#" that contains "Enterprise User" context
html = re.sub(
    r'(<a[^>]*class="[^"]*"[^>]*href=")#("[^>]*>(?:(?!</a>).)*?Enterprise User)',
    r'\1sectors.html\2',
    html, count=1, flags=re.DOTALL
)
html = re.sub(
    r'(<a[^>]*class="[^"]*"[^>]*href=")#("[^>]*>(?:(?!</a>).)*?System Administrator)',
    r'\1admin-login.html\2',
    html, count=1, flags=re.DOTALL
)
with open(os.path.join(DST, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched index.html navigation")

# ── admin-login.html (folder 2) ───────────────────────────────────────────
# Authorize Access button -> admin-command.html
with open(os.path.join(DST, "admin-login.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace(
    'type="button">\n                    Authorize Access',
    'type="button" onclick="window.location.href=\'admin-command.html\'">\n                    Authorize Access'
)
with open(os.path.join(DST, "admin-login.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched admin-login.html")

# ── admin-login-error.html (folder 3) ─────────────────────────────────────
with open(os.path.join(DST, "admin-login-error.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace(
    'type="button">\n                    Authorize Access',
    'type="button" onclick="window.location.href=\'admin-login.html\'">\n                    Authorize Access'
)
with open(os.path.join(DST, "admin-login-error.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched admin-login-error.html")

# ── sectors.html (folder 4) ───────────────────────────────────────────────
# All department cards point to secure-login.html
with open(os.path.join(DST, "sectors.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace('href="#"', 'href="secure-login.html"')
with open(os.path.join(DST, "sectors.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched sectors.html")

# ── secure-login.html (folder 5) ──────────────────────────────────────────
with open(os.path.join(DST, "secure-login.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace(
    'type="button">\n<span class="relative z-10 flex items-center justify-center gap-2">\n                        Initialize Session',
    'type="button" onclick="window.location.href=\'terminal.html\'">\n<span class="relative z-10 flex items-center justify-center gap-2">\n                        Initialize Session'
)
with open(os.path.join(DST, "secure-login.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched secure-login.html")

# ── secure-login-error.html (folder 6) ───────────────────────────────────
with open(os.path.join(DST, "secure-login-error.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = html.replace(
    'type="button">\n<span class="relative z-10 flex items-center justify-center gap-2">\n                        Initialize Session',
    'type="button" onclick="window.location.href=\'secure-login.html\'">\n<span class="relative z-10 flex items-center justify-center gap-2">\n                        Initialize Session'
)
with open(os.path.join(DST, "secure-login-error.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched secure-login-error.html")

# ── Helper: wire sidebar links in admin pages ─────────────────────────────
SIDEBAR_NAV_MAP = [
    # (text_pattern, new_href)
    ("Hyperparameters",          "hyperparameters.html"),
    ("Query Terminal",           "terminal.html"),
    ("Source Vault",             "source-vault.html"),
    ("System Health",            "system-health.html"),
    ("Access Control and Logs",  "access-control.html"),
    ("Access Control",           "access-control.html"),
    ("Neural Mesh",              "hyperparameters.html"),
]

def wire_sidebar(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    def replace_href(match):
        full_tag = match.group(0)
        inner    = match.group(1)   # content between > and </a>
        for label, dest in SIDEBAR_NAV_MAP:
            if label.lower() in inner.lower():
                return re.sub(r'href="[^"]*"', f'href="{dest}"', full_tag, count=1)
        return full_tag

    html = re.sub(r'<a\b[^>]*>(.*?)</a>', replace_href, html, flags=re.DOTALL)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

for num in [7, 8, 9, 10, 11]:
    fname = MAPPING[num]
    wire_sidebar(os.path.join(DST, fname))
    print(f"  Wired sidebar in {fname}")

# ── terminal.html (folder 12): wire chat to backend ───────────────────────
with open(os.path.join(DST, "terminal.html"), "r", encoding="utf-8") as f:
    html = f.read()

# Add IDs to input and send button
html = html.replace(
    'placeholder="Enter command or query..." type="text">',
    'id="chat-input" placeholder="Enter command or query..." type="text">'
)
html = html.replace(
    '<button class="p-2 text-primary-container hover:text-primary-fixed transition-colors flex items-center justify-center bg-surface-container-high rounded hover:bg-surface-variant/50">\n<span class="material-symbols-outlined">send</span>',
    '<button id="chat-send" class="p-2 text-primary-container hover:text-primary-fixed transition-colors flex items-center justify-center bg-surface-container-high rounded hover:bg-surface-variant/50">\n<span class="material-symbols-outlined">send</span>'
)

# Inject JS before </body>
CHAT_JS = """
<script>
const chatInput = document.getElementById('chat-input');
const chatSend  = document.getElementById('chat-send');
const chatArea  = document.querySelector('.flex-1.overflow-y-auto');

async function sendQuery() {
    const q = chatInput.value.trim();
    if (!q) return;
    chatInput.value = '';

    // User bubble
    const user = document.createElement('div');
    user.className = 'flex flex-col items-end gap-2 w-full max-w-3xl ml-auto';
    user.innerHTML = `
        <div class="flex items-center gap-3 mb-1">
            <span class="font-label-sm text-label-sm text-on-surface-variant">OPERATOR</span>
            <span class="material-symbols-outlined text-on-surface-variant text-sm">person</span>
        </div>
        <div class="bg-surface-container-high border border-outline-variant/30 rounded-xl rounded-tr-sm p-4 text-on-surface font-body-md text-body-md">${q}</div>`;
    chatArea.appendChild(user);
    chatArea.scrollTop = chatArea.scrollHeight;

    try {
        const res  = await fetch('/query', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({question:q, department:'Intelligence Dept'}) });
        const data = await res.json();
        let srcHtml = '';
        if (data.chunks) {
            srcHtml = '<div class="border-t border-outline-variant/30 pt-3 flex flex-wrap items-center gap-2"><span class="font-label-sm text-label-sm text-on-surface-variant mr-2">SOURCES:</span>';
            data.chunks.forEach(c => { srcHtml += `<div class="flex items-center gap-1 bg-surface-container px-2 py-1 border border-outline-variant/50 rounded-sm"><span class="font-mono text-[11px] text-on-surface">${c.node_id}</span></div>`; });
            srcHtml += '</div>';
        }
        const ai = document.createElement('div');
        ai.className = 'flex flex-col items-start gap-2 w-full max-w-4xl mr-auto';
        ai.innerHTML = `
            <div class="flex items-center gap-3 mb-1">
                <span class="material-symbols-outlined text-primary-container text-sm">smart_toy</span>
                <span class="font-label-sm text-label-sm text-primary-container">AEGIS SYNTHESIS</span>
            </div>
            <div class="glass-container rounded-xl rounded-tl-sm p-6 w-full">
                <p class="font-body-md text-body-md text-on-surface mb-4 leading-relaxed">${data.answer || 'No response.'}</p>
                ${srcHtml}
            </div>
            <span class="font-mono text-[10px] text-outline tracking-wider mt-1">LATENCY: ${data.latency_ms||0}ms</span>`;
        chatArea.appendChild(ai);
        chatArea.scrollTop = chatArea.scrollHeight;
    } catch(e) { console.error(e); }
}

chatSend.addEventListener('click', sendQuery);
chatInput.addEventListener('keypress', e => { if (e.key==='Enter') sendQuery(); });
</script>
"""
html = html.replace('</body>', CHAT_JS + '</body>')

with open(os.path.join(DST, "terminal.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("  Patched terminal.html with chat JS")

print("\n✅ Frontend build complete! All 12 pages assembled and wired.")
