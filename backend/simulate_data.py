import pandas as pd
import numpy as np
import os

print(os.getcwd())

os.makedirs("data", exist_ok=True)

rng = pd.date_range("2025-01-01", periods=1000, freq="h")
data = {
    "timestamp": rng,
    "consumption_kWh": np.random.normal(220, 40, len(rng)).round(2),
    "temperature_C": np.random.uniform(25, 35, len(rng)).round(1),
    "humidity_%": np.random.uniform(50, 80, len(rng)).round(1)
}
df = pd.DataFrame(data)
print(df.head())
print(df.shape)
df.to_csv("data/energy_data.csv", index=False)
print("✅ Simulated dataset created at data/energy_data.csv")
file_path = os.path.join(os.getcwd(), "data", "energy_data.csv")
df.to_csv(file_path, index=False)
print("✅ Data saved to:", file_path)

