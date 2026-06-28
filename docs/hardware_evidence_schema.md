# Hardware Evidence Schema

## Purpose

The baseline demo previously used generic diagnostic logs. This schema moves the project closer to a hardware engineering workbench by modeling build phase, component, fixture, station, test, measurement, reproduction rate, and evidence strength.

## Case lifecycle

```text
new -> evidence_collected -> triaged -> needs_reproduction -> assigned_to_domain_owner -> corrective_action_proposed -> verification_pending -> closed
```

A case should not move to `closed` only because AI triage produced a hypothesis. Closure requires reproduction, domain-owner review, and verification evidence.

## Case fields

| Field | Meaning |
|---|---|
| `case_id` | Synthetic case identifier prefixed with `SYNTH-` |
| `device_id` | Synthetic device identifier prefixed with `SYNTH-` |
| `build_phase` | `EVT`, `DVT`, `PVT`, `MP`, or `UNKNOWN` |
| `component` | Hardware subsystem such as connector, microphone, display, battery, thermal system |
| `symptom` | Observable issue, not root cause |
| `facts` | Evidence already observed |
| `hypotheses` | Candidate explanations that remain unverified |

## Evidence fields

| Field | Meaning |
|---|---|
| `log_id` | Synthetic evidence identifier |
| `case_id` | Case being investigated |
| `source` | Mock sensor, fixture, station, or engineer note source |
| `severity` | `info`, `warning`, or `critical` |
| `component` | Suspected subsystem |
| `test_name` | Controlled test or fixture loop name |
| `fixture_id` | Synthetic fixture identifier |
| `station` | Synthetic station identifier |
| `message` | Human-readable observation |
| `measurement` | Metric, value, unit, and optional limit |
| `reproduction_rate` | Example: `3/10`; never presented as final yield |
| `evidence_strength` | `low`, `medium`, or `high`; separate from AI confidence |

## Example

```json
{
  "log_id": "SYNTH-LOG-EVIDENCE-001",
  "case_id": "SYNTH-CASE-EVIDENCE-001",
  "device_id": "SYNTH-DEVICE-EVIDENCE-001",
  "source": "fixture_continuity_mock",
  "severity": "warning",
  "component": "connector",
  "test_name": "vibration_continuity_loop",
  "fixture_id": "SYNTH-FIXTURE-CONN-001",
  "station": "SYNTH-STATION-EVT-01",
  "message": "Connector continuity loss observed during synthetic vibration loop.",
  "measurement": {
    "metric": "continuity_drop_count",
    "value": 3,
    "unit": "count",
    "limit": 0
  },
  "reproduction_rate": "3/10",
  "evidence_strength": "medium"
}
```

## Interpretation rules

- Evidence strength is not model confidence.
- A symptom is not a root cause.
- A single log line cannot close a case.
- AI output is an engineering hypothesis until reproduced and reviewed.
- Synthetic data must remain visibly synthetic in public artifacts.
