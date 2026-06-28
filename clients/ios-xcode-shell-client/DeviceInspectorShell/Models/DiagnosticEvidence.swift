import Foundation

struct DiagnosticEvidence: Identifiable, Hashable {
    let id: String
    let caseID: String
    let source: String
    let severity: String
    let component: String
    let testName: String
    let message: String
    let metric: String
    let valueText: String
    let evidenceStrength: String
}
