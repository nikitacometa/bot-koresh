#!/bin/bash

docker-compose down && docker-compose up -d

if [[ "$1" == "-v" ]]
then
  scripts/logs.sh
fi
