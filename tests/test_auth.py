from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Disable rate limiting so tests don't fail on repeated runs
app.state.limiter.enabled = False

def test_signup():
    # We use a unique username to avoid "Username already exists" 400 errors
    response = client.post("/auth/signup", json={
        "username": "newuser_auth",
        "email": "auth@example.com",
        "hashed_password": "testpassword123" 
    })
    assert response.status_code == 201
    assert "user_id" in response.json()

def test_login():
    # 1. Ensure user exists
    client.post("/auth/signup", json={
        "username": "loginuser",
        "email": "login@example.com",
        "hashed_password": "testpassword123"
    })

    # 2. Login using FORM DATA (required by OAuth2PasswordRequestForm)
    response = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "testpassword123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"