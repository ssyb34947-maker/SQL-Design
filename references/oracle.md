# Oracle Guide

## Default Version Assumption

When version is unknown, reason conservatively around Oracle 19c while calling out version-sensitive behavior and enterprise governance constraints.

## Optimizer and Diagnostics

- Oracle uses the cost-based optimizer.
- Statistics quality is critical.
- Use DBMS_XPLAN with actual execution stats where possible.
- Use SQL Monitor for active long-running SQL.
- Use AWR and ASH for historical workload and wait analysis.
- Track plan hash changes when performance regresses.

## Indexing

- B-tree indexes suit common OLTP predicates.
- Bitmap indexes are usually for low-cardinality analytical workloads, not high-concurrency OLTP writes.
- Function-based indexes can support expression predicates.
- Partitioned tables require local versus global index decisions.

## Plan Stability

- Fix statistics and SQL shape before using hints.
- Hints can be useful but create maintenance obligations.
- SQL Plan Baselines may help stabilize critical SQL after analysis.

## Migration and Operations

- Respect DBA approval, maintenance windows, and enterprise release controls.
- Evaluate locking, redo/undo, temp space, and index maintenance.
- For large objects, include rollback and monitoring plans.
