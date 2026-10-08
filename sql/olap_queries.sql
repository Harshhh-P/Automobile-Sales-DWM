USE automobile_sales_dwm;


-- ============================================================
-- 1. TOTAL SALES
-- ============================================================

SELECT
    COUNT(*) AS total_sales,
    SUM(price) AS total_revenue,
    AVG(price) AS average_sale_price
FROM fact_sales;


-- ============================================================
-- 2. ROLL-UP
-- Monthly Sales
-- ============================================================

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


-- ============================================================
-- 3. ROLL-UP
-- Yearly Sales
-- ============================================================

SELECT
    d.year,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year;


-- ============================================================
-- 4. DRILL-DOWN
-- Year → Quarter → Month
-- ============================================================

SELECT
    d.year,
    d.quarter,
    d.month,
    d.month_name,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.quarter,
    d.month;


-- ============================================================
-- 5. SLICE
-- Sales for one company
-- ============================================================

SELECT
    v.company,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_price
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
WHERE v.company = 'Ford'
GROUP BY v.company;


-- ============================================================
-- 6. DICE
-- Company + Region + Transmission
-- ============================================================

SELECT
    v.company,
    l.dealer_region,
    v.transmission,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
JOIN dim_location l
    ON f.location_id = l.location_id
WHERE v.company IN ('Ford', 'Toyota', 'BMW')
  AND l.dealer_region IN ('Middletown', 'Aurora', 'Greenville')
  AND v.transmission IN ('Automatic', 'Manual')
GROUP BY
    v.company,
    l.dealer_region,
    v.transmission
ORDER BY total_revenue DESC;


-- ============================================================
-- 7. COMPANY-WISE SALES
-- ============================================================

SELECT
    v.company,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue,
    AVG(f.price) AS average_price
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY v.company
ORDER BY total_revenue DESC;


-- ============================================================
-- 8. REGION-WISE SALES
-- ============================================================

SELECT
    l.dealer_region,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.dealer_region
ORDER BY total_revenue DESC;


-- ============================================================
-- 9. BODY STYLE-WISE SALES
-- ============================================================

SELECT
    v.body_style,
    COUNT(f.sale_id) AS total_sales,
    SUM(f.price) AS total_revenue
FROM fact_sales f
JOIN dim_vehicle v
    ON f.vehicle_id = v.vehicle_id
GROUP BY v.body_style
ORDER BY total_sales DESC;