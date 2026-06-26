# MySQL Guide

## Default Version Assumption

When version is unknown, distinguish MySQL 5.7 and 8.0 before recommending features such as window functions, functional indexes, invisible indexes, and `EXPLAIN ANALYZE`.

## InnoDB Basics

- The primary key is clustered.
- Secondary indexes store primary key values.
- Wide primary keys increase secondary index size.
- Composite indexes depend heavily on leading columns.
- Covering indexes can avoid table lookups.

## Plan Analysis

Use `EXPLAIN` and `EXPLAIN ANALYZE` where available. Watch:

- `type`: `const`, `ref`, `range`, `index`, `ALL`.
- `key`: chosen index.
- `rows` and `filtered`: estimated scanned rows.
- `Extra`: `Using where`, `Using index`, `Using temporary`, `Using filesort`.

## Indexing

- Use composite indexes based on equality, range, and ordering requirements.
- Avoid redundant indexes with the same left prefix.
- Consider covering indexes for hot reads.
- Avoid too many indexes on hot write tables.

## Locking

- InnoDB uses row locks, gap locks, and next-key locks depending on isolation level and query shape.
- Missing indexes in update/delete predicates can widen lock impact.
- Long transactions and large batch writes can block production traffic.

## Migration

- Verify online DDL support for the exact version, engine, and operation.
- For large tables, consider online schema change tooling when native online DDL is insufficient.
- Monitor replication lag during heavy DDL or backfill.
