# Threat Model

## Scope

This threat model applies to the public-safe demo. It is intentionally narrower than a production device diagnostics platform.

## Assets

| Asset | Protection goal |
|---|---|
| Synthetic diagnostic evidence | Preserve integrity and clear data classification |
| Signed reports | Detect tampering |
| Case lifecycle | Maintain auditable state transitions |
| AI triage output | Prevent overclaiming and preserve human review boundary |
| Public repository | Avoid real identifiers, credentials, and proprietary material |

## Trust boundaries

```text
Client skeleton / API caller
  -> Flask API boundary
  -> SQLite repository boundary
  -> AI triage stub boundary
  -> RSA report signature boundary
```

The public demo does not trust user-submitted identifiers unless they carry the `SYNTH-` prefix and pass schema checks.

## Threats and controls

| Threat | Control |
|---|---|
| Real identifier accidentally enters public repo | `SYNTH-` prefix guard, public-safety scan, review checklist |
| Report payload is modified after generation | RSA-PSS signature verification |
| AI output is mistaken for verified root cause | triage output includes confidence, invalidators, next tests, and human-review action |
| Case status is changed without trace | audit events record case upsert, evidence upsert, status update, report signing |
| Generic logs hide weak evidence | hardware evidence schema separates measurement, reproduction rate, and evidence strength |
| Demo is mistaken for production | README and docs state public-safe synthetic-data boundary |

## Out of scope

- Production identity provider.
- Real key-management service.
- Network data-loss prevention.
- Device fleet enrollment.
- Real manufacturing systems.
- Real defect-image datasets.

## Production hardening backlog

- Managed identity and RBAC.
- Key rotation and external KMS.
- Encrypted persistence and retention policy.
- Audit export and reviewer approval workflow.
- Dependency scanning and SBOM.
- Model card, calibration, and domain-owner review for CV/VLM outputs.
