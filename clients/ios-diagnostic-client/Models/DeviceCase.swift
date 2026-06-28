import Foundation

struct DeviceCase: Identifiable, Codable, Equatable {
    let id: String
    let deviceID: String
    let status: CaseStatus
    let buildPhase: BuildPhase
    let component: String
    let symptom: String
    let facts: [String]
    let hypotheses: [String]

    enum CodingKeys: String, CodingKey {
        case id = "case_id"
        case deviceID = "device_id"
        case status
        case buildPhase = "build_phase"
        case component
        case symptom
        case facts
        case hypotheses
    }
}

enum CaseStatus: String, Codable, CaseIterable {
    case new
    case evidenceCollected = "evidence_collected"
    case triaged
    case needsReproduction = "needs_reproduction"
    case assignedToDomainOwner = "assigned_to_domain_owner"
    case correctiveActionProposed = "corrective_action_proposed"
    case verificationPending = "verification_pending"
    case closed
}

enum BuildPhase: String, Codable, CaseIterable {
    case evt = "EVT"
    case dvt = "DVT"
    case pvt = "PVT"
    case mp = "MP"
    case unknown = "UNKNOWN"
}
