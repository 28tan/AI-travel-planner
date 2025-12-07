from pydantic import BaseModel, Field, BeforeValidator
from typing import List, Optional, Annotated
from datetime import date, datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class ItineraryDay(BaseModel):
    day_number: int
    date: date
    morning: str
    afternoon: str
    evening: str
    weather_summary: Optional[str] = None

class Itinerary(BaseModel):
    trip_id: PyObjectId
    days: List[ItineraryDay]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat()
        }
