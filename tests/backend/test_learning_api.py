import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_and_get_semester():
    res = client.post("/api/v1/learning/semesters", json={
        "name": "Semester 5 (Fall 2026)",
        "is_current": True
    })
    assert res.status_code == 201
    sem_id = res.json()["id"]

    get_res = client.get("/api/v1/learning/semesters")
    assert get_res.status_code == 200
    ids = [s["id"] for s in get_res.json()]
    assert sem_id in ids

def test_subject_lifecycle_and_study_session():
    # 1. Create Subject
    sub_res = client.post("/api/v1/learning/subjects", json={
        "name": "Operating Systems",
        "code": "IT501",
        "category": "Core Academic",
        "difficulty": "Hard",
        "priority": "P0"
    })
    assert sub_res.status_code == 201
    sub_id = sub_res.json()["id"]
    assert sub_res.json()["name"] == "Operating Systems"

    # 2. Add Topic
    top_res = client.post("/api/v1/learning/topics", json={
        "subject_id": sub_id,
        "title": "Process Synchronization & Semaphores",
        "status": "Learning"
    })
    assert top_res.status_code == 201
    top_id = top_res.json()["id"]

    # 3. Log a 45-minute focus study session
    sess_res = client.post("/api/v1/learning/sessions", json={
        "subject_id": sub_id,
        "topic_id": top_id,
        "duration_minutes": 45,
        "session_type": "Study",
        "notes": "Reviewed Peterson's algorithm and mutex locks."
    })
    assert sess_res.status_code == 201

    # 4. Verify subject total study minutes updated
    get_sub = client.get(f"/api/v1/learning/subjects/{sub_id}")
    assert get_sub.status_code == 200
    assert get_sub.json()["total_study_minutes"] == 45

    # 5. Add a Markdown Note
    note_res = client.post("/api/v1/learning/notes", json={
        "subject_id": sub_id,
        "topic_id": top_id,
        "title": "Critical Section Problem Requirements",
        "content_markdown": "1. Mutual Exclusion\n2. Progress\n3. Bounded Waiting"
    })
    assert note_res.status_code == 201
    assert "Mutual Exclusion" in note_res.json()["content_markdown"]

