---
name: sql-design
description: Enterprise SQL design, optimization, indexing, security, ORM, and database migration guidance for coding agents. Use when working on SQL, relational schema design, query performance, PostgreSQL-first optimization, MySQL or Oracle compatibility, SQL injection prevention, ORM-generated SQL review, transaction and locking risk, or production database change plans in developer projects.
---

# SQL Design

Use this skill to help developers write, review, optimize, and safely ship SQL-related code in real backend projects. Treat it as an open-source productivity layer for Claude Code, Codex, and similar coding agents, not as an application product.

## Operating Principles

- Classify the task before acting: existing-system optimization or requirement-stage design.
- Prefer PostgreSQL guidance by default unless the project or user clearly indicates MySQL or Oracle.
- Collect evidence before making performance claims. If evidence is missing, state assumptions and ask only for the minimum missing inputs needed to avoid risky work.
- Check security on every task involving SQL construction, ORM code, dynamic filters, dynamic ordering, user input, tenant boundaries, or permissions.
- Include locking, transaction, migration, version compatibility, validation, and rollback considerations for production-impacting changes.
- Do not expose full chain-of-thought. Use structured analysis internally and output concise, auditable reasoning: facts, assumptions, diagnosis, recommendation, risk, validation.

## Workflow Selection

### Existing-System Optimization

Use this path when SQL, schema, indexes, execution plans, ORM code, or production behavior already exists.

Read:

- `references/sop.md`
- `references/intake-checklist.md`
- `references/execution-plan.md` when an execution plan or slow query is involved
- `references/index-design.md` when indexes are involved
- `references/query-rewrite.md` when SQL can be rewritten
- `references/sql-injection-security.md` when user input or dynamic SQL exists
- `references/orm-and-application-stack.md` when ORM or application code is involved
- `references/transaction-locking.md` when concurrency, locks, transactions, or high-write paths exist
- `references/migration-version-control.md` before recommending DDL or data migration

### Requirement-Stage Design

Use this path when designing a new module, table, query, API persistence layer, or migration from business requirements.

Read:

- `references/sop.md`
- `references/intake-checklist.md`
- `references/schema-design.md`
- `references/database-selection.md` if database choice is not fixed
- `references/index-design.md`
- `references/sql-injection-security.md`
- `references/orm-and-application-stack.md` when application code will be written
- `references/transaction-locking.md` for concurrent writes or consistency-sensitive flows
- `references/migration-version-control.md` when migrations are required

## Database-Specific Routing

- PostgreSQL: read `references/postgresql.md` for most database-specific work.
- MySQL: read `references/mysql.md` when the project uses MySQL, MariaDB, or InnoDB-specific behavior.
- Oracle: read `references/oracle.md` when the project uses Oracle or enterprise systems that depend on CBO, AWR/ASH, hints, baselines, or Oracle partitioning.

## Output Requirements

For optimization tasks, include:

- Conclusion
- Confirmed facts
- Assumptions or missing evidence
- Diagnosis
- Recommended SQL, DDL, ORM, or code changes
- Security findings
- Index impact
- Locking and concurrency impact
- Version compatibility
- Validation plan
- Rollback plan

For design tasks, include:

- Design summary
- Business and workload assumptions
- Database choice if relevant
- Schema design
- Constraint design
- Index design
- SQL or ORM implementation
- Security design
- Transaction and concurrency design
- Migration plan
- Validation plan

## Hard Rules

- Never recommend string-concatenated SQL with untrusted input.
- Prefer parameterized queries, prepared statements, or safe ORM/query-builder APIs.
- Whitelist dynamic identifiers such as column names, sort fields, directions, schemas, and table names.
- Do not propose blocking large-table DDL without discussing lock behavior and safer alternatives.
- Do not claim performance improvement without a validation method.
- Do not assume one database's index or optimizer behavior applies unchanged to another database.
