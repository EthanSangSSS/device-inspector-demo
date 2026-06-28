"""Public-safe CV/VLM interface stub.

This module intentionally does not load model weights or process real defect images.
It defines the data contract that a future approved CV/VLM component would satisfy.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class VisualDefectObservation:
    image_id: str
    defect_type: str
    confidence: str
    evidence_note: str
    requires_human_review: bool = True


def inspect_synthetic_image(metadata: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic mock visual observation.

    The input is metadata only. No binary image data is accepted in this public demo.
    """

    image_id = str(metadata.get("image_id", "SYNTH-IMAGE-UNKNOWN"))
    hint = str(metadata.get("synthetic_hint", "")).lower()

    if "scratch" in hint:
        observation = VisualDefectObservation(
            image_id=image_id,
            defect_type="surface-scratch-candidate",
            confidence="low",
            evidence_note="Synthetic metadata suggests a scratch-like artifact; image review is required.",
        )
    elif "thermal" in hint:
        observation = VisualDefectObservation(
            image_id=image_id,
            defect_type="thermal-discoloration-candidate",
            confidence="low",
            evidence_note="Synthetic metadata suggests thermal discoloration; correlate with sensor logs.",
        )
    else:
        observation = VisualDefectObservation(
            image_id=image_id,
            defect_type="unknown-visual-anomaly",
            confidence="low",
            evidence_note="No reliable synthetic visual hint found.",
        )

    return asdict(observation)
