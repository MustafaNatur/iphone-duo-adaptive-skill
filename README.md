# iPhone Duo Adaptive Skill

An **interactive** agent skill for Claude Code and other agent-skill–compatible tools. It adapts your iOS app to **iPhone Duo**, Apple's foldable iPhone, and verifies the result.

The skill builds your app, screenshots it on the outer and inner displays in every pose, and asks you the design questions only you can answer. Then it makes the changes and proves they work.

> **Status:** in design. The research ([RESOURCES.md](RESOURCES.md)) and the specification ([DESIGN.md](DESIGN.md)) are done, and `SKILL.md` is being written. The sections below describe the planned behaviour.

## What it does

1. **Checks your setup:** Xcode version, iPhone Duo simulator, SDK, deployment target, UIKit / SwiftUI / mixed, and app type.
2. **Screenshots your app as it is now** on both displays: closed, open, rotated and half-folded.
3. **Audits your code** for patterns that break on iPhone Duo (`UIScreen.main`, orientation checks, idiom checks, fixed sizes, custom bars, asymmetric safe-area math) and lists every screen.
4. **Writes a plan** you can edit, and changes nothing until you approve it.
5. **Asks you the design questions**, each with your current screenshots, 2–3 sketched alternatives and a recommended answer. For example:
   - What goes in the second pane on the big screen?
   - Split or overlay arrangement?
   - Sidebar or tab bar?
   - Which toolbar buttons overflow?
   - How do grids handle the fold?
   - Should it support the half-folded "tabletop" position?
   - Camera and game special cases.
   - Do you have Figma designs to build to?
6. **Makes the changes.** It does the mechanical fixes first, then implements your design decisions, with every new API guarded so older iOS versions still build.
7. **Verifies everything:**
   - Rebuilds, including at your minimum deployment target.
   - Re-screenshots every pose.
   - Shows you a before/after comparison.
   - Lists exactly what was and wasn't tested.
8. **Prepares App Store screenshots** for both displays and checks their sizes, format and transparency.
9. **Reports** what changed, what was already correct, what you decided, any TODOs left, and what to test on a real device.

Every answer is saved in `DUO_DECISIONS.md` in your project, so nothing gets redesigned silently. If nobody is around to answer (CI, headless runs, "just do it"), the skill uses safe defaults, marks them as defaults, and leaves clear TODOs.

## Inspired by Apple's own skills

Xcode ships its own agent skills, and this skill follows their design. Its workflow mirrors Apple's `uikit-app-modernization` and `audit-xcode-security-settings`:
- **Workflow:** detection → analysis → decision → implementation → verification.
- **Decision rule:** a safe one-to-one replacement is applied automatically. When there are several valid options, it asks you. When no safe option exists, it leaves an actionable TODO.
- **Plan approval:** you approve the plan before anything changes.
- **Guardrails:** public API only, no invented API, stay in scope.

It also **uses Apple's skills directly.** When Xcode is installed, it exports them at runtime with `xcrun agent skills export` and lets them handle general modernization (UIScreen, orientation, scene lifecycle, safe areas, and App Resizability on Xcode 27.1+). This skill then handles the iPhone Duo–specific work. Apple's skills are never bundled or copied into this repo.

## How it's different

There are already about 30 iPhone Duo skills on GitHub (see [RESOURCES.md §9](RESOURCES.md#9-third-party-coverage-verify-against-apple)). Most are static checklists or cheat sheets. This skill focuses on what they don't do well:

| What none of them do well | What this skill does |
|---|---|
| Checking the result | **Fixes, then screenshots every pose on both displays**, compares before and after, and states which poses were actually tested |
| Getting API names right | Uses only APIs from a list checked against Apple's documentation, and **compiles after every change**. Other skills get some names wrong (e.g. "UIViewReservedRegion") |
| Working with Apple's tools | **Runs Apple's Xcode skills at runtime** and builds on them instead of duplicating or contradicting them |
| Design decisions | **Asks you at a decision checkpoint**, with screenshots, mockups and a recommended answer for each question, and records the answers |
| Shipping | **Produces and validates App Store screenshots** for both displays (required from April 2027) |
| Real-world codebases | Handles **mixed UIKit/SwiftUI apps**, keeps a file-coverage list, and guards every new API so older iOS versions still build |
| Honesty about gaps | States what Apple hasn't documented yet (games, widgets on the outer display, right-to-left layouts with side bars, keyboard at the fold) instead of inventing guidance |

## Simulator note

Apple provides no command-line way to fold the iPhone Duo simulator. Only Device Hub's **Closed / Book / Open** buttons can do it. The skill does everything else itself: create, boot, install, launch, screenshot each display, read the hinge angle and try rotation. For folding, it gives you one-line instructions and checks the hinge angle afterwards to confirm the pose. If you already have the third-party [`hinge`](https://github.com/artemnovichkov/hinge) or [`duoctl`](https://github.com/skarol/duoctl) tools installed, it can use them with your permission.

## What Apple actually requires

- **April 2027:** new App Store submissions must include iPhone Duo screenshots.
- **April 2027:** apps must be built with the iOS 27 SDK or later.
- **Fold-aware adaptive layout:** strongly recommended, but not a dated requirement.

## Requirements

- macOS on Apple silicon with **Xcode 27.1** or later (needed for the iPhone Duo simulator and the iOS 27.1 SDK). Older Xcode versions work in a limited mode: code audit and fixes only.
- An iOS project in UIKit, SwiftUI or both. Flutter, React Native and other cross-platform frameworks are out of scope.

## Repository contents

- [DESIGN.md](DESIGN.md): the skill's specification. Workflow, Apple conventions, decision questions, simulator strategy, file structure, failure modes.
- [RESOURCES.md](RESOURCES.md): all research sources. Apple news, docs, design guidelines, API reference, Tech Talks, WWDC26 sessions, tools, App Store specs, labs, third-party coverage, peer skills, and known unknowns.
