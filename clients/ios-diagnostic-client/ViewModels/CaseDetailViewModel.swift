import Combine
import Foundation

@MainActor
final class CaseDetailViewModel: ObservableObject {
    @Published private(set) var caseRecord: DeviceCase?
    @Published private(set) var evidence: [DiagnosticEvidence] = []
    @Published var errorMessage: String?

    private let apiClient: DiagnosticAPIClient
    private var cancellables = Set<AnyCancellable>()

    init(apiClient: DiagnosticAPIClient = DiagnosticAPIClient()) {
        self.apiClient = apiClient
    }

    func load(caseID: String) {
        apiClient.fetchCase(caseID: caseID)
            .receive(on: DispatchQueue.main)
            .sink { [weak self] completion in
                if case let .failure(error) = completion {
                    self?.errorMessage = error.localizedDescription
                }
            } receiveValue: { [weak self] envelope in
                self?.caseRecord = envelope.case
                self?.evidence = envelope.evidence
            }
            .store(in: &cancellables)
    }
}
