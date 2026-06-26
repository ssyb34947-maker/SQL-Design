# SQL Engineering SOP

## Table of Contents

- Existing-system optimization
- Requirement-stage design
- SQL review
- Production change review
- Output discipline

## Existing-System Optimization

Use this process when the project already has SQL, schema, indexes, ORM code, query plans, or production behavior.

1. Identify the database engine and version.
2. Identify the application stack and ORM or query builder.
3. Collect the SQL, table DDL, existing indexes, row counts, query frequency, latency target, and execution plan.
4. Check SQL injection and authorization risk before focusing only on speed.
5. Read the execution plan and compare estimated rows with actual rows when available.
6. Classify the root cause: SQL shape, missing or wrong index, stale statistics, schema design, transaction locking, ORM behavior, or workload mismatch.
7. Propose the smallest useful change first.
8. Evaluate read improvement, write cost, storage cost, lock impact, replication impact, version compatibility, and rollback difficulty.
9. Provide exact SQL, DDL, ORM, or code changes only after risk is stated.
10. Provide validation steps and rollback steps.

## Requirement-Stage Design

Use this process when the module does not exist yet or the agent must design SQL from business requirements.

1. Extract business entities, relationships, invariants, lifecycle states, and access patterns.
2. Determine whether database choice is fixed. If not, compare PostgreSQL, MySQL, and Oracle with the project constraints.
3. Design schema, constraints, data types, audit fields, soft-delete policy, tenant boundary, and retention strategy.
4. Design query paths before designing indexes.
5. Add indexes for known high-value reads, uniqueness guarantees, foreign-key joins, and common ordering requirements.
6. Keep write-heavy tables index-light unless reads justify the cost.
7. Design SQL and ORM access with parameter binding and identifier whitelists.
8. Define transaction boundaries and concurrency control.
9. Prepare migration scripts with versioning, expand-contract compatibility, validation, and rollback.
10. Recommend tests and performance checks.

## SQL Review

During review, check these areas in order:

- Correctness: Does the query return the intended rows and preserve business semantics?
- Safety: Can untrusted input affect SQL text, identifiers, filters, sort order, tenant scope, or authorization?
- Performance: Does the plan match expected indexes, selectivity, ordering, joins, and row counts?
- Maintainability: Is SQL readable, deterministic, and compatible with the application stack?
- Operations: Can changes be deployed without unacceptable locks, downtime, or rollback risk?

## Production Change Review

For DDL, index, migration, backfill, partitioning, or data repair:

- State risk level.
- Identify whether the change is blocking or online.
- For large tables, prefer online or concurrent approaches where supported.
- Separate schema expansion, code rollout, backfill, and cleanup when possible.
- Include pre-check SQL, deploy steps, post-check SQL, monitoring signals, and rollback.

## Output Discipline

Output concise audit-friendly reasoning. Separate:

- Facts observed in the repo, SQL, schema, or execution plan.
- Assumptions made because inputs are missing.
- Diagnosis.
- Recommendation.
- Risks.
- Validation.
- Rollback.
