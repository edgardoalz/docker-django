#!/bin/sh

set -o errexit
set -o nounset

curl -s -f "http://localhost:${PORT}/up" || exit 1
