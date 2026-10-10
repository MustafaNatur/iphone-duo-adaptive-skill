# App Store Assets

## Requirements

- **From April 2027**, every new App Store submission must include **iPhone Duo screenshots** (Apple Developer News, 2026-10-05).
- **From April 2027**, apps must be built with the iOS 27 SDK or later.
- Until then, App Store Connect falls back to scaled large-iPhone screenshots.

## Screenshot specifications

| Display | Portrait | Landscape |
|---|---|---|
| Outer | 1398 × 2034 px | 2034 × 1398 px |
| Inner | 2007 × 2853 px | 2853 × 2007 px |

1–10 screenshots per size; `.png`, `.jpg` or `.jpeg`; **no alpha channel or transparency**. Re-check the current values on Apple's "Screenshot specifications" page before submitting; they can change.

App previews (video) have their own specs on Apple's "App preview specifications" page; this skill doesn't produce videos.

## Workflow

1. Ask which screens and orientations (decision Q14). Default: root screen of each tab, portrait, both displays.
2. Prepare clean state: sample data, no debug overlays, a clean status bar:
   ```bash
   xcrun simctl status_bar "$UDID" override --time "9:41" --batteryState charged --batteryLevel 100 --cellularBars 4 --wifiBars 3
   ```
   (Clear afterwards with `xcrun simctl status_bar "$UDID" clear`.)
3. Capture per display and pose with `simctl io … screenshot` (see `simulator.md`) into `DuoAdaptive/appstore/`.
4. Validate:
   ```bash
   python3 <skill>/scripts/check_screenshots.py DuoAdaptive/appstore
   ```
   It checks dimensions against the table above, format, and alpha. If the raw simulator capture size differs from the spec, report it — **don't stretch**. Offer to scale proportionally only if the aspect ratio matches exactly, and remove alpha by flattening onto an opaque background.
5. Tell the user where the files are and that uploading happens in App Store Connect (Media Manager), which also has a new iPhone Duo preview tool. Never sign in to App Store Connect for the user.

## Optional

- Apple's "App Store asset best practices" page has design templates for iPhone Duo product-page assets.
- Developers can mention iPhone Duo optimization in a featuring nomination.
