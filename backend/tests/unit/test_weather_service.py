import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.weather_service import WeatherService
import httpx

@pytest.mark.asyncio
async def test_get_forecast_success():
    with patch('app.services.weather_service.get_settings') as mock_get_settings, \
         patch('httpx.AsyncClient') as MockClient:
        
        # Mock settings
        mock_settings = MagicMock()
        mock_settings.OPENWEATHER_API_KEY = "fake_key"
        mock_get_settings.return_value = mock_settings

        # Mock HTTP client
        mock_client_instance = MockClient.return_value.__aenter__.return_value
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"list": [{"dt": 123, "main": {"temp": 20}}]}
        mock_client_instance.get = AsyncMock(return_value=mock_response)

        service = WeatherService()
        result = await service.get_forecast(40.7128, -74.0060)

        assert result["list"][0]["main"]["temp"] == 20
        mock_client_instance.get.assert_called_once()

@pytest.mark.asyncio
async def test_get_forecast_no_key():
    with patch('app.services.weather_service.get_settings') as mock_get_settings:
        mock_settings = MagicMock()
        mock_settings.OPENWEATHER_API_KEY = None
        mock_get_settings.return_value = mock_settings

        service = WeatherService()
        result = await service.get_forecast(40.7128, -74.0060)

        assert result["mock"] is True

@pytest.mark.asyncio
async def test_get_forecast_failure():
    with patch('app.services.weather_service.get_settings') as mock_get_settings, \
         patch('httpx.AsyncClient') as MockClient:
        
        mock_settings = MagicMock()
        mock_settings.OPENWEATHER_API_KEY = "fake_key"
        mock_get_settings.return_value = mock_settings

        mock_client_instance = MockClient.return_value.__aenter__.return_value
        mock_client_instance.get = AsyncMock(side_effect=httpx.HTTPError("API Error"))

        service = WeatherService()
        result = await service.get_forecast(40.7128, -74.0060)

        assert "error" in result
        assert "API Error" in result["error"]
