#!/bin/bash

WORKDIR=$(dirname "$0")

cd "${WORKDIR}/.." || exit

if [ -z "${ENVIRONMENT}" ]; then
    echo "ENVIRONMENT variable not defined"
    exit 1
fi

if [ -z "${ANSIBLE_VAULT_KEY}" ]; then
    echo "ANSIBLE_VAULT_KEY variable not defined"
    exit 1
fi

ansible-vault decrypt \
--vault-password-file <(cat <<<"$ANSIBLE_VAULT_KEY") \
".secrets/${ENVIRONMENT}.env" \
--output ".env.${ENVIRONMENT}"