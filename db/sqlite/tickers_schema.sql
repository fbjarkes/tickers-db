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
  --catalyst_type_id INTEGER,
  catalyst_type TEXT CHECK(catalyst_type IN ('NEWS', 'ER', 'UPGRADE', 'DOWNGRADE')),
  FOREIGN KEY (news_id) REFERENCES news (id),
  --FOREIGN KEY (catalyst_type_id) REFERENCES catalyst_types (id),
  llm TEXT,
  date TEXT
);

-- CREATE TABLE IF NOT EXISTS catalyst_types (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   type TEXT
-- );


-- TODO: specific earnings table? with surprise %, EPS, etc
-- TODO: specific upgrade/downgrade table? If lots of entries, could be better if the reason for upgrade/downgrade is irrelevant