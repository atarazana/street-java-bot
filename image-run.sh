#!/bin/sh

. ./image-env.sh

# --entrypoint bash \

podman run -it --rm -p 8080:8080 \
  -e SLACK_BOT_TOKEN=xoxb-977421453095-5526400499283-i1hU5XID62yIjvsRyt8cfuXc \
  -e SLACK_SIGNING_SECRET=4438c30e8074cd4b01d3c98df8af66b1 \
  -e SLACK_APP_TOKEN=xapp-1-A05FFN73T8T-5528979515332-7e4597b12bc74096af4bdb28ed3afd7d2586084d1932dd9b0aabf8aa74dc36a0 \
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

