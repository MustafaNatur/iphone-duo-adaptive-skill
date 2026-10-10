# Task: Resizing Fundamentals (fallback)

**SDK Version:** iOS 27 (all APIs here predate iOS 27.1)

## Overview

Use this task **only when Apple's `uikit-app-modernization` / App Resizability skill isn't available** (see `apple-skills-bridge.md`), or for SwiftUI code those skills don't cover. It removes assumptions that the app has one fixed screen, one orientation, or runs on a specific device.

## Detection

`scripts/audit.py` flags these; confirm each by reading the code:

| Pattern | Rule id |
|---|---|
| `UIScreen.main`, `UIScreen.mainScreen`, `[UIScreen mainScreen]` | `uiscreen-main` |
| `UIWindow(frame: UIScreen.main.bounds)` | `window-frame` |
| `UIDevice.current.orientation`, `statusBarOrientation`, `interfaceOrientation` | `orientation` |
| `userInterfaceIdiom == .phone/.pad` used for layout | `idiom` |
| Comparisons with device sizes (`== 844`, `height > 900`) | `fixed-size` |
| `safeAreaInsets.left * 2`, `.right * 2` | `symmetric-safe-area` |
| `AppDelegate` with `window` and no `SceneDelegate` / `UIApplicationSceneManifest` | `app-lifecycle` |
| `.scaleAspectFill` / `.aspectRatio(contentMode: .fill)` on hero media | `full-bleed` (review only) |

## Patterns

### 1. Size from the view, not the screen
```swift
// AVOID
let width = UIScreen.main.bounds.width
// PREFER (UIKit, inside a view/view controller)
let width = view.bounds.width            // re-read in viewDidLayoutSubviews / layoutSubviews
// PREFER (SwiftUI)
.onGeometryChange(for: CGFloat.self) { $0.size.width } action: { width = $0 }
```
Do size-dependent work in `layoutSubviews` / `viewDidLayoutSubviews`; use `viewWillTransition(to:with:)` for work that must run on size change.

### 2. Scale from traits
```swift
// AVOID
let scale = UIScreen.main.scale
// PREFER
let scale = traitCollection.displayScale          // UIKit
@Environment(\.displayScale) private var scale    // SwiftUI
```

### 3. Windows from scenes
```swift
// AVOID
window = UIWindow(frame: UIScreen.main.bounds)
// PREFER (in scene(_:willConnectTo:options:))
guard let windowScene = scene as? UIWindowScene else { return }
window = UIWindow(windowScene: windowScene)
```
Never store a `UIScreen`; read `view.window?.windowScene?.screen` when you truly need one.

### 4. Scene lifecycle
If the app still uses app-delegate-only lifecycle, migration is required for resizing. Follow TN3187 ("Migrating to the UIKit scene-based life cycle"). This is a structural change: **ask the user first** and keep it as its own commit-sized step.

### 5. Orientation → available space
```swift
// AVOID
if UIDevice.current.orientation.isLandscape { useTwoColumns() }
// PREFER
if view.bounds.width > view.bounds.height { useTwoColumns() }
// or, for "is there room?" decisions
if traitCollection.horizontalSizeClass == .regular { useTwoColumns() }
```
If left-vs-right matters (e.g. camera), ask the user; that's not a pure layout decision.

### 6. Idiom and device-size checks → size classes / space
```swift
// AVOID
if UIDevice.current.userInterfaceIdiom == .pad { showSidebar() }
if view.bounds.height == 844 { compactHeader() }
// PREFER
if traitCollection.horizontalSizeClass == .regular { showSidebar() }
if view.bounds.height < 700 { compactHeader() }   // threshold from design, not a device
```
Don't treat regular width as "iPad": the iPhone Duo inner display is regular × regular.

Keep idiom checks that are **not** layout (e.g. feature availability, analytics); note them in the report.

### 7. Asymmetric safe areas
```swift
// AVOID
let contentWidth = view.bounds.width - view.safeAreaInsets.left * 2
// PREFER
let contentWidth = view.bounds.inset(by: view.safeAreaInsets).width
```
Foreground controls stay inside the safe area; backgrounds may extend edge to edge (`.ignoresSafeArea()` / `backgroundView.frame = view.bounds`).

### 8. Full-bleed media
For hero images/video using fill modes, choose fill vs. fit by aspect ratio or size class so important content isn't cropped on the wide outer display or the near-square inner display. Flag; change only with a decision.

## Implementation Gates

- The line contains the targeted pattern (no off-target edits).
- The replacement is dynamic (no literals substituted for screen values).
- Existing guards and branches are preserved.
- No shared global (`UIApplication.shared`, `UIDevice.current`, `UIScreen.main`) introduced as a replacement.

## Post-file Checklist

- [ ] File builds.
- [ ] Every flagged occurrence handled (changed / TODO with reason / not layout-related with reason).
- [ ] No formatting churn.

## Final Verification

Rebuild; recapture closed and open poses; the app fills each display without letterboxing and nothing is clipped.

## API Reference

See `api-facts.md` → Layout & resizing.
