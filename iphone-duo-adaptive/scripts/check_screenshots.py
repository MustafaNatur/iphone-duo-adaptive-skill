#!/usr/bin/env python3
"""Validate iPhone Duo App Store screenshots (size, format, alpha). Uses macOS `sips`.

Usage: python3 check_screenshots.py <dir> [--fix-alpha]

Spec (App Store Connect, checked 2026-10-10; re-check Apple's page before submitting):
  outer: 1398x2034 portrait, 2034x1398 landscape
  inner: 2007x2853 portrait, 2853x2007 landscape
  1-10 per size; .png/.jpg/.jpeg; no alpha.
"""
import argparse
import os
import subprocess
import sys
from collections import Counter

SPEC = {
    (1398, 2034): "outer portrait", (2034, 1398): "outer landscape",
    (2007, 2853): "inner portrait", (2853, 2007): "inner landscape",
}
EXT = (".png", ".jpg", ".jpeg")


def props(path):
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", "-g", "hasAlpha", path],
                         capture_output=True, text=True).stdout
    vals = {}
    for line in out.splitlines()[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            vals[k.strip()] = v.strip()
    return int(vals.get("pixelWidth", 0)), int(vals.get("pixelHeight", 0)), vals.get("hasAlpha") == "yes"


def flatten(path):
    # Re-encode as JPEG (no alpha) next to the original, then back to PNG.
    tmp = path + ".noalpha.jpg"
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "best", path, "--out", tmp], capture_output=True)
    subprocess.run(["sips", "-s", "format", "png", tmp, "--out", path], capture_output=True)
    os.remove(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--fix-alpha", action="store_true")
    a = ap.parse_args()
    files = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(a.dir) for f in fs if f.lower().endswith(EXT))
    if not files:
        print("No screenshots found.")
        return 1
    problems, per_size = 0, Counter()
    for f in files:
        w, h, alpha = props(f)
        kind = SPEC.get((w, h))
        issues = []
        if not kind:
            issues.append(f"size {w}x{h} is not an iPhone Duo size")
            ratio_match = [k for (sw, sh), k in SPEC.items() if abs(w / max(h, 1) - sw / sh) < 0.002]
            if ratio_match:
                issues.append(f"same aspect as {ratio_match[0]}: may be scaled proportionally")
        else:
            per_size[kind] += 1
        if alpha:
            if a.fix_alpha:
                flatten(f)
                _, _, alpha = props(f)
            if alpha:
                issues.append("has alpha channel (use --fix-alpha)")
        status = "OK  " if not issues else "FAIL"
        problems += bool(issues)
        print(f"{status} {os.path.relpath(f, a.dir)}  {w}x{h}  {kind or ''}  {'; '.join(issues)}")
    print()
    for kind in SPEC.values():
        n = per_size.get(kind, 0)
        note = "" if n <= 10 else "  (max 10)"
        print(f"{kind:16s} {n}{note}")
        problems += n > 10
    print("\nAll screenshots valid." if not problems else f"\n{problems} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
