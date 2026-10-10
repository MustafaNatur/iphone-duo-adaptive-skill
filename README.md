# iPhone Duo Adaptive Skill

An **interactive** agent skill for Claude Code and other agent-skill–compatible tools. It adapts your iOS app to **iPhone Duo**, Apple's foldable iPhone, and verifies the result.

The skill builds your app, screenshots it on the outer and inner displays in every pose, and asks you the design questions only you can answer. Then it makes the changes and proves they work.

> **Status:** version 0.2. The skill is written, and its scripts have been tested on sample code. It has **not yet been run end to end** against a real app on the iPhone Duo simulator, which needs Xcode 27.1. Expect rough edges, and please report them.

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

Every answer is saved in `DuoAdaptive/DUO_DECISIONS.md` in your project, so nothing gets redesigned silently. If nobody is around to answer (CI, headless runs, "just do it"), the skill still repairs layouts that are clearly broken on the big display. For anything that would be a redesign, it uses safe defaults, marks them as defaults, and leaves clear TODOs. Normal iPhones never change unless you decide they should.

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

## Evaluation

**Tessl skill review** (`tessl review run quality`, 2026-10-10):

| Skill | Score |
|---|---|
| **This skill** | **100%** (5/5 on all 8 criteria, no validation warnings) |
| mirzaaghazadeh/iphone-duo-skills | 93% for its main readiness skill; its 11 skills average 90.7% |
| d-date/iphone-duo-skill | 89% |

**Benchmark on a real production SwiftUI app.** The prompt was "Get my app ready for iPhone Duo. Make the changes in the code." Each run worked unattended on the iOS 27.0 SDK. Results were graded against 13 objective checks, and a separate blind reviewer ranked them as anonymous pull requests.

| Run | Checks passed | Blind review | Notes |
|---|---|---|---|
| **This skill v0.2** | **13/13** | **1st, 42/50, merge as-is** | Builds; layout repairs; no change on normal iPhones |
| No skill | 10/13 | 5th, 31/50 | Unlocked landscape on every iPhone |
| This skill v0.1 | 12/13 | 3rd, 33/50 | Safe, but left a broken layout as a proposal |
| d-date | 9/13 | 2nd, 36/50 | Unlocked landscape on every iPhone |
| mirzaaghazadeh | 9/13 | 4th, 33/50 | Most ambitious; regressions on Plus/Pro Max phones |

This is one app with one run per contestant, so treat the numbers as indicative. The interactive question flow and the simulator capture weren't exercised, because no user or Xcode 27.1 was available.

## Install

Copy the skill folder into your Claude Code skills directory (personal or per project):

```bash
git clone https://github.com/MustafaNatur/iphone-duo-adaptive-skill.git
cp -R iphone-duo-adaptive-skill/iphone-duo-adaptive ~/.claude/skills/
```

Then, in your iOS project, ask: *"Get my app ready for iPhone Duo."*

## Repository contents

- [iphone-duo-adaptive/](iphone-duo-adaptive/): the skill. `SKILL.md`, task and reference files, helper scripts, and plan/decision templates.
- [DESIGN.md](DESIGN.md): the skill's specification. Workflow, Apple conventions, decision questions, simulator strategy, file structure, failure modes.
- [RESOURCES.md](RESOURCES.md): all research sources. Apple news, docs, design guidelines, API reference, Tech Talks, WWDC26 sessions, tools, App Store specs, labs, third-party coverage, peer skills, and known unknowns.
