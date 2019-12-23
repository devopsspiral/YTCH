#!/usr/bin/env bash
set -e
timeout 300 bash -c 'while [[ "$(curl -s -o /dev/null -w "%{http_code}" $RD_URL/api/ -H "X-Rundeck-Auth-Token: $RD_TOKEN" -k )" != "200" ]]; do sleep 5; done' || false
source $1

