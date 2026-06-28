"""Evaluate the deterministic synthetic visual classifier."""

from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ml" / "models"))

from cv_baseline import classify  # noqa: E402


def evaluate() -> dict[str, object]:
    manifest_path = ROOT / "ml" / "data" / "synthetic_defect_manifest.json"
    examples = json.loads(manifest_path.read_text(encoding="utf-8"))
    correct = 0
    rows = []
    for item in examples:
        prediction = classify(item)
        is_correct = prediction["predicted_label"] == item["expected_label"]
        correct += int(is_correct)
        rows.append({
            "image_id": item["image_id"],
            "expected_label": item["expected_label"],
            "predicted_label": prediction["predicted_label"],
            "correct": is_correct,
        })
    accuracy = correct / len(examples) if examples else 0.0
    return {"sample_count": len(examples), "accuracy": accuracy, "rows": rows}


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["accuracy"] == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
