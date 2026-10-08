import pandas as pd
import mysql.connector

# ============================================================
# 1. READ RAW DATA
# ============================================================

file_path = "data/raw/car_data.csv"

df = pd.read_csv(file_path)

print("Raw dataset loaded successfully.")
print("Rows:", len(df))


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()

# Rename columns for easier processing
df.rename(columns={
    "Customer Name": "Customer_Name",
    "Annual Income": "Annual_Income",
    "Dealer_Name": "Dealer_Name",
    "Dealer_No": "Dealer_No",
    "Price ($)": "Price",
    "Body Style": "Body_Style",
    "Dealer_Region": "Dealer_Region"
}, inplace=True)


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

# There is 1 missing Customer Name
df["Customer_Name"] = df["Customer_Name"].fillna("Unknown Customer")


# ============================================================
# 4. CONVERT DATA TYPES
# ============================================================

df["Date"] = pd.to_datetime(df["Date"])

# Keep Phone and Dealer_No as strings
df["Phone"] = df["Phone"].astype(str)
df["Dealer_No"] = df["Dealer_No"].astype(str)


# ============================================================
# 5. CONNECT TO MYSQL
# ============================================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="automobile_sales_dwm"
)

cursor = connection.cursor()

print("Connected to MySQL successfully.")


# ============================================================
# 6. LOAD DIM_DATE
# ============================================================

dates = df["Date"].drop_duplicates().sort_values()

for date in dates:

    date_id = int(date.strftime("%Y%m%d"))
    day = date.day
    month = date.month
    month_name = date.strftime("%B")
    quarter = (date.month - 1) // 3 + 1
    year = date.year

    cursor.execute("""
        INSERT IGNORE INTO dim_date
        (date_id, full_date, day, month, month_name, quarter, year)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        date_id,
        date.date(),
        day,
        month,
        month_name,
        quarter,
        year
    ))


print("dim_date loaded.")


# ============================================================
# 7. LOAD DIM_CUSTOMER
# ============================================================

customer_columns = [
    "Customer_Name",
    "Gender",
    "Annual_Income",
    "Phone"
]

customers = df[customer_columns].drop_duplicates()

for _, row in customers.iterrows():

    cursor.execute("""
        INSERT INTO dim_customer
        (customer_name, gender, annual_income, phone)
        VALUES (%s, %s, %s, %s)
    """, (
        row["Customer_Name"],
        row["Gender"],
        row["Annual_Income"],
        row["Phone"]
    ))


print("dim_customer loaded.")


# ============================================================
# 8. LOAD DIM_VEHICLE
# ============================================================

vehicle_columns = [
    "Company",
    "Model",
    "Engine",
    "Transmission",
    "Color",
    "Body_Style"
]

vehicles = df[vehicle_columns].drop_duplicates()

for _, row in vehicles.iterrows():

    cursor.execute("""
        INSERT INTO dim_vehicle
        (company, model, engine, transmission, color, body_style)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row["Company"],
        row["Model"],
        row["Engine"],
        row["Transmission"],
        row["Color"],
        row["Body_Style"]
    ))


print("dim_vehicle loaded.")


# ============================================================
# 9. LOAD DIM_DEALER
# ============================================================

dealer_columns = [
    "Dealer_Name",
    "Dealer_No"
]

dealers = df[dealer_columns].drop_duplicates()

for _, row in dealers.iterrows():

    cursor.execute("""
        INSERT INTO dim_dealer
        (dealer_name, dealer_no)
        VALUES (%s, %s)
    """, (
        row["Dealer_Name"],
        row["Dealer_No"]
    ))


print("dim_dealer loaded.")


# ============================================================
# 10. LOAD DIM_LOCATION
# ============================================================

locations = df[["Dealer_Region"]].drop_duplicates()

for _, row in locations.iterrows():

    cursor.execute("""
        INSERT INTO dim_location
        (dealer_region)
        VALUES (%s)
    """, (
        row["Dealer_Region"],
    ))


print("dim_location loaded.")


# ============================================================
# 11. CREATE LOOKUP DICTIONARIES
# ============================================================

cursor.execute("""
    SELECT customer_id, customer_name, gender, annual_income, phone
    FROM dim_customer
""")

customer_lookup = {}

for row in cursor.fetchall():
    key = (
        row[1],
        row[2],
        float(row[3]),
        str(row[4])
    )
    customer_lookup[key] = row[0]


cursor.execute("""
    SELECT vehicle_id, company, model, engine, transmission, color, body_style
    FROM dim_vehicle
""")

vehicle_lookup = {}

for row in cursor.fetchall():
    key = (
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6]
    )
    vehicle_lookup[key] = row[0]


cursor.execute("""
    SELECT dealer_id, dealer_name, dealer_no
    FROM dim_dealer
""")

dealer_lookup = {}

for row in cursor.fetchall():
    key = (
        row[1],
        row[2]
    )
    dealer_lookup[key] = row[0]


cursor.execute("""
    SELECT location_id, dealer_region
    FROM dim_location
""")

location_lookup = {}

for row in cursor.fetchall():
    location_lookup[row[1]] = row[0]


# ============================================================
# 12. LOAD FACT_SALES
# ============================================================

for _, row in df.iterrows():

    date_id = int(row["Date"].strftime("%Y%m%d"))

    customer_key = (
        row["Customer_Name"],
        row["Gender"],
        float(row["Annual_Income"]),
        str(row["Phone"])
    )

    vehicle_key = (
        row["Company"],
        row["Model"],
        row["Engine"],
        row["Transmission"],
        row["Color"],
        row["Body_Style"]
    )

    dealer_key = (
        row["Dealer_Name"],
        row["Dealer_No"]
    )

    location_key = row["Dealer_Region"]

    customer_id = customer_lookup[customer_key]
    vehicle_id = vehicle_lookup[vehicle_key]
    dealer_id = dealer_lookup[dealer_key]
    location_id = location_lookup[location_key]

    cursor.execute("""
        INSERT INTO fact_sales
        (sale_id, date_id, customer_id, vehicle_id,
         dealer_id, location_id, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["Car_id"],
        date_id,
        customer_id,
        vehicle_id,
        dealer_id,
        location_id,
        row["Price"]
    ))


print("fact_sales loaded.")


# ============================================================
# 13. COMMIT
# ============================================================

connection.commit()

print("\n======================================")
print("ETL PROCESS COMPLETED SUCCESSFULLY")
print("======================================")


# ============================================================
# 14. CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("MySQL connection closed.")