#!/usr/bin/env python3
"""Static SQL risk scanner for the sql-design skill.

The scanner is intentionally conservative and dependency-free. It does not try to
fully parse SQL; it flags common enterprise review issues that deserve human or
agent attention before shipping SQL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass
class Finding:
    severity: str
    rule: str
    line: int
    message: str
    suggestion: str
    snippet: str


RISKY_FUNCTION_PREDICATE = re.compile(
    r"\bwhere\b[\s\S]*?\b(lower|upper|date|to_char|substring|substr|coalesce|cast)\s*\(\s*[a-zA-Z_][\w.]*",
    re.IGNORECASE,
)
LEADING_WILDCARD_LIKE = re.compile(r"\blike\s+(['\"]?)%", re.IGNORECASE)
DYNAMIC_ORDER = re.compile(r"\border\s+by\s+(\$\{|\{\{|%s|\?|:[a-zA-Z_]|\+)", re.IGNORECASE)
STRING_CONCAT_SQL = re.compile(
    r"(select|insert|update|delete|where|order\s+by)[^\n;]*(\+|\$\{|\{\{|f['\"]|format\(|concat\()",
    re.IGNORECASE,
)
SELECT_STAR = re.compile(r"\bselect\s+(?:distinct\s+)?\*\b", re.IGNORECASE)
OFFSET_WITHOUT_LIMIT = re.compile(r"\boffset\s+\d+\b(?![\s\S]*\blimit\b)", re.IGNORECASE)
LARGE_OFFSET = re.compile(r"\boffset\s+([1-9]\d{3,})\b", re.IGNORECASE)
UPDATE_OR_DELETE_NO_WHERE = re.compile(r"^\s*(update|delete\s+from)\b(?![\s\S]*\bwhere\b)", re.IGNORECASE)
SELECT_NO_BOUND = re.compile(r"^\s*select\b(?![\s\S]*\b(where|limit|fetch\s+first|top\s+\d+)\b)", re.IGNORECASE)
NOT_IN = re.compile(r"\bnot\s+in\s*\(", re.IGNORECASE)
OR_CHAIN = re.compile(r"\bwhere\b[\s\S]*(?:\bor\b[\s\S]*){2,}", re.IGNORECASE)
PG_CREATE_INDEX_NO_CONCURRENTLY = re.compile(r"^\s*create\s+(unique\s+)?index\b(?!\s+concurrently\b)", re.IGNORECASE)
DDL_RISK = re.compile(r"^\s*(alter\s+table|drop\s+table|truncate\s+table)\b", re.IGNORECASE)
IMPLICIT_NUMERIC_STRING = re.compile(r"\b[a-zA-Z_][\w.]*\s*=\s*'\d+'", re.IGNORECASE)


def strip_sql_comments(sql: str) -> str:
    sql = re.sub(r"/\*[\s\S]*?\*/", " ", sql)
    sql = re.sub(r"--.*", "", sql)
    return sql


def split_statements(sql: str) -> List[str]:
    statements: List[str] = []
    current: List[str] = []
    quote: str | None = None
    escape = False
    for char in sql:
        current.append(char)
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                quote = None
        elif char in {"'", '"'}:
            quote = char
        elif char == ";":
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, max(0, offset)) + 1


def snippet(statement: str) -> str:
    compact = re.sub(r"\s+", " ", statement).strip()
    return compact[:180]


def add_if(pattern: re.Pattern[str], statement: str, full_text: str, findings: List[Finding], severity: str, rule: str, message: str, suggestion: str) -> None:
    match = pattern.search(statement)
    if not match:
        return
    global_offset = full_text.find(statement)
    local_offset = match.start()
    findings.append(
        Finding(
            severity=severity,
            rule=rule,
            line=line_for_offset(full_text, max(0, global_offset) + local_offset),
            message=message,
            suggestion=suggestion,
            snippet=snippet(statement),
        )
    )


def lint_sql(sql: str, dialect: str) -> List[Finding]:
    clean = strip_sql_comments(sql)
    findings: List[Finding] = []
    for statement in split_statements(clean):
        normalized = statement.strip()
        add_if(SELECT_STAR, normalized, clean, findings, "medium", "select-star", "SELECT * in a production path can expose unnecessary columns and increase IO.", "Project only required columns, especially in API responses and hot paths.")
        add_if(SELECT_NO_BOUND, normalized, clean, findings, "medium", "unbounded-select", "SELECT has no visible WHERE, LIMIT, FETCH FIRST, or TOP bound.", "Add a business predicate, pagination, or document why a full scan/export is intended.")
        add_if(UPDATE_OR_DELETE_NO_WHERE, normalized, clean, findings, "critical", "write-without-where", "UPDATE or DELETE statement has no WHERE clause.", "Add a precise predicate and consider a pre-check SELECT before running in production.")
        add_if(RISKY_FUNCTION_PREDICATE, normalized, clean, findings, "medium", "function-on-predicate-column", "Predicate appears to wrap a column in a function, which can prevent normal index usage.", "Rewrite the predicate or add a matching expression/function-based index if justified.")
        add_if(LEADING_WILDCARD_LIKE, normalized, clean, findings, "medium", "leading-wildcard-like", "LIKE pattern starts with %, which usually cannot use a normal B-tree index efficiently.", "Use full-text, trigram/search index, or a prefix-search requirement if possible.")
        add_if(DYNAMIC_ORDER, normalized, clean, findings, "high", "dynamic-order-by", "ORDER BY appears to use a dynamic value or placeholder.", "Whitelist sort columns and directions; bind only values, not SQL identifiers.")
        add_if(STRING_CONCAT_SQL, normalized, clean, findings, "high", "possible-sql-concatenation", "SQL text appears to be constructed with interpolation or concatenation.", "Use parameter binding for values and whitelists for identifiers.")
        add_if(OFFSET_WITHOUT_LIMIT, normalized, clean, findings, "medium", "offset-without-limit", "OFFSET appears without a LIMIT/FETCH bound.", "Add a limit and prefer keyset pagination for deep pages.")
        add_if(NOT_IN, normalized, clean, findings, "low", "not-in-null-semantics", "NOT IN can produce surprising results when the subquery or list contains NULL.", "Consider NOT EXISTS or explicitly exclude NULLs.")
        add_if(OR_CHAIN, normalized, clean, findings, "low", "wide-or-chain", "WHERE clause has multiple OR branches that may complicate index usage.", "Validate the execution plan; consider UNION ALL or targeted composite indexes if needed.")
        add_if(IMPLICIT_NUMERIC_STRING, normalized, clean, findings, "low", "possible-implicit-cast", "Predicate compares a column to a quoted numeric literal.", "Ensure bind parameter types match column types to avoid implicit casts.")
        large_offset = LARGE_OFFSET.search(normalized)
        if large_offset:
            global_offset = clean.find(statement)
            findings.append(Finding("medium", "large-offset-pagination", line_for_offset(clean, max(0, global_offset) + large_offset.start()), "Large OFFSET pagination can become expensive on large ordered result sets.", "Prefer keyset pagination with a stable indexed order.", snippet(statement)))
        if dialect in {"postgres", "postgresql"}:
            add_if(PG_CREATE_INDEX_NO_CONCURRENTLY, normalized, clean, findings, "medium", "postgres-index-without-concurrently", "PostgreSQL CREATE INDEX is not using CONCURRENTLY.", "For large active tables, consider CREATE INDEX CONCURRENTLY and remember it cannot run inside a transaction block.")
        add_if(DDL_RISK, normalized, clean, findings, "high", "production-ddl-risk", "DDL statement may lock or rewrite production objects.", "Document lock behavior, version support, deploy window, validation, and rollback plan.")
    return findings


def read_inputs(paths: Sequence[str]) -> str:
    if not paths:
        return sys.stdin.read()
    return "\n\n".join(Path(path).read_text(encoding="utf-8") for path in paths)


def print_markdown(findings: Iterable[Finding]) -> None:
    findings = list(findings)
    if not findings:
        print("No findings.")
        return
    for item in findings:
        print(f"- [{item.severity}] {item.rule} (line {item.line})")
        print(f"  - {item.message}")
        print(f"  - Suggestion: {item.suggestion}")
        print(f"  - Snippet: `{item.snippet}`")


def main() -> int:
    parser = argparse.ArgumentParser(description="Static SQL risk scanner for enterprise SQL review.")
    parser.add_argument("paths", nargs="*", help="SQL files to scan. Reads stdin when omitted.")
    parser.add_argument("--dialect", default="generic", choices=["generic", "postgres", "postgresql", "mysql", "oracle"], help="SQL dialect hint.")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format.")
    args = parser.parse_args()

    sql = read_inputs(args.paths)
    findings = lint_sql(sql, args.dialect)
    if args.format == "json":
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    else:
        print_markdown(findings)
    return 1 if any(item.severity in {"critical", "high"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
