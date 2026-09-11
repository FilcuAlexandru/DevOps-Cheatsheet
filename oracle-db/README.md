# Oracle Database

```bash
sqlplus <username>/<password>@<tns_alias>                     # connect via a configured TNS entry
sqlplus <username>/<password>@<host>:<port>/<service_name>       # connect directly without relying on tnsnames.ora
tnsping <tns_alias>                                                # confirm the listener is reachable and how long it takes, before blaming the DB
lsnrctl status                                                       # listener status — services registered, uptime
```

```sql
SELECT * FROM v$version;                                    -- confirm exact Oracle version/patch level
SELECT username, status, sid, serial# FROM v$session;          -- who's connected right now
SELECT tablespace_name, ROUND(used_percent,1) AS used_pct       -- quick tablespace usage check
  FROM dba_tablespace_usage_metrics;
SELECT * FROM dba_data_files WHERE tablespace_name = '<TABLESPACE>';   -- datafiles backing a tablespace, and their sizes
ALTER SYSTEM SWITCH LOGFILE;                                     -- force a log switch (useful before checking archive status)
SELECT name, open_mode, log_mode FROM v$database;                  -- is it in ARCHIVELOG mode, mount/open state
```

**Enhanced:**
```sql
SELECT sid, serial#, sql_id, status, event FROM v$session WHERE status = 'ACTIVE';   -- what's actually running right now, and what it's waiting on
ALTER SYSTEM KILL SESSION '<sid>,<serial#>';                                            -- kill a stuck/runaway session (confirm it's actually the right one first)
SELECT sql_text, executions, elapsed_time/1000000 AS elapsed_sec                          -- top time-consuming SQL, from the shared pool
  FROM v$sql ORDER BY elapsed_time DESC FETCH FIRST 10 ROWS ONLY;
SELECT * FROM v$diag_info WHERE name = 'Diag Trace';                                        -- where the alert log / trace files actually live on disk
tail -f $(sqlplus -s <username>/<password> <<< "SELECT value FROM v\$diag_info WHERE name='Diag Trace';" | tail -1)/alert_<SID>.log   -- tail the alert log directly from the shell, no separate lookup step
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
SELECT tablespace_name, ROUND(used_percent,1) FROM dba_tablespace_usage_metrics WHERE used_percent > 90;   -- confirm which one, first
ALTER TABLESPACE mytablespace ADD DATAFILE '/path/to/new_datafile.dbf' SIZE 500M AUTOEXTEND ON;   -- add space; autoextend prevents an immediate repeat
```

---
