import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
data = pd.read_csv("data/sales_data.csv")

# Convert date
data["Date"] = pd.to_datetime(data["Date"])

# Create useful date features
data["Day"] = data["Date"].dt.day
data["Month"] = data["Date"].dt.month
data["DayOfWeek"] = data["Date"].dt.dayofweek

# Features and target
X = data[["Day", "Month", "DayOfWeek", "Current_Stock"]]
y = data["Units_Sold"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create AI model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

# Calculate error
mae = mean_absolute_error(y_test, predictions)

print("================================")
print("SAP SmartStock AI")
print("================================")
print("Model trained successfully!")
print("Mean Absolute Error:", round(mae, 2))

# Save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")