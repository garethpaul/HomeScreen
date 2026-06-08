#!/usr/bin/env bash
set -euo pipefail

fabric_api="abb870ac2c6cd77fc0a3ee166f786a86748f4e""b9"
fabric_secret="47d331d25396fd56e08c5c5891c16a003ba5647e584bf8fc07feb0e8ae""92ab92"

rg --hidden --glob '!.git/**' --fixed-strings \
  -e "$fabric_api" \
  -e "$fabric_secret" \
  . && {
    echo "Committed Fabric secret value found" >&2
    exit 1
  }

echo "No committed Fabric secret values found."
