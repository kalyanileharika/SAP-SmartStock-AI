from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="leharika@17",
    database="smartstock"
)

# Load trained AI model
coefficients = np.load("model_coefficients.npy")


@app.route("/")
def home():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            COUNT(DISTINCT product_id) AS total_products
            SUM(current_stock) AS total_stock,
            SUM(units_sold) AS total_sold
        FROM inventory
    """)

    stats = cursor.fetchone()
    cursor.close()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT product_id, product_name,
       MAX(current_stock) AS current_stock,
       SUM(units_sold) AS units_sold
FROM inventory
GROUP BY product_id, product_name
ORDER BY product_id
    """)

    inventory_data = cursor.fetchall()
    cursor.close()

    return render_template(
        "dashboard.html",
        total_products=stats["total_products"],
        total_stock=stats["total_stock"],
        total_sold=stats["total_sold"],
        inventory_data=inventory_data,
        history_dates=[],
        history_sales=[]
    )

@app.route("/predict", methods=["POST"])
def predict():

    product = request.form["product"]

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM inventory WHERE product_id = %s ORDER BY date DESC LIMIT 1",
        (product,)
    )

    product_data = cursor.fetchone()
    history_cursor = db.cursor(dictionary=True)

    history_cursor.execute(
        "SELECT date, units_sold FROM inventory WHERE product_id = %s ORDER BY date",
        (product,)
    )

    history_data = history_cursor.fetchall()
    history_cursor.close()
    cursor.close()

    if product_data is None:
        return "Product not found in database"

    stock = product_data["current_stock"]

    today = pd.Timestamp.today()

    day = today.day
    month = today.month
    day_of_week = today.dayofweek

    X = np.array([[1, day, month, day_of_week, stock]])

    predicted_demand = X @ coefficients
    predicted_demand = max(0, predicted_demand[0])
    replenishment = max(0, predicted_demand - stock)

    if stock < predicted_demand:
        risk = "HIGH"
        recommendation = "Replenish Stock"
    elif stock < predicted_demand * 1.5:
        risk = "MEDIUM"
        recommendation = "Monitor Stock"
    else:
        risk = "LOW"
        recommendation = "Stock Level is Healthy"

    return render_template(
        "dashboard.html",
        product=product,
        product_name=product_data["product_name"],
        stock=int(stock),
        demand=round(predicted_demand, 2),
        risk=risk,
        recommendation=recommendation,
        replenishment=round(replenishment),
        history_dates=[str(row["date"]) for row in history_data],
        history_sales=[row["units_sold"] for row in history_data]
    )


if __name__ == "__main__":
    app.run(debug=True)