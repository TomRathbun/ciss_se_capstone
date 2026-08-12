# SW-A04 — JDBC Repository Slice

**Weight:** 15% · **Due:** After sw-04-java-postgresql · **Module:** sw-04-java-postgresql

## Prompt

Implement a **small repository-style** Java slice against PostgreSQL (lab VM or approved host): parameterized queries, basic transaction, no SQL string concatenation for inputs.

## Scenario (lab)

Track a tiny **lab inventory** table, e.g. `lab_items(id, name, qty, updated_at)` — or equivalent you create.

## Deliverables

1. **Schema SQL** (`CREATE TABLE` + sample seed).
2. **Java code:** connect via JDBC URL (config outside source if possible), insert, select, update qty with **PreparedStatement**.
3. **Transaction demo:** two writes that **commit** on success and **rollback** on a deliberate failure path (show both outcomes in notes/log).
4. **Design note (½ page):** DriverManager vs DataSource/pool vs JBoss JNDI — when you would use each.
5. **Security note:** how secrets are supplied (env / properties not committed).

## Quality bar

- No string-built SQL with user input.
- Failures leave DB consistent (rollback path real).
- Code is short and readable (not a framework dump).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| correctness | 15 | CRUD + transaction behavior works |
| safety | 10 | PreparedStatement + secret handling |
| communication | 5 | Schema and notes clear |
