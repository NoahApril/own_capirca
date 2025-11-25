"""Tests for Capirca Phase 2 API endpoints."""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from capirca.api.main import app
from capirca.db.base import Base, get_db


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    """Provide a TestClient with an isolated in-memory database."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, future=True
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)


def test_policy_crud_and_validation(test_client: TestClient):
    policy_payload = {
        "name": "test-policy",
        "description": "Phase 2 policy",
        "content": """
header {
  target:: juniper TEST-FILTER
}

term allow-any {
  source-address:: any
  destination-address:: any
  protocol:: tcp
  action:: accept
}
""".strip(),
    }

    response = test_client.post("/api/policies", json=policy_payload)
    assert response.status_code == 201
    policy_id = response.json()["id"]

    response = test_client.get(f"/api/policies/{policy_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "test-policy"

    response = test_client.post(f"/api/policies/{policy_id}/validate")
    assert response.status_code == 200
    validation = response.json()
    assert "errors" in validation

    warnings = [err for err in validation["errors"] if err["severity"] == "warning"]
    assert warnings, "Expected at least one warning for any->any rule"


def test_network_and_service_objects(test_client: TestClient):
    network_payload = {
        "name": "INTERNAL_NETS",
        "addresses": ["10.0.0.0/8", "192.168.0.0/16"],
        "description": "Internal networks",
    }
    response = test_client.post("/api/network-objects", json=network_payload)
    assert response.status_code == 201
    network_id = response.json()["id"]

    service_payload = {
        "name": "WEB_SERVICES",
        "ports": ["80", "443"],
        "protocols": ["tcp"],
        "description": "Web ports",
    }
    response = test_client.post("/api/service-objects", json=service_payload)
    assert response.status_code == 201
    service_id = response.json()["id"]

    response = test_client.get(f"/api/network-objects/{network_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["addresses"] == network_payload["addresses"]

    response = test_client.get(f"/api/service-objects/{service_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ports"] == service_payload["ports"]
    assert data["protocols"] == service_payload["protocols"]


def test_create_deployment_record(test_client: TestClient):
    policy_payload = {
        "name": "deploy-policy",
        "description": "Deployment test",
        "content": """
header {
  target:: juniper TEST-FILTER
}
term default-deny {
  action:: deny
}
""".strip(),
    }
    response = test_client.post("/api/policies", json=policy_payload)
    assert response.status_code == 201
    policy_id = response.json()["id"]

    deployment_payload = {
        "policy_id": policy_id,
        "platform": "juniper",
        "target": "TEST-FILTER",
        "status": "pending",
    }
    response = test_client.post("/api/deployments", json=deployment_payload)
    assert response.status_code == 201
    deployment = response.json()
    assert deployment["policy_id"] == policy_id
    assert deployment["platform"] == "juniper"
