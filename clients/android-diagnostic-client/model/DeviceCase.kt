data class DeviceCase(
    val caseId: String,
    val deviceId: String,
    val status: String,
    val buildPhase: String,
    val component: String,
    val symptom: String,
    val facts: List<String> = emptyList(),
    val hypotheses: List<String> = emptyList()
)
