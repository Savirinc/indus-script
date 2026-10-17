#!/usr/bin/env bash
# Reproduces two known numbers (~10 s). Expect:  indus -1 -46.888   and   lb -1 -19.093
set -euo pipefail
cd "$(dirname "$0")/.."; source setup/paths.sh
cd indus-lab/round43
rm -f split_indus_-1.json split_lb_-1.json
python3 run43.py indus -1 0 $DATA_ARGS
python3 run43.py lb -1 0 $DATA_ARGS
rm -f split_indus_-1.json split_lb_-1.json
