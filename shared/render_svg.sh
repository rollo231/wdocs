#!/bin/bash
# SVG를 2배 해상도 PNG로 만든다. 사용: bash render_svg.sh <파일.svg> <너비> <높이>
# 헤드리스 Chrome(또는 Chromium)을 쓴다. 경로는 CHROME 환경변수가 먼저다.
set -e
svg="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
png="${svg%.svg}.png"
chrome="${CHROME:-}"
if [ -z "$chrome" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Chromium.app/Contents/MacOS/Chromium" \
           google-chrome google-chrome-stable chromium chromium-browser; do
    if [ -x "$c" ] || command -v "$c" >/dev/null 2>&1; then chrome="$c"; break; fi
  done
fi
if [ -z "$chrome" ]; then
  echo "Chrome or Chromium not found. Set CHROME=/path/to/chrome." >&2
  exit 1
fi
"$chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 --window-size="$2,$3" --screenshot="$png" "file://$svg" >/dev/null 2>&1
echo "$png"
