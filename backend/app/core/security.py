from fastapi import Request, HTTPException

def get_current_user_id(request: Request) -> str:
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user.get('sub') or user.get('id')
