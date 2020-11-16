FROM bitnami/fluentd
USER root
## Install custom Fluentd plugins
RUN fluent-gem install 'fluent-plugin-azure-loganalytics'

USER 1001
