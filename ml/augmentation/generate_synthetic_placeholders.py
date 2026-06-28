"""Generate plain-text placeholders for synthetic visual examples."""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "ml" / "generated"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT / "ml" / "data" / "synthetic_defect_manifest.json").read_text(encoding="utf-8"))
    for item in manifest:
        path = OUT_DIR / f"{item['image_id']}.txt"
        path.write_text(f"synthetic placeholder: {item['expected_label']}\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
