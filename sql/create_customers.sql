CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(254) NOT NULL,
    country VARCHAR(100),
    signup_date DATE NOT NULL,
    total_spend DECIMAL(10, 2) NOT NULL CHECK (total_spend >= 0)
);