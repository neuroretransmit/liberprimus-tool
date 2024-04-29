CREATE TABLE solution_attempts (
  id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  scheme TEXT NOT NULL,
  key TEXT,
  shift INT,
  max_confidence REAL NOT NULL,
  max_confidence_lang TEXT,
  skips JSONB,
  excludes JSONB,
  CONSTRAINT uniq_solution_attempts UNIQUE (scheme, key, shift, skips, excludes) 
);
