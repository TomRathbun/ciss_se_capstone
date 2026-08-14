# PRSAS — Situational Awareness Client

> **Phase:** implementation. Web **or** JavaFX is acceptable; pick one and finish it.

## Learning outcomes

After this module you can:

- Authenticate with **lab IPA / client certificate** (not a hard-coded god user in source)  
- **Bulk load** current tracks from PostgreSQL (JDBC or a thin REST proxy)  
- **Subscribe** to `radar.output` over TLS  
- Render a **map** with symbol, Mode 3/A, velocity vector, history trail, source  
- Filter / zoom without blocking the messaging thread  
- Reconnect when the broker drops  

## Two legal clients

| Option | When to choose | Stack |
|--------|----------------|-------|
| **A. JavaFX** | Matches sw-07 and desktop operator story | JavaFX + JMS + JDBC |
| **B. Web** | Matches the project “web client” sentence | React/Leaflet **or** a simple server-rendered page + JS; JMS via a **small Java or allowed** bridge |

The project text allows a web client. The **SW hiring bar is still Java** — if you choose web UI, the **bridge** (auth check, JDBC bulk, AMQ subscription → WebSocket) should be Java unless the instructor waives it.

Do not download a random closed-source C2.

## Picture requirements

| Element | Rule |
|---------|------|
| Map | Geographic (Leaflet OSM / OpenLayers **or** a JavaFX map with lat/lon). Lab may be offline — cache tiles or use a simple grid with labelled lat/lon if OSM is blocked. |
| Symbol | Distinct mark; CONFLICT is visually obvious |
| Label | Mode 3/A required; callsign if present |
| Vector | Heading/speed from `vx_kt`, `vy_kt` |
| Trail | Last *k* history points (k configurable, default 10) |
| Filter | By state and/or Mode 3/A prefix |
| Time | Show `tod` or age; stale/COAST styled differently |

**Human-in-the-loop:** a supervisor action (button or dialog) records CONFLICT disposition. It does **not** fire a weapon.

## Session start

```text
1. Auth (cert or IPA password via the bridge)
2. SELECT FROM system_track WHERE state <> 'DROP'  (or SE’s rule)
3. Subscribe radar.output
4. Apply live updates by track_id
5. On reconnect: repeat 2 then 3 (do not double-draw)
```

## Threading

- JavaFX: JMS callback **must not** touch the scene graph; use `Platform.runLater`.  
- Web: WebSocket handler updates state; React setState / Leaflet layer in the UI tick.  
- Never run JDBC on the JavaFX application thread.

## Auth integration

ADMIN issues the trust store and (optionally) client certs. You:

- Point the client at the trust store path from config  
- Fail closed on trust errors  
- Show a readable “not authorized” — not a stack trace to the operator  

If IPA is not ready this week, a **temporary** file-based user list is allowed **if** you file a ticket-shaped note that it is a stub and list the ADMIN dependency.

## Monday workshop (builds SW-A11)

1. **15 min** — Choose option A or B; write it at the top of the README.  
2. **25 min** — Bulk load → table view of tracks (map can wait 30 minutes).  
3. **25 min** — Subscribe and append a row on each message.  
4. **15 min** — Map symbols + Mode 3/A labels for two tracks.

## Thursday assignment

**SW-A11 — SA client.** Screenshot (unclassified, lab data) + reconnect note.

## Next

**Integration & container PoC** — three-stack demo and the virt numbers SE-15 needs.
