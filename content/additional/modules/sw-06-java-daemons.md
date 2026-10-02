# Java Daemons and Background Services

## Learning outcomes

After this module you can:

- Explain what a **daemon / background service** is (vs a one-shot CLI)  
- Structure a long-running Java process with a clear **lifecycle** (start → run → shutdown)  
- Host an **AMQP consumer** or **scheduled job** inside that process  
- Handle **SIGINT/SIGTERM** and graceful shutdown  
- Add minimal **health / logging** so ops can see if it is alive  

## Why daemons matter

Many systems are not “request/response only.” They need processes that:

| Job | Example |
|-----|---------|
| Drain queues | ActiveMQ / JMS consumer writing to PostgreSQL |
| Poll external systems | Import TEMPO-like files on a schedule |
| Run periodic calculations | Nightly summary recompute |
| Bridge protocols | Protocol adapter between bus and REST |

SE link: a daemon is a **runtime component** you allocate requirements to (`FR-…` → `CheckInConsumerService`).

## CLI vs daemon

| One-shot CLI | Daemon / service |
|--------------|------------------|
| `main` runs task and **exits** | `main` runs until **signaled to stop** |
| Easy to cron externally | Embeds loop / listeners |
| No long-held connections | Holds DB pool, AMQP channel, timers |

Both are valid. Prefer **external scheduler + short job** when possible; use an in-process daemon when you need continuous listeners (message consumers).

### If you know Python

```python
# Familiar shape — not the lab deliverable
import signal, time
stop = False
def handle(sig, frame):
    global stop
    stop = True
signal.signal(signal.SIGINT, handle)
while not stop:
    time.sleep(1)
```

| Python | Java |
|--------|------|
| `signal.signal` / `try/finally` | `Runtime.addShutdownHook` + `CountDownLatch` |
| `while True:` + `time.sleep` | Latch `await`, or a `ScheduledExecutorService` |
| `systemd` `Type=simple` ExecStart=`python worker.py` | Same systemd idea; **ExecStart** is `java -jar` / `java -cp … Main` |

The ops story is identical. The process you install on the VM is a **JVM**.

## Lifecycle pattern

```text
START
  load config / env
  open resources (DB, AMQP)
  start workers / consumers / schedulers
RUN
  block (CountDownLatch / Thread.join / wait on channel)
SHUTDOWN (hook)
  stop accepting work
  finish or nack in-flight carefully
  close consumers, channels, pools
  exit 0
```

### Skeleton

```java
public final class WorkerMain {
    private static final Logger log = LoggerFactory.getLogger(WorkerMain.class);
    private static final CountDownLatch shutdown = new CountDownLatch(1);

    public static void main(String[] args) throws Exception {
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            log.info("Shutdown signal received");
            shutdown.countDown();
        }, "shutdown-hook"));

        Config cfg = Config.fromEnv();
        try (AppContext ctx = AppContext.start(cfg)) {
            ctx.startConsumers();
            log.info("Worker running");
            shutdown.await();          // block until SIGINT/SIGTERM
            ctx.stopConsumers();
        }
        log.info("Worker stopped cleanly");
    }
}
```

On Windows, stop with **Ctrl+C** in the terminal; in labs/containers, orchestrators send **SIGTERM**.

## Hosting an ActiveMQ / JMS consumer

From the AMQP/ActiveMQ module: an async `MessageListener` needs the process to **stay alive**.

```java
MessageConsumer consumer = session.createConsumer(queue);
consumer.setMessageListener(message -> {
    // process quickly or hand off to an executor
});
connection.start();
shutdown.await(); // do not exit main
// on shutdown: close consumer, session, connection in reverse order
```

### Threading notes

- JMS may deliver on client library threads — keep handlers **short** or hand off to an `ExecutorService`.  
- Cap pool size; never unbounded thread creation.  
- Prefer **CLIENT_ACKNOWLEDGE** (or transactions) when DB writes must complete before ack.

## Scheduled jobs (in-process)

Simple approach — `ScheduledExecutorService`:

```java
ScheduledExecutorService sched =
    Executors.newSingleThreadScheduledExecutor(r -> {
        Thread t = new Thread(r, "nightly-job");
        t.setDaemon(false);
        return t;
    });

sched.scheduleAtFixedRate(
    () -> {
        try {
            summaryJob.runOnce();
        } catch (Exception e) {
            log.error("Job failed", e); // do not kill the whole JVM silently
        }
    },
    0, 15, TimeUnit.MINUTES
);

// on shutdown:
sched.shutdown();
sched.awaitTermination(30, TimeUnit.SECONDS);
```

| Habit | Why |
|-------|-----|
| Catch exceptions inside the job | Uncaught exceptions can cancel future schedules |
| Overlap guard | Skip if previous run still going (`AtomicBoolean`) |
| Config intervals via env | Ops can tune without recompile |

External **cron / systemd timer** + one-shot `main` is often easier to observe — know both options.

## Configuration

Daemons should read **environment variables** (12-factor style):

```text
CISS_JDBC_URL=
CISS_AMQP_HOST=
CISS_QUEUE_NAME=
CISS_JOB_INTERVAL_SEC=900
```

Fail fast at startup if required config is missing (log clearly, exit non-zero).

## Observability (minimum bar)

1. **Structured logs** — start/stop, message id processed, job duration.  
2. **Health** — even a simple `/healthz` HTTP port **or** a heartbeat file touch.  
3. **Metrics later** — counts of success/fail (optional in this course).  

If nobody can tell whether the daemon is alive, it will fail silently in production.

## Packaging & run

```bash
mvn -q -DskipTests package
java -jar target/worker-1.0.0.jar
```

Lab: run under VS Code **Java** launch config with env vars, or terminal.  
Admin track (later): systemd unit, Docker `CMD`, restart policies.

## Drill (45 min)

Build a tiny “worker” project that:

1. Connects to **ActiveMQ** (or simulates with a `BlockingQueue` if no broker).  
2. Consumes messages and appends a line to a local file or Postgres table.  
3. Stays running until Ctrl+C.  
4. Logs “shutdown complete” only after the consumer is closed.  
5. Optional: branch `DR-###`, push to **GitLab**, open an **MR** (program equivalent: Bitbucket **PR**).  

Stretch: add a scheduled job that prints queue depth or row counts every minute.

## Common failures

| Symptom | Checks |
|---------|--------|
| Process exits immediately | You forgot to block `main` after `basicConsume` |
| Messages pile up | Consumer crashed; autoAck false without ack; exception loop |
| Duplicate side effects | Need idempotency keys |
| “Works until Ctrl+C hangs” | Shutdown hook deadlock; close order wrong; await timeout |

## Integrity

- Lab-only credentials.  
- Do not install uncontrolled background services on shared machines without permission.  
- Same AI citation rules as other modules.

## Further reading

| Topic | Source |
|-------|--------|
| ActiveMQ / JMS | [ActiveMQ Classic docs](https://activemq.apache.org/components/classic/documentation/) · course **AMQP Messaging with Java (ActiveMQ)** |
| 12-factor config | [12factor.net/config](https://12factor.net/config) |
| Graceful shutdown | Search “Java shutdown hook graceful” + your framework docs |
| systemd (ops follow-on) | [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) |

## Next

**JavaFX for Desktop GUIs** — build desktop operator/engineer UIs; keep slow work off the UI thread (pair with DB/AMQP services).
