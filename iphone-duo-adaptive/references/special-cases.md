# Special Cases

Load the section that applies.

## Games

Apple's iPhone Duo guidance for games is limited to the HIG:
- Make the game playable in every pose. Locking to portrait or landscape is allowed, but fill the screen as the pose changes.
- Keep text and control sizes as consistent as possible when resizing.
- Prefer changing the aspect ratio over letterboxing/pillarboxing; if unavoidable, put artwork in the padding.

Do:
- Make the render surface follow the view/scene size (e.g. resize the drawable on layout, SpriteKit `scaleMode` that adapts, re-layout HUD with safe areas).
- Keep HUD/touch controls out of reserved regions and safe areas.

Don't invent guidance for Metal drawable handling, GameController, or touch-control overlays on iPhone Duo — it isn't documented. Flag and recommend testing on hardware.

## Hinge-driven effects

Use `onHingeChange` (SwiftUI) or `UIHingeInteraction` (UIKit) only for **live interactions** (e.g. a pitch bend, a parallax effect, a lid-angle readout). Never for layout. Handle `context.hinge == nil` (no hinge) and gate for iOS 27.1. Only add hinge effects if the user asks.

```swift
.onHingeChange { _, context in
    if let hinge = context.hinge, hinge.status == .partiallyOpen {
        effectAmount = amount(for: hinge.angle)
    } else {
        effectAmount = 0
    }
}
```

## Multiwindow & Split View multitasking

- All resizable apps take part in Split View on the inner display; the bars of each app sit on its outer edge, so safe areas are asymmetric (`resizing-task.md` §7).
- New windows can be created only on the inner display. `UIWindowScene.ActivationAction` hides itself when unavailable; always handle errors from scene requests.
- If the app doesn't support multiple scenes and the user wants it, follow Apple's "Bringing multiple windows to your SwiftUI app" / "Supporting multiple windows on iPad" samples. This is a feature, not a fix: ask first.

## State across fold / unfold

Folding changes the window size and possibly the display, not the scene. Check in captures that:
- Navigation stack, selection, scroll position, text field contents and sheet state survive.
- No view model is recreated because a view identity depends on size class.
If state is lost, fix the identity (`@State`/`@StateObject` placement, `.id(…)` keyed to size) rather than adding persistence.

## Sheets, popovers, keyboard

- System sheets/popovers/alerts move away from the fold automatically.
- Keyboard interaction with the fold is undocumented; keep using `keyboardLayoutGuide` / safe areas and flag custom keyboard-anchored UI for hardware testing.

## Widgets, Live Activities, Dynamic Island, App Clips, extensions

No iPhone Duo–specific guidance has been published. Most app extensions can't run in the iPhone Duo simulator. Leave them unchanged unless they use the same resizing anti-patterns; list them under "Test on a physical iPhone Duo".

## Cross-platform apps

Flutter, React Native, Capacitor, .NET MAUI and web wrappers are out of scope. Say so and stop, or limit work to native host code (e.g. a native `SceneDelegate`) if the user asks.
