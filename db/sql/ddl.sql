CREATE TABLE solution_attempts (
  id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  section TEXT NOT NULL,
  nums JSONB NOT NULL,
  scheme TEXT NOT NULL,
  key TEXT,
  shift INT,
  max_confidence REAL NOT NULL,
  max_confidence_lang TEXT,
  skips JSONB,
  excludes JSONB,
  CONSTRAINT uniq_solution_attempts UNIQUE NULLS NOT DISTINCT (section, nums, scheme, key, shift, skips, excludes)
);
