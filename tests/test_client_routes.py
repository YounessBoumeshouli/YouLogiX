from fastapi.testclient import TestClient
from tests.conftest import logistics_manager_token
from main import app

client = TestClient(app)




def test_get_single_client():
    # 1. Create a client with a VALID payload first
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "unique@user.com",
        "password": "password",
        "role": "client",
        "phone": "0000",
        "address": "Test City"
    }

    create_res = client.post("/auth/register", json=payload)
    assert create_res.status_code == 201

    # 2. Login

    login_payload = {
        "email": "unique@user.com",
        "password": "password"
    }    

    response = client.post(f"/auth/login", json=login_payload)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 3. Get user id

    client_id = create_res.json()["user_id"]

    # 4. Now fetch it
    response = client.get(f"/clients/{client_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.json()["id"] == client_id



def test_get_all_clients(logistics_manager_token):

    response = client.get(
        "/clients",
        headers={"Authorization": f"Bearer {logistics_manager_token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)