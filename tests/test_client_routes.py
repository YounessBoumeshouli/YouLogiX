import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app instance

client = TestClient(app)


def test_create_client():
    # 1. Prepare data
    payload = {
        "first_name": "Amine",
        "last_name": "Logix",
        "email": "amine@example.com",
        "phone": "0612345678"
    }

    # 2. Call the POST route
    response = client.post("/clients", json=payload)

    # 3. Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "amine@example.com"
    assert "id" in data


def test_get_all_clients():
    # Call the GET route
    response = client.get("/clients")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_client():
    # First, create a client to ensure one exists
    payload = {"first_name": "Test", "last_name": "User", "email": "test@user.com", "phone": "0000"}
    create_res = client.post("/clients", json=payload)
    client_id = create_res.json()["id"]

    # Now, test the GET /{id} route
    response = client.get(f"/clients/{client_id}")

    assert response.status_code == 200
    assert response.json()["id"] == client_id


def test_get_client_not_found():
    # Test a non-existent ID
    response = client.get("/clients/99999")
    assert response.status_code == 404