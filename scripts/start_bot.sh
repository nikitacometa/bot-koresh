#!/bin/bash


LOGS_DIR=".logs"
mkdir -p $LOGS_DIR

FULL_LOG="${LOGS_DIR}/total.log"
echo "FULL_LOG=$FULL_LOG"

SCRIPTS="$(dirname $0)"

"$SCRIPTS"/init_tor.sh || exit
echo

python3 -m pipenv run python main.py | tee -a "$FULL_LOG"
