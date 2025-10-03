from playwright.sync_api import sync_playwright
from playwright_stealth import stealth
import os, sys, time

ud = (
    os.path.expanduser("~/Library/Application Support/Google/Chrome Beta") if sys.platform == "darwin" else
    os.path.join(os.environ.get("LOCALAPPDATA",""), "Google", "Chrome Beta", "User Data") if sys.platform.startswith("win") else
    (os.path.expanduser("~/.config/google-chrome-beta") if os.path.exists(os.path.expanduser("~/.config/google-chrome-beta")) else os.path.expanduser("~/.config/google-chrome"))
)

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        ud,
        channel="chrome-beta",
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        ignore_default_args=["--enable-automation"],
    )
    page = ctx.new_page(); stealth(page)
    page.goto("https://example.com")
    print(f"Using real profile: {ud}. Ctrl+C to exit.")
    try:
        while True: time.sleep(3600)
    except KeyboardInterrupt:
        pass
    ctx.close()
