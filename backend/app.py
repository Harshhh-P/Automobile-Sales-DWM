from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# MYSQL DATABASE CONFIGURATION
# ============================================================

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import get_connection

def execute_query(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# HOME / HEALTH
# ============================================================

@app.route("/")
def home():
    return jsonify({
        "project": "Automobile Sales Data Warehouse and Mining System",
        "status": "Backend API is running",
        "modules": [
            "Dashboard",
            "OLAP",
            "Vehicles",
            "Dealers",
            "Regions",
            "Data Mining"
        ]
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "database": "MySQL"
    })


# ============================================================
# DASHBOARD - SUMMARY
# ============================================================

@app.route("/api/dashboard/summary")
def dashboard_summary():

    query = """
        SELECT
            COUNT(*) AS total_sales,
            COALESCE(SUM(price), 0) AS total_revenue,
            COALESCE(AVG(price), 0) AS average_sale
        FROM fact_sales
    """

    result = execute_query(query)

    return jsonify(result[0])


# ============================================================
# DASHBOARD - COMPANY COUNT
# ============================================================

@app.route("/api/dashboard/company-count")
def dashboard_company_count():

    query = """
        SELECT
            COUNT(DISTINCT company) AS total_companies
        FROM dim_vehicle
    """

    result = execute_query(query)

    return jsonify(result[0])


# ============================================================
# DASHBOARD - DEALER COUNT
# ============================================================

@app.route("/api/dashboard/dealer-count")
def dashboard_dealer_count():

    query = """
        SELECT
            COUNT(*) AS total_dealers
        FROM dim_dealer
    """

    result = execute_query(query)

    return jsonify(result[0])


# ============================================================
# DASHBOARD - YEARLY SALES
# ============================================================

@app.route("/api/dashboard/yearly-sales")
def yearly_sales():

    query = """
        SELECT
            d.year,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_id = d.date_id
        GROUP BY d.year
        ORDER BY d.year
    """

    return jsonify(execute_query(query))


# ============================================================
# DASHBOARD - MONTHLY SALES
# ============================================================

@app.route("/api/dashboard/monthly-sales")
def monthly_sales():

    query = """
        SELECT
            d.year,
            d.month,
            d.month_name,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_id = d.date_id
        GROUP BY
            d.year,
            d.month,
            d.month_name
        ORDER BY
            d.year,
            d.month
    """

    return jsonify(execute_query(query))


# ============================================================
# DASHBOARD - REGIONS
# ============================================================

@app.route("/api/dashboard/regions")
def dashboard_regions():

    query = """
        SELECT
            l.dealer_region AS region,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_location l
            ON f.location_id = l.location_id
        GROUP BY l.dealer_region
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DASHBOARD - BODY STYLE
# ============================================================

@app.route("/api/dashboard/body-styles")
def dashboard_body_styles():

    query = """
        SELECT
            v.body_style,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.body_style
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DASHBOARD - TRANSMISSION
# ============================================================

@app.route("/api/dashboard/transmission")
def dashboard_transmission():

    query = """
        SELECT
            v.transmission,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.transmission
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DASHBOARD - COMPANIES
# ============================================================

@app.route("/api/dashboard/companies")
def dashboard_companies():

    query = """
        SELECT
            v.company,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue,
            COALESCE(AVG(f.price), 0) AS average_price
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.company
        ORDER BY revenue DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# OLAP - ROLL UP
# ============================================================

@app.route("/api/olap/roll-up")
def olap_roll_up():

    level = request.args.get("level", "year").lower()

    if level == "month":

        query = """
            SELECT
                d.year,
                d.month,
                d.month_name,
                COUNT(f.sale_id) AS sales,
                COALESCE(SUM(f.price), 0) AS revenue
            FROM fact_sales f
            JOIN dim_date d
                ON f.date_id = d.date_id
            GROUP BY
                d.year,
                d.month,
                d.month_name
            ORDER BY
                d.year,
                d.month
        """

    elif level == "quarter":

        query = """
            SELECT
                d.year,
                d.quarter,
                COUNT(f.sale_id) AS sales,
                COALESCE(SUM(f.price), 0) AS revenue
            FROM fact_sales f
            JOIN dim_date d
                ON f.date_id = d.date_id
            GROUP BY
                d.year,
                d.quarter
            ORDER BY
                d.year,
                d.quarter
        """

    else:

        query = """
            SELECT
                d.year,
                COUNT(f.sale_id) AS sales,
                COALESCE(SUM(f.price), 0) AS revenue
            FROM fact_sales f
            JOIN dim_date d
                ON f.date_id = d.date_id
            GROUP BY d.year
            ORDER BY d.year
        """

    return jsonify(execute_query(query))


# ============================================================
# OLAP - DRILL DOWN
# ============================================================

@app.route("/api/olap/drill-down")
def olap_drill_down():

    year = request.args.get("year")

    if year:

        query = """
            SELECT
                d.year,
                d.quarter,
                d.month,
                d.month_name,
                COUNT(f.sale_id) AS sales,
                COALESCE(SUM(f.price), 0) AS revenue
            FROM fact_sales f
            JOIN dim_date d
                ON f.date_id = d.date_id
            WHERE d.year = %s
            GROUP BY
                d.year,
                d.quarter,
                d.month,
                d.month_name
            ORDER BY
                d.quarter,
                d.month
        """

        return jsonify(execute_query(query, (year,)))

    query = """
        SELECT
            d.year,
            d.quarter,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_id = d.date_id
        GROUP BY
            d.year,
            d.quarter
        ORDER BY
            d.year,
            d.quarter
    """

    return jsonify(execute_query(query))


# ============================================================
# OLAP - SLICE
# ============================================================

@app.route("/api/olap/slice")
def olap_slice():

    year = request.args.get("year")

    if not year:
        return jsonify({
            "error": "Please provide year"
        }), 400

    query = """
        SELECT
            d.year,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue,
            COALESCE(AVG(f.price), 0) AS average_sale
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_id = d.date_id
        WHERE d.year = %s
        GROUP BY d.year
    """

    return jsonify(execute_query(query, (year,)))


# ============================================================
# OLAP - DICE
# ============================================================

@app.route("/api/olap/dice")
def olap_dice():

    year = request.args.get("year")
    region = request.args.get("region")
    body_style = request.args.get("body_style")
    company = request.args.get("company")

    conditions = []
    params = []

    if year:
        conditions.append("d.year = %s")
        params.append(year)

    if region:
        conditions.append("l.dealer_region = %s")
        params.append(region)

    if body_style:
        conditions.append("v.body_style = %s")
        params.append(body_style)

    if company:
        conditions.append("v.company = %s")
        params.append(company)

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            d.year,
            l.dealer_region AS region,
            v.company,
            v.body_style,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f

        JOIN dim_date d
            ON f.date_id = d.date_id

        JOIN dim_location l
            ON f.location_id = l.location_id

        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id

        {where_clause}

        GROUP BY
            d.year,
            l.dealer_region,
            v.company,
            v.body_style

        ORDER BY sales DESC
    """

    return jsonify(execute_query(query, tuple(params)))


# ============================================================
# VEHICLE ANALYSIS
# ============================================================

@app.route("/api/vehicles/companies")
def vehicle_companies():

    query = """
        SELECT
            v.company,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue,
            COALESCE(AVG(f.price), 0) AS average_price
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.company
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


@app.route("/api/vehicles/models")
def vehicle_models():

    query = """
        SELECT
            v.company,
            v.model,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY
            v.company,
            v.model
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


@app.route("/api/vehicles/top-models")
def top_models():

    query = """
        SELECT
            v.company,
            v.model,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY
            v.company,
            v.model
        ORDER BY sales DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


@app.route("/api/vehicles/body-style")
def vehicle_body_style():

    query = """
        SELECT
            v.body_style,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.body_style
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


@app.route("/api/vehicles/transmission")
def vehicle_transmission():

    query = """
        SELECT
            v.transmission,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.transmission
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


@app.route("/api/vehicles/colors")
def vehicle_colors():

    query = """
        SELECT
            v.color,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.color
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DEALER ANALYSIS
# ============================================================

@app.route("/api/dealers/performance")
def dealer_performance():

    query = """
        SELECT
            d.dealer_name,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue,
            COALESCE(AVG(f.price), 0) AS average_sale
        FROM fact_sales f
        JOIN dim_dealer d
            ON f.dealer_id = d.dealer_id
        GROUP BY d.dealer_name
        ORDER BY revenue DESC
    """

    return jsonify(execute_query(query))


@app.route("/api/dealers/top")
def top_dealers():

    query = """
        SELECT
            d.dealer_name,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_dealer d
            ON f.dealer_id = d.dealer_id
        GROUP BY d.dealer_name
        ORDER BY revenue DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


# ============================================================
# REGION ANALYSIS
# ============================================================

@app.route("/api/regions/performance")
def region_performance():

    query = """
        SELECT
            l.dealer_region AS region,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue,
            COALESCE(AVG(f.price), 0) AS average_sale
        FROM fact_sales f
        JOIN dim_location l
            ON f.location_id = l.location_id
        GROUP BY l.dealer_region
        ORDER BY revenue DESC
    """

    return jsonify(execute_query(query))


@app.route("/api/regions/company-region")
def company_region():

    query = """
        SELECT
            v.company,
            l.dealer_region AS region,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f

        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id

        JOIN dim_location l
            ON f.location_id = l.location_id

        GROUP BY
            v.company,
            l.dealer_region

        ORDER BY revenue DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - COMPANY
# ============================================================

@app.route("/api/mining/company")
def mining_company():

    query = """
        SELECT
            v.company,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue,
            COALESCE(AVG(f.price), 0) AS average_price
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.company
        ORDER BY revenue DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - MODEL
# ============================================================

@app.route("/api/mining/model")
def mining_model():

    query = """
        SELECT
            v.company,
            v.model,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY
            v.company,
            v.model
        ORDER BY sales DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - DEALER
# ============================================================

@app.route("/api/mining/dealer")
def mining_dealer():

    query = """
        SELECT
            d.dealer_name,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_dealer d
            ON f.dealer_id = d.dealer_id
        GROUP BY d.dealer_name
        ORDER BY revenue DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - REGION
# ============================================================

@app.route("/api/mining/region")
def mining_region():

    query = """
        SELECT
            l.dealer_region AS region,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_location l
            ON f.location_id = l.location_id
        GROUP BY l.dealer_region
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - CUSTOMER GENDER
# ============================================================

@app.route("/api/mining/customer-gender")
def mining_customer_gender():

    query = """
        SELECT
            c.gender,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_customer c
            ON f.customer_id = c.customer_id
        GROUP BY c.gender
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - CUSTOMER INCOME
# ============================================================

@app.route("/api/mining/customer-income")
def mining_customer_income():

    query = """
        SELECT
            CASE
                WHEN c.annual_income < 50000
                    THEN 'Low Income'
                WHEN c.annual_income < 100000
                    THEN 'Medium Income'
                ELSE 'High Income'
            END AS income_group,

            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue

        FROM fact_sales f

        JOIN dim_customer c
            ON f.customer_id = c.customer_id

        GROUP BY income_group
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - VEHICLE COLOR
# ============================================================

@app.route("/api/mining/vehicle-color")
def mining_vehicle_color():

    query = """
        SELECT
            v.color,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.color
        ORDER BY sales DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - TOP COMPANIES
# ============================================================

@app.route("/api/mining/top-companies")
def mining_top_companies():

    query = """
        SELECT
            v.company,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        GROUP BY v.company
        ORDER BY revenue DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - TOP DEALERS
# ============================================================

@app.route("/api/mining/top-dealers")
def mining_top_dealers():

    query = """
        SELECT
            d.dealer_name,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_dealer d
            ON f.dealer_id = d.dealer_id
        GROUP BY d.dealer_name
        ORDER BY revenue DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - YEAR
# ============================================================

@app.route("/api/mining/year")
def mining_year():

    query = """
        SELECT
            d.year,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_id = d.date_id
        GROUP BY d.year
        ORDER BY d.year
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - MONTH
# ============================================================

@app.route("/api/mining/month")
def mining_month():

    query = """
        SELECT
            d.year,
            d.month,
            d.month_name,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f
        JOIN dim_date d
            ON f.date_id = d.date_id
        GROUP BY
            d.year,
            d.month,
            d.month_name
        ORDER BY
            d.year,
            d.month
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - EXPENSIVE VEHICLES
# ============================================================

@app.route("/api/mining/expensive")
def mining_expensive():

    query = """
        SELECT
            v.company,
            v.model,
            f.price
        FROM fact_sales f
        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id
        ORDER BY f.price DESC
        LIMIT 10
    """

    return jsonify(execute_query(query))


# ============================================================
# DATA MINING - COMPANY + REGION
# ============================================================

@app.route("/api/mining/company-region")
def mining_company_region():

    query = """
        SELECT
            v.company,
            l.dealer_region AS region,
            COUNT(f.sale_id) AS sales,
            COALESCE(SUM(f.price), 0) AS revenue
        FROM fact_sales f

        JOIN dim_vehicle v
            ON f.vehicle_id = v.vehicle_id

        JOIN dim_location l
            ON f.location_id = l.location_id

        GROUP BY
            v.company,
            l.dealer_region

        ORDER BY revenue DESC
    """

    return jsonify(execute_query(query))


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )