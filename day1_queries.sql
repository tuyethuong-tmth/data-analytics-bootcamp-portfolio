-- create customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    signup_date DATE,
    country TEXT,
    total_spent DECIMAL(10,2)
);

INSERT INTO customers (customer_id, name, email, signup_date, country, total_spent)
VALUES
(1, 'Nguyen Van A', 'a@email.com', '2023-01-15', 'Vietnam', 1250.00),
(2, 'Tran Thi B', 'b@email.com', '2023-02-20', 'Vietnam', 890.50),
(3, 'John Smith', 'john@email.com', '2023-03-10', 'USA', 3200.00),
(4, 'Le Van C', 'c@email.com', '2023-04-05', 'Vietnam', 450.00),
(5, 'Maria Garcia', 'maria@email.com', '2023-05-12', 'Spain', 2100.75),
(6, 'Pham Thi D', 'd@email.com', '2023-06-18', 'Vietnam', 75.00),
(7, 'David Lee', 'david@email.com', '2023-07-22', 'Korea', 1800.00),
(8, 'Hoang Van E', 'e@email.com', '2023-08-30', 'Vietnam', 980.25);

-- #1. List all customers from Vietnam, sorted by total spent
SELECT * FROM customers c WHERE country = 'Vietnam' ORDER BY total_spent DESC;

-- #2. Find all customers who have spent more than \$1,000, regardless of country
SELECT * FROM customers c WHERE total_spent > 1000 ORDER BY total_spent DESC;

-- #3. Find all customers whose email ends in "@email.com" AND who signed up after March 2023
SELECT * FROM customers c WHERE email LIKE '%@email.com' AND signup_date >'2023-03-01';

-- #4. Find all customers who spent between $500 and $1,500
SELECT * FROM customers c WHERE total_spent BETWEEN 500 AND 1500;

-- #5. Find all customers from Vietnam OR Korea who have spent more than $800, sorted by total spent descending
SELECT * FROM customers c WHERE country IN ('Vietnam','Korea') AND total_spent >800 ORDER BY total_spent DESC;

