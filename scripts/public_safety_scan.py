"""Lightweight public-safety scan for demo repositories.

This is intentionally conservative. It looks for patterns that should not appear
in a public hardware diagnostics demo.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DENY_PATTERNS = {
    "possible_imei_15_digits": re.compile(r"\b\d{15}\b"),
    "private_key_block": re.compile(r"BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY"),
    "common_secret_assignment": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]+['\"]"),
}
ALLOWLISTED_PATH_PARTS = {".git", ".venv", "__pycache__"}
ALLOWLISTED_FILES = {"public_safety_scan.py"}


def should_skip(path: pathlib.Path) -> bool:
    return any(part in ALLOWLISTED_PATH_PARTS for part in path.parts)


def main() -> int:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.name in ALLOWLISTED_FILES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in DENY_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{name}: {path.relative_to(ROOT)}")

    if findings:
        print("Public-safety scan failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Public-safety scan passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
