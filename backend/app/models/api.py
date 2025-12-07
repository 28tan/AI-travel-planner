from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import date
from app.models.trip import TransportationPreference

class CreateTripRequest(BaseModel):
    origin: str
    destination: str
    start_date: date
    end_date: date
    budget: float
    transportation_preference: TransportationPreference = TransportationPreference.BOTH
    trip_preferences: Optional[str] = None

class TripSummaryResponse(BaseModel):
    trip_id: Optional[str] = None
    weather_summary: Any
    flight_options: Optional[List[Any]] = None
    return_flight_options: Optional[List[Any]] = None
    driving_options: Optional[Any] = None
    poi_highlights: List[Any]
    currency_rate: str = "1 USD = 145 JPY" # Mock for now
