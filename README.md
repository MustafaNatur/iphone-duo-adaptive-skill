# Make your app shine on iPhone Duo

![iPhone Duo](https://developer.apple.com/iphone-duo/images/hero-versatility_2x.jpg)

An interactive agent skill that adapts your iOS app to iPhone Duo, Apple's foldable iPhone. It works with Claude Code and other agent-skill–compatible tools.

## What makes it different

- **It asks before it redesigns.** Every design question shows your current screenshots, the options, and a recommended answer. Your choices are saved in `DuoAdaptive/DUO_DECISIONS.md`.
- **It repairs what's broken.** Layouts that break at iPhone Duo sizes are fixed without changing your design, even when no one is around to answer.
- **It leaves normal iPhones alone.** It never unlocks orientation for the whole app, and every new API is gated so your minimum iOS version stays the same.
- **It builds on Apple's skills.** It runs Apple's own App Resizability skill from Xcode first, then handles what's specific to iPhone Duo.
- **It shows you the result.** It captures your app on both displays before and after, and tells you exactly which poses were tested. You fold the simulator in Device Hub, because Apple has no command for it.
- **It uses only real API.** Every symbol is checked against Apple's SDK, and the app is compiled after every change.
- **It prepares App Store screenshots**, which are required for iPhone Duo starting April 2027.

In a benchmark on a production SwiftUI app, it passed 13 of 13 checks and ranked first in a blind review, ahead of the two most-starred iPhone Duo skills.

## Install

```bash
git clone https://github.com/MustafaNatur/iphone-duo-adaptive-skill.git
cp -R iphone-duo-adaptive-skill/iphone-duo-adaptive ~/.claude/skills/
```

Then ask your agent to "get my app ready for iPhone Duo." Xcode 27.1 is recommended for the iPhone Duo simulator.

## Learn more

- [DESIGN.md](DESIGN.md): how the skill works
- [RESOURCES.md](RESOURCES.md): sources and Apple documentation
- [Apple: Make sure your app is ready](https://developer.apple.com/iphone-duo/prepare/)

_Image © Apple Inc., shown from developer.apple.com._
