import SwiftUI

struct CaseDetailView: View {
    @StateObject private var viewModel = CaseDetailViewModel()
    let caseID: String

    var body: some View {
        List {
            if let caseRecord = viewModel.caseRecord {
                Section("Case") {
                    Text(caseRecord.symptom)
                    Text(caseRecord.status.rawValue)
                    Text(caseRecord.buildPhase.rawValue)
                    Text(caseRecord.component)
                }
            }

            Section("Evidence") {
                ForEach(viewModel.evidence) { item in
                    VStack(alignment: .leading) {
                        Text(item.testName).font(.headline)
                        Text(item.message)
                        Text("Strength: \(item.evidenceStrength.rawValue)")
                    }
                }
            }

            if let errorMessage = viewModel.errorMessage {
                Section("Error") {
                    Text(errorMessage)
                }
            }
        }
        .navigationTitle("Diagnostic Case")
        .task {
            viewModel.load(caseID: caseID)
        }
    }
}
