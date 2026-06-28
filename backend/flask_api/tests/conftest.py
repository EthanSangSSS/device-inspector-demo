import pytest

from app import create_app
from database import DiagnosticRepository
from rsa_signing import ReportSigner


@pytest.fixture()
def client():
    repo = DiagnosticRepository(":memory:")
    signer = ReportSigner()
    app = create_app(repository=repo, signer=signer)
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture()
def auth_header(client):
    response = client.post("/auth/token", json={"subject": "demo.engineer", "role": "engineer"})
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
