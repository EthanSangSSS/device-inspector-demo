import Foundation

struct SampleCaseStore {
    static let cases: [DeviceCase] = [
        DeviceCase(
            id: "SYNTH-CASE-THERMAL-001",
            deviceID: "SYNTH-DEVICE-THERMAL-001",
            status: .triaged,
            buildPhase: .dvt,
            component: "thermal_system",
            symptom: "Thermal drift during synthetic camera stress loop",
            facts: ["Synthetic thermal delta exceeded demo limit."],
            hypotheses: ["Heat-spreader contact variance."]
        ),
        DeviceCase(
            id: "SYNTH-CASE-CONNECTOR-001",
            deviceID: "SYNTH-DEVICE-CONNECTOR-001",
            status: .needsReproduction,
            buildPhase: .evt,
            component: "connector",
            symptom: "Intermittent connector continuity loss under synthetic vibration loop",
            facts: ["Synthetic continuity drop observed in 3 of 10 runs."],
            hypotheses: ["Connector seating variation."]
        )
    ]

    static let evidenceByCase: [String: [DiagnosticEvidence]] = [
        "SYNTH-CASE-THERMAL-001": [
            DiagnosticEvidence(
                id: "SYNTH-LOG-THERMAL-001",
                caseID: "SYNTH-CASE-THERMAL-001",
                source: "thermal_sensor_mock",
                severity: "warning",
                component: "thermal_system",
                testName: "camera_stress_loop",
                message: "Thermal envelope exceeded expected synthetic range.",
                metric: "surface_temp_delta_c",
                valueText: "8.4 C / limit 5.0 C",
                evidenceStrength: "medium"
            )
        ],
        "SYNTH-CASE-CONNECTOR-001": [
            DiagnosticEvidence(
                id: "SYNTH-LOG-CONNECTOR-001",
                caseID: "SYNTH-CASE-CONNECTOR-001",
                source: "fixture_continuity_mock",
                severity: "warning",
                component: "connector",
                testName: "vibration_continuity_loop",
                message: "Connector continuity loss observed during synthetic vibration loop.",
                metric: "continuity_drop_count",
                valueText: "3 / limit 0",
                evidenceStrength: "medium"
            )
        ]
    ]
}
