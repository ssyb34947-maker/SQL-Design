# ORM and Application Stack

## General Rules

- Prefer framework-native parameter binding.
- Review generated SQL for hot paths.
- Avoid N+1 query patterns.
- Keep transaction scopes short and explicit.
- Avoid lazy loading in API list endpoints unless intentionally batched.
- Use batch reads and writes where supported.
- Use connection pools sized to database capacity, not only application traffic.

## Java

### JPA and Hibernate

- Watch lazy loading and N+1 queries.
- Use fetch joins, entity graphs, or batch fetching deliberately.
- Avoid huge persistence contexts in batch jobs.
- Use projections for read-heavy endpoints.

### MyBatis

- Prefer `#{}` parameter binding for values.
- Treat `${}` as unsafe unless used only with strict identifier whitelists.
- Review dynamic SQL branches for missing tenant or authorization predicates.

### jOOQ

- Prefer typed DSL expressions and bind values.
- Use generated schema metadata for safer refactors.
- Inspect generated SQL for complex queries.

## Python

### SQLAlchemy

- Use bound parameters and expression APIs.
- Avoid string-built raw SQL.
- Use eager loading strategies to avoid N+1.
- Keep sessions scoped and transactions explicit.

### Django ORM

- Use `select_related` and `prefetch_related`.
- Watch `.all()` in request paths.
- Use `QuerySet.explain()` when optimizing.
- Avoid unsafe `.extra()` or raw SQL without parameters.

## Node.js

### Prisma

- Prefer Prisma query APIs.
- Use `$queryRaw` safely with parameterization.
- Avoid `$queryRawUnsafe` unless there is no user input and identifiers are controlled.
- Review generated queries for pagination and relation loading.

### TypeORM, Sequelize, Knex

- Use bind parameters.
- Avoid raw string interpolation.
- Review relation loading and generated joins.
- Use explicit transactions for multi-step writes.

## Go

### GORM

- Use parameterized conditions.
- Watch implicit preloads and N+1 queries.
- Use explicit transactions for consistency-sensitive writes.

### sqlc

- Prefer checked SQL files and generated parameterized methods.
- Keep migrations and queries versioned together.

## .NET

### Entity Framework Core

- Use projections and `AsNoTracking` for read-only queries.
- Avoid client-side evaluation surprises.
- Inspect generated SQL for complex LINQ.

### Dapper

- Use named parameters.
- Avoid interpolated SQL with user input.
- Whitelist dynamic identifiers.
