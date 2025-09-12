**Worker & Jobs**

Engine
- RQ (Redis-backed) chosen for simplicity.
- Start worker: `zebras worker` (uses `REDIS_URL`, queue name `zebras`).

Usage
- Enqueue jobs from plugins for long-running tasks or retries (helpers to be added).
- Default worker starts with a single queue; extend as needed.

Scheduling
- Not implemented yet. Options: `rq-scheduler` or `APScheduler`.

Future
- Retry policies, DLQ routing, and job decorators for common patterns.

