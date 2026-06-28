"""Check that iOS and Android public-safe client skeletons are present."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED = [
    "clients/ios-diagnostic-client/Models/DeviceCase.swift",
    "clients/ios-diagnostic-client/Models/DiagnosticEvidence.swift",
    "clients/ios-diagnostic-client/Networking/DiagnosticAPIClient.swift",
    "clients/ios-diagnostic-client/Persistence/PersistenceController.swift",
    "clients/ios-diagnostic-client/ViewModels/CaseDetailViewModel.swift",
    "clients/ios-diagnostic-client/Views/CaseDetailView.swift",
    "clients/android-diagnostic-client/model/DeviceCase.kt",
    "clients/android-diagnostic-client/model/DiagnosticEvidence.kt",
    "clients/android-diagnostic-client/data/DiagnosticDataSource.kt",
    "clients/android-diagnostic-client/store/CaseStore.kt",
    "clients/android-diagnostic-client/viewmodel/CaseViewModel.kt",
    "clients/android-diagnostic-client/ui/CaseDetailScreen.kt",
]


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        print("Missing mobile skeleton files:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("Mobile skeleton check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
