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

from schemas.parcel_schema import ParcelCreateSchema , ParcelResponseSchema


@patch("controllers.parcel_controller.ParcelController.create_parcel")
def test_create_parcel(mock_create, valid_client):

    payload_data = {
        "description": "Laptop",
        "weight": 2.5,
        "status": "CREATED",
        "idClient": valid_client.id,
        "idRecipient": valid_client.id,
        "DestinationCity": "Casablanca"
    }

    ParcelCreateSchema(**payload_data)

    mock_create.return_value = {
        "id": 1,
        "description": "Laptop",
        "weight": 2.5,
        "status": "CREATED",
        "idDeliveryMan": None,
        "idClient": valid_client.id,
        "idRecipient": valid_client.id,
        "DestinationCity": "Casablanca",
        "code": "XYZ-123"
    }

    response = client.post("/parcels", json=payload_data)

    if response.status_code == 422:
        print(f"Validation Error: {response.json()}")

    assert response.status_code == 201
    assert response.json()["description"] == "Laptop"


@patch("controllers.parcel_controller.ParcelController.get_all_parcels")
def test_get_all_parcels(mock_get_all):
    # Create raw data
    raw_data = {
        "id": 1,
        "description": "P1",
        "weight": 1.0,
        "status": "SENT",
        "idDeliveryMan": None,
        "idClient": 10,
        "idRecipient": 20,
        "DestinationCity": "Paris",
        "code": "ABC-123"
    }

    # USE THE SCHEMA: This validates that your mock matches the real structure
    # .model_dump() converts the Pydantic object back to a dict for the mock
    mock_get_all.return_value = [ParcelResponseSchema(**raw_data).model_dump()]

    response = client.get("/parcels")

    assert response.status_code == 200
    assert len(response.json()) == 1
    # Verify the API returned data that matches our Schema
    assert response.json()[0]["code"] == raw_data["code"]

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