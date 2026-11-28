import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_project_crud_and_auto_import():
    # 1. Trigger auto-import of existing projects
    res = client.post("/api/v1/projects/auto-import")
    assert res.status_code == 200
    
    # 2. Get projects
    list_res = client.get("/api/v1/projects")
    assert list_res.status_code == 200
    projects = list_res.json()
    assert len(projects) >= 1
    slugs = [p["slug"] for p in projects]
    assert "billing-2-0" in slugs or "sentinel-nlp" in slugs or "venturebot" in slugs

    # 3. Pick first project and add task
    proj_id = projects[0]["id"]
    task_res = client.post("/api/v1/projects/tasks", json={
        "project_id": proj_id,
        "title": "Setup Docker compose configuration",
        "task_type": "Feature",
        "priority": "High",
        "status": "Todo",
        "estimated_hours": 2.0
    })
    assert task_res.status_code == 201
    task_id = task_res.json()["id"]

    # 4. Transition task to Done
    update_res = client.put(f"/api/v1/projects/tasks/{task_id}", json={
        "status": "Done"
    })
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "Done"
    assert update_res.json()["completed_at"] is not None

    # 5. Add Architecture Decision Record (ADR)
    adr_res = client.post("/api/v1/projects/adrs", json={
        "project_id": proj_id,
        "adr_number": 1,
        "title": "Use FastAPI over Express",
        "status": "Accepted",
        "context": "Need high performance async with automatic OpenAPI validation.",
        "decision": "Adopted FastAPI with Pydantic V2.",
        "consequences": "Faster development and native Python AI integration."
    })
    assert adr_res.status_code == 201
    assert adr_res.json()["adr_number"] == 1

