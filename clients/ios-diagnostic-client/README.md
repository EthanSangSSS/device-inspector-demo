# iOS Diagnostic Client Skeleton

Public-safe SwiftUI skeleton for a synthetic hardware diagnostic client.

## Purpose

This client demonstrates the architecture expected from an iOS-facing diagnostic evidence collection tool while keeping all records synthetic.

## Architecture

```text
SwiftUI Views
  -> Combine ViewModels
  -> DiagnosticAPIClient
  -> CoreData local synthetic case cache
  -> Flask demo backend
```

## Files

- `Models/DeviceCase.swift`
- `Models/DiagnosticEvidence.swift`
- `Networking/DiagnosticAPIClient.swift`
- `Persistence/PersistenceController.swift`
- `ViewModels/CaseDetailViewModel.swift`
- `Views/CaseDetailView.swift`

## Next implementation step

Create an Xcode project around these source files, add unit tests for `DiagnosticAPIClient`, and wire CoreData entities to the synthetic case model.
