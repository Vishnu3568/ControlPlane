import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "ControlPlane" in data["message"]
    assert data["docs"] == "/docs"

def test_system_health():
    response = client.get("/api/v1/system/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["database_connected"] is True
    assert data["app_name"] == "ControlPlane"
    assert data["version"] == "1.0.0"

def test_settings_crud():
    # Write a setting
    payload = {
        "key": "test_key",
        "value": "active_test_value",
        "description": "Integration test key"
    }
    post_res = client.post("/api/v1/system/settings", json=payload)
    assert post_res.status_code == 200
    assert post_res.json()["key"] == "test_key"
    assert post_res.json()["value"] == "active_test_value"

    # Read settings
    get_res = client.get("/api/v1/system/settings")
    assert get_res.status_code == 200
    keys = [item["key"] for item in get_res.json()]
    assert "test_key" in keys

