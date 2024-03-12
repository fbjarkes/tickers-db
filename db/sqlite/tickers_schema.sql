CREATE TABLE IF NOT EXISTS staging_nasdaq (
  symbol TEXT PRIMARY KEY,
  company_name TEXT
);

CREATE TABLE IF NOT EXISTS staging_other (
  symbol TEXT PRIMARY KEY,
  company_name TEXT
);

CREATE TABLE IF NOT EXISTS tickers (
  symbol TEXT PRIMARY KEY,
  company_name TEXT
);

