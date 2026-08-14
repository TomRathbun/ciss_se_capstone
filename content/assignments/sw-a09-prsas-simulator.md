# SW-A09 — Radar Message Simulator

**Phase:** capstone · **Weight:** 25% of capstone-SW · **Due:** After sw-09 · **Module:** sw-09-prsas-simulator

## Prompt

Ship a **Java** simulator that publishes CISS-TEACH-1 messages to `radar.input`.

## Deliverables

1. Maven project with site A and site B configs (`sic` / `source_id` differ).
2. Scenario file format + **four** scenarios (happy, agree, conflict, dropout).
3. TLS JMS (or approved STOMP) publisher; runbook with broker URL (no secrets).
4. Start/stop/throttle evidence (CLI flags OK).
5. Log excerpt: ≥ 3 messages per site, `mode3a` valid.
6. Unit test: payload schema / Mode 3/A pattern.

## Quality bar

- Not a Python script as the graded artifact.
- No `trustAll` TLS.
- Kinematics documented (flat plane OK).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| publisher | 15 | Real publish path; two site identities |
| scenarios | 10 | Four scenarios; throttle/start-stop |
| communication | 5 | Runbook a peer can execute |
