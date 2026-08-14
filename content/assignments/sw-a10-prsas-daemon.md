# SW-A10 — Track Processing Daemon

**Phase:** capstone · **Weight:** 30% of capstone-SW · **Due:** After sw-10 · **Module:** sw-10-prsas-daemon

## Prompt

Implement the **central daemon**: consume, correlate, persist, publish, survive blips.

## Deliverables

1. Java worker with systemd unit (or equivalent documented).
2. Correlator tests: initiate, update, **conflict**, coast, drop.
3. JDBC upsert + history against the SE schema (or se-14 baseline, labelled).
4. Publish `SYSTEM_TRACK` to `radar.output`.
5. Failure notes: Postgres down, AMQ down, bad JSON.
6. Config via env/file — no passwords in Git.

## Quality bar

- Ack policy stated.
- CONFLICT does not silent-pick feed A.
- Graceful SIGTERM.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| lifecycle | 15 | States implemented and tested |
| persistence | 10 | Schema used; history exists |
| robustness | 5 | Blip behaviour documented |
