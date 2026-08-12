# AMQP Messaging with Java (ActiveMQ)

## Learning outcomes

After this module you can:

- Explain **why** systems use messaging (decoupling, async, buffering)  
- Describe **AMQP / JMS** building blocks used with **Apache ActiveMQ**  
- Explain **ConnectionFactory**, **Connection**, **Session**, and **pooling**  
- **Publish** and **consume** messages from Java using the JMS API  
- Use an app-created factory **or** a **JBoss/WildFly** JNDI connection factory  
- Apply at-least-once habits: ack modes, idempotent consumers, clear payloads  
- State **trade-offs** between standalone clients and container-managed JMS resources  

## Why messaging on CISS-type systems

Not every integration should be a synchronous HTTP call.

| Problem | Messaging helps by… |
|---------|---------------------|
| Producer faster than consumer | Queue buffers work |
| Many consumers | Competing consumers scale out |
| Temporal decoupling | Publisher does not wait for handler |
| Integration across languages/services | Shared message contract (ICD for payloads) |

SE link: the **message schema** is an **interface**. Version it; document fields; do not break consumers silently.

## ActiveMQ + JMS mental model

This course uses **Apache ActiveMQ** (Classic) as the broker — matching the program environment more closely than RabbitMQ.

```text
Publisher  →  Destination (Queue or Topic)  →  Consumer
                 ▲
            ActiveMQ broker (lab VM)
```

| Piece | Role |
|-------|------|
| **Broker** | ActiveMQ process that stores and routes messages |
| **Queue** | Point-to-point: each message to one consumer |
| **Topic** | Pub/sub: each message to all active subscribers |
| **ConnectionFactory** | Creates `Connection` objects to the broker |
| **Connection** | TCP (or similar) session to the broker; start() before consume |
| **Session** | Context for producers/consumers; ack / transaction mode |
| **Producer / Consumer** | Send and receive |
| **Ack** | How the session confirms consumption |

JMS is the **Java API**; ActiveMQ is the **broker** implementing the wire protocol (OpenWire by default on `61616`).

```text
ConnectionFactory
       │ createConnection()
       ▼
   Connection  ──start()──►
       │ createSession(transacted, ackMode)
       ▼
    Session
     /      \
Producer   Consumer
```

## Lab broker (VM)

Course labs use **VMs, not Docker**. ActiveMQ runs as a service on an assigned guest (or shared broker VM).

```bash
# On the broker VM — service name varies by install
sudo systemctl status activemq
# or check the lab runbook for the exact unit name / install path

ss -lntp | grep 61616
```

| Port | Typical use |
|------|-------------|
| **61616** | OpenWire (Java client default) |
| **8161** | Web console (if enabled) |

From the lab sheet, record:

| Item | Example |
|------|---------|
| Broker host / IP | `amq-lab-01.example.local` |
| OpenWire URL | `tcp://amq-lab-01.example.local:61616` |
| Console | `http://amq-lab-01.example.local:8161` |
| User / password | instructor-provided |

Use `localhost` in the URL **only** when your client runs on the **same VM** as the broker. Otherwise use the broker VM hostname/IP and confirm firewall rules with the admin track.

```bash
# From the client host
ping -c 2 <broker-host>
# Optional: open console in a browser if allowed on the lab network
```

## Maven dependencies

```xml
<dependency>
  <groupId>org.apache.activemq</groupId>
  <artifactId>activemq-client</artifactId>
  <version>5.18.3</version>
</dependency>
<!-- If your JDK/lab uses Jakarta EE 9+ packaging, follow the instructor BOM;
     many labs still use javax.jms via activemq-client (Java 8 / older EAP). -->
```

Optional pooling helper (standalone apps):

```xml
<dependency>
  <groupId>org.apache.activemq</groupId>
  <artifactId>activemq-pool</artifactId>
  <version>5.18.3</version>
</dependency>
```

---

## ConnectionFactory essentials (standalone)

A **ConnectionFactory** is the object you configure once (broker URL, credentials, timeouts). You then create connections from it.

```java
String brokerUrl = System.getenv().getOrDefault(
    "CISS_AMQP_BROKER_URL", "tcp://localhost:61616");

ActiveMQConnectionFactory factory = new ActiveMQConnectionFactory(brokerUrl);
// Lab-only — never hard-code production passwords in Git
// factory.setUserName(...);
// factory.setPassword(...);

try (Connection connection = factory.createConnection()) {
    connection.start();
    Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
    // work…
    session.close();
}
```

Prefer env vars (set host to the **broker VM** when needed):

```text
CISS_AMQP_BROKER_URL=tcp://amq-lab-01.example.local:61616
CISS_AMQP_USER=...
CISS_AMQP_PASSWORD=...
CISS_AMQP_QUEUE=ciss.demo.events
```

### Why not one Connection per message?

Creating a connection is relatively expensive (network + auth). Patterns:

| Pattern | Typical use |
|---------|-------------|
| One connection, many sessions | Some clients; session is not always thread-safe |
| One connection per thread | Simple mental model |
| **Pooled ConnectionFactory** | Borrow/return connections under load |

JMS rule of thumb: a **Session** is generally **not thread-safe** — do not share one session across threads.

### Pooled ConnectionFactory (standalone)

```java
ActiveMQConnectionFactory raw =
    new ActiveMQConnectionFactory(System.getenv().getOrDefault(
        "CISS_AMQP_BROKER_URL", "tcp://localhost:61616"));

PooledConnectionFactory pooled = new PooledConnectionFactory();
pooled.setConnectionFactory(raw);
pooled.setMaxConnections(8);       // tune under guidance
pooled.setMaximumActiveSessionPerConnection(10);

Connection connection = pooled.createConnection();
try {
    connection.start();
    Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
    // …
    session.close();
} finally {
    connection.close();            // returns to pool when using pooled CF
}
// on JVM shutdown:
pooled.stop();
```

For long-running **consumers**, it is often clearer to hold **one dedicated connection** (or a small fixed set) for the life of the process rather than churning the pool on every message — pools shine for **many short-lived producers** (e.g. request threads sending one message each).

---

## JBoss / WildFly: connection factories in server config

On **JBoss EAP / WildFly** (typically on an **app-server VM**), JMS resources are often defined in the **messaging** subsystem (embedded Artemis on newer EAP, or a **resource adapter** to external ActiveMQ Classic — program-dependent). The idea is the same as datasources: **name it once in server config**, look it up from the app.

### What you will see in `standalone.xml` (illustrative)

**A. Embedded / subsystem connection factory (Artemis-style naming varies by version):**

```xml
<!-- Conceptual — exact subsystem XML is version-specific -->
<connection-factory name="CissConnectionFactory"
                    entries="java:/CissConnectionFactory java:jboss/DefaultJMSConnectionFactory"
                    connectors="in-vm"/>
```

**B. Resource adapter to an external ActiveMQ broker (common when the broker is on another VM):**

```xml
<!-- Conceptual resource-adapter snippet — follow your program’s exact module -->
<subsystem xmlns="urn:jboss:domain:resource-adapters:…">
  <resource-adapters>
    <resource-adapter id="activemq-rar">
      <!-- .rar module providing ActiveMQ inbound/outbound -->
      <connection-definitions>
        <connection-definition
            class-name="org.apache.activemq.ra.ActiveMQManagedConnectionFactory"
            jndi-name="java:/CissActiveMQConnectionFactory"
            pool-name="CissActiveMQPool">
          <config-property name="ServerUrl">tcp://broker-host:61616</config-property>
          <!-- user/password via config or security domain -->
          <pool>
            <min-pool-size>2</min-pool-size>
            <max-pool-size>20</max-pool-size>
          </pool>
        </connection-definition>
      </connection-definitions>
    </resource-adapter>
  </resource-adapters>
</subsystem>
```

| Object | Role |
|--------|------|
| **Connection factory JNDI name** | What Java code looks up |
| **Admin object / destination** | Queue or topic bound in JNDI (optional but common) |
| **Pool** | Managed connections in the app server |
| **MDB activation config** | Message-driven beans consume without manual `MessageConsumer` loops |

Also common: destinations such as `java:/jms/queue/CissEvents` defined alongside the factory.

### Using the factory from Java

**1. JNDI lookup**

```java
import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.Session;
import javax.naming.InitialContext;

InitialContext ic = new InitialContext();
ConnectionFactory cf =
    (ConnectionFactory) ic.lookup("java:/CissActiveMQConnectionFactory");

try (Connection connection = cf.createConnection()) {
    connection.start();
    Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
    // createProducer / createConsumer as usual
    session.close();
}
```

**2. Injection**

```java
import javax.annotation.Resource;
import javax.jms.ConnectionFactory;
import javax.jms.Queue;

@Resource(lookup = "java:/CissActiveMQConnectionFactory")
private ConnectionFactory connectionFactory;

@Resource(lookup = "java:/jms/queue/CissEvents")
private Queue eventsQueue;
```

**3. Message-driven bean (container consumer)**

On full EE, an **MDB** can listen to a destination declared in activation config — the container holds the consumer lifecycle. You write `onMessage`, not a manual receive loop. Useful on JBoss; overkill for a tiny lab `main`.

### Pairing with datasources (XA note)

When **one business action** must update PostgreSQL **and** acknowledge/send JMS atomically, architectures use **XA** (two-phase commit) with an XA datasource + XA JMS connection factory under JTA.

| Choice | When |
|--------|------|
| Non-XA + careful order + idempotency | Most lab and many production flows |
| XA / JTA | Hard requirement for atomic multi-resource commit |

Prefer **idempotent consumers** and clear failure handling before introducing XA complexity.

---

## Trade-offs: factory strategies

| Approach | Best when | Pros | Cons |
|----------|-----------|------|------|
| **`new ActiveMQConnectionFactory(url)`** | Labs, simple tools | Explicit, easy to debug | Easy to forget pooling; config scattered in code/env |
| **Pooled CF in-app** (`activemq-pool`) | Standalone daemons / many short sends | Better connection reuse without EE | App owns pool lifecycle and tuning |
| **Long-lived single Connection** | Dedicated consumer process | Predictable; simple shutdown | Must handle reconnect on broker outage |
| **JBoss JNDI ConnectionFactory** | Apps on EAP/WildFly | Ops-managed URL/pool; shared naming; fits MDBs | Server config + RAR/module discipline; tests need container or mocks |
| **MDB (container listener)** | EE services on JBoss | Lifecycle, pooling, TX integration | Harder to run as plain `main`; server-centric |

**Practical guidance**

1. **Course drills:** plain `ActiveMQConnectionFactory` + one connection to the **lab broker VM**.  
2. **Standalone worker (daemons module):** dedicated connection(s) or a small pooled CF; reconnect policy documented.  
3. **War/EAR on JBoss:** look up `java:/…ConnectionFactory` (and destinations) defined in standalone (or the program’s resource adapter).  
4. Align with the **Postgres** module: same “app pool vs container resource” story — do not double-pool blindly.

---

## Publish to a queue

```java
Queue queue = session.createQueue("ciss.demo.events");
MessageProducer producer = session.createProducer(queue);
producer.setDeliveryMode(DeliveryMode.PERSISTENT);

String body = "{\"schemaVersion\":1,\"eventId\":\"" + UUID.randomUUID()
    + "\",\"type\":\"CHECK_IN\",\"badge\":\"E42\"}";

TextMessage message = session.createTextMessage(body);
message.setStringProperty("type", "CHECK_IN"); // optional filter-friendly header
producer.send(message);
```

If the queue is bound in JNDI on JBoss:

```java
Queue queue = (Queue) ic.lookup("java:/jms/queue/CissEvents");
```

## Consume from a queue

```java
Queue queue = session.createQueue("ciss.demo.events");
MessageConsumer consumer = session.createConsumer(queue);

// Blocking receive (simple lab)
Message msg = consumer.receive(5000); // 5s timeout
if (msg instanceof TextMessage) {
    TextMessage textMessage = (TextMessage) msg;
    String body = textMessage.getText();
    // process…
}

// Or async:
consumer.setMessageListener(message -> {
    try {
        if (message instanceof TextMessage) {
            handle(((TextMessage) message).getText());
        }
    } catch (Exception e) {
        // log; consider Session.CLIENT_ACKNOWLEDGE for finer control
        throw new RuntimeException(e);
    }
});
// keep process alive — see Daemons module
```

### Acknowledge modes (know these)

| Mode | Meaning |
|------|---------|
| `AUTO_ACKNOWLEDGE` | Session acks after `onMessage` returns successfully |
| `CLIENT_ACKNOWLEDGE` | You call `message.acknowledge()` after success |
| `DUPS_OK_ACKNOWLEDGE` | Lazy ack — possible duplicates |
| `SESSION_TRANSACTED` | Commit/rollback groups of messages |

For course work, start with **AUTO_ACKNOWLEDGE**, then practice **CLIENT_ACKNOWLEDGE** so you only ack after DB write succeeds.

## Topics (brief)

```java
Topic topic = session.createTopic("ciss.demo.alerts");
// producer.send(topic, message);
// multiple consumers each get a copy (while subscribed)
```

Use **queues** for work distribution; **topics** for fan-out notifications.

## Design habits

1. **Idempotent consumers** — same `eventId` twice must not double-apply side effects (unique key in PostgreSQL).  
2. **Contract first** — document queue name + JSON fields (lightweight ICD).  
3. **Don’t use the broker as system of record** — persist what matters in the DB.  
4. **Poison messages** — log, park, or dead-letter; don’t infinite-retry crash loops.  
5. **Close in reverse order** — consumer → producer → session → connection → stop pool.  

### Example payload contract (ICD-ish)

| Field | Type | Notes |
|-------|------|-------|
| `schemaVersion` | int | Start at 1 |
| `eventId` | uuid | Idempotency |
| `type` | string | e.g. `CHECK_IN` |
| `badge` | string | Employee key |
| `occurredAt` | ISO-8601 | Producer timestamp |

## Drill (45 min)

1. Confirm ActiveMQ on the **lab VM** (`systemctl status`, port `61616`).  
2. Publish 3 JSON `TextMessage`s to `ciss.demo.events` using a standalone `ActiveMQConnectionFactory` pointed at that host.  
3. Consume and print them; confirm queue depth drops in the console if available.  
4. Stop consumer, publish more, restart consumer — confirm drain.  
5. Sketch where a JBoss `java:/CissActiveMQConnectionFactory` would replace `new ActiveMQConnectionFactory`.  
6. Write 5 bullets on pool vs dedicated long-lived connection for a consumer daemon.  
7. Draw sequence: Producer → ActiveMQ queue → Consumer → DB (optional).  
8. Name your branch `DR-###` and open a **GitLab MR** for the CISS lab (same as a Bitbucket PR at work).  

## Integrity

- Lab credentials only; never commit broker passwords.  
- Do not publish classified operational data to shared brokers.

## Further reading

| Topic | Source |
|-------|--------|
| ActiveMQ Classic | [ActiveMQ documentation](https://activemq.apache.org/components/classic/documentation/) |
| activemq-pool | ActiveMQ “Connection Pooling” docs for your version |
| JMS overview | Search “Jakarta Messaging” / “JMS 2.0 tutorial” for API concepts |
| JBoss messaging / resource adapters | EAP/WildFly admin guides (version-matched) |
| EIP patterns | Hohpe & Woolf *Enterprise Integration Patterns* (overview online) |
| Team workflow | Course **Team Workflow: Jira / Bitbucket / Nexus → GitLab** |
| Postgres + pools | Course **PostgreSQL with Java (JDBC)** |

## Next

**Java Daemons and Background Services** — long-running processes that host ActiveMQ consumers and scheduled jobs.
