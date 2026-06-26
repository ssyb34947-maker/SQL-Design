# Index Design

## Table of Contents

- Principles
- Column order
- PostgreSQL
- MySQL
- Oracle
- Anti-patterns
- Production rollout

## Principles

- Design indexes from queries, not from columns alone.
- Prioritize high-frequency, high-latency, high-business-value queries.
- Balance read speed against write cost, storage cost, cache pressure, and maintenance overhead.
- Use unique indexes or constraints for business invariants.
- Prefer fewer high-quality composite indexes over many overlapping single-column indexes.
- Re-check index value after query rewrite or schema change.

## Column Order

For composite indexes, usually consider:

1. Equality predicates.
2. Tenant or partition boundary when every query includes it.
3. Highly selective predicates.
4. Range predicates.
5. Ordering columns.
6. Covering columns when the engine supports include columns or when coverage is worth write cost.

Do not apply this mechanically. Validate against workload and optimizer behavior.

## PostgreSQL

Useful index forms:

- B-tree for equality, range, ordering, and most normal OLTP predicates.
- Partial index for frequent predicates over a subset such as active rows.
- Expression index for computed predicates.
- Covering index with `INCLUDE` for index-only scans.
- GIN for arrays, JSONB containment, and full-text search.
- GiST for geometric, range, and specialized operators.
- BRIN for very large append-only or naturally ordered tables.

Production notes:

- Use `CREATE INDEX CONCURRENTLY` for large active tables when possible.
- Remember concurrent index creation cannot run inside a transaction block.
- Analyze table statistics after major data changes.

## MySQL

In InnoDB:

- The primary key is clustered; keep it stable and reasonably compact.
- Secondary indexes include the primary key and may require back-to-table lookups.
- Composite indexes follow leftmost-prefix behavior.
- Covering indexes can avoid row lookups.
- Indexes used for ordering depend on predicate and sort direction compatibility.

Check MySQL version before assuming online DDL behavior.

## Oracle

Consider:

- B-tree indexes for common OLTP predicates.
- Bitmap indexes mainly for low-cardinality analytical or warehouse-style workloads, not high-concurrency OLTP writes.
- Function-based indexes for expression predicates.
- Local versus global indexes for partitioned tables.
- Statistics, histograms, bind peeking, and plan stability.

Hints should be a last resort after understanding statistics and plan choice.

## Anti-Patterns

- Adding an index for every filter column.
- Many overlapping indexes with the same leading columns.
- Indexing low-selectivity columns without a supporting query pattern.
- Ignoring write amplification on hot tables.
- Creating large-table blocking indexes in business hours.
- Expecting an index to help when SQL wraps the column in a function or causes implicit type conversion.

## Production Rollout

For index changes:

- Estimate table size, write rate, and lock behavior.
- Use online or concurrent options where supported.
- Monitor lock waits, replication lag, IO, CPU, and query plans.
- Keep rollback SQL ready, usually dropping the new index.
- Remove redundant old indexes only after observing production behavior.
