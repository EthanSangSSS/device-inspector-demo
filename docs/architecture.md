# Architecture

## System goal

Device Inspector Demo models a public-safe internal engineering tool for hardware diagnostics and failure analysis. It converts synthetic device evidence into a signed report with an explicit AI-assisted hypothesis layer.

## Data flow

```text
Synthetic client / tester
  -> POST /devices
  -> POST /diagnostic-logs
  -> POST /triage
  -> POST /reports
  -> POST /reports/verify
```

## Components

### Flask API

The Flask API is intentionally small and inspectable. It handles authentication, diagnostic evidence intake, triage, report generation, and signature verification.

### SQLite repository

The repository layer stores three public-safe entities:

- `devices`
- `diagnostic_logs`
- `reports`

The demo accepts only identifiers prefixed with `SYNTH-`. This is a deliberate public-safety boundary.

### AI triage agent stub

The triage layer is deterministic. It demonstrates the expected output contract of a future CV/VLM or multi-agent system without calling external model providers.

Each triage result includes:

- likely failure mode;
- confidence;
- evidence list;
- invalidators;
- recommended next tests;
- action note for the owning engineering team.

### RSA report signing

Reports are serialized as canonical JSON and signed with RSA-PSS/SHA-256. Verification fails if report payload is changed after signing.

## Future production architecture

A production system would require:

- real identity and access management;
- approved device-data ingestion contracts;
- encrypted storage and retention policy;
- cloud object storage with audit trail;
- CV/VLM model registry and evaluation harness;
- monitoring, model-risk review, and incident-response process;
- hardware-team review before corrective action is treated as accepted root cause.
