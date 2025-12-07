from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated, List, Dict, Any
from datetime import datetime, date
from enum import Enum

PyObjectId = Annotated[str, BeforeValidator(str)]

class TransportationPreference(str, Enum):
    FLIGHT = "FLIGHT"
    DRIVE = "DRIVE"
    BOTH = "BOTH"

class TripStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    COMPLETED = "COMPLETED"

class Trip(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    origin: str
    destination: str
    start_date: date
    end_date: date
    budget: float
    transportation_preference: TransportationPreference = TransportationPreference.BOTH
    trip_preferences: Optional[str] = None
    status: TripStatus = TripStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Embedded Data
    weather_summary: Optional[Dict[str, Any]] = None
    flight_options: Optional[List[Dict[str, Any]]] = None
    return_flight_options: Optional[List[Dict[str, Any]]] = None
    driving_options: Optional[Dict[str, Any]] = None
    poi_highlights: Optional[List[Dict[str, Any]]] = None
    currency_rate: Optional[str] = None
    itinerary: Optional[Dict[str, Any]] = None
    
    class Config:
        populate_by_name = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
