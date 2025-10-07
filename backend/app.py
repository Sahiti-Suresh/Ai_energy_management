from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# Load data & model
df = pd.read_csv("data/energy_data.csv")
model = joblib.load("model/energy_model.pkl")

# --- Forecast Generation ---
def generate_forecast():
    last_time = pd.to_datetime(df["timestamp"].iloc[-1])
    forecast = []
    for i in range(1, 25):  # next 24 hours
        next_time = last_time + timedelta(hours=i)
        hour = next_time.hour
        dayofweek = next_time.dayofweek
        temp = np.random.uniform(25, 35)
        humidity = np.random.uniform(50, 80)
        pred = model.predict([[hour, dayofweek, temp, humidity]])[0]
        forecast.append({
            "timestamp": next_time.isoformat(),
            "predicted_kWh": round(pred, 2),
            "temperature_C": round(temp, 1),
            "humidity_%": round(humidity, 1)
        })
    return forecast

# --- Routes ---
@app.route("/")
def home():
    return jsonify({"message": "Smart City backend is running successfully!"})

@app.route("/current", methods=["GET"])
def current_usage():
    last = df.iloc[-1].to_dict()
    return jsonify(last)

@app.route("/predict", methods=["GET"])
def predict():
    forecast = generate_forecast()
    return jsonify(forecast)

@app.route("/anomalies", methods=["GET"])
def anomalies():
    mean = df["consumption_kWh"].mean()
    std = df["consumption_kWh"].std()
    anom = df[np.abs(df["consumption_kWh"] - mean) > 2 * std].tail(10)
    return jsonify(anom.to_dict(orient="records"))

@app.route("/impact", methods=["GET"])
def impact():
    avg = df["consumption_kWh"].mean()
    forecast = generate_forecast()
    peak = max(f["predicted_kWh"] for f in forecast)
    saved_energy = max(0, (peak - avg) * 0.1)
    co2_saved = saved_energy * 0.85
    return jsonify({
        "average_usage_kWh": round(avg, 2),
        "predicted_peak_kWh": round(peak, 2),
        "energy_saved_kWh": round(saved_energy, 2),
        "carbon_saved_kg": round(co2_saved, 2)
    })

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    target = data.get("target", "default")
    actions = [
        "Shift EV charging to off-peak hours",
        "Reduce HVAC usage between 2 PM - 5 PM",
        "Dim street lighting by 15%",
        "Use stored solar energy for evening load"
    ]
    return jsonify({
        "target": target,
        "suggestions": actions,
        "status": "Optimization plan generated successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)
