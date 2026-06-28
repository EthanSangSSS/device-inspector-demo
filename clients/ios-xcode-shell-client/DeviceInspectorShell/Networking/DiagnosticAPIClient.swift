import Foundation

struct DiagnosticAPIClient {
    let baseURL = URL(string: "http://127.0.0.1:5001")!

    func caseURL(caseID: String) -> URL {
        baseURL.appending(path: "cases").appending(path: caseID)
    }

    func evidenceURL(caseID: String) -> URL {
        baseURL.appending(path: "cases").appending(path: caseID).appending(path: "evidence")
    }
}
