# Availability & SDK Gating

**SDK Version:** iOS 27.1

iPhone Duo APIs (vertical bars, reserved regions, arrangements, hinge, scene accessories, direction coordinator) need the **iOS 27.1 SDK** to compile and **iOS 27.1** to run. A few related APIs (`visibilityPriority`, `ToolbarOverflowMenu`, `topBarPinnedTrailing`, `presentationPlacement`) are **iOS 27.0** — gate each API with the version in `api-facts.md`, confirmed against the SDK.

## Rules

1. Don't raise the deployment target unless the user chose it (decision Q2). Default: keep it and gate.
2. Gate every iPhone Duo API at run time.
3. Keep the old code path; never delete it to make room for the new one.
4. Preserve existing `#available` / `respondsToSelector:` guards around the code you touch.
5. After changes, build for the minimum deployment target and run on an older simulator if one is installed.

## Run-time gating

```swift
// PREFER: gate the modifier, keep the old view
extension View {
    @ViewBuilder
    func duoVerticalBarsDisabled() -> some View {
        if #available(iOS 27.1, *) {
            self.toolbarVerticalBehavior(.disabled)
        } else {
            self
        }
    }
}
```

```swift
// PREFER: gate a container swap
var body: some View {
    if #available(iOS 27.1, *) {
        ArrangementView { PlayerView() } secondary: { UpNextView() }
    } else {
        VStack { PlayerView(); UpNextView() }   // existing layout, unchanged
    }
}
```

```swift
// UIKit
override func viewDidLayoutSubviews() {
    super.viewDidLayoutSubviews()
    if #available(iOS 27.1, *) {
        let folds = view.reservedRegions(kind: .division)
        layoutAvoiding(folds.map(\.frame))
    } else {
        layoutAvoiding([])
    }
}
```

```objc
// Objective-C
if (@available(iOS 27.1, *)) {
    // iPhone Duo API
}
```

Mark new helper types/extensions that only make sense on 27.1 with `@available(iOS 27.1, *)`.

## Compile-time (SDK) gating

Run-time checks don't help if the project must **also** build with an Xcode older than 27.1 (e.g. CI pinned to Xcode 27.0): the symbols won't exist.

Ask the user (part of Q2) whether any build environment uses older Xcode. If yes:
- Recommended: update CI to Xcode 27.1.
- Otherwise: put iPhone Duo code in dedicated files and wrap it in a custom compilation condition (e.g. `#if DUO_SDK`), set `SWIFT_ACTIVE_COMPILATION_CONDITIONS = DUO_SDK` only in configurations built with Xcode 27.1. Tell the user exactly what you set.

Don't guess a `#if compiler(>=X)` version for the 27.1 toolchain; check `xcrun swift --version` first if you want to use it.

## Info.plist

Don't add, remove or change `UIRequiresFullScreen`, `UISupportedInterfaceOrientations` or `UIApplicationSceneManifest` without the user's agreement. In particular, **don't unlock landscape app-wide to "support" iPhone Duo**: the inner display already ignores `supportedInterfaceOrientations`, so unlocking only changes every other iPhone. Make the layout work in landscape (the inner display will show it) and leave the setting alone. Scene-lifecycle migration belongs to Apple's `uikit-app-modernization` skill (or `resizing-task.md` §4).
