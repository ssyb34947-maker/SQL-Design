# Intake Checklist

## Existing-System Optimization

Collect or infer:

- Database engine and version.
- Application language, framework, ORM, and driver.
- SQL text or ORM query code.
- Table DDL, constraints, indexes, partitions, triggers, and generated columns.
- Approximate row count and data distribution for key columns.
- Current execution plan, preferably with actual timing and buffers when supported.
- Query frequency, peak concurrency, latency target, timeout settings, and affected API.
- Current slow query log, wait events, lock waits, deadlocks, or CPU/IO symptoms.
- Existing connection pool and transaction boundary.
- Read/write ratio and freshness requirements.
- Deployment constraints, maintenance windows, replication topology, and rollback expectations.

If unavailable, state the missing evidence and provide a conservative next step.

## Requirement-Stage Design

Collect or infer:

- Business entities and relationships.
- Required invariants and uniqueness rules.
- Query paths: by id, list, search, dashboard, export, aggregation, reconciliation.
- Write paths: create, update, status transition, delete, batch import, background job.
- Expected scale: rows now, rows in one year, peak QPS, peak write rate.
- Multi-tenant or authorization model.
- Data retention, archival, audit, and compliance requirements.
- Consistency requirements and acceptable race behavior.
- Sorting, pagination, filtering, full-text search, JSON, geospatial, or analytical needs.
- Existing project database and migration tool.
- ORM or query builder conventions in the codebase.

## Minimum Safe Inputs

For optimization, do not make strong claims without at least SQL, schema, indexes, database type, and a plausible workload description.

For design, do not finalize schema or indexes without knowing core queries, uniqueness rules, write paths, and expected scale.
