# DeviceInspectorShell

A minimal SwiftUI Xcode project for the public-safe Device Inspector demo.

## Purpose

This is a real `.xcodeproj` shell that can be opened in Xcode and used as the starting point for an iOS diagnostic client. It keeps all sample records synthetic and routes user-facing inspection concepts into the public hardware-diagnostics workflow.

## What it demonstrates

- SwiftUI app entry point.
- Case list and case detail screens.
- Observable view model state.
- Synthetic case and evidence models.
- Local sample store.
- API client placeholder pointed at the local Flask demo.

## Open in Xcode

```bash
open clients/ios-xcode-shell-client/DeviceInspectorShell.xcodeproj
```

The project is intentionally dependency-free. A future PR can add a real network adapter, CoreData model, and unit-test target.
