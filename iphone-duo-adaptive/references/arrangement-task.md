# Task: Arrangements & Split Views

**SDK Version:** iOS 27.1 for arrangements; split views and sidebar tabs predate it.

## Overview

Implements decisions **Q3** (inner-display layout per screen) and **Q4** (sidebar). Never run this task on a screen without a recorded decision; defaults don't introduce new containers.

## Choosing (from decision Q3)

| Relationship | Container |
|---|---|
| Navigation: list → detail | `NavigationSplitView` / `UISplitViewController` |
| Two pieces of content, neither should be hidden (player + queue, map + results, editor + preview) | `ArrangementView` **split** |
| Foreground over background (controls over video, panel over map) | `ArrangementView` **overlay** |
| One stream of content | No container change; readable width |

Arrangements lay out content; they don't navigate. Keep `NavigationStack`/`NavigationSplitView`/`TabView` **around** them.

## Patterns

### 1. Split view from existing push navigation
```swift
// Before
NavigationStack { MailboxList(selection: $selection) }
// After
NavigationSplitView {
    MailboxList(selection: $selection)
} detail: {
    if let selection { MessageView(id: selection) } else { ContentUnavailableView("No Message", systemImage: "envelope") }
}
```
Collapses to a single column on the outer display automatically. Preserve the existing navigation state and deep links; selection must survive fold/unfold.

UIKit: `UISplitViewController(style: .doubleColumn)` with the existing list and detail controllers; keep the compact (collapsed) behavior equal to today's push flow.

### 2. Sidebar tabs (Q4)
```swift
TabView { … }
    .tabViewStyle(.sidebarAdaptable)          // if not already
    .defaultTabBarPlacement(.sidebar)          // gate if needed
```
UIKit: `tabBarController.sidebar.preferredPlacement = .sidebar` (check the property in the SDK). Verify the chosen API's availability and gate it.

### 3. Arrangement — split
```swift
NavigationStack {
    if #available(iOS 27.1, *) {
        ArrangementView { NowPlayingView() } secondary: { UpNextView() }
            .arrangementViewStyle(.split)                      // .split.axes(.horizontal) to split only side by side
    } else {
        VStack { NowPlayingView(); UpNextView() }              // existing layout
    }
}
```
UIKit:
```swift
let arrangement = UIArrangementViewController()
arrangement.setViewController(playerVC, for: .primary, animated: false)
arrangement.setViewController(upNextVC, for: .secondary, animated: false)
arrangement.updateArrangement(.split.axes(.horizontal), animated: false)
navigationController.setViewControllers([arrangement], animated: false)
```
Confirm `setViewController(_:for:animated:)` vs. `setViewController(_:for:)` in the SDK headers before writing it. Tune size with `splitArrangementLayoutRatio(_:)` / `splitArrangementLayoutSize(…)`; read the current axis in children with `\.splitArrangementAxis`.

### 4. Arrangement — overlay
```swift
ArrangementView { PlayerControls() } secondary: { VideoSurface() }
    .arrangementViewStyle(.overlay)
```
Flat or closed: primary sits over secondary. Book pose: they move to either side of the fold. Children can adapt with `@Environment(\.overlayArrangementZIndex)` (e.g. collapse a list when it's on top). Anchor with `overlayArrangementEdge(_:)`.

### 5. Don'ts
- No arrangement inside `List`, `ScrollView`, or a `NavigationSplitView` column where part can become unreachable.
- No navigation containers inside an arrangement.
- Don't tie functionality to a pose: everything reachable in one pose must be reachable in all.

## Implementation Gates

- A recorded decision exists for the screen.
- Old layout kept for iOS < 27.1 (arrangements).
- Navigation state, selection, and scroll position survive folding (check in captures).

## Post-file Checklist

- [ ] Builds at the minimum deployment target.
- [ ] Outer display still shows the original single-column flow.

## Final Verification

Capture Closed, Open portrait, Open landscape and Book for each changed screen. The outer display matches the old flow; the inner display shows the chosen layout; in Book pose split/overlay content sits on each side of the fold; nothing is lost when folding mid-task.

## API Reference

See `api-facts.md` → Arrangements, Layout & resizing.
