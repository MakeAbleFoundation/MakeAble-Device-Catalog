#!/bin/zsh
set -e
P="/Users/justinrui/Desktop/M/Makebot P1S Print Files"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
rm -f "$P/Validation/.finish3_done"
echo "### rebuilding plates whose reference keeps meshes inline"
$PY -u build.py "$P" bag-carrier-medium bag-carrier-small bag-carrier-large can-opener blister-pack-opener book-holder phone-magnifier-stand
echo "### rebuilding the catalogue"
$PY -u catalogue.py "$P"
echo "### slicing every full plate"
$PY -u report.py slice-devices "$P"
echo "### widening spacing where paths conflict"
$PY -u fixgaps.py "$P"
echo "### slicing catalogue plates"
$PY -u report.py slice-catalogue "$P"
echo "### structural self-check"
$PY -u selfcheck.py "$P"
echo "### reports"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### done"
touch "$P/Validation/.finish3_done"
