# Oracle Database

```bash
sqlplus <username>/<password>@<tns_alias>                     # connect via a configured TNS entry
sqlplus <username>/<password>@<host>:<port>/<service_name>       # connect directly without relying on tnsnames.ora
sqlplus / as sysdba                                                # connect locally as SYSDBA, OS authentication
tnsping <tns_alias>                                                  # confirm the listener is reachable and how long it takes, before blaming the DB
lsnrctl status                                                         # listener status — services registered, uptime
```

```sql
SELECT * FROM v$version;   -- confirm exact Oracle version/patch level

SELECT user FROM dual;   -- current connected user

SELECT table_name FROM user_tables ORDER BY table_name;   -- every table owned by the current user

DESC employees;   -- columns, types, nullability for one table (SQL*Plus shorthand for DESCRIBE)

SELECT username, status, sid, serial#   -- who's connected right now
  FROM   v$session;

SELECT tablespace_name, ROUND(used_percent, 1) AS used_pct   -- quick tablespace usage check
  FROM   dba_tablespace_usage_metrics;

SELECT file_name, tablespace_name, bytes/1024/1024 AS size_mb   -- datafiles backing a tablespace, and their sizes
  FROM   dba_data_files
  WHERE  tablespace_name = '<TABLESPACE>';

SELECT name, open_mode, log_mode FROM v$database;   -- is it in ARCHIVELOG mode, mount/open state

ALTER SYSTEM SWITCH LOGFILE;   -- force a log switch (useful before checking archive status)
```

**Enhanced:**
```sql
SELECT sid, serial#, sql_id, status, event   -- what's actually running right now, and what it's waiting on
  FROM   v$session
  WHERE  status = 'ACTIVE';

ALTER SYSTEM KILL SESSION '<sid>,<serial#>';   -- kill a stuck/runaway session (confirm it's actually the right one first)

SELECT sql_text, executions, elapsed_time/1000000 AS elapsed_sec   -- top time-consuming SQL, from the shared pool
  FROM   v$sql
  ORDER  BY elapsed_time DESC
  FETCH  FIRST 10 ROWS ONLY;

SELECT blocking_session, sid, serial#, wait_class, seconds_in_wait   -- sessions currently blocked, and who's blocking them
  FROM   v$session
  WHERE  blocking_session IS NOT NULL;

EXPLAIN PLAN FOR SELECT * FROM employees WHERE department_id = 10;   -- generate an execution plan without running the query

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);   -- read the plan generated above — look for full table scans where an index was expected

SELECT index_name, table_name, uniqueness   -- indexes on a table, and whether they're actually unique as intended
  FROM   user_indexes
  WHERE  table_name = '<TABLE_NAME>';

SELECT name, value, description   -- check the live value of an init parameter, no restart needed to read it
  FROM   v$parameter
  WHERE  name LIKE '%<parameter_fragment>%';

SELECT * FROM v$diag_info WHERE name = 'Diag Trace';   -- where the alert log / trace files actually live on disk

SELECT owner, object_name, object_type   -- every invalid object in the schema — stale views/procedures after a migration
FROM   dba_objects
WHERE  status = 'INVALID';

SELECT profile, resource_name, limit   -- password/resource limits applied to a user's profile — check before assuming a lockout is a mistake
FROM   dba_profiles
WHERE  profile = 'DEFAULT';

SELECT username, account_status, lock_date   -- confirm whether an account is actually locked, and since when
FROM   dba_users
WHERE  username = '<USERNAME>';
```

## Health check

1. **Instance status** — `SELECT open_mode FROM v$database;` — red flag: anything other than `READ WRITE` when you expect the DB to be fully open.
2. **Session count** — `SELECT count(*) FROM v$session;` — red flag: approaching `sessions` parameter limit — new connections will start failing soon.
3. **Tablespace usage** — `dba_tablespace_usage_metrics` — red flag: any tablespace above 90% used.
4. **Alert log** — tail the current alert log — red flag: any `ORA-` error, especially repeating ones — a single old one in history is not urgent, a fresh repeating one is.

## Troubleshooting

**Database won't accept connections:**
```bash
lsnrctl status                                    # is the listener even up
sqlplus / as sysdba <<< "SELECT status FROM v\$instance;"   # is the instance actually open, or stuck in MOUNT
```

**Archiver stuck / "ORA-00257: archiver error":**
```sql
SELECT * FROM v$flash_recovery_area_usage;   -- almost always the recovery area filling up
```
```bash
rman target / <<< "DELETE ARCHIVELOG ALL COMPLETED BEFORE 'SYSDATE-3';"   # clear old archived logs older than 3 days — adjust the window to your actual recovery needs before running
```

**Tablespace full:**
```sql
SELECT tablespace_name, ROUND(used_percent, 1)   -- confirm which one, first
  FROM   dba_tablespace_usage_metrics
  WHERE  used_percent > 90;

ALTER TABLESPACE mytablespace ADD DATAFILE '/path/to/new_datafile.dbf' SIZE 500M AUTOEXTEND ON;   -- add space; autoextend prevents an immediate repeat
```

---
