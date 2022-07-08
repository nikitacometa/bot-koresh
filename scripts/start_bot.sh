#!/bin/bash


#if [ "$(whoami)" != "root" ]; then
#  # otherwise tor won't restart
#  echo "Script must be run as root" && exit 1
#fi

. .env

if [[ -z "${KORESH_HOME}" ]]; then
  echo "\$KORESH_HOME is not set!" && exit 1
fi

#if [[ -z "${PYTHON_HOME}" ]]; then
#  echo "\$PYTHON_HOME is not set!" && exit 1
#fi

echo
echo "KORESH_HOME=$KORESH_HOME"

FULL_LOG=".logs/total.log"
echo "FULL_LOG=$FULL_LOG"

"$KORESH_HOME"/scripts/init_tor.sh || exit
echo

#"$KORESH_HOME"/scripts/start_mongodb.sh || exit
echo

while true
do
   python3 -m pipenv run python3 "main.py" | tee -a "$FULL_LOG"
   sleep 1
done
