from fastapi import APIRouter, Request, HTTPException, Depends
from app.services.trip_service import TripService
from app.models.api import CreateTripRequest, TripSummaryResponse
from app.models.trip import Trip
from app.core.security import get_current_user_id
from typing import List

router = APIRouter(prefix="/trips", tags=["trips"])
trip_service = TripService()

@router.post("/", response_model=TripSummaryResponse)
async def plan_trip(request: CreateTripRequest, user_id: str = Depends(get_current_user_id)):
    return await trip_service.create_trip_plan(user_id, request)

@router.put("/{trip_id}/confirm")
async def confirm_trip(trip_id: str, user_id: str = Depends(get_current_user_id)):
    success = await trip_service.confirm_trip(trip_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trip not found or not authorized")
    return {"message": "Trip confirmed successfully"}

@router.get("/", response_model=List[dict])
async def get_trips(user_id: str = Depends(get_current_user_id)):
    trips = await trip_service.get_user_trips(user_id)
    print(f"DEBUG: Found {len(trips)} trips")
    if trips:
        print(f"DEBUG: First trip ID: {trips[0].id}")
        # Force serialization to ensure 'id' is present and dates are strings
        return [t.model_dump(mode='json', by_alias=False) for t in trips]
    return []

@router.get("/{trip_id}", response_model=Trip)
async def get_trip(trip_id: str, user_id: str = Depends(get_current_user_id)):
    trip = await trip_service.get_trip(trip_id, user_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.delete("/{trip_id}")
async def delete_trip(trip_id: str, user_id: str = Depends(get_current_user_id)):
    success = await trip_service.delete_trip(trip_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Trip not found or not authorized")
    return {"message": "Trip deleted successfully"}
