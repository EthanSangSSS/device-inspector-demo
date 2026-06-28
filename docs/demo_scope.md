# Demo Scope

## What is included

- Flask backend for diagnostic workflow demonstration.
- SQLite persistence for synthetic devices, logs, and reports.
- JWT-protected write endpoints.
- RSA report signing and verification.
- Deterministic AI-assisted triage stub.
- Pytest coverage and GitHub Actions CI.
- Public-safety guardrails against realistic identifiers.

## What is excluded

- Real device data ingestion.
- Third-party IMEI or activation-lock lookup.
- Proprietary manufacturing, factory, or hardware logs.
- Production identity provider integration.
- Cloud object storage credentials or OSS buckets.
- Real CV/VLM model weights or private image datasets.
- Mobile app binaries or store submission assets.

## Why this matters for interviews

The goal is not to claim production-scale hardware failure analysis. The goal is to make the engineering thinking inspectable:

- privacy boundary;
- evidence contract;
- API design;
- report integrity;
- testability;
- AI workflow boundaries;
- cross-functional handoff format.

## Extension roadmap

1. Add a small Flutter or SwiftUI client that submits synthetic logs.
2. Add image upload using generated synthetic defect images.
3. Replace deterministic triage with a local model interface.
4. Add calibration metrics for confidence labels.
5. Add audit events and role-based access control.
6. Add object-storage abstraction with local filesystem adapter.
