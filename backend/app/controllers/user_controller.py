from fastapi import APIRouter, Request, HTTPException, Depends
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import get_current_user_id
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])
user_repo = UserRepository()

from typing import Optional

class UpdatePreferencesRequest(BaseModel):
    preferences: Optional[str] = None
    home_airport: Optional[str] = None
    default_budget: Optional[float] = None

@router.get("/me", response_model=User)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    user = await user_repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me/preferences", response_model=User)
async def update_preferences(
    request: UpdatePreferencesRequest, 
    user_id: str = Depends(get_current_user_id)
):
    # We need to update the repository method to accept more fields
    user = await user_repo.update_preferences(
        user_id, 
        preferences=request.preferences,
        home_airport=request.home_airport,
        default_budget=request.default_budget
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
