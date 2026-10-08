import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="automobile_sales_dwm"
)

cursor = conn.cursor()

# Top-selling car models
query = """
SELECT
    v.company,
    v.model,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY
    v.company,
    v.model
ORDER BY
    total_sales DESC
LIMIT 10;
"""

cursor.execute(query)

print("\nTOP 10 SELLING CAR MODELS")
print("-" * 60)

for row in cursor.fetchall():
    print(
        f"Company: {row[0]} | "
        f"Model: {row[1]} | "
        f"Sales: {row[2]} | "
        f"Revenue: ${row[3]:,.2f}"
    )

cursor.close()
conn.close()