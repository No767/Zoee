CREATE TABLE IF NOT EXISTS guild (
  id BIGINT PRIMARY KEY,
  antispam BOOLEAN DEFAULT FALSE,
  prefixes TEXT[],
);


