from app.core.database import get_database
from app.models.trip import Trip
from typing import List, Optional
from bson import ObjectId
from datetime import datetime, date

class TripRepository:
    def __init__(self):
        self.collection_name = "trips"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create_trip(self, trip: Trip) -> Trip:
        collection = await self.get_collection()
        trip_dict = trip.model_dump(by_alias=True, exclude={"id"})
        
        # Convert date objects to datetime for MongoDB
        if 'start_date' in trip_dict:
            trip_dict['start_date'] = datetime.combine(trip_dict['start_date'], datetime.min.time())
        if 'end_date' in trip_dict:
            trip_dict['end_date'] = datetime.combine(trip_dict['end_date'], datetime.min.time())
            
        result = await collection.insert_one(trip_dict)
        trip.id = str(result.inserted_id)
        return trip

    async def get_trip(self, trip_id: str) -> Optional[Trip]:
        collection = await self.get_collection()
        try:
            oid = ObjectId(trip_id)
        except:
            return None
            
        doc = await collection.find_one({"_id": oid})
        if doc:
            return Trip(**doc)
        return None

    async def get_user_trips(self, user_id: str) -> List[Trip]:
        collection = await self.get_collection()
        # Only return trips that are NOT in DRAFT status (i.e., PLANNED or COMPLETED)
        cursor = collection.find({"user_id": user_id, "status": {"$ne": "DRAFT"}})
        trips = []
        async for doc in cursor:
            trips.append(Trip(**doc))
        return trips

    async def update_trip_status(self, trip_id: str, status: str) -> bool:
        collection = await self.get_collection()
        try:
            oid = ObjectId(trip_id)
        except:
            return False
        result = await collection.update_one({"_id": oid}, {"$set": {"status": status}})
        return result.modified_count > 0

    async def delete_trip(self, trip_id: str, user_id: str) -> bool:
        collection = await self.get_collection()
        try:
            oid = ObjectId(trip_id)
        except:
            return False
            
        result = await collection.delete_one({"_id": oid, "user_id": user_id})
        return result.deleted_count > 0

    async def update_trip(self, trip_id: str, update_data: dict) -> bool:
        collection = await self.get_collection()
        try:
            oid = ObjectId(trip_id)
        except:
            return False
            
        # Convert date objects to datetime for MongoDB
        if 'start_date' in update_data and isinstance(update_data['start_date'], date):
             update_data['start_date'] = datetime.combine(update_data['start_date'], datetime.min.time())
        if 'end_date' in update_data and isinstance(update_data['end_date'], date):
             update_data['end_date'] = datetime.combine(update_data['end_date'], datetime.min.time())

        result = await collection.update_one(
            {"_id": oid},
            {"$set": update_data}
        )
        return result.modified_count > 0
