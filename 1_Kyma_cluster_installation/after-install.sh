#!/usr/bin/env bash
set -e
EXTERNAL_PUBLIC_IP=$(kubectl get service -n istio-system istio-ingressgateway -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
APISERVER_PUBLIC_IP=$(kubectl get service -n kyma-system apiserver-proxy-ssl -o jsonpath="{.status.loadBalancer.ingress[0].ip}")
CONSOLE_FQDN=$(kubectl get virtualservice core-console -n kyma-system -o jsonpath='{ .spec.hosts[0] }')
ADMIN_PASSWORD=$(kubectl get secret admin-user -n kyma-system -o jsonpath="{.data.password}" | base64 --decode)
echo "External Kyma IP: $EXTERNAL_PUBLIC_IP"
echo "External APIServer IP: $APISERVER_PUBLIC_IP"
echo "Kyma Console FQDN: $CONSOLE_FQDN"
echo "Admin user: admin@kyma.cx"
echo "Admin password: $ADMIN_PASSWORD"
