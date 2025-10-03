from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import os, sys, time, subprocess

ud = (
    os.path.expanduser("~/Library/Application Support/Google/Chrome Beta") if sys.platform == "darwin" else
    os.path.join(os.environ.get("LOCALAPPDATA",""), "Google", "Chrome Beta", "User Data") if sys.platform.startswith("win") else
    (os.path.expanduser("~/.config/google-chrome-beta") if os.path.exists(os.path.expanduser("~/.config/google-chrome-beta")) else os.path.expanduser("~/.config/google-chrome"))
)

# Close any existing Chrome Beta instances
subprocess.run(["pkill", "-9", "-f", "chrome-beta"], stderr=subprocess.DEVNULL)
time.sleep(1)

print("Launching browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="chrome-beta",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--enable-features=UseOzonePlatform",
            "--ozone-platform=wayland",
        ],
    )
    print("Browser launched, creating context...")
    ctx = browser.new_context()
    page = ctx.new_page()
    print("Applying stealth...")
    stealth = Stealth()
    stealth.apply_stealth_sync(page)
    try:
        page.goto("https://pixai.art/", wait_until="domcontentloaded", timeout=60000)
        print(f"Navigated to https://pixai.art/")
    except Exception as e:
        print(f"Navigation error: {e}")
    print("Browser ready. Ctrl+C to exit.")
    try:
        while True: time.sleep(3600)
    except KeyboardInterrupt:
        pass
    browser.close()