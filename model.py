import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import shap

# Simulated sensor data
X = pd.DataFrame({
    "voltage": np.random.randint(200, 280, 100),
    "temperature": np.random.randint(50, 100, 100),
    "vibration": np.random.rand(100),
    "pressure": np.random.rand(100)
})
y = np.random.choice([0, 1], 100)  # 0 = safe, 1 = unsafe

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

# SHAP explainer
explainer = shap.TreeExplainer(model)
joblib.dump(explainer, "explainer.pkl")

print("✅ model.pkl and explainer.pkl generated.")
