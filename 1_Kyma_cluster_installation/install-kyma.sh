#!/usr/bin/env bash
set -e
WORKDIR="kyma"
KYMA_VERSION=1.4.0

download_tiller_conf(){
if [ -f "${WORKDIR}/tiller.yaml" ]; then
    echo "tiller.yaml exists. Skipping..."
else
    wget https://raw.githubusercontent.com/kyma-project/kyma/$KYMA_VERSION/installation/resources/tiller.yaml -O ${WORKDIR}/tiller.yaml
fi
}

download_kyma_installer_conf(){
if [ -f "${WORKDIR}/kyma-installer-cluster.yaml" ]; then
    echo "kyma-installer-cluster.yaml exists. Skipping..."
else
    wget https://github.com/kyma-project/kyma/releases/download/$KYMA_VERSION/kyma-installer-cluster.yaml -O ${WORKDIR}/kyma-installer-cluster.yaml
fi
}

generate_wildcard_cert(){
if [ -f "${WORKDIR}/cert.pem" ]; then
    echo "Wildcard cert exists. Skipping..."
else
    #CA cert
    openssl req -newkey rsa:4096 -nodes -keyout ${WORKDIR}/ca.key -x509 -days 365 -out ${WORKDIR}/ca.crt -subj "/C=PL/ST=Gliwice/L=Gliwice/O=Kyma CA/CN=Kyma-CA-SS"

    openssl genrsa -out "${WORKDIR}/key.pem" 4096
    openssl req -key "${WORKDIR}/key.pem" -new -sha256 -out "${WORKDIR}/csr.pem" -subj "/C=PL/ST=Gliwice/L=Gliwice/O=Kyma cluster/CN=*.${DOMAIN}"
    openssl x509 -req -CA "${WORKDIR}/ca.crt" -CAkey "${WORKDIR}/ca.key" -CAcreateserial -in "${WORKDIR}/csr.pem" -out "${WORKDIR}/cert.pem" -days 365

fi
}

if [ -n "$1" ]; then
    [ -d $WORKDIR ] || mkdir $WORKDIR
    export DOMAIN=$1
    echo "--- Download configs if not present ---"
    download_tiller_conf
    download_kyma_installer_conf
    
    echo "--- Generate wildcard certificate  ---"
    generate_wildcard_cert
    export TLS_KEY=$(cat ${WORKDIR}/key.pem | base64 | sed 's/ /\\ /g' | tr -d '\n')
    export TLS_CERT=$(cat ${WORKDIR}/cert.pem | base64 | sed 's/ /\\ /g' | tr -d '\n')
    
    echo "--- Inject global variables  ---"
    kubectl create namespace kyma-installer && kubectl create configmap owndomain-overrides -n kyma-installer \
    --from-literal=global.ingress.domainName=$DOMAIN \
    --from-literal=global.domainName=$DOMAIN --from-literal=global.tlsCrt=$TLS_CERT \
    --from-literal=global.tlsKey=$TLS_KEY && kubectl label configmap owndomain-overrides -n kyma-installer installer=overrides
    
    echo "--- Install tiller  ---"
    kubectl apply -f "${WORKDIR}/tiller.yaml"
    kubectl wait --for=condition=complete --timeout=30s job/tiller-certs-job -n kube-system
    kubectl get -n kube-system secret tiller-secret -o jsonpath="{.data['ca\.crt']}" | base64 --decode > "${WORKDIR}/catiller.crt"
    kubectl get -n kube-system secret tiller-secret -o jsonpath="{.data['ca\.key']}" | base64 --decode > "${WORKDIR}/catiller.key"
    
    echo "--- Generate Helm client cert  ---"
    openssl genrsa -out "${WORKDIR}/helm.key.pem" 4096
    openssl req -key "${WORKDIR}/helm.key.pem" -new -sha256 -out "${WORKDIR}/helm.csr.pem" -subj "/C=PL/ST=Gliwice/L=Gliwice/O=Helm Client/CN=helm-client"
    openssl x509 -req -CA "${WORKDIR}/catiller.crt" -CAkey "${WORKDIR}/catiller.key" -CAcreateserial -in "${WORKDIR}/helm.csr.pem" -out "${WORKDIR}/helm.cert.pem" -days 365

    echo "--- Generate Helm client cert  ---"
    . helm-tls.sh ${WORKDIR}
    
    echo "--- Create Kyma installer instance  ---"
    vim ${WORKDIR}/kyma-installer-cluster.yaml
    kubectl apply -f ${WORKDIR}/kyma-installer-cluster.yaml
    while true; do   kubectl -n default get installation/kyma-installation -o jsonpath="{'Status: '}{.status.state}{', description: '}{.status.description}"; echo;   sleep 5; done
else
    echo "You need to pass domain base for your kyma installation"
    exit 1
fi
