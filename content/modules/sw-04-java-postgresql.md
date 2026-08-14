# PostgreSQL with Java (JDBC)

## Learning outcomes

After this module you can:

- Explain **JDBC**’s role (driver, connection, statement, result set)  
- Connect Java to **PostgreSQL** with a connection URL  
- Distinguish **DriverManager**, **DataSource**, and **connection pools**  
- Use a pool in code (e.g. **HikariCP**) and look up a **JBoss/WildFly** datasource via **JNDI**  
- Run **parameterized** queries (no string-concatenated SQL)  
- Handle basic **transactions** (commit / rollback)  
- Place DB access behind a small **repository-style** boundary  
- Explain **trade-offs** between app-managed and container-managed connections  

## Why PostgreSQL + Java here

Many CISS-style services persist operational and engineering data. PostgreSQL is a strong open-source RDBMS; Java remains common in enterprise backends — including apps deployed on **JBoss EAP / WildFly**.

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

### If you know Python (`psycopg` / `psycopg2`)

| Python | Java on this track |
|--------|--------------------|
| `psycopg.connect(...)` | `DriverManager.getConnection` or `DataSource.getConnection` |
| `cur.execute("... %s ...", (badge,))` | `PreparedStatement` + `ps.setString(1, badge)` — **`?` placeholders**, not `%s` |
| `conn.commit()` / context manager | `conn.commit()` / `rollback()`; **try-with-resources** closes the connection |
| `f"SELECT … '{badge}'"` | Same crime: **SQL injection**. Forbidden in both languages. |
| SQLAlchemy ORM | Not the lab default — raw JDBC first (like writing SQL in `psycopg`) |

The SQL is the same. The ceremony (checked `SQLException`, pools, JNDI) is why Java looks longer. Submit **Java**.

## Prerequisites

- **PostgreSQL on a lab VM** (or a host/IP the instructor assigns) — course standard is **VMs, not Docker**  
- JDK (lab may still target **Java 8** on operational stacks; learning installs often use 17+)  
- Maven dependency:

```xml
<dependency>
  <groupId>org.postgresql</groupId>
  <artifactId>postgresql</artifactId>
  <version>42.7.4</version>
</dependency>
```

### Lab database (VM)

Use the **Postgres service on your assigned VM** (or shared lab DB VM). From the guest or your workstation:

```bash
# On the DB VM (examples — names vary by lab image)
sudo systemctl status postgresql
# or: sudo systemctl status postgresql-16

psql --version
sudo -u postgres psql -c "\l"
```

Record from the lab sheet:

| Item | Example |
|------|---------|
| Host / IP | `pg-lab-01.example.local` or VM IP |
| Port | `5432` |
| Database | `cisslab` |
| User / password | instructor-provided (env vars, not Git) |

Connection URL shape:

```text
jdbc:postgresql://<host>:5432/cisslab
```

If your Java process runs **on the same VM** as Postgres, `localhost` is fine. If it runs on another VM or your laptop, use the **DB VM hostname or IP** and ensure firewall/`pg_hba.conf` allow the path (coordinate with admin track — do not open networks casually).

```bash
# Reachability check from the client host
ping -c 2 <db-host>
ss -lntp | grep 5432          # on the DB VM: is Postgres listening?
psql "host=<db-host> port=5432 dbname=cisslab user=<user>" -c 'SELECT 1'
```

## Connection essentials (DriverManager)

Simplest path for small labs and one-shot tools:

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
3. Opening a new TCP connection + auth on **every** request is expensive — that is why production code uses pools.

---

## Connection pools and DataSource

### Why pool?

| Cost of a new connection | What a pool does |
|--------------------------|------------------|
| TCP handshake, auth, session setup | Keep a set of **ready** connections |
| Latency under load | Borrow / return instead of connect / close |
| Risk of exhausting Postgres `max_connections` | Cap concurrent app connections |

A **connection pool** implements (or sits behind) `javax.sql.DataSource`:

```text
App thread  →  dataSource.getConnection()  →  borrowed Connection
                     │
              [ idle pool of N connections ]
                     │
              conn.close() returns to pool (does not drop TCP)
```

### App-managed pool — HikariCP (common standalone choice)

```xml
<dependency>
  <groupId>com.zaxxer</groupId>
  <artifactId>HikariCP</artifactId>
  <version>5.1.0</version>
</dependency>
```

```java
HikariConfig cfg = new HikariConfig();
cfg.setJdbcUrl(url);
cfg.setUsername(user);
cfg.setPassword(pass);
cfg.setMaximumPoolSize(10);          // tune with DBA / load tests
cfg.setMinimumIdle(2);
cfg.setConnectionTimeout(30_000);
cfg.setPoolName("ciss-pg-pool");

HikariDataSource ds = new HikariDataSource(cfg);

try (Connection conn = ds.getConnection()) {
    // same JDBC as before
}
// on shutdown:
ds.close();
```

**Daemon / service rule:** create **one** pool per process (or per distinct database), not one pool per request.

### Tuning knobs (know the names)

| Setting | Meaning |
|---------|---------|
| `maximumPoolSize` | Hard cap on concurrent connections from this app |
| `minimumIdle` | Connections kept warm |
| `connectionTimeout` | How long to wait for a free connection before failing |
| `idleTimeout` / `maxLifetime` | Recycle stale connections |
| `validation` / test query | Detect dead connections before borrow |

Sum of all app pools + admin sessions must stay under Postgres `max_connections`.

---

## JBoss / WildFly: datasources in standalone config

On **JBoss EAP** or **WildFly**, the preferred production pattern is often a **container-managed datasource** defined in server config (not hard-coded pool settings inside every WAR/JAR).

### Where it lives

Typical file: `standalone/configuration/standalone.xml` (or `standalone-full.xml`, domain profiles, etc.) **on the app-server VM**.

Illustrative fragment (names and drivers vary by program):

```xml
<subsystem xmlns="urn:jboss:domain:datasources:…">
  <datasources>
    <datasource jndi-name="java:jboss/datasources/CissDS"
                pool-name="CissDS"
                enabled="true"
                use-java-context="true">
      <connection-url>jdbc:postgresql://dbhost:5432/cisslab</connection-url>
      <driver>postgresql</driver>
      <security>
        <user-name>…</user-name>
        <password>…</password>   <!-- prefer credential store / vault in real systems -->
      </security>
      <pool>
        <min-pool-size>5</min-pool-size>
        <max-pool-size>30</max-pool-size>
      </pool>
      <validation>
        <valid-connection-checker
          class-name="org.jboss.jca.adapters.jdbc.extensions.postgres.PostgreSQLValidConnectionChecker"/>
        <background-validation>true</background-validation>
      </validation>
    </datasource>

    <drivers>
      <driver name="postgresql" module="org.postgresql">
        <xa-datasource-class>org.postgresql.xa.PGXADataSource</xa-datasource-class>
      </driver>
    </drivers>
  </datasources>
</subsystem>
```

| Concept | Meaning |
|---------|---------|
| **`jndi-name`** | Lookup key apps use (e.g. `java:jboss/datasources/CissDS`) |
| **`pool-name`** | Server-side pool identity (metrics, admin console) |
| **Driver module** | Postgres JDBC packaged as a JBoss **module**, not always inside the app WAR |
| **XA datasource** | For multi-resource transactions (DB + JMS) — heavier; use when required |

Ops change pool size, URL, or credentials in **server config** (or management CLI) without rebuilding the application — when the app only depends on the JNDI name.

### Using the datasource from Java

**1. JNDI lookup (works in servlets, EJBs, plain code in the container)**

```java
import javax.naming.InitialContext;
import javax.sql.DataSource;
import java.sql.Connection;

InitialContext ic = new InitialContext();
DataSource ds = (DataSource) ic.lookup("java:jboss/datasources/CissDS");

try (Connection conn = ds.getConnection()) {
    // PreparedStatement work — same as lab JDBC
}
```

**2. Injection (EE components)**

```java
import javax.annotation.Resource;
import javax.sql.DataSource;

@Resource(lookup = "java:jboss/datasources/CissDS")
private DataSource ds;
```

After injection or lookup, **all SQL looks the same** — only acquisition of `Connection` changed.

### What you do *not* do in the app when using container DS

- Do not also create a second Hikari pool to the same DB “just in case” without capacity planning.  
- Do not call `DriverManager.getConnection` for the same workload in production code paths.  
- Do not store the password in `persistence.xml` *and* duplicate it in standalone unless the program standard says so — one source of truth.

---

## Trade-offs: how should we get connections?

| Approach | Best when | Pros | Cons |
|----------|-----------|------|------|
| **`DriverManager`** | Scripts, drills, tiny tools | Zero config, obvious | No pooling; poor under concurrency |
| **App pool (HikariCP, etc.)** | Standalone daemons, Spring Boot, non-EE fat jars | Fast, portable, app-owned tuning | Every process has its own pool; secrets/config in app or env; no shared server console |
| **JBoss/WildFly datasource (JNDI)** | Apps deployed to EAP/WildFly | Ops-managed pools; one place for URL/creds; integrates with container TX / monitoring | Requires server config + modules; local unit tests need mocks or an embedded DS; less portable outside the app server |
| **XA datasource** | Single TX across DB + JMS (or multiple DBs) | Atomic multi-resource commit | Complexity, failure modes, performance cost — avoid unless the requirement is real |

**Practical guidance for this program**

1. **Lab / course projects:** `DriverManager` first, then HikariCP once you feel the pain.  
2. **Long-running standalone workers:** one Hikari (or similar) pool per DB, closed on shutdown.  
3. **Services on JBoss:** prefer the **named datasource** in `standalone.xml` (or equivalent) and JNDI/`@Resource`.  
4. Always size pools against **Postgres `max_connections`** and the number of app instances.

```text
Instances × maxPoolSize  ≤  (Postgres max_connections − headroom for admins/migrations)
```

---

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
String sql =
    "SELECT id, badge_code, full_name " +
    "FROM employee " +
    "WHERE badge_code = ?";
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

On JBoss with **JTA**, EE components may use container-managed transactions instead of bare `commit`/`rollback` — same need for clear unit-of-work boundaries.

Example invariant: “check-in event only if not already checked in today” — read + write in one transaction (or enforce with constraints + careful SQL).

## Small design: repository boundary

Keep SQL out of UI / HTTP handlers:

```text
App / Service  →  EmployeeRepository  →  DataSource / JDBC  →  PostgreSQL
```

Inject or pass a `DataSource` into the repository — not a single long-lived `Connection`.

## Errors you will see

| Symptom | Checks |
|---------|--------|
| `Connection refused` | Postgres up on the **VM**? `systemctl status`? Port 5432 listening? Firewall between client VM and DB VM? |
| `FATAL: password authentication failed` | User/password env or standalone security block; `pg_hba.conf` |
| `relation "employee" does not exist` | Migrations / SQL not applied on that database |
| `SSL error` | URL sslmode for TLS-required environments |
| `NameNotFoundException` on lookup | Wrong JNDI name; datasource not deployed; wrong server profile |
| `Timeout waiting for connection` | Pool exhausted — leak (connection not closed) or undersized pool |
| `FATAL: too many connections` | Sum of pools > `max_connections` |

## Drill (45 min)

1. Confirm Postgres on the **lab VM** (`systemctl status`, `psql`).  
2. Apply the schema SQL (instructor DB or your lab database).  
3. Java program: insert one employee; query by badge; print result (`DriverManager`). Use the real host/IP in `CISS_JDBC_URL` if not local.  
4. Refactor to **HikariCP** `DataSource`; confirm behavior unchanged.  
5. Attempt a duplicate `badge_code`; handle `SQLException` cleanly.  
6. Write 5 bullets: when you would use JBoss `java:jboss/datasources/…` instead of Hikari in-process.  
7. Optional: insert `CHECK_IN` in a transaction.  

Commit to Git with a message that does **not** include passwords.

## Integrity & security

- Lab passwords only in env / local untracked config / approved server credential stores.  
- No production credentials in screenshots for submission.  
- Parameterize every query.  
- Always close connections (try-with-resources) so pools do not leak.

## Further reading

| Topic | Source |
|-------|--------|
| PostgreSQL JDBC | [JDBC Driver docs](https://jdbc.postgresql.org/documentation/) |
| PostgreSQL tutorial | [postgresql.org/docs/current/tutorial.html](https://www.postgresql.org/docs/current/tutorial.html) |
| SQL injection | [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) |
| HikariCP | [HikariCP](https://github.com/brettwooldridge/HikariCP) |
| JBoss datasources | Red Hat JBoss EAP / WildFly “Datasource Management” docs (version-matched) |
| Admin track | **PostgreSQL Database Management for Admins** |

## Next

**AMQP messaging with Java** — publish and consume messages; connection factories and pooling on the broker side.
