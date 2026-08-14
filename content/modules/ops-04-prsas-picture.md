# PRSAS — Air Picture for Operators

> **Phase:** implementation. Military track contribution to UC-CISS_PROJECT-001.  
> **Classification:** unclassified teaching picture only.

## Learning outcomes

After this module you can:

- Brief what a **fused air picture** is for (and is *not* for)  
- Use **track / Mode 3/A / coast / conflict** language consistently with SE  
- Write an operator **watch script** for a 10-minute lab sit  
- Mark **human-in-the-loop** points (conflict, drop, stale)  
- Produce an unclassified **picture annex** a supervisor intern can read aloud  

## Why MIL is in this pack

The other tracks can move JSON across IPsec and still build a **video game**. You keep the picture honest:

| Honest | Not this lab |
|--------|----------------|
| “Two lab sensors, one watch operator” | “National C2 with automatic engage” |
| Mode 3/A is a **code**, not identity | “That squawk is a hostile” |
| CONFLICT means **sensors disagree** | “Pick the red one and shoot” |
| COAST means **no recent plot** | “The track disappeared so the target is gone” |

Link-16, IFF Mode 4/5, real ATO tasking: **out**. Use **ops-00 / ops-01** vocabulary only at the unclassified level.

## Watch roles

| Role | During the demo |
|------|-----------------|
| Operator | Call new tracks, read Mode 3/A, notice COAST |
| Supervisor | Dispose CONFLICT (which hypothesis you *display*; you do not prosecute) |
| Safety / instructor | Stop the floor if anyone talks real unit tracks |

## 10-minute watch script (template)

1. Authenticate; confirm empty or residual DROP tracks.  
2. “Simulators on.” Call first Mode 3/A from source RSA, then RSB.  
3. Dual-feed agree: report **one** fused track, both sources.  
4. Inject conflict scenario: say “conflict, same Mode 3/A, two positions,” wait for supervisor.  
5. Kill sim-A: report COAST then DROP.  
6. Stop. No weapons language.

## Monday workshop (builds MIL-A04)

1. **15 min** — Glossary card: picture, track, plot, Mode 3/A, coast, drop, conflict.  
2. **25 min** — Write the 10-minute script with SE at the table.  
3. **20 min** — Red-team your own script: find one sentence that over-claims.  
4. **20 min** — Draft the annex (one page).

## Thursday assignment

**MIL-A04 — Picture annex & watch script.**

## Further reading

| Topic | Source |
|-------|--------|
| AOC / picture | **ops-00** |
| UAE context (open source) | **ops-uae-military** |
| Endsley SA | public paper — theory, not a CONOPS copy |
| Framing integrity | **se-10** |

## Next

You speak the demo. SE chairs. If the client lies, you say so.
