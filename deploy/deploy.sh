#!/bin/sh

ENV_FILE=../.env.deploy

if ! test -f "${ENV_FILE}"; then
    echo "${ENV_FILE} does not exist."
    exit 1
fi

oc new-project street-java-bot

oc delete secret street-java-bot-env -n street-java-bot
oc create secret generic street-java-bot-env --from-env-file=${ENV_FILE} -n street-java-bot

oc apply -n street-java-bot -f deploy.yaml