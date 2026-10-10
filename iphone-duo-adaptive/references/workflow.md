# Workflow

Read this file fully before Phase 0. Phases run in order. Keep a todo list with one item per phase and, from Phase 3 on, one item per flagged file.

All artifacts go in `DuoAdaptive/` at the project root. Don't commit it and don't put files in the project root. At the end, offer to move `DUO_DECISIONS.md` into the repo (e.g. `docs/`) if the user wants it under version control; suggest adding `DuoAdaptive/` to `.gitignore`:

```
DuoAdaptive/
├── preflight.json
├── audit.json, audit.md
├── baseline/<pose>/<display>-<screen>.png
├── after/<pose>/<display>-<screen>.png
├── contact-sheet.html
├── appstore/<display>-<orientation>-<n>.png
├── DUO_PLAN.md        (user-editable plan)
└── DUO_DECISIONS.md   (decision record)
```

---

## Phase 0: Preflight

1. Run `python3 <skill>/scripts/preflight.py <project-dir> > DuoAdaptive/preflight.json`. It reports Xcode version, iOS 27.1 SDK/runtime, iPhone Duo device type, git state, project/workspace, schemes, deployment target, UI framework mix, and app-type signals.
2. Run `bash <skill>/scripts/export_apple_skills.sh` and follow `references/apple-skills-bridge.md`.
3. Act on the results:

| Finding | Action |
|---|---|
| Xcode < 27.1 or no iOS 27.1 SDK | Tell the user. Offer **limited mode**: audit + fixes that don't need 27.1 APIs, no simulator capture. Recommend installing Xcode 27.1. |
| iOS 27.1 simulator runtime missing | Ask before downloading (about 8 GB): `xcodebuild -downloadPlatform iOS`. If declined, limited mode. |
| No iPhone Duo simulator device | Create one (see `simulator.md`); no consent needed, it's local and removable. |
| Uncommitted changes | Ask: commit/stash first (recommended), continue anyway, or stop. Never stash or commit on your own. |
| Not a git repo | Warn that changes can't be easily reverted; ask to continue. |
| Flutter / React Native / Capacitor / MAUI / web wrapper | Stop and explain this skill is for native iOS code. |
| Game engine (Metal-only, SpriteKit, SceneKit, Unity export) | Continue; load `special-cases.md` → Games. |
| Camera capture found | Note it; `camera-task.md` becomes active. |
| Multiple app targets / schemes | Ask which scheme to adapt (recommend the main app scheme). |

## Phase 1: Briefing

Tell the user, in a few sentences:
- What you'll do: capture the app on both displays, audit, propose a plan, ask design questions, apply changes, verify, and prepare App Store screenshots.
- What you need from them: switching the simulator between Closed, Book and Open in Device Hub (Apple has no command for it), answering design questions, approving the plan.
- Whether you're in full or limited mode, and why.
- Ask whether they have designs (Figma frames from Apple's iPhone Duo kit, mockups) or a test account for screens behind login. Neither blocks the run.

## Phase 2: Baseline capture

1. Build for the iPhone Duo simulator (see `simulator.md` → Build & launch). If the build fails **before** any change, fix only what blocks building with the 27.1 SDK, or fall back to a static audit and tell the user.
2. Decide the screen list: root screen of each tab/sidebar item plus screens the user names, plus screens with custom layout found later by the audit. Reach deeper screens via deep links, launch arguments, or Xcode's `device-interaction` tools; never guess credentials.
3. Capture the pose matrix in `simulator.md` into `DuoAdaptive/baseline/`. For each pose: ask the user to set it, confirm with the hinge angle, then capture each screen on the visible display(s).
4. Describe what you see per screen and pose: letterboxing, clipped content, controls under the fold or camera, bars that stayed horizontal, single-column layouts stretched across the inner display, broken sheets or popovers.

## Phase 3: Audit & inventory

1. Run `python3 <skill>/scripts/audit.py <project-dir> --json DuoAdaptive/audit.json --md DuoAdaptive/audit.md`.
2. Read `audit.md`. For every finding, open the code and confirm it (the scanner is pattern-based and has false positives, e.g. `UIScreen.main` inside a comment or `#if false`).
3. Build the **screen inventory**: for each screen, its container (NavigationStack / NavigationSplitView / TabView / UINavigationController / UISplitViewController / UITabBarController / custom), its bars and items, custom layout code, and full-bleed media.
4. Add every flagged file to the todo list.

## Phase 4: Plan

Create `DuoAdaptive/DUO_PLAN.md` from `assets/DUO_PLAN.template.md`:
- **Mechanical fixes** — each finding, file:line, the planned replacement, and the task file that covers it.
- **Layout repairs** — every existing layout that breaks in a baseline capture or by reading the code at regular width (inner display) or a near-square size: what breaks, the design-preserving repair, and proof that compact iPhones stay identical.
- **Proposed design changes** — per screen, the recommended option and alternatives (these become questions).
- **Open questions** — anything only the user can answer.
- **Out of scope / not verifiable** — e.g. camera on hardware.

## Phase 5: Decision checkpoint

1. Load `references/decisions.md`.
2. Drop questions the evidence already answers (e.g. no camera code → no camera question). Ask the rest in batches of related questions, each with screenshots, sketched alternatives (ASCII or `contact-sheet.html`), code locations, and a recommendation.
3. Record every answer in `DuoAdaptive/DUO_DECISIONS.md` (from `assets/DUO_DECISIONS.template.md`) as **chosen by user** or **default**.
4. Update `DuoAdaptive/DUO_PLAN.md`, show the summary, and ask: **Run** (recommended) / **Edit the plan first** / **Cancel**. Change nothing before **Run**.

## Phase 6: Mechanical fixes & layout repairs

1. If Apple's `uikit-app-modernization` (or App Resizability) skill is available, run its tasks first, on this project, following its own rules.
2. Then run each active task file from the registry in order, file by file. After each file: build, tick the todo item.
3. Apply every layout repair from the plan (`resizing-task.md` §9). These are not optional and don't need a decision.
4. Every new API goes behind an availability guard (`availability.md`, `api-facts.md`).

## Phase 7: Design implementation

Implement each recorded decision using `arrangement-task.md`, `vertical-bars-task.md`, `reserved-regions-task.md`, `camera-task.md` or `special-cases.md`. Keep diffs minimal: wrap existing views rather than rewriting them. If implementation reveals a new design question, ask it (or use the default and record it).

## Phase 8: Verification

1. Build at the current deployment target and run any existing unit/UI tests.
2. **Normal-iPhone check:** re-read every diff hunk and confirm compact-width iPhones keep today's layout and behavior (orientation, navigation, sheets). If a non-Duo iPhone simulator is installed and it isn't the user's own in-use device, launch there and compare. Revert anything that changes normal iPhones without a decision.
3. Recapture the same screens and poses into `DuoAdaptive/after/`.
4. Run `python3 <skill>/scripts/contact_sheet.py DuoAdaptive/baseline DuoAdaptive/after -o DuoAdaptive/contact-sheet.html` and review every pair yourself before showing it.
5. Reconcile the todo list: every flagged file ends as changed / already correct / TODO with reason / out of scope with reason.

## Phase 9: App Store assets

Follow `references/app-store-assets.md`. Ask which screens to use (default: root screen of each tab, portrait, both displays).

## Phase 10: Report

Use the Report format in `SKILL.md`. Link `DuoAdaptive/DUO_DECISIONS.md`, `DuoAdaptive/DUO_PLAN.md`, the contact sheet, and the App Store folder.
