"""Run and validate synthetic CV evaluation report generation."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPORTS = [
    "ml/reports/synthetic_cv_metrics.json",
    "ml/reports/confusion_matrix.csv",
    "ml/reports/synthetic_cv_eval_report.md",
    "ml/reports/confusion_matrix.svg",
]


def main() -> int:
    subprocess.run([sys.executable, "ml/evaluation/generate_eval_report.py"], cwd=ROOT, check=True)
    missing = [path for path in REPORTS if not (ROOT / path).exists()]
    if missing:
        print("Missing synthetic CV reports:")
        for path in missing:
            print(f"- {path}")
        return 1
    metrics = json.loads((ROOT / "ml/reports/synthetic_cv_metrics.json").read_text(encoding="utf-8"))
    if metrics["summary"]["sample_count"] < 3:
        print("Expected at least 3 synthetic samples")
        return 1
    if "confusion_matrix" not in metrics:
        print("Metrics report missing confusion matrix")
        return 1
    print("Synthetic CV report check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
