# SW-A06 — Java Daemon / Worker

**Weight:** 10% · **Due:** After sw-06-java-daemons · **Module:** sw-06-java-daemons

## Prompt

Turn background work into a **long-running process** with clear lifecycle: start → run loop → graceful shutdown.

## Deliverables

1. **Daemon `main`** that stays alive until SIGINT/SIGTERM (or console Ctrl+C).
2. **Work loop:** either poll a queue (preferred if A05 done) **or** a scheduled tick (e.g. every N seconds) that does a small unit of work.
3. **Shutdown hook / signal handling** that stops accepting work and exits cleanly (log “shutting down”).
4. **Lifecycle diagram** (text or Mermaid): states `Starting`, `Running`, `Stopping`, `Stopped`.
5. **Ops notes:** how you would run it under `systemd` or a lab service account (bullets, not full unit file required).

## Quality bar

- Process does not busy-spin the CPU without sleep/block.
- Shutdown is graceful (no silent kill reliance only).
- Logs show start and stop clearly.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| lifecycle | 15 | Start/run/stop correct |
| robustness | 10 | Graceful shutdown + sane loop |
| communication | 5 | Diagram + ops notes clear |
