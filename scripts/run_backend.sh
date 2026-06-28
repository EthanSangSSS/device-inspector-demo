#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT/backend/flask_api"

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
