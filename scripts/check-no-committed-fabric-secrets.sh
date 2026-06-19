#!/usr/bin/env bash
set -euo pipefail

literal_fabric_credentials="Fabric\\.framework/run[[:space:]]+[\"']?[[:xdigit:]]{40}[\"']?[[:space:]]+[\"']?[[:xdigit:]]{64}[\"']?([^[:xdigit:]]|$)"

if rg --quiet --hidden --glob '!.git/**' --glob '!scripts/check-no-committed-fabric-secrets.sh' \
  --regexp "$literal_fabric_credentials" .; then
  echo "Committed Fabric credential-shaped values found" >&2
  exit 1
else
  scan_status=$?
fi

if [ "$scan_status" -ne 1 ]; then
  echo "Unable to complete Fabric credential scan" >&2
  exit "$scan_status"
fi

echo "No committed Fabric credential-shaped values found."
