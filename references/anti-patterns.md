# SQL Anti-Patterns

## Query Anti-Patterns

- `SELECT *` in hot API paths.
- Unbounded list queries.
- Deep `OFFSET` pagination on large ordered sets.
- Functions around indexed columns without expression indexes.
- Implicit type conversion between parameters and columns.
- `LIKE '%term%'` with a normal B-tree expectation.
- `NOT IN` with nullable inputs.
- Large `OR` predicates without plan validation.
- Heavy aggregation in latency-sensitive OLTP requests.

## Index Anti-Patterns

- Indexing every filter column.
- Many redundant indexes sharing the same leading columns.
- Ignoring write overhead.
- Low-selectivity indexes with no supporting query pattern.
- Creating blocking indexes on large active tables.

## ORM Anti-Patterns

- N+1 queries.
- Lazy loading in list endpoints.
- Raw SQL string interpolation.
- Missing tenant predicates in dynamically generated filters.
- Fetching full entities when projections are enough.

## Transaction Anti-Patterns

- Long transactions.
- External API calls inside transactions.
- Batch updates without indexes.
- Inconsistent lock order.
- Large data migrations in a single transaction.

## Security Anti-Patterns

- String-concatenated SQL.
- Unwhitelisted dynamic `ORDER BY`.
- Caller-controlled table or column names.
- Overprivileged database users.
- Returning sensitive columns by default.
