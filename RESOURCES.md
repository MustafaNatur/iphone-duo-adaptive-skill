# iPhone Duo — Research Resources

Everything we use as source material for the iPhone Duo adaptive-layout agent skill.
Apple's own material comes first; third-party coverage is listed separately and should be
cross-checked against Apple before it goes into the skill.

_Last updated: 2026-10-10. Apple URLs are relative to `https://developer.apple.com` unless written in full._

---

## 1. What is actually required (and what isn't)

| Date | Event / rule | Mandatory? | Source |
|---|---|---|---|
| 2026-09-09 | iPhone Duo developer resources open | — | [Get ready for iPhone Duo](https://developer.apple.com/news/?id=vn8abkxx) |
| 2026-09-18 | Xcode 27.1 beta (27A9269) with iPhone Duo simulator | — | [Build for iPhone Duo with new resources](https://developer.apple.com/news/?id=nyuppv9r) |
| 2026-10 | Xcode 27.1 **RC** available | — | [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes) |
| 2026-10-05 | App Store accepts iPhone Duo–optimized apps (built with Xcode 27.1) | — | [Prepare and submit your apps for iPhone Duo](https://developer.apple.com/news/?id=kkphp5qo) |
| 2026-10-16 | Pre-orders open | — | press coverage (§9) |
| 2026-10-23 | iPhone Duo on sale, iOS 27.1 | — | [Prepare and submit…](https://developer.apple.com/news/?id=kkphp5qo) |
| 2027-04 | **New submissions must include iPhone Duo screenshots** | **Yes** | [Prepare and submit…](https://developer.apple.com/news/?id=kkphp5qo) |
| 2027-04 | **Apps must be built with the iOS 27 / iPadOS 27 SDK or later** | **Yes** | [App Store submissions now open for the latest OS releases](https://developer.apple.com/news/?id=k1mtkt1k) |
| — | Adaptive layout / fold support | **No — strongly recommended guidance** | [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) |

**How each SDK behaves on iPhone Duo** (from [/iphone-duo/prepare/](https://developer.apple.com/iphone-duo/prepare/) and the "Prepare your app" talk):

| Built with | Behaviour |
|---|---|
| iOS 26 SDK or earlier | Runs unmodified; centred iPhone-sized window with black space on the inner display; left of status bar when closed |
| iOS 27 SDK | Resizes to fill most of the inner display; avoids status bar on the right edge |
| iOS 27.1 SDK+ | Full edge-to-edge; vertical tab bars/toolbars; reserved regions, ArrangementView, hinge APIs; "Optimized for iPhone Duo" badge on the App Store |

---

## 2. Apple Developer news posts

- [Get ready for iPhone Duo](https://developer.apple.com/news/?id=vn8abkxx) — 2026-09-09
- [App Store submissions now open for the latest OS releases](https://developer.apple.com/news/?id=k1mtkt1k) — 2026-09-09 (April 2027 SDK rule)
- [Get ready with the latest beta releases](https://developer.apple.com/news/?id=rfb1rooi) — 2026-09-16 (iOS 27.1 beta)
- [Build for iPhone Duo with new resources](https://developer.apple.com/news/?id=nyuppv9r) — 2026-09-18 (Xcode 27.1 beta, Figma/Sketch kits, workshops)
- [Prepare and submit your apps for iPhone Duo](https://developer.apple.com/news/?id=kkphp5qo) — 2026-10-05 (submissions open, April 2027 screenshot rule)
- [Showcase your apps with new assets on the App Store](https://developer.apple.com/news/?id=ljpl7kyn) — 2026-10-05 (new product-page assets)
- [Hello Developer: October 2026](https://developer.apple.com/news/?id=gv788oj6) → [/hello/october26/](https://developer.apple.com/hello/october26/) — group labs round 2, on-demand recap, [forums highlights thread](https://developer.apple.com/forums/thread/847644)
- [Upcoming requirements](https://developer.apple.com/news/upcoming-requirements/) — watch this page for changes

---

## 3. Apple hub pages

- [iPhone Duo hub](https://developer.apple.com/iphone-duo/)
- [Make sure your app is ready — three steps](https://developer.apple.com/iphone-duo/prepare/)
  1. Run Xcode's **App Resizability** skill ("get my app ready for iPhone Duo"; export with `xcrun agent skills export`)
  2. Fix patterns: stop sizing from `UIScreen.main`, stop using orientation for layout, stop assuming idiom/size class = device, check full-bleed media
  3. Test resizing: resizable simulator, iPhone Mirroring (macOS 27), iPhone Duo simulator (Xcode 27.1)

---

## 4. Apple documentation

### Complete API inventory (start here when writing the skill)
- [SwiftUI updates](https://developer.apple.com/documentation/updates/swiftui) and [UIKit updates](https://developer.apple.com/documentation/updates/uikit) — Apple's authoritative list of every iOS 27 / 27.1 API (arrangement views, reserved regions, hinge, scene accessories, vertical-axis controls)
- Note: Apple publishes **no iOS 27.1 release notes** (only iOS 27 and 27.2 beta); and the [sample code index](https://developer.apple.com/documentation/samplecode) has **no iPhone Duo sample** yet.

### Overviews & guides
- [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo) — **primary technical doc**
- [Designing for iPhone Duo (HIG)](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) — **primary design doc** (new page 2026-09-09)
- [HIG: Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [Size classes](https://developer.apple.com/design/human-interface-guidelines/layout#Size-classes) · [Split views](https://developer.apple.com/design/human-interface-guidelines/split-views) · [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) · [Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games)
- [TN3210: Optimizing your app for iPhone Mirroring](https://developer.apple.com/documentation/technotes/tn3210-optimizing-your-app-for-iphone-mirroring)
- [Adapting your app when traits change](https://developer.apple.com/documentation/uikit/adapting-your-app-when-traits-change)
- [Automatic trait tracking](https://developer.apple.com/documentation/uikit/automatic-trait-tracking)
- [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass)
- [Choosing a camera by the direction it faces](https://developer.apple.com/documentation/avkit/choosing-a-camera-by-the-direction-it-faces)
- [Registering a camera capture accessory on iPhone Duo](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo)

### Scene lifecycle & multiwindow (prerequisite for resizing)
- [TN3187: Migrating to the UIKit scene-based life cycle](https://developer.apple.com/documentation/technotes/tn3187-migrating-to-the-uikit-scene-based-life-cycle)
- [Specifying the scenes your app supports](https://developer.apple.com/documentation/uikit/specifying-the-scenes-your-app-supports)
- [UIApplicationSupportsMultipleScenes](https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest/uiapplicationsupportsmultiplescenes)
- [UIRequiresFullScreen](https://developer.apple.com/documentation/bundleresources/information-property-list/uirequiresfullscreen) — doc page only describes iPad; iOS 27 iPhone behaviour is in WWDC26 session 278 (see §10)
- [UIWindowScene.ActivationAction](https://developer.apple.com/documentation/uikit/uiwindowscene/activationaction) (iOS 15+, not Duo-specific; on Duo new windows open only on the inner display)

### Apple sample code (related, not Duo-specific)
- [Bringing multiple windows to your SwiftUI app](https://developer.apple.com/documentation/swiftui/bringing-multiple-windows-to-your-swiftui-app)
- [Supporting multiple windows on iPad](https://developer.apple.com/documentation/uikit/supporting-multiple-windows-on-ipad)
- [Supporting device rotation in your camera app](https://developer.apple.com/documentation/avfoundation/supporting-device-rotation-in-your-camera-app)
- [Adjusting your layout with keyboard layout guide](https://developer.apple.com/documentation/uikit/adjusting-your-layout-with-keyboard-layout-guide)

### Xcode & testing
- [Device Hub](https://developer.apple.com/documentation/xcode/device-hub)
- [Running your app on simulated or physical devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices)
- [Interacting with your app in Device Hub](https://developer.apple.com/documentation/xcode/interacting-with-your-app-in-device-hub)
- [Configuring the environment of a simulated device](https://developer.apple.com/documentation/xcode/configuring-the-environment-of-a-simulated-device)
- [Capturing screenshots and videos from devices](https://developer.apple.com/documentation/xcode/capturing-screenshots-and-videos-from-devices)
- [Interacting with devices using the command line](https://developer.apple.com/documentation/xcode/interacting-with-devices-using-the-command-line)
- [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes) — known iPhone Duo simulator issues: slow first launch, no StandBy, most app extensions can't run/debug
- [iOS & iPadOS release notes](https://developer.apple.com/documentation/ios-ipados-release-notes) (no 27.1 entry exists)

### API reference — layout & resizing
| Concept | SwiftUI | UIKit |
|---|---|---|
| Size classes | [horizontalSizeClass](https://developer.apple.com/documentation/swiftui/environmentvalues/horizontalsizeclass) / [verticalSizeClass](https://developer.apple.com/documentation/swiftui/environmentvalues/verticalsizeclass) | [horizontalSizeClass](https://developer.apple.com/documentation/uikit/uitraitcollection/horizontalsizeclass) / [verticalSizeClass](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalsizeclass) |
| Safe area | [GeometryProxy.safeAreaInsets](https://developer.apple.com/documentation/swiftui/geometryproxy/safeareainsets) | [UIView.safeAreaInsets](https://developer.apple.com/documentation/uikit/uiview/safeareainsets) |
| Geometry | [GeometryReader](https://developer.apple.com/documentation/swiftui/geometryreader), [GeometryProxy](https://developer.apple.com/documentation/swiftui/geometryproxy), [onGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)) | `view.bounds`, `viewWillTransition(to:with:)` |
| Windows | — | [UIWindow(windowScene:)](https://developer.apple.com/documentation/uikit/uiwindow/init(windowscene:)) instead of `UIWindow(frame: UIScreen.main.bounds)`; `view.window?.windowScene?.screen` |
| Corners | [ConcentricRectangle](https://developer.apple.com/documentation/swiftui/concentricrectangle) | [UICornerConfiguration](https://developer.apple.com/documentation/uikit/uicornerconfiguration-swift.struct) |
| Display scale | [displayScale](https://developer.apple.com/documentation/swiftui/environmentvalues/displayscale) | `traitCollection.displayScale` |
| Don't use for layout | — | [userInterfaceIdiom](https://developer.apple.com/documentation/uikit/uidevice/userinterfaceidiom), [UIInterfaceOrientation](https://developer.apple.com/documentation/uikit/uiinterfaceorientation), `UIScreen.main` |

### API reference — reserved regions (fold & cameras), iOS 27.1
- SwiftUI: [ReservedRegion](https://developer.apple.com/documentation/swiftui/reservedregion) · [reservedRegions(kind:options:layoutDirectionBehavior:)](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)) · [ReservedRegion.Kind](https://developer.apple.com/documentation/swiftui/reservedregion/kind-swift.struct) · [QueryOptions](https://developer.apple.com/documentation/swiftui/reservedregion/queryoptions) · [includeInactive](https://developer.apple.com/documentation/swiftui/reservedregion/queryoptions/includeinactive) · [ReservedRegion.ID](https://developer.apple.com/documentation/swiftui/reservedregion/id-swift.struct) · [LayoutDirectionBehavior.fixed](https://developer.apple.com/documentation/swiftui/layoutdirectionbehavior/fixed)
- UIKit: [UIView.ReservedRegion](https://developer.apple.com/documentation/uikit/uiview/reservedregion) (blogs sometimes misspell it "UIViewReservedRegion") · [reservedRegions(kind:options:)](https://developer.apple.com/documentation/uikit/uiview/reservedregions(kind:options:))
- Kinds: `.division` (fold, active only when partially open) and `.occlusion` (outer camera always; inner camera when active). Use `.includeInactive` for high-level decisions (e.g. even grid columns).

### API reference — arrangement views, iOS 27.1
- SwiftUI: [ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview) · [arrangementViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/arrangementviewstyle(_:)) · [SplitArrangementViewStyle](https://developer.apple.com/documentation/swiftui/splitarrangementviewstyle) · [OverlayArrangementViewStyle](https://developer.apple.com/documentation/swiftui/overlayarrangementviewstyle) · [AutomaticArrangementViewStyle](https://developer.apple.com/documentation/swiftui/automaticarrangementviewstyle) · [ArrangementViewStyle](https://developer.apple.com/documentation/swiftui/arrangementviewstyle) · [overlayArrangementEdge(_:)](https://developer.apple.com/documentation/swiftui/view/overlayarrangementedge(_:)) · [splitArrangementLayoutRatio(_:)](https://developer.apple.com/documentation/swiftui/view/splitarrangementlayoutratio(_:)) · [splitArrangementFixedLayoutSize](https://developer.apple.com/documentation/swiftui/view/splitarrangementfixedlayoutsize(horizontal:vertical:)) · [splitArrangementLayoutSize(…)](https://developer.apple.com/documentation/swiftui/view/splitarrangementlayoutsize(minwidth:idealwidth:maxwidth:minheight:idealheight:maxheight:)) · [splitArrangementAxis](https://developer.apple.com/documentation/swiftui/environmentvalues/splitarrangementaxis) (env) · [overlayArrangementZIndex](https://developer.apple.com/documentation/swiftui/environmentvalues/overlayarrangementzindex) (env)
- UIKit extras: [UIViewController.arrangementViewController](https://developer.apple.com/documentation/uikit/uiviewcontroller/arrangementviewcontroller) · [UISplitArrangement.Dimension](https://developer.apple.com/documentation/uikit/uisplitarrangement-swift.struct/dimension) · [UIArrangementViewController.Arrangement](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller/arrangement) · [ViewPlacement](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller/viewplacement)
- UIKit: [UIArrangementViewController](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller) · [UISplitArrangement](https://developer.apple.com/documentation/uikit/uisplitarrangement-swift.struct) · [UIOverlayArrangement](https://developer.apple.com/documentation/uikit/uioverlayarrangement-swift.struct) · [updateArrangement(_:animated:)](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller/updatearrangement(_:animated:)) · [setViewController(_:for:animated:)](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller/setviewcontroller(_:for:animated:)) · [state(for:)](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller/state(for:))
- Rules: don't nest navigation containers inside; don't put inside List/ScrollView/NavigationSplitView.

### API reference — vertical bars, iOS 27.1
| Purpose | SwiftUI | UIKit |
|---|---|---|
| Opt out | [toolbarVerticalBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/toolbarverticalbehavior(_:)) | [preferredVerticalBarBehavior](https://developer.apple.com/documentation/uikit/uiviewcontroller/preferredverticalbarbehavior) |
| Which edge | [toolbarVerticalEdge](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge) | [verticalBarEdge](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge) |
| Compression | [ToolbarVerticalCompressionBehavior](https://developer.apple.com/documentation/swiftui/toolbarverticalcompressionbehavior) | [UIVerticalBarCompressionBehavior](https://developer.apple.com/documentation/uikit/uiverticalbarcompressionbehavior) |
| Axis per item | [axisBehavior(_:)](https://developer.apple.com/documentation/swiftui/toolbarcontent/axisbehavior(_:)) | [axisBehavior](https://developer.apple.com/documentation/uikit/uibarbuttonitem/axisbehavior-swift.property) |
| Overflow order | [visibilityPriority(_:)](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)) / [ToolbarItemVisibilityPriority](https://developer.apple.com/documentation/swiftui/toolbaritemvisibilitypriority) | [visibilityPriority](https://developer.apple.com/documentation/uikit/uibarbuttonitem/visibilitypriority) / [UIBarButtonItemVisibilityPriority](https://developer.apple.com/documentation/uikit/uibarbuttonitemvisibilitypriority) |
| System overflow menu | [ToolbarOverflowMenu](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu) | [additionalOverflowItems](https://developer.apple.com/documentation/uikit/uinavigationitem/additionaloverflowitems) |
| Pinned prominent action | [topBarPinnedTrailing](https://developer.apple.com/documentation/swiftui/toolbaritemplacement/topbarpinnedtrailing) | [pinnedTrailingGroup](https://developer.apple.com/documentation/uikit/uinavigationitem/pinnedtrailinggroup) |
| Back / Close | [cancellationAction](https://developer.apple.com/documentation/swiftui/toolbaritemplacement/cancellationaction) | [leadingItemGroups](https://developer.apple.com/documentation/uikit/uinavigationitem/leadingitemgroups) |
| Grouping | [ToolbarItemGroup](https://developer.apple.com/documentation/swiftui/toolbaritemgroup) | [UIBarButtonItemGroup](https://developer.apple.com/documentation/uikit/uibarbuttonitemgroup) |
| Sheet placement | [presentationPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:)) | [preferredPlacement](https://developer.apple.com/documentation/uikit/uisheetpresentationcontroller/preferredplacement) |
| Hero under bar | [backgroundExtensionEffect()](https://developer.apple.com/documentation/swiftui/view/backgroundextensioneffect()) | [UIBackgroundExtensionView](https://developer.apple.com/documentation/uikit/uibackgroundextensionview) |
| Containers | [NavigationStack](https://developer.apple.com/documentation/swiftui/navigationstack), [NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview), [toolbar(content:)](https://developer.apple.com/documentation/swiftui/view/toolbar(content:)) | [UISplitViewController](https://developer.apple.com/documentation/uikit/uisplitviewcontroller), `UINavigationController`, `UITabBarController` (avoid standalone [UIToolbar](https://developer.apple.com/documentation/uikit/uitoolbar) / [UINavigationBar](https://developer.apple.com/documentation/uikit/uinavigationbar) / [UITabBar](https://developer.apple.com/documentation/uikit/uitabbar)) |

### API reference — hinge, scenes, accessories, camera
- Hinge (live effects only, never layout): SwiftUI [onHingeChange(isEnabled:_:)](https://developer.apple.com/documentation/swiftui/view/onhingechange(isenabled:_:)) → closure gets old/new [DeviceHingeContext](https://developer.apple.com/documentation/swiftui/devicehingecontext); `context.hinge` ([DeviceHinge](https://developer.apple.com/documentation/swiftui/devicehinge)) is `nil` on hinge-less devices; `status` `.closed` / `.partiallyOpen` / `.fullyOpen` + `angle`. UIKit [UIHingeInteraction](https://developer.apple.com/documentation/uikit/uihingeinteraction) · [UIHinge](https://developer.apple.com/documentation/uikit/uihinge)
- Scenes: [UIWindowScene.ActivationAction](https://developer.apple.com/documentation/uikit/uiwindowscene/activationaction) (new windows only on the inner display; handle request errors)
- Scene accessories: SwiftUI [sceneAccessory(content:)](https://developer.apple.com/documentation/swiftui/view/sceneaccessory(content:)) + [CameraCaptureAccessory](https://developer.apple.com/documentation/swiftui/cameracaptureaccessory) (`isEnabled:`, `.onAvailabilityChange`); UIKit [registerSceneAccessory(_:)](https://developer.apple.com/documentation/uikit/uiviewcontroller/registersceneaccessory(_:)) · [UISceneAccessory](https://developer.apple.com/documentation/uikit/uisceneaccessory) · session role [windowCameraCaptureAccessory](https://developer.apple.com/documentation/uikit/uiscenesession/role-swift.struct/windowcameracaptureaccessory)
- Camera: [AVCaptureDeviceDirectionCoordinator](https://developer.apple.com/documentation/avkit/avcapturedevicedirectioncoordinator) · [AVCaptureDeviceDirectionMap](https://developer.apple.com/documentation/avkit/avcapturedevicedirectionmap) · [builtInOuterUltraWideCamera](https://developer.apple.com/documentation/avfoundation/avcapturedevice/devicetype-swift.struct/builtinouterultrawidecamera) · [builtInInnerUltraWideCamera](https://developer.apple.com/documentation/avfoundation/avcapturedevice/devicetype-swift.struct/builtininnerultrawidecamera) · [activePrimaryConstituent](https://developer.apple.com/documentation/avfoundation/avcapturedevice/activeprimaryconstituent) · [AVCaptureDevice.RotationCoordinator](https://developer.apple.com/documentation/avfoundation/avcapturedevice/rotationcoordinator) · `dynamicAspectRatio`
- Navigation: `TabView` + `.defaultTabBarPlacement(.sidebar)`; UIKit `tabBarController.sidebar.preferredPlacement`

---

## 5. Apple videos

### iPhone Duo Tech Talks (Sept 2026)
| Talk | Covers |
|---|---|
| [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) | Anatomy, poses, design principles |
| [Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) | SDK behaviour, size classes, `UIScreen.main`, asymmetric safe areas, reserved regions, testing, App Resizability skill |
| [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) | Vertical toolbars/tab bars, ordering, axis behaviour, overflow, compression, opting out |
| [Strike a pose with adaptive layouts on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111463/) | Reserved regions, displacement patterns, ArrangementView split/overlay |
| [Leverage multiple displays and scenes on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111464/) | Hinge API, Split View multitasking, multiple scenes, scene accessories, teleprompter demo |
| [Build a great camera experience for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111465/) | Virtual front camera, physical cameras, direction coordinator, preview, rotation |

### iPhone Duo Group Labs (Meet with Apple)
- [iPhone Duo Group Lab — Day 1](https://developer.apple.com/videos/play/meet-with-apple/285/)
- [iPhone Duo Group Lab — Day 2](https://developer.apple.com/videos/play/meet-with-apple/286/)

### Related WWDC26 sessions
- **Core:** [Modernize your UIKit app](https://developer.apple.com/videos/play/wwdc2026/278/) — resizable iPhone apps, `UIRequiresFullScreen` changes, scene geometry
- Supporting: [What's new in SwiftUI](https://developer.apple.com/videos/play/wwdc2026/269/) · [Get the most out of Device Hub](https://developer.apple.com/videos/play/wwdc2026/260/) · [What's new in Xcode 27](https://developer.apple.com/videos/play/wwdc2026/258/) · [Xcode, agents, and you](https://developer.apple.com/videos/play/wwdc2026/259/) · [Build a responsive camera app that launches quickly](https://developer.apple.com/videos/play/wwdc2026/303/) · [Support the Center Stage front camera](https://developer.apple.com/videos/play/wwdc2026/341/) · [Enhance your presence on the App Store](https://developer.apple.com/videos/play/wwdc2026/205/)

### Earlier background
- [Make your UIKit app more flexible (WWDC25)](https://developer.apple.com/videos/play/wwdc2025/282/)

---

## 6. Tools

- **Xcode 27.1 RC** (first beta 27A9269 on 2026-09-18) — [Downloads](https://developer.apple.com/download/applications/) · [Xcode](https://developer.apple.com/xcode/). Requires Apple silicon Mac, macOS 26.6+.
- **iPhone Duo simulator** in Device Hub — open/close/fold/rotate controls; hold ⌥ for a hinge-angle slider. Appears only with the iOS 27.1 runtime (Xcode → Settings → Components).
- **Simulator command line** (details in [DESIGN.md §5](DESIGN.md#5-simulator-strategy)): `simctl create/boot/install/launch`; per-display screenshots `simctl io <udid> screenshot --display=primary|primary-1`; `devicectl device motion hinge-angle` (read-only); `devicectl device orientation set` (reported not to work on Duo — verify). **No Apple CLI, MCP tool or XCTest API folds the simulator** — only Device Hub's Closed / Book / Open toolbar.
- **Resizable iOS simulator** (Xcode 27) and **SwiftUI preview resize handles**
- **iPhone Mirroring** on macOS 27 — resize the window to extreme sizes
- **Xcode's built-in agent skills** — export with `xcrun agent skills export --output-dir <dir>`. Xcode 27.0 exports `uikit-app-modernization` (UIScreen, orientation, scene lifecycle, safe areas) and `swiftui-whats-new-27` (incl. `references/toolbar.md`), among others. Not redistributed here (Apple content) — the skill exports them at runtime. Apple's prepare page names the 27.1 skill **"App Resizability"** (prompt: "get my app ready for iPhone Duo"); its content isn't published and the "formerly App Modernization" lineage is **unverified**. Our skill must complement, not duplicate, these.
- **Design kits**: [Apple Design Resources](https://developer.apple.com/design/resources/) (Figma + Sketch iPhone Duo kits)
- **App Store Connect preview tool** — preview screenshots/metadata on iPhone Duo

---

## 7. App Store assets

- [Screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)
  - Outer display: 1398 × 2034 (portrait), 2034 × 1398 (landscape)
  - Inner display: 2007 × 2853 (portrait), 2853 × 2007 (landscape)
  - 1–10 per size, `.jpg`/`.jpeg`/`.png`, no alpha. Until April 2027, falls back to scaled large-iPhone screenshots.
- [App preview specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications)
- [App Store asset best practices & templates](https://developer.apple.com/app-store/asset-best-practices/)
- [Manage your App Store assets](https://developer.apple.com/help/app-store-connect/manage-app-information/manage-your-app-store-assets)
- [Submitting your app](https://developer.apple.com/app-store/submitting/)
- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- Featuring nomination: mention iPhone Duo optimization

---

## 8. Events, labs, forums

- [Upcoming iPhone Duo workshops (in person)](https://developer.apple.com/events/view/upcoming-events?topics=iphone-duo&formats=inperson)
- Online group labs: [Oct 13, 6–7 p.m. PT](https://developer.apple.com/events/view/9Q8VP547C9/dashboard) · [Oct 15, 9–10 a.m. PT](https://developer.apple.com/events/view/4NU9WP84LC/dashboard)
- Forums Q&A: [Popular Q&A](https://apple.co/iPhoneDuo-QA01) · [Photos & Camera](https://developer.apple.com/forums/activities/1659080) · [SwiftUI](https://developer.apple.com/forums/activities/1664080) · [UIKit](https://developer.apple.com/forums/activities/1670080)
- [Feedback Assistant](https://feedbackassistant.apple.com/)

---

## 9. Third-party coverage (verify against Apple)

### News (only items that add something beyond Apple's posts)
- MacRumors — [Apple Announces iPhone Duo Apps Can Now Be Submitted to App Store](https://www.macrumors.com/2026/10/05/apple-opens-iphone-duo-app-submissions/) (2026-10-05)
- 9to5Mac — [Apple invites developers to submit iPhone Duo-ready apps](https://9to5mac.com/2026/10/05/apple-invites-developers-to-submit-iphone-duo-ready-apps-to-the-app-store/) (2026-10-05)
- InfoQ — [What iOS Developers Need to Change to Prepare for the iPhone Duo](https://www.infoq.com/news/2026/09/apple-iphone-duo-api/)

### Tutorials & deep dives
- SwiftLee — [iPhone Duo Simulator: Testing and optimizing your SwiftUI app](https://www.avanderlee.com/swiftui/iphone-duo-simulator/) (2026-09-22)
- Blake Crosley — [Xcode 27.1 Beta: Your App in the iPhone Duo Simulator](https://blakecrosley.com/blog/xcode-27-1-beta-iphone-duo-simulator)
- The Swift Dev — [Prepare Your SwiftUI App For iPhone Duo](https://www.theswift.dev/posts/prepare-your-swiftui-app-for-iphone-duo/)
- Livsy Code — [Building iPhone Duo Layouts with ArrangementView](https://livsycode.com/swiftui/building-iphone-duo-layouts-with-arrangementview/)
- BleepingSwift — [Building Fold-Aware Layouts with ArrangementView](https://bleepingswift.com/blog/arrangementview-swiftui-iphone-duo) · [Keeping Content Clear of the Fold with ReservedRegion](https://bleepingswift.com/blog/reservedregion-swiftui-iphone-duo-fold)
- onmyway133 — [How to adapt layout for iPhone Duo](https://github.com/onmyway133/blog/issues/1062)
- Fatbobman — [From Size Class to Available Space: Is horizontalSizeClass Still Reliable?](https://fatbobman.com/en/posts/from-size-class-to-available-space/)
- DEV Community — [iPhone Duo for iOS Developers: What Actually Changes in Your Swift Code](https://dev.to/arshtechpro/iphone-duo-for-ios-developers-what-actually-changes-in-your-swift-code-5gc5)
- WWDC Index — [Modernize your UIKit app (transcript index)](https://nonstrict.eu/wwdcindex/wwdc2026/278/)

### Sample code
- [artemnovichkov/iPhone-Duo-by-Examples](https://github.com/artemnovichkov/iPhone-Duo-by-Examples) — SwiftUI samples for hinge, reserved regions, ArrangementView, vertical toolbar, container margins (MIT)
- [BleepingSwift/iphone-duo-split-view-left-or-right](https://github.com/BleepingSwift/iphone-duo-split-view-left-or-right) — detecting which side of Split View the app is on
- [TarunYadgirkar/duo-test](https://github.com/TarunYadgirkar/duo-test) — test app

### Peer skills (surveyed 2026-10-10: ~30 standalone repos)
| Repo | ★ | Notes |
|---|---|---|
| [mirzaaghazadeh/iphone-duo-skills](https://github.com/mirzaaghazadeh/iphone-duo-skills) | 149 | 11 skills, broadest scope (incl. Flutter/RN/Capacitor, App Store); static checklists; never compiled; inconsistent `UIViewReservedRegion` vs `UIView.ReservedRegion` |
| [alexey1312/iPhone-Duo-Agent-Skill](https://github.com/alexey1312/iPhone-Duo-Agent-Skill) | 5 | Most rigorous: scanner, SDK-header check, drives simulator via `hinge`, cites talk timestamps; likely the same as the paid agensi.io "iPhone Duo Adaptivity Audit" |
| [sven-ericmolzahn/iphone-duo-skill](https://github.com/sven-ericmolzahn/iphone-duo-skill) | 16 | `swiftc -typecheck` on samples, display-capture scripts; companion `iphone-duo-probe` |
| [FloWritesCode/fwc-swiftui-skills](https://github.com/FloWritesCode/fwc-swiftui-skills) (`swiftui-iphone-duo`) | 400 (pack) | Good SwiftUI decision tree; no UIKit, no scripts |
| [d-date/iphone-duo-skill](https://github.com/d-date/iphone-duo-skill) | 35 | Japanese; built from the Tech Talks + HIG; checklist |
| [hechen/iphone-duo-skills](https://github.com/hechen/iphone-duo-skills) | 4 | 8 skills, test-plan template; Cursor/Copilot/Gemini support |
| [dogfooter8750/iphone-duo-skill](https://github.com/dogfooter8750/iphone-duo-skill) | 1 | Audit script + cheatsheet; uses `UIViewReservedRegion` |
| [CharlesWiltgen/Axiom](https://github.com/CharlesWiltgen/Axiom) (`axiom-audit-resize`) | 1.2k (pack) | Generic resize-readiness audit, not Duo-specific |
| [AvdLee/SwiftUI-Agent-Skill](https://github.com/AvdLee/SwiftUI-Agent-Skill) | 3.7k (pack) | Duo reference PR #85 closed unmerged |
| [EvanBacon/serve-sim](https://tessl.io/registry/skills/github/EvanBacon/serve-sim/serve-sim-duo-verification) | — | Duo verification skill for the simulator |

Plus ~20 small generic, design-only or copy repos. No published Cursor rule pack, no Duo MCP server.
Apple's own Xcode skills — see §6 (exported locally, not redistributed).

### Simulator tooling (third-party, use with care)
- [artemnovichkov/hinge](https://github.com/artemnovichkov/hinge) — CLI + skill to fold the iPhone Duo simulator / set the hinge angle (private Apple interfaces; unverified)
- [skarol/duoctl](https://github.com/skarol/duoctl) — CLI to open/close/set hinge on the Duo simulator (private interfaces; unverified)
- [Appium xcuitest-driver PR #3001](https://github.com/appium/appium-xcuitest-driver/pull/3001) · [Maestro PR #3621](https://github.com/mobile-dev-inc/Maestro/pull/3621) · [idb #965](https://github.com/facebook/idb/issues/965) — tooling issues with the Duo's two displays (taps landing on the outer screen when open)

---

## 10. Known gotchas collected so far

- The inner display is regular × regular and **ignores `supportedInterfaceOrientations`**; the outer display behaves like a normal iPhone. _(Source: "Prepare your app for iPhone Duo" talk, "Use size classes" chapter ~2:46 — not in the written docs.)_
- `UIRequiresFullScreen`: the Duo talk says it is still honored but the app still resizes on open/close; third parties say since iOS 27 it no longer opts out of resizing and instead enables discrete resizing honoring supported orientations. **Unverified — confirm against WWDC26 session 278 before putting in the skill.**
- Safe areas are **asymmetric** (vertical bars sit on one edge) — use `bounds.inset(by: safeAreaInsets)`, never `left * 2`.
- New windows can only be created on the inner display.
- Hinge angle is for effects, never for layout.
- Simulator cannot test camera transitions, outer-display capture accessories, haptics, reachability or performance — use hardware.
- ArrangementView / reserved regions / hinge / vertical-bar APIs need the iOS 27.1 SDK; the 27.0 SDK won't compile them. Keep `#available` fallbacks.

## 11. Known unknowns (no Apple guidance found yet — the skill must not invent any)

- Games: Metal / GameController / touch controls on iPhone Duo (only the HIG "fill the screen, prefer aspect change over letterboxing" line)
- Widgets, Live Activities and Dynamic Island on the outer display
- App Clips and app extensions (simulator can't run most extensions)
- Right-to-left layouts with vertical bars (HIG: bars stay on the same hardware side; reserved-region frames are mirrored unless `.fixed`)
- Keyboard / text input around the fold
