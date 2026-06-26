#!/usr/bin/env python3
"""Generate SQL design or optimization intake checklists."""

from __future__ import annotations

import argparse
import json
from typing import Dict, List


COMMON = [
    "Confirm database engine and version.",
    "Confirm application language, framework, ORM, driver, and migration tool.",
    "Identify production constraints: data volume, peak concurrency, release window, rollback expectation.",
]

OPTIMIZATION = [
    "Collect SQL text or ORM query code.",
    "Collect table DDL, constraints, indexes, partitions, triggers, and generated columns.",
    "Collect approximate row counts and data distribution for filter, join, and order columns.",
    "Collect execution plan with runtime evidence when possible.",
    "Collect query frequency, P95/P99 latency, timeout, and affected API or job.",
    "Check SQL injection, dynamic SQL, dynamic ORDER BY, and tenant predicate risks.",
    "Classify root cause: SQL shape, index, statistics, schema, ORM, transaction lock, or workload mismatch.",
    "Prepare validation plan comparing before and after behavior.",
    "Prepare deploy and rollback plan for SQL, index, or migration changes.",
]

DESIGN = [
    "Extract entities, relationships, lifecycle states, and business invariants.",
    "List required read paths, write paths, filters, sorting, pagination, search, and aggregation.",
    "Define uniqueness, tenant scope, authorization, audit, retention, and archival requirements.",
    "Estimate current and future row counts, write rate, read QPS, and hot paths.",
    "Design schema, constraints, data types, and timestamps before adding indexes.",
    "Design indexes from known query paths and write/read tradeoffs.",
    "Design SQL or ORM access with parameter binding and identifier whitelists.",
    "Define transaction boundary, isolation expectation, optimistic or pessimistic locking, and idempotency.",
    "Prepare versioned migration, validation, and rollback plan.",
]

DB_ITEMS: Dict[str, List[str]] = {
    "postgres": [
        "Prefer EXPLAIN (ANALYZE, BUFFERS) for runtime plans.",
        "Consider partial, expression, INCLUDE, GIN, GiST, and BRIN indexes only when query operators justify them.",
        "For large active tables, evaluate CREATE INDEX CONCURRENTLY and transaction-block limitations.",
        "Check autovacuum, bloat, stale statistics, and long transactions when symptoms suggest MVCC pressure.",
    ],
    "mysql": [
        "Confirm MySQL 5.7 versus 8.0 before using advanced optimizer or DDL features.",
        "Account for InnoDB clustered primary key and secondary-index back-to-table lookups.",
        "Check leftmost-prefix behavior for composite indexes.",
        "Evaluate gap locks, next-key locks, and replication lag for write-heavy changes.",
    ],
    "oracle": [
        "Check statistics, histograms, bind behavior, and plan hash changes.",
        "Use DBMS_XPLAN, SQL Monitor, AWR, or ASH when available.",
        "Evaluate B-tree, bitmap, function-based, local, and global indexes based on workload.",
        "Treat hints and plan baselines as governed operational choices, not first-line fixes.",
    ],
}

ORM_ITEMS: Dict[str, List[str]] = {
    "hibernate": ["Check lazy loading, N+1 queries, fetch joins, projections, and transaction scope."],
    "jpa": ["Check lazy loading, N+1 queries, fetch joins, projections, and transaction scope."],
    "mybatis": ["Use #{} for values; allow ${} only for strict whitelisted identifiers."],
    "sqlalchemy": ["Use bound parameters, expression APIs, scoped sessions, and eager loading where needed."],
    "django": ["Check select_related, prefetch_related, QuerySet.explain(), and unsafe raw SQL."],
    "prisma": ["Prefer Prisma APIs; use $queryRaw safely and avoid $queryRawUnsafe with user input."],
    "typeorm": ["Check relation loading, generated joins, bind parameters, and explicit transactions."],
    "sequelize": ["Check relation loading, generated joins, bind parameters, and explicit transactions."],
    "gorm": ["Use parameterized conditions, explicit transactions, and controlled preloads."],
    "efcore": ["Use projections, AsNoTracking for read-only paths, and inspect generated SQL."],
    "dapper": ["Use named parameters and whitelist dynamic identifiers."],
}


def normalize_db(value: str) -> str:
    value = value.lower()
    if value in {"postgresql", "pg"}:
        return "postgres"
    return value


def build_checklist(mode: str, database: str, orm: str | None) -> Dict[str, List[str] | str]:
    db = normalize_db(database)
    items = list(COMMON)
    items.extend(OPTIMIZATION if mode == "optimization" else DESIGN)
    if db in DB_ITEMS:
        items.extend(DB_ITEMS[db])
    if orm:
        key = orm.lower().replace(".", "").replace(" ", "")
        items.extend(ORM_ITEMS.get(key, [f"Review {orm} generated SQL, bind parameters, transaction scope, and N+1 risk."]))
    return {"mode": mode, "database": db, "orm": orm or "unspecified", "checklist": items}


def print_markdown(result: Dict[str, List[str] | str]) -> None:
    print(f"# SQL {str(result['mode']).title()} Checklist")
    print()
    print(f"- Database: {result['database']}")
    print(f"- ORM: {result['orm']}")
    print()
    for idx, item in enumerate(result["checklist"], start=1):
        print(f"{idx}. {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SQL design or optimization checklists.")
    parser.add_argument("--mode", required=True, choices=["optimization", "design"], help="Task mode.")
    parser.add_argument("--database", default="postgres", choices=["postgres", "postgresql", "pg", "mysql", "oracle", "generic"], help="Database engine.")
    parser.add_argument("--orm", help="ORM or query builder, for example MyBatis, Prisma, SQLAlchemy, Hibernate.")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format.")
    args = parser.parse_args()
    result = build_checklist(args.mode, args.database, args.orm)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
