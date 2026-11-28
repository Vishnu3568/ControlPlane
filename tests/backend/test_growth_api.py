import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_daily_review_and_priorities():
    # 1. Fetch or create today's review
    res = client.get("/api/v1/growth/daily/today")
    assert res.status_code == 200
    review = res.json()
    review_id = review["id"]

    # 2. Update Top 3 priorities
    update_res = client.put(f"/api/v1/growth/daily/{review_id}", json={
        "priority_1": "Study Process Synchronization",
        "priority_1_done": True,
        "priority_2": "Complete Billing 2.0 invoice PDF endpoint",
        "priority_2_done": False,
        "priority_3": "Review 2 ML papers for Sentinel-NLP",
        "priority_3_done": False
    })
    assert update_res.status_code == 200
    assert update_res.json()["priority_1_done"] is True
    assert update_res.json()["priority_2"] == "Complete Billing 2.0 invoice PDF endpoint"

def test_habit_creation_and_toggle():
    # 1. Create a habit
    res = client.post("/api/v1/growth/habits", json={
        "name": "Solve 1 LeetCode Hard/Medium in Java",
        "category": "Coding",
        "target_days_per_week": 7
    })
    assert res.status_code == 201
    habit_id = res.json()["id"]

    # 2. Toggle today's habit completion
    toggle_res = client.post(f"/api/v1/growth/habits/{habit_id}/toggle")
    assert toggle_res.status_code == 200
    assert toggle_res.json()["is_completed"] is True

def test_weekly_retrospective_generator():
    res = client.get("/api/v1/growth/retrospective/weekly")
    assert res.status_code == 200
    retro = res.json()
    assert "total_study_minutes" in retro
    assert "tasks_completed_count" in retro
    assert "habits_consistency_pct" in retro

