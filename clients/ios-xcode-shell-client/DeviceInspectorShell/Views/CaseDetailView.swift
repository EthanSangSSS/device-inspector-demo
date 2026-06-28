import SwiftUI

struct CaseDetailView: View {
    let caseRecord: DeviceCase
    let evidence: [DiagnosticEvidence]

    var body: some View {
        List {
            Section("Case") {
                LabeledContent("ID", value: caseRecord.id)
                LabeledContent("Build phase", value: caseRecord.buildPhase.rawValue)
                LabeledContent("Component", value: caseRecord.component)
                LabeledContent("Status", value: caseRecord.status.rawValue)
                Text(caseRecord.symptom)
            }

            Section("Facts") {
                ForEach(caseRecord.facts, id: \.self) { fact in
                    Text(fact)
                }
            }

            Section("Hypotheses") {
                ForEach(caseRecord.hypotheses, id: \.self) { hypothesis in
                    Text(hypothesis)
                }
            }

            Section("Evidence") {
                ForEach(evidence) { item in
                    VStack(alignment: .leading, spacing: 6) {
                        Text(item.testName).font(.headline)
                        Text(item.message)
                        Text("\(item.metric): \(item.valueText)")
                            .font(.caption)
                            .foregroundStyle(.secondary)
                        Text("Strength: \(item.evidenceStrength)")
                            .font(.caption)
                    }
                }
            }
        }
        .navigationTitle("Diagnostic Case")
    }
}
