FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl git \
    && curl -fsSL https://download.docker.com/linux/static/stable/aarch64/docker-27.5.1.tgz \
        | tar xz --strip-components=1 -C /usr/local/bin docker/docker \
    && rm -rf /var/lib/apt/lists/* \
    && jenkins-plugin-cli --plugins "workflow-aggregator git pipeline-stage-view"

USER jenkins
