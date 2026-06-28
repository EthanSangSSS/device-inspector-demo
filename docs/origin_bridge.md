# Origin Bridge: Private Device Inspector to Public-Safe Demo

## Purpose

This repository is derived from the same product idea as the private Device Inspector project: helping users and engineers reason about device condition, diagnostic evidence, and trustworthy inspection reports.

The public demo is intentionally **not** a source-code copy of the private project. It is a sanitized, recruitment-oriented abstraction that keeps the engineering idea visible while removing private history, real-device workflows, external lookup dependencies, and any production-sensitive material.

## Product lineage

```text
Private Device Inspector idea
  -> user-facing device inspection, report generation, desktop/mobile pairing concepts
  -> public-safe hardware diagnostic workbench
  -> synthetic evidence, case lifecycle, AI-assisted triage, signed reports, mobile skeletons
```

## Concept mapping

| Private product concept | Public demo abstraction | Reason |
|---|---|---|
| Device inspection flow | Synthetic diagnostic case lifecycle | Keeps the workflow without exposing real inspection paths |
| Desktop/mobile pairing | Client skeletons plus Flask API contract | Shows architecture without production pairing credentials |
| Device data collection | Structured synthetic hardware evidence | Avoids real identifiers and private telemetry |
| Inspection report | RSA-signed diagnostic report | Preserves trust and tamper-evidence narrative |
| Verification QR / report verification | `/reports/verify` endpoint | Keeps verification concept in a public-safe form |
| Failure / anomaly explanation | AI-assisted engineering hypothesis | Moves from user-facing explanation to engineering FA triage |
| Private implementation history | Fresh public-safe repo history | Avoids leaking private development artifacts |

## Design rule

This demo should acknowledge the original idea without inheriting private implementation detail.

Allowed:

- product-level lineage;
- abstract architecture mapping;
- synthetic cases and generated examples;
- public-safe docs and tests;
- interview explanation of how the idea evolved.

Not allowed:

- copying private source history;
- real device identifiers or user records;
- proprietary logs;
- production credentials or endpoints;
- third-party lookup calls;
- private screenshots or customer data.

## Interview narrative

The original idea started as a practical device-inspection product: collect device signals, structure the inspection flow, and produce a trustworthy report. I then extracted the engineering core into this public-safe demo: a hardware diagnostic workbench with case lifecycle, structured evidence, audit trail, AI-assisted triage, and signed report verification. That lets me discuss the architecture and failure-analysis thinking publicly without exposing private implementation details or real device data.
