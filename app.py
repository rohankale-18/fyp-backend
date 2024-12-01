from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load the saved model
model = joblib.load("predictive_model.pkl")

# Initialize FastAPI app
app = FastAPI()

# Define input schema
class ModelInput(BaseModel):
    Vrms: float
    Humidity: float
    Temperature: float
    Vmax: float


# Define the feature names used during training
feature_names = ['RMS Voltage', 'Humidity', 'Temperature', 'Peak Voltage']

# Define a prediction endpoint
@app.post("/predict")
def predict(input_data: ModelInput):
    # Create a DataFrame with the correct feature names
    input_df = pd.DataFrame([[input_data.Vrms, input_data.Humidity, input_data.Temperature, input_data.Vmax]],
                            columns=feature_names)
    
    # Perform prediction
    prediction = model.predict(input_df)
    
    return {"prediction": prediction.tolist()}