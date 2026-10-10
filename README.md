# Three steps to make your app shine on iPhone Duo

iPhone Duo brings a compact outer display, a large inner display and a fold to iPhone. The iPhone Duo Adaptive skill gives your coding agent everything it needs to bring your app there. It looks at your running app in every pose, asks you the design questions only you can answer, makes the changes, and shows you the result before and after.

It works with Claude Code and other agent-skill–compatible tools, and it builds on the skills Apple ships in Xcode.

> **Status:** version 0.2. Run interactively on a production SwiftUI app on the iPhone Duo simulator with Xcode 27.1. Please report rough edges.

## Before you begin

Install Xcode 27.1 to get the iPhone Duo simulator and the iOS 27.1 SDK. The skill adapts to the tools you have.

##### Xcode 27.1 or later

Full mode. The skill builds your app, runs it on the iPhone Duo simulator, captures every pose, applies changes, verifies them, and prepares App Store screenshots. Apple's App Resizability skill is available and is used first.

##### Xcode 27.0

Limited mode. The skill audits and fixes your code, but can't run the iPhone Duo simulator or compile APIs that are new in iOS 27.1.

##### No Xcode

Audit only. The skill reviews your code and leaves clear TODOs for everything it can't verify.

## Step 1: Install the skill

Clone the repository and copy the skill into your skills folder.

```bash
git clone https://github.com/MustafaNatur/iphone-duo-adaptive-skill.git
cp -R iphone-duo-adaptive-skill/iphone-duo-adaptive ~/.claude/skills/
```

Then open your iOS project and ask your agent to "get my app ready for iPhone Duo."

## Step 2: Answer the design questions

The skill gathers evidence first, so every question it asks is about your app, not a generic checklist.

### See your app as it is today

- **Capture every pose.** The skill builds your app and screenshots both displays. Apple provides no command to fold the simulator, so it asks you to click **Closed**, **Book** or **Open** in Device Hub.
- **Audit the code.** It searches for patterns that break when the window changes size, like `UIScreen.main`, orientation and idiom checks, fixed sizes, custom bars, and sizes that grow with width.
- **Start with Apple's skills.** When Xcode is installed, it exports Apple's own skills with `xcrun agent skills export` and lets them handle general resizing first.

### Decide what changes

- **Get a recommendation for every question.** Each question shows your current screenshots, the alternatives, and a recommended option, for example whether a list and its detail should sit side by side on the inner display.
- **Approve the plan.** Nothing changes until you reply **Run**.
- **Keep a record.** Every answer is saved in `DuoAdaptive/DUO_DECISIONS.md`, marked as yours or as a default.

**Note:** When no one is available to answer, as in CI or a headless run, the skill still repairs layouts that are clearly broken. For anything that would be a redesign, it uses safe defaults and leaves TODOs.

## Step 3: Review and test

The skill applies the changes, then proves they work.

### Make the changes safely

- **Repair what's broken.** An existing layout that breaks at iPhone Duo sizes is fixed while keeping your design, for example header tiles that grow until they push your list off screen.
- **Leave normal iPhones alone.** Today's iPhone layout and behavior stay identical unless you decide otherwise. The skill never unlocks orientation for the whole app to support iPhone Duo; the inner display already ignores the lock.
- **Gate every new API.** Each iOS 27 and 27.1 API goes behind `#available`, so your app keeps its current minimum iOS version.
- **Use only real API.** Every symbol comes from a list checked against Apple's SDK, and the app is compiled after every change.

### Verify the result

- **Compare before and after.** The skill captures the same screens and poses again and builds a side-by-side contact sheet.
- **Know what was tested.** The report lists the poses that were actually captured, and everything that needs a physical iPhone Duo, like the camera and haptics.

## Go further: Stand out on the App Store

**Prepare your screenshots.** Starting in April 2027, apps and games submitted to the App Store need screenshots for iPhone Duo. The skill captures the screens you choose on both displays and checks them against the exact sizes, format and transparency rules. [View screenshot specifications.](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)

**Build with the latest SDK.** Starting in April 2027, apps must be built with the iOS 27 SDK or later. Only apps built with the iOS 27.1 SDK fill the inner display edge to edge and get the side toolbars.

## Why this skill

There are already around 30 iPhone Duo skills on GitHub. Most are checklists. This one is built to finish the job:

- **It looks at your running app**, before and after, in every pose it can capture.
- **It asks before it redesigns**, and records what you decided.
- **It builds on Apple's skills** instead of repeating or contradicting them.
- **It's honest about gaps.** It says what Apple hasn't documented yet, like games, widgets on the outer display, and the keyboard at the fold, instead of guessing.

In an unattended benchmark on a production SwiftUI app, this skill passed 13 of 13 objective checks. A blind reviewer ranked it first of five as "merge as-is", ahead of the two most-starred iPhone Duo skills and a run with no skill. In Tessl's skill review it scored 100%, compared with 93% and 89% for those two skills. This was one app with one run each, so treat the results as indicative.

## Additional resources

- News: [Prepare and submit your apps for iPhone Duo](https://developer.apple.com/news/?id=kkphp5qo)
- Documentation: [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)
- Design: [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)
- Video: [Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/)
- Guide: [Make sure your app is ready](https://developer.apple.com/iphone-duo/prepare/)
- Specification: [DESIGN.md](DESIGN.md), how the skill works and why
- Research: [RESOURCES.md](RESOURCES.md), every source used to build the skill
- Skill: [iphone-duo-adaptive/](iphone-duo-adaptive/), the skill, its references, scripts and templates
