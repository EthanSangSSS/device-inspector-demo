data class DiagnosticEvidence(
    val logId: String,
    val caseId: String,
    val deviceId: String,
    val source: String,
    val severity: String,
    val component: String,
    val testName: String,
    val message: String,
    val measurement: DiagnosticMeasurement? = null,
    val reproductionRate: String = "unknown",
    val evidenceStrength: String
)

data class DiagnosticMeasurement(
    val metric: String,
    val value: Double,
    val unit: String,
    val limit: Double? = null
)
