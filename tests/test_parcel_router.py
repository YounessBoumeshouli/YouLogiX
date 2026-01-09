import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app  # Ensure this points to your FastAPI entry point
from app.db.database import get_db
from auth.dependencies import get_current_user
# 1. Setup Mock Database Dependency
mock_db = MagicMock()


def override_get_db():
    yield mock_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


## --- Tests for ParcelController Routes ---

from schemas.parcel_schema import ParcelCreateSchema , ParcelResponseSchema

def skip_auth():
    return {"id": 1, "username": "testuser"}
@patch("controllers.parcel_controller.ParcelController.create_parcel")
def test_create_parcel(mock_create, valid_client):
    app.dependency_overrides[get_current_user] = lambda: valid_client

    payload_data = {
        "description": "Laptop",
        "weight": 2.5,
        "status": "CREATED",
        "idClient": valid_client.id,
        "idRecipient": valid_client.id,
        "DestinationCity": "Casablanca"
    }

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

    app.dependency_overrides = {}

    assert response.status_code == 201
@patch("controllers.parcel_controller.ParcelController.get_all_parcels")
def test_get_all_parcels(mock_get_all,valid_logistic_manager,valid_client):
    # Create raw data
    app.dependency_overrides[get_current_user] = lambda: valid_logistic_manager

    raw_data = {
        "id": 1,
        "description": "P1",
        "weight": 1.0,
        "status": "SENT",
        "idDeliveryMan": None,
        "idClient": valid_client.id,
        "idRecipient": valid_client.id,
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
def test_get_parcel_by_id(mock_get_one,valid_logistic_manager,valid_client):
    app.dependency_overrides[get_current_user] = lambda: valid_logistic_manager

    raw_data = {
        "id": 19,
        "description": "P1",
        "weight": 1.0,
        "status": "SENT",
        "idDeliveryMan": None,
        "idClient": valid_client.id,
        "idRecipient": valid_client.id,
        "DestinationCity": "Paris",
        "code": "ABC-123"
    }
    mock_get_one.return_value = ParcelResponseSchema(**raw_data).model_dump()

    response = client.get("/parcels/99")

    assert response.status_code == 200
    assert response.json()["id"] == 19
    mock_get_one.assert_called_once_with(99)



@patch("controllers.client_controller.ClientController.getSentParcels")
def test_get_sent_parcels(mock_sent,valid_client):
    app.dependency_overrides[get_current_user] = lambda: valid_client

    raw_data = {
        "id": 1,
        "description": "P1",
        "weight": 1.0,
        "status": "DELIVERED",
        "idDeliveryMan": None,
        "idClient": valid_client.id,
        "idRecipient": 20,
        "DestinationCity": "Paris",
        "code": "ABC-123"
    }


    mock_sent.return_value = [ParcelResponseSchema(**raw_data).model_dump()]
    response = client.get("/parcels/sent")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    mock_sent.assert_called_once_with(valid_client.id)


@patch("controllers.parcel_controller.ParcelController.get_parcels_by_status")
def test_get_parcels_by_status(mock_status,valid_logistic_manager):
    app.dependency_overrides[get_current_user] = lambda: valid_logistic_manager

    mock_status.return_value = []

    response = client.get("/parcels/status/delivered")

    assert response.status_code == 200
    mock_status.assert_called_once_with("delivered")