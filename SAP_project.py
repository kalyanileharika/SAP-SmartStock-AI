import pandas as pd
import numpy as np

# Load dataset
data = pd.read_csv("data/sales_data.csv")

# Convert date
data["Date"] = pd.to_datetime(data["Date"])

# Create features
data["Day"] = data["Date"].dt.day
data["Month"] = data["Date"].dt.month
data["DayOfWeek"] = data["Date"].dt.dayofweek

# Select features
X = data[["Day", "Month", "DayOfWeek", "Current_Stock"]].values
y = data["Units_Sold"].values

# Add a column of 1s for the intercept
X = np.column_stack((np.ones(len(X)), X))

# Train using Linear Regression mathematics
coefficients = np.linalg.pinv(X.T @ X) @ X.T @ y

# Predictions
predictions = X @ coefficients

# Calculate Mean Absolute Error
mae = np.mean(np.abs(y - predictions))

print("================================")
print("SAP SmartStock AI")
print("================================")
print("Dataset loaded successfully!")
print("AI model trained successfully!")
print("Mean Absolute Error:", round(mae, 2))

# Save trained model
np.save("model_coefficients.npy", coefficients)

print("Model saved successfully!")