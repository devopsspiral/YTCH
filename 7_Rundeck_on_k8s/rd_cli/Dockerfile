FROM openjdk:8-jre-slim

ARG _RD_CLI_VERSION_="1.1.7"
ARG _RD_CLI_DEB_CHECKSUM_="4f1b83ee36e900a2b8a650867d6ccc7788931e7fd34d7c505439147b08ebe1c2eb1a7a903e8f52c05cc5a9380c5a9c14723f7f43ceecb8a647dce8685e883e58"

RUN apt-get update \
  && apt-get install -y curl \
  && curl -Lo /tmp/rundeck-cli.deb https://dl.bintray.com/rundeck/rundeck-deb/rundeck-cli_${_RD_CLI_VERSION_}-1_all.deb \
  && echo "${_RD_CLI_DEB_CHECKSUM_}  /tmp/rundeck-cli.deb" > /tmp/rundeck-cli.sig \
  && sha512sum -c /tmp/rundeck-cli.sig \
  && dpkg -i /tmp/rundeck*.deb \
  && rm /tmp/rundeck*.deb /tmp/rundeck-cli.sig\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV RD_AUTH_PROMPT false

COPY entry.sh /entry.sh
RUN chmod +x /entry.sh

ENTRYPOINT ["/entry.sh"]
