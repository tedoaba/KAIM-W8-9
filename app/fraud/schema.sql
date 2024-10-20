DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    TransactionID SERIAL PRIMARY KEY,
    FraudIndicator BOOLEAN NOT NULL,
    Category VARCHAR NOT NULL,
    TransactionAmount FLOAT NOT NULL,
    AnomalyScore FLOAT NOT NULL,
    Timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    MerchantID INT NOT NULL,
    Amount FLOAT NOT NULL,
    CustomerID INT NOT NULL,
    Name VARCHAR NOT NULL,
    Age INT NOT NULL,
    Address TEXT NOT NULL,
    AccountBalance FLOAT NOT NULL,
    LastLogin TIMESTAMP NOT NULL,
    SuspiciousFlag BOOLEAN NOT NULL
);
