# Oracle Database

```bash
sqlplus <username>/<password>@<tns_alias>                     # connect via a configured TNS entry — the standard way once tnsnames.ora is set up
sqlplus <username>/<password>@<host>:<port>/<service_name>       # connect directly without relying on tnsnames.ora — useful on a box where it isn't configured
sqlplus / as sysdba                                                # connect locally as SYSDBA — OS-level authentication, no password needed if you're the right OS user
tnsping <tns_alias>                                                  # confirm the listener is reachable — rules out network/listener issues before you start debugging the database itself
lsnrctl status                                                         # listener status — services registered, uptime
```

```sql
SELECT * FROM v$version;   -- confirm exact Oracle version/patch level — matters when a fix or feature is version-specific

SELECT user FROM dual;   -- current connected user — quick sanity check before you run anything against the wrong schema

SELECT table_name FROM user_tables ORDER BY table_name;   -- every table owned by the current user — a fast inventory before you go hunting through docs

DESC employees;   -- columns, types, nullability for one table — SQL*Plus shorthand for DESCRIBE, the first thing to check before writing a query against an unfamiliar table

SELECT username, status, sid, serial#   -- who's connected right now — useful before a maintenance window to confirm nobody's mid-transaction
  FROM   v$session;

SELECT tablespace_name, ROUND(used_percent, 1) AS used_pct   -- quick tablespace usage check — Oracle tablespaces fill independently of OS disk space, so this catches a problem `df -h` never would
  FROM   dba_tablespace_usage_metrics;

SELECT file_name, tablespace_name, bytes/1024/1024 AS size_mb   -- datafiles backing a tablespace, and their sizes — shows exactly which physical files would need more room
  FROM   dba_data_files
  WHERE  tablespace_name = '<TABLESPACE>';

SELECT name, open_mode, log_mode FROM v$database;   -- is it in ARCHIVELOG mode, mount/open state — confirms the DB is actually usable, not just that the process is running

ALTER SYSTEM SWITCH LOGFILE;   -- force a log switch — useful before checking archive status, so you're not waiting on a switch that hasn't happened yet
```

**Enhanced:**
```sql
SELECT sid, serial#, sql_id, status, event   -- what's actually running right now, and what it's waiting on — the event column tells you if it's CPU-bound, I/O-bound, or blocked on a lock
  FROM   v$session
  WHERE  status = 'ACTIVE';

ALTER SYSTEM KILL SESSION '<sid>,<serial#>';   -- kill a stuck/runaway session — confirm sid/serial# match the right one first, this is irreversible

SELECT sql_text, executions, elapsed_time/1000000 AS elapsed_sec   -- top time-consuming SQL, from the shared pool — the fastest way to find what's actually eating time, without guessing
  FROM   v$sql
  ORDER  BY elapsed_time DESC
  FETCH  FIRST 10 ROWS ONLY;

SELECT blocking_session, sid, serial#, wait_class, seconds_in_wait   -- sessions currently blocked, and who's blocking them — the blocking_session column points straight at the root cause
  FROM   v$session
  WHERE  blocking_session IS NOT NULL;

EXPLAIN PLAN FOR SELECT * FROM employees WHERE department_id = 10;   -- generate an execution plan without running the query — safe to use on a slow query in production, since it never actually executes it

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);   -- read the plan generated above — look for full table scans where an index was expected

SELECT index_name, table_name, uniqueness   -- indexes on a table, and whether they're actually unique as intended — a missing unique constraint is a common silent data-quality bug
  FROM   user_indexes
  WHERE  table_name = '<TABLE_NAME>';

SELECT name, value, description   -- check the live value of an init parameter — reading doesn't need a restart, only some changes do
  FROM   v$parameter
  WHERE  name LIKE '%<parameter_fragment>%';

SELECT * FROM v$diag_info WHERE name = 'Diag Trace';   -- where the alert log / trace files actually live on disk — the path varies by version/config, don't assume it

SELECT owner, object_name, object_type   -- every invalid object in the schema — stale views/procedures after a migration
FROM   dba_objects
WHERE  status = 'INVALID';

SELECT profile, resource_name, limit   -- password/resource limits applied to a user's profile — check before assuming a lockout is a mistake
FROM   dba_profiles
WHERE  profile = 'DEFAULT';

SELECT username, account_status, lock_date   -- confirm whether an account is actually locked, and since when — separates a real lockout from a forgotten password
FROM   dba_users
WHERE  username = '<USERNAME>';
```

## Backup & restore (Data Pump)

Data Pump (`expdp`/`impdp`) replaced the old `exp`/`imp` tools — faster, parallel, and the standard way to move data in and out of Oracle today.

```bash
expdp <username>/<password>@<tns_alias> directory=DATA_PUMP_DIR dumpfile=full_%U.dmp logfile=export.log full=y   # full database export — %U auto-splits into multiple numbered files
expdp <username>/<password>@<tns_alias> schemas=<SCHEMA_NAME> directory=DATA_PUMP_DIR dumpfile=schema.dmp logfile=export_schema.log   # export just one schema — the most common case in practice, smaller and faster than a full export
expdp <username>/<password>@<tns_alias> tables=<SCHEMA_NAME>.<TABLE_NAME> directory=DATA_PUMP_DIR dumpfile=table.dmp   # export a single table — a quick safety net before a risky migration touching just that table
expdp <username>/<password>@<tns_alias> parfile=export.par   # everything above as a parameter file instead of a long command line — the real-world way this is actually run
```

`export.par` contents, for reference:
```text
SCHEMAS=<SCHEMA_NAME>
DIRECTORY=DATA_PUMP_DIR
DUMPFILE=schema_%U.dmp
LOGFILE=export_schema.log
PARALLEL=4
COMPRESSION=ALL
```

```bash
impdp <username>/<password>@<tns_alias> directory=DATA_PUMP_DIR dumpfile=schema.dmp logfile=import.log   # import a Data Pump dump — needs the same directory object that was used for the export
impdp <username>/<password>@<tns_alias> parfile=import.par remap_schema=<OLD_SCHEMA>:<NEW_SCHEMA>   # import into a differently-named schema — common when restoring into a test/staging environment
impdp <username>/<password>@<tns_alias> directory=DATA_PUMP_DIR dumpfile=schema.dmp sqlfile=preview.sql   # don't actually import — just generate the DDL it WOULD run, to review first
```

```sql
SELECT directory_name, directory_path FROM dba_directories;   -- confirm the DIRECTORY object exists and points where expected — before expdp fails on it
```

**Enhanced — RMAN (the actual database-level backup tool, separate from Data Pump's logical export):**
```bash
rman target /                                                    # connect to the target database — opens an RMAN session for backup/restore operations
rman target / <<< "BACKUP DATABASE PLUS ARCHIVELOG;"                # full backup — includes the archived logs needed to make the backup consistent and restorable
rman target / <<< "BACKUP DATABASE PLUS ARCHIVELOG DELETE INPUT;"     # same, and delete archive logs once safely backed up — prevents them piling up
rman target / <<< "LIST BACKUP SUMMARY;"                                # see what backups actually exist and when they ran — confirm a backup job actually succeeded, don't just assume it did
rman target / <<< "RESTORE DATABASE VALIDATE;"                            # dry-run a restore without touching anything — confirms the backup is actually usable, before you're in an emergency and find out it isn't
```
Data Pump exports **data** (logical, portable across versions/platforms, good for migrations and single-schema restores). RMAN backs up the **database itself** (physical, faster for full disaster recovery, what you'd actually reach for to restore a crashed instance). Know which one a given situation calls for — they solve different problems.

## Health check

1. **Instance status** — `SELECT open_mode FROM v$database;` — red flag: anything other than `READ WRITE` when you expect the DB to be fully open.
2. **Session count** — `SELECT count(*) FROM v$session;` — red flag: approaching `sessions` parameter limit — new connections will start failing soon.
3. **Tablespace usage** — `dba_tablespace_usage_metrics` — red flag: any tablespace above 90% used.
4. **Alert log** — tail the current alert log — red flag: any `ORA-` error, especially repeating ones — a single old one in history is not urgent, a fresh repeating one is.

## Troubleshooting

**Database won't accept connections:**
```bash
lsnrctl status                                    # is the listener even up — the first thing to check, since no listener means no connections regardless of the DB's own state
sqlplus / as sysdba <<< "SELECT status FROM v\$instance;"   # is the instance actually open, or stuck in MOUNT — a DB can be "running" but not actually accepting application connections
```

**Archiver stuck / "ORA-00257: archiver error":**
```sql
SELECT * FROM v$flash_recovery_area_usage;   -- almost always the recovery area filling up — check this before digging into anything more exotic
```
```bash
rman target / <<< "DELETE ARCHIVELOG ALL COMPLETED BEFORE 'SYSDATE-3';"   # clear old archived logs older than 3 days — adjust the window to your actual recovery needs before running
```

**Tablespace full:**
```sql
SELECT tablespace_name, ROUND(used_percent, 1)   -- confirm which tablespace first — don't guess and extend the wrong one
  FROM   dba_tablespace_usage_metrics
  WHERE  used_percent > 90;

ALTER TABLESPACE mytablespace ADD DATAFILE '/path/to/new_datafile.dbf' SIZE 500M AUTOEXTEND ON;   -- add space to the tablespace — autoextend prevents this exact problem from recurring immediately
```

---
