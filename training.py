import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv('paddydataset.csv')

# --- Feature Selection ---
# We select only features accessible to a typical user (Soil test, Weather forecast/history, Location)
# We exclude specific log-based features like 'Urea_40Days', 'DAP_20days', 'Nursery area', etc.

# Target Variable
target = 'Paddy yield(in Kg)'

# Categorical Features (User Input)
categorical_features = [
    'Agriblock',               # Location Context
    'Variety',                 # Crop Variety
    'Soil Types',              # Soil Test Result
    # Weather: Wind Directions for different growth stages
    'Wind Direction_D1_D30', 'Wind Direction_D31_D60',
    'Wind Direction_D61_D90', 'Wind Direction_D91_D120'
]

# Numerical Features (User Input / Weather Data)
numerical_features = [
    'Hectares ',               # Land Size (Note: Dataset has a trailing space in column name)
    
    # Rainfall (Accessible from weather records)
    '30DRain( in mm)', '30_50DRain( in mm)', '51_70DRain(in mm)', '71_105DRain(in mm)',
    
    # Temperature (Min/Max for different stages)
    'Min temp_D1_D30', 'Max temp_D1_D30',
    'Min temp_D31_D60', 'Max temp_D31_D60',
    'Min temp_D61_D90', 'Max temp_D61_D90',
    'Min temp_D91_D120', 'Max temp_D91_D120',
    
    # Wind Speed
    'Inst Wind Speed_D1_D30(in Knots)', 'Inst Wind Speed_D31_D60(in Knots)', 
    'Inst Wind Speed_D61_D90(in Knots)', 'Inst Wind Speed_D91_D120(in Knots)',
    
    # Humidity
    'Relative Humidity_D1_D30', 'Relative Humidity_D31_D60', 
    'Relative Humidity_D61_D90', 'Relative Humidity_D91_D120'
]

# Create X (Features) and y (Target)
X = df[categorical_features + numerical_features]
y = df[target]

# --- Preprocessing Pipeline ---
# OneHotEncode categorical data (handle_unknown='ignore' allows new categories in future)
# Standardize numerical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# --- Model Definition ---
# Using Random Forest for robustness
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# --- Training ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training model...")
model.fit(X_train, y_train)

# --- Evaluation ---
y_pred = model.predict(X_test)
print(f"Model R2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"Model RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:.2f}")

# --- Save Model ---
joblib.dump(model, 'yield_prediction_model.pkl')
print("Model saved as 'yield_prediction_model.pkl'")