# Requirements that can be tested

> **When:** Week 3 · Monday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [se-fa03-requirements — Six testable shalls](/assignments/se-fa03-requirements) (~2 hours), due **Week 3 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Write a shall that can be tested without a meeting
- Use an EARS pattern (WHEN / WHILE / IF-THEN / ubiquitous)
- Write an acceptance criterion in Given/When/Then that proves a shall
- Keep design out of the requirement

## Why this afternoon exists

‘The system shall be user-friendly’ cannot be failed. Interns who cannot write a testable shall cannot later write an ICD or a lab procedure. This is the last foundation SE skill before we learn to *read* architecture.

## Teach

A **requirement** says what the system **shall** do. It stands alone. The acceptance criterion **proves** it; it does not explain it.

### EARS patterns (use the names)

| Pattern | Shape |
|---------|--------|
| Ubiquitous | The system shall … |
| Event-driven | WHEN <event> the system shall … |
| State-driven | WHILE <state> the system shall … |
| Unwanted | IF <condition> THEN the system shall … |

Give every FR an **ID** (`FR-FA03-01`). NFRs (latency, availability, classification of the lab) get IDs too.

### Acceptance criteria

```text
Given <precondition>
When  <action>
Then  <observable result>
```

The Then must be something a tester can see or log — not “the user is happy.”

### Design smuggling

If your shall names Java, Junos, Postgres, or a screen widget, you wrote a design. Put it in a decision record later. The shall stays about behavior.

SE-allocated_to: use case → requirement. Next week we only *read* structure. We do not allocate yet.

## In-class exercise (30–40 min)

From one use-case extension last week, write two EARS shalls (one IF/THEN) and one AC. Peer marks any shall that needs the AC to be understood.

## Tomorrow morning

Do **se-fa03-requirements** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
