# Skill Design

How the iPhone Duo adaptive skill is built and how it behaves. This document is the specification for `SKILL.md` and its reference files. Sources are in [RESOURCES.md](RESOURCES.md).

_Last updated: 2026-10-10_

---

## 1. Principles

1. **Follow Apple's skill conventions.** The skill is modelled on Apple's workflow skills that ship with Xcode, mainly `uikit-app-modernization` and `audit-xcode-security-settings`: the same section order, decision rules, guardrails and reporting style (§3).
2. **Interactive, with a non-interactive fallback.** The skill gathers evidence first, then asks the user the design questions it can't answer from code. The number of questions isn't capped. Every question is grounded in screenshots and code and has a recommended default. When nobody can answer (headless runs, CI, or "just do it"), it uses conservative defaults and leaves actionable TODOs.
3. **Build on Apple's skills; don't copy them.** If Xcode is present, the skill exports Apple's own skills at runtime and defers to them for everything they cover. It never bundles Apple content.
4. **Verify everything.** Every change is compiled. Every screen is screenshotted in every pose before and after, and every API comes from a verified list. The skill never claims something was tested when it wasn't.
5. **Stay in scope.** Make minimal diffs, prefer system containers, and never rewrite a working layout without a user decision.

---

## 2. Workflow

| Phase | What happens | Mode | When nobody can answer |
|---|---|---|---|
| **0. Preflight** | Read Xcode version, iOS 27.1 runtime and iPhone Duo device type, SDK, deployment target, UIKit / SwiftUI / mixed, and app type (standard, camera, game, cross-platform). Export Apple's skills. Check source control. | Auto | Continue with this skill's own guidance and record what's missing |
| **1. Briefing** | Tell the user what will happen, roughly how long it takes, and which steps need them | Auto | — |
| **2. Baseline capture** | Build, install and launch on the iPhone Duo simulator. Screenshot every screen on every display and pose (§5). | Auto, with user help for poses | Static audit only; mark poses as untested |
| **3. Audit & inventory** | Scan for anti-patterns, inventory screens, navigation containers, toolbars and custom layouts, and list everything with file and line | Auto | — |
| **4. Plan** | Write an editable plan (`DUO_PLAN.md`) with checkboxes: mechanical fixes, proposed design changes, open questions | Auto | — |
| **5. Decision checkpoint(s)** | Ask the design questions (§4), showing current screenshots and 2–3 sketched alternatives per screen. The user approves the plan with **Run / Cancel**. | **User** | Apply the defaults and mark them as defaults in `DUO_DECISIONS.md` |
| **6. Mechanical fixes** | Hand off general modernization to Apple's skills (UIScreen, orientation, scene lifecycle, safe areas). Then make the iPhone Duo–specific fixes, guarded with `#available` / SDK checks. | Auto | Apply them, since they're one-to-one replacements |
| **7. Design implementation** | Implement the decisions: split views, arrangement views, sidebar, toolbar priorities, fold handling, camera, games | Auto | Only what the defaults allow; no new `ArrangementView` without a decision |
| **8. Verification** | Rebuild, also at the minimum deployment target. Re-capture every pose, then build a before/after contact sheet. Check the file-coverage list. | Auto, with user help for poses | List what wasn't verified |
| **9. App Store assets** | Capture screenshots for the outer and inner displays and validate size, format and alpha | Auto capture; user picks screens | The root screen of each tab, portrait, both displays |
| **10. Report** | Numbered summary: changed / already correct / decisions made / TODOs left / test on a physical device | Auto | — |

---

## 3. Following Apple's skill conventions

Taken from Apple's skills that ship with Xcode 27.0. Apple's content is not reproduced here.

**Frontmatter**
- `name` matches the folder.
- `description` lists trigger symbols, APIs and user phrasings, has a `SKIP:` list, and names sibling skills.
- Apple uses `effort: high`; the open Agent Skills spec doesn't allow that key, so it lives under `metadata`. The description stays under 1,024 characters.

**SKILL.md sections, in order**
1. Grounding line: public API only; never invent API.
2. Purpose
3. Scope
4. Core Principles: numbered, each a bold rule plus its reason
5. Tool Preferences: Xcode MCP tools first (look up the server prefix in the tool registry, don't guess it); when Bash is allowed
6. Workflow, by phase
7. Task Registry: `| Task | File | Description |`, run top to bottom
8. Common Failure Modes: `| Symptom | Cause | Correct Response |`
9. Report: a short numbered summary
10. User-Facing Interaction Guidelines: complete sentences, no phase numbers or jargon, questions asked only at named points

**Decision rule**
- A safe one-to-one replacement is applied automatically.
- If there are several valid options, ask the user.
- If no safe option exists, or nobody can answer, leave a TODO that says why, gives the fix, and notes any lifecycle or threading concern.
- A TODO alone, without that context, counts as a failure.

**Other conventions**
- **Progress lines:** `▶ label` while working, `✓ label: outcome` when done.
- **Reference files:** each `*-task.md` follows Overview → Detection → Patterns (decision trees) → Implementation Gates → Post-file Checklist → Final Verification → API Reference. Version files open with an **SDK Version** line, and each section ends with an **Availability** line.
- **Load rules:** say explicitly which files must be read and which are read on demand.
- **Code style:** before/after pairs marked `// AVOID:` and `// PREFER:`.
- **Completeness:** keep a file list in the todo tool and use subagents for coverage. Silently skipping a file counts as a failure.

---

## 4. Decision questions

Every question has a recommended option, listed first. The default is what the skill uses when nobody can answer. Questions are asked with the ask-user tool, in batches, after evidence is gathered. The skill never asks something the code already answers.

| # | Question | Options | Default |
|---|---|---|---|
| 1 | How far should we go? | A: readiness only (mechanical fixes, system containers) · B: A + inner-display improvements on top screens · C: full per-screen design pass | B if interactive, A if headless |
| 2 | Deployment target | Keep current minimum and gate new APIs · Raise to iOS 27.1 | Keep and gate |
| 3 | Inner display, per screen | One column with flexible width · List + detail (`NavigationSplitView` / `UISplitViewController`) · `ArrangementView` split (primary + companion) · Overlay arrangement | One column for feeds and articles; split view where list→detail already exists |
| 4 | Extra hierarchy level | Keep tab bar · Sidebar on the inner display (`.defaultTabBarPlacement(.sidebar)`) | Keep tab bar |
| 5 | Toolbar priorities, per screen | The skill proposes pinned / high / overflow items from code | `.automatic`; text items and segmented controls stay horizontal |
| 6 | Tab bar vs. toolbar when space is short | Navigation-focused (keep tabs) · Task-focused (keep toolbar) | Navigation-focused |
| 7 | Custom grids and canvases at the fold | Even column counts via inactive division region · Move key controls off the fold · Leave as is and flag | Even columns for grids |
| 8 | Tabletop (half-folded) layout | No · Yes for media and camera screens | No |
| 9 | Opt out of vertical bars | No · Yes, for single-page utilities only | No |
| 10 | Full-width immersive screens | No · Yes, for non-scrolling visual screens (like Calculator) | No |
| 11 | Camera | Fix preview, rotation and direction only · Also add outer-display `CameraCaptureAccessory` | Fix only |
| 12 | Games | Change aspect ratio · Letterbox with artwork | Change aspect ratio if the engine allows (Apple guidance is thin) |
| 13 | Designs | "Do you have Figma frames (Apple's iPhone Duo kit) or screenshots of the intended design?" · Generate proposals from current UI | Generate proposals; never blocks |
| 14 | App Store screenshots | Which screens, which orientations | Root screen of each tab, portrait, both displays |
| 15 | Hard-to-reach screens | Test account, deep links or launch arguments to reach screens behind login | Skip and mark untested |

**How each question is presented**
- The current screenshot on the outer and inner displays.
- 2–3 sketched alternatives, as ASCII mockups or an HTML contact sheet.
- The code locations involved.
- The recommendation and why.

---

## 5. Simulator strategy

Apple provides **no command line, Xcode agent tool or XCTest API** that folds, unfolds or sets the hinge angle on the iPhone Duo simulator. Only the Device Hub toolbar can do it.

| Action | Method | Who |
|---|---|---|
| Create / boot / install / launch | `xcrun simctl create "iPhone Duo" com.apple.CoreSimulator.SimDeviceType.iPhone-Duo com.apple.CoreSimulator.SimRuntime.iOS-27-1`, then `simctl boot / install / launch` | Skill |
| Screenshot per display | `xcrun simctl io <udid> screenshot --display=primary` (outer) and `--display=primary-1` (inner) | Skill |
| Read the current pose | `xcrun devicectl device motion hinge-angle --device <udid>` (0° closed, ~127° book, 180° open) and `devicectl device info displays` | Skill |
| Rotate | `xcrun devicectl device orientation set <value>` or Xcode MCP `DeviceEventSynthesize orientation <value>`; afterwards check that screenshot dimensions changed | Skill, falls back to the user |
| Fold / unfold / set angle | Device Hub toolbar **Closed / Book / Open**; hold **Option** for the angle slider | **User** |
| Fold via third-party tools | [`hinge`](https://github.com/artemnovichkov/hinge) or [`duoctl`](https://github.com/skarol/duoctl) | Skill, **only if already installed and the user consents** (they use Apple's private interfaces) |

**Instructions the skill gives the user for each pose:**
> In Device Hub, select the iPhone Duo simulator. In the toolbar under the device, click **Closed**, **Book** or **Open**. For an exact angle, hold **Option** and drag the hinge slider. To rotate, use the rotate button or **Controls → Rotate Left/Right**. Reply when done.

The skill then reads back the hinge angle to confirm the pose before capturing.

**Pose matrix:** closed portrait, closed landscape, open portrait, open landscape, book (~127°), and Split View on the inner display if reachable.

**Runtime capability detection**
- `xcrun simctl list devicetypes | grep -i iPhone-Duo`
- `xcrun simctl list runtimes | grep "iOS 27.1"`
- `simctl io <udid> enumerate`: look for `primary-1`
- Grep `devicectl device motion --help` and `simctl help` for fold or posture commands a future Xcode might add.

**The simulator can't test:**
- camera and camera direction changes
- outer-display capture accessories
- haptics, reachability, performance
- StandBy
- most app extensions

The skill reports these as needing a physical iPhone Duo.

**Known simulator caveats**
- The first launch is slow.
- Some third-party tools send taps to the outer screen when the device is open.
- `simctl io screenConfig power off` is not a fold, and can crash SpringBoard.

---

## 6. Using Apple's Xcode skills at runtime

1. Check `xcodebuild -version`.
2. If Xcode is installed, run `xcrun agent skills export --output-dir "$TMPDIR/apple-skills"` and read:
   - `uikit-app-modernization` (UIScreen, orientation, scene lifecycle, safe-area tasks)
   - `swiftui-whats-new-27/references/toolbar.md`
   - **App Resizability** on Xcode 27.1+
   - `device-interaction` for driving the app through Xcode's agent tools
3. Apple's skill wins wherever the two overlap. This skill handles iPhone Duo–specific work: vertical bars, reserved regions, `ArrangementView`, hinge, scene accessories, camera, App Store assets, and the decision workflow.
4. If Xcode is missing or older than 27.1, use this skill's own references and tell the user that Xcode 27.1 adds Apple's App Resizability skill and the iPhone Duo simulator.

---

## 7. File structure

```
iphone-duo-adaptive/
├── SKILL.md                         workflow, principles, task registry, failure modes
├── references/
│   ├── workflow.md                  phase-by-phase instructions (read before Phase 0)
│   ├── apple-skills-bridge.md       export Apple skills, routing, fallbacks
│   ├── resizing-task.md             fallback resizing fundamentals when Apple's skills are unavailable
│   ├── api-facts.md                 verified API table with availability; known unknowns
│   ├── decisions.md                 question bank, heuristics, mockup templates
│   ├── simulator.md                 pose matrix, commands, user instructions, limits
│   ├── availability.md              #available / SDK gating patterns
│   ├── app-store-assets.md          sizes, capture, validation, April 2027 rule
│   ├── vertical-bars-task.md        bar migration task
│   ├── reserved-regions-task.md     fold and camera occlusion task
│   ├── arrangement-task.md          split / overlay / split-view decisions
│   ├── camera-task.md               direction coordinator, rotation, accessories
│   └── special-cases.md             games, hinge effects, scenes, cross-platform (out of scope)
├── scripts/
│   ├── preflight.py                 environment and project facts as JSON
│   ├── export_apple_skills.sh       export Apple skills; non-zero exit → fallback
│   ├── audit.py                     anti-patterns and screen inventory with file:line
│   ├── capture.sh                   build, install, launch, screenshot per pose
│   ├── contact_sheet.py             before/after grid
│   └── check_screenshots.py         App Store size, format and alpha validation
└── assets/
    ├── DUO_PLAN.template.md
    └── DUO_DECISIONS.template.md
```

---

## 8. Common failure modes to design against

| Symptom | Cause | Correct response |
|---|---|---|
| Too many generic questions | Asking before gathering evidence | Capture and audit first; ask only what the code can't answer |
| Code uses an API that doesn't exist | Invented or misspelled API (e.g. "UIViewReservedRegion") | Use only `api-facts.md` and Apple's skills; compile after each change |
| Working layout rewritten | No scope discipline | Minimal diffs; structural change only after a decision |
| Build breaks below iOS 27.1 | Missing `#available` | Gate every new API; build at the minimum deployment target |
| "Tested in all poses" when it wasn't | Fold can't be automated | Read back the hinge angle; list the poses actually captured |
| Layout keyed to hinge angle or pose | Misuse of the hinge API | Hinge is for live effects only; layout uses size classes and reserved regions |
| Conflicts with Apple's guidance | Duplicated advice | Apple's skills win on overlap |
| Context overflow on large apps | Too many files | Use subagents per screen or module; keep a file-coverage list |
