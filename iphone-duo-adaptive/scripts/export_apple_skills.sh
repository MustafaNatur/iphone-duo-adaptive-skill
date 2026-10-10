#!/usr/bin/env bash
# Export Apple's Xcode agent skills for this session (never copy them into the user's repo).
# Usage: export_apple_skills.sh [output-dir]
# Exit: 0 exported · 2 Xcode/xcrun missing · 3 export unsupported or failed
set -uo pipefail

OUT="${1:-${TMPDIR:-/tmp}/apple-agent-skills}"

if ! command -v xcrun >/dev/null 2>&1 || ! xcodebuild -version >/dev/null 2>&1; then
  echo "Xcode not found; continue with this skill's own references." >&2
  exit 2
fi

mkdir -p "$OUT"
if ! xcrun agent skills export --output-dir "$OUT" >/dev/null 2>"$OUT/.export.err"; then
  echo "This Xcode can't export agent skills ($(xcodebuild -version | head -1))." >&2
  sed -n 1,5p "$OUT/.export.err" >&2
  exit 3
fi

echo "$OUT"
echo "Exported skills ($(xcodebuild -version | head -1)):"
for f in "$OUT"/*/SKILL.md; do
  [ -f "$f" ] || continue
  name=$(basename "$(dirname "$f")")
  desc=$(awk '/^description:/{sub(/^description: *"?/,""); if ($0=="|"||$0==">") {getline; sub(/^ +/,"")} sub(/"$/,""); print substr($0,1,140); exit}' "$f")
  rel=""
  grep -qiE 'resiz|iphone duo|uiscreen|orientation|safe area|toolbar|size class' "$f" && rel="  <- relevant"
  printf -- "- %s: %s%s\n" "$name" "$desc" "$rel"
done
