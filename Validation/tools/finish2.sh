#!/bin/zsh
set -e
P="/Users/justinrui/Desktop/M/Makebot P1S Print Files"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
rm -f "$P/Validation/.finish2_done"
echo "### widening spacing on plates whose paths conflict"
$PY -u fixgaps.py "$P"
echo "### slicing catalogue plates one at a time"
$PY -u report.py slice-catalogue "$P"
echo "### structural self-check"
$PY -u selfcheck.py "$P"
echo "### reports"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### done"
touch "$P/Validation/.finish2_done"
