#!/usr/bin/env python3
"""Normalize database execution-plan text into a compact review summary."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Sequence


@dataclass
class PlanNode:
    engine: str
    line: int
    node_type: str
    relation: str | None
    estimated_rows: int | None
    actual_rows: int | None
    cost: str | None
    actual_time: str | None
    raw: str


PG_NODE_WITH_RELATION = re.compile(
    r"(?P<node>[A-Z][A-Za-z ]+?)(?:\s+using\s+\S+)?\s+on\s+(?P<relation>[\w.]+)\s+"
    r"\(cost=(?P<cost>[^)]*?rows=(?P<est>\d+)[^)]*)\)"
    r"(?:\s+\(actual\s+time=(?P<actual_time>[^)]*?rows=(?P<actual>\d+)[^)]*)\))?",
    re.IGNORECASE,
)
PG_NODE_NO_RELATION = re.compile(
    r"(?P<node>[A-Z][A-Za-z ]+?)\s+"
    r"\(cost=(?P<cost>[^)]*?rows=(?P<est>\d+)[^)]*)\)"
    r"(?:\s+\(actual\s+time=(?P<actual_time>[^)]*?rows=(?P<actual>\d+)[^)]*)\))?",
    re.IGNORECASE,
)
MYSQL_EXTRA = re.compile(r"Using\s+(temporary|filesort|index|where)", re.IGNORECASE)
MYSQL_TABULAR_SPLIT = re.compile(r"\s*\|\s*")
ORACLE_ROW = re.compile(r"^\s*\|\s*\d+\s*\|\s*(?P<node>[^|]+?)\s*\|\s*(?P<relation>[^|]*?)\s*\|.*?\|\s*(?P<rows>\d+)?\s*\|", re.IGNORECASE)


def read_input(paths: Sequence[str]) -> str:
    if not paths:
        return sys.stdin.read()
    return "\n\n".join(Path(path).read_text(encoding="utf-8") for path in paths)


def detect_engine(text: str, requested: str) -> str:
    if requested != "auto":
        return requested
    lowered = text.lower()
    if "cost=" in lowered and "actual" in lowered or "seq scan" in lowered or "bitmap heap scan" in lowered:
        return "postgres"
    if "using filesort" in lowered or "using temporary" in lowered or "possible_keys" in lowered:
        return "mysql"
    if "dbms_xplan" in lowered or "plan hash value" in lowered or "| operation" in lowered:
        return "oracle"
    return "generic"


def parse_postgres(text: str) -> List[PlanNode]:
    nodes: List[PlanNode] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        clean_line = line.replace("->", " ").strip()
        match = PG_NODE_WITH_RELATION.search(clean_line) or PG_NODE_NO_RELATION.search(clean_line)
        if not match:
            continue
        node_type = " ".join(match.group("node").split())
        relation = match.groupdict().get("relation")
        if relation is None:
            relation_match = re.match(r"(?P<node>.+?)\s+on\s+(?P<relation>[\w.]+)$", node_type, re.IGNORECASE)
            if relation_match:
                node_type = relation_match.group("node")
                relation = relation_match.group("relation")
        nodes.append(
            PlanNode(
                engine="postgres",
                line=line_no,
                node_type=node_type,
                relation=relation,
                estimated_rows=int(match.group("est")) if match.group("est") else None,
                actual_rows=int(match.group("actual")) if match.group("actual") else None,
                cost=match.group("cost"),
                actual_time=match.group("actual_time"),
                raw=line.strip(),
            )
        )
    return nodes


def parse_mysql(text: str) -> List[PlanNode]:
    nodes: List[PlanNode] = []
    lines = text.splitlines()
    header: List[str] | None = None
    for line_no, line in enumerate(lines, start=1):
        if "|" in line:
            cols = [part.strip().lower() for part in MYSQL_TABULAR_SPLIT.split(line.strip(" |"))]
            if {"select_type", "table", "type"}.issubset(set(cols)):
                header = cols
                continue
            if header and not set(cols) <= {"", "+", "-"} and len(cols) >= len(header):
                row = dict(zip(header, cols))
                if row.get("table") and row.get("type"):
                    rows = row.get("rows")
                    nodes.append(
                        PlanNode(
                            engine="mysql",
                            line=line_no,
                            node_type=f"access:{row.get('type')}",
                            relation=row.get("table") or None,
                            estimated_rows=int(rows) if rows and rows.isdigit() else None,
                            actual_rows=None,
                            cost=None,
                            actual_time=None,
                            raw=line.strip(),
                        )
                    )
        elif MYSQL_EXTRA.search(line):
            nodes.append(PlanNode("mysql", line_no, "extra", None, None, None, None, None, line.strip()))
    return nodes


def parse_oracle(text: str) -> List[PlanNode]:
    nodes: List[PlanNode] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = ORACLE_ROW.search(line)
        if not match:
            continue
        rows = match.group("rows")
        relation = match.group("relation").strip() or None
        nodes.append(
            PlanNode(
                engine="oracle",
                line=line_no,
                node_type=" ".join(match.group("node").split()),
                relation=relation,
                estimated_rows=int(rows) if rows and rows.isdigit() else None,
                actual_rows=None,
                cost=None,
                actual_time=None,
                raw=line.strip(),
            )
        )
    return nodes


def parse_generic(text: str) -> List[PlanNode]:
    patterns = ["scan", "join", "sort", "aggregate", "temporary", "filesort", "index"]
    nodes: List[PlanNode] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if any(word in line.lower() for word in patterns):
            nodes.append(PlanNode("generic", line_no, "plan-line", None, None, None, None, None, line.strip()))
    return nodes


def parse_plan(text: str, engine: str) -> List[PlanNode]:
    if engine in {"postgres", "postgresql"}:
        return parse_postgres(text)
    if engine == "mysql":
        return parse_mysql(text)
    if engine == "oracle":
        return parse_oracle(text)
    return parse_generic(text)


def summarize(nodes: List[PlanNode]) -> List[str]:
    notes: List[str] = []
    for node in nodes:
        lower = node.raw.lower()
        if "seq scan" in lower or "full table" in lower or "access:all" in lower:
            notes.append(f"Line {node.line}: full/sequential scan candidate. Validate selectivity and index fit before changing it.")
        if "filesort" in lower or "sort" in lower:
            notes.append(f"Line {node.line}: sort operation detected. Check ORDER BY, memory, and order-compatible indexes.")
        if "temporary" in lower or "temp" in lower:
            notes.append(f"Line {node.line}: temporary storage detected. Check grouping, sorting, and intermediate row counts.")
        if "nested loop" in lower:
            notes.append(f"Line {node.line}: nested loop detected. Good for small outer rows, risky if row estimates are low.")
        if node.estimated_rows is not None and node.actual_rows is not None:
            if node.estimated_rows == 0 and node.actual_rows > 0 or node.estimated_rows and node.actual_rows / max(node.estimated_rows, 1) >= 10:
                notes.append(f"Line {node.line}: actual rows greatly exceed estimates. Check statistics, skew, and correlated predicates.")
    return notes


def print_markdown(engine: str, nodes: List[PlanNode], notes: List[str]) -> None:
    print(f"# Execution Plan Summary")
    print()
    print(f"- Engine: {engine}")
    print(f"- Parsed nodes: {len(nodes)}")
    print()
    if nodes:
        print("## Nodes")
        for node in nodes:
            relation = f" on {node.relation}" if node.relation else ""
            rows = []
            if node.estimated_rows is not None:
                rows.append(f"estimated_rows={node.estimated_rows}")
            if node.actual_rows is not None:
                rows.append(f"actual_rows={node.actual_rows}")
            suffix = f" ({', '.join(rows)})" if rows else ""
            print(f"- Line {node.line}: {node.node_type}{relation}{suffix}")
    if notes:
        print()
        print("## Review Notes")
        for note in notes:
            print(f"- {note}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize execution plan text into a review summary.")
    parser.add_argument("paths", nargs="*", help="Plan files. Reads stdin when omitted.")
    parser.add_argument("--database", default="auto", choices=["auto", "postgres", "postgresql", "mysql", "oracle", "generic"], help="Database engine.")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"], help="Output format.")
    args = parser.parse_args()

    text = read_input(args.paths)
    engine = detect_engine(text, args.database)
    nodes = parse_plan(text, engine)
    notes = summarize(nodes)
    if args.format == "json":
        print(json.dumps({"engine": engine, "nodes": [asdict(node) for node in nodes], "notes": notes}, ensure_ascii=False, indent=2))
    else:
        print_markdown(engine, nodes, notes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
