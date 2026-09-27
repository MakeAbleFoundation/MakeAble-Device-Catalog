#!/bin/zsh
set -e
P="/Users/justinrui/Desktop/M/Makebot P1S Print Files"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
rm -f "$P/Validation/.finish4_done" "$P/Full Plates/"*.3mf "$P/Validation/plate previews/"*.png
echo "### building every plate (exclusion zone widened to 26 x 36 mm)"
$PY -u build.py "$P"
echo "### building the catalogue"
$PY -u catalogue.py "$P"
echo "### slicing every full plate"
$PY -u report.py slice-devices "$P"
echo "### widening spacing where paths still conflict"
$PY -u fixgaps.py "$P"
echo "### slicing catalogue plates"
$PY -u report.py slice-catalogue "$P"
echo "### structural self-check"
$PY -u selfcheck.py "$P"
echo "### reports"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### done"
touch "$P/Validation/.finish4_done"
