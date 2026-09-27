#!/bin/zsh
set -e
P="/Users/justinrui/Desktop/M/Makebot P1S Print Files"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
rm -f "$P/Validation/.finish5_done"
echo "### rebuilding the 4 plates that reach the excluded corner"
$PY -u build.py "$P" bag-carrier-large bottle-opener-wide-handle flipper-nail-clipper-large eating-utensil-aid
echo "### re-slicing those plates"
$PY -u report.py slice-devices "$P"
echo "### widening spacing where paths still conflict"
$PY -u fixgaps.py "$P"
echo "### structural self-check"
$PY -u selfcheck.py "$P"
echo "### reports"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### done"
touch "$P/Validation/.finish5_done"
