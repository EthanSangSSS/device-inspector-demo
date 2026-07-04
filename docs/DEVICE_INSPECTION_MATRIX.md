# Device Inspection Matrix

This document turns Device Inspector from a feature list into a verifiable inspection system. Each inspection capability must state its data source, automation level, confidence, limitation, and follow-up validation path before it can be represented as production-ready.

## Scope

The public demo remains synthetic and public-safe. The matrix below defines the product-grade diagnostic model that future private or platform-specific clients can implement without leaking real device identifiers, production logs, user data, or proprietary hardware process material.

## Inspection confidence model

| Confidence | Meaning | Required evidence |
|---|---|---|
| `high` | The signal is directly observable and repeatable through an approved API, fixture, or deterministic calculation. | Raw reading, timestamp, client version, platform, repeat count, and pass/fail rule. |
| `medium` | The signal is useful but may be affected by platform permission, environment, user handling, lighting, temperature, or accessory state. | Raw reading plus limitation text and recommended retest condition. |
| `low` | The signal is only a heuristic, visual aid, or user-confirmed observation. | Explicit user confirmation, screenshot/photo placeholder, or manual checklist response. |
| `not_supported` | The platform does not expose enough information for reliable automation. | Platform limitation and suggested manual or service-center verification path. |

## Automation level

| Level | Definition |
|---|---|
| `automatic` | App can collect and classify the signal without user interpretation. |
| `guided` | App can display a test pattern or prompt, but user confirmation is required. |
| `manual` | App records a checklist result or external measurement only. |
| `external_fixture` | Requires lab hardware, service tooling, or an approved fixture. |

## Capability matrix

| Domain | Diagnostic capability | Evidence source | Automation | Confidence | Key risks / limitations | Report output |
|---|---|---|---|---|---|---|
| Device identity | Public model identifier, OS version, app build, inspection session ID | Platform public APIs and generated case metadata | automatic | high | Must not collect real serial, IMEI, owner account, carrier account, or internal asset IDs in the public demo. | Device profile with provenance. |
| Case provenance | Case lifecycle, actor, timestamp, audit event hash | Backend case repository and signed audit trail | automatic | high | Clock skew and local-only storage must be called out if no trusted server timestamp is available. | Audit timeline. |
| Display basics | Brightness state, orientation, resolution class, color-space capability flag where available | Platform display APIs and user-visible test state | automatic / guided | medium | Mobile platforms expose different display capabilities; HDR capability may not imply correct HDR rendering. | Display capability summary. |
| Display uniformity | White, mid-gray, low-gray, and dark-mode gray visual uniformity checks | Guided test patterns plus user confirmation or lab photo fixture | guided / external_fixture | low to medium | Ambient light, screen protector, camera exposure, brightness, PWM, and viewing angle can create false positives. | `pass`, `suspect`, or `retest_required` with conditions. |
| Dead / stuck pixels | Full-screen RGBW and black patterns | Guided test patterns plus user confirmation | guided | low | Small defects may be missed without magnification; OLED subpixel layout can confuse manual review. | Pixel anomaly checklist. |
| Low-gray clipping | Near-black gradient and step patches | Guided test pattern | guided | low | Human-visible only unless paired with a calibrated camera or probe. | Low-gray clipping risk note. |
| HDR / wide gamut | HDR test pattern availability, P3/sRGB comparison flow, declared HDR capability | Platform capability flags plus synthetic test patterns | guided | medium | Declared HDR/P3 support is not equivalent to measured EOTF/gamut accuracy. | HDR capability status plus limitation. |
| Refresh-rate behavior | Static and motion scenarios for refresh switch visibility | Platform refresh APIs where available plus guided visual test | guided | low to medium | OS compositor, power mode, brightness, low-power mode, and app foreground state affect behavior. | Refresh-rate flicker observation. |
| Touch | Multi-touch count, edge touch, dead zone, gesture tracking | Client-side touch event capture | automatic / guided | medium | Screen protector, case, palm rejection, and accessibility settings can affect results. | Touch heatmap or checklist. |
| Camera | Camera availability, permission state, preview open, synthetic focus/exposure prompt | Platform camera APIs and guided capture | automatic / guided | medium | Real optical defects require controlled lighting and focus targets; public demo must not store real photos by default. | Camera readiness and manual defect notes. |
| Microphone / speaker | Permission state, loopback prompt, level meter, speaker playback prompt | Platform audio APIs and user confirmation | guided | low to medium | Background noise and device volume affect results; automatic diagnosis is limited without fixture. | Audio readiness and retest notes. |
| Sensors | Accelerometer, gyroscope, magnetometer availability and live readings | Platform sensor APIs | automatic | medium | Calibration state, table vibration, magnetic interference, and OS sensor fusion vary by device. | Sensor availability and stability indicators. |
| Haptics | Haptic engine trigger and user confirmation | Platform haptics APIs and guided checklist | guided | low | User perception varies; app may not access deeper hardware diagnostics. | Haptic confirmation. |
| Battery / thermal | Public battery state, charging state, coarse thermal state where available | Platform public APIs | automatic | medium | iOS/Android expose limited battery-health detail to third-party apps; service diagnostics may be required. | Battery/thermal summary with limitation. |
| Connectivity | Wi-Fi/Bluetooth permission state and basic capability flags | Platform public APIs | automatic / guided | medium | OS privacy restrictions limit SSID/BSSID and radio diagnostics; no network scanning in public demo. | Connectivity readiness. |
| Enclosure / liquid damage | Visual checklist and photo placeholder only | User checklist or service fixture | manual / external_fixture | low | Cannot reliably detect water damage, internal repair, counterfeit parts, or board-level faults without authorized hardware inspection. | Manual finding with disclaimer. |
| AI-assisted triage | Evidence-to-finding mapping with confidence, invalidators, and next tests | Deterministic triage agent over structured evidence | automatic | medium | AI output must never override raw evidence, platform limitation, or missing-data state. | Candidate failure modes with invalidators. |
| Report integrity | Signed report, verification endpoint, tamper detection | RSA signing and verification workflow | automatic | high | Signature proves report integrity, not truth of upstream evidence. | Verifiable report status. |

## Finding severity

| Severity | Definition | Action |
|---|---|---|
| `critical` | Evidence suggests safety, privacy, data-loss, or severe hardware-function risk. | Stop normal handoff; require expert review. |
| `major` | Core device function may be impaired or evidence is strong enough to affect acceptance. | Recommend retest or repair path before acceptance. |
| `minor` | Usability issue or weak signal with limited impact. | Record and monitor. |
| `info` | Capability, limitation, or observation without a defect claim. | Include as context only. |

## Required classification rule

Every report finding must include:

1. `fact`: what was directly observed.
2. `why_it_matters`: device-quality or workflow impact.
3. `evidence_strength`: high / medium / low / not_supported.
4. `invalidators`: conditions that could make the finding wrong.
5. `next_test`: the smallest retest that would increase confidence.

## Public-demo boundary

The public repository may show the workflow, schema, tests, synthetic examples, and report signing. It must not include real device serials, real defect photos, real customer information, proprietary logs, production credentials, or vendor-internal diagnostic procedures.
