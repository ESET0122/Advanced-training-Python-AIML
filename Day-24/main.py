from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import tensorflow as tf
import os

# Load the preprocessor and model
preprocessor = joblib.load("preprocessor.joblib")
model = tf.keras.models.load_model("hotel_cancellation_model.keras")

# Define the input schema with all features
class BookingData(BaseModel):
    lead_time: int
    arrival_date_week_number: int
    arrival_date_day_of_month: int
    stays_in_weekend_nights: int
    stays_in_week_nights: int
    adults: int
    children: int
    babies: int
    is_repeated_guest: int
    previous_cancellations: int
    previous_bookings_not_canceled: int
    required_car_parking_spaces: int
    total_of_special_requests: int
    adr: float
    hotel: str
    arrival_date_month: int  # (1-12)
    meal: str
    market_segment: str
    distribution_channel: str
    reserved_room_type: str
    deposit_type: str
    customer_type: str

app = FastAPI()

# Serve static files (web page)
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index_html():
    return FileResponse("static/index.html")

@app.post("/predict")
def predict_cancellation(data: BookingData):
    data_dict = data.dict()
    df = pd.DataFrame([data_dict])
    try:
        X_trans = preprocessor.transform(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing failed: {e}")
    pred = model.predict(X_trans)
    return {"cancellation_probability": float(pred[0][0])}
