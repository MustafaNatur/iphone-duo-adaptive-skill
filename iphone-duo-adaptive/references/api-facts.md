# Verified API Facts

**SDK Version:** iOS 27.1 (Xcode 27.1). Checked against Apple's documentation, the "SwiftUI updates" / "UIKit updates" pages, and Apple's iPhone Duo Tech Talks, as of 2026-10-10.

Use only symbols from this file, from Apple skills exported this session, or from SDK headers you grep. When unsure of an exact signature, grep the SDK:

```bash
SDK=$(xcrun --sdk iphonesimulator --show-sdk-path)
grep -rn "reservedRegions" "$SDK/System/Library/Frameworks/UIKit.framework/Headers" | head
find "$SDK/System/Library/Frameworks/SwiftUI.framework" -name "*.swiftinterface" | head -1 | xargs grep -n "ArrangementView" | head
```

---

## Device facts

- Outer display: compact width; behaves like a regular iPhone; honors `supportedInterfaceOrientations`.
- Inner display: regular width **and** regular height; does **not** honor `supportedInterfaceOrientations`.
- Outer front camera: always an occlusion reserved region (top corner, expands into the Dynamic Island for Live Activities).
- Inner front camera: hidden under the display; an occlusion reserved region only while the camera is active.
- Fold: a division reserved region, **active only when partially open** (book/tabletop); inactive when flat.
- Vertical bars: on the outer display and on the inner display in landscape, navigation bars, toolbars and tab bars move to one side. Inner display portrait keeps horizontal bars.
- Split View multitasking: two apps on the inner display; each app puts its bars on its outer edge.
- New windows (scenes) can be opened only on the inner display.
- `UIRequiresFullScreen`: the iPhone Duo talk says it's still honored and the app still resizes on open/close. Other sources say iOS 27 changed it to discrete resizing. **Unverified — don't rely on it; don't add or remove it without asking.**

### What each build SDK gets
| Built with | On iPhone Duo |
|---|---|
| iOS 26 SDK or earlier | Centered, iPhone-sized; black space on the inner display |
| iOS 27 SDK | Fills most of the inner display; avoids the status bar edge |
| iOS 27.1 SDK | Edge to edge; vertical bars; reserved regions, arrangements, hinge |

---

## Layout & resizing (all iOS versions)

| Need | SwiftUI | UIKit |
|---|---|---|
| Available size | `GeometryReader`, `onGeometryChange(for:of:action:)` | `view.bounds`, `superview.bounds`, `viewWillTransition(to:with:)`, `layoutSubviews`, `viewDidLayoutSubviews` |
| Size classes | `@Environment(\.horizontalSizeClass)`, `\.verticalSizeClass` | `traitCollection.horizontalSizeClass`, `.verticalSizeClass`; `registerForTraitChanges` / automatic trait tracking |
| Display scale | `@Environment(\.displayScale)` | `traitCollection.displayScale` |
| Screen (if truly needed) | — | `view.window?.windowScene?.screen` (never store it) |
| Window creation | — | `UIWindow(windowScene:)` |
| Safe area | `GeometryProxy.safeAreaInsets` | `view.safeAreaInsets`, `safeAreaLayoutGuide`; width = `bounds.inset(by: safeAreaInsets).width` (never `left * 2`) |
| Corners | `ConcentricRectangle` | `UICornerConfiguration` |
| Sidebar for tabs | `TabView { … }.defaultTabBarPlacement(.sidebar)` | `tabBarController.sidebar.preferredPlacement = .sidebar` |
| List → detail | `NavigationSplitView` | `UISplitViewController` |

**Don't use for layout:** `UIScreen.main` (bounds, scale), `UIDevice.current.orientation`, `statusBarOrientation`, `interfaceOrientation` (incl. `windowScene.effectiveGeometry.interfaceOrientation`), `userInterfaceIdiom`, hard-coded sizes (`== 844`), "regular width ⇒ iPad".

---

## Vertical bars

Availability below was checked against the installed iOS 27.0 SDK (`@available` in the SwiftUI `.swiftinterface`, `API_AVAILABLE` in UIKit headers). **Gate with the version in the column, not a blanket 27.1.** "27.1" = not in the 27.0 SDK (from Apple's 27.1 docs).

| Purpose | SwiftUI | UIKit | Available |
|---|---|---|---|
| Opt a view out | `.toolbarVerticalBehavior(.disabled)` | `override var preferredVerticalBarBehavior: UIVerticalBarBehavior { .disabled }` | 27.1 |
| Which edge (nil = none) | `@Environment(\.toolbarVerticalEdge)` | `traitCollection.verticalBarEdge` | 27.1 |
| Compression | `.toolbarVerticalCompressionBehavior(.automatic / .prefersTabBar / .prefersToolbarItems)` | `UIVerticalBarCompressionBehavior` | 27.1 |
| Item axis | `.axisBehavior(.horizontalOnly / .verticalPreferred)` (`ToolbarItemAxisBehavior`) | `UIBarButtonItem.axisBehavior` | 27.1 |
| Overflow order | `.visibilityPriority(…)` (`ToolbarItemVisibilityPriority`, e.g. `.high`) | `UIBarButtonItem.visibilityPriority` (`UIBarButtonItemVisibilityPriority`) | **27.0** |
| Put items in system overflow | `ToolbarOverflowMenu { … }` | `navigationItem.additionalOverflowItems` | **27.0** / UIKit 16.0 |
| Prominent pinned action (Done) | `ToolbarItem(placement: .topBarPinnedTrailing)` | `navigationItem.pinnedTrailingGroup` | **27.0** / UIKit 16.0 |
| Custom Back/Close | `ToolbarItem(placement: .cancellationAction)` | `navigationItem.leadingItemGroups` | long-standing |
| Groups / spacing | `ToolbarItemGroup`, `ToolbarSpacer` (26.0) | `UIBarButtonItemGroup` | ≤ 26.0 |
| Sheet placement (inner display) | `.presentationPlacement(_:)` (`PresentationPlacement`) | `UISheetPresentationController.preferredPlacement` | **27.0** |
| Hero image under bar | `.backgroundExtensionEffect()` | `UIBackgroundExtensionView` | 26.0 |

Before writing any of these, re-check the SDK you're building with (grep command at the top of this file); availability may differ in later SDKs.

Item representation: vertical → icon; horizontal → icon or title (prefers icon); overflow → icon + title. **Title-only or custom-view items never go vertical** (unless `axisBehavior(.verticalPreferred)` on a custom view). Inspectors keep horizontal bars. Split views: sidebar/content horizontal, detail vertical. Sheets on the outer display: vertical by default.

---

## Reserved regions (iOS 27.1)

- SwiftUI: `GeometryProxy.reservedRegions(kind:options:layoutDirectionBehavior:)` → `[ReservedRegion]`.
- UIKit: `UIView.reservedRegions(kind:options:)` → `[UIView.ReservedRegion]`. (**Not** "UIViewReservedRegion".)
- Kinds: `.division` (fold), `.occlusion` (cameras).
- Options: `.includeInactive` (default returns active only).
- Region properties: `frame`, `margins`, `isActive`, `kind`, `id` (`ReservedRegion.ID`, SwiftUI).
- RTL: SwiftUI mirrors region frames by default; pass `LayoutDirectionBehavior.fixed` to get unmirrored frames.

---

## Arrangements (iOS 27.1)

- SwiftUI: `ArrangementView { primary } secondary: { secondary }` + `.arrangementViewStyle(.split | .overlay | .automatic)` (automatic → split). Styles: `.split.axes(.horizontal)`, `.overlay.axes(…)`.
  - Modifiers: `splitArrangementLayoutRatio(_:)`, `splitArrangementLayoutRatio(minHorizontal:idealHorizontal:maxHorizontal:minVertical:idealVertical:maxVertical:)`, `splitArrangementLayoutSize(minWidth:idealWidth:maxWidth:minHeight:idealHeight:maxHeight:)`, `splitArrangementFixedLayoutSize(horizontal:vertical:)`, `overlayArrangementEdge(_:)`.
  - Environment: `\.splitArrangementAxis`, `\.overlayArrangementZIndex`.
  - Custom styles: `ArrangementViewStyle` + `makeBody(configuration:)`.
- UIKit: `UIArrangementViewController` — `setViewController(_:for:animated:)` with `.primary` / `.secondary`, `updateArrangement(_:animated:)` with `UISplitArrangement` / `UIOverlayArrangement` (`.split.axes(.horizontal)`), `state(for:)` (`.zIndex`), `placement(for:)`, `viewController(for:)`; `UIViewController.arrangementViewController`; `UISplitArrangement.Dimension`.
- Rules: put navigation containers **around** an arrangement, never inside; never place one inside `List`, `ScrollView`, or `NavigationSplitView` columns where part could become inaccessible.

---

## Hinge (iOS 27.1) — live effects only, never layout

- SwiftUI: `.onHingeChange { oldContext, newContext in … }` (`onHingeChange(isEnabled:_:)`); `DeviceHingeContext.hinge` is a `DeviceHinge?` (`nil` on devices without a hinge) with `status` (`.closed`, `.partiallyOpen`, `.fullyOpen`) and `angle` (`Angle`).
- UIKit: `UIHingeInteraction`, `UIHinge`.

---

## Scenes & accessories

- `UIWindowScene.ActivationAction` (iOS 15+): hides itself when a new window can't be opened (outer display). Always handle scene-request errors.
- Scene lifecycle is required for resizing: TN3187; `UIApplicationSupportsMultipleScenes`.
- SwiftUI: `.sceneAccessory { CameraCaptureAccessory(isEnabled: $flag) { View() }.onAvailabilityChange { available in … } }`.
- UIKit: `UIViewController.registerSceneAccessory(_:)`, `UISceneAccessory`; session role `UISceneSession.Role.windowCameraCaptureAccessory`.

---

## Camera

- Virtual front camera: `AVCaptureDevice.DiscoverySession(deviceTypes: [.builtInWideAngleCamera, .builtInUltraWideCamera], mediaType: .video, position: .front)` → follows the display; `isVirtualDevice == true`; `activePrimaryConstituent` = streaming camera.
- Physical front cameras: `.builtInOuterUltraWideCamera`, `.builtInInnerUltraWideCamera`.
- `AVCaptureDeviceDirectionCoordinator(view:deviceTypes:changeHandler:)` (AVKit, main actor) → `AVCaptureDeviceDirectionMap` with `forwardFacingDeviceDescriptors` / `backwardFacingDeviceDescriptors` (`AVCaptureDeviceDescriptor`).
- `AVCaptureDevice.RotationCoordinator` for preview/capture rotation.
- `position` still reports where a camera sits, not which way it faces.

---

## Known unknowns — do not invent guidance

- Games: Metal / GameController / touch controls on iPhone Duo (only HIG: fill the screen in every pose; prefer aspect-ratio change over letterboxing).
- Widgets, Live Activities, Dynamic Island content on the outer display.
- App Clips and most app extensions (can't run in the iPhone Duo simulator).
- Keyboard / text input interaction with the fold.
- Exact `UIRequiresFullScreen` behavior on iPhone Duo.
- Exported folder name of Apple's App Resizability skill.
- Any CLI to fold the simulator.

If the user's app depends on one of these, say Apple hasn't documented it yet, implement the general resizing rules, and leave a TODO pointing to the Apple Developer Forums iPhone Duo Q&A.
