from fastapi import APIRouter, Request, HTTPException, Depends
from app.services.openai_service import OpenAIService
from app.services.places_service import PlacesService
from app.repositories.trip_repository import TripRepository
from app.models.trip import Trip
from app.core.security import get_current_user_id
from typing import Dict, Any
import asyncio

router = APIRouter(prefix="/trips", tags=["itinerary"])
openai_service = OpenAIService()
places_service = PlacesService()
trip_repository = TripRepository()

@router.post("/{trip_id}/itinerary")
async def generate_trip_itinerary(
    trip_id: str, 
    preview: bool = False,
    user_id: str = Depends(get_current_user_id)
):
    # 1. Fetch Trip
    trip = await trip_repository.get_trip(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this trip")

    # 2. Prepare Context
    # We convert the trip model to a dict to pass to the service
    trip_context = trip.model_dump(mode='json')
    
    # 3. Generate Itinerary
    itinerary = await openai_service.generate_itinerary(trip_context)
    
    # 3.5 Enrich Itinerary with Images
    if itinerary and "days" in itinerary:
        tasks = []
        for day in itinerary["days"]:
            for activity in day.get("activities", []):
                location = activity.get("location")
                if location:
                    # Create a task to fetch image
                    tasks.append(enrich_activity_with_image(activity, location))
        
        if tasks:
            await asyncio.gather(*tasks)

    # 4. Save Itinerary to Trip (Unless Preview)
    if not preview:
        success = await trip_repository.update_trip(trip_id, {"itinerary": itinerary})
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save itinerary")
        
    return itinerary

@router.put("/{trip_id}/itinerary")
async def save_trip_itinerary(
    trip_id: str, 
    request: Request,
    user_id: str = Depends(get_current_user_id)
):
    try:
        itinerary = await request.json()
    except Exception as e:
        print(f"DEBUG: Failed to parse JSON body: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    print(f"DEBUG: Saving itinerary for trip {trip_id} by user {user_id}")
    # print(f"DEBUG: Itinerary keys: {itinerary.keys()}")
    
    trip = await trip_repository.get_trip(trip_id)
    if not trip:
        print("DEBUG: Trip not found")
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip.user_id != user_id:
        print(f"DEBUG: Not authorized. Trip user: {trip.user_id}, Request user: {user_id}")
        raise HTTPException(status_code=403, detail="Not authorized to access this trip")

    success = await trip_repository.update_trip(trip_id, {"itinerary": itinerary})
    if not success:
        print("DEBUG: Update failed (modified_count=0)")
        # Check if it's because it's already the same
        if trip.itinerary == itinerary:
             print("DEBUG: Itinerary was already up to date")
             return {"message": "Itinerary saved successfully (no changes)"}
        raise HTTPException(status_code=500, detail="Failed to save itinerary")
    
    print("DEBUG: Itinerary saved successfully")
    return {"message": "Itinerary saved successfully"}


import logging

logger = logging.getLogger(__name__)

async def enrich_activity_with_image(activity: Dict[str, Any], location: str):
    logger.info(f"DEBUG: Fetching image for {location}")
    image_url = await places_service.get_place_photo(location)
    if image_url:
        logger.info(f"DEBUG: Found image for {location}: {image_url}")
        activity["image_url"] = image_url
    else:
        logger.warning(f"DEBUG: No image found for {location}")
