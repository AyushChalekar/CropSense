import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor  # Changed from RandomForest
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv('paddydataset.csv')

# --- Feature Selection ---
target = 'Paddy yield(in Kg)'

categorical_features = [
    'Agriblock', 'Variety', 'Soil Types',
    'Wind Direction_D1_D30', 'Wind Direction_D31_D60',
    'Wind Direction_D61_D90', 'Wind Direction_D91_D120'
]

numerical_features = [
    'Hectares ', '30DRain( in mm)', '30_50DRain( in mm)', 
    '51_70DRain(in mm)', '71_105DRain(in mm)',
    'Min temp_D1_D30', 'Max temp_D1_D30',
    'Min temp_D31_D60', 'Max temp_D31_D60',
    'Min temp_D61_D90', 'Max temp_D61_D90',
    'Min temp_D91_D120', 'Max temp_D91_D120',
    'Inst Wind Speed_D1_D30(in Knots)', 'Inst Wind Speed_D31_D60(in Knots)', 
    'Inst Wind Speed_D61_D90(in Knots)', 'Inst Wind Speed_D91_D120(in Knots)',
    'Relative Humidity_D1_D30', 'Relative Humidity_D31_D60', 
    'Relative Humidity_D61_D90', 'Relative Humidity_D91_D120'
]

X = df[categorical_features + numerical_features]
y = df[target]

# --- Preprocessing Pipeline ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# --- Model Definition ---
# XGBoost typically benefits from a lower learning rate and more estimators 
# compared to Random Forest.
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        objective='reg:squarederror' # Explicitly set for regression
    ))
])

# --- Training ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Training XGBoost model...")
model.fit(X_train, y_train)

# --- Evaluation ---
y_pred = model.predict(X_test)
print(f"Model R2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"Model RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:.2f}")

# --- Save Model ---
joblib.dump(model, 'yield_prediction_model_xgb.pkl')
print("Model saved as 'yield_prediction_model_xgb.pkl'")