import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_business_opportunity_and_experiment_lifecycle():
    # 1. Create Business Opportunity
    opp_res = client.post("/api/v1/business/opportunities", json={
        "title": "B2B Travel ERP Cloud Sync",
        "problem_statement": "Travel agents spend 20+ hours manually reconciling GDS tickets and invoicing.",
        "target_customer": "Mid-tier travel agencies with 5-20 agents",
        "revenue_model": "Monthly SaaS ($99/mo)",
        "stage": "Validation",
        "estimated_tam": "$120M in regional travel agencies"
    })
    assert opp_res.status_code == 201
    opp = opp_res.json()
    opp_id = opp["id"]
    assert opp["title"] == "B2B Travel ERP Cloud Sync"
    assert opp["stage"] == "Validation"

    # 2. Add an Experiment
    exp_res = client.post("/api/v1/business/experiments", json={
        "opportunity_id": opp_id,
        "hypothesis": "At least 3 of 10 travel agents contacted will agree to a 15-min workflow demo.",
        "validation_method": "Cold Outreach & Phone Interviews",
        "budget_allocated": 50.0,
        "budget_spent": 15.0,
        "success_criteria": "3 demo commitments within 7 days",
        "decision": "In Progress"
    })
    assert exp_res.status_code == 201
    exp_id = exp_res.json()["id"]

    # 3. Update Experiment Outcome & Decision
    update_res = client.put(f"/api/v1/business/experiments/{exp_id}", json={
        "actual_outcome": "4 agencies booked demos, 2 requested trial pricing.",
        "decision": "Validated"
    })
    assert update_res.status_code == 200
    assert update_res.json()["decision"] == "Validated"

    # 4. Advance Opportunity Stage
    opp_update = client.put(f"/api/v1/business/opportunities/{opp_id}", json={
        "stage": "Prototype"
    })
    assert opp_update.status_code == 200
    assert opp_update.json()["stage"] == "Prototype"

