from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from app.core.database import db
from app.core.logging import setup_logging
from app.core.config import get_settings
from app.controllers import auth_controller, trip_controller, itinerary_controller, user_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    db.connect()
    yield
    db.close()

app = FastAPI(title="AI Travel Planner API", lifespan=lifespan)

settings = get_settings()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Frontend
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(trip_controller.router)
app.include_router(itinerary_controller.router)
app.include_router(user_controller.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-travel-planner-backend"}

@app.get("/")
async def root():
    return {"message": "Welcome to AI Travel Planner API"}
