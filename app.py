from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

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

# Define a prediction endpoint
@app.post("/predict")
def predict(input_data: ModelInput):
    # Convert input data to NumPy array
    features = np.array([[input_data.Vrms, input_data.Humidity, input_data.Temperature, input_data.Vmax]])
    prediction = model.predict(features)
    return {"prediction": prediction.tolist()}
