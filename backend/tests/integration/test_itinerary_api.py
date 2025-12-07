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
async def test_generate_itinerary_endpoint():
    # Mock TripRepository
    with patch('app.controllers.itinerary_controller.trip_repository.get_trip') as mock_get_trip:
        mock_get_trip.return_value = Trip(
            id="trip_123",
            user_id="test_user_id",
            origin="NYC",
            destination="Paris",
            start_date="2023-06-01",
            end_date="2023-06-05",
            budget=2000.0,
            transportation_preference="FLIGHT",
            status=TripStatus.DRAFT
        )

        # Mock OpenAIService
        with patch('app.controllers.itinerary_controller.openai_service.generate_itinerary') as mock_generate:
            mock_generate.return_value = {
                "days": [
                    {
                        "day": 1,
                        "activities": [
                            {"title": "Eiffel Tower", "location": "Paris"}
                        ]
                    }
                ]
            }

            # Mock TripRepository update (for saving itinerary)
            with patch('app.controllers.itinerary_controller.trip_repository.update_trip') as mock_update:
                mock_update.return_value = True

                response = client.post("/trips/trip_123/itinerary")
                
                assert response.status_code == 200
                data = response.json()
                assert "days" in data
                assert data["days"][0]["activities"][0]["title"] == "Eiffel Tower"

@pytest.mark.asyncio
async def test_generate_itinerary_not_found():
    with patch('app.controllers.itinerary_controller.trip_repository.get_trip') as mock_get_trip:
        mock_get_trip.return_value = None
        
        response = client.post("/trips/non_existent_trip/itinerary")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_generate_itinerary_forbidden():
    with patch('app.controllers.itinerary_controller.trip_repository.get_trip') as mock_get_trip:
        mock_get_trip.return_value = Trip(
            id="trip_123",
            user_id="other_user", # Different user
            origin="NYC",
            destination="Paris",
            start_date="2023-06-01",
            end_date="2023-06-05",
            budget=2000.0,
            transportation_preference="FLIGHT",
            status=TripStatus.DRAFT
        )
        
        response = client.post("/trips/trip_123/itinerary")
        assert response.status_code == 403
