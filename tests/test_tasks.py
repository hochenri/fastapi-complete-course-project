from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
app.state.limiter.enabled = False

def test_task_lifecycle():
    # 1. Setup: Create and Login
    username = "taskuser"
    password = "taskpassword"
    client.post("/auth/signup", json={
        "username": username,
        "email": "tasks@example.com",
        "hashed_password": password
    })
    
    login_res = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Task
    create_res = client.post(
        "/tasks/", 
        json={"title": "Finish API Tests", "description": "Ensure everything passes"},
        headers=headers
    )
    assert create_res.status_code == 201
    task_id = create_res.json()["id"]

    # 3. Get Tasks
    get_res = client.get("/tasks/", headers=headers)
    assert get_res.status_code == 200
    assert any(t["id"] == task_id for t in get_res.json())

    # 4. Update Task
    update_res = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Title", "completed": True},
        headers=headers
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated Title"

    # 5. Delete Task
    del_res = client.delete(f"/tasks/{task_id}", headers=headers)
    assert del_res.status_code == 204