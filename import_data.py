import pandas as pd
import mysql.connector

# Load CSV
data = pd.read_csv("data/sales_data.csv")

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="leharika@17",
    database="smartstock"
)

cursor = db.cursor()

# Insert data
sql = """
INSERT INTO inventory
(product_id, product_name, category, units_sold, current_stock, date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in data.iterrows():
    values = (
        row["Product_ID"],
        row["Product_Name"],
        row["Category"],
        int(row["Units_Sold"]),
        int(row["Current_Stock"]),
        row["Date"]
    )

    cursor.execute(sql, values)

db.commit()

print("Data imported successfully!")
print("Rows inserted:", len(data))

cursor.close()
db.close()