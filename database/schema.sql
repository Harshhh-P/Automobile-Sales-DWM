USE defaultdb;

-- =========================================
-- DIMENSION: DATE
-- =========================================

CREATE TABLE IF NOT EXISTS dim_date (
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

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    gender VARCHAR(20),
    annual_income DECIMAL(15,2),
    phone VARCHAR(30)
);


-- =========================================
-- DIMENSION: VEHICLE
-- =========================================

CREATE TABLE IF NOT EXISTS dim_vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    company VARCHAR(100),
    model VARCHAR(100),
    engine VARCHAR(100),
    transmission VARCHAR(50),
    color VARCHAR(50),
    body_style VARCHAR(50)
);


-- =========================================
-- DIMENSION: DEALER
-- =========================================

CREATE TABLE IF NOT EXISTS dim_dealer (
    dealer_id INT AUTO_INCREMENT PRIMARY KEY,
    dealer_no VARCHAR(50),
    dealer_name VARCHAR(150)
);


-- =========================================
-- DIMENSION: LOCATION
-- =========================================

CREATE TABLE IF NOT EXISTS dim_location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    dealer_region VARCHAR(100)
);


-- =========================================
-- FACT: SALES
-- =========================================

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,

    date_id INT,
    customer_id INT,
    vehicle_id INT,
    dealer_id INT,
    location_id INT,

    price DECIMAL(15,2),

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