from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_client():
    payload = {
        "first_name": "Amine",
        "last_name": "Logix",
        "email": "amine.test@example.com",
        "phone": "0612345678",
        "password": "securepassword",
        "address": "123 Rue Marrakech"  # Ensure this matches your Schema!
    }
    response = client.post("/clients", json=payload)
    # If it still fails, print response.json() to see the exact field missing
    assert response.status_code == 201


def test_get_single_client():
    # 1. Create a client with a VALID payload first
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "unique@user.com",
        "phone": "0000",
        "password": "password",
        "address": "Test City"
    }
    create_res = client.post("/clients", json=payload)
    assert create_res.status_code == 201

    client_id = create_res.json()["id"]

    # 2. Now fetch it
    response = client.get(f"/clients/{client_id}")
    assert response.status_code == 200
    assert response.json()["id"] == client_id