# Known Limitations

This document prevents diagnostic overclaiming. Device Inspector is an evidence workbench, not an authorized service-center diagnostic system, not a guarantee of device authenticity, and not a substitute for destructive or fixture-based hardware analysis.

## Platform-access limitations

| Area | Limitation | Required wording in product/report |
|---|---|---|
| Device identity | Public mobile APIs do not expose all serial, IMEI, component, repair, or internal manufacturing records to third-party apps. | `This report uses public device and session metadata only. It does not verify factory serial records or ownership history.` |
| Battery health | iOS and Android third-party access to battery cycle count, health, and component provenance is limited and varies by vendor/API. | `Battery status is a public-API summary and may require service diagnostics for confirmation.` |
| Repair / tamper history | App-only inspection cannot reliably detect replaced displays, batteries, board repairs, or counterfeit parts. | `Repair and tamper findings require authorized diagnostics or physical inspection.` |
| Water damage | App-only inspection cannot reliably detect liquid-contact indicator state or board corrosion. | `Liquid damage cannot be ruled out by this app.` |
| Network and radio diagnostics | OS privacy controls restrict SSID/BSSID, radio scanning, and low-level modem/Wi-Fi/Bluetooth data. | `Connectivity checks are readiness checks, not RF lab measurements.` |

## Display limitations

| Test | Limitation | Mitigation |
|---|---|---|
| Uniformity | Ambient light, brightness, color temperature, screen protector, viewing angle, OLED aging, and camera exposure can alter results. | Require brightness/environment metadata and mark user-visible checks as `guided`. |
| Dead/stuck pixels | Very small defects require close inspection or magnification. | Provide RGBW/black patterns and record user confirmation instead of automatic certainty. |
| HDR / P3 / wide gamut | Declared support is not the same as measured EOTF, gamut coverage, or tone-mapping accuracy. | Separate `declared capability` from `measured performance`. |
| Refresh-rate/flicker | OS compositor, power mode, brightness, LTPO/LTPS strategy, and app foreground state affect behavior. | Record settings and recommend repeated tests under controlled conditions. |
| PWM / temporal artifacts | Reliable quantification needs a camera/probe/oscilloscope fixture. | Treat app-only flicker as qualitative observation. |

## Sensor and audio limitations

- Sensor values can be affected by calibration, table vibration, magnetic interference, case accessories, and OS-level sensor fusion.
- Microphone and speaker checks are affected by environmental noise, volume, permissions, and device routing.
- Haptics are user-perceived unless an external fixture measures vibration.
- Camera optical defects require controlled lighting, focus charts, and exposure control; public demo must not store real user photos by default.

## AI-assisted triage limitations

The AI-assisted triage layer must remain deterministic and evidence-bounded in this public demo.

It must not:

- claim autonomous hardware diagnosis;
- invent missing sensor values;
- treat user perception as high-confidence telemetry;
- infer private identity, ownership, repair history, or fraud;
- hide invalidators or missing-data states;
- override raw evidence or platform limitations.

Every AI triage result must include facts, confidence, invalidators, and next tests.

## Public repository safety boundary

This public repository must not contain:

- real serial numbers, IMEI/MEID, UDID, owner account, phone number, carrier account, or asset tags;
- real defect photos, customer logs, production crash logs, private supplier files, or internal company procedures;
- production cloud credentials, signing keys, certificates, tokens, or API secrets;
- proprietary App Store Connect, vendor diagnostic, or hardware service workflows;
- private model weights or datasets derived from real device images.

## Report integrity limitation

A signed report proves that the report payload has not been modified after signing. It does not prove that upstream evidence was collected truthfully, that the device was not substituted, or that the user did not misreport a guided/manual test. Production deployments require trusted capture, access control, audit logging, retention policy, and device/session binding.

## Release gate

Before any production-oriented claim is added to README, App Store metadata, job-demo materials, or investor/product decks, the claim must be mapped to:

1. an inspection matrix row;
2. a validation-log entry;
3. a report-schema field;
4. a known limitation or invalidator;
5. a deterministic test, fixture result, or manual evidence path.
