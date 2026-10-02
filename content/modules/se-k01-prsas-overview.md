# PRSAS capstone overview

> **When:** Week 5 · Monday afternoon · Masdar
> **Who:** All interns (all-hands, including those who will later drop electives)
> **Tomorrow morning:** [se-ka01-overview — PRSAS one-minute brief](/assignments/se-ka01-overview) (~2 hours), due **Week 5 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Restate UC-CISS_PROJECT-001 in one minute
- Name the three VMware stacks and what lives on each
- Point at shared contracts (topics, ports, teaching payload)
- Keep unclassified / VM-first discipline

## Why this afternoon exists

Specialization without a shared problem produces four intern projects. This afternoon is the whole picture before anyone picks an elective.

## Teach

**PRSAS** — Prototype Radar Situational Awareness System. Unclassified lab. Not a live C2.

Two simulated radars (Remote A, Remote B) publish ASTERIX-*like* Category 062 messages (Mode 3/A present) across a secured path to Central: ActiveMQ (`radar.input`) → track daemon → PostgreSQL → `radar.output` → authenticated client.

Read the live module [se-12-prsas-overview](/modules/se-12-prsas-overview) after class. Contracts freeze there: ports (**61617** TLS), topics, CISS-TEACH-1 JSON payload. Do not claim official ASTERIX encoding.

Electives open **next week**. SE remains mandatory. Networking, Software, and Admin continue only if you stay in those rooms.

Military lectures remain Friday-flex and **TAA-gated** — not part of this kickoff.

## In-class exercise (30–40 min)

In four mixed groups: 60-second brief of the picture with no notes. Peer group marks anything that sounded like a live air-defense system.

## Additional lesson

The long-form original is archived as **[se-12-prsas-overview](/modules/se-12-prsas-overview)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **se-ka01-overview** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
