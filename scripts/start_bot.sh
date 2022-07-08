#!/bin/bash


LOGS_DIR=".logs"
mkdir -p $LOGS_DIR

FULL_LOG="${LOGS_DIR}/total.log"
echo "FULL_LOG=$FULL_LOG"

SCRIPTS="$(dirname $0)"

"$SCRIPTS"/scripts/init_tor.sh || exit
echo

#"$SCRIPTS"/scripts/start_mongodb.sh || exit
#echo

python3 -m pipenv run python main.py | tee -a "$FULL_LOG"
