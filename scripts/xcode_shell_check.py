"""Check that the iOS Xcode shell client exists."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = [
    "clients/ios-xcode-shell-client/DeviceInspectorShell.xcodeproj/project.pbxproj",
    "clients/ios-xcode-shell-client/DeviceInspectorShell.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/DeviceInspectorShellApp.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/Models/DeviceCase.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/Models/DiagnosticEvidence.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/Store/SampleCaseStore.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/ViewModels/CaseListViewModel.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/Views/CaseListView.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/Views/CaseDetailView.swift",
    "clients/ios-xcode-shell-client/DeviceInspectorShell/Networking/DiagnosticAPIClient.swift",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing Xcode shell files:")
        for path in missing:
            print(f"- {path}")
        return 1
    project = (ROOT / "clients/ios-xcode-shell-client/DeviceInspectorShell.xcodeproj/project.pbxproj").read_text(encoding="utf-8")
    for term in ["PBXProject", "PBXNativeTarget", "DeviceInspectorShell"]:
        if term not in project:
            print(f"Missing Xcode project marker: {term}")
            return 1
    print("Xcode shell check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
