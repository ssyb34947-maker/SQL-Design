# Performance Testing

## Goals

Validate that SQL or schema changes improve the target workload without creating unacceptable write, lock, storage, or operational costs.

## Metrics

Capture:

- Latency: average, P95, P99.
- Throughput.
- Error and timeout rate.
- Rows scanned and returned.
- Execution count.
- CPU, IO, memory, buffer/cache behavior.
- Lock waits and deadlocks.
- Replication lag.
- Application connection pool saturation.

## Test Shape

- Use production-like data volume and distribution when possible.
- Compare before and after plans.
- Test both hot-cache and cold-cache behavior when relevant.
- Include peak concurrency for write paths.
- Test rollback or disabling strategy where practical.

## Report

Include:

- Baseline.
- Change applied.
- Result.
- Tradeoffs.
- Remaining risk.
- Recommendation.
