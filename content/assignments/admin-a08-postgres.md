# ADMIN-A08 — PostgreSQL Operator Checks

**Weight:** 10% · **Due:** After admin-08-postgres-admin · **Module:** admin-08-postgres-admin

## Prompt

Run **operator-safe** PostgreSQL checks (lab DB) and produce an admin health snapshot for app teammates.

## Deliverables

1. **Instance sheet:** version, data directory if visible, uptime/start time if available.
2. **SQL evidence** (paste): list databases; connection/activity view; one size query; one lock/activity observation (even if “none”).
3. **Role design:** propose `app_rw` and `readonly_ops` privileges for a sample app schema (GRANT sketch).
4. **Maintenance awareness:** what `VACUUM`/`ANALYZE` are for; when you escalate vacuum/wraparound issues.
5. **Backup note:** `pg_dump` scope (what you would dump) + restore caution (one paragraph).
6. Coordination: JDBC URL shape you would hand a SW intern (no password in the doc).

## Quality bar

- No drop/truncate “for fun.”
- Least privilege is real.
- Distinguishes admin ops from app SQL development.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| checks | 15 | Useful health evidence |
| privilege_design | 10 | Sensible roles/grants |
| communication | 5 | SW-handoff ready |
