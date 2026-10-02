# Reading and writing code

> **When:** Week 3 · Wednesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [sw-fa03-reading-code — Requirement vs code vs secret](/assignments/sw-fa03-reading-code) (~2 hours), due **Week 3 Thursday morning**.

## Learning outcomes

After this afternoon you can:

- Read a short function and say what requirement it implements
- State the hiring bar: Python may be how you think; Java is the contract language
- Keep secrets out of Git
- Refuse to invent a requirement in code

## Why this afternoon exists

Interns ship clever code that nobody asked for. SE just taught you shalls. Software’s job is to implement them — in the language the program pays for.

## Teach

**Python** is allowed as a scratchpad. **Java** is what JDBC, JMS/ActiveMQ, daemons, and JavaFX labs will use. After the depth bridge module, graded work is Java.

When you read code, ask:

1. What shall is this?
2. What happens on failure?
3. Where would a secret leak?
4. What would a test look like?

```text
Requirement  →  code  →  test that can fail the shall
     ↑                        |
     └── if the code invents behavior, stop and write a shall
```

Secrets: connection passwords, private keys, tokens. Environment or a secrets file that is **gitignored**, never a screenshot in a ticket.

## In-class exercise (30–40 min)

Instructor shows a 15-line function (any language). Class: shall it implements, one failure path, one secret risk.

## Additional lesson

The long-form original is archived as **[sw-03-python-java](/modules/sw-03-python-java)**. Read it after class if you will keep this discipline.

## Hold for later

JDBC pools, ActiveMQ resource adapters, JavaFX, Jenkins. Depth.

## Tomorrow morning

Do **sw-fa03-reading-code** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
