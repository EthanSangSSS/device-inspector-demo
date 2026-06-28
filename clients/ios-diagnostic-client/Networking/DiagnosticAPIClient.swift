import Combine
import Foundation

final class DiagnosticAPIClient {
    private let baseURL: URL
    private let session: URLSession

    init(baseURL: URL = URL(string: "http://127.0.0.1:5001")!, session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
    }

    func fetchCase(caseID: String) -> AnyPublisher<CaseEnvelope, Error> {
        var request = URLRequest(url: baseURL.appendingPathComponent("cases/\(caseID)"))
        request.httpMethod = "GET"
        return session.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: CaseEnvelope.self, decoder: JSONDecoder())
            .eraseToAnyPublisher()
    }

    func postEvidence(_ evidence: DiagnosticEvidence) -> AnyPublisher<EvidenceEnvelope, Error> {
        var request = URLRequest(url: baseURL.appendingPathComponent("cases/\(evidence.caseID)/evidence"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONEncoder().encode(evidence)
        return session.dataTaskPublisher(for: request)
            .map(\.data)
            .decode(type: EvidenceEnvelope.self, decoder: JSONDecoder())
            .eraseToAnyPublisher()
    }
}

struct CaseEnvelope: Codable {
    let `case`: DeviceCase
    let evidence: [DiagnosticEvidence]
}

struct EvidenceEnvelope: Codable {
    let evidence: DiagnosticEvidence
}
