# Schema Design

## Design Order

1. Identify entities, relationships, lifecycle states, and invariants.
2. Define access patterns before indexes.
3. Choose data types that preserve semantics and avoid implicit casts.
4. Add constraints for business invariants that must hold under concurrency.
5. Add audit, tenant, and lifecycle fields where needed.
6. Plan migrations and backward compatibility.

## Table Principles

- Use stable primary keys. Prefer generated identity or UUID only when distribution, merge, or external id requirements justify it.
- Keep natural business keys as unique constraints, not necessarily primary keys.
- Use `NOT NULL` when a value is required.
- Use check constraints for small invariant rules where supported and maintainable.
- Use foreign keys when referential integrity is critical and operational policy allows them.
- Avoid storing comma-separated values or encoded multi-values in scalar columns.
- Avoid over-normalizing hot read paths when it causes repeated joins with no integrity benefit.
- Avoid denormalizing before understanding update consistency and write amplification.

## Common Fields

Common enterprise tables often need:

- `created_at`
- `updated_at`
- `created_by`
- `updated_by`
- `deleted_at` or explicit status when soft delete is required
- `tenant_id` for multi-tenant systems
- `version` for optimistic locking

Do not add fields mechanically. Tie each field to query, audit, compliance, or concurrency needs.

## Data Type Rules

- Use numeric types for numeric comparisons and sorting.
- Use timestamp types consistently with timezone policy.
- Use fixed precision decimals for money and rates.
- Avoid string ids for values that need numeric range queries.
- Avoid implicit casts between application parameters and database columns.

## Multi-Tenant Design

- Include tenant scope in tables and queries when data is tenant-isolated.
- Add tenant-aware unique constraints when uniqueness is tenant-local.
- Add tenant-aware indexes for tenant-filtered queries.
- Treat missing tenant predicates as a security issue, not only a performance issue.
