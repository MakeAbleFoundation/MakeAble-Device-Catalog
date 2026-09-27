#!/bin/zsh
# Whole pipeline: build every plate, fit each one (clean slice, under the print-time cap),
# build and slice both catalogues, slice the designer references, check, write the reports.
# Long (hours): start it detached (nohup ./all.sh > ../logs/all_log.txt 2>&1 &!).
set -e
P="$(cd "$(dirname "$0")/../.." && pwd)"
PY=~/Library/Caches/makebot-build/venv/bin/python
cd "$P/Validation/tools"
rm -f "$P/Validation/.pipeline_done"
SLUGS=($($PY -c "import devices; print(' '.join(d['slug'] for d in devices.DEVICES))"))

echo "### building full plates"
$PY -u build.py "$P"
echo "### fitting plates (spacing for brims/supports, print-time cap)"
$PY -u fitplate.py "$P" $SLUGS
echo "### building and slicing the catalogues"
for n in 1 2; do
  $PY -u catalogue.py "$P" $n
  $PY -u report.py slice-catalogue "$P" $n
done
echo "### slicing designer references"
$PY -u report.py slice-refs "$P"
echo "### structural self-check"
$PY -u selfcheck.py "$P"
echo "### writing reports"
$PY -u report.py refresh "$P"
$PY -u report.py write "$P"
$PY -u readme.py "$P"
echo "### pipeline complete"
touch "$P/Validation/.pipeline_done"
