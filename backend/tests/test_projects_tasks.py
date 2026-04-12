import pytest
from httpx import AsyncClient
import uuid

@pytest.fixture
async def auth_header(client: AsyncClient):
    # Register a user and get token
    email = f"test_{uuid.uuid4()}@example.com"
    register_data = {
        "name": "Project Test User",
        "email": email,
        "password": "password123"
    }
    response = await client.post("/auth/register", json=register_data)
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_project_crud(client: AsyncClient, auth_header: dict):
    # Create
    project_data = {"name": "Test Project", "description": "Test Description"}
    response = await client.post("/projects", json=project_data, headers=auth_header)
    assert response.status_code == 201
    project = response.json()
    assert project["name"] == project_data["name"]
    project_id = project["id"]

    # List
    response = await client.get("/projects", headers=auth_header)
    assert response.status_code == 200
    assert any(p["id"] == project_id for p in response.json()["projects"])

    # Get Detail
    response = await client.get(f"/projects/{project_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["id"] == project_id

    # Update
    update_data = {"name": "Updated Project"}
    response = await client.patch(f"/projects/{project_id}", json=update_data, headers=auth_header)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

    # Delete
    response = await client.delete(f"/projects/{project_id}", headers=auth_header)
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_task_crud(client: AsyncClient, auth_header: dict):
    # Create project first
    response = await client.post("/projects", json={"name": "Task Test Project"}, headers=auth_header)
    project_id = response.json()["id"]

    # Create Task
    task_data = {"title": "Test Task", "priority": "high", "status": "todo"}
    response = await client.post(f"/projects/{project_id}/tasks", json=task_data, headers=auth_header)
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == task_data["title"]
    task_id = task["id"]

    # List Tasks
    response = await client.get(f"/projects/{project_id}/tasks", headers=auth_header)
    assert response.status_code == 200
    assert any(t["id"] == task_id for t in response.json()["tasks"])

    # Update Task
    update_data = {"status": "in_progress"}
    response = await client.patch(f"/tasks/{task_id}", json=update_data, headers=auth_header)
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

    # Delete Task
    response = await client.delete(f"/tasks/{task_id}", headers=auth_header)
    assert response.status_code == 204
