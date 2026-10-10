#!/usr/bin/env bash
# Build, install, launch and screenshot the app on the iPhone Duo simulator.
#
# Usage:
#   capture.sh setup   <udid|name> <scheme> [-workspace X | -project Y]   # build + install, prints BUNDLE_ID
#   capture.sh launch  <udid> <bundle-id> [launch args...]
#   capture.sh pose    <udid>                                             # prints hinge angle / displays
#   capture.sh shoot   <udid> <out-dir> <pose> <screen>                   # screenshots every display
#   capture.sh rotate  <udid> <portrait|landscapeLeft|landscapeRight>     # tries, then verifies
#
# Folding cannot be automated with Apple's tools: ask the user to use Device Hub,
# then run `pose` to confirm before `shoot`.
set -uo pipefail

cmd="${1:-}"; shift || true
DD="DuoAdaptive/DerivedData"

resolve_udid() {
  local id="$1"
  if [[ "$id" =~ ^[0-9A-F-]{36}$ ]]; then echo "$id"; return; fi
  xcrun simctl list devices | grep -F "$id (" | grep -Eo '[0-9A-F-]{36}' | head -1
}

displays() {
  # Prints display ids reported by simctl; falls back to the reported defaults.
  local out ids
  out=$(xcrun simctl io "$1" enumerate 2>/dev/null)
  ids=$(echo "$out" | grep -Eo 'primary(-[0-9]+)?' | sort -u)
  [ -n "$ids" ] && echo "$ids" || printf 'primary\nprimary-1\n'
}

png_size() { sips -g pixelWidth -g pixelHeight "$1" 2>/dev/null | awk '/pixel/{print $2}' | paste -sd x -; }

is_blank() {
  # Blank if a 16x16 downscale is (almost) entirely black: the display is off.
  local tmp; tmp=$(mktemp).bmp
  sips -z 16 16 -s format bmp "$1" --out "$tmp" >/dev/null 2>&1 || return 1
  python3 - "$tmp" <<'PY'
import sys
d = open(sys.argv[1], "rb").read()
off = int.from_bytes(d[10:14], "little")
px = d[off:]
sys.exit(0 if px and max(px) < 12 else 1)
PY
  local rc=$?; rm -f "$tmp"; return $rc
}

case "$cmd" in
  setup)
    UDID=$(resolve_udid "$1"); SCHEME="$2"; shift 2
    [ -z "$UDID" ] && { echo "Simulator not found" >&2; exit 1; }
    xcrun simctl boot "$UDID" 2>/dev/null || true
    xcodebuild -scheme "$SCHEME" "$@" -destination "platform=iOS Simulator,id=$UDID" \
      -derivedDataPath "$DD" -quiet build || { echo "BUILD FAILED" >&2; exit 2; }
    APP=$(find "$DD/Build/Products" -maxdepth 2 -name "*.app" -path "*iphonesimulator*" | head -1)
    [ -z "$APP" ] && { echo "No .app found" >&2; exit 2; }
    xcrun simctl install "$UDID" "$APP"
    BUNDLE_ID=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$APP/Info.plist")
    echo "UDID=$UDID"; echo "APP=$APP"; echo "BUNDLE_ID=$BUNDLE_ID"
    ;;
  launch)
    UDID=$(resolve_udid "$1"); BID="$2"; shift 2
    xcrun simctl terminate "$UDID" "$BID" 2>/dev/null || true
    xcrun simctl launch "$UDID" "$BID" "$@"
    ;;
  pose)
    UDID=$(resolve_udid "$1")
    echo "== hinge angle (0 closed, ~127 book, 180 open)"
    xcrun devicectl device motion hinge-angle --device "$UDID" --timeout 5 2>&1 || echo "hinge-angle unavailable: infer pose from screenshots"
    echo "== displays"
    displays "$UDID"
    ;;
  shoot)
    UDID=$(resolve_udid "$1"); OUT="$2"; POSE="$3"; SCREEN="$4"
    mkdir -p "$OUT/$POSE"
    for d in $(displays "$UDID"); do
      name=$([ "$d" = "primary" ] && echo outer || echo inner)
      f="$OUT/$POSE/$name-$SCREEN.png"
      if xcrun simctl io "$UDID" screenshot --display="$d" "$f" >/dev/null 2>&1; then
        if is_blank "$f"; then echo "blank  $f ($(png_size "$f")) — display off in this pose"; rm -f "$f"
        else echo "saved  $f ($(png_size "$f"))"; fi
      else
        echo "failed $d"
      fi
    done
    ;;
  rotate)
    UDID=$(resolve_udid "$1"); ORI="$2"
    tmp=$(mktemp -d)
    xcrun simctl io "$UDID" screenshot "$tmp/before.png" >/dev/null 2>&1
    xcrun devicectl device orientation set "$ORI" --device "$UDID" >/dev/null 2>&1
    sleep 2
    xcrun simctl io "$UDID" screenshot "$tmp/after.png" >/dev/null 2>&1
    b=$(png_size "$tmp/before.png"); a=$(png_size "$tmp/after.png")
    if [ "$b" != "$a" ] || [ "$ORI" = "portrait" ]; then echo "ROTATED ($b -> $a)"
    else echo "NOT_ROTATED ($b): ask the user to rotate in Device Hub (Controls > Rotate Left)"; fi
    rm -rf "$tmp"
    ;;
  *)
    sed -n '2,13p' "$0"; exit 1 ;;
esac
