DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    user_id INT PRIMARY KEY, -- user_id as the unique identifier
    signup_time TIMESTAMP NOT NULL, -- Signup time as timestamp
    purchase_time TIMESTAMP NOT NULL, -- Purchase time as timestamp
    purchase_value FLOAT NOT NULL, -- Purchase value as a float
    device_id VARCHAR NOT NULL, -- Device ID as a string
    source VARCHAR NOT NULL, -- Source as a string (e.g., app, web)
    browser VARCHAR NOT NULL, -- Browser as a string
    sex VARCHAR NOT NULL, -- Sex as a string
    age INT NOT NULL, -- Age as integer
    ip_address FLOAT NOT NULL, -- IP address as a float
    lower_bound_ip_address FLOAT NOT NULL, -- Lower bound of IP address
    upper_bound_ip_address FLOAT NOT NULL, -- Upper bound of IP address
    country VARCHAR NOT NULL -- Country as a string
);
