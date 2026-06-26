# Query Rewrite

## Goals

Rewrite SQL to reduce scanned rows, avoid unnecessary work, improve index usability, and preserve business semantics.

## Rules

- Push selective filters as early as semantics allow.
- Avoid functions on indexed columns in predicates unless using a matching expression index.
- Avoid implicit type conversion between bind parameters and columns.
- Replace deep offset pagination with keyset pagination when stable ordering is available.
- Avoid `SELECT *` in hot paths; project only needed columns.
- Avoid unbounded queries in API paths.
- Split complex queries only when it improves optimizer choices, memory pressure, readability, or operational control.
- Preserve NULL semantics when rewriting `NOT IN`, `LEFT JOIN`, and anti-join logic.

## Common Rewrites

### Pagination

Prefer keyset pagination for high offsets:

```sql
WHERE (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT :limit
```

Ensure the index matches filter and order.

### OR Conditions

Large `OR` predicates may prevent efficient index usage. Consider:

- Separate queries combined with `UNION ALL`.
- Composite indexes per branch.
- Predicate normalization.

Validate duplicates and ordering when using `UNION ALL`.

### EXISTS vs IN vs JOIN

Choose based on semantics and optimizer behavior:

- Use `EXISTS` for existence checks.
- Use `JOIN` when columns from both sides are needed.
- Be careful with duplicates when replacing subqueries with joins.
- Be careful with NULL behavior for `NOT IN`.

### Aggregation

For expensive aggregation:

- Filter before grouping.
- Index group keys when useful.
- Consider materialized views, summary tables, or incremental aggregation for repeated dashboards.
- Avoid mixing OLTP request paths with heavy analytical aggregation when scale is high.

### LIKE and Search

- Prefix search can use B-tree indexes in some engines and collations.
- Contains search such as `%term%` often needs full-text, trigram, or search infrastructure.
- Do not pretend a normal B-tree index will solve arbitrary substring search.
