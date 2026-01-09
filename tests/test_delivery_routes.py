from fastapi.testclient import TestClient
from tests.conftest import logistics_manager_token
from main import app

client = TestClient(app)



def test_get_all_delivery_men(logistics_manager_token):

    response = client.get(
        "/delivery_men",
        headers={"Authorization": f"Bearer {logistics_manager_token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)