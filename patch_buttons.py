"""Patch all button-based navigation across the frontend."""
import os, re

DST = r"e:\project\enterprise-rag\frontend"

def patch_buttons(filepath, replacements):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    for old, new in replacements:
        if old in html:
            html = html.replace(old, new, 1)
            print(f"    [OK] Patched in {os.path.basename(filepath)}")
        else:
            print(f"    [MISS] Pattern not found in {os.path.basename(filepath)}: {old[:60]}")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

# ── admin-login.html: Authorize Access -> admin-command.html ───────────────
with open(os.path.join(DST, "admin-login.html"), "r", encoding="utf-8") as f:
    html = f.read()

# Replace ANY submit-style button containing "Authorize Access"
html = re.sub(
    r'(<button\b[^>]*type="button"[^>]*>)\s*\n\s*Authorize Access',
    lambda m: m.group(1).replace('type="button"', 'type="button" onclick="window.location.href=\'admin-command.html\'"') + '\n                    Authorize Access',
    html
)
with open(os.path.join(DST, "admin-login.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Patched admin-login.html")

# ── admin-login-error.html: Authorize Access -> admin-login.html ───────────
with open(os.path.join(DST, "admin-login-error.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = re.sub(
    r'(<button\b[^>]*type="button"[^>]*>)\s*\n\s*Authorize Access',
    lambda m: m.group(1).replace('type="button"', 'type="button" onclick="window.location.href=\'admin-login.html\'"') + '\n                    Authorize Access',
    html
)
with open(os.path.join(DST, "admin-login-error.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Patched admin-login-error.html")

# ── secure-login.html: Initialize Session -> terminal.html ────────────────
with open(os.path.join(DST, "secure-login.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = re.sub(
    r'(<button\b[^>]*type="button"[^>]*>)',
    lambda m: m.group(1).replace('type="button"', 'type="button" onclick="window.location.href=\'terminal.html\'"') if 'onclick' not in m.group(1) else m.group(1),
    html, count=1
)
with open(os.path.join(DST, "secure-login.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Patched secure-login.html")

# ── secure-login-error.html: Initialize Session -> secure-login.html ──────
with open(os.path.join(DST, "secure-login-error.html"), "r", encoding="utf-8") as f:
    html = f.read()
html = re.sub(
    r'(<button\b[^>]*type="button"[^>]*>)',
    lambda m: m.group(1).replace('type="button"', 'type="button" onclick="window.location.href=\'secure-login.html\'"') if 'onclick' not in m.group(1) else m.group(1),
    html, count=1
)
with open(os.path.join(DST, "secure-login-error.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("Patched secure-login-error.html")

# ── Verify all patches applied ────────────────────────────────────────────
print("\nVerification:")
for fname in ["admin-login.html", "admin-login-error.html", "secure-login.html", "secure-login-error.html", "index.html"]:
    with open(os.path.join(DST, fname), "r", encoding="utf-8") as f:
        content = f.read()
    count = content.count("onclick")
    print(f"  {fname}: {count} onclick(s) found")
