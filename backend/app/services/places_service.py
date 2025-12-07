import httpx
from app.core.config import get_settings
from typing import Dict, Any, List, Optional

class PlacesService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://maps.googleapis.com/maps/api"

    async def geocode(self, address: str) -> Optional[Dict[str, float]]:
        if not self.settings.GOOGLE_MAPS_API_KEY:
            print("DEBUG: No Google Maps API Key provided.")
            return None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/geocode/json",
                    params={
                        "address": address,
                        "key": self.settings.GOOGLE_MAPS_API_KEY
                    }
                )
                response.raise_for_status()
                data = response.json()
                if data["status"] == "OK" and data["results"]:
                    return data["results"][0]["geometry"]["location"]
                return None
            except httpx.HTTPError as e:
                print(f"Geocoding Error: {e}")
                return None

    async def get_country(self, address: str) -> Optional[str]:
        if not self.settings.GOOGLE_MAPS_API_KEY:
            print("DEBUG: No Google Maps API Key provided.")
            return None

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/geocode/json",
                    params={
                        "address": address,
                        "key": self.settings.GOOGLE_MAPS_API_KEY
                    }
                )
                response.raise_for_status()
                data = response.json()
                if data["status"] == "OK" and data["results"]:
                    # Extract country from address components
                    for component in data["results"][0]["address_components"]:
                        if "country" in component["types"]:
                            return component["long_name"]
                return None
            except httpx.HTTPError as e:
                print(f"Geocoding Error: {e}")
                return None

    async def get_place_photo(self, query: str) -> Optional[str]:
        """
        Searches for a place by text query and returns a photo URL if available.
        """
        if not self.settings.GOOGLE_MAPS_API_KEY:
            print("DEBUG: No Google Maps API Key provided.")
            return None

        async with httpx.AsyncClient() as client:
            try:
                # 1. Find Place ID
                find_url = f"{self.base_url}/place/findplacefromtext/json"
                response = await client.get(find_url, params={
                    "input": query,
                    "inputtype": "textquery",
                    "fields": "photos,place_id",
                    "key": self.settings.GOOGLE_MAPS_API_KEY
                })
                data = response.json()
                
                if data.get("status") == "OK" and data.get("candidates"):
                    candidate = data["candidates"][0]
                    if "photos" in candidate and candidate["photos"]:
                        photo_ref = candidate["photos"][0]["photo_reference"]
                        return f"{self.base_url}/place/photo?maxwidth=400&photo_reference={photo_ref}&key={self.settings.GOOGLE_MAPS_API_KEY}"
                
                return None
            except Exception as e:
                print(f"Error fetching photo for {query}: {e}")
                return None

    async def search_nearby(self, lat: float, lng: float, preferences: str = "") -> List[Dict[str, Any]]:
        if not self.settings.GOOGLE_MAPS_API_KEY:
            print("DEBUG: No Google Maps API Key provided.")
            return []

        # Determine keywords/types to search
        # Exclude lodging by default unless requested
        search_queries = ["tourist_attraction", "restaurant", "museum", "park", "point_of_interest"]
        
        # Simple preference matching to add more specific searches
        if preferences:
            pref_lower = preferences.lower()
            if "hotel" in pref_lower or "stay" in pref_lower:
                search_queries.append("lodging")
            if "museum" in pref_lower or "history" in pref_lower:
                search_queries.append("museum")
            if "park" in pref_lower or "nature" in pref_lower:
                search_queries.append("park")
            if "shopping" in pref_lower:
                search_queries.append("shopping_mall")
            if "food" in pref_lower or "eat" in pref_lower:
                search_queries.append("restaurant")
                search_queries.append("cafe")

        all_results = []
        seen_place_ids = set()

        async with httpx.AsyncClient() as client:
            import asyncio
            tasks = []
            for query in set(search_queries): # Use set to avoid duplicates
                tasks.append(self._fetch_places(client, lat, lng, query))
            
            results_list = await asyncio.gather(*tasks)
            
            for results in results_list:
                for place in results:
                    if place["place_id"] not in seen_place_ids:
                        # Add photo URL if available
                        if "photos" in place and place["photos"]:
                            photo_ref = place["photos"][0]["photo_reference"]
                            place["photo_url"] = f"{self.base_url}/place/photo?maxwidth=400&photo_reference={photo_ref}&key={self.settings.GOOGLE_MAPS_API_KEY}"
                        else:
                            place["photo_url"] = None
                        
                        all_results.append(place)
                        seen_place_ids.add(place["place_id"])

        return all_results

    async def _fetch_places(self, client: httpx.AsyncClient, lat: float, lng: float, keyword: str) -> List[Dict[str, Any]]:
        try:
            response = await client.get(
                f"{self.base_url}/place/nearbysearch/json",
                params={
                    "location": f"{lat},{lng}",
                    "radius": 5000, # 5km
                    "keyword": keyword,
                    "key": self.settings.GOOGLE_MAPS_API_KEY
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except httpx.HTTPError as e:
            print(f"Places Search Error for {keyword}: {e}")
            return []
