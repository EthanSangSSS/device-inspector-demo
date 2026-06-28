"""Synthetic demo data.

No value in this file is a real IMEI, serial number, UDID, MAC address, or user record.
The identifiers are deliberately prefixed with SYNTH- to make public-safety review easy.
"""

SYNTHETIC_DEVICE = {
    "device_id": "SYNTH-DEVICE-001",
    "product_family": "mobile-device",
    "model_hint": "synthetic-phone-prototype",
    "firmware_version": "demo-1.0",
    "build_stage": "engineering-validation",
    "privacy_class": "synthetic",
}

SYNTHETIC_LOGS = [
    {
        "log_id": "SYNTH-LOG-001",
        "device_id": "SYNTH-DEVICE-001",
        "source": "thermal_sensor_mock",
        "severity": "warning",
        "message": "Thermal envelope exceeded expected range during camera stress loop.",
        "evidence_strength": "medium",
    },
    {
        "log_id": "SYNTH-LOG-002",
        "device_id": "SYNTH-DEVICE-001",
        "source": "audio_path_mock",
        "severity": "info",
        "message": "Intermittent microphone noise observed only after enclosure pressure event.",
        "evidence_strength": "low",
    },
]
