"""Check that the public demo documents its origin without private leakage."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "docs/origin_bridge.md",
    "docs/demo_from_product_principles.md",
]
REQUIRED_README_TERMS = [
    "origin_bridge.md",
    "public-safe engineering abstraction",
]
FORBIDDEN_TERMS = [
    "/Users/",
    "EthandeMac-Studio",
    "device-inspector-private.git",
    "private endpoint",
    "production endpoint",
]


def main() -> int:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        print("Missing origin bridge docs:")
        for path in missing:
            print(f"- {path}")
        return 1

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    missing_terms = [term for term in REQUIRED_README_TERMS if term not in readme]
    if missing_terms:
        print("README missing origin bridge terms:")
        for term in missing_terms:
            print(f"- {term}")
        return 1

    combined = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.md"))
    leaked = [term for term in FORBIDDEN_TERMS if term in combined]
    if leaked:
        print("Potential private-origin leakage detected:")
        for term in leaked:
            print(f"- {term}")
        return 1

    print("Origin bridge check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
