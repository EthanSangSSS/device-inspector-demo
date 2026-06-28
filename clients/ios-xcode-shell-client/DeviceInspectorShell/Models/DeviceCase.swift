import Foundation

struct DeviceCase: Identifiable, Hashable {
    let id: String
    let deviceID: String
    var status: CaseStatus
    let buildPhase: BuildPhase
    let component: String
    let symptom: String
    let facts: [String]
    let hypotheses: [String]
}

enum CaseStatus: String, CaseIterable, Hashable {
    case new
    case evidenceCollected = "evidence_collected"
    case triaged
    case needsReproduction = "needs_reproduction"
    case assignedToDomainOwner = "assigned_to_domain_owner"
    case correctiveActionProposed = "corrective_action_proposed"
    case verificationPending = "verification_pending"
    case closed
}

enum BuildPhase: String, CaseIterable, Hashable {
    case evt = "EVT"
    case dvt = "DVT"
    case pvt = "PVT"
    case mp = "MP"
    case unknown = "UNKNOWN"
}
