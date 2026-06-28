"""Deterministic synthetic visual classifier.

This module uses metadata hints only. It exists to demonstrate an evaluation
contract for diagnostic triage, not production model performance.
"""

from __future__ import annotations

from typing import Any


def classify(metadata: dict[str, Any]) -> dict[str, Any]:
    image_id = str(metadata.get("image_id", "SYNTH-IMAGE-UNKNOWN"))
    hint = str(metadata.get("synthetic_hint", "")).lower()
    if "thermal" in hint:
        label = "thermal-discoloration-candidate"
    elif "scratch" in hint:
        label = "surface-scratch-candidate"
    else:
        label = "unknown-visual-anomaly"
    return {
        "image_id": image_id,
        "predicted_label": label,
        "confidence": "low",
        "requires_human_review": True,
    }
