# PostgreSQL

```bash
psql -h <host> -U <username> -d <database>          # opens an interactive session against a database — the standard way to poke around manually
psql -h <host> -U <username> -d <database> -c "<SQL>"   # run one statement without an interactive session — scriptable, no psql prompt needed
pg_dump -h <host> -U <username> <database> > backup.sql   # logical backup, plain SQL — human-readable, restorable with just psql -f, no special tooling
pg_dump -Fc -h <host> -U <username> <database> > backup.dump   # custom format — required for pg_restore, supports parallel restore
pg_restore -h <host> -U <username> -d <database> backup.dump   # restore from a custom-format dump — needs pg_restore specifically, plain SQL won't work here
```

```sql
\l                          -- list databases — the first thing to check when you're not sure which database you're even connected to
\c <database>                -- switch database — psql sessions are locked to one database, this is how you move to another
\dt                            -- list tables in the current schema — a fast inventory before writing a query against an unfamiliar database
\d <table>                      -- describe a table: columns, types, indexes, constraints — the first thing to check before writing a query against it
\du                               -- list roles/users and their privileges — confirms who can actually do what, not just who exists
\dx                                -- list installed extensions — confirms whether something like pg_stat_statements is even available before you try to query it

SELECT version();   -- confirm exact PostgreSQL version — matters since syntax and available features differ across major versions

SELECT current_user, current_database();   -- who you're connected as, and to which database — a quick sanity check before running anything destructive

SELECT * FROM pg_stat_activity WHERE state = 'active';   -- what's running right now — the starting point for almost any performance investigation

SELECT pg_size_pretty(pg_database_size('<database>'));   -- database size, human-readable — quick check before assuming disk pressure is unrelated to this database

SELECT relname, pg_size_pretty(pg_total_relation_size(relid))   -- largest tables in the current database — usually the first suspects when disk usage grows unexpectedly
  FROM   pg_catalog.pg_statio_user_tables
  ORDER  BY pg_total_relation_size(relid) DESC
  LIMIT  10;
```

**Enhanced:**
```sql
SELECT pid, now() - query_start AS duration, query   -- longest-running active queries, sorted — the fastest way to spot a query that's stuck or badly optimized
  FROM   pg_stat_activity
  WHERE  state = 'active'
  ORDER  BY duration DESC;

SELECT pg_terminate_backend(<pid>);   -- kill a stuck query by PID — confirm it's the right one via the query above first, this is irreversible

EXPLAIN ANALYZE <query>;   -- actual execution plan + real timings — the planner's estimate can be wildly wrong, this runs the query and shows what actually happened

VACUUM (VERBOSE, ANALYZE) <table>;   -- reclaim dead tuple space and refresh planner stats — routine maintenance, not just an emergency tool

SELECT client_addr, state, sent_lsn, replay_lsn,   -- replication lag, if this instance has standbys — confirms replicas are actually keeping up, not just connected
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes
  FROM   pg_stat_replication;

SELECT schemaname, relname, n_dead_tup, n_live_tup   -- dead-tuple bloat per table — the number autovacuum is racing against
  FROM   pg_stat_user_tables
  ORDER  BY n_dead_tup DESC
  LIMIT  10;

SELECT indexrelname, idx_scan, idx_tup_read   -- indexes that are barely (or never) used — candidates for dropping
  FROM   pg_stat_user_indexes
  WHERE  idx_scan < 50
  ORDER  BY idx_scan;

SELECT locktype, relation::regclass, mode, granted, pid   -- current locks — granted=false rows are the ones actually blocked
  FROM   pg_locks
  WHERE  NOT granted;

SELECT query, calls, total_exec_time, mean_exec_time   -- top queries by total time — needs the pg_stat_statements extension enabled, the standard way to find what's actually slow across the whole workload
  FROM   pg_stat_statements
  ORDER  BY total_exec_time DESC
  LIMIT  10;

SELECT rolname, rolsuper, rolcanlogin   -- roles/users and whether they're superusers or can even log in — a quick security-relevant inventory
FROM   pg_roles;

SELECT n.nspname AS schema, c.relname AS table, c.reltuples::bigint AS approx_rows   -- approximate row counts for every table — fast because it skips a full COUNT scan, good enough for a quick size sense
  FROM   pg_class c
  JOIN   pg_namespace n ON n.oid = c.relnamespace
  WHERE  c.relkind = 'r'
  ORDER  BY c.reltuples DESC
  LIMIT  10;

SELECT datname, numbackends, xact_commit, xact_rollback   -- per-database activity summary — commit/rollback ratio hints at app-level error rates
FROM   pg_stat_database;
```

## Backup & restore

```bash
pg_dump -h <host> -U <username> -d <database> -Fp > backup.sql          # plain SQL, human-readable — restore with psql -f, no special tooling needed
pg_dump -h <host> -U <username> -d <database> -Fc -f backup.dump          # custom format — compressed, required for pg_restore, supports selective/parallel restore
pg_dump -h <host> -U <username> -d <database> -Fd -j 4 -f backup_dir        # directory format, dumped in parallel with 4 jobs — much faster on a large database
pg_dumpall -h <host> -U <username> > full_cluster.sql                         # every database in the cluster, plus roles/tablespaces — pg_dump alone only covers one database
pg_dump --schema-only -h <host> -U <username> -d <database> > schema.sql        # structure only, no data — useful for spinning up an empty copy of the schema
pg_dump --data-only -h <host> -U <username> -d <database> > data.sql              # data only, no structure — for reloading into an already-migrated schema
pg_dump -t <schema>.<table> -h <host> -U <username> -d <database> > table.sql       # a single table, not the whole database — useful before a risky change touching just that table
```

```bash
psql -h <host> -U <username> -d <database> -f backup.sql                     # restore a plain-SQL dump — just runs the SQL file through psql
pg_restore -h <host> -U <username> -d <database> backup.dump                   # restore a custom-format dump — needs pg_restore specifically, this format isn't plain SQL
pg_restore -h <host> -U <username> -d <database> -j 4 backup_dir                 # parallel restore from directory format — matches the parallel dump above
pg_restore -l backup.dump                                                          # list the contents of a dump without restoring anything — confirm what's actually in it first
pg_restore -h <host> -U <username> -d <database> -t <table> backup.dump              # restore just one table out of a full dump — no need to restore everything to get one table back
```

**Enhanced — physical backups (pg_basebackup):**
```bash
pg_basebackup -h <host> -U <username> -D /backup/path -Fp -Xs -P   # full physical copy of the data directory, streaming WAL as it goes — the basis for point-in-time recovery, not just a snapshot
pg_basebackup -h <host> -U <username> -D /backup/path -Ft -z -P      # same idea, but tarred and gzip-compressed output — smaller for storage/transfer than a plain directory
```
`pg_dump` is a **logical** backup — portable across versions, good for migrations and picking out individual tables, but it's a point-in-time SQL/data snapshot with no way to replay changes since. `pg_basebackup` is a **physical** backup — combined with WAL archiving, it supports true point-in-time recovery (restore to any specific moment, not just the backup time). Know which one the situation actually calls for: routine migrations and table-level restores want `pg_dump`; disaster recovery for the whole cluster wants a physical backup strategy.

## Health check

1. **Connection count** — `SELECT count(*) FROM pg_stat_activity;` — red flag: approaching `max_connections` — new connections are about to start failing.
2. **Long-running queries** — filter `pg_stat_activity` by `now() - query_start` — red flag: queries running far longer than your normal workload's baseline.
3. **Replication lag** (if you have standbys) — `pg_stat_replication` — red flag: lag bytes climbing over successive checks, not just momentarily nonzero.
4. **Autovacuum keeping up** — check `pg_stat_user_tables` for `n_dead_tup` — red flag: dead tuple count growing faster than autovacuum clears it — bloat and slow queries follow.

## Troubleshooting

**"too many connections" errors:**
```sql
SELECT count(*), state   -- see where connections are actually going — active vs idle, before assuming the count itself is the problem
  FROM   pg_stat_activity
  GROUP  BY state;

SELECT pid, state, now() - state_change AS idle_for   -- long-idle connections usually mean pool misconfiguration — real active load looks different in this same view
  FROM   pg_stat_activity
  WHERE  state = 'idle'
  ORDER  BY idle_for DESC
  LIMIT  10;
```

**Replication lag growing:**
```sql
SELECT client_addr, pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes   -- confirm lag is actually growing over successive checks — a momentary nonzero value alone isn't necessarily a problem
  FROM   pg_stat_replication;
```
Check the standby's own disk I/O and network to the primary — lag is almost always a resource bottleneck on the replica, not the primary doing anything wrong.

**Query stuck / deadlock suspected:**
```sql
SELECT pid, query, state, wait_event_type   -- who's waiting, and on what kind of lock — narrows a stuck query down to a specific blocking cause
  FROM   pg_stat_activity
  WHERE  wait_event_type = 'Lock';

SELECT pg_terminate_backend(<pid>);   -- terminate the blocking session once you've confirmed which one it is — this is irreversible, don't guess
```

---
