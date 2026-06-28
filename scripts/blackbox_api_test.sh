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

echo "[case]"
curl -fsS -X POST "$BASE_URL/cases" \
  -H "Authorization: Bearer $BEARER" \
  -H 'Content-Type: application/json' \
  -d '{"case_id":"SYNTH-CASE-BLACKBOX","device_id":"SYNTH-DEVICE-BLACKBOX","build_phase":"DVT","component":"thermal_system","symptom":"Synthetic thermal drift"}' \
  | python3 -m json.tool

echo "[evidence]"
curl -fsS -X POST "$BASE_URL/cases/SYNTH-CASE-BLACKBOX/evidence" \
  -H "Authorization: Bearer $BEARER" \
  -H 'Content-Type: application/json' \
  -d '{"log_id":"SYNTH-LOG-BLACKBOX","device_id":"SYNTH-DEVICE-BLACKBOX","source":"thermal_sensor_mock","severity":"warning","component":"thermal_system","test_name":"camera_stress_loop","message":"Thermal instability after repeated stress loop.","measurement":{"metric":"surface_temp_delta_c","value":8.4,"unit":"C","limit":5.0},"evidence_strength":"medium"}' \
  | python3 -m json.tool

echo "[case triage]"
curl -fsS -X POST "$BASE_URL/cases/SYNTH-CASE-BLACKBOX/triage" \
  -H "Authorization: Bearer $BEARER" \
  -H 'Content-Type: application/json' \
  -d '{}' \
  | python3 -m json.tool

echo "black-box API smoke test passed"
