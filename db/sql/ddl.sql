-- Optimizations for inserting things extremely fast

-- No transaction journal
PRAGMA journal_mode = OFF;
-- Asynchronous
PRAGMA synchronous = 0;
-- Specify cache size
PRAGMA cache_size = 100000;
-- Modify locks
PRAGMA locking_mode = EXCLUSIVE;
-- In-memory temp storet
PRAGMA temp_store = MEMORY;

CREATE TABLE solution_attempts (
  id INT PRIMARY KEY,
  scheme TEXT NOT NULL,
  key TEXT,
  shift INT,
  max_confidence REAL NOT NULL,
  max_confidence_lang TEXT,
  skips JSON NOT NULL,
  excludes JSON NOT NULL,
  UNIQUE(scheme, key, shift, skips, excludes) ON CONFLICT IGNORE
);
