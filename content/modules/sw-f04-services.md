# Services, not scripts

> **When:** Week 4 · Wednesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [sw-fa04-services — Service conversation sketch](/assignments/sw-fa04-services) (~2 hours), due **Week 4 Thursday morning**.

## Learning outcomes

After this afternoon you can:

- Sketch a process that talks to a database
- Sketch a process that publishes or consumes a message
- List ICD fields before anyone writes a parser
- Place those processes on VMs, not as Docker-first

## Why this afternoon exists

PRSAS is not a notebook script. It is simulators, a daemon, a broker, a database, and a client. This afternoon is the shape — not JDBC.

## Teach

A **service** is a long-running process with a clear job, a failure story, and a contract.

```text
Producer  →  broker topic  →  consumer / daemon  →  database
                                      ↓
                                   client
```

**ICD before parser:** field name, type/units, who sends, who receives, rate, what happens when it is late. SE owns the contract language; Software implements it.

CISS runtime: **VMs** (vSphere guests). Docker may appear later as a PoC, not as the default.

Hold: connection pools, JMS factories, JavaFX threads, Jenkins.

## In-class exercise (30–40 min)

Boxes: simulator, broker, daemon, DB, client. Label one ICD between simulator and daemon (five fields). Label who owns each box (SW/NET/ADMIN/SE).

## Tomorrow morning

Do **sw-fa04-services** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
