"""SQLite repository for the public-safe diagnostics demo."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class DiagnosticRepository:
    """Small SQLite wrapper used by the Flask demo.

    The default path can be ':memory:' for tests. Production-grade deployments would need
    migrations, encryption-at-rest policy, access control, backup policy, and retention policy.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._connection = sqlite3.connect(db_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self.init_schema()

    def init_schema(self) -> None:
        cur = self._connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnostic_logs (
                log_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(device_id) REFERENCES devices(device_id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                report_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                signature TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(device_id) REFERENCES devices(device_id)
            )
            """
        )
        self._connection.commit()

    def reset(self) -> None:
        cur = self._connection.cursor()
        cur.execute("DELETE FROM reports")
        cur.execute("DELETE FROM diagnostic_logs")
        cur.execute("DELETE FROM devices")
        self._connection.commit()

    def save_device(self, device: dict[str, Any]) -> dict[str, Any]:
        device_id = require_synthetic_identifier(device.get("device_id"), "device_id")
        self._connection.execute(
            "INSERT OR REPLACE INTO devices(device_id, payload_json) VALUES (?, ?)",
            (device_id, json.dumps(device, sort_keys=True)),
        )
        self._connection.commit()
        return device

    def save_log(self, log: dict[str, Any]) -> dict[str, Any]:
        log_id = require_synthetic_identifier(log.get("log_id"), "log_id")
        device_id = require_synthetic_identifier(log.get("device_id"), "device_id")
        if self.get_device(device_id) is None:
            raise ValueError(f"Unknown device_id: {device_id}")
        self._connection.execute(
            "INSERT OR REPLACE INTO diagnostic_logs(log_id, device_id, payload_json) VALUES (?, ?, ?)",
            (log_id, device_id, json.dumps(log, sort_keys=True)),
        )
        self._connection.commit()
        return log

    def save_report(self, report: dict[str, Any], signature: str) -> dict[str, Any]:
        report_id = require_synthetic_identifier(report.get("report_id"), "report_id")
        device_id = require_synthetic_identifier(report.get("device_id"), "device_id")
        self._connection.execute(
            "INSERT OR REPLACE INTO reports(report_id, device_id, payload_json, signature) VALUES (?, ?, ?, ?)",
            (report_id, device_id, json.dumps(report, sort_keys=True), signature),
        )
        self._connection.commit()
        return {"report": report, "signature": signature}

    def get_device(self, device_id: str) -> dict[str, Any] | None:
        row = self._connection.execute(
            "SELECT payload_json FROM devices WHERE device_id = ?", (device_id,)
        ).fetchone()
        return json.loads(row["payload_json"]) if row else None

    def list_logs(self, device_id: str) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT payload_json FROM diagnostic_logs WHERE device_id = ? ORDER BY created_at, log_id",
            (device_id,),
        ).fetchall()
        return [json.loads(row["payload_json"]) for row in rows]

    def get_report(self, report_id: str) -> dict[str, Any] | None:
        row = self._connection.execute(
            "SELECT payload_json, signature FROM reports WHERE report_id = ?", (report_id,)
        ).fetchone()
        if not row:
            return None
        return {"report": json.loads(row["payload_json"]), "signature": row["signature"]}


def require_synthetic_identifier(value: Any, field: str) -> str:
    """Reject identifiers that do not carry the SYNTH- prefix.

    This public demo intentionally refuses plausible real device identifiers.
    """

    if not isinstance(value, str) or not value.startswith("SYNTH-"):
        raise ValueError(f"{field} must be a synthetic identifier prefixed with SYNTH-")
    return value
