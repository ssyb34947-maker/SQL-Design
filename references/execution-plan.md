# Execution Plan Analysis

## Reading Order

1. Confirm the database engine and plan format.
2. Identify the expensive nodes by actual time, loops, rows, buffers, temp IO, or cost when actual data is unavailable.
3. Compare estimated rows and actual rows.
4. Identify scan methods, join methods, sort nodes, aggregation nodes, materialization, and temporary storage.
5. Connect plan symptoms to query predicates, indexes, statistics, and data distribution.
6. Recommend validation, not just a guessed fix.

## Common Symptoms

### Bad Row Estimates

Possible causes:

- Stale statistics.
- Correlated columns.
- Skewed data distribution.
- Missing histograms or extended statistics.
- Parameter-sensitive plans.

### Sequential or Full Table Scan

Not always bad. It may be correct when:

- The table is small.
- Predicate selectivity is low.
- A large portion of the table is needed.
- Existing indexes are more expensive than scanning.

Investigate when a selective query scans a large table unexpectedly.

### Nested Loop Hotspot

Nested loops can be excellent for small outer sets and indexed inner lookups. They can be bad when:

- The outer side is much larger than estimated.
- The inner lookup has no useful index.
- Loops multiply random IO.

### Sort or Temporary Spill

Sort spill often means:

- No suitable order-compatible index.
- Too many rows sorted.
- Memory settings are too low for the workload.
- Query should filter earlier or paginate differently.

## PostgreSQL Notes

Prefer `EXPLAIN (ANALYZE, BUFFERS)` for serious diagnosis. Watch:

- Actual rows versus estimated rows.
- Buffers hit/read/dirtied.
- Loops.
- Sort method and disk usage.
- Join strategy.
- Index-only scan heap fetches.

## MySQL Notes

Use `EXPLAIN`, `EXPLAIN ANALYZE` when available, and optimizer trace when needed. Watch:

- `type`
- `key`
- `rows`
- `filtered`
- `Extra`, especially `Using temporary`, `Using filesort`, `Using index`, and `Using where`

## Oracle Notes

Use execution plan plus runtime evidence when possible:

- DBMS_XPLAN with actual stats.
- SQL Monitor for active expensive SQL.
- AWR/ASH for historical workload.
- Row estimate mismatch, access paths, join methods, temp usage, and plan hash changes.
