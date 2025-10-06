from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# -----------------------------
# 1️⃣ Current Energy Usage (simulated)
# -----------------------------
@app.route("/api/current")
def current_usage():
    data = {
        "timestamp": datetime.now().isoformat(),
        "usage_kWh": round(random.uniform(50, 150), 2)  # simulate energy usage
    }
    return jsonify(data)

# -----------------------------
# 2️⃣ Forecast Endpoint (next 24h)
# -----------------------------
@app.route("/api/forecast")
def forecast():
    forecast_data = []
    now = datetime.now()
    for i in range(24):
        hour = now + timedelta(hours=i)
        forecast_data.append({
            "hour": hour.strftime("%H:%M"),
            "predicted_kWh": round(random.uniform(50, 150), 2)
        })
    return jsonify(forecast_data)

# -----------------------------
# 3️⃣ AI Recommendations
# -----------------------------
@app.route("/api/recommendations")
def recommendations():
    tips = [
        "Shift heavy appliances to off-peak hours.",
        "Use solar charging between 9 AM - 3 PM.",
        "Expected low demand at night — schedule EV charging."
    ]
    return jsonify(tips)

# -----------------------------
# 4️⃣ Impact Metrics
# -----------------------------
@app.route("/api/impact")
def impact():
    return jsonify({
        "energy_saved_kWh": round(random.uniform(50, 500), 2),
        "carbon_reduced_kg": round(random.uniform(20, 200), 2),
        "renewable_percent": round(random.uniform(30, 90), 2)
    })

# -----------------------------
# 5️⃣ Contact Form
# -----------------------------
@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")
    # For demo, just print to console
    print(f"Message received from {name} ({email}): {message}")
    return jsonify({"status": "success", "message": "Thank you for reaching out!"})

# -----------------------------
# Optional: Alerts for high usage
# -----------------------------
@app.route("/api/alerts")
def alerts():
    current = round(random.uniform(50, 150), 2)
    alert = "High usage detected!" if current > 120 else ""
    return jsonify({"current_kWh": current, "alert": alert})

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
