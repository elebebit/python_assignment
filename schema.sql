CREATE TABLE IF NOT EXISTS financial_data (
      id SERIAL PRIMARY KEY,
      symbol VARCHAR(255) NOT NULL,
      date DATE NOT NULL,
      open_price DECIMAL(10,2) DEFAULT NULL,
      close_price DECIMAL(10,2) DEFAULT NULL,
      volume INTEGER DEFAULT NULL
);