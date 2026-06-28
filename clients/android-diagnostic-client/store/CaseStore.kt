class CaseStore(
    private val dataSource: DiagnosticDataSource = DiagnosticDataSource()
) {
    fun loadSampleCase(): DeviceCase {
        return dataSource.sampleCase()
    }
}
