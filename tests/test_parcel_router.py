import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app  # Ensure this points to your FastAPI entry point
from app.db.database import get_db

# 1. Setup Mock Database Dependency
mock_db = MagicMock()


def override_get_db():
    yield mock_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


## --- Tests for ParcelController Routes ---

@patch("controllers.parcel_controller.ParcelController.create_parcel")
def test_create_parcel(valid_client):
    # We use valid_client.id which was just created in the DB
    parcel_payload = {
        "description": "Laptop",
        "weight": 2.5,
        "idClient": valid_client.id,  # <--- THE KEY FIX
        "idRecipient": valid_client.id,  # Using same ID for test simplicity
        "DestinationCity": "Casablanca",
    }

    response = client.post("/parcels", json=parcel_payload)

    # Assertions
    assert response.status_code == 201
    assert response.json()["idClient"] == valid_client.id


@patch("controllers.parcel_controller.ParcelController.get_all_parcels")
def test_get_all_parcels(mock_get_all):
    mock_get_all.return_value = [{"id": 1, "description": "P1", "weight": 1.0, "status": "sent", "city": "Paris"}]

    response = client.get("/parcels")

    assert response.status_code == 200
    assert len(response.json()) == 1
    mock_get_all.assert_called_once()


@patch("controllers.parcel_controller.ParcelController.get_parcel")
def test_get_parcel_by_id(mock_get_one):
    mock_get_one.return_value = {"id": 99, "description": "Specific", "weight": 1.0, "status": "sent", "city": "Berlin"}

    response = client.get("/parcels/99")

    assert response.status_code == 200
    assert response.json()["id"] == 99
    mock_get_one.assert_called_once_with(99)


## --- Tests for ClientController Routes ---

@patch("controllers.client_controller.ClientController.getSentParcels")
def test_get_sent_parcels(mock_sent):
    mock_sent.return_value = [{"id": 10, "description": "Sent Item", "weight": 1.0, "status": "sent", "city": "Madrid"}]

    response = client.get("/parcels/sent/5")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 10
    mock_sent.assert_called_once_with(5)


@patch("controllers.parcel_controller.ParcelController.get_parcels_by_status")
def test_get_parcels_by_status(mock_status):
    mock_status.return_value = []

    response = client.get("/parcels/status/delivered")

    assert response.status_code == 200
    mock_status.assert_called_once_with("delivered")