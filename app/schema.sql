DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    user_id INT PRIMARY KEY, 
    signup_time TIMESTAMP NOT NULL,
    purchase_time TIMESTAMP NOT NULL, 
    purchase_value FLOAT NOT NULL,
    device_id VARCHAR NOT NULL,
    source VARCHAR NOT NULL, 
    browser VARCHAR NOT NULL, 
    sex VARCHAR NOT NULL, 
    age INT NOT NULL, 
    ip_address FLOAT NOT NULL, 
    lower_bound_ip_address FLOAT NOT NULL, 
    upper_bound_ip_address FLOAT NOT NULL, 
    country VARCHAR NOT NULL 

DROP TABLE IF EXISTS features;

CREATE TABLE features (
    user_id SERIAL PRIMARY KEY,
    signup_time TIMESTAMP,
    purchase_time TIMESTAMP,
    purchase_value FLOAT,
    device_id VARCHAR,
    source VARCHAR,
    browser VARCHAR,
    sex VARCHAR,
    age INTEGER,
    ip_address VARCHAR,
    class INTEGER,
    lower_bound_ip_address BIGINT,
    upper_bound_ip_address BIGINT,
    country VARCHAR
);
