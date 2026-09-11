# PostgreSQL

```bash
psql -h <host> -U <username> -d <database>          # opens an interactive session against a specific database on a host
psql -h <host> -U <username> -d <database> -c "<SQL>"   # run one statement without an interactive session, scriptable
pg_dump -h <host> -U <username> <database> > backup.sql   # logical backup, plain SQL
pg_dump -Fc -h <host> -U <username> <database> > backup.dump   # custom format — required for pg_restore, supports parallel restore
pg_restore -h <host> -U <username> -d <database> backup.dump   # restore from a custom-format dump
```

```sql
\l                          -- list databases
\c <database>                -- switch database
\dt                            -- list tables in the current schema
\d <table>                      -- describe a table: columns, types, indexes, constraints
\du                               -- list roles/users and their privileges
SELECT * FROM pg_stat_activity WHERE state = 'active';   -- what's running right now
SELECT pg_size_pretty(pg_database_size('<database>'));     -- database size, human-readable
```

**Enhanced:**
```sql
SELECT pid, now() - query_start AS duration, query        -- longest-running active queries, sorted
  FROM pg_stat_activity WHERE state = 'active'
  ORDER BY duration DESC;
SELECT pg_terminate_backend(<pid>);                          -- kill a stuck query by PID (confirm it's the right one via the query above first)
EXPLAIN ANALYZE <query>;                                       -- actual execution plan + real timings, not just the estimate
VACUUM (VERBOSE, ANALYZE) <table>;                               -- reclaim dead tuple space and refresh planner stats — routine maintenance, not just an emergency tool
SELECT client_addr, state, sent_lsn, replay_lsn,                   -- replication lag, if this instance has standbys
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
  FROM pg_stat_replication;
```

## Health check

1. **Connection count** — `SELECT count(*) FROM pg_stat_activity;` — red flag: approaching `max_connections` — new connections are about to start failing.
2. **Long-running queries** — filter `pg_stat_activity` by `now() - query_start` — red flag: queries running far longer than your normal workload's baseline.
3. **Replication lag** (if you have standbys) — `pg_stat_replication` — red flag: lag bytes climbing over successive checks, not just momentarily nonzero.
4. **Autovacuum keeping up** — check `pg_stat_user_tables` for `n_dead_tup` — red flag: dead tuple count growing faster than autovacuum clears it — bloat and slow queries follow.

## Troubleshooting

**"too many connections" errors:**
```sql
SELECT count(*), state FROM pg_stat_activity GROUP BY state;   -- see where connections are actually going (active vs idle)
SELECT pid, state, now() - state_change AS idle_for FROM pg_stat_activity WHERE state = 'idle' ORDER BY idle_for DESC LIMIT 10;   -- long-idle connections are usually a connection pool misconfiguration, not real load
```

**Replication lag growing:**
```sql
SELECT client_addr, pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes FROM pg_stat_replication;   -- confirm it's actually growing, not just momentarily behind
```
Check the standby's own disk I/O and network to the primary — lag is almost always a resource bottleneck on the replica, not the primary doing anything wrong.

**Query stuck / deadlock suspected:**
```sql
SELECT pid, query, state, wait_event_type FROM pg_stat_activity WHERE wait_event_type = 'Lock';   -- who's waiting, and on what kind of lock
SELECT pg_terminate_backend(<pid>);   -- terminate the blocking session once you've confirmed which one it is
```

---
