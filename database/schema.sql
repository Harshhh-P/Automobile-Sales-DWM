CREATE DATABASE IF NOT EXISTS automobile_sales_dwm;

USE automobile_sales_dwm;

-- =========================================
-- DIMENSION: DATE
-- =========================================

CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT
);

-- =========================================
-- DIMENSION: CUSTOMER
-- =========================================

CREATE TABLE dim_customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(20),
    annual_income DECIMAL(15,2),
    phone VARCHAR(30)
);

-- =========================================
-- DIMENSION: VEHICLE
-- =========================================

CREATE TABLE dim_vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(100),
    model VARCHAR(100),
    engine VARCHAR(150),
    transmission VARCHAR(50),
    color VARCHAR(50),
    body_style VARCHAR(50)
);

-- =========================================
-- DIMENSION: DEALER
-- =========================================

CREATE TABLE dim_dealer (
    dealer_id INT AUTO_INCREMENT PRIMARY KEY,
    dealer_name VARCHAR(150),
    dealer_no VARCHAR(50)
);

-- =========================================
-- DIMENSION: LOCATION
-- =========================================

CREATE TABLE dim_location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    dealer_region VARCHAR(100)
);

-- =========================================
-- FACT TABLE: SALES
-- =========================================

CREATE TABLE fact_sales (
    sale_id VARCHAR(50) PRIMARY KEY,
    date_id INT NOT NULL,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    dealer_id INT NOT NULL,
    location_id INT NOT NULL,
    price DECIMAL(15,2) NOT NULL,

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customer(customer_id),

    FOREIGN KEY (vehicle_id)
        REFERENCES dim_vehicle(vehicle_id),

    FOREIGN KEY (dealer_id)
        REFERENCES dim_dealer(dealer_id),

    FOREIGN KEY (location_id)
        REFERENCES dim_location(location_id)
);