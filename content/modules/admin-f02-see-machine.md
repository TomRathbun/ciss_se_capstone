# See what the machine is doing

> **When:** Week 2 · Thursday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [admin-fa02-see-machine — Evidence pack for a symptom](/assignments/admin-fa02-see-machine) (~2 hours), due **Week 2 Friday morning**.

## Learning outcomes

After this afternoon you can:

- Read logs without drowning
- Run symptom → hypothesis → test
- Tell incident vs change vs request
- Build an evidence pack a peer can reuse

## Why this afternoon exists

The difference between a useful intern and a dangerous one is whether they paste 4,000 lines of log or a hypothesis with a 20-line excerpt.

## Teach

**Method:** symptom (observable) → hypothesis (one) → test (command) → next hypothesis.

Tools for this afternoon: `journalctl`, `tail`, `grep`, `less`, `ps`, `ss`. You do not need to be a DBA.

**Tickets**

| Kind | Use |
|------|-----|
| Incident | Something is broken |
| Change | You will alter a system |
| Request | Please give me access / a VM |

A ticket without evidence is a rumor.

Hold: deep `strace`, tcpdump on shared hosts without permission.

## In-class exercise (30–40 min)

Symptom: ‘I cannot SSH.’ Three hypotheses (service down, firewall, wrong key). What command tests each? Write a four-field ticket: symptom, last change, evidence, ask.

## Additional lesson

The long-form original is archived as **[admin-09-troubleshooting](/modules/admin-09-troubleshooting)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **admin-fa02-see-machine** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
