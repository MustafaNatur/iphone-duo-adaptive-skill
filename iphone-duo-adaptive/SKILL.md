---
name: iphone-duo-adaptive
description: "Interactively adapts and verifies native iOS apps (UIKit, SwiftUI or mixed) for iPhone Duo, Apple's foldable iPhone: screenshots every pose, audits code, asks design questions, fixes, re-verifies, and makes App Store screenshots. Use when the user mentions iPhone Duo, foldable iPhone, inner/outer display, fold, hinge, book/tabletop pose, iOS 27.1 resizing, 'get my app ready for iPhone Duo', or symbols like ArrangementView, UIArrangementViewController, ReservedRegion, reservedRegions(kind:), onHingeChange, UIHingeInteraction, toolbarVerticalBehavior, toolbarVerticalEdge, verticalBarEdge, ToolbarOverflowMenu, CameraCaptureAccessory, AVCaptureDeviceDirectionCoordinator. SKIP: Flutter, React Native, Capacitor, MAUI, web, Android. Hands general UIScreen.main/orientation/scene-lifecycle/safe-area work to Apple's uikit-app-modernization skill."
compatibility: "macOS with Xcode 27.1+ for full mode (iPhone Duo simulator, iOS 27.1 SDK); older Xcode runs a limited audit-and-fix mode. Python 3 and sips (macOS) for scripts."
metadata:
  effort: high
  version: "0.1.0"
---
# iPhone Duo Adaptive Skill

Use only public Apple API. Every symbol you write must appear in `references/api-facts.md`, in an Apple skill you exported this session, or in the iOS SDK headers you can grep. Never invent API. If something is listed under **Known unknowns**, tell the user rather than guessing.

## Purpose

Make an existing iOS app work well on iPhone Duo and prove it:
- Fix code that assumes one screen, one orientation, or one device size.
- Adopt iPhone Duo behaviors (vertical bars, reserved regions, arrangements, camera direction) where they help.
- Make the design decisions **with** the user, record them, implement them, and verify every change on the iPhone Duo simulator.

## Scope

- Swift and Objective-C; UIKit, SwiftUI, and mixed apps.
- Changes code, Info.plist and (only with consent) the deployment target. Never changes signing, bundle IDs, or third-party code under `Pods/`, `Carthage/`, `.build/`, or vendored SDKs.
- Out of scope: cross-platform frameworks, Android, server code, visual redesigns the user did not approve.

## Core Principles

1. **Evidence before questions.** Build, screenshot, and audit before you ask anything. Never ask what the code or screenshots already answer.
2. **Apple's skills first.** When Xcode is installed, export Apple's skills (see `references/apple-skills-bridge.md`) and let them handle what they cover. Where Apple's guidance and this skill overlap, Apple wins.
3. **Safe replacement → apply. Several valid options → ask. No safe option or nobody to ask → actionable TODO.** A TODO must say why the change is needed, what the fix looks like, and any lifecycle or threading concern. A vague TODO is a failure.
4. **Design is the user's call.** Mechanical fixes are yours. Anything that changes what the user sees beyond "now fills the space correctly" (a second pane, a sidebar, an arrangement, a tabletop layout, opting out of vertical bars) needs a decision from the checkpoint or an explicit default from `references/decisions.md`. Defaults never introduce an `ArrangementView`.
5. **Honor explicit user instructions.** If the user asks for a specific approach, do that. Otherwise use the defaults in the reference files.
6. **Lay out by available space, never by device.** Use view/scene bounds, size classes, safe areas and reserved regions. Never key layout to `UIScreen.main`, `UIDevice.current.orientation`, `userInterfaceIdiom`, hard-coded sizes, the hinge angle, or "regular width means iPad".
7. **Gate every new API.** iPhone Duo APIs need the iOS 27.1 SDK. Keep the app building at its current minimum deployment target with `if #available(iOS 27.1, *)` / `@available`. If any build environment still uses Xcode older than 27.1, follow the compile-time gating in `references/availability.md`.
8. **Stay in scope.** Edit only lines that the active task targets. No drive-by refactors, reformatting, or renames. Preserve existing guards, fallbacks and control flow.
9. **Compile after every file.** A change that does not build is not done.
10. **Never claim what you did not verify.** The fold cannot be automated with Apple's tools. Record which poses were actually captured, confirmed by the hinge angle, and list everything that needs a physical device.
11. **Never silently skip a file.** Track every file the audit flags in the todo list. Each ends as changed, already correct, TODO with reason, or out of scope with reason.

## Tool Preferences

- Prefer Xcode's MCP tools when they are available (names may carry a server prefix; look them up in the tool registry, never guess). Use them for search, build settings, building, and driving the app (`device-interaction`).
- Otherwise use `xcodebuild`, `xcrun simctl`, `xcrun devicectl`, and the bundled `scripts/`.
- Use the ask-user tool (e.g. `AskUserQuestion`) for every question, with the recommended option first and labeled. If no such tool exists, ask in chat and wait.
- For large apps, use subagents per module or screen, each with the relevant task file, and merge results into the coverage list.

## Workflow

Load `references/workflow.md` **before Phase 0** and follow it. Summary:

| Phase | What | User involvement |
|---|---|---|
| 0. Preflight | `scripts/preflight.py`; export Apple skills; detect app type; check git state | Consent for downloads or a dirty tree |
| 1. Briefing | Tell the user what will happen and what you'll need from them | — |
| 2. Baseline capture | Build and run on the iPhone Duo simulator, screenshot every pose (`references/simulator.md`) | Fold / unfold in Device Hub when asked |
| 3. Audit & inventory | `scripts/audit.py`; list screens, containers, bars, custom layouts | — |
| 4. Plan | Write `DUO_PLAN.md` from `assets/DUO_PLAN.template.md` | — |
| 5. Decision checkpoint | Ask the questions in `references/decisions.md`; get **Run / Cancel** on the plan | **Yes** |
| 6. Mechanical fixes | Apple skills first, then the task files below | — |
| 7. Design implementation | Implement recorded decisions | Only if something new comes up |
| 8. Verification | Rebuild (incl. minimum deployment target), recapture, contact sheet | Fold / unfold again |
| 9. App Store assets | Capture and validate screenshots (`references/app-store-assets.md`) | Pick screens |
| 10. Report | Lean summary (below) | — |

**Fast path:** if the audit finds nothing and the baseline screenshots look correct in every captured pose, skip Phases 4–7, say so, and offer Phase 9.

**Non-interactive runs** (headless, CI, or the user says "just do it"): skip questions, apply the defaults marked in `references/decisions.md`, mark every one as a default in `DUO_DECISIONS.md`, skip poses that need a human, and say so in the report.

## Task Registry

Run in order. Load a task file only when the audit or a decision makes it active.

| Task | File | When |
|---|---|---|
| General modernization | Apple's `uikit-app-modernization` (via bridge), else `references/resizing-task.md` | Audit finds `UIScreen.main`, orientation, idiom, fixed-size, app-lifecycle, or symmetric-safe-area patterns |
| Vertical bars | `references/vertical-bars-task.md` | Any navigation bar, toolbar or tab bar |
| Reserved regions | `references/reserved-regions-task.md` | Custom layouts, canvases, grids, edge-to-edge or manually positioned controls |
| Arrangements & split views | `references/arrangement-task.md` | Decisions Q3 / Q4 choose a new layout |
| Camera | `references/camera-task.md` | AVFoundation / AVKit capture found |
| Special cases | `references/special-cases.md` | Games, hinge-driven effects, multiwindow, scene accessories, extensions |

Always available: `references/api-facts.md` (verified API list and known unknowns), `references/availability.md`, `references/simulator.md`, `references/decisions.md`.

## Common Failure Modes

| Symptom | Cause | Correct response |
|---|---|---|
| Build fails on an iPhone Duo symbol | Older SDK, or invented/misspelled API (e.g. `UIViewReservedRegion`) | Check `api-facts.md`; the UIKit type is `UIView.ReservedRegion`; require Xcode 27.1 or guard the code |
| Build breaks for older iOS | Missing availability guard | Wrap with `if #available(iOS 27.1, *)` and keep the old path |
| Bars stay horizontal on the outer display | Custom `UIToolbar`/`UINavigationBar`/`UITabBar` or bars outside a navigation container | Move items into the container's toolbar (`vertical-bars-task.md`) |
| Item missing from the vertical bar | Item has a title but no icon, or a custom view | Give it both a title and an SF Symbol; use `axisBehavior` for custom views |
| Content hidden under the fold or camera | Manual frames ignore reserved regions | Query `.division` / `.occlusion` regions and move only what's necessary |
| Layout jumps when folding | Layout keyed to hinge angle or pose | Use size classes, bounds and reserved regions; hinge only for live effects |
| Rotation command "succeeds" but nothing changes | `devicectl` orientation reportedly ignored on iPhone Duo | Compare screenshot dimensions; if unchanged, ask the user to rotate in Device Hub |
| Screenshot of inner display is black | Device is closed | Read the hinge angle; ask the user to open it |
| Too many generic questions | Asked before gathering evidence | Capture and audit first; only ask what code can't answer |
| A flagged file was never touched | Lost track on a large app | Reconcile the todo coverage list before the report |

## Report

End with a lean numbered summary in full sentences, no phase numbers:

1. **Changed** — files and what changed, grouped by task.
2. **Already correct** — what needed no change.
3. **Decisions** — each decision and whether the user chose it or it was a default (link `DUO_DECISIONS.md`).
4. **TODOs left** — with file:line and reason.
5. **Verified** — poses actually captured (with hinge angles), builds that passed, link to the contact sheet.
6. **Test on a physical iPhone Duo** — camera, capture accessories, haptics, performance, extensions, anything not captured.
7. **App Store** — screenshots produced and where; reminder that iPhone Duo screenshots are required from April 2027.

## User-Facing Interaction Guidelines

- Start with a short briefing: what you'll do, roughly how long, and when you'll need the user (folding the simulator, answering design questions, approving the plan).
- Show progress as `▶ label` when starting a step and `✓ label: outcome` when done.
- Ask questions only at the named points: preflight consent, pose changes, the decision checkpoint, plan approval, and App Store screen selection. Batch related questions; each has a recommended option first.
- Every design question shows the current screenshots, the alternatives, the code locations, and why you recommend one.
- Write in full sentences without internal jargon or phase numbers.
