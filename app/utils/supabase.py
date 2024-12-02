# app/utils/supabase.py
from ..db import supabase
from ..core.security import hash_password, verify_password
from fastapi import HTTPException

async def create_user(email: str, username: str, password: str):
    hashed_password = hash_password(password)
    
    try:
        # Check if the email already exists
        email_check_response = supabase.from_("users").select("*").eq("email", email).execute()
        
        if email_check_response.data and len(email_check_response.data) > 0:
            return {"error": "Email is already in use."}
        
        # Check if the username already exists
        username_check_response = supabase.from_("users").select("*").eq("username", username).execute()
        
        if username_check_response.data and len(username_check_response.data) > 0:
            return {"error": "Username is already taken."}
        
        # Proceed to create the user
        response = supabase.from_("users").insert({
            "email": email,
            "username": username,
            "password": hashed_password
        }).execute()

        return response.data  # Return the created user data if successful
    
    except Exception as e:
        print(f"Exception during user creation: {str(e)}")  # Log the exception
        raise HTTPException(status_code=500, detail="An error occurred during user creation.")

async def authenticate_user(loginIdentifier: str, password: str):
    try:
        email_response = supabase.from_("users").select("*").eq("email", loginIdentifier).execute()
        username_response = supabase.from_("users").select("*").eq("username", loginIdentifier).execute()
        response = email_response if email_response.data else username_response
        user = response.data[0] if response.data else None
        if user and verify_password(password, user["password"]):
            return user
        return None
    
    except Exception as e:
        return None  # Or you can return {"error": str(e)} to handle exceptions if needed