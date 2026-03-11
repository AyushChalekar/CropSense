import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CropSense API - Production")

# CORS: Allow Vue frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
try:
    model = joblib.load("../yield_prediction_model.pkl") 
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Pydantic model matches the specific features in training.py
class CropInput(BaseModel):
    # --- Field Data ---
    hectares: float
    agriblock: str
    variety: str
    soil_type: str
    
    # --- Weather Phase 1 (Days 1-30) ---
    rain_d1_30: float
    min_temp_d1_30: float
    max_temp_d1_30: float
    wind_speed_d1_30: float
    wind_dir_d1_30: str
    humidity_d1_30: float
    
    # --- Weather Phase 2 (Days 31-60) ---
    rain_d30_50: float  # Note: training.py uses '30_50DRain'
    min_temp_d31_60: float
    max_temp_d31_60: float
    wind_speed_d31_60: float
    wind_dir_d31_60: str
    humidity_d31_60: float
    
    # --- Weather Phase 3 (Days 61-90) ---
    rain_d51_70: float # Note: training.py uses '51_70DRain'
    min_temp_d61_90: float
    max_temp_d61_90: float
    wind_speed_d61_90: float
    wind_dir_d61_90: str
    humidity_d61_90: float

    # --- Weather Phase 4 (Days 91-120) ---
    rain_d71_105: float # Note: training.py uses '71_105DRain'
    min_temp_d91_120: float
    max_temp_d91_120: float
    wind_speed_d91_120: float
    wind_dir_d91_120: str
    humidity_d91_120: float

@app.post("/predict")
def predict_yield(data: CropInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # STRICT MAPPING: Pydantic -> DataFrame Columns (Must match training.py exactly)
    input_dict = {
        # Categorical
        'Agriblock': [data.agriblock],
        'Variety': [data.variety],
        'Soil Types': [data.soil_type],
        'Wind Direction_D1_D30': [data.wind_dir_d1_30],
        'Wind Direction_D31_D60': [data.wind_dir_d31_60],
        'Wind Direction_D61_D90': [data.wind_dir_d61_90],
        'Wind Direction_D91_D120': [data.wind_dir_d91_120],
        
        # Numerical - Field
        'Hectares ': [data.hectares], # Note the space
        
        # Numerical - Rain
        '30DRain( in mm)': [data.rain_d1_30],
        '30_50DRain( in mm)': [data.rain_d30_50],
        '51_70DRain(in mm)': [data.rain_d51_70],
        '71_105DRain(in mm)': [data.rain_d71_105],
        
        # Numerical - Temp
        'Min temp_D1_D30': [data.min_temp_d1_30], 'Max temp_D1_D30': [data.max_temp_d1_30],
        'Min temp_D31_D60': [data.min_temp_d31_60], 'Max temp_D31_D60': [data.max_temp_d31_60],
        'Min temp_D61_D90': [data.min_temp_d61_90], 'Max temp_D61_D90': [data.max_temp_d61_90],
        'Min temp_D91_D120': [data.min_temp_d91_120], 'Max temp_D91_D120': [data.max_temp_d91_120],
        
        # Numerical - Wind Speed
        'Inst Wind Speed_D1_D30(in Knots)': [data.wind_speed_d1_30],
        'Inst Wind Speed_D31_D60(in Knots)': [data.wind_speed_d31_60],
        'Inst Wind Speed_D61_D90(in Knots)': [data.wind_speed_d61_90],
        'Inst Wind Speed_D91_D120(in Knots)': [data.wind_speed_d91_120],
        
        # Numerical - Humidity
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
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)