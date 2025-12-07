import httpx
from app.core.config import get_settings
from typing import Dict, Any, Optional

class RouteService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://maps.googleapis.com/maps/api"

    async def get_driving_estimate(self, origin: str, destination: str) -> Optional[Dict[str, Any]]:
        if not self.settings.GOOGLE_MAPS_API_KEY:
            # Mock data for testing
            return {
                "distance_km": 350.5,
                "duration_min": 255,
                "possible": True,
                "origin": origin,
                "destination": destination
            }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/directions/json",
                    params={
                        "origin": origin,
                        "destination": destination,
                        "mode": "driving",
                        "key": self.settings.GOOGLE_MAPS_API_KEY
                    }
                )
                data = response.json()
                
                if data["status"] == "OK" and data["routes"]:
                    leg = data["routes"][0]["legs"][0]
                    return {
                        "distance_km": round(leg["distance"]["value"] / 1000, 1),
                        "duration_min": round(leg["duration"]["value"] / 60),
                        "possible": True,
                        "origin": origin,
                        "destination": destination
                    }
                elif data["status"] == "ZERO_RESULTS":
                     return {
                        "possible": False,
                        "reason": "No driving route found."
                    }
                
                return None
            except Exception as e:
                print(f"Route API Error: {e}")
                return None
