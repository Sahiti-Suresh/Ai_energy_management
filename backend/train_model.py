import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

os.makedirs("model", exist_ok=True)

# Load simulated data
df = pd.read_csv("data/energy_data.csv")
df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
df["dayofweek"] = pd.to_datetime(df["timestamp"]).dt.dayofweek

X = df[["hour", "dayofweek", "temperature_C", "humidity_%"]]
y = df["consumption_kWh"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/energy_model.pkl")

print("✅ Model trained and saved to model/energy_model.pkl")
