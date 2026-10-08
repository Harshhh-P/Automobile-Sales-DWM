import pandas as pd
from db_connection import get_connection


CSV_PATH = "data/raw/car_data.csv"


def load_data():
    connection = None
    cursor = None

    try:
        # -----------------------------------------
        # 1. Read CSV
        # -----------------------------------------
        print("Reading automobile sales dataset...")

        df = pd.read_csv(CSV_PATH)

        print(f"Rows found: {len(df)}")

        # -----------------------------------------
        # 2. Basic cleaning
        # -----------------------------------------
        df.columns = df.columns.str.strip()

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Clean text columns
        text_columns = [
            "Customer Name",
            "Gender",
            "Dealer_Name",
            "Company",
            "Model",
            "Engine",
            "Transmission",
            "Color",
            "Dealer_No",
            "Body Style",
            "Phone",
            "Dealer_Region"
        ]

        for column in text_columns:
            df[column] = df[column].fillna("").astype(str).str.strip()

        # Convert numeric columns
        df["Annual Income"] = pd.to_numeric(
            df["Annual Income"],
            errors="coerce"
        ).fillna(0)

        df["Price ($)"] = pd.to_numeric(
            df["Price ($)"],
            errors="coerce"
        ).fillna(0)

        # Convert date
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        # Remove rows with invalid dates
        df = df.dropna(subset=["Date"])

        print(f"Rows after cleaning: {len(df)}")

        # -----------------------------------------
        # 3. Connect to Aiven
        # -----------------------------------------
        connection = get_connection()
        cursor = connection.cursor()

        print("Connected to Aiven MySQL.")

        # -----------------------------------------
        # 4. Clear existing warehouse data
        # -----------------------------------------
        print("Clearing existing warehouse data...")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        cursor.execute("TRUNCATE TABLE fact_sales")
        cursor.execute("TRUNCATE TABLE dim_date")
        cursor.execute("TRUNCATE TABLE dim_customer")
        cursor.execute("TRUNCATE TABLE dim_vehicle")
        cursor.execute("TRUNCATE TABLE dim_dealer")
        cursor.execute("TRUNCATE TABLE dim_location")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        # -----------------------------------------
        # 5. DIM_DATE
        # -----------------------------------------
        print("Loading dim_date...")

        dates = df["Date"].drop_duplicates().sort_values()

        date_records = []

        for date in dates:
            date_id = int(date.strftime("%Y%m%d"))

            date_records.append((
                date_id,
                date.date(),
                date.day,
                date.month,
                date.strftime("%B"),
                ((date.month - 1) // 3) + 1,
                date.year
            ))

        cursor.executemany(
            """
            INSERT INTO dim_date
            (
                date_id,
                full_date,
                day,
                month,
                month_name,
                quarter,
                year
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            date_records
        )

        # -----------------------------------------
        # 6. DIM_CUSTOMER
        # -----------------------------------------
        print("Loading dim_customer...")

        customers = df[
            [
                "Customer Name",
                "Gender",
                "Annual Income",
                "Phone"
            ]
        ].drop_duplicates()

        customer_records = [
            (
                row["Customer Name"],
                row["Gender"],
                float(row["Annual Income"]),
                row["Phone"]
            )
            for _, row in customers.iterrows()
        ]

        cursor.executemany(
            """
            INSERT INTO dim_customer
            (
                customer_name,
                gender,
                annual_income,
                phone
            )
            VALUES (%s, %s, %s, %s)
            """,
            customer_records
        )

        # -----------------------------------------
        # 7. DIM_VEHICLE
        # -----------------------------------------
        print("Loading dim_vehicle...")

        vehicles = df[
            [
                "Company",
                "Model",
                "Engine",
                "Transmission",
                "Color",
                "Body Style"
            ]
        ].drop_duplicates()

        vehicle_records = [
            (
                row["Company"],
                row["Model"],
                row["Engine"],
                row["Transmission"],
                row["Color"],
                row["Body Style"]
            )
            for _, row in vehicles.iterrows()
        ]

        cursor.executemany(
            """
            INSERT INTO dim_vehicle
            (
                company,
                model,
                engine,
                transmission,
                color,
                body_style
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            vehicle_records
        )

        # -----------------------------------------
        # 8. DIM_DEALER
        # -----------------------------------------
        print("Loading dim_dealer...")

        dealers = df[
            [
                "Dealer_No",
                "Dealer_Name"
            ]
        ].drop_duplicates()

        dealer_records = [
            (
                row["Dealer_No"],
                row["Dealer_Name"]
            )
            for _, row in dealers.iterrows()
        ]

        cursor.executemany(
            """
            INSERT INTO dim_dealer
            (
                dealer_no,
                dealer_name
            )
            VALUES (%s, %s)
            """,
            dealer_records
        )

        # -----------------------------------------
        # 9. DIM_LOCATION
        # -----------------------------------------
        print("Loading dim_location...")

        locations = df[
            ["Dealer_Region"]
        ].drop_duplicates()

        location_records = [
            (row["Dealer_Region"],)
            for _, row in locations.iterrows()
        ]

        cursor.executemany(
            """
            INSERT INTO dim_location
            (
                dealer_region
            )
            VALUES (%s)
            """,
            location_records
        )

        # -----------------------------------------
        # 10. Create lookup dictionaries
        # -----------------------------------------

        cursor.execute("""
            SELECT date_id, full_date
            FROM dim_date
        """)

        date_lookup = {
            row[1]: row[0]
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT
                customer_id,
                customer_name,
                gender,
                annual_income,
                phone
            FROM dim_customer
        """)

        customer_lookup = {
            (
                row[1],
                row[2],
                float(row[3]),
                row[4]
            ): row[0]
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT
                vehicle_id,
                company,
                model,
                engine,
                transmission,
                color,
                body_style
            FROM dim_vehicle
        """)

        vehicle_lookup = {
            (
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            ): row[0]
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT
                dealer_id,
                dealer_no,
                dealer_name
            FROM dim_dealer
        """)

        dealer_lookup = {
            (
                row[1],
                row[2]
            ): row[0]
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT
                location_id,
                dealer_region
            FROM dim_location
        """)

        location_lookup = {
            row[1]: row[0]
            for row in cursor.fetchall()
        }

        # -----------------------------------------
        # 11. FACT_SALES
        # -----------------------------------------
        print("Loading fact_sales...")

        sales_records = []

        for _, row in df.iterrows():

            date_id = date_lookup[row["Date"].date()]

            customer_key = (
                row["Customer Name"],
                row["Gender"],
                float(row["Annual Income"]),
                row["Phone"]
            )

            vehicle_key = (
                row["Company"],
                row["Model"],
                row["Engine"],
                row["Transmission"],
                row["Color"],
                row["Body Style"]
            )

            dealer_key = (
                row["Dealer_No"],
                row["Dealer_Name"]
            )

            location_key = row["Dealer_Region"]

            customer_id = customer_lookup[customer_key]
            vehicle_id = vehicle_lookup[vehicle_key]
            dealer_id = dealer_lookup[dealer_key]
            location_id = location_lookup[location_key]

            sales_records.append((
                date_id,
                customer_id,
                vehicle_id,
                dealer_id,
                location_id,
                float(row["Price ($)"])
            ))

        cursor.executemany(
            """
            INSERT INTO fact_sales
            (
                date_id,
                customer_id,
                vehicle_id,
                dealer_id,
                location_id,
                price
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            sales_records
        )

        # -----------------------------------------
        # 12. Commit
        # -----------------------------------------
        connection.commit()

        print("\n========================================")
        print("ETL COMPLETED SUCCESSFULLY!")
        print("========================================")
        print(f"Date records     : {len(date_records)}")
        print(f"Customer records : {len(customer_records)}")
        print(f"Vehicle records  : {len(vehicle_records)}")
        print(f"Dealer records   : {len(dealer_records)}")
        print(f"Location records : {len(location_records)}")
        print(f"Sales records    : {len(sales_records)}")
        print("========================================")

    except Exception as error:
        if connection:
            connection.rollback()

        print("\nETL FAILED!")
        print("Error:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    load_data()