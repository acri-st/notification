# This argument is used to build in the CI
ARG BASE_VERSION=v5.2.0
ARG REGISTRY=harbor.shared.acrist-services.com/dsy/desp-aas/
ARG CI_COMMIT_SHORT_SHA=xxxxxx
ARG CI_COMMIT_TAG=0.0.0
#FROM should stay with the simple name of the image for tilt build
FROM ${REGISTRY}desp-base-image:${BASE_VERSION}
ENV GIT_HASH=$CI_COMMIT_SHORT_SHA
ENV VERSION=$CI_COMMIT_TAG
# This line indicates what folder contains the main.py file
ENV ENTRYPOINT=notification
# This copy change the owner, this is needed for Tilt to override during development
COPY --chown=$LOCAL_USER:$LOCAL_GROUP ./${ENTRYPOINT} /app/${ENTRYPOINT}
COPY requirements.txt ./${ENTRYPOINT}
#Install dependencies in addition to the parents ones
RUN pip install --no-cache-dir -r ./${ENTRYPOINT}/requirements.txt
# DO NOT OVERRIDE THE ENTRYPOINT BUT USE THE ENTRYPOINT ENV VAR
