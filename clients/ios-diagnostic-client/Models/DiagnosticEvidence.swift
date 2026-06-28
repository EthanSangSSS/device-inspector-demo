import Foundation

struct DiagnosticEvidence: Identifiable, Codable, Equatable {
    let id: String
    let caseID: String
    let deviceID: String
    let source: String
    let severity: Severity
    let component: String
    let testName: String
    let message: String
    let measurement: Measurement?
    let reproductionRate: String
    let evidenceStrength: EvidenceStrength

    enum CodingKeys: String, CodingKey {
        case id = "log_id"
        case caseID = "case_id"
        case deviceID = "device_id"
        case source
        case severity
        case component
        case testName = "test_name"
        case message
        case measurement
        case reproductionRate = "reproduction_rate"
        case evidenceStrength = "evidence_strength"
    }
}

struct Measurement: Codable, Equatable {
    let metric: String
    let value: Double
    let unit: String
    let limit: Double?
}

enum Severity: String, Codable, CaseIterable {
    case info
    case warning
    case critical
}

enum EvidenceStrength: String, Codable, CaseIterable {
    case low
    case medium
    case high
}
