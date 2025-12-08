import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.services.weather_service import WeatherService
from datetime import date, datetime

@pytest.mark.asyncio
async def test_get_forecast_date_filtering():
    with patch('app.services.weather_service.get_settings') as mock_get_settings, \
         patch('httpx.AsyncClient') as MockClient:
        
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.OPENWEATHER_API_KEY = "fake_key"
        mock_get_settings.return_value = mock_settings

        # Mock HTTP client response
        mock_client_instance = MockClient.return_value.__aenter__.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        # Create mock data for 5 days
        # Dates: 2023-01-01 to 2023-01-05
        mock_data = {
            "list": [
                {
                    "dt": 1672531200,
                    "dt_txt": "2023-01-01 12:00:00",
                    "main": {"temp": 10},
                    "weather": [{"main": "Clear", "icon": "01d"}]
                },
                {
                    "dt": 1672617600,
                    "dt_txt": "2023-01-02 12:00:00",
                    "main": {"temp": 12},
                    "weather": [{"main": "Clouds", "icon": "02d"}]
                },
                {
                    "dt": 1672704000,
                    "dt_txt": "2023-01-03 12:00:00",
                    "main": {"temp": 15},
                    "weather": [{"main": "Rain", "icon": "10d"}]
                },
                {
                    "dt": 1672790400,
                    "dt_txt": "2023-01-04 12:00:00",
                    "main": {"temp": 11},
                    "weather": [{"main": "Snow", "icon": "13d"}]
                },
                {
                    "dt": 1672876800,
                    "dt_txt": "2023-01-05 12:00:00",
                    "main": {"temp": 9},
                    "weather": [{"main": "Clear", "icon": "01d"}]
                }
            ]
        }
        mock_response.json.return_value = mock_data
        mock_client_instance.get = AsyncMock(return_value=mock_response)

        service = WeatherService()
        
        # Test Case 1: Filter for middle 3 days (Jan 2 to Jan 4)
        start_date = date(2023, 1, 2)
        end_date = date(2023, 1, 4)
        
        result = await service.get_forecast(40.7128, -74.0060, start_date, end_date)
        
        assert "daily" in result
        daily = result["daily"]
        assert len(daily) == 3
        assert daily[0]["date"] == "2023-01-02"
        assert daily[1]["date"] == "2023-01-03"
        assert daily[2]["date"] == "2023-01-04"

        # Test Case 2: Filter for single day (Jan 1)
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 1)
        
        result = await service.get_forecast(40.7128, -74.0060, start_date, end_date)
        
        assert len(result["daily"]) == 1
        assert result["daily"][0]["date"] == "2023-01-01"

        # Test Case 3: No filter (should return all 5)
        result = await service.get_forecast(40.7128, -74.0060)
        assert len(result["daily"]) == 5
