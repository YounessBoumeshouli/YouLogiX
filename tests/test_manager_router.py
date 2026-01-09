import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from auth.dependencies import get_current_user
from main import app  # Import your FastAPI app instance
from app.db.database import get_db

# Mock database session
mock_db = MagicMock()


# Override the get_db dependency to return our mock session
def override_get_db():
    yield mock_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@patch("controllers.delivery_man_controller.DeliveryManController.seed_delivery_men")
def test_seed_delivery_men(mock_seed):
    """Tests the GET /delivery_man route"""
    response = client.get("/delivery_man")

    assert response.status_code == 200
    assert response.json() == {"message": "This route is running"}
    mock_seed.assert_called_once()


@patch("controllers.delivery_man_controller.DeliveryManController.fetch_percels")
def test_show_parcels(mock_fetch):
    """Tests the GET /delivery_man/parcels route"""
    # Setup mock return value
    mock_fetch.return_value = [{"id": 1, "name": "Parcel A"}, {"id": 2, "name": "Parcel B"}]

    response = client.get("/delivery_man/parcels")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Parcel A"
    mock_fetch.assert_called_once()


@patch("controllers.logistic_manager_controller.LogisticMangerController.assignParcel")
def test_assign_parcel_to_delivery_man(mock_assign,valid_logistic_manager):
    app.dependency_overrides[get_current_user] = lambda: valid_logistic_manager

    """Tests the GET /parcels/{parcel_id}/assign_to_delivery_man route"""
    parcel_id = "123"
    mock_assign.return_value = {"status": "success", "parcel_id": parcel_id}

    response = client.get(f"/parcels/{parcel_id}/assign_to_delivery_man")

    assert response.status_code == 200
    assert response.json()["parcel_id"] == parcel_id
    mock_assign.assert_called_once_with(parcel_id)