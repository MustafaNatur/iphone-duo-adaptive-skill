# Task: Vertical Bars

**SDK Version:** iOS 27.1

## Overview

On iPhone Duo the system moves navigation bars, toolbars and tab bars to the side of the display — on the outer display, and on the inner display in landscape. Apps get this automatically **only** when bars come from system navigation containers and items are representable as icons. This task makes bars adopt vertical placement and organizes items so the important ones stay visible.

In SwiftUI, read Apple's `swiftui-whats-new-27/references/toolbar.md` first if it was exported.

## Detection

| Finding | Rule id |
|---|---|
| `UIToolbar(`, `UINavigationBar(`, `UITabBar(` created manually / added as subviews | `custom-bar` |
| SwiftUI custom bars built from `HStack` pinned with `.safeAreaInset(edge: .top/.bottom)` acting as toolbars | `custom-bar-swiftui` (review) |
| `.toolbar` items with `Text` only / `Button("Title")` without an image | `title-only-item` (review) |
| `UIBarButtonItem(title:style:target:action:)` without `image` | `title-only-item` |
| `UIBarButtonItem(customView:)` | `custom-view-item` |
| App-made "more" menus using `ellipsis` symbols | `custom-overflow` |
| Layout that assumes bars are top/bottom (fixed top/bottom insets, `navigationBar.frame.height`) | `bar-assumption` |

Then inspect captures: in Closed and Open-landscape poses, bars should be on the side.

## Patterns

### 1. Use the container's bars
```swift
// AVOID: a hand-built bottom bar
VStack { content; HStack { Button(…); Button(…) } }
// PREFER
NavigationStack {
    content
        .toolbar {
            ToolbarItem(placement: .bottomBar) { Button("Share", systemImage: "square.and.arrow.up") { … } }
        }
}
```
UIKit: set `toolbarItems` / `navigationItem` items on a view controller inside a `UINavigationController` (`setToolbarHidden(false)`), not a standalone `UIToolbar`. Keep a custom bar only if the user decides it must stay custom; then use `toolbarVerticalEdge` / `verticalBarEdge` to place it.

### 2. Order: Back/Close → prominent action → the rest
```swift
.toolbar {
    ToolbarItem(placement: .cancellationAction) { Button("Close", systemImage: "xmark") { dismiss() } }
    ToolbarItem(placement: .topBarPinnedTrailing) { Button("Done", systemImage: "checkmark") { save() } }
    ToolbarItemGroup(placement: .bottomBar) { … }
}
```
UIKit: custom Back/Close in `navigationItem.leadingItemGroups`; Done in `navigationItem.pinnedTrailingGroup`. The navigation controller adds the system Back button itself.

### 3. Every item gets a title and a symbol
```swift
// AVOID
Button("Filter") { … }
// PREFER
Button("Filter", systemImage: "line.3.horizontal.decrease") { … }   // or Label("Filter", systemImage: …)
```
UIKit: `UIBarButtonItem(title: "Filter", image: UIImage(systemName: "line.3.horizontal.decrease"), …)` — check the initializer you use exists in the SDK. Text-only items stay in horizontal bars; keep them minimal. A badge can turn a text item into a symbol item (`.badge(7)`).

### 4. Axis per item
- Item that must stay horizontal (segmented control, text field, a symbol/text transition): `.axisBehavior(.horizontalOnly)`.
- Custom view that works vertically: `.axisBehavior(.verticalPreferred)`.
UIKit: `UIBarButtonItem.axisBehavior`.

### 5. Overflow
- Priority (decision Q5): `.visibilityPriority(.high)` for frequent or badged items; low for rare ones. Group first, then individual items. UIKit: `visibilityPriority`.
- Move the app's own "more" menu into the system overflow: `ToolbarOverflowMenu { … }` / `navigationItem.additionalOverflowItems`. Reserve the ellipsis symbol for overflow.
- Tab bar vs. toolbar (decision Q6): `.toolbarVerticalCompressionBehavior(.prefersToolbarItems)` for task-focused screens.
- Use `ToolbarItemGroup` / `UIBarButtonItemGroup` instead of fixed spacers.

### 6. Content next to vertical bars
- Don't assume equal left/right space; use safe areas (`resizing-task.md` §7).
- Hero/background images: `.backgroundExtensionEffect()` / `UIBackgroundExtensionView` so art extends under the bar.
- Controls that belong to a pane (e.g. list filters in a split view) stay with that pane.

### 7. Sheets
On the outer display sheets get vertical bars by default. On the inner display: centered/leading placement → horizontal, trailing → vertical. Set placement with `.presentationPlacement(_:)` / `preferredPlacement` only if a decision requires it.

### 8. Opting out (decision Q9 only)
```swift
NavigationStack { SingleScreenUtility() }
    .duoVerticalBarsDisabled()          // gated helper from availability.md
```
UIKit: override `preferredVerticalBarBehavior` to return `.disabled` (guarded with `@available`).

## Implementation Gates

- New modifiers/properties are inside `#available(iOS 27.1, *)` or a gated helper.
- No item lost: count bar items before and after per screen.
- Items keep their original groupings (HIG).
- No override of default placement without decision Q9.

## Post-file Checklist

- [ ] Builds.
- [ ] Every item has title + symbol, or a recorded reason.
- [ ] Back/Close first, one pinned prominent action at most.

## Final Verification

Capture Closed portrait and Open landscape: bars are vertical, top item is Back/Close, the pinned action is visible, overflow contains the low-priority items, nothing overlaps content. Capture Open portrait: bars are horizontal and unchanged.

## API Reference

See `api-facts.md` → Vertical bars.
