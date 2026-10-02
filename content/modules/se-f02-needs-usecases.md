# Needs → use cases

> **When:** Week 2 · Monday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [se-fa02-needs-usecases — Needs and two use-case briefs](/assignments/se-fa02-needs-usecases) (~2 hours), due **Week 2 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Write a need as As … we need … so that …
- Turn a need into a use case with actor, goal, and main success scenario
- Write at least one extension (failure/alternate path)
- Reject a use case that is really a design

## Why this afternoon exists

Requirements written without needs become a wishlist. Use cases without extensions become happy-path fiction. This afternoon is how people actually use a system — still not how we will build it.

## Teach

### Needs grammar

```text
As  <stakeholder>,
we need  <capability>,
so that  <outcome they care about>.
```

Bad: “As a user we need a Kubernetes cluster so that it is modern.”
Good: “As a supervisor we need one defensible air picture so that we do not brief two different tracks as truth.”

Needs **derives_from** the vision. If you cannot point at the vision sentence, it is not a need yet.

### Use cases

A **use case** is a goal-oriented interaction: an **actor** wants an **outcome**.

| Field | Put this |
|-------|----------|
| Name | Verb-noun, goal-shaped (`Correlate dual feeds`) |
| Actor | Who is trying |
| Goal | What success looks like |
| Main success scenario | Numbered steps, no UI chrome |
| Extensions | `3a` if the second feed disagrees… |

**traces_to:** need → use case. One need can fan out.

### Reject list

A use case is **not**: a screen layout, a vendor name, a protocol, a class name, “make it fast.” Those are design or NFRs. Write them down as *rejected — design* so they do not sneak back in.

## In-class exercise (30–40 min)

Take yesterday’s daily-app vision. Write two needs in grammar. Turn one into a use case with a main scenario (5–8 steps) and one extension. Reject one fake use case that is actually a design.

## Tomorrow morning

Do **se-fa02-needs-usecases** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
