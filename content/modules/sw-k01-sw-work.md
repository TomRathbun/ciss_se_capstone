# Software work on the capstone

> **When:** Week 5 · Wednesday afternoon · Masdar
> **Who:** All interns this week; elective from week 6
> **Tomorrow morning:** [sw-ka01-sw-work — SW accomplishment list](/assignments/sw-ka01-sw-work) (~2 hours), due **Week 5 Thursday morning**.

## Learning outcomes

After this afternoon you can:

- List simulator, daemon, client, integration as four jobs
- Refuse to invent the schema or the ICD
- See containers as a later PoC, not the default runtime

## Why this afternoon exists

Three applications, one picture. If Software starts with a GUI, the daemon and ICD lose.

## Teach

**Software must accomplish**

- Radar-message simulators on Remote A and B (CISS-TEACH-1, TLS to `radar.input`)
- Track-processing daemon (Mode 3/A correlate, persist, `radar.output`)
- Authenticated SA client (bulk load + live)
- Integration test card; container PoC of two components for the SE virt study

**Software does not** invent the Postgres schema without SE or talk to live radars.

Depth starts the Java bridge next week for those who stay. Live modules: [sw-09](/modules/sw-09-prsas-simulator) onward.

## In-class exercise (30–40 min)

Order the four jobs. Name the SE artifact each one requires before code. Name the NET/ADMIN artifact each one requires before it can run.

## Additional lesson

The long-form original is archived as **[sw-09-prsas-simulator](/modules/sw-09-prsas-simulator)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **sw-ka01-sw-work** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
