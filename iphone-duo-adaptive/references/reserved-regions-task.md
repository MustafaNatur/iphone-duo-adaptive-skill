# Task: Reserved Regions (fold & cameras)

**SDK Version:** iOS 27.1

## Overview

Reserved regions are parts of a view that hardware claims:
- **Division** — the fold. Active only when the device is partially open (book/tabletop); it splits the inner display into two usable areas.
- **Occlusion** — the outer front camera (always) and the inner front camera (only while active).

System containers, alerts, sheets, context menus and split views already avoid them. **Only custom layouts need this task**: manual frames, custom `Layout`s, canvases, grids, edge-to-edge or full-width screens, and controls placed in absolute positions.

## Detection

| Finding | Rule id |
|---|---|
| Manual frame math (`frame =`, `CGRect(x:`, `.position(`, `.offset(` with computed values) in view code | `manual-frame` (review) |
| Custom SwiftUI `Layout` conformances | `custom-layout` |
| `.ignoresSafeArea()` on interactive content | `ignores-safe-area` (review) |
| `LazyVGrid`/`UICollectionViewCompositionalLayout` with column counts computed from width | `grid-columns` |

Confirm with the Book-pose and Closed captures: look for controls or text under the crease or the camera.

## Patterns

### 1. Read the regions

SwiftUI:
```swift
GeometryReader { proxy in
    let folds = proxy.reservedRegions(kind: .division)         // active only
    let cameras = proxy.reservedRegions(kind: .occlusion)
    Content(avoiding: (folds + cameras).map(\.frame))
}
```
UIKit:
```swift
override func viewDidLayoutSubviews() {
    super.viewDidLayoutSubviews()
    let folds = view.reservedRegions(kind: .division)
    layoutControls(avoiding: folds.map(\.frame))
}
```
Gate both with `#available(iOS 27.1, *)`. Re-read on every layout pass; regions become active/inactive as the device folds.

### 2. Displace only what's necessary (HIG)
- Move a control or a group as a unit; avoid large rearrangements.
- **Never displace continuous scrolling content** (feeds, articles, lists) — it scrolls past the fold.
- Keep contextual placement (e.g. a search field stays above the keyboard).
- Prefer small adjustments over relayout; controls that jump are hard to find.

### 3. Grids: even columns
```swift
GeometryReader { proxy in
    let hasFold = !proxy.reservedRegions(kind: .division, options: .includeInactive).isEmpty
    let columns = evenColumnCount(for: proxy.size.width, preferEven: hasFold)
    LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: columns)) { … }
}
```
`.includeInactive` lets you plan for the fold even while the device is flat, so the grid doesn't reflow when folding.

### 4. Split a custom canvas at the fold
When a decision calls for two halves (e.g. a reader showing two pages), use the active division's frame to split; when no division is active, show the single layout. Consider `ArrangementView` first (`arrangement-task.md`) — it already does this.

### 5. Right-to-left
SwiftUI mirrors region frames automatically, so a `Layout` needn't handle RTL. If you position content in fixed physical coordinates, pass `layoutDirectionBehavior: .fixed`.

### 6. Hinge is not layout
Don't use the hinge angle or status to decide layout. `onHingeChange` / `UIHingeInteraction` are for live effects only (`special-cases.md`).

## Implementation Gates

- Only views that intersect a region in a captured pose are changed.
- Old layout path kept for iOS < 27.1.
- No scrolling content displaced.

## Post-file Checklist

- [ ] Builds.
- [ ] Region reads happen on each layout pass, not cached.
- [ ] Interactive content avoids active occlusions.

## Final Verification

Capture Book pose: no interactive element or essential text sits on the crease; grids split cleanly. Capture Closed: nothing under the outer camera. Capture Open (flat): layout identical to before except intended changes.

## API Reference

See `api-facts.md` → Reserved regions.
