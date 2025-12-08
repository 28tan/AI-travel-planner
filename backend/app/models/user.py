from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str = Field(alias="_id")
    preferences: Optional[str] = None
    home_airport: Optional[str] = None
    default_budget: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
