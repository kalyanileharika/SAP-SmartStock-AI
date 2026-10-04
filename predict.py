import pandas as pd
import numpy as np

# Load dataset
data = pd.read_csv("data/sales_data.csv")
data["Date"] = pd.to_datetime(data["Date"])

# Load trained model
coefficients = np.load("model_coefficients.npy")

print("================================")
print("SAP SMARTSTOCK AI")
print("Demand Prediction System")
print("================================")

# Ask user for input
product = input("Enter Product ID (P001-P008): ")
stock = float(input("Enter Current Stock: "))

# Get today's date features
today = pd.Timestamp.today()

day = today.day
month = today.month
day_of_week = today.dayofweek

# Create input
X = np.array([[1, day, month, day_of_week, stock]])

# Predict demand
predicted_demand = X @ coefficients
predicted_demand = max(0, predicted_demand[0])

print()
print("Product:", product)
print("Current Stock:", int(stock))
print("Predicted Demand:", round(predicted_demand, 2), "units")

# Stock risk
if stock < predicted_demand:
    risk = "HIGH"
    recommendation = "Replenish Stock"
elif stock < predicted_demand * 1.5:
    risk = "MEDIUM"
    recommendation = "Monitor Stock"
else:
    risk = "LOW"
    recommendation = "Stock Level is Healthy"

print("Stock Risk:", risk)
print("Recommendation:", recommendation)