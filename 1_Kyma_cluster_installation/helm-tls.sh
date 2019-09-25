#!/usr/bin/env bash

export HELM_TLS_CERT=${1}/helm.cert.pem
export HELM_TLS_KEY=${1}/helm.key.pem
export HELM_TLS_VERIFY=false
export HELM_TLS_ENABLE=true
