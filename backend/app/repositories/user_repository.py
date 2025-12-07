from app.core.database import get_database
from app.models.user import User
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.collection_name = "users"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def get_user(self, user_id: str):
        collection = await self.get_collection()
        user_doc = await collection.find_one({"_id": user_id})
        if user_doc:
            return User(**user_doc)
        return None

    async def create_or_update_user(self, user_id: str):
        collection = await self.get_collection()
        now = datetime.utcnow()
        
        # Try to find existing user
        user = await self.get_user(user_id)
        
        if user:
            # Update last login
            await collection.update_one(
                {"_id": user_id},
                {"$set": {"last_login": now}}
            )
            user.last_login = now
            return user
        else:
            # Create new user
            new_user = User(id=user_id, created_at=now, last_login=now)
            await collection.insert_one(new_user.model_dump(by_alias=True))
            return new_user

    async def update_preferences(self, user_id: str, preferences: str = None, home_airport: str = None, default_budget: float = None):
        collection = await self.get_collection()
        update_data = {}
        if preferences is not None:
            update_data["preferences"] = preferences
        if home_airport is not None:
            update_data["home_airport"] = home_airport
        if default_budget is not None:
            update_data["default_budget"] = default_budget
            
        if update_data:
            await collection.update_one(
                {"_id": user_id},
                {"$set": update_data}
            )
        return await self.get_user(user_id)
