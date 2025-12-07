import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.core.security import get_current_user_id
from app.models.trip import Trip, TripStatus

# Override auth dependency
async def mock_get_current_user_id():
    return "test_user_id"

app.dependency_overrides[get_current_user_id] = mock_get_current_user_id

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_trip_endpoint():
    # Mock the service method
    with patch('app.controllers.trip_controller.trip_service.create_trip_plan') as mock_create_plan:
        # Setup mock return value
        mock_create_plan.return_value = {
            "trip_id": "new_trip_123",
            "weather_summary": {"temp": 20},
            "flight_options": [],
            "poi_highlights": [],
            "currency_rate": "1 USD = 1 EUR"
        }

        payload = {
            "origin": "New York",
            "destination": "Paris",
            "start_date": "2023-06-01",
            "end_date": "2023-06-10",
            "budget": 5000.0,
            "transportation_preference": "FLIGHT"
        }

        response = client.post("/trips/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["trip_id"] == "new_trip_123"
        assert data["weather_summary"]["temp"] == 20

@pytest.mark.asyncio
async def test_get_trips_endpoint():
    with patch('app.controllers.trip_controller.trip_service.get_user_trips') as mock_get_trips:
        mock_get_trips.return_value = [
            Trip(
                id="trip_1",
                user_id="test_user_id",
                origin="NYC",
                destination="London",
                start_date="2023-01-01",
                end_date="2023-01-05",
                budget=2000.0,
                transportation_preference="FLIGHT",
                status=TripStatus.DRAFT
            )
        ]

        response = client.get("/trips/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["destination"] == "London"
