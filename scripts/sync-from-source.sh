#!/usr/bin/env bash
# Syncs the java-evolved skill references from the upstream source repository.
# Usage: ./scripts/sync-from-source.sh
# Can be run manually or via GitHub Actions / cron.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REFERENCES_DIR="$SKILL_DIR/references"
SOURCE_REPO="https://github.com/javaevolved/javaevolved.github.io.git"
TEMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

echo "==> Cloning source repository..."
git clone --depth 1 --quiet "$SOURCE_REPO" "$TEMP_DIR/source"

CONTENT_DIR="$TEMP_DIR/source/content"

if [ ! -d "$CONTENT_DIR" ]; then
  echo "ERROR: Content directory not found at $CONTENT_DIR" >&2
  exit 1
fi

YAML_COUNT=$(find "$CONTENT_DIR" -name "*.yaml" | wc -l | tr -d ' ')
echo "==> Found $YAML_COUNT pattern YAML files"

if [ "$YAML_COUNT" -eq 0 ]; then
  echo "ERROR: No YAML files found. Source repo structure may have changed." >&2
  exit 1
fi

echo "==> Generating reference files..."
python3 "$SCRIPT_DIR/generate-references.py" \
  --content-dir "$CONTENT_DIR" \
  --output-dir "$REFERENCES_DIR"

echo "==> Sync complete. $YAML_COUNT patterns processed."
echo ""

# Show git diff summary if in a git repo
if git -C "$SKILL_DIR" rev-parse --git-dir > /dev/null 2>&1; then
  CHANGES=$(git -C "$SKILL_DIR" diff --stat -- references/ 2>/dev/null || true)
  if [ -n "$CHANGES" ]; then
    echo "Changed files:"
    echo "$CHANGES"
  else
    echo "No changes detected — references are up to date."
  fi
fi
