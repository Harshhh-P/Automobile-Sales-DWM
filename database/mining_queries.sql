USE defaultdb;

-- =========================================================
-- AUTOMOBILE SALES DATA WAREHOUSE
-- DATA MINING / ANALYTICS QUERIES
-- =========================================================


-- =========================================================
-- 1. TOP 10 SELLING CAR MODELS
-- =========================================================

SELECT
    dv.company,
    dv.model,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company,
    dv.model
ORDER BY
    total_sales DESC
LIMIT 10;


-- =========================================================
-- 2. TOP AUTOMOBILE COMPANIES BY SALES
-- =========================================================

SELECT
    dv.company,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company
ORDER BY
    total_sales DESC;


-- =========================================================
-- 3. REVENUE BY AUTOMOBILE COMPANY
-- =========================================================

SELECT
    dv.company,
    SUM(fs.price) AS total_revenue
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company
ORDER BY
    total_revenue DESC;


-- =========================================================
-- 4. AVERAGE VEHICLE PRICE BY COMPANY
-- =========================================================

SELECT
    dv.company,
    ROUND(AVG(fs.price), 2) AS average_price
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company
ORDER BY
    average_price DESC;


-- =========================================================
-- 5. SALES BY DEALER
-- =========================================================

SELECT
    dd.dealer_name,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_dealer dd
    ON fs.dealer_id = dd.dealer_id
GROUP BY
    dd.dealer_name
ORDER BY
    total_sales DESC;


-- =========================================================
-- 6. REVENUE BY DEALER
-- =========================================================

SELECT
    dd.dealer_name,
    SUM(fs.price) AS total_revenue
FROM fact_sales fs
JOIN dim_dealer dd
    ON fs.dealer_id = dd.dealer_id
GROUP BY
    dd.dealer_name
ORDER BY
    total_revenue DESC;


-- =========================================================
-- 7. SALES BY REGION
-- =========================================================

SELECT
    dl.dealer_region,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_location dl
    ON fs.location_id = dl.location_id
GROUP BY
    dl.dealer_region
ORDER BY
    total_sales DESC;


-- =========================================================
-- 8. REVENUE BY REGION
-- =========================================================

SELECT
    dl.dealer_region,
    SUM(fs.price) AS total_revenue
FROM fact_sales fs
JOIN dim_location dl
    ON fs.location_id = dl.location_id
GROUP BY
    dl.dealer_region
ORDER BY
    total_revenue DESC;


-- =========================================================
-- 9. SALES BY BODY STYLE
-- =========================================================

SELECT
    dv.body_style,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.body_style
ORDER BY
    total_sales DESC;


-- =========================================================
-- 10. REVENUE BY BODY STYLE
-- =========================================================

SELECT
    dv.body_style,
    SUM(fs.price) AS total_revenue
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.body_style
ORDER BY
    total_revenue DESC;


-- =========================================================
-- 11. MANUAL VS AUTOMATIC TRANSMISSION
-- =========================================================

SELECT
    dv.transmission,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.transmission
ORDER BY
    total_sales DESC;


-- =========================================================
-- 12. SALES BY GENDER
-- =========================================================

SELECT
    dc.gender,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_customer dc
    ON fs.customer_id = dc.customer_id
GROUP BY
    dc.gender
ORDER BY
    total_sales DESC;


-- =========================================================
-- 13. AVERAGE ANNUAL INCOME OF CUSTOMERS
-- =========================================================

SELECT
    ROUND(AVG(dc.annual_income), 2) AS average_annual_income
FROM dim_customer dc;


-- =========================================================
-- 14. SALES BY YEAR
-- =========================================================

SELECT
    dd.year,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_date dd
    ON fs.date_id = dd.date_id
GROUP BY
    dd.year
ORDER BY
    dd.year;


-- =========================================================
-- 15. SALES BY MONTH
-- =========================================================

SELECT
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_date dd
    ON fs.date_id = dd.date_id
GROUP BY
    dd.year,
    dd.month,
    dd.month_name
ORDER BY
    dd.year,
    dd.month;


-- =========================================================
-- 16. REVENUE BY YEAR
-- =========================================================

SELECT
    dd.year,
    SUM(fs.price) AS total_revenue
FROM fact_sales fs
JOIN dim_date dd
    ON fs.date_id = dd.date_id
GROUP BY
    dd.year
ORDER BY
    dd.year;


-- =========================================================
-- 17. QUARTERLY SALES
-- =========================================================

SELECT
    dd.year,
    dd.quarter,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_date dd
    ON fs.date_id = dd.date_id
GROUP BY
    dd.year,
    dd.quarter
ORDER BY
    dd.year,
    dd.quarter;


-- =========================================================
-- 18. TOP 10 MOST EXPENSIVE VEHICLE SALES
-- =========================================================

SELECT
    dv.company,
    dv.model,
    fs.price
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
ORDER BY
    fs.price DESC
LIMIT 10;


-- =========================================================
-- 19. LOWEST 10 VEHICLE SALES PRICES
-- =========================================================

SELECT
    dv.company,
    dv.model,
    fs.price
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
ORDER BY
    fs.price ASC
LIMIT 10;


-- =========================================================
-- 20. TOP COMPANIES BY AVERAGE SALES PRICE
-- =========================================================

SELECT
    dv.company,
    ROUND(AVG(fs.price), 2) AS average_sales_price,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company
HAVING
    COUNT(fs.sale_id) >= 10
ORDER BY
    average_sales_price DESC;


-- =========================================================
-- 21. TOP CUSTOMERS BY NUMBER OF PURCHASES
-- =========================================================

SELECT
    dc.customer_name,
    COUNT(fs.sale_id) AS purchases
FROM fact_sales fs
JOIN dim_customer dc
    ON fs.customer_id = dc.customer_id
GROUP BY
    dc.customer_id,
    dc.customer_name
ORDER BY
    purchases DESC
LIMIT 10;


-- =========================================================
-- 22. CUSTOMER SPENDING
-- =========================================================

SELECT
    dc.customer_name,
    SUM(fs.price) AS total_spending
FROM fact_sales fs
JOIN dim_customer dc
    ON fs.customer_id = dc.customer_id
GROUP BY
    dc.customer_id,
    dc.customer_name
ORDER BY
    total_spending DESC
LIMIT 10;


-- =========================================================
-- 23. COMPANY + BODY STYLE ANALYSIS
-- =========================================================

SELECT
    dv.company,
    dv.body_style,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company,
    dv.body_style
ORDER BY
    total_sales DESC;


-- =========================================================
-- 24. COMPANY + TRANSMISSION ANALYSIS
-- =========================================================

SELECT
    dv.company,
    dv.transmission,
    COUNT(fs.sale_id) AS total_sales
FROM fact_sales fs
JOIN dim_vehicle dv
    ON fs.vehicle_id = dv.vehicle_id
GROUP BY
    dv.company,
    dv.transmission
ORDER BY
    total_sales DESC;


-- =========================================================
-- 25. COMPLETE SALES SUMMARY
-- =========================================================

SELECT
    COUNT(fs.sale_id) AS total_sales,
    ROUND(SUM(fs.price), 2) AS total_revenue,
    ROUND(AVG(fs.price), 2) AS average_price,
    MIN(fs.price) AS minimum_price,
    MAX(fs.price) AS maximum_price
FROM fact_sales fs;