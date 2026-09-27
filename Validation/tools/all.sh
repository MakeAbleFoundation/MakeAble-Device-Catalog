#!/bin/zsh
# Whole pipeline: build the plates, build the catalogue, check them, slice everything
# for validation, then write the reports.
set -e
P="/Users/justinrui/Desktop/M/Makebot P1S Print Files"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
rm -f "$P/Validation/.pipeline_done"

echo "### building full plates"
$PY -u build.py "$P"
echo "### building the catalogue"
$PY -u catalogue.py "$P"
echo "### structural self-check"
$PY -u selfcheck.py "$P"
echo "### slicing full plates"
$PY -u report.py slice-devices "$P"
echo "### slicing designer references"
$PY -u report.py slice-refs "$P"
echo "### slicing catalogue plates"
$PY -u report.py slice-catalogue "$P"
echo "### writing reports"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### pipeline complete"
touch "$P/Validation/.pipeline_done"
