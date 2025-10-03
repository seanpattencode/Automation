# Automation Scripts

## Troubleshooting

### Chrome Beta Script Not Opening Website

If the script launches Chrome Beta but doesn't navigate to the website, check the following:

#### 1. Wayland Display Server
If you're running on Wayland (check with `echo $XDG_SESSION_TYPE`), Chrome needs specific flags:
```python
args=[
    "--enable-features=UseOzonePlatform",
    "--ozone-platform=wayland",
]
```

#### 2. Persistent Context vs Regular Launch
Using `launch_persistent_context()` with an existing Chrome profile can fail if:
- Chrome Beta is already running with that profile
- The profile is locked by another process

**Solution**: Use regular `launch()` instead:
```python
browser = p.chromium.launch(
    channel="chrome-beta",
    headless=False,
    args=[...],
)
ctx = browser.new_context()
page = ctx.new_page()
```

#### 3. playwright_stealth Usage
The correct way to use playwright_stealth is:
```python
from playwright_stealth import Stealth

stealth = Stealth()
stealth.apply_stealth_sync(page)
```

Not `stealth(page)` or `stealth_sync(page)`.

#### 4. Killing Chrome Processes
To kill only Chrome Beta (not regular Chrome):
```bash
pkill -9 -f chrome-beta
```

Not `pkill -9 chrome` which kills all Chrome instances.
