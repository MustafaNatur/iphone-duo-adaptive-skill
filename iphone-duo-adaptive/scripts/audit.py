#!/usr/bin/env python3
"""Static audit for iPhone Duo readiness. Read-only, pattern based.

Usage: python3 audit.py <project-dir> [--json out.json] [--md out.md]

Findings are candidates: confirm each one by reading the code. Lines inside
comments are skipped; `#if 0`/`#if false` blocks are not, so check those.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

SKIP_DIRS = {"Pods", "Carthage", ".build", "DerivedData", "DuoAdaptive", "node_modules", ".git", "Tests"}
EXT = (".swift", ".m", ".mm", ".h")

# (rule id, regex, severity, task file, message)
RULES = [
    ("uiscreen-main", r"UIScreen\.main\b|UIScreen\.mainScreen|\[UIScreen mainScreen\]", "fix",
     "resizing-task.md#1", "Sizing/scale from the main screen; use view/scene bounds or traitCollection.displayScale"),
    ("window-frame", r"UIWindow\(\s*frame:", "fix",
     "resizing-task.md#3", "Window created from a frame; use UIWindow(windowScene:)"),
    ("orientation", r"UIDevice\.current\.orientation|\[\[UIDevice currentDevice\] orientation\]|statusBarOrientation|\binterfaceOrientation\b",
     "fix", "resizing-task.md#5", "Orientation used (possibly for layout); compare available bounds or size classes"),
    ("idiom", r"userInterfaceIdiom\s*==|UI_USER_INTERFACE_IDIOM\(\)|\.userInterfaceIdiom\s*\{|case \.pad\b", "review",
     "resizing-task.md#6", "Idiom check; if it drives layout, use size classes / available space"),
    ("fixed-size", r"\b(height|width)\s*(==|>=|<=|>|<)\s*(568|667|736|812|844|852|874|896|926|932|956)\b|\b(375|390|393|402|414|428|430|440)\s*\)?\s*$",
     "review", "resizing-task.md#6", "Device-size constant; derive from available space instead"),
    ("symmetric-safe-area", r"safeAreaInsets\.(left|right)\s*\*\s*2|2\s*\*\s*[\w.]*safeAreaInsets\.(left|right)", "fix",
     "resizing-task.md#7", "Assumes symmetric safe area; use bounds.inset(by: safeAreaInsets)"),
    ("custom-bar", r"\b(UIToolbar|UINavigationBar|UITabBar)\s*\(|\[\[(UIToolbar|UINavigationBar|UITabBar) alloc\]", "fix",
     "vertical-bars-task.md#1", "Standalone bar; it won't move to the vertical axis. Use the container's bars"),
    ("custom-view-item", r"UIBarButtonItem\(\s*customView:|initWithCustomView:", "review",
     "vertical-bars-task.md#4", "Custom-view bar item never goes vertical unless axisBehavior allows it"),
    ("title-only-item", r"UIBarButtonItem\(\s*title:(?![^)]*image:)|initWithTitle:[^\]]*style:", "review",
     "vertical-bars-task.md#3", "Title-only bar item; add an SF Symbol so it can appear vertically"),
    ("swiftui-text-toolbar-item", r"ToolbarItem[^{]*\{\s*Button\(\s*\"[^\"]+\"\s*\)", "review",
     "vertical-bars-task.md#3", "Toolbar button with a title but no systemImage"),
    ("custom-overflow", r"systemName:\s*\"ellipsis(\.circle)?\"|systemImage:\s*\"ellipsis(\.circle)?\"", "review",
     "vertical-bars-task.md#5", "App-made overflow menu; consider ToolbarOverflowMenu / additionalOverflowItems"),
    ("bar-assumption", r"navigationBar\.frame\.(size\.)?height|tabBar\.frame\.(size\.)?height|toolbar\.frame\.(size\.)?height", "review",
     "vertical-bars-task.md#6", "Layout assumes horizontal bar height; use safe areas"),
    ("custom-layout", r":\s*Layout\s*\{|struct \w+\s*:\s*(\w+,\s*)*Layout\b", "review",
     "reserved-regions-task.md#1", "Custom Layout; check content vs. fold/camera reserved regions"),
    ("manual-frame", r"\.frame\s*=\s*CGRect\(|\.position\(\s*x:|setFrame:", "review",
     "reserved-regions-task.md#2", "Manual positioning; check against reserved regions"),
    ("grid-columns", r"GridItem\(|UICollectionViewCompositionalLayout|NSCollectionLayoutGroup", "review",
     "reserved-regions-task.md#3", "Grid; prefer even column counts when a fold exists"),
    ("ignores-safe-area", r"\.ignoresSafeArea\(|\.edgesIgnoringSafeArea\(", "review",
     "reserved-regions-task.md#1", "Ignores safe area; fine for backgrounds, not for interactive content"),
    ("width-derived-size", r"\.width\s*/\s*2|width\s*\*\s*0?\.5|\.aspectRatio\(\s*1(\.0)?\s*,|containerRelativeFrame\(", "review",
     "resizing-task.md#9", "Size derived from width; may grow huge on the inner display (layout repair)"),
    ("orientation-lock", r"UIInterfaceOrientationMaskPortrait\b|supportedInterfaceOrientations", "review",
     "availability.md#info-plist", "Orientation lock: inner display ignores it; do not unlock app-wide as a Duo fix"),
    ("full-bleed", r"\.scaleAspectFill|contentMode:\s*\.fill|\.aspectRatio\([^)]*\.fill", "review",
     "resizing-task.md#8", "Fill content mode; may crop on wide/near-square displays"),
    ("camera-discovery", r"AVCaptureDevice\.DiscoverySession|AVCaptureDevice\.default\(|AVCaptureDeviceDiscoverySession", "review",
     "camera-task.md#1", "Camera discovery; check facing direction on iPhone Duo"),
    ("camera-position-logic", r"\.position\s*==\s*\.(front|back)|AVCaptureDevicePosition(Front|Back)", "review",
     "camera-task.md#2", "Uses camera position for logic; on iPhone Duo position != facing direction"),
    ("camera-rotation", r"videoOrientation|videoRotationAngle", "review",
     "camera-task.md#3", "Manual camera rotation; consider AVCaptureDevice.RotationCoordinator"),
    ("hinge-for-layout", r"onHingeChange|UIHingeInteraction", "review",
     "special-cases.md#hinge-driven-effects", "Hinge API in use; it must not drive layout"),
    ("misspelled-api", r"\bUIViewReservedRegion\b", "fix",
     "api-facts.md", "Not an API: the UIKit type is UIView.ReservedRegion"),
]

SCREEN_PATTERNS = {
    "swiftui_view": re.compile(r"struct\s+(\w+)\s*:\s*(?:[\w.]+\s*,\s*)*View\b"),
    "uikit_vc": re.compile(r"class\s+(\w+)\s*:\s*(\w*ViewController)\b"),
    "objc_vc": re.compile(r"@interface\s+(\w+)\s*:\s*(\w*ViewController)\b"),
}
CONTAINERS = re.compile(r"\b(NavigationStack|NavigationSplitView|NavigationView|TabView|UINavigationController|"
                        r"UISplitViewController|UITabBarController|ArrangementView|UIArrangementViewController)\b")
TOOLBAR = re.compile(r"\.toolbar\s*\{|toolbarItems\s*=|navigationItem\.(right|left)BarButtonItems?|ToolbarItem")
COMMENT_LINE = re.compile(r"^\s*(//|/\*|\*)")


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith("Tests") and not d.endswith(".xcassets")]
        for f in filenames:
            if f.endswith(EXT):
                yield os.path.join(dirpath, f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--json")
    ap.add_argument("--md")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    compiled = [(rid, re.compile(rx), sev, task, msg) for rid, rx, sev, task, msg in RULES]

    findings, screens = [], []
    containers = Counter()
    for path in iter_files(root):
        rel = os.path.relpath(path, root)
        try:
            lines = open(path, errors="ignore").read().splitlines()
        except OSError:
            continue
        text = "\n".join(lines)
        for i, line in enumerate(lines, 1):
            if COMMENT_LINE.match(line):
                continue
            for rid, rx, sev, task, msg in compiled:
                if rx.search(line):
                    findings.append({"rule": rid, "severity": sev, "file": rel, "line": i,
                                     "code": line.strip()[:160], "task": task, "message": msg})
        for kind, rx in SCREEN_PATTERNS.items():
            for m in rx.finditer(text):
                screens.append({"name": m.group(1), "kind": kind, "file": rel,
                                "has_toolbar": bool(TOOLBAR.search(text)),
                                "containers": sorted(set(CONTAINERS.findall(text)))})
        containers.update(CONTAINERS.findall(text))

    by_rule = Counter(f["rule"] for f in findings)
    by_file = defaultdict(list)
    for f in findings:
        by_file[f["file"]].append(f)
    result = {"root": root, "summary": {"findings": len(findings), "files": len(by_file),
                                        "by_rule": dict(by_rule.most_common()),
                                        "containers": dict(containers.most_common()),
                                        "screens": len(screens)},
              "findings": findings, "screens": screens}

    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        json.dump(result, open(a.json, "w"), indent=2)

    md = ["# iPhone Duo audit", "",
          f"{len(findings)} candidate findings in {len(by_file)} files; {len(screens)} screens. "
          "Candidates only: confirm each in code.", "", "## By rule", "", "| Rule | Count | Task |", "|---|---|---|"]
    task_of = {r[0]: r[3] for r in RULES}
    for rid, n in by_rule.most_common():
        md.append(f"| `{rid}` | {n} | {task_of[rid]} |")
    md += ["", "## Containers in use", ""]
    md += [f"- {c}: {n}" for c, n in containers.most_common()] or ["- none found"]
    md += ["", "## Findings by file", ""]
    for file in sorted(by_file):
        md.append(f"### {file}")
        for f in by_file[file]:
            md.append(f"- [{f['severity']}] `{f['rule']}` L{f['line']}: `{f['code']}` - {f['message']}")
        md.append("")
    md += ["## Screens", "", "| Screen | Kind | File | Toolbar | Containers |", "|---|---|---|---|---|"]
    for s in screens:
        md.append(f"| {s['name']} | {s['kind']} | {s['file']} | {'yes' if s['has_toolbar'] else ''} | {', '.join(s['containers'])} |")
    report = "\n".join(md) + "\n"
    if a.md:
        os.makedirs(os.path.dirname(os.path.abspath(a.md)), exist_ok=True)
        open(a.md, "w").write(report)
    if not a.json and not a.md:
        sys.stdout.write(report)
    else:
        print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
