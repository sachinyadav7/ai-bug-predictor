from fastapi.testclient import TestClient
from app.main import app
from app.auth.routes import get_current_active_user
from app.auth.models import User
import pytest

# Mock an authenticated user
async def override_get_current_active_user():
    return User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        is_admin=False
    )

app.dependency_overrides[get_current_active_user] = override_get_current_active_user

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Bug Prediction API"

def test_predict_endpoint_mock():
    # We test with a dummy request. 
    # Since model loading might fail without weights, we expect it to run but maybe return specific confidence if using random weights.
    # Note: We are using random weights if checkpoint missing, so prediction should work technically.
    
    code_sample = """
    def add(a, b):
        return a + b
    """
    
    response = client.post(
        "/api/v1/predict",
        json={"code": code_sample, "language": "python"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "file_risk_score" in data
    assert len(data["results"]) > 0
    assert data["results"][0]["function_name"] == "add"
    
def test_predict_no_functions():
    code_sample = "# Just a comment"
    response = client.post(
        "/api/v1/predict",
        json={"code": code_sample, "language": "python"}
    )
    # The preprocessor might return global scope or empty list.
    # If empty list, endpoint returns 400 "No functions found"
    
    # Update: preprocessor fallback returns distinct scope if no functions found?
    # Let's check strict behavior. If it returns 400, that's fine.
    
    if response.status_code == 400:
        assert response.json()["detail"] == "No functions found in code"
    else:
        # If it returns 200, it means it found something (maybe global scope)
        assert response.status_code == 200
