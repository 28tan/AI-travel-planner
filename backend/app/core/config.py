from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Travel Planner"
    DEBUG: bool = False
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    
    # Database
    MONGODB_URL: str
    DATABASE_NAME: str = "ai_travel_planner"
    
    # Auth (Google)
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    # External APIs
    OPENAI_API_KEY: str
    OPENWEATHER_API_KEY: str
    AVIATIONSTACK_API_KEY: str
    GOOGLE_MAPS_API_KEY: str
    
    model_config = SettingsConfigDict(env_file=[".env", "../.env"], extra="ignore")

@lru_cache
def get_settings():
    return Settings()
