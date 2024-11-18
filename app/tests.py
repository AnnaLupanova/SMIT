import pytest
from fastapi.testclient import TestClient
from main import app,get_db, SessionLocal, engine, Base
from unittest.mock import patch,  AsyncMock
from models import Rate
from datetime import date


client = TestClient(app)


@pytest.mark.asyncio
def test_upload_rates():
    test_data = {
        "2024-01-01": [
            {"cargo_type": "Glass", "rate": "0.5"},
            {"cargo_type": "Electronics", "rate": "1.2"}
        ],
        "2024-02-01": [
            {"cargo_type": "Furniture", "rate": "0.8"},
            {"cargo_type": "Glass", "rate": "0.55"}
        ]
    }

    response = client.post("/upload_rates/", json=test_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Rates successfully uploaded to the database."}


@pytest.fixture
def mock_rates():
    with patch('crud.get_current_rate', new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
def test_exist_calculate_insurance(mock_rates):
        mock_rates.return_value = Rate(cargo_type="Glass", rate=0.5, date=date(2024, 1, 1))
        response = client.get("/calculate_insurance/", params={
            "cargo_type": "Glass",
            "declared_value": 1000.0,
            "target_date": "2024-01-01"
        })
        assert response.status_code == 200
        assert response.json() == 500.0


@pytest.mark.asyncio
def test_not_exist_calculate_insurance(mock_rates):
        mock_rates.return_value = None

        response = client.get("/calculate_insurance/", params={
            "cargo_type": "NonExistentCargo",
            "declared_value": 1000.0,
            "target_date": "2024-01-01"
        })
        assert response.status_code == 404
        assert response.json() == {"detail": "Rate not found for cargo type and date"}