# Backend Infrastructure Ideas

Open technical ideas for the Andavo backend — not yet scoped into a project.

## Ideas

- (2026-07-24, from warroom notes) **Prune Spring Batch database tables.** The Spring Batch metadata tables grow unbounded; needs a retention/cleanup strategy.
- (2026-07-24, from warroom notes) **Use Postgres for leader election.** Investigate `pg_advisory_lock` as a leader-election primitive instead of adding a separate coordination service.
