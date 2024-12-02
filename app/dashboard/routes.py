from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from ..db import supabase
from ..core.security import get_current_user
import joblib
import pandas as pd

# Load the saved model
model = joblib.load("predictive_model.pkl")

router = APIRouter()

# Pydantic model for response (removed 'date' from here)
class MaintenanceLogResponse(BaseModel):
    generator_id: str
    maintenance_detail: str
    status: str
    name_of_person: str
    created_at: str
class MaintenanceLogEntry(BaseModel):
    generator_id: str
    maintenance_detail: str
    status: str
    name_of_person: str

# Route to get maintenance log entries for a specific user
@router.get("/entries", response_model=List[MaintenanceLogResponse])
async def get_user_maintenance_logs(user_id: str = Depends(get_current_user)):
    # Fetch entries for the logged-in user's user_id
    response = supabase.from_("generator_table").select("*").eq("user_id", user_id).execute()
    
    if not response:
        raise HTTPException(status_code=404, detail="No entries found for this user")
    
    print(response.data)
    return response.data

# Route to create a maintenance log entry (removed 'date' from here as well)
@router.post("/create-entry")
async def create_maintenance_log_entry(entry: MaintenanceLogEntry, user_id: str = Depends(get_current_user)):
    response = supabase.from_("generator_table").insert({
        "generator_id": entry.generator_id,
        "maintenance_detail": entry.maintenance_detail,
        "status": entry.status,
        "name_of_person": entry.name_of_person,
        "user_id": user_id,
    }).execute()

    # If insert failed, raise an error
    # if response.status_code != 201:
    #     raise HTTPException(status_code=400, detail="Failed to create maintenance log entry")

    return response.data

# Define input schema for prediction
class ModelInput(BaseModel):
    Vrms: float
    Humidity: float
    Temperature: float
    Vmax: float

# Define the feature names used during training
feature_names = ['RMS Voltage', 'Humidity', 'Temperature', 'Peak Voltage']

# Define a prediction endpoint
@router.post("/predict")
def predict(input_data: ModelInput):
    # Create a DataFrame with the correct feature names
    input_df = pd.DataFrame([[input_data.Vrms, input_data.Humidity, input_data.Temperature, input_data.Vmax]], columns=feature_names)
    
    # Perform prediction
    prediction = model.predict(input_df)
    
    return {"prediction": prediction.tolist()}
