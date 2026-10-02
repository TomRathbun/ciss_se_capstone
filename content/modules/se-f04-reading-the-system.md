# Reading the system

> **When:** Week 4 · Monday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [se-fa04-reading-system — Context sketch and V&V note](/assignments/se-fa04-reading-system) (~2 hours), due **Week 4 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Read a context diagram (who is outside the box)
- Tell structure (containers) from deployment (VMs)
- Read a simple sequence and a simple state
- Say verify vs validate in one sentence each
- Explain how SE will coordinate Network, Admin, and Software

## Why this afternoon exists

Next week we open PRSAS. You must be able to look at a picture and not confuse ‘who talks to whom’ with ‘which VM it runs on’ with ‘what we will test.’

## Teach

### Three views (do not mix them)

| View | Question it answers |
|------|---------------------|
| **Context** | Who/what is outside our system? |
| **Structure / containers** | What major pieces exist and what they owe each other? |
| **Deployment** | Where does it run? (For CISS: **VMs**, not Docker-first) |

A sequence diagram is **behavior over time**. A state machine is **legal vs illegal modes**. You do not need SysML fluency this week. You need to *read* them.

```text
Actor → Client → Daemon → Database
         │          │
         └─ messages over a broker
```

### Verify vs validate

| | Question |
|--|----------|
| **Verify** | Did we build it right? (tests against shalls) |
| **Validate** | Did we build the right thing? (operator / stakeholder) |

A passing unit test that nobody wanted is verified and not validated.

### How SE coordinates the other three

| Track | SE asks them for |
|-------|------------------|
| Software | Implementation of shalls and ICDs |
| Networking | Path, ports, protection matching NFRs |
| Admin | Runtime (VMs, identity, certs) that V&V can stand on |

SE does not write Junos or Java as the system of record. SE owns the **shared contracts** the others build against.

## In-class exercise (30–40 min)

Given a three-box sketch (client, daemon, DB): label context vs structure vs deployment. Write one sequence (login → load → live update). Write one verify activity and one validate activity for a shall from last week.

## Hold for later

Full architecture allocation, hierarchical states, messaging ICDs, MBSE frameworks. Depth starts week 6. PRSAS itself is next Monday.

## Tomorrow morning

Do **se-fa04-reading-system** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
