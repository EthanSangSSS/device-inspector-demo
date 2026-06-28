import SwiftUI

struct CaseListView: View {
    @State var viewModel: CaseListViewModel

    var body: some View {
        NavigationStack {
            List(viewModel.cases) { caseRecord in
                NavigationLink(value: caseRecord) {
                    VStack(alignment: .leading, spacing: 6) {
                        Text(caseRecord.symptom)
                            .font(.headline)
                        Text("\(caseRecord.buildPhase.rawValue) · \(caseRecord.component) · \(caseRecord.status.rawValue)")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                }
            }
            .navigationTitle("Device Inspector")
            .navigationDestination(for: DeviceCase.self) { caseRecord in
                CaseDetailView(caseRecord: caseRecord, evidence: viewModel.evidence(for: caseRecord))
            }
        }
    }
}
