class CaseViewModel(
    private val store: CaseStore = CaseStore()
) {
    var currentCase: DeviceCase? = null
        private set

    fun load() {
        currentCase = store.loadSampleCase()
    }
}
