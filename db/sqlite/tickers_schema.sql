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
  description TEXT
);

CREATE TABLE IF NOT EXISTS themes (
  symbol TEXT PRIMARY KEY,  
  theme
);

CREATE TABLE IF NOT EXISTS shares_float_history (
  symbol TEXT PRIMARY KEY,
  shares_float REAL,
  date TEXT,
);

CREATE TABLE IF NOT EXISTS news (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  symbol TEXT,
  date TEXT,
  condition TEXT,
  crawler TEXT,
  url TEXT,
  text TEXT
);

CREATE TABLE IF NOT EXISTS catalyst (
  symbol TEXT PRIMARY KEY,
  news_id INTEGER,
  FOREIGN KEY (news_id) REFERENCES news (id)
  llm TEXT,
  date TEXT
);