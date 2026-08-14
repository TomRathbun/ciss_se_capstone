# PRSAS — Radar Message Simulator

> **Phase:** implementation. Java is the hiring bar. Python notebooks are not the deliverable.  
> **Deploys on:** `sim-a-01` and `sim-b-01` (VMs).

## Learning outcomes

After this module you can:

- Implement a **configurable ASTERIX-like Cat 062** publisher (CISS-TEACH-1 JSON)  
- Drive **scripted and random** scenarios (Mode 3/A, position, velocity, rate)  
- Publish with a **TLS JMS** (or instructor-approved STOMP) client to `radar.input`  
- Expose **start / stop / scenario / throttle** without a secret UI framework  
- Keep Site A and Site B **SIC / source_id** distinct  

## Why this component exists

Remote stacks have **no real radar**. The simulator *is* the sensor as far as the rest of PRSAS is concerned. If the payload drifts from the SE ICD, the daemon is not wrong — the contract is.

```text
scenario file  →  generator loop  →  JMS producer (TLS)  →  radar.input
                      ↑
              start/stop, rate Hz
```

## Contract you implement

See **se-12** for the frozen JSON. Your code must:

| Rule | Detail |
|------|--------|
| Edition | `msg_type = CAT062_LIKE`, `edition = CISS-TEACH-1` |
| Identity | `sic` and `source_id` from config (`RSA` vs `RSB`) — not hard-coded in Java if you can help it |
| Key | `mode3a` four octal digits as string |
| Time | `tod` UTC ISO-8601 |
| Units | `lat_deg`, `lon_deg`, `alt_ft`, `vx_kt`, `vy_kt` |
| Rate | configurable (default **1 Hz** per track) |

Official ASTERIX binary is a **stretch**, not the grade. If you encode binary, still emit the JSON (or a documented twin) so the daemon can start this week.

## Scenario file (teaching)

```json
{
  "name": "two-tracks-over-abudhabi",
  "hz": 1,
  "tracks": [
    {
      "track_num": 1,
      "mode3a": "4521",
      "callsign": "UAE421",
      "lat0": 24.45,
      "lon0": 54.38,
      "alt_ft": 18000,
      "vx_kt": 120,
      "vy_kt": 20
    }
  ]
}
```

Motion: simple dead-reckoning each tick is enough. Document the Earth model (flat lab plane is acceptable if stated).

**Required scenarios**

1. Happy path — 5–20 tracks, both sites can run a subset.  
2. Dual-feed agree — same `mode3a`, positions within gate.  
3. Dual-feed conflict — same `mode3a`, offset > gate.  
4. Dropout — stop one track after T seconds (for coast tests).

## Java shape (suggested)

```text
com.ciss.prsas.sim
  SimMain          # args: --site A|B --scenario file --broker url
  ScenarioLoader
  TrackKinematics
  Teach062Factory  # builds JSON / Map
  InputPublisher   # JMS, TLS
```

Reuse **sw-05** habits: pooled connection, `TextMessage`, clear start/stop of the Connection.

Controls: CLI flags are enough (`--hz`, `--start-delay`). A tiny JavaFX panel is optional and must not block the publisher thread (sw-07).

## TLS and lab URLs

- Broker: `ssl://amq-c-01:61617` (live host from the lab sheet).  
- Trust the **lab CA**. Do not `trustAll`.  
- Client cert if ADMIN issued one; else user/password from the sheet, **not** committed.  
- `radar.input` is a **topic**. Both sims publish; the daemon fans in.

## Monday workshop (builds SW-A09)

1. **15 min** — Load CISS-TEACH-1; write a unit test that a message has `mode3a` matching `[0-7]{4}`.  
2. **30 min** — Kinematics + one scenario file running to **stdout** (no broker yet).  
3. **25 min** — Wire JMS to the lab broker or an instructor desktop broker.  
4. **10 min** — Run Site A and Site B configs; show different `sic` on the console.

## Thursday assignment

**SW-A09 — Simulator.** Due this Thursday. Evidence: logs of ≥ 3 published messages from each site config.

## Integrity

- No real flight data dumps.  
- No production broker URLs.  
- Cite AI if it wrote a class; you must be able to change the kinematics.

## Tools

| Job | Tool |
|-----|------|
| Build | Maven, Java 8+ as per **sw-03-vscode-java** |
| Broker | Lab ActiveMQ VM |
| Inspect | `tcpdump` is NET’s job; you use AMQ console + your logs |

## Next

**Track processing daemon** — consume `radar.input`, correlate, persist, publish `radar.output`.
