# Apple Skills Bridge

Xcode ships Apple-written agent skills. This skill does not copy them; it exports them at runtime and defers to them.

## Export

```bash
bash <skill>/scripts/export_apple_skills.sh            # prints the export dir on success
```

The script runs `xcrun agent skills export --output-dir "$TMPDIR/apple-agent-skills"` and lists what was exported. Exit codes: `0` exported, `2` Xcode/xcrun not found, `3` export command not supported by this Xcode.

## What to use

| Apple skill | Use it for | Notes |
|---|---|---|
| **App Resizability** (Xcode 27.1+; prompt in Xcode: "get my app ready for iPhone Duo") | General resizing and iPhone Duo readiness | Exported folder name not yet confirmed; look for a folder whose `SKILL.md` description mentions resizing or iPhone Duo |
| `uikit-app-modernization` | `UIScreen.main`, `interfaceOrientation`, app→scene lifecycle, asymmetric safe areas (UIKit) | Has its own task files (`uiscreen-task`, `orientation-task`, `scene-lifecycle-task`, `safe-area-task`) and strict rules; follow them as written |
| `swiftui-whats-new-27` → `references/toolbar.md` | iOS 27 SwiftUI toolbar APIs | Read before `vertical-bars-task.md` in SwiftUI code |
| `swiftui-specialist` | General SwiftUI correctness/performance | Consult when touching SwiftUI views |
| `device-interaction` | Driving the app through Xcode's MCP tools (install/run, screenshots, taps, orientation) | Only works when Xcode's MCP tools are connected |

Read each relevant exported `SKILL.md` fully before using it. Skill names can change between Xcode versions: match by description, not only by folder name.

## Precedence

1. The user's explicit instruction.
2. Apple's exported skill, for anything it covers.
3. This skill.

If Apple's skill and this one disagree, follow Apple's and mention the difference in the report.

## Fallbacks

| Situation | Do this |
|---|---|
| Exit 2 (no Xcode) | Limited mode: static audit and code changes only, using `resizing-task.md`; tell the user verification needs Xcode 27.1 |
| Exit 3 (export unsupported) | Use this skill's references; mention that newer Xcode ships Apple's skills |
| Xcode 27.0 (no App Resizability) | Use `uikit-app-modernization` + this skill; recommend Xcode 27.1 |
| Export produced no relevant skill | Use `resizing-task.md` |

Never copy exported Apple files into the user's repository.
