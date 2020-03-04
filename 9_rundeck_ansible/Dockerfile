FROM rundeck/rundeck:3.1.2

RUN mkdir -p /tmp/tools \
    && curl -s -L https://storage.googleapis.com/kubernetes-release/release/v1.16.4/bin/linux/amd64/kubectl -o /tmp/tools/kubectl \
    && chmod +x /tmp/tools/kubectl

RUN sudo apt-get -y update \
  && sudo apt-get -y --no-install-recommends install ca-certificates python3-pip sshpass \
  && sudo -H pip3 --no-cache-dir install --upgrade pip setuptools \
  && sudo -H pip3 --no-cache-dir install ansible==2.9.5 \
  && sudo rm -rf /var/lib/apt/lists/* \
  && sudo mkdir /etc/ansible