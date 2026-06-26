# Transactions and Locking

## Principles

- Keep transactions short.
- Acquire locks in consistent order.
- Index predicates used by updates and deletes.
- Avoid user interaction or network calls inside database transactions.
- Batch large writes and backfills.
- Treat lock behavior as part of the design, not an afterthought.

## Isolation

Ask for the database and isolation level before making strong concurrency claims.

Common concerns:

- Dirty reads.
- Non-repeatable reads.
- Phantom reads.
- Serialization failures.
- Lost updates.

## Optimistic Locking

Use a version column or compare-and-set update when:

- Conflicts are possible but not constant.
- Users edit stale records.
- You want to avoid long-held locks.

Example shape:

```sql
UPDATE account
SET balance = :new_balance, version = version + 1
WHERE id = :id AND version = :expected_version;
```

## Pessimistic Locking

Use row locks when:

- Conflicts are expected.
- Only one worker should process a row.
- Invariants require immediate exclusion.

Keep locked result sets small and indexed.

## Deadlock Review

Check:

- Transaction order.
- Missing indexes on update/delete predicates.
- Multiple tables updated in different orders.
- Batch size.
- Foreign key checks.
- Long-running reads in high isolation levels.

## DDL Locking

Before recommending DDL:

- Identify table size and write rate.
- Identify whether the DDL is metadata-only, online, concurrent, or blocking.
- Include maintenance window or online migration plan.
- Include rollback and monitoring.
