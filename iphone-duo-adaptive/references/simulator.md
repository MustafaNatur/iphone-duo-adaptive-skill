# iPhone Duo Simulator

**Requires:** Xcode 27.1+, iOS 27.1 simulator runtime, Apple silicon Mac on macOS 26.6+.

Apple provides **no command line, Xcode MCP tool or XCTest API that folds the simulator**. Only Device Hub's toolbar (**Closed / Book / Open**, Option for an angle slider) can. Everything else can be automated. Several identifiers below come from third-party reports and are **detected at run time**, not assumed.

## Detect

```bash
xcrun simctl list devicetypes | grep -i "duo"           # expect …SimDeviceType.iPhone-Duo
xcrun simctl list runtimes | grep -i "iOS 27.1"          # expect …SimRuntime.iOS-27-1
xcrun simctl list devices | grep -i "duo"                # existing devices
xcrun devicectl device motion --help 2>&1 | grep -iE "hinge|fold|posture"
xcrun simctl help 2>&1 | grep -iE "hinge|fold|posture"   # a future Xcode may add a fold command
```

Use the exact identifiers printed; don't hard-code them if they differ.

## Create & boot

```bash
# Only if no iPhone Duo device exists. Runtime download (~8 GB) needs the user's consent:
#   xcodebuild -downloadPlatform iOS
UDID=$(xcrun simctl create "iPhone Duo (DuoAdaptive)" <devicetype-id> <runtime-id>)
xcrun simctl boot "$UDID"
open -a Simulator --args -CurrentDeviceUDID "$UDID"     # or select it in Device Hub
```

First launch can take several minutes (known issue). StandBy and most app extensions don't run in this runtime.

## Build & launch

`scripts/capture.sh` wraps these steps:

```bash
xcodebuild -scheme <Scheme> [-workspace X.xcworkspace | -project X.xcodeproj] \
  -destination "platform=iOS Simulator,id=$UDID" \
  -derivedDataPath DuoAdaptive/DerivedData build
APP=$(find DuoAdaptive/DerivedData/Build/Products -name "*.app" -path "*iphonesimulator*" | head -1)
BUNDLE_ID=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$APP/Info.plist")
xcrun simctl install "$UDID" "$APP"
xcrun simctl launch "$UDID" "$BUNDLE_ID" [launch args for deep screens]
```

Prefer Xcode's MCP tools (via Apple's `device-interaction` skill) when connected: they install, run, tap, and rotate without the CLI.

## Read the current pose

```bash
xcrun devicectl device motion hinge-angle --device "$UDID" --timeout 5   # 0° closed · ~127° book · 180° open
xcrun devicectl device info displays --device "$UDID"
xcrun simctl io "$UDID" enumerate                                        # lists displays (look for a second one)
```

If `hinge-angle` isn't available, infer the pose from which display returns a non-black screenshot and from its dimensions, and say the pose is inferred.

## Screenshot each display

```bash
xcrun simctl io "$UDID" screenshot --display=<outer-id> outer.png
xcrun simctl io "$UDID" screenshot --display=<inner-id> inner.png
```

Reported display ids: `primary` (outer) and `primary-1` (inner). Confirm with `simctl io enumerate`. The inner display is black while closed. Check every image isn't blank before saving it as evidence.

## Rotate

Try automation, then verify:

```bash
xcrun devicectl device orientation set landscapeLeft --device "$UDID"
```

Or Xcode MCP `DeviceEventSynthesize` with `orientation landscapeLeft` when connected. Take a screenshot; if the pixel dimensions didn't swap, rotation didn't happen (reported on iPhone Duo) → ask the user.

## Fold / unfold — ask the user

Say, once per pose:

> Please set the simulator to **<Closed | Book | Open>**: in Device Hub, select the iPhone Duo simulator and click **<Closed | Book | Open>** in the toolbar under the device. <If landscape:> Then rotate it with the rotate button or **Controls → Rotate Left**. Reply "done" when it's set.

Then read the hinge angle and check it matches (Closed ≈ 0°, Book ≈ 110–150°, Open ≈ 180°). If it doesn't, ask again; never capture a pose you haven't confirmed.

**Third-party fold tools** — [`hinge`](https://github.com/artemnovichkov/hinge) and [`duoctl`](https://github.com/skarol/duoctl) claim to fold the simulator from the command line using Apple's private interfaces. Only if `command -v hinge` or `command -v duoctl` succeeds **and** the user agrees, use them, and still confirm with the hinge angle. Never install them yourself.

## Pose matrix

| Pose | Displays to capture | Why |
|---|---|---|
| Closed, portrait | outer | Compact layout; vertical bars |
| Closed, landscape | outer | If the app supports landscape |
| Open, portrait | inner | Regular × regular; horizontal bars |
| Open, landscape | inner | Vertical bars on the inner display |
| Book (~127°), portrait | inner | Active fold division; arrangements |
| Split View (optional) | inner | Asymmetric bars/safe areas; ask the user to drag a second app in |

Capture each screen from the screen list in each pose. Name files `<pose>/<display>-<screen>.png`.

## Can't be tested in the simulator

Camera and camera direction changes; outer-display capture accessories; haptics; touch reachability; performance; StandBy; most app extensions. Put these in the report under "Test on a physical iPhone Duo".

## Tooling caveats

- `simctl io … screenConfig power off` is **not** a fold and has crashed SpringBoard.
- Some third-party automation tools send taps to the outer display while the device is open; prefer Xcode's MCP tools or manual taps for inner-display interaction.
