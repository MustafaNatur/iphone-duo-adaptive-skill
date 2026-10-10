# Task: Resizing Fundamentals (fallback)

**SDK Version:** iOS 27 (all APIs here predate iOS 27.1)

## Overview

Use §1–8 **only when Apple's `uikit-app-modernization` / App Resizability skill isn't available** (see `apple-skills-bridge.md`), or for SwiftUI code those skills don't cover. **§9 (layout repairs) always applies**, in every mode. It removes assumptions that the app has one fixed screen, one orientation, or runs on a specific device.

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
| Sizes derived from width (`width / 2`, `aspectRatio(1, …)`, `containerRelativeFrame`) | `width-derived-size` (review → §9) |

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
For hero images/video using fill modes, choose fill vs. fit by aspect ratio or size class so important content isn't cropped on the wide outer display or the near-square inner display. If it crops important content in a capture, it's a layout repair (§9); otherwise flag.

### 9. Layout repairs (apply without a decision)

An existing design that breaks at iPhone Duo sizes is a bug, not a design question. Repair it so the **same design** works at every size, and keep compact-width iPhones pixel-identical.

Find them by reading layout code for sizes derived from width (`width / 2`, `aspectRatio(1, …)` on width-filling views, `containerRelativeFrame` fractions, `GeometryReader` math) and by checking baseline captures on the inner display (regular × regular, roughly 1.4:1) and in landscape.

| Breakage | Repair |
|---|---|
| Element sized from width grows until it pushes the main content off screen (e.g. square header tiles at half width) | Cap its height/size (`.frame(maxHeight:)`, `min(width/2, cap)`) or switch the aspect ratio when the container is wide; compact layout unchanged |
| Text or forms stretched across the inner display | Readable width: `.frame(maxWidth: 600)` centered, or `readableContentGuide` in UIKit |
| Content cropped by fill mode | Choose fit vs. fill by the container's aspect ratio |
| Fixed-size elements leave large empty areas | Let them flex (flexible frames, `GridItem(.adaptive)`), no new structure |
| Controls under the fold or a camera | `reserved-regions-task.md` |
| Zoom/scroll state that becomes invalid after a size change | Reset or clamp on size change |

```swift
// AVOID: square tiles at half the width — fine on iPhone, huge on the inner display
HStack { SpendingTile(); PlacesTile() }
    .frame(height: proxy.size.width / 2)
// PREFER: same design, bounded
HStack { SpendingTile(); PlacesTile() }
    .frame(height: min(proxy.size.width / 2, 220))   // 220 ≥ today's largest iPhone value → compact unchanged
```

Choose caps at or above today's largest compact-iPhone value so normal iPhones don't change. Not a repair (needs a decision): moving content into a second column, new navigation, a sidebar, an arrangement.

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
