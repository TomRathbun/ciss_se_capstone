# PRSAS — Track Processing Daemon

> **Phase:** implementation. This is the long-running service from **sw-06**, with a real ICD.

## Learning outcomes

After this module you can:

- Run a **systemd-friendly** Java daemon on `trk-c-01`  
- Consume `radar.input`, **correlate** on Mode 3/A, fallback to a position/velocity gate  
- Implement **initiate / update / coast / drop / conflict**  
- **Persist** system tracks + history with JDBC (schema from SE-A14)  
- Publish fused updates to `radar.output` immediately after a persist  
- Degrade when AMQ or Postgres blips (retry, log, do not corrupt state)  

## Pipeline

```text
JMS consume radar.input
        → parse CISS-TEACH-1
        → correlate
        → lifecycle
        → JDBC upsert + history row
        → JMS publish radar.output
        → ack input
```

Ack **after** persist+publish (or document why you ack earlier). At-least-once + idempotent upsert on `(track_id)` / `(mode3a, live)`.

## Correlation rules (implement these numbers unless SE changed them)

| Case | Action |
|------|--------|
| New `mode3a` not in LIVE/COAST/CONFLICT | **Initiate** system track |
| Existing `mode3a`, distance ≤ **1.0 NM** and speed delta ≤ **50 kt** | **Update**, reset miss counter, add source |
| Existing `mode3a`, beyond gate | **CONFLICT** — keep both hypotheses in history; do not delete the older one |
| Missing `mode3a` | Gate-only associate or reject with a log; never invent a squawk |
| No plot for **N=3** periods | **Coast** |
| Coast longer than **T=30 s** | **Drop** with reason `COAST_TIMEOUT` |

Use the same units as the payload. Document the NM calculation (haversine is fine).

## Output message (teaching)

```json
{
  "msg_type": "SYSTEM_TRACK",
  "edition": "CISS-TEACH-1",
  "track_id": 1001,
  "mode3a": "4521",
  "state": "LIVE",
  "sources": ["RSA", "RSB"],
  "lat_deg": 24.46,
  "lon_deg": 54.39,
  "alt_ft": 18100,
  "vx_kt": 118.0,
  "vy_kt": 21.0,
  "tod": "2026-08-14T08:01:12.000Z"
}
```

`state` ∈ `INIT | LIVE | COAST | CONFLICT | DROP`.

## Daemon craft

| Topic | Expectation |
|-------|-------------|
| Process | `main` loop; SIGTERM shutdown hook closes JMS + DataSource |
| systemd | unit file with `Restart=on-failure`, no `KillMode=none` tricks |
| Config | broker URL, JDBC URL, N, T, gate — file or env, **not** source |
| Logs | one line per initiate/conflict/drop; no payload spam at INFO |
| JDBC | `PreparedStatement`, one DataSource (Hikari); daemon role from ADMIN |
| Threads | consumer thread ≠ JDBC if you must, but keep it simple and correct |

```ini
# /etc/systemd/system/prsas-daemon.service  (shape)
[Service]
User=prsas
EnvironmentFile=/etc/prsas/daemon.env
ExecStart=/usr/bin/java -jar /opt/prsas/daemon.jar
Restart=on-failure
```

## Failure behaviour

| Fault | Daemon does |
|-------|-------------|
| Postgres down | Stop acking (or park); retry; log; **do not** publish a track you did not persist |
| AMQ down | Backoff reconnect; keep in-memory tracks; do not exit-loop-spin at 100% CPU |
| Bad JSON | Log, skip, ack (poison pill policy — document it) |
| Duplicate delivery | Upsert; history may record a duplicate `tod` — say so |

## Monday workshop (builds SW-A10)

1. **15 min** — Agree schema with SE (or use se-14 SQL if SE-A14 is late — label it **baseline**).  
2. **30 min** — Correlator unit tests: new, update, conflict, coast. **No broker required.**  
3. **25 min** — JDBC upsert against `pg-c-01` or a local Postgres the instructor allows.  
4. **10 min** — Hook consume/publish if the broker is up.

## Thursday assignment

**SW-A10 — Daemon.** Evidence: unit tests + a journal excerpt showing initiate → update → coast.

## Next

**SA client** — bulk load + live topic + map.
