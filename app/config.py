# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")  # Replace with a strong key

settings = Settings()
