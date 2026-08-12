# PostgreSQL with Java (JDBC)

## Learning outcomes

After this module you can:

- Explain **JDBC**’s role (driver, connection, statement, result set)  
- Connect Java to **PostgreSQL** with a connection URL  
- Run **parameterized** queries (no string-concatenated SQL)  
- Handle basic **transactions** (commit / rollback)  
- Place DB access behind a small **repository-style** boundary  

## Why PostgreSQL + Java here

Many CISS-style services persist operational and engineering data. PostgreSQL is a strong open-source RDBMS; Java remains common in enterprise backends.

| SE idea | DB analogue |
|---------|-------------|
| Requirements | Schema + constraints enforce invariants |
| Interfaces | Connection string, SQL contract, migrations |
| Verification | Tests against a known schema / seed data |
| Integrity | Least-privilege DB users; no secrets in Git |

## Mental model

```text
Java app  --JDBC-->  Driver  --TCP-->  PostgreSQL
                         │
                    Connection
                     /        \
              Statement    PreparedStatement
                     \        /
                    ResultSet / update counts
```

Prefer **PreparedStatement** always for user or external input.

## Prerequisites

- PostgreSQL running locally or in lab (Docker example below)  
- JDK 17+  
- Maven dependency:

```xml
<dependency>
  <groupId>org.postgresql</groupId>
  <artifactId>postgresql</artifactId>
  <version>42.7.4</version>
</dependency>
```

### Docker quick lab DB

```bash
docker run --name ciss-pg -e POSTGRES_PASSWORD=ciss -e POSTGRES_DB=cisslab -p 5432:5432 -d postgres:16
```

Connection URL:

```text
jdbc:postgresql://localhost:5432/cisslab
user: postgres
password: ciss
```

## Connection essentials

```java
String url = System.getenv().getOrDefault(
    "CISS_JDBC_URL", "jdbc:postgresql://localhost:5432/cisslab");
String user = System.getenv().getOrDefault("CISS_JDBC_USER", "postgres");
String pass = System.getenv().getOrDefault("CISS_JDBC_PASSWORD", "ciss");

try (Connection conn = DriverManager.getConnection(url, user, pass)) {
    conn.setAutoCommit(true); // or false for explicit transactions
    // work…
}
```

Rules:

1. Use **try-with-resources** for `Connection`, `PreparedStatement`, `ResultSet`.  
2. Never hard-code production passwords in source.  
3. One connection per short unit of work unless you introduce a pool (HikariCP later).

## Schema sketch (lab)

```sql
CREATE TABLE IF NOT EXISTS employee (
  id          SERIAL PRIMARY KEY,
  badge_code  TEXT NOT NULL UNIQUE,
  full_name   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS time_event (
  id           BIGSERIAL PRIMARY KEY,
  employee_id  INT NOT NULL REFERENCES employee(id),
  event_type   TEXT NOT NULL CHECK (event_type IN ('CHECK_IN', 'CHECK_OUT')),
  event_ts     TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## CRUD with PreparedStatement

### Insert

```java
String sql = "INSERT INTO employee (badge_code, full_name) VALUES (?, ?)";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, badge);
    ps.setString(2, name);
    int n = ps.executeUpdate();
}
```

### Select

```java
String sql = """
    SELECT id, badge_code, full_name
    FROM employee
    WHERE badge_code = ?
    """;
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setString(1, badge);
    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) {
            long id = rs.getLong("id");
            String fullName = rs.getString("full_name");
        }
    }
}
```

### Never do this

```java
// SQL injection risk — forbidden in course work
String bad = "SELECT * FROM employee WHERE badge_code = '" + badge + "'";
```

## Transactions

When two writes must succeed together:

```java
conn.setAutoCommit(false);
try {
    // insert A
    // insert B
    conn.commit();
} catch (SQLException e) {
    conn.rollback();
    throw e;
} finally {
    conn.setAutoCommit(true);
}
```

Example invariant: “check-in event only if not already checked in today” — read + write in one transaction (or enforce with constraints + careful SQL).

## Small design: repository boundary

Keep SQL out of UI / HTTP handlers:

```text
App / Service  →  EmployeeRepository  →  JDBC  →  PostgreSQL
```

Benefits: testability, clearer allocation of requirements (`FR-…` lives in service rules; persistence is design).

## Errors you will see

| Symptom | Checks |
|---------|--------|
| `Connection refused` | Postgres up? Port 5432? Docker running? |
| `FATAL: password authentication failed` | User/password env |
| `relation "employee" does not exist` | Migrations / SQL not applied |
| `SSL error` | URL sslmode for cloud DBs |

## Drill (40 min)

1. Start Postgres (Docker or local).  
2. Apply the schema SQL.  
3. Java program: insert one employee; query by badge; print result.  
4. Attempt a duplicate `badge_code`; handle `SQLException` cleanly.  
5. Optional: insert `CHECK_IN` in a transaction.  

Commit to Git with a message that does **not** include passwords.

## Integrity & security

- Lab passwords only in env / local untracked config.  
- No production credentials in screenshots for submission.  
- Parameterize every query.

## Further reading

| Topic | Source |
|-------|--------|
| PostgreSQL JDBC | [JDBC Driver docs](https://jdbc.postgresql.org/documentation/) |
| PostgreSQL tutorial | [postgresql.org/docs/current/tutorial.html](https://www.postgresql.org/docs/current/tutorial.html) |
| SQL injection | [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) |
| HikariCP (pools) | [HikariCP](https://github.com/brettwooldridge/HikariCP) — next step after raw DriverManager |

## Next

**AMQP messaging with Java** — publish and consume messages for decoupled services.
