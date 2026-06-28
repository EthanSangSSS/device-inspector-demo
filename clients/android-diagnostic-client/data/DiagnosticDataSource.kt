class DiagnosticDataSource {
    fun sampleCase(): DeviceCase {
        return DeviceCase(
            caseId = "SYNTH-CASE-MOBILE-001",
            deviceId = "SYNTH-DEVICE-MOBILE-001",
            status = "new",
            buildPhase = "DVT",
            component = "thermal_system",
            symptom = "Synthetic mobile diagnostic case",
            facts = listOf("Synthetic fact"),
            hypotheses = listOf("Synthetic hypothesis")
        )
    }
}
