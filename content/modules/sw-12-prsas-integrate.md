# PRSAS — Integration & Container PoC

> **Phase:** implementation close. You are not “done” when the JAR runs on your laptop.

## Learning outcomes

After this module you can:

- Run **sim A + sim B + daemon + client** across the lab path NET/ADMIN built  
- Own a written **integration test card** (same faults as SE-15)  
- Containerize **two** components (simulator and daemon) and run them on Docker **or** minikube/kind  
- Capture **start time, RSS, recover** numbers for SE  
- Contribute maintainability notes to the lessons-learned  

## End-to-end card (software view)

| Step | Pass |
|------|------|
| 1 | Both sims publish CISS-TEACH-1 to `radar.input` (AMQ console or log) |
| 2 | Daemon upserts; `SELECT count(*)` grows |
| 3 | Client shows both SICs |
| 4 | Conflict scenario → CONFLICT visible, not silent merge |
| 5 | Stop sim-A → COAST then DROP on those tracks |
| 6 | Restart AMQ → daemon and client recover without DB wipe |
| 7 | Second client sees the same picture (bulk + live) |

If step 4 fails, it is an **SE/SW defect**, not a NET defect.

## Who to call

| Symptom | First track |
|---------|-------------|
| No TCP to 61617 from sim VLAN | NET |
| TLS handshake “unknown CA” | ADMIN |
| JDBC `permission denied` | ADMIN + your role SQL |
| JSON parse errors | You (payload drift) |
| IPsec down | NET |

Bring **evidence** (timestamped log, `journalctl`, redacted). Do not bring “it doesn’t work.”

## Container PoC

VM-native remains the graded production path. The PoC exists so SE can write SE-A15.

1. Dockerfile for `sim` and `daemon` (JRE + JAR).  
2. `docker compose` on one lab host **or** kind/minikube if present.  
3. Same TLS story — do not “just to make compose easy” turn SSL off unless you record it as a **known PoC limitation**.  
4. Measure against the SE test card.

K8s manifests may be ugly. Grade is honesty + numbers, not a Helm chart.

## Monday workshop (builds SW-A12)

1. **40 min** — Execute the e2e card with NET/ADMIN in the room. Log fails.  
2. **30 min** — Build the two images; time a compose up.  
3. **10 min** — Hand SE the numbers table (even if partial).

## Thursday assignment

**SW-A12 — Integration pack.** Test card results + PoC notes + two maintainability observations.

## Next

Support the shared demo. Fix only what the card failed. Do not gold-plate a third UI theme.
