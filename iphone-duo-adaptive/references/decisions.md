# Decision Checkpoint

Ask these after baseline capture and audit. Skip any question the evidence already answers or that doesn't apply. There's no cap on the number of questions — quality matters more than brevity — but batch related ones (about 3–4 per ask) and never ask the same thing twice.

Each question must include:
1. The current screenshots (outer + inner, relevant poses).
2. 2–3 alternatives, sketched (ASCII below, or images in `contact-sheet.html`).
3. The code locations involved.
4. Your recommendation and the reason, listed first and labeled **(Recommended)**.

**Default** = what to do when nobody can answer. Record every answer in `DuoAdaptive/DUO_DECISIONS.md` as *user* or *default*.

---

## Q1. Ambition (always ask)

| Option | Meaning |
|---|---|
| **B (Recommended when interactive)** Readiness + inner-display improvements on the top screens | Mechanical fixes, then the per-screen questions below for 3–5 key screens |
| A. Readiness only | Mechanical fixes, system-container adoption and layout repairs (broken layouts fixed, existing design kept); no redesigns |
| C. Full design pass | Per-screen questions for every screen |

Default: **A** — which still includes all layout repairs. Never leave a layout you found broken.

## Q2. Deployment target & toolchain

| Option | Meaning |
|---|---|
| **Keep the current minimum and gate new APIs (Recommended)** | `#available(iOS 27.1, *)` everywhere |
| Raise the minimum to iOS 27.1 | Simpler code, drops older iOS users |

Also ask: "Does any build machine or CI use Xcode older than 27.1?" (affects `availability.md` → compile-time gating). Default: keep and gate; assume CI uses 27.1 and note it.

## Q3. Inner display layout — per screen

Recommend from what the screen already is:

| Screen today | Recommend |
|---|---|
| Feed, article, long scrolling content | **Single column**, readable width, keep as is |
| List → detail already (push navigation) | **`NavigationSplitView` / `UISplitViewController`** |
| Two distinct pieces side by side or stacked (`HStack`/`VStack`), e.g. player + queue, map + results | **`ArrangementView` split** |
| One view layered over another (`ZStack`), e.g. controls over video, sheet over map | **`ArrangementView` overlay** |

```
Single column          Split view (list | detail)     Arrangement split        Overlay (book pose)
┌───────────────┐     ┌──────┬────────────────┐       ┌────────┬────────┐      ┌────────┬────────┐
│   ┌───────┐   │     │ List │ Detail         │       │ Player │ Up next│      │ Video  │Controls│
│   │content│   │     │ ···  │                │       │        │  ···   │      │        │        │
│   └───────┘   │     │ ···  │                │       │        │  ···   │      │        │        │
└───────────────┘     └──────┴────────────────┘       └────────┴────────┘      └────────┴────────┘
```

Default: single column, except list→detail screens get a split view only if they already use `NavigationSplitView`/`UISplitViewController` (no new containers by default).

## Q4. Extra hierarchy level

| Option | Meaning |
|---|---|
| **Keep the tab bar (Recommended unless the app has 5+ tabs or deep sections)** | System places it vertically where appropriate |
| Sidebar on the inner display | `.defaultTabBarPlacement(.sidebar)` / `sidebar.preferredPlacement = .sidebar` |

Default: keep the tab bar.

## Q5. Toolbar priorities — per screen with 3+ bar items

Propose from the code: the Back/Close item at the top, one pinned prominent action (Done/Save/Compose), high priority for frequent or badged items, low priority / overflow for rare ones. Show the proposed vertical order:

```
Outer display (vertical bar)
┌──┬──────────────────┐
│← │                  │   ← Back / Close   (cancellationAction)
│✓ │                  │   ← Done           (topBarPinnedTrailing)
│  │     content      │
│✎ │                  │   ← Compose        (visibilityPriority .high)
│⋯ │                  │   ← overflow: Share, Print, Settings
└──┴──────────────────┘
```

Default: keep `.automatic` priorities; ensure every item has a title + SF Symbol; text-only buttons and segmented controls stay horizontal.

## Q6. When space runs out: tab bar or toolbar?

| Option | When |
|---|---|
| **Navigation-focused — keep tabs, overflow toolbar items (Recommended for browsing apps)** | `.automatic` |
| Task-focused — keep toolbar actions, minimize tab bar | `.toolbarVerticalCompressionBehavior(.prefersToolbarItems)` on editors/composers |

Default: automatic.

## Q7. Custom grids & canvases at the fold

| Option | Meaning |
|---|---|
| **Even column counts using the inactive fold region (Recommended for grids)** | `reservedRegions(kind: .division, options: .includeInactive)` |
| Move key controls away from the fold when partially open | Displace only the controls that intersect the active division |
| Leave as is and flag | TODO with screenshots |

Default: even columns for grids; flag canvases.

## Q8. Tabletop / book pose layout

Only for media, camera, video-call, reading or game screens.

| Option | Meaning |
|---|---|
| **No special layout (Recommended for most apps)** | System containers handle the fold |
| Yes — content on one half, controls on the other | Overlay `ArrangementView` (Q3) |

Default: no.

## Q9. Opt out of vertical bars

| Option | When |
|---|---|
| **No (Recommended)** | HIG: don't override default placement |
| Yes, for specific views | Single-page utilities or sheets with one or two controls |

Default: no.

## Q10. Full-width immersive screens

For non-scrolling visual screens (e.g. calculator, camera viewfinder, canvas) that don't need bars.

Default: no change.

## Q11. Camera (only if capture code exists)

| Option | Meaning |
|---|---|
| **Correctness only (Recommended)** | Virtual front camera or direction coordinator, rotation, preview aspect |
| Also show content on the outer display while recording | `CameraCaptureAccessory` (teleprompter, countdown, framing preview) |

Default: correctness only.

## Q12. Games (only for games)

| Option | Meaning |
|---|---|
| **Change the aspect ratio to fill each pose (Recommended if the engine allows)** | Keep text/control sizes consistent |
| Letterbox/pillarbox with artwork in the padding | When the game can't change aspect |

Say Apple's guidance here is thin. Default: change aspect ratio if the render path already supports resizing; otherwise flag.

## Q13. Designs

"Do you have designs for iPhone Duo (Figma frames from Apple's iPhone Duo kit, mockups, screenshots)?"
- **No — propose layouts from the current UI (Recommended)**
- Yes — share files or paths; implement to them and point out conflicts with HIG.

Never blocks. Default: propose.

## Q14. App Store screenshots

Which screens and orientations? Default: root screen of each tab, portrait, both displays, up to 10 each.

## Q15. Hard-to-reach screens

Test account, deep links or launch arguments for screens behind login or purchases. Never guess credentials; never type real credentials into the app yourself — ask the user to sign in in the simulator. Default: skip and mark untested.

---

## Asking well

- Lead with what you saw: "On the inner display, Settings is a 390-pt column centered in 900 pt of space (screenshot)."
- Offer concrete options, not open questions.
- One decision per question; per-screen questions can be batched as one question per screen.
- If the user answers "you decide", use the recommendation and record it as *user-delegated*.
