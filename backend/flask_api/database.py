"""SQLite repository for the public-safe diagnostics demo."""

from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from schemas import normalize_case, normalize_evidence, normalize_status, require_synthetic_identifier


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
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(device_id) REFERENCES devices(device_id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS diagnostic_logs (
                log_id TEXT PRIMARY KEY,
                case_id TEXT,
                device_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(case_id) REFERENCES cases(case_id),
                FOREIGN KEY(device_id) REFERENCES devices(device_id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                report_id TEXT PRIMARY KEY,
                case_id TEXT,
                device_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                signature TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(case_id) REFERENCES cases(case_id),
                FOREIGN KEY(device_id) REFERENCES devices(device_id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                case_id TEXT,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._connection.commit()

    def reset(self) -> None:
        cur = self._connection.cursor()
        cur.execute("DELETE FROM audit_events")
        cur.execute("DELETE FROM reports")
        cur.execute("DELETE FROM diagnostic_logs")
        cur.execute("DELETE FROM cases")
        cur.execute("DELETE FROM devices")
        self._connection.commit()

    def save_device(self, device: dict[str, Any]) -> dict[str, Any]:
        device_id = require_synthetic_identifier(device.get("device_id"), "device_id")
        payload = dict(device)
        payload.setdefault("privacy_class", "synthetic")
        self._connection.execute(
            "INSERT OR REPLACE INTO devices(device_id, payload_json) VALUES (?, ?)",
            (device_id, json.dumps(payload, sort_keys=True)),
        )
        self._connection.commit()
        return payload

    def save_case(self, case: dict[str, Any], actor: str = "system") -> dict[str, Any]:
        normalized = normalize_case(case)
        if self.get_device(normalized["device_id"]) is None:
            raise ValueError(f"Unknown device_id: {normalized['device_id']}")
        self._connection.execute(
            """
            INSERT OR REPLACE INTO cases(case_id, device_id, status, payload_json, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                normalized["case_id"],
                normalized["device_id"],
                normalized["status"],
                json.dumps(normalized, sort_keys=True),
            ),
        )
        self._connection.commit()
        self.record_audit_event(normalized["case_id"], actor, "case.upsert", normalized)
        return normalized

    def update_case_status(self, case_id: str, status: str, actor: str = "system") -> dict[str, Any]:
        case_id = require_synthetic_identifier(case_id, "case_id")
        normalized_status = normalize_status(status)
        case = self.get_case(case_id)
        if case is None:
            raise ValueError(f"Unknown case_id: {case_id}")
        case["status"] = normalized_status
        self._connection.execute(
            "UPDATE cases SET status = ?, payload_json = ?, updated_at = CURRENT_TIMESTAMP WHERE case_id = ?",
            (normalized_status, json.dumps(case, sort_keys=True), case_id),
        )
        self._connection.commit()
        self.record_audit_event(case_id, actor, "case.status.update", {"status": normalized_status})
        return case

    def save_log(self, log: dict[str, Any], actor: str = "system") -> dict[str, Any]:
        if "case_id" in log:
            normalized = normalize_evidence(log)
            if self.get_case(normalized["case_id"]) is None:
                raise ValueError(f"Unknown case_id: {normalized['case_id']}")
        else:
            # Backward-compatible baseline path for simple device logs.
            log_id = require_synthetic_identifier(log.get("log_id"), "log_id")
            device_id = require_synthetic_identifier(log.get("device_id"), "device_id")
            normalized = dict(log)
            normalized["log_id"] = log_id
            normalized["device_id"] = device_id
            normalized.setdefault("privacy_class", "synthetic")
        if self.get_device(normalized["device_id"]) is None:
            raise ValueError(f"Unknown device_id: {normalized['device_id']}")
        self._connection.execute(
            """
            INSERT OR REPLACE INTO diagnostic_logs(log_id, case_id, device_id, payload_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                normalized["log_id"],
                normalized.get("case_id"),
                normalized["device_id"],
                json.dumps(normalized, sort_keys=True),
            ),
        )
        self._connection.commit()
        if normalized.get("case_id"):
            self.record_audit_event(normalized["case_id"], actor, "evidence.upsert", normalized)
        return normalized

    def save_report(self, report: dict[str, Any], signature: str) -> dict[str, Any]:
        report_id = require_synthetic_identifier(report.get("report_id"), "report_id")
        device_id = require_synthetic_identifier(report.get("device_id"), "device_id")
        case_id = report.get("case_id")
        if case_id is not None:
            require_synthetic_identifier(case_id, "case_id")
        self._connection.execute(
            "INSERT OR REPLACE INTO reports(report_id, case_id, device_id, payload_json, signature) VALUES (?, ?, ?, ?, ?)",
            (report_id, case_id, device_id, json.dumps(report, sort_keys=True), signature),
        )
        self._connection.commit()
        if case_id:
            self.record_audit_event(case_id, "system", "report.signed", {"report_id": report_id})
        return {"report": report, "signature": signature}

    def get_device(self, device_id: str) -> dict[str, Any] | None:
        row = self._connection.execute(
            "SELECT payload_json FROM devices WHERE device_id = ?", (device_id,)
        ).fetchone()
        return json.loads(row["payload_json"]) if row else None

    def get_case(self, case_id: str) -> dict[str, Any] | None:
        row = self._connection.execute(
            "SELECT payload_json FROM cases WHERE case_id = ?", (case_id,)
        ).fetchone()
        return json.loads(row["payload_json"]) if row else None

    def list_logs(self, device_id: str) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT payload_json FROM diagnostic_logs WHERE device_id = ? ORDER BY created_at, log_id",
            (device_id,),
        ).fetchall()
        return [json.loads(row["payload_json"]) for row in rows]

    def list_case_logs(self, case_id: str) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT payload_json FROM diagnostic_logs WHERE case_id = ? ORDER BY created_at, log_id",
            (case_id,),
        ).fetchall()
        return [json.loads(row["payload_json"]) for row in rows]

    def get_report(self, report_id: str) -> dict[str, Any] | None:
        row = self._connection.execute(
            "SELECT payload_json, signature FROM reports WHERE report_id = ?", (report_id,)
        ).fetchone()
        if not row:
            return None
        return {"report": json.loads(row["payload_json"]), "signature": row["signature"]}

    def record_audit_event(self, case_id: str | None, actor: str, action: str, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            "event_id": f"SYNTH-AUDIT-{uuid.uuid4().hex[:8].upper()}",
            "case_id": case_id,
            "actor": actor,
            "action": action,
            "payload": payload,
        }
        self._connection.execute(
            "INSERT INTO audit_events(event_id, case_id, actor, action, payload_json) VALUES (?, ?, ?, ?, ?)",
            (event["event_id"], case_id, actor, action, json.dumps(payload, sort_keys=True)),
        )
        self._connection.commit()
        return event

    def list_audit_events(self, case_id: str) -> list[dict[str, Any]]:
        rows = self._connection.execute(
            "SELECT event_id, case_id, actor, action, payload_json, created_at FROM audit_events WHERE case_id = ? ORDER BY created_at, event_id",
            (case_id,),
        ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "case_id": row["case_id"],
                "actor": row["actor"],
                "action": row["action"],
                "payload": json.loads(row["payload_json"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]
