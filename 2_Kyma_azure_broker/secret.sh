#!/usr/bin/env bash

export AZURE_SUBSCRIPTION_ID=$(az account show --query id | sed s/\"//g)
export AZURE_TENANT_ID=<tenant_id>
export AZURE_CLIENT_ID=<client_id>
export AZURE_CLIENT_SECRET=<client_secret>

kubectl create secret generic azure-secret -n demo \
 --from-literal=subscription_id=$AZURE_SUBSCRIPTION_ID \
 --from-literal=tenant_id=$AZURE_TENANT_ID \
 --from-literal=client_secret=$AZURE_CLIENT_SECRET \
 --from-literal=client_id=$AZURE_CLIENT_ID