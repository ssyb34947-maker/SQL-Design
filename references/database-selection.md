# Database Selection

## Default Stance

Use the database already chosen by the project unless the user is explicitly choosing technology for a new system. Avoid unnecessary rewrites across database engines.

## PostgreSQL

Prefer PostgreSQL when the project needs:

- Strong general-purpose OLTP with rich SQL.
- Advanced indexing such as partial, expression, GIN, GiST, BRIN, and covering indexes.
- JSONB with relational integrity.
- Complex constraints, CTEs, window functions, and analytical queries inside an OLTP database.
- Mature extensions, full-text search, geospatial support, or custom types.
- Strong open-source ecosystem and operational flexibility.

Default to PostgreSQL-first guidance for this skill.

## MySQL

Prefer MySQL or MariaDB when the project needs:

- Simple high-throughput OLTP with common web application patterns.
- InnoDB-centric operations and teams with strong MySQL experience.
- Existing infrastructure, replication, monitoring, and operational standards built around MySQL.
- Compatibility with applications or managed platforms standardized on MySQL.

Account for MySQL 5.7 versus 8.0 differences before using advanced features.

## Oracle

Prefer Oracle when the project needs:

- Existing enterprise Oracle estate.
- Mature tooling around AWR, ASH, SQL Monitor, partitioning, plan baselines, and enterprise support.
- Mission-critical transaction systems with teams trained on Oracle operations.
- Strong compatibility with legacy enterprise applications.

Oracle recommendations must respect licensing, version, and DBA governance constraints.

## Selection Criteria

Compare engines across:

- Existing stack and team expertise.
- Operational maturity and managed service availability.
- SQL features and indexing needs.
- Transaction and isolation requirements.
- Write throughput and read workload.
- Partitioning and archival needs.
- Audit, compliance, and security requirements.
- Cost, licensing, support, and migration risk.
