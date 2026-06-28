# Architecture

## System goal

Device Inspector Demo models a public-safe internal engineering tool for hardware diagnostics and failure analysis. It converts synthetic engineering evidence into a signed report with an explicit AI-assisted hypothesis layer, lifecycle state, and audit trail.

## Data flow

```text
Synthetic iOS / Android client skeleton
  -> POST /devices
  -> POST /cases
  -> POST /cases/{case_id}/evidence
  -> POST /cases/{case_id}/triage
  -> POST /reports
  -> POST /reports/verify
```

## Components

### Flask API

The Flask API is intentionally small and inspectable. It handles authentication, diagnostic evidence intake, case lifecycle, audit events, triage, report generation, and signature verification.

### SQLite repository

The repository layer stores five public-safe entities:

- `devices`
- `cases`
- `diagnostic_logs`
- `reports`
- `audit_events`

The demo accepts only identifiers prefixed with `SYNTH-`. This is a deliberate public-safety boundary.

### Hardware evidence schema

The evidence schema models build phase, component, fixture, station, test name, measurement, reproduction rate, and evidence strength. This keeps weak signals separate from confidence and avoids turning a symptom into a root cause.

### AI triage agent stub

The triage layer is deterministic. It demonstrates the expected output contract of a future CV/VLM or multi-agent system without calling external model providers.

Each triage result includes:

- likely failure mode;
- confidence;
- owner-domain hint;
- evidence list;
- invalidators;
- recommended next tests;
- facts versus hypotheses boundary;
- action note for the owning engineering team.

### Mobile skeletons

The `clients/` folder contains public-safe skeletons for:

- iOS SwiftUI / Combine / CoreData architecture;
- Android Kotlin / MVVM architecture.

They are source skeletons, not production mobile apps.

### Synthetic evaluation lab

The `ml/` folder contains a deterministic visual triage evaluation path using synthetic metadata only. It exists to demonstrate evaluation discipline, not model performance.

### RSA report signing

Reports are serialized as canonical JSON and signed with RSA-PSS/SHA-256. Verification fails if report payload is changed after signing.

## Future production architecture

A production system would require:

- real identity and access management;
- approved device-data ingestion contracts;
- encrypted storage and retention policy;
- cloud object storage with audit trail;
- CV/VLM registry and evaluation harness;
- monitoring, model-risk review, and incident-response process;
- hardware-team review before corrective action is treated as accepted root cause.
