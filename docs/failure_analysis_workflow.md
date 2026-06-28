# Failure Analysis Workflow

## Purpose

This workflow shows how a hardware engineering tool can structure diagnostic evidence without turning weak signals into unsupported root-cause claims.

## Workflow

```text
1. Intake synthetic diagnostic evidence
2. Normalize logs into source / severity / message / evidence strength
3. Generate AI-assisted hypothesis
4. Attach invalidators and next tests
5. Generate signed diagnostic report
6. Verify report integrity before review
7. Hand off to owning hardware, EE, ME, acoustic, or operations team
```

## Evidence model

Each diagnostic log should include:

- `log_id`
- `device_id`
- `source`
- `severity`
- `message`
- `evidence_strength`

Evidence strength is not confidence. It describes how directly the log supports the hypothesis.

## Triage output contract

Each AI-assisted triage result must include:

- suspected failure mode;
- confidence label;
- supporting evidence;
- invalidators;
- next tests;
- action note.

## Decision rule

A triage result is an engineering hypothesis, not a final root cause. A corrective action should not be treated as accepted until:

- the failure is reproduced;
- alternative explanations are tested;
- hardware-domain owner reviews the evidence;
- corrective action is validated by follow-up telemetry or controlled experiment.

## Cross-functional handoff

The report should be written so that different domain owners can act on it:

| Team | Needs |
|---|---|
| EE | electrical trace, power/current, sensor telemetry |
| ME | enclosure, stress, tolerance, fixture condition |
| Acoustic | microphone/speaker path, waveform, sealing condition |
| Software | firmware build, logs, reproduction path |
| Operations | lot, station, process change, repeatability |

## Anti-patterns

- Treating one log line as root cause.
- Hiding weak evidence behind confident language.
- Mixing facts, hypotheses, and corrective actions.
- Using real identifiers in public demos.
- Sending diagnostics to unapproved third-party services.
