# PostgreSQL Guide

## Default Version Assumption

When version is unknown, reason conservatively around PostgreSQL 14+ while noting version-sensitive features. Ask for version when using features that may vary across PostgreSQL 12 to 17.

## Performance Tools

- Use `EXPLAIN (ANALYZE, BUFFERS)` for runtime plans.
- Use `pg_stat_statements` for workload-level query frequency and latency.
- Use `pg_locks`, `pg_stat_activity`, and wait events for blocking.
- Use `VACUUM`, `ANALYZE`, and autovacuum status for MVCC and statistics issues.

## Indexing

Common choices:

- B-tree for most OLTP predicates and sorting.
- Partial index for common filtered subsets.
- Expression index for computed predicates.
- `INCLUDE` columns for covering index use cases.
- GIN for JSONB, arrays, and full-text.
- BRIN for very large naturally ordered tables.

Use `CREATE INDEX CONCURRENTLY` on large active tables when possible:

```sql
CREATE INDEX CONCURRENTLY idx_orders_tenant_status_created
ON orders (tenant_id, status, created_at DESC);
```

Remember it cannot run inside a normal transaction block.

## Query Notes

- Avoid implicit casts from mismatched parameter types.
- Avoid wrapping indexed columns in functions unless an expression index exists.
- Prefer keyset pagination for deep pages.
- Use JSONB indexes only for the operators actually used.
- Consider extended statistics for correlated predicates.

## Locking and MVCC

- Long transactions can prevent vacuum cleanup and cause bloat.
- DDL often requires locks; even short locks can block in high-concurrency systems.
- Check blocking chains before assuming a slow query is only a bad plan.
- Be careful with `SELECT ... FOR UPDATE` in list queries.

## Schema and Migration

- Prefer additive migrations before destructive changes.
- Backfill in batches.
- Validate constraints separately when supported.
- For large tables, separate column addition, backfill, constraint validation, and cleanup.

## Anti-Patterns

- Creating blocking indexes on active large tables.
- Ignoring autovacuum and bloat.
- Using JSONB for relational data that needs joins and constraints.
- Assuming `LIMIT` makes a query cheap when ordering still requires sorting a huge set.
- Treating sequential scan as automatically wrong.
