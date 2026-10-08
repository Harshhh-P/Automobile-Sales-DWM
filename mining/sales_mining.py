import mysql.connector

# ============================================================
# CONNECT TO MYSQL
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="automobile_sales_dwm"
)

cursor = conn.cursor()


# ============================================================
# 1. TOP 10 SELLING CAR MODELS
# ============================================================

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
print("-" * 70)

for row in cursor.fetchall():
    print(
        f"Company: {row[0]} | "
        f"Model: {row[1]} | "
        f"Sales: {row[2]} | "
        f"Revenue: ${row[3]:,.2f}"
    )


# ============================================================
# 2. DEALER PERFORMANCE ANALYSIS
# ============================================================

query = """
SELECT
    d.dealer_name,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_dealer d
    ON f.dealer_id = d.dealer_id
GROUP BY
    d.dealer_name
ORDER BY
    total_revenue DESC;
"""

cursor.execute(query)

print("\nDEALER PERFORMANCE ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Dealer: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 3. COMPANY PERFORMANCE ANALYSIS
# ============================================================

query = """
SELECT
    v.company,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY
    v.company
ORDER BY
    total_revenue DESC;
"""

cursor.execute(query)

print("\nCOMPANY PERFORMANCE ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Company: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 4. REGIONAL PERFORMANCE ANALYSIS
# ============================================================

query = """
SELECT
    l.dealer_region,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY
    l.dealer_region
ORDER BY
    total_revenue DESC;
"""

cursor.execute(query)

print("\nREGIONAL PERFORMANCE ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Region: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 5. VEHICLE / BODY STYLE ANALYSIS
# ============================================================

query = """
SELECT
    v.body_style,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY
    v.body_style
ORDER BY
    total_sales DESC;
"""

cursor.execute(query)

print("\nBODY STYLE PERFORMANCE ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Body Style: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 6. TRANSMISSION ANALYSIS
# ============================================================

query = """
SELECT
    v.transmission,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY
    v.transmission
ORDER BY
    total_sales DESC;
"""

cursor.execute(query)

print("\nTRANSMISSION ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Transmission: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 7. CUSTOMER GENDER ANALYSIS
# ============================================================

query = """
SELECT
    c.gender,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    c.gender
ORDER BY
    total_sales DESC;
"""

cursor.execute(query)

print("\nCUSTOMER GENDER ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Gender: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 8. INCOME GROUP ANALYSIS
# ============================================================

query = """
SELECT
    CASE
        WHEN c.annual_income < 50000 THEN 'Low Income'
        WHEN c.annual_income < 100000 THEN 'Medium Income'
        ELSE 'High Income'
    END AS income_group,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    CASE
        WHEN c.annual_income < 50000 THEN 'Low Income'
        WHEN c.annual_income < 100000 THEN 'Medium Income'
        ELSE 'High Income'
    END
ORDER BY
    total_revenue DESC;
"""

cursor.execute(query)

print("\nCUSTOMER INCOME GROUP ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Income Group: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 9. COLOR PREFERENCE ANALYSIS
# ============================================================

query = """
SELECT
    v.color,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY
    v.color
ORDER BY
    total_sales DESC;
"""

cursor.execute(query)

print("\nCAR COLOR PREFERENCE ANALYSIS")
print("-" * 70)

for row in cursor.fetchall():
    print(
        f"Color: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f}"
    )


# ============================================================
# 10. TOP 10 DEALERS BY REVENUE
# ============================================================

query = """
SELECT
    d.dealer_name,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_dealer d
    ON f.dealer_id = d.dealer_id
GROUP BY
    d.dealer_name
ORDER BY
    total_revenue DESC
LIMIT 10;
"""

cursor.execute(query)

print("\nTOP 10 DEALERS BY REVENUE")
print("-" * 70)

for row in cursor.fetchall():
    print(
        f"Dealer: {row[0]} | "
        f"Revenue: ${row[1]:,.2f}"
    )


# ============================================================
# 11. TOP 10 COMPANIES BY REVENUE
# ============================================================

query = """
SELECT
    v.company,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY
    v.company
ORDER BY
    total_revenue DESC
LIMIT 10;
"""

cursor.execute(query)

print("\nTOP 10 COMPANIES BY REVENUE")
print("-" * 70)

for row in cursor.fetchall():
    print(
        f"Company: {row[0]} | "
        f"Revenue: ${row[1]:,.2f}"
    )


# ============================================================
# 12. YEAR-WISE SALES ANALYSIS
# ============================================================

query = """
SELECT
    d.year,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_sale_value
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY
    d.year
ORDER BY
    d.year;
"""

cursor.execute(query)

print("\nYEAR-WISE SALES ANALYSIS")
print("-" * 75)

for row in cursor.fetchall():
    print(
        f"Year: {row[0]} | "
        f"Sales: {row[1]} | "
        f"Revenue: ${row[2]:,.2f} | "
        f"Average Sale: ${row[3]:,.2f}"
    )


# ============================================================
# 13. MONTH-WISE SALES ANALYSIS
# ============================================================

query = """
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;
"""

cursor.execute(query)

print("\nMONTH-WISE SALES ANALYSIS")
print("-" * 80)

for row in cursor.fetchall():
    print(
        f"Year: {row[0]} | "
        f"Month: {row[2]} | "
        f"Sales: {row[3]} | "
        f"Revenue: ${row[4]:,.2f}"
    )


# ============================================================
# 14. TOP 10 MOST EXPENSIVE VEHICLE SALES
# ============================================================

query = """
SELECT
    v.company,
    v.model,
    f.price
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
ORDER BY
    f.price DESC
LIMIT 10;
"""

cursor.execute(query)

print("\nTOP 10 MOST EXPENSIVE VEHICLE SALES")
print("-" * 70)

for row in cursor.fetchall():
    print(
        f"Company: {row[0]} | "
        f"Model: {row[1]} | "
        f"Price: ${row[2]:,.2f}"
    )


# ============================================================
# 15. COMPANY + REGION ANALYSIS
# ============================================================

query = """
SELECT
    v.company,
    l.dealer_region,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY
    v.company,
    l.dealer_region
ORDER BY
    total_revenue DESC
LIMIT 20;
"""

cursor.execute(query)

print("\nCOMPANY + REGION ANALYSIS")
print("-" * 85)

for row in cursor.fetchall():
    print(
        f"Company: {row[0]} | "
        f"Region: {row[1]} | "
        f"Sales: {row[2]} | "
        f"Revenue: ${row[3]:,.2f}"
    )


# ============================================================
# CLOSE CONNECTION
# ============================================================

cursor.close()
conn.close()

print("\n" + "=" * 70)
print("DATA MINING ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)