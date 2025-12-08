import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.core.security import get_current_user_id
from app.models.user import User

# Override auth dependency
async def mock_get_current_user_id():
    return "test_user_id"

app.dependency_overrides[get_current_user_id] = mock_get_current_user_id

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_current_user_endpoint():
    with patch('app.controllers.user_controller.user_repo.get_user') as mock_get_user:
        mock_get_user.return_value = User(
            id="test_user_id"
        )

        response = client.get("/users/me")
        
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == "test_user_id"

@pytest.mark.asyncio
async def test_update_preferences_endpoint():
    with patch('app.controllers.user_controller.user_repo.update_preferences') as mock_update:
        mock_update.return_value = User(
            id="test_user_id",
            preferences="Vegetarian",
            home_airport="JFK",
            default_budget=1000.0
        )

        payload = {
            "preferences": "Vegetarian",
            "home_airport": "JFK",
            "default_budget": 1000.0
        }

        response = client.put("/users/me/preferences", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["preferences"] == "Vegetarian"
        assert data["home_airport"] == "JFK"
