fun renderCaseDetail(caseRecord: DeviceCase): String {
    return buildString {
        appendLine("Case: ${caseRecord.caseId}")
        appendLine("Status: ${caseRecord.status}")
        appendLine("Build phase: ${caseRecord.buildPhase}")
        appendLine("Component: ${caseRecord.component}")
        appendLine("Symptom: ${caseRecord.symptom}")
    }
}
