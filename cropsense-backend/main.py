import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CropSense API - Production")

# CORS Configuration for Vue.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model pipeline
try:
    # Ensure this matches the filename in your training.py joblib.dump()
    model = joblib.load("yield_prediction_model.pkl") 
    print("Model pipeline loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class CropInput(BaseModel):
    # General & Soil
    hectares: float
    agriblock: str
    variety: str
    soil_type: str
    
    # Rainfall
    rain_30d: float
    rain_30_50d: float
    rain_51_70d: float
    rain_71_105d: float
    
    # Temperature (Min/Max)
    min_temp_d1_30: float
    max_temp_d1_30: float
    min_temp_d31_60: float
    max_temp_d31_60: float
    min_temp_d61_90: float
    max_temp_d61_90: float
    min_temp_d91_120: float
    max_temp_d91_120: float
    
    # Wind Speed
    wind_speed_d1_30: float
    wind_speed_d31_60: float
    wind_speed_d61_90: float
    wind_speed_d91_120: float
    
    # Wind Direction (Categorical)
    wind_dir_d1_30: str
    wind_dir_d31_60: str
    wind_dir_d61_90: str
    wind_dir_d91_120: str
    
    # Humidity
    humidity_d1_30: float
    humidity_d31_60: float
    humidity_d61_90: float
    humidity_d91_120: float

@app.post("/predict")
def predict_yield(data: CropInput):
    if not model:
        raise HTTPException(status_code=500, detail="Prediction model not found on server.")

    # Data mapping strictly following training.py feature selection
    input_dict = {
        # Categorical
        'Agriblock': [data.agriblock],
        'Variety': [data.variety],
        'Soil Types': [data.soil_type],
        'Wind Direction_D1_D30': [data.wind_dir_d1_30],
        'Wind Direction_D31_D60': [data.wind_dir_d31_60],
        'Wind Direction_D61_D90': [data.wind_dir_d61_90],
        'Wind Direction_D91_D120': [data.wind_dir_d91_120],
        
        # Numerical
        'Hectares ': [data.hectares], # Crucial: Maintain the trailing space from training
        '30DRain( in mm)': [data.rain_30d],
        '30_50DRain( in mm)': [data.rain_30_50d],
        '51_70DRain(in mm)': [data.rain_51_70d],
        '71_105DRain(in mm)': [data.rain_71_105d],
        'Min temp_D1_D30': [data.min_temp_d1_30],
        'Max temp_D1_D30': [data.max_temp_d1_30],
        'Min temp_D31_D60': [data.min_temp_d31_60],
        'Max temp_D31_D60': [data.max_temp_d31_60],
        'Min temp_D61_D90': [data.min_temp_d61_90],
        'Max temp_D61_D90': [data.max_temp_d61_90],
        'Min temp_D91_D120': [data.min_temp_d91_120],
        'Max temp_D91_D120': [data.max_temp_d91_120],
        'Inst Wind Speed_D1_D30(in Knots)': [data.wind_speed_d1_30],
        'Inst Wind Speed_D31_D60(in Knots)': [data.wind_speed_d31_60],
        'Inst Wind Speed_D61_D90(in Knots)': [data.wind_speed_d61_90],
        'Inst Wind Speed_D91_D120(in Knots)': [data.wind_speed_d91_120],
        'Relative Humidity_D1_D30': [data.humidity_d1_30],
        'Relative Humidity_D31_D60': [data.humidity_d31_60],
        'Relative Humidity_D61_D90': [data.humidity_d61_90],
        'Relative Humidity_D91_D120': [data.humidity_d91_120]
    }
    
    try:
        df = pd.DataFrame(input_dict)
        prediction = model.predict(df)
        
        return {
            "predicted_yield": round(float(prediction[0]), 2),
            "unit": "Kg",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)