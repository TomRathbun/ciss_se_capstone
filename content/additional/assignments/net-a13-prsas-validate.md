# NET-A13 — Path Validation & Config Guide

**Phase:** capstone · **Weight:** 30% of capstone-NET · **Due:** After net-13 · **Module:** net-13-prsas-validate

## Prompt

Prove the **app path** and leave a replayable **configuration guide**.

## Deliverables

1. Six-layer evidence table (L2 → TLS/app).
2. Negative test: 5432 or 8161 from radar VLAN fails.
3. Bounded scan/hit-count note (command + result).
4. Configuration guide (chapters in net-13).
5. One-page “how SW reaches AMQ” handout.
6. Backout notes (`rollback` / confirmed commit).

## Quality bar

- ICMP-only packs fail.
- No full-network scans.
- Guide is executable, not a memoir.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| evidence | 15 | Layered, includes 61617 |
| guide | 10 | Replayable; backout present |
| communication | 5 | SW handout is short and true |
