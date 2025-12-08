import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.trip_service import TripService
from app.models.api import CreateTripRequest
from app.models.trip import Trip, TripStatus

@pytest.mark.asyncio
async def test_create_trip_plan():
    # Mock dependencies
    with patch('app.services.trip_service.WeatherService') as MockWeatherService, \
         patch('app.services.trip_service.FlightService') as MockFlightService, \
         patch('app.services.trip_service.PlacesService') as MockPlacesService, \
         patch('app.services.trip_service.TripRepository') as MockTripRepo:

        # Setup mocks
        mock_weather_service = MockWeatherService.return_value
        mock_flight_service = MockFlightService.return_value
        mock_places_service = MockPlacesService.return_value
        mock_trip_repo = MockTripRepo.return_value

        # Configure async mocks
        mock_places_service.geocode = AsyncMock(return_value={'lat': 40.7128, 'lng': -74.0060})
        mock_places_service.get_country = AsyncMock(return_value="USA")
        mock_weather_service.get_forecast = AsyncMock(return_value={'summary': 'Sunny'})
        mock_flight_service.search_flights = AsyncMock(return_value=[{'flight': 'AA123'}])
        mock_places_service.search_nearby = AsyncMock(return_value=[{'name': 'Central Park'}])
        mock_trip_repo.create_trip = AsyncMock()
        
        mock_saved_trip = Trip(
            id="trip_123",
            user_id="user_123",
            origin="NYC",
            destination="London",
            start_date="2023-01-01",
            end_date="2023-01-05",
            budget=2000.0,
            transportation_preference="FLIGHT",
            status=TripStatus.DRAFT
        )
        mock_trip_repo.create_trip.return_value = mock_saved_trip

        # Initialize service
        service = TripService()
        
        # Execute
        request = CreateTripRequest(
            origin="NYC",
            destination="London",
            start_date="2023-01-01",
            end_date="2023-01-05",
            budget=2000.0,
            transportation_preference="FLIGHT"
        )
        response = await service.create_trip_plan("user_123", request)

        # Assert
        assert response.trip_id == "trip_123"
        assert response.weather_summary == {'summary': 'Sunny'}
        assert response.flight_options == [{'flight': 'AA123'}]
        assert response.poi_highlights == [{'name': 'Central Park'}]
        
        mock_places_service.geocode.assert_called()
        # Verify that get_forecast was called with the correct dates
        mock_weather_service.get_forecast.assert_called_with(
            40.7128, 
            -74.0060, 
            request.start_date, 
            request.end_date
        )
        mock_trip_repo.create_trip.assert_called()
