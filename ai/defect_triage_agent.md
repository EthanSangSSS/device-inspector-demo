# Defect Triage Agent Contract

## Purpose

The defect triage agent converts diagnostic evidence into an engineering hypothesis. It must not present a hypothesis as a verified root cause.

## Input contract

```json
{
  "device": {
    "device_id": "SYNTH-DEVICE-001",
    "product_family": "mobile-device",
    "privacy_class": "synthetic"
  },
  "logs": [
    {
      "log_id": "SYNTH-LOG-001",
      "source": "thermal_sensor_mock",
      "severity": "warning",
      "message": "Thermal envelope exceeded expected range.",
      "evidence_strength": "medium"
    }
  ]
}
```

## Output contract

```json
{
  "failure_mode": "thermal-envelope-instability",
  "confidence": "medium",
  "evidence": [],
  "invalidators": [],
  "next_tests": [],
  "action": "Keep as engineering hypothesis until reproduced and reviewed."
}
```

## Required safety behavior

- Always separate facts from hypotheses.
- Always include invalidators.
- Always include next tests.
- Never recommend production corrective action from weak evidence alone.
- Never transmit diagnostic evidence to external model providers in this public demo.

## Future CV/VLM integration

A production extension could add:

- generated or approved defect-image dataset;
- image encoder for scratch/dent/liquid/thermal discoloration classification;
- VLM summarizer for engineer notes and defect images;
- model evaluation with false-positive and false-negative analysis;
- calibration by hardware-domain owner review.
