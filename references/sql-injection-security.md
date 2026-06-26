# SQL Injection and Data Security

## Hard Rules

- Never concatenate untrusted input into SQL text.
- Use parameterized queries, prepared statements, or safe ORM/query-builder APIs.
- Whitelist dynamic identifiers such as column names, table names, schema names, sort fields, and sort directions.
- Treat tenant predicates and authorization filters as security controls.
- Use least-privilege database accounts.

## Unsafe Patterns

```sql
-- Unsafe when user_input is concatenated into SQL text.
WHERE name = '" + user_input + "'
```

```sql
-- Unsafe when sort is user-controlled without a whitelist.
ORDER BY ${sort_field} ${sort_direction}
```

## Safe Dynamic Ordering

Map user input to known identifiers in application code:

```text
allowed_sort_fields = {
  "createdAt": "created_at",
  "name": "name"
}
allowed_directions = {"asc": "ASC", "desc": "DESC"}
```

Only emit SQL identifiers from the whitelist.

## ORM Security

- Prefer bind parameters and ORM expressions.
- Avoid raw SQL escape hatches unless necessary.
- If raw SQL is needed, keep values parameterized and identifiers whitelisted.
- Review dynamic filters generated from request bodies.
- Check multi-tenant predicates cannot be omitted by caller-controlled input.

## Data Exposure

- Avoid `SELECT *` in APIs with sensitive fields.
- Separate public projection from internal persistence model.
- Apply row-level authorization in addition to route-level checks where needed.
- Audit privileged access and data export queries.
