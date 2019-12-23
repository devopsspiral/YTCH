FROM rundeck/rundeck:3.1.2

RUN mkdir -p /tmp/tools \
    && curl -s -L https://storage.googleapis.com/kubernetes-release/release/v1.16.4/bin/linux/amd64/kubectl -o /tmp/tools/kubectl \
    && chmod +x /tmp/tools/kubectl
