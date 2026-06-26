# Migration and Version Control

## Principles

- Store migrations in version control.
- Make migrations deterministic and repeatable.
- Prefer additive changes before destructive changes.
- Separate schema expansion, application rollout, data backfill, and cleanup.
- Include rollback guidance even when the exact rollback is manual.

## Expand and Contract

For risky schema changes:

1. Expand: add new nullable column, table, index, or compatibility layer.
2. Deploy code that writes both old and new shapes when needed.
3. Backfill in batches.
4. Validate data parity.
5. Switch reads.
6. Stop writing old shape.
7. Contract: remove old column or table in a later release.

## Migration Tools

Respect the project's chosen tool:

- Flyway.
- Liquibase.
- Rails migrations.
- Django migrations.
- Prisma migrations.
- Alembic.
- EF Core migrations.

Do not introduce a new migration framework without project-level reason.

## Production Checklist

- Pre-checks.
- Backup or restore point expectations.
- Lock and online DDL behavior.
- Expected runtime.
- Disk, WAL/binlog/redo, undo, temp, and replication impact.
- Deployment order.
- Post-checks.
- Rollback or forward-fix plan.

## Data Backfill

- Process in batches.
- Use stable ordering.
- Commit between batches.
- Rate-limit under production load.
- Make the operation idempotent.
- Track progress.
