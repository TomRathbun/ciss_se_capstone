# PostgreSQL Database Management for Admins

## Learning outcomes

After this module you can:

- Describe **Postgres** roles: instance, database, schema, role/user  
- Perform safe **admin SQL** (inspect, not destroy)  
- Check **connections, size, activity, and locks**  
- Apply basic **backup / restore awareness** and maintenance (`VACUUM`, analyze)  
- Coordinate with app developers (JDBC URLs, privileges, migrations)  

## Why admins touch Postgres

On this program, Java services (JDBC) and internal tools often use **PostgreSQL**. Admins are asked to:

| Request | Admin response |
|---------|----------------|
| “DB is slow” | Activity, locks, size, logs |
| “Create an app user” | Role + grants (least privilege) |
| “Disk full” | Table/index size, logs, WAL |
| “Restore last night’s dump” | `pg_dump` / `pg_restore` discipline |

SE link: the database is a **critical external interface** — availability and schema change control belong in V&V and release process.

> App development SQL is deeper in the SW track; this module is **operator** focused.

---

## Architecture snapshot

```text
PostgreSQL instance (port 5432)
 ├── database: appdb
 │     ├── schema: public
 │     └── schema: app
 ├── role: app_rw          (login + grants)
 └── role: readonly_ops    (SELECT only)
```

| Object | Meaning |
|--------|---------|
| **Instance / cluster** | One running `postgres` service with its data directory |
| **Database** | Named database inside the instance |
| **Schema** | Namespace inside a database |
| **Role** | User or group identity (login optional) |

---

## Connect and inspect

```bash
sudo systemctl status postgresql       # service name may vary
psql --version
# Local peer auth often works for OS user postgres:
sudo -u postgres psql
```

Inside `psql`:

```sql
\conninfo
\l                  -- list databases
\c appdb            -- connect to database
\dn                 -- schemas
\dt                 -- tables in current schema
\du                 -- roles
\q                  -- quit
```

Connection URI shape (apps):

```text
jdbc:postgresql://dbhost:5432/appdb?user=app_rw
```

---

## Common admin SQL

### Who is connected?

```sql
SELECT pid, usename, datname, client_addr, state, query_start, left(query, 80)
FROM pg_stat_activity
ORDER BY query_start NULLS LAST;
```

### Terminate a runaway session (privileged, careful)

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid = 12345;
```

### Database and table sizes

```sql
SELECT pg_size_pretty(pg_database_size(current_database()));

SELECT relname AS table,
       pg_size_pretty(pg_total_relation_size(relid)) AS total
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 20;
```

### Locks (slow / blocked queries)

```sql
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query
FROM pg_stat_activity AS blocked
JOIN pg_locks bl ON bl.pid = blocked.pid AND NOT bl.granted
JOIN pg_locks kl ON kl.locktype = bl.locktype
  AND kl.DATABASE IS NOT DISTINCT FROM bl.DATABASE
  AND kl.relation IS NOT DISTINCT FROM bl.relation
  AND kl.pid <> bl.pid
JOIN pg_stat_activity AS blocking ON blocking.pid = kl.pid
WHERE blocked.state = 'active';
```

### Roles and grants (pattern)

```sql
CREATE ROLE app_rw LOGIN PASSWORD '...';   -- password via secret process
GRANT CONNECT ON DATABASE appdb TO app_rw;
GRANT USAGE ON SCHEMA app TO app_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_rw;
-- Prefer migrator role for DDL; app role without CREATE when possible
```

### Read-only checks

```sql
SELECT version();
SHOW data_directory;
SHOW shared_buffers;
SHOW max_connections;
```

---

## Maintenance awareness

| Task | Purpose |
|------|---------|
| **VACUUM** | Reclaim dead tuples; visibility map |
| **ANALYZE** | Update planner statistics |
| **REINDEX** | Rebuild corrupted or bloated indexes (costly) |
| **Autovacuum** | Background worker — usually leave enabled |

```sql
VACUUM (VERBOSE) some_table;
ANALYZE some_table;
```

Run heavy maintenance in change windows; watch disk and I/O.

---

## Backup and restore (operator level)

```bash
# Logical dump (common)
sudo -u postgres pg_dump -Fc -f /backup/appdb_$(date +%F).dump appdb

# Restore into a database (destructive if objects exist — coordinate)
sudo -u postgres pg_restore -d appdb_new /backup/appdb_2026-08-11.dump
```

| Habit | Why |
|-------|-----|
| Test restore periodically | Untested backups are hopes |
| Store dumps off-box | Host failure takes disk and dump together |
| Document version | `pg_dump` from version X into Y has rules |
| Never ad-hoc restore production | Change ticket + owner approval |

Physical/base backups and PITR (WAL archiving) exist for larger estates — know they exist; follow program runbooks.

---

## Config and logs

| Item | Typical location / view |
|------|-------------------------|
| Main config | `postgresql.conf` |
| Client auth | `pg_hba.conf` (who may connect how) |
| Logs | `journalctl -u postgresql` or `data/log/` |

`pg_hba.conf` mistakes cause “authentication failed” even with correct passwords — check method (`scram-sha-256`, `md5`, `peer`) and source address.

---

## Troubleshooting map

| Symptom | Look at |
|---------|---------|
| Cannot connect | Service up? port? `pg_hba.conf`? firewall? password? |
| Too many connections | `max_connections`, idle sessions, app pool size |
| Slow query | `pg_stat_activity`, locks, `EXPLAIN` (with developer) |
| Disk full | DB size, logs, WAL, filesystem `df -h` |
| After reboot | Service enabled? data dir permissions? |

---

## Drill (45 min)

1. Connect with `psql` (lab instance) and run `\l`, `\du`.  
2. Report database size with `pg_size_pretty(pg_database_size(...))`.  
3. List active sessions via `pg_stat_activity` (sanitize queries in notes).  
4. Write a least-privilege grant sketch for a reporting user (SELECT only on one schema).  
5. Document the backup command you would use for a logical dump and where the file should *not* live.  

## Integrity

- No production dumps in Git or chat.  
- No shared superuser passwords in tickets.  
- Prefer read-only roles for humans doing investigation.  
- DDL/migrations follow app change control — admins do not “fix schema” casually.  

## Further reading

| Topic | Source |
|-------|--------|
| psql | `man psql` · [PostgreSQL docs — psql](https://www.postgresql.org/docs/current/app-psql.html) |
| Role system | PostgreSQL docs — Database Roles |
| Backup | docs — Backup and Restore |
| Monitoring views | `pg_stat_activity`, `pg_stat_user_tables` |
| SW track | **PostgreSQL with Java (JDBC)** module |

## Next

**Troubleshooting methodology** — systematic diagnosis and deep dive on everyday Linux tools.
