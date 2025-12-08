import httpx
from app.core.config import get_settings
from app.core.resilience import CircuitBreaker
from typing import Dict, Any, Optional
from datetime import date, datetime

class WeatherService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def get_forecast(self, lat: float, lon: float, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[str, Any]:
        try:
            return await self._get_forecast_impl(lat, lon, start_date, end_date)
        except Exception as e:
            print(f"Weather API Error (Circuit Breaker): {e}")
            return {"error": str(e)}

    @CircuitBreaker(failure_threshold=3, recovery_timeout=60)
    async def _get_forecast_impl(self, lat: float, lon: float, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Fetch 5 day / 3 hour forecast data from OpenWeatherMap and aggregate to daily.
        """
        if not self.settings.OPENWEATHER_API_KEY:
            print("DEBUG: No OpenWeather API Key provided.")
            return {}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.settings.OPENWEATHER_API_KEY,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            data = response.json()
            result = self._process_forecast(data)
            
            # Filter by date range if provided
            if start_date and end_date and "daily" in result:
                filtered_daily = []
                for day in result["daily"]:
                    day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
                    if start_date <= day_date <= end_date:
                        filtered_daily.append(day)
                result["daily"] = filtered_daily
                
            return result

    def _process_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        daily_summary = {}
        
        for item in data.get("list", []):
            dt_txt = item.get("dt_txt", "")
            date_str = dt_txt.split(" ")[0] # YYYY-MM-DD
            
            # Parse time to 12h format
            hour_str = dt_txt.split(" ")[1][:2]
            hour = int(hour_str)
            period = "AM" if hour < 12 else "PM"
            if hour == 0:
                hour_12 = 12
            elif hour > 12:
                hour_12 = hour - 12
            else:
                hour_12 = hour
            time_str = f"{hour_12} {period}"
            
            if date_str not in daily_summary:
                daily_summary[date_str] = {
                    "temps": [],
                    "conditions": [],
                    "icons": [],
                    "hourly": []
                }
            
            daily_summary[date_str]["temps"].append(item["main"]["temp"])
            daily_summary[date_str]["conditions"].append(item["weather"][0]["main"])
            daily_summary[date_str]["icons"].append(item["weather"][0]["icon"])
            
            daily_summary[date_str]["hourly"].append({
                "time": time_str,
                "temp": round(item["main"]["temp"]),
                "condition": item["weather"][0]["main"],
                "icon": self._get_weather_emoji(item["weather"][0]["icon"])
            })

        # Create final list
        daily_list = []
        from collections import Counter
        
        for date_str, info in daily_summary.items():
            temps = info["temps"]
            # Most common condition and icon
            condition = Counter(info["conditions"]).most_common(1)[0][0]
            icon_code = Counter(info["icons"]).most_common(1)[0][0]
            
            # Map icon code to emoji
            icon_emoji = self._get_weather_emoji(icon_code)

            daily_list.append({
                "date": date_str,
                "temp_min": round(min(temps)),
                "temp_max": round(max(temps)),
                "condition": condition,
                "icon": icon_emoji,
                "hourly": info["hourly"]
            })
            
        return {"daily": daily_list}

    def _get_weather_emoji(self, icon_code: str) -> str:
        # Simple mapping
        if "01" in icon_code: return "☀️" # clear
        if "02" in icon_code: return "⛅" # few clouds
        if "03" in icon_code or "04" in icon_code: return "☁️" # clouds
        if "09" in icon_code or "10" in icon_code: return "🌧️" # rain
        if "11" in icon_code: return "⛈️" # thunder
        if "13" in icon_code: return "❄️" # snow
        if "50" in icon_code: return "🌫️" # mist
        return "🌤️"

    def _get_mock_weather(self) -> Dict[str, Any]:
        return {
            "daily": [
                {"date": "2023-01-01", "temp_min": 10, "temp_max": 15, "condition": "Cloudy", "icon": "☁️"},
                {"date": "2023-01-02", "temp_min": 12, "temp_max": 18, "condition": "Sunny", "icon": "☀️"},
                {"date": "2023-01-03", "temp_min": 8, "temp_max": 12, "condition": "Rain", "icon": "🌧️"},
            ]
        }
