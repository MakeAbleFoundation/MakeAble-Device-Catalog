#!/bin/zsh
# Everything after the plates are built: catalogue, structural checks, validation
# slices, then the reports.
set -e
P="/Users/justinrui/Desktop/M/Makebot P1S Print Files"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"

echo "=== catalogue ==="
$PY -u catalogue.py "$P"

echo "=== structural self-check ==="
$PY -u selfcheck.py "$P"

echo "=== slicing every full plate ==="
$PY -u report.py slice-devices "$P"

echo "=== slicing the designer references ==="
$PY -u report.py slice-refs "$P"

echo "=== slicing every catalogue plate ==="
$PY -u report.py slice-catalogue "$P"

echo "=== reports ==="
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "=== done ==="
