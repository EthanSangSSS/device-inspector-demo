"""Generate deterministic synthetic visual triage evaluation reports."""

from __future__ import annotations

import csv
import json
import pathlib
from collections import defaultdict
from typing import Any

from evaluate_triage import evaluate

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "ml" / "reports"
LABELS = [
    "thermal-discoloration-candidate",
    "surface-scratch-candidate",
    "unknown-visual-anomaly",
]


def build_confusion_matrix(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    matrix: dict[str, dict[str, int]] = {
        expected: {predicted: 0 for predicted in LABELS} for expected in LABELS
    }
    for row in rows:
        matrix[row["expected_label"]][row["predicted_label"]] += 1
    return matrix


def per_label_metrics(matrix: dict[str, dict[str, int]]) -> list[dict[str, Any]]:
    metrics = []
    for label in LABELS:
        tp = matrix[label][label]
        fp = sum(matrix[other][label] for other in LABELS if other != label)
        fn = sum(matrix[label][other] for other in LABELS if other != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        metrics.append({
            "label": label,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": sum(matrix[label].values()),
        })
    return metrics


def write_json_report(result: dict[str, Any], matrix: dict[str, dict[str, int]], metrics: list[dict[str, Any]]) -> None:
    payload = {
        "summary": {
            "sample_count": result["sample_count"],
            "accuracy": result["accuracy"],
            "data_boundary": "synthetic metadata only",
            "decision_boundary": "engineering hint; not root cause",
        },
        "labels": LABELS,
        "confusion_matrix": matrix,
        "per_label_metrics": metrics,
        "rows": result["rows"],
    }
    (REPORT_DIR / "synthetic_cv_metrics.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
    )


def write_csv_matrix(matrix: dict[str, dict[str, int]]) -> None:
    with (REPORT_DIR / "confusion_matrix.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["expected_label", *LABELS])
        for expected in LABELS:
            writer.writerow([expected, *[matrix[expected][predicted] for predicted in LABELS]])


def write_markdown(result: dict[str, Any], matrix: dict[str, dict[str, int]], metrics: list[dict[str, Any]]) -> None:
    lines = [
        "# Synthetic CV Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Sample count: {result['sample_count']}",
        f"- Accuracy: {result['accuracy']:.4f}",
        "- Data boundary: synthetic metadata only",
        "- Decision boundary: engineering hint, not root cause",
        "",
        "## Confusion matrix",
        "",
        "| Expected \\ Predicted | " + " | ".join(LABELS) + " |",
        "|---|" + "---|" * len(LABELS),
    ]
    for expected in LABELS:
        lines.append("| " + expected + " | " + " | ".join(str(matrix[expected][predicted]) for predicted in LABELS) + " |")
    lines.extend([
        "",
        "## Per-label metrics",
        "",
        "| Label | Precision | Recall | F1 | Support |",
        "|---|---:|---:|---:|---:|",
    ])
    for item in metrics:
        lines.append(
            f"| {item['label']} | {item['precision']:.4f} | {item['recall']:.4f} | {item['f1']:.4f} | {item['support']} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "The current classifier is deterministic and metadata-driven. Perfect performance here only proves that the evaluation pipeline is wired correctly for synthetic labels. It does not imply real visual defect performance.",
    ])
    (REPORT_DIR / "synthetic_cv_eval_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_svg_matrix(matrix: dict[str, dict[str, int]]) -> None:
    cell = 170
    header = 90
    width = header + cell * len(LABELS)
    height = header + cell * len(LABELS)
    max_value = max(max(row.values()) for row in matrix.values()) or 1
    parts = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='white'/>",
        "<text x='20' y='32' font-size='18' font-family='Helvetica'>Synthetic confusion matrix</text>",
    ]
    for index, label in enumerate(LABELS):
        short = label.replace("-candidate", "").replace("-", " ")
        parts.append(f"<text x='{header + index * cell + 8}' y='70' font-size='12' font-family='Helvetica'>{short}</text>")
        parts.append(f"<text x='8' y='{header + index * cell + 28}' font-size='12' font-family='Helvetica'>{short}</text>")
    for row_index, expected in enumerate(LABELS):
        for col_index, predicted in enumerate(LABELS):
            value = matrix[expected][predicted]
            shade = 245 - int(120 * value / max_value)
            x = header + col_index * cell
            y = header + row_index * cell
            parts.append(f"<rect x='{x}' y='{y}' width='{cell}' height='{cell}' fill='rgb({shade},{shade},{shade})' stroke='black'/>")
            parts.append(f"<text x='{x + cell / 2 - 6}' y='{y + cell / 2 + 6}' font-size='20' font-family='Helvetica'>{value}</text>")
    parts.append("</svg>")
    (REPORT_DIR / "confusion_matrix.svg").write_text("\n".join(parts), encoding="utf-8")


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    result = evaluate()
    matrix = build_confusion_matrix(result["rows"])
    metrics = per_label_metrics(matrix)
    write_json_report(result, matrix, metrics)
    write_csv_matrix(matrix)
    write_markdown(result, matrix, metrics)
    write_svg_matrix(matrix)
    print(f"Wrote reports to {REPORT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
