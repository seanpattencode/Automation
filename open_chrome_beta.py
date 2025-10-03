from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import os, sys, time, subprocess, shutil, tempfile

ud = (
    os.path.expanduser("~/Library/Application Support/Google/Chrome Beta") if sys.platform == "darwin" else
    os.path.join(os.environ.get("LOCALAPPDATA",""), "Google", "Chrome Beta", "User Data") if sys.platform.startswith("win") else
    (os.path.expanduser("~/.config/google-chrome-beta") if os.path.exists(os.path.expanduser("~/.config/google-chrome-beta")) else os.path.expanduser("~/.config/google-chrome"))
)

# Close any existing Chrome Beta instances
subprocess.run(["pkill", "-9", "-f", "chrome-beta"], stderr=subprocess.DEVNULL)
time.sleep(1)

# Create temp directory with profile copy
print("Copying profile to temp directory...")
temp_profile = os.path.join(tempfile.gettempdir(), "chrome-beta-profile")
if os.path.exists(temp_profile):
    shutil.rmtree(temp_profile, ignore_errors=True)

# Copy critical profile data (Default directory with cookies, history, etc.)
os.makedirs(temp_profile, exist_ok=True)
default_dir = os.path.join(ud, "Default")
if os.path.exists(default_dir):
    shutil.copytree(default_dir, os.path.join(temp_profile, "Default"), dirs_exist_ok=True)

# Copy Local State (preferences)
local_state = os.path.join(ud, "Local State")
if os.path.exists(local_state):
    shutil.copy2(local_state, temp_profile)

print("Launching browser with profile...")
with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        temp_profile,
        channel="chrome-beta",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--enable-features=UseOzonePlatform",
            "--ozone-platform=wayland",
        ],
        ignore_default_args=["--enable-automation"],
    )

    page = ctx.new_page()

    print("Applying stealth...")
    stealth = Stealth()
    stealth.apply_stealth_sync(page)

    print("Navigating to pixai.art...")
    try:
        page.goto("https://pixai.art/", wait_until="domcontentloaded", timeout=60000)
        print(f"Navigated to https://pixai.art/")
    except Exception as e:
        print(f"Navigation error: {e}")

    print(f"Using copied profile from: {ud}. Ctrl+C to exit.")
    try:
        while True: time.sleep(3600)
    except KeyboardInterrupt:
        pass

    ctx.close()

# Clean up
print("Cleaning up temp profile...")
shutil.rmtree(temp_profile, ignore_errors=True)
