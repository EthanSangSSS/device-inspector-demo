# Demo Scope

## What is included

- Flask backend for diagnostic workflow demonstration.
- SQLite persistence for synthetic devices, cases, evidence logs, reports, and audit events.
- Protected write endpoints.
- Case lifecycle state transitions.
- Structured hardware evidence schema.
- RSA report signing and verification.
- Deterministic AI-assisted triage stub.
- Synthetic visual triage evaluation path.
- iOS SwiftUI / Combine / CoreData source skeleton.
- Android Kotlin / MVVM source skeleton.
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
- App Store or Play Store purchase verification.
- Private mobile platform probes or review-sensitive system-property reads.
- Real serial-number prefix databases or production model-identification data.

## Why this matters for interviews

The goal is not to claim production-scale hardware failure analysis. The goal is to make the engineering thinking inspectable:

- privacy boundary;
- evidence contract;
- API design;
- report integrity;
- testability;
- AI workflow boundaries;
- mobile architecture awareness;
- cross-functional handoff format.

## Extension roadmap

1. Wrap the iOS skeleton in a compilable Xcode project.
2. Wrap the Android skeleton in a Gradle project.
3. Add generated synthetic visual patterns and a confusion-matrix artifact.
4. Add calibration metrics for confidence labels.
5. Add role-based access control and audit review UI.
6. Add object-storage abstraction with local filesystem adapter.
7. Add a public model-identifier field to evidence examples with confidence and provenance.
8. Add a demo entitlement boundary that fails closed without real store integration.
