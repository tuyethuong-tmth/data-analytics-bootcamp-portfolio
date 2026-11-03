-- create orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    product_name TEXT,
    quantity INTEGER,
    order_total DECIMAL(10,2),
    status TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO orders (order_id, customer_id, order_date, product_name, quantity, order_total, status)
VALUES
(101, 1, '2023-02-01', 'Wireless Mouse', 2, 45.00, 'completed'),
(102, 1, '2023-03-15', 'Keyboard', 1, 60.00, 'completed'),
(103, 2, '2023-02-20', 'Monitor', 1, 180.00, 'completed'),
(104, 3, '2023-03-25', 'Laptop Stand', 1, 35.00, 'cancelled'),
(105, 3, '2023-04-10', 'Webcam', 1, 75.00, 'completed'),
(106, 5, '2023-05-20', 'Headphones', 2, 120.00, 'completed'),
(107, 5, '2023-06-01', 'Monitor', 2, 360.00, 'completed'),
(108, 7, '2023-07-25', 'Keyboard', 1, 60.00, 'completed'),
(109, 9, '2023-08-05', 'Mouse Pad', 3, 15.00, 'completed');

-- Aggregate funtions
SELECT c.customer_id, c.name, SUM(o.order_total) AS total_spent
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name
HAVING SUM(o.order_total) > 100
ORDER BY total_spent DESC;

-- ROW_NUMBER(), RANK(), DENSE_RANK()
SELECT
    c.name,
    o.order_total,
    RANK() OVER (ORDER BY o.order_total DESC) AS revenue_rank,
    DENSE_RANK () OVER (ORDER BY o.order_total DESC) AS revenue_dense_rank
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'completed';

-- PARTITION BY — Resetting Calculations per Group
SELECT
    c.country,
    c.name,
    o.order_total,
    RANK() OVER (PARTITION BY c.country ORDER BY o.order_total DESC) AS rank_in_country
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'completed';

-- Running Totals with SUM() OVER()
SELECT
    order_date,
    order_total,
    SUM(order_total) OVER (ORDER BY order_date) AS running_total
FROM orders
WHERE status = 'completed';

-- CTEs (Common Table Expressions)
WITH customer_revenue AS (
    SELECT c.customer_id, c.name, SUM(o.order_total) AS total_spent
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.name
)
SELECT *
FROM customer_revenue
WHERE total_spent > 100
ORDER BY total_spent DESC;

-- Handling NULLs with COALESCE
SELECT name, COALESCE(email, 'no email provided') AS email
FROM customers;

-- TRIM, UPPER, LOWER — Cleaning Text
SELECT DISTINCT TRIM(LOWER(country)) AS clean_country
FROM customers;

-- Find duplicate rows based on email
SELECT email, COUNT(*) AS occurrences
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;

-- CASE WHEN — Conditional Logic
SELECT
    name,
    total_spent,
    CASE
        WHEN total_spent > 2000 THEN 'VIP'
        WHEN total_spent BETWEEN 500 AND 2000 THEN 'Regular'
        ELSE 'New'
    END AS customer_segment
FROM customers;

-- Data Type Casting
SELECT name, CAST(total_spent AS INTEGER) AS total_spent_rounded
FROM customers;

-- #1. List all customers with their orders, including customers with no orders
SELECT c.customer_id, c.name, o.order_id, o.product_name, o.order_total
FROM customers c 
LEFT JOIN orders o ON c.customer_id =o.customer_id;

-- #2. Find each customer's rank by total spending (completed orders only), using `RANK()`
SELECT c.name, SUM(o.order_total) AS total_spending, RANK() OVER (ORDER BY sum(o.order_total) DESC) AS spending_rank
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id 
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name;

-- #3. Using a CTE, find the total revenue per country, then filter to only countries with revenue above $100
WITH country_revenue AS (
SELECT country, sum(order_total) AS total_revenue
FROM orders o
INNER JOIN customers c ON c.customer_id = o.customer_id 
WHERE o.status = 'completed'
GROUP BY 1
)
SELECT *
FROM country_revenue
WHERE total_revenue > 100;

-- #4. Clean the `country` column (trim whitespace, standardize casing) and count customers per cleaned country value
SELECT TRIM(LOWER(country)) AS cleaned_country, count(*) AS n_customers
FROM customers c 
GROUP BY 1;

-- #5. Calculate a running total of revenue by `order_date`, and label each customer as 'VIP' (>$200 total) or 'Regular' using `CASE WHEN`
SELECT order_date, c.customer_id, c.name, o.order_total,
sum(o.order_total) over(ORDER BY order_date ASC) AS running_total,
CASE WHEN sum(o.order_total) over(PARTITION BY c.customer_id) > 200 THEN 'VIP' ELSE 'Regular' END AS 
FROM customers c 
INNER JOIN orders o ON c.customer_id = o.customer_id 
WHERE o.status ='completed';


