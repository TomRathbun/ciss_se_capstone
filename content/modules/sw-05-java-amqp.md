# AMQP Messaging with Java (ActiveMQ)

## Learning outcomes

After this module you can:

- Explain **why** systems use messaging (decoupling, async, buffering)  
- Describe **AMQP / JMS** building blocks used with **Apache ActiveMQ**  
- **Publish** and **consume** messages from Java using the JMS API  
- Apply at-least-once habits: ack modes, idempotent consumers, clear payloads  

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
            ActiveMQ broker
```

| Piece | Role |
|-------|------|
| **Broker** | ActiveMQ process that stores and routes messages |
| **Queue** | Point-to-point: each message to one consumer |
| **Topic** | Pub/sub: each message to all active subscribers |
| **Connection / Session** | JMS handles to the broker |
| **Producer / Consumer** | Send and receive |
| **Ack** | How the session confirms consumption |

JMS is the **Java API**; ActiveMQ is the **broker** implementing the wire protocol (OpenWire by default on `61616`).

## Lab broker (Docker)

```bash
docker run --name ciss-activemq -p 61616:61616 -p 8161:8161 -d apache/activemq-classic:5.18.3
# Web console often at http://localhost:8161  (default lab user/pass per image docs — lab only)
```

| Port | Typical use |
|------|-------------|
| **61616** | OpenWire (Java client default) |
| **8161** | Web console |

Confirm exact image/tag and credentials with your lab notes if the default image differs.

## Maven dependencies

```xml
<dependency>
  <groupId>org.apache.activemq</groupId>
  <artifactId>activemq-client</artifactId>
  <version>5.18.3</version>
</dependency>
<!-- If your JDK/lab uses Jakarta EE 9+ packaging, follow the instructor BOM;
     many labs still use javax.jms via activemq-client. -->
```

## Connection essentials

```java
String brokerUrl = System.getenv().getOrDefault(
    "CISS_AMQP_BROKER_URL", "tcp://localhost:61616");

ActiveMQConnectionFactory factory = new ActiveMQConnectionFactory(brokerUrl);
// Lab-only defaults — never hard-code production passwords in Git
// factory.setUserName(...); factory.setPassword(...);

try (Connection connection = factory.createConnection()) {
    connection.start();
    Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
    // work…
    session.close();
}
```

Prefer env vars:

```text
CISS_AMQP_BROKER_URL=tcp://localhost:61616
CISS_AMQP_USER=...
CISS_AMQP_PASSWORD=...
CISS_AMQP_QUEUE=ciss.demo.events
```

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

## Consume from a queue

```java
Queue queue = session.createQueue("ciss.demo.events");
MessageConsumer consumer = session.createConsumer(queue);

// Blocking receive (simple lab)
Message msg = consumer.receive(5000); // 5s timeout
if (msg instanceof TextMessage textMessage) {
    String body = textMessage.getText();
    // process…
}

// Or async:
consumer.setMessageListener(message -> {
    try {
        if (message instanceof TextMessage tm) {
            handle(tm.getText());
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

### Example payload contract (ICD-ish)

| Field | Type | Notes |
|-------|------|-------|
| `schemaVersion` | int | Start at 1 |
| `eventId` | uuid | Idempotency |
| `type` | string | e.g. `CHECK_IN` |
| `badge` | string | Employee key |
| `occurredAt` | ISO-8601 | Producer timestamp |

## Drill (40 min)

1. Start ActiveMQ.  
2. Publish 3 JSON `TextMessage`s to `ciss.demo.events`.  
3. Consume and print them; confirm queue depth drops in the console.  
4. Stop consumer, publish more, restart consumer — confirm drain.  
5. Draw sequence: Producer → ActiveMQ queue → Consumer → DB (optional).  
6. Name your branch `DR-###` and open a **GitLab MR** for the CISS lab (same as a Bitbucket PR at work).  

## Integrity

- Lab credentials only; never commit broker passwords.  
- Do not publish classified operational data to shared brokers.

## Further reading

| Topic | Source |
|-------|--------|
| ActiveMQ Classic | [ActiveMQ documentation](https://activemq.apache.org/components/classic/documentation/) |
| JMS overview | Search “Jakarta Messaging” / “JMS 2.0 tutorial” for API concepts |
| EIP patterns | Hohpe & Woolf *Enterprise Integration Patterns* (overview online) |
| Team workflow | Course **Team Workflow: Jira / Bitbucket / Nexus → GitLab** |

## Next

**Java Daemons and Background Services** — long-running processes that host ActiveMQ consumers and scheduled jobs.
