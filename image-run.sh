#!/bin/sh

. .env

. ./image-env.sh

# --entrypoint bash \

podman run -it --rm -p 8080:8080 \
  -e SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN} \
  -e SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET} \
  -e SLACK_APP_TOKEN=${SLACK_APP_TOKEN} \
  -e DATA_DIR=/deployments/data \
  -e DEV_USERNAME=user1 \
  -e DEV_PASSWORD=openshift \
  -e PROJECT_NAME=street-java-${DEV_USERNAME} \
  -e FRUIT_SERVICE_APP_NAME=fruit-service-${DEV_USERNAME} \
  -e FRUIT_GATEWAY_APP_NAME=fruit-gateway-${DEV_USERNAME} \
  -e SLACK_WEBHOOK=changeme \
  -e SLACK_CHANNEL=changeme \
  -e REPOSITORY="image-registry.openshift-image-registry.svc:5000/${PROJECT_NAME}/fruit-gateway" \
  -e TAG=1.0.0-SNAPSHOT \
  --name bot localhost/street-java-bot:${VERSION}

