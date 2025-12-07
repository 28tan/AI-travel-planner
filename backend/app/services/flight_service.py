import httpx
from app.core.config import get_settings
from typing import Dict, Any, List

class FlightService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "http://api.aviationstack.com/v1"

    def get_iata_code(self, city_name: str) -> str:
        # Simple mock mapping for demo purposes
        mapping = {
            "New York": "JFK", "London": "LHR", "Tokyo": "HND", "Paris": "CDG",
            "Los Angeles": "LAX", "San Francisco": "SFO", "Chicago": "ORD",
            "Dubai": "DXB", "Singapore": "SIN", "Sydney": "SYD", "Toronto": "YYZ",
            "Vancouver": "YVR", "Berlin": "BER", "Rome": "FCO", "Madrid": "MAD",
            "Barcelona": "BCN", "Amsterdam": "AMS", "Hong Kong": "HKG",
            "Seoul": "ICN", "Bangkok": "BKK", "Miami": "MIA", "Orlando": "MCO",
            "Atlanta": "ATL", "Dallas": "DFW", "Denver": "DEN", "Seattle": "SEA",
            "Boston": "BOS", "Las Vegas": "LAS", "Phoenix": "PHX", "Houston": "IAH",
            "Pittsburgh": "PIT", "Pittburgh": "PIT", "Philadelphia": "PHL", "Detroit": "DTW",
            "Ohio": "CMH", "Ophoi": "CMH", "Columbus": "CMH", "Cleveland": "CLE", "Cincinnati": "CVG",
            "Washington": "IAD", "Baltimore": "BWI", "Charlotte": "CLT",
            # Countries / Major Destinations
            "Japan": "HND", "UK": "LHR", "United Kingdom": "LHR", "France": "CDG",
            "Germany": "FRA", "Italy": "FCO", "Spain": "MAD", "China": "PEK",
            "India": "DEL", "Australia": "SYD", "Canada": "YYZ", "Brazil": "GRU",
            "Mexico": "MEX"
        }
        # Normalize
        key = city_name.strip()
        for k, v in mapping.items():
            if k.lower() in key.lower():
                return v
        
        # Fallback: If it looks like an IATA code (3 uppercase letters), return it
        if len(key) == 3 and key.isalpha():
            return key.upper()
            
        return "JFK" # Default fallback

    async def search_flights(self, origin_iata: str, destination_iata: str) -> List[Dict[str, Any]]:
        """
        Search for active flights between two airports.
        Note: Free tier of Aviationstack might be limited to active flights, not future schedules.
        """
        # Mock data for fallback
        mock_flights = [
            {
                "flight_date": "2025-12-20",
                "flight_status": "scheduled",
                "departure": {"airport": origin_iata, "iata": origin_iata, "scheduled": "2025-12-20T10:00:00+00:00"},
                "arrival": {"airport": destination_iata, "iata": destination_iata, "scheduled": "2025-12-20T22:00:00+00:00"},
                "airline": {"name": "Mock Airlines", "iata": "MA"},
                "flight": {"number": "MA123", "iata": "MA123"},
                "price": 450.00,
                "currency": "USD",
                "booking_link": "https://www.example.com/book/MA123"
            },
            {
                "flight_date": "2025-12-20",
                "flight_status": "scheduled",
                "departure": {"airport": origin_iata, "iata": origin_iata, "scheduled": "2025-12-20T14:00:00+00:00"},
                "arrival": {"airport": destination_iata, "iata": destination_iata, "scheduled": "2025-12-21T02:00:00+00:00"},
                "airline": {"name": "Test Airways", "iata": "TA"},
                "flight": {"number": "TA456", "iata": "TA456"},
                "price": 520.50,
                "currency": "USD",
                "booking_link": "https://www.example.com/book/TA456"
            }
        ]

        if not self.settings.AVIATIONSTACK_API_KEY:
            print("DEBUG: No Aviationstack API Key provided. Using mock data.")
            return mock_flights

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/flights",
                    params={
                        "access_key": self.settings.AVIATIONSTACK_API_KEY,
                        "dep_iata": origin_iata,
                        "arr_iata": destination_iata,
                        "limit": 10
                    }
                )
                response.raise_for_status()
                data = response.json()
                flights = data.get("data", [])
                if not flights:
                    # Optional: return mock if no flights found? 
                    # User said "limit reached", so maybe only on error.
                    # But sometimes free tier returns empty for future dates.
                    # Let's stick to returning empty if successful but empty.
                    return []
                return flights
            except httpx.HTTPError as e:
                print(f"Flight API Error: {e}. Using mock data.")
                return mock_flights
            except Exception as e:
                print(f"Flight API Unexpected Error: {e}. Using mock data.")
                return mock_flights
