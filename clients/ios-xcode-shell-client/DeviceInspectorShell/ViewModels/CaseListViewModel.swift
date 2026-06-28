import Foundation
import Observation

@Observable
final class CaseListViewModel {
    private(set) var cases: [DeviceCase]
    private let evidenceByCase: [String: [DiagnosticEvidence]]

    init(
        cases: [DeviceCase] = SampleCaseStore.cases,
        evidenceByCase: [String: [DiagnosticEvidence]] = SampleCaseStore.evidenceByCase
    ) {
        self.cases = cases
        self.evidenceByCase = evidenceByCase
    }

    func evidence(for caseRecord: DeviceCase) -> [DiagnosticEvidence] {
        evidenceByCase[caseRecord.id] ?? []
    }
}
