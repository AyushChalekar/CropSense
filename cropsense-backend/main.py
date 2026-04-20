# cropsense-backend/main.py
import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime, timedelta

app = FastAPI(title="CropSense API - Production")
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

def generate_actionable_insights(data: CropInput) -> list:
    """
    Generates specific warnings OR success signals for every major factor.
    """
    insights = []
    
    # --- 1. RAINFALL ANALYSIS ---
    if data.rain_d1_30 < 30:
        insights.append({"type": "warning", "text": f"[P1] Critical low rainfall (<b>{data.rain_d1_30}mm</b>). Supplement irrigation immediately."})
    else:
        insights.append({"type": "success", "text": f"Phase 1 rainfall (<b>{data.rain_d1_30}mm</b>) is optimal for root establishment."})
    
    total_mid_rain = data.rain_d30_50 + data.rain_d51_70
    if total_mid_rain < 100:
         insights.append({"type": "warning", "text": f"[P2-P3] Low mid-season rain (<b>{total_mid_rain}mm</b>) may reduce grain filling."})
    elif total_mid_rain > 400:
         insights.append({"type": "info", "text": f"[P2-P3] Excessive moisture detected. Watch for root rot in <b>{data.soil_type}</b> soil."})
    else:
         insights.append({"type": "success", "text": f"Mid-season rainfall (<b>{total_mid_rain}mm</b>) is highly favorable for vegetative growth."})

    # --- 2. TEMPERATURE STRESS ---
    phases_max_temps = [data.max_temp_d1_30, data.max_temp_d31_60, data.max_temp_d61_90, data.max_temp_d91_120]
    if any(t > 35 for t in phases_max_temps):
        insights.append({"type": "warning", "text": "Heat stress detected (>35 C). Ensure adequate soil moisture to cool the canopy."})
    else:
        insights.append({"type": "success", "text": "Temperature profiles remained within safe metabolic limits throughout the season."})

    # --- 3. HUMIDITY & DISEASE ---
    if data.humidity_d61_90 > 85:
        insights.append({"type": "warning", "text": f"High humidity (<b>{data.humidity_d61_90}%</b>) in Phase 3. High Blast/Blight risk for <b>{data.variety}</b>."})
    elif data.humidity_d61_90 < 40:
        insights.append({"type": "info", "text": "Very dry air in Phase 3. Monitor for spider mites or leaf desiccation."})
    else:
        insights.append({"type": "success", "text": f"Phase 3 humidity (<b>{data.humidity_d61_90}%</b>) is optimal, keeping fungal risks low."})

    # --- 4. WIND & LODGING ---
    max_wind = max(data.wind_speed_d1_30, data.wind_speed_d31_60, data.wind_speed_d61_90, data.wind_speed_d91_120)
    if max_wind > 12:
        insights.append({"type": "warning", "text": f"High wind speeds (<b>{max_wind} Kts</b>) detected. Consider windbreaks to prevent lodging."})
    else:
        insights.append({"type": "success", "text": f"Wind conditions (Max <b>{max_wind} Kts</b>) are safe from lodging risks."})
        
    return insights
@app.post("/predict")
def predict_yield(data: CropInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # 1. Map the incoming Pydantic data to the dictionary FIRST
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
        'Hectares ': [data.hectares], 
        
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
    
    # 2. THEN create the DataFrame, run the prediction, and generate insights
    try:
        df = pd.DataFrame(input_dict)
        prediction = model.predict(df)
        
        # Generate the dynamic insights based on the incoming data
        dynamic_insights = generate_actionable_insights(data)
        
        return {
            "predicted_yield": round(float(prediction[0]), 2),
            "insights": dynamic_insights,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/fetch-weather")
async def fetch_weather(lat: float, lon: float, plant_date: str):
    """
    Fetches 120 days of weather data starting from plant_date 
    and aggregates them into the 4 phases.
    """
    end_date = (datetime.strptime(plant_date, "%Y-%m-%d") + timedelta(days=120)).strftime("%Y-%m-%d")
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={plant_date}&end_date={end_date}&daily=rain_sum,temperature_2m_max,temperature_2m_min,windspeed_10m_max,relative_humidity_2m_max&timezone=auto"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch weather data")
        
        raw_data = response.json()['daily']
        
        def aggregate_phase(start_idx, end_idx):
            # Slicing the lists for the specific phase days
            return {
                "rain": sum(raw_data['rain_sum'][start_idx:end_idx]),
                "min_temp": sum(raw_data['temperature_2m_min'][start_idx:end_idx]) / (end_idx - start_idx),
                "max_temp": sum(raw_data['temperature_2m_max'][start_idx:end_idx]) / (end_idx - start_idx),
                "wind": sum(raw_data['windspeed_10m_max'][start_idx:end_idx]) / (end_idx - start_idx),
                "humidity": sum(raw_data['relative_humidity_2m_max'][start_idx:end_idx]) / (end_idx - start_idx),
            }

        # Mapping phases to your specific day ranges
        p1 = aggregate_phase(0, 30)
        p2 = aggregate_phase(31, 60)
        p3 = aggregate_phase(61, 90)
        p4 = aggregate_phase(91, 120)

        return {
            "p1": p1, "p2": p2, "p3": p3, "p4": p4,
            "wind_dir": "NE" # Open-Meteo provides degrees, mapping to strings (SW/NE) would require a helper
        }
    
# CORS: Allow Vue frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "yield_prediction_model.pkl")

try:
    model = joblib.load(MODEL_PATH) 
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)