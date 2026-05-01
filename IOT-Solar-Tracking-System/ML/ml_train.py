import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# IMPORTANT: Read the correct file
df = pd.read_csv("ml_dataset.csv")

print("Columns seen by ML:", df.columns)
print("Shape:", df.shape)

# Create prediction target
df["future_energy"] = df["energy"].shift(-1)

df.dropna(inplace=True)

X = df[["sun_angle", "panel_angle", "voltage", "current", "power"]]
y = df["future_energy"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R2:", r2_score(y_test, y_pred))

print("ML OK")
