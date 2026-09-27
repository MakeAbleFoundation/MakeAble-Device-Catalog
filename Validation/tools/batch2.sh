#!/bin/zsh
# Second batch (devices 31-48) plus the plates it changed in the first (08 and 19 re-capped
# for print time, 13 now carrying the designer's variable layer height). Builds, fits each
# plate (clean slice, under the print-time cap), builds and slices Catalogue 2, slices the
# designers' references, then checks everything and writes the reports.
# Long: start it detached (nohup ./batch2.sh > ../logs/batch2_log.txt 2>&1 &!).
set -e
P="$(cd "$(dirname "$0")/../.." && pwd)"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
NEW=(bedside-box toothpaste-squeezer-gear chopstick-helper soup-can-opener jar-opener-vacuum
     younger-grip plug-puller pinky-saver cup-holder cane-holder hand-press-light
     hand-press-medium hand-press-hard coffee-gimbal pen-ball card-holder-4row boot-jack
     pencil-grip)
CHANGED=(keywings toothbrush-grip clothes-button-handles)

echo "### building plates"
$PY -u build.py "$P" $NEW $CHANGED
echo "### Catalogue 2"
$PY -u catalogue.py "$P" 2
$PY -u report.py slice-catalogue "$P" 2
echo "### designer references"
$PY -u report.py slice-refs "$P" $NEW
echo "### fitting plates: clean slice, under the print-time cap"
$PY -u fitplate.py "$P" $NEW $CHANGED
echo "### Catalogue 1, plate 13 (clothes-button handles gained their layer heights)"
$PY -u catalogue.py "$P" 1
$PY -u report.py slice-catalogue "$P" 1 13
echo "### checks and reports"
$PY -u selfcheck.py "$P"
$PY -u report.py refresh "$P"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### done"
