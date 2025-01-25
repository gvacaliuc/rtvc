#!/usr/bin/env bash

set -euo pipefail

_DEFAULT="+18654108388"
NUMBER="${1:-$_DEFAULT}"

curl \
  -u "$RTVC_USERNAME:$RTVC_PASSWORD" \
  -H "Content-type: application/json" \
  -d "{\"number\": \"$NUMBER\"}" \
  https://rtvc.fly.dev/api/v1/call
