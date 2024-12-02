# app/auth/models.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    loginIdentifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
