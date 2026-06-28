import SwiftUI

@main
struct DeviceInspectorShellApp: App {
    var body: some Scene {
        WindowGroup {
            CaseListView(viewModel: CaseListViewModel())
        }
    }
}
