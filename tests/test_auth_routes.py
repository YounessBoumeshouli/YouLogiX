from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


##### Tests

def test_register_client():
    payload = {
        "first_name": "Amine",
        "last_name": "Logix",
        "email": "amine.test@example.com",
        "role": "client",
        "phone": "0612345678",
        "password": "securepassword",
        "address": "123 Rue Marrakech"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201


def test_register_delivery_man():
    payload = {
        "first_name": "Amine",
        "last_name": "Logix",
        "email": "amine.test@example.com",
        "role": "delivery_man",
        "phone": "0612345678",
        "password": "securepassword",
        "address": "123 Rue Marrakech",
        "vehicule": "CAR"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201


def test_login():
    payload = {
        "first_name": "Amine",
        "last_name": "Logix",
        "email": "amine.test@example.com",
        "password": "securepassword",
        "role": "delivery_man",
        "phone": "0612345678",
        "address": "123 Rue Marrakech",
        "vehicule": "CAR"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201

    login_payload = {
        "email": "amine.test@example.com",
        "password": "securepassword"
    }    

    response = client.post(f"/auth/login", json=login_payload)
    assert response.status_code == 200

    assert "access_token" in response.json()
