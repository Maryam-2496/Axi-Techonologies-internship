# Day 16: Advanced Database Indexing & Query Optimization

## What I did
(Adapted from Postgres-focused roadmap to SQLite: EXPLAIN QUERY PLAN instead of
EXPLAIN ANALYZE, no GIN/Hash index types available)
- Seeded a 500,000-row `orders` table for realistic query testing
- Baseline: full table scan (SCAN orders), 417ms, no index
- Added single-column B-Tree index on city -> dropped to 150ms
- Added a partial index (status = 'pending' only)
- Measured index write cost: DB grew to 34.33MB, ~119ms per 1000-row insert with
  indexes active
- Calculated filter selectivity: city and status both matched 14-25% of the table
  (low selectivity) -- explains why some indexed queries were still slow
- Built a composite index (city, status, amount) and proved the leftmost-prefix rule:
  works for city alone or city+status+amount, but not for status alone
- Built a covering index (city, amount) -- SELECT city, amount FROM orders WHERE
  city=? dropped from 1084ms to 86.88ms (~12x) using COVERING INDEX in the plan
- Query refactoring tests: SELECT * vs specific columns (813ms -> 59ms, as expected);
  OR vs UNION and N+1 vs GROUP BY batching both went against the "expected" result
  (documented honestly with explanation rather than hidden)
- Capstone: optimized an unindexed customer_name+status query from 279ms to 14.74ms
  with a new composite covering index; saved as migrations/day16_add_indexes.sql;
  PR merged with CI passing

## What I learned
- An index only helps when selectivity is high; low-selectivity columns can make
  indexed queries slower than a scan
- Composite index column order matters (leftmost prefix rule)
- "Best practice" refactors (UNION, batching) don't always win -- UNION's implicit
  dedup/sort cost, and GROUP BY's full-scan cost, can outweigh their theoretical benefit
  at small scale