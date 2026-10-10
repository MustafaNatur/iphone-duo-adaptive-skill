# iPhone Duo Adaptive Skill

An agent skill (for Claude Code and other agent-skill–compatible tools) that helps adapt iOS apps to **iPhone Duo**, Apple's foldable iPhone. It covers resizing, size classes, vertical bars, reserved regions (the fold and the cameras), `ArrangementView`, scenes and camera handling, and App Store assets.

> **Status:** research phase. The skill itself hasn't been written yet.

## What Apple actually requires

- **April 2027:** new App Store submissions must include iPhone Duo screenshots.
- **April 2027:** apps must be built with the iOS 27 SDK or later.
- **Fold-aware adaptive layout:** strongly recommended, but not a dated requirement.

See [RESOURCES.md](RESOURCES.md) for the sources.

## Contents

- [RESOURCES.md](RESOURCES.md): all research sources. Apple news, docs, design guidelines, API reference, Tech Talks, WWDC26 sessions, tools, App Store specs, labs, third-party coverage, peer skills, and known unknowns.

## Design decisions for the skill

- **Use Apple's Xcode skills; don't bundle them.** Xcode ships its own agent skills: `uikit-app-modernization` and `swiftui-whats-new-27` in Xcode 27.0, and "App Resizability" in Xcode 27.1. These are Apple's content, so this repo doesn't redistribute them. Instead, the skill should tell the agent to:
  1. Check whether Xcode is installed (`xcodebuild -version`).
  2. If it is, export the skills with `xcrun agent skills export --output-dir <tmp-dir>` and read the relevant ones: `uikit-app-modernization` for UIScreen, orientation, scene lifecycle and safe areas, `swiftui-whats-new-27/references/toolbar.md`, and App Resizability on Xcode 27.1+.
  3. Follow Apple's skill for anything it covers, and use this skill for iPhone Duo–specific work: vertical bars, reserved regions, `ArrangementView`, hinge, scene accessories, camera, and App Store assets.
  4. If Xcode isn't available, or is older than 27.1, fall back to this skill's own guidance and tell the user that installing Xcode 27.1 gives access to Apple's App Resizability skill.
