"""RSA signing utilities for tamper-evident diagnostic reports."""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


@dataclass
class SigningKeyPair:
    private_key: RSAPrivateKey
    public_key: RSAPublicKey


class ReportSigner:
    """Generate and verify RSA signatures for canonical JSON payloads."""

    def __init__(self, key_pair: SigningKeyPair | None = None) -> None:
        self.key_pair = key_pair or generate_demo_key_pair()

    def sign(self, payload: dict[str, Any]) -> str:
        canonical = canonical_json(payload)
        signature = self.key_pair.private_key.sign(
            canonical.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return base64.b64encode(signature).decode("ascii")

    def verify(self, payload: dict[str, Any], signature: str) -> bool:
        canonical = canonical_json(payload)
        try:
            self.key_pair.public_key.verify(
                base64.b64decode(signature.encode("ascii")),
                canonical.encode("utf-8"),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False

    def public_key_pem(self) -> str:
        return self.key_pair.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def generate_demo_key_pair() -> SigningKeyPair:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return SigningKeyPair(private_key=private_key, public_key=private_key.public_key())
