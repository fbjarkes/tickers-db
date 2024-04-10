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
  llm TEXT,
  date TEXT,
  FOREIGN KEY (news_id) REFERENCES news (id)
);