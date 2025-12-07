from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from app.services.auth_service import setup_oauth
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])
oauth = setup_oauth()
user_repo = UserRepository()

@router.get("/login")
async def login(request: Request):
    # Explicitly set the redirect URI for local development to avoid container hostname issues
    redirect_uri = "http://localhost:8000/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth Error: {str(e)}")
        
    user_info = token.get('userinfo')
    if user_info:
        user_id = user_info['sub']
        # Save user persistence
        await user_repo.create_or_update_user(user_id)
        
        # Set session
        request.session['user'] = dict(user_info)
        
        # Redirect to frontend dashboard or home
        return RedirectResponse(url="http://localhost:3000")
        
    raise HTTPException(status_code=400, detail="Login failed: No user info")

@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return {"message": "Logged out"}

@router.get("/me")
async def get_current_user(request: Request):
    user = request.session.get('user')
    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authenticated")
