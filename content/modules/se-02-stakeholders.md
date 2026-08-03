# Stakeholders, Context & Boundaries

## Learning outcomes

- List stakeholders and their **concerns**
- Draw a simple **context diagram**
- Write clear **in-scope / out-of-scope**

## Stakeholders

A stakeholder is anyone who cares about the system’s success or failure.

For SDC Time Tracker examples:

| Stakeholder | Cares about |
|-------------|-------------|
| Employee | Fast punch, leave balance, fair rules |
| Manager | Approvals, declared vs submitted time |
| Program / FOSC admin | Contract Excel package, TEMPO shortfalls |
| IT / security | PIN safety, audit trail |
| Systems engineer | Traceability, testability |

**Tip:** If you cannot name who cares, you do not understand the system yet.

## Operational need

Write need in **user/operator language**, not code language.

> SDC staff supporting FOSC must record attendance that is auditable, matches schedule rules, supports leave, and exports for contract submission with TEMPO comparison.

## Context diagram

Show:

- Actors (people)
- Your system (one box)
- External systems
- Arrows labeled with *what* flows (not every API path)

```
Employee ──PIN / punches──► [ SDC Time Tracker ] ──import──► TEMPO
Manager  ──approve/export─► [                 ] ──xlsx───► FOSC package
```

## System boundary

| In scope (example) | Out of scope (example) |
|--------------------|------------------------|
| Check-in state machine | Replacing TEMPO itself |
| BEOD credit rules | Payroll tax calculation |
| Discrepancy Tracker sheet | Multi-company HRIS |

Boundaries stop **scope creep** and clarify interfaces.

## Workshop (Monday)

In pairs (15 min):

1. Stakeholder table (min 4 rows) for either ETAS or a simple library app  
2. Three in-scope and three out-of-scope bullets  
3. One context sketch  

## Assignment A1

See **Assignments → A1 Context & Stakeholders**. Due Week 2 Thursday.

## Next

**Requirements & Acceptance Criteria** — turning concerns into shall statements.
