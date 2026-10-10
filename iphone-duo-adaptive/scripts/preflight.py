#!/usr/bin/env python3
"""Read-only preflight for the iPhone Duo adaptive skill.

Usage: python3 preflight.py [project-dir]  -> JSON facts on stdout.
"""
import json
import os
import re
import shutil
import subprocess
import sys

SKIP_DIRS = {"Pods", "Carthage", ".build", "DerivedData", "DuoAdaptive", "node_modules", ".git"}
SOURCE_EXT = (".swift", ".m", ".mm", ".h")


def run(*cmd, timeout=60):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def version_at_least(text, major, minor):
    for m in re.finditer(r"(\d+)\.(\d+)", text):
        if (int(m.group(1)), int(m.group(2))) >= (major, minor):
            return True
    return False


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith((".xcassets", ".lproj"))]
        yield dirpath, dirnames, filenames


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    out = {"project_dir": root}

    # Toolchain
    rc, xv = run("xcodebuild", "-version")
    lines = xv.splitlines()
    out["xcode"] = {
        "installed": rc == 0,
        "version": lines[0].split()[-1] if rc == 0 and lines else None,
        "build": lines[1].split()[-1] if rc == 0 and len(lines) > 1 else None,
    }
    _, sdks = run("xcodebuild", "-showsdks")
    sim_sdks = sorted(set(re.findall(r"iphonesimulator(\d+\.\d+)", sdks)))
    out["iphonesimulator_sdks"] = sim_sdks
    out["has_ios_27_1_sdk"] = any(version_at_least(v, 27, 1) for v in sim_sdks)

    _, runtimes = run("xcrun", "simctl", "list", "runtimes")
    ios_rt = [l.strip() for l in runtimes.splitlines() if l.strip().startswith("iOS")]
    out["ios_runtimes"] = ios_rt
    out["has_ios_27_1_runtime"] = any(version_at_least(l.split("(")[0], 27, 1) for l in ios_rt)

    _, dtypes = run("xcrun", "simctl", "list", "devicetypes")
    out["duo_device_types"] = [l.strip() for l in dtypes.splitlines() if "duo" in l.lower()]
    _, devs = run("xcrun", "simctl", "list", "devices")
    out["duo_devices"] = [l.strip() for l in devs.splitlines() if "duo" in l.lower()]

    out["fold_cli"] = [c for c in ("hinge", "duoctl") if shutil.which(c)]
    _, h1 = run("xcrun", "simctl", "help")
    _, h2 = run("xcrun", "devicectl", "device", "motion", "--help")
    out["fold_or_hinge_hints"] = [l.strip() for l in (h1 + h2).splitlines()
                                  if re.search(r"fold|posture|hinge", l, re.I)][:8]

    # Git
    rc, _ = run("git", "-C", root, "rev-parse", "--is-inside-work-tree")
    git = {"is_repo": rc == 0}
    if rc == 0:
        _, br = run("git", "-C", root, "rev-parse", "--abbrev-ref", "HEAD")
        _, st = run("git", "-C", root, "status", "--porcelain")
        git.update(branch=br.strip(), dirty=bool(st.strip()))
    out["git"] = git

    # Project layout
    workspaces, projects, plists = [], [], []
    counts = {"swift": 0, "objc": 0, "swiftui": 0, "uikit": 0, "camera": 0, "game": 0, "hinge_or_duo_api": 0}
    scene_manifest = False
    for dirpath, dirnames, filenames in walk(root):
        for d in list(dirnames):
            if d.endswith(".xcodeproj"):
                projects.append(os.path.relpath(os.path.join(dirpath, d), root))
                pbx = os.path.join(dirpath, d, "project.pbxproj")
                try:
                    if "UIApplicationSceneManifest_Generation = YES" in open(pbx, errors="ignore").read():
                        scene_manifest = True
                except OSError:
                    pass
                dirnames.remove(d)
            elif d.endswith(".xcworkspace"):
                workspaces.append(os.path.relpath(os.path.join(dirpath, d), root))
                dirnames.remove(d)
        for f in filenames:
            path = os.path.join(dirpath, f)
            if f.endswith(".plist"):
                plists.append(path)
                try:
                    if "UIApplicationSceneManifest" in open(path, errors="ignore").read():
                        scene_manifest = True
                except OSError:
                    pass
            if not f.endswith(SOURCE_EXT):
                continue
            if f.endswith(".swift"):
                counts["swift"] += 1
            elif f.endswith((".m", ".mm")):
                counts["objc"] += 1
            try:
                text = open(path, errors="ignore").read()
            except OSError:
                continue
            if "import SwiftUI" in text:
                counts["swiftui"] += 1
            if re.search(r"import UIKit|#import <UIKit", text):
                counts["uikit"] += 1
            if re.search(r"AVCaptureSession|AVCaptureDevice|AVCaptureVideoPreviewLayer", text):
                counts["camera"] += 1
            if re.search(r"import (SpriteKit|SceneKit|MetalKit|GameController|RealityKit)", text):
                counts["game"] += 1
            if re.search(r"ArrangementView|reservedRegions|onHingeChange|toolbarVerticalBehavior|UIHingeInteraction", text):
                counts["hinge_or_duo_api"] += 1
    out["workspaces"] = sorted(workspaces)
    out["projects"] = sorted(projects)
    out["swift_package"] = os.path.exists(os.path.join(root, "Package.swift"))
    out["files"] = counts
    out["ui_framework"] = ("mixed" if counts["swiftui"] and counts["uikit"] else
                           "swiftui" if counts["swiftui"] else "uikit" if counts["uikit"] else "unknown")
    out["scene_manifest"] = scene_manifest

    # Schemes and deployment targets from the first project/workspace
    schemes, targets = [], set()
    container = (["-workspace", os.path.join(root, workspaces[0])] if workspaces else
                 ["-project", os.path.join(root, projects[0])] if projects else None)
    if container:
        _, lst = run("xcodebuild", "-list", *container, timeout=120)
        m = re.search(r"Schemes:\n((?:\s+.+\n?)+)", lst)
        if m:
            schemes = [s.strip() for s in m.group(1).splitlines() if s.strip()]
    for p in projects:
        try:
            pbx = open(os.path.join(root, p, "project.pbxproj"), errors="ignore").read()
            targets.update(re.findall(r"IPHONEOS_DEPLOYMENT_TARGET = ([0-9.]+)", pbx))
        except OSError:
            pass
    out["schemes"] = schemes
    out["deployment_targets"] = sorted(targets)

    cross = []
    if os.path.exists(os.path.join(root, "pubspec.yaml")):
        cross.append("flutter")
    pj = os.path.join(root, "package.json")
    if os.path.exists(pj) and '"react-native"' in open(pj, errors="ignore").read():
        cross.append("react-native")
    if any(os.path.exists(os.path.join(root, f)) for f in ("capacitor.config.json", "capacitor.config.ts")):
        cross.append("capacitor")
    if any(f.endswith(".csproj") for f in os.listdir(root)):
        cross.append("dotnet")
    out["cross_platform"] = cross

    # Mode recommendation
    if cross:
        mode = "out-of-scope"
    elif out["xcode"]["installed"] and out["has_ios_27_1_sdk"] and out["has_ios_27_1_runtime"]:
        mode = "full"
    else:
        mode = "limited"
    out["recommended_mode"] = mode

    json.dump(out, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
