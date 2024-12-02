# app/auth/routes.py
from fastapi import APIRouter, HTTPException
from ..auth.models import UserCreate, UserLogin, Token
from ..utils.supabase import create_user, authenticate_user
from ..core.security import create_access_token

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    user_data = await create_user(user.email, user.username, user.password)
    # Check if there's an error in the user data
    if "error" in user_data:
        raise HTTPException(status_code=400, detail=user_data["error"])
    access_token = create_access_token(data={"sub": user_data[0]['user_id']})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    auth_user = await authenticate_user(user.loginIdentifier, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": auth_user['user_id']})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
	return {"message": "Logout successful"}