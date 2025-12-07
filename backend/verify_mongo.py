import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import sys
from dotenv import load_dotenv

# Load environment variables from ../.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

async def verify_data():
    # Get URL from env or default to localhost (but we expect env now)
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        print("Error: MONGODB_URL not found in environment variables.")
        return

    # Mask password for printing
    masked_url = mongodb_url
    if "@" in mongodb_url:
        try:
            prefix = mongodb_url.split("@")[0]
            suffix = mongodb_url.split("@")[1]
            # simple mask
            masked_url = f"{prefix.split(':')[0]}:****@{suffix}"
        except:
            pass

    print(f"Connecting to {masked_url}...")
    
    try:
        client = AsyncIOMotorClient(mongodb_url)
        # Force a connection to verify
        await client.admin.command('ping')
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    db_name = os.getenv("DATABASE_NAME", "ai_travel_planner")
    db = client[db_name]
    
    print(f"\nChecking database: '{db_name}'")
    
    collections = await db.list_collection_names()
    print(f"Collections found: {collections}")
    
    if "trips" in collections:
        count = await db.trips.count_documents({})
        print(f"Number of documents in 'trips' collection: {count}")
        
        if count > 0:
            latest_trip = await db.trips.find_one(sort=[("created_at", -1)])
            print("\nSample Trip (latest):")
            print(latest_trip)
    else:
        print("'trips' collection not found.")

if __name__ == "__main__":
    asyncio.run(verify_data())
