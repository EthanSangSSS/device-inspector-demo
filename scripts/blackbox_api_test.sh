#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:5001}"

echo "[health]"
curl -fsS "$BASE_URL/health" | python3 -m json.tool

echo "[auth]"
BEARER="$(curl -fsS -X POST "$BASE_URL/auth/token" \
  -H 'Content-Type: application/json' \
  -d '{"subject":"demo.engineer","role":"engineer"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')"

echo "[device]"
curl -fsS -X POST "$BASE_URL/devices" \
  -H "Authorization: Bearer $BEARER" \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"SYNTH-DEVICE-BLACKBOX","product_family":"mobile-device","privacy_class":"synthetic"}' \
  | python3 -m json.tool

echo "[log]"
curl -fsS -X POST "$BASE_URL/diagnostic-logs" \
  -H "Authorization: Bearer $BEARER" \
  -H 'Content-Type: application/json' \
  -d '{"log_id":"SYNTH-LOG-BLACKBOX","device_id":"SYNTH-DEVICE-BLACKBOX","source":"thermal_sensor_mock","severity":"warning","message":"Thermal instability after repeated stress loop.","evidence_strength":"medium"}' \
  | python3 -m json.tool

echo "[triage]"
curl -fsS -X POST "$BASE_URL/triage" \
  -H "Authorization: Bearer $BEARER" \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"SYNTH-DEVICE-BLACKBOX"}' \
  | python3 -m json.tool

echo "black-box API smoke test passed"
