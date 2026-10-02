# PRSAS Virtualization Study & Lessons-Learned

> **Phase:** implementation close. SE owns the *comparison* and the *report*. SW/ADMIN provide numbers.

## Learning outcomes

After this module you can:

- Separate the **VM baseline** (course standard) from a **container PoC**  
- Define **measurable** comparison axes (start time, RAM/CPU, recoverability, ops friction)  
- Run or witness a fair test with SW-12 / ADMIN  
- Write a **lessons-learned** that a hiring panel can use  
- Make a **migration recommendation** that is honest about lab vs program  

## Baseline vs experiment

| Mode | What it is on CISS | Status |
|------|--------------------|--------|
| **VMware / ESXi guests** | Simulators, AMQ, daemon, Postgres, IPA | **System of record** |
| **Docker + minikube/kind** | PoC for **two** components only (usually sim + daemon) | Experiment |

The question is **not** “containers are the future.” The question is: *for these two components, what changed, and would we recommend it on a TR2-class program?*

## What to measure

Pick the same scenario on both runtimes (same payload edition, same plot rate, same host class).

| Axis | How to measure | Notes |
|------|----------------|-------|
| Cold start | Wall clock, first plot on `radar.input` | Three runs, report median |
| Recover | Kill process / pod / VM; time to first new plot | Say what you killed |
| CPU / RSS | `top` / `ps` vs `docker stats` / `kubectl top` | Same workload ≥ 2 minutes |
| Ops steps | Count of commands to redeploy | Include registry/auth if used |
| Failure mode | One injected fault (bad cert, broker down) | Same fault both sides |

**Fairness rules**

1. Do not compare a 4-vCPU VM to a 128 MB pod and call it science.  
2. Do not disable TLS on one side.  
3. Write the host names and image IDs.  
4. If minikube is not available, **worksheet + honest constraint** — do not invent Grafana screenshots.

## Suggested test card

```text
Scenario: 20 tracks, 1 Hz, two SICs, 120 seconds
Baseline: sim-a-01 + trk-c-01 as systemd on Rocky/RHEL guests
PoC:      same JARs in Docker; kind/minikube if instructor enabled
Fault:    stop amq-c-01 for 20 s, then start
Record:   start median, RSS, time-to-live-plot after fault, notes
```

SE does not have to write the Dockerfiles. SE **defines the card** and **interprets** SW/ADMIN evidence.

## Lessons-learned structure (required)

1. **Context** — what we built, who was in the team, what was in/out.  
2. **What worked** — three concrete items with evidence.  
3. **What hurt** — three items (integration, schema drift, certs, topics, …).  
4. **Quantitative findings** — the comparison table.  
5. **Recommendations** — numbered, owner-tagged (SE/SW/NET/ADMIN).  
6. **Would we migrate the daemon to K8s on the program?** — yes / not yet / no, with *why*.  
7. **Integrity** — data sources, AI citations, what you did not measure.

Hiring panels read section 5–6 first. Slogans without numbers fail.

## Monday workshop (builds SE-A15)

1. **15 min** — Freeze the test card with SW and ADMIN at the table.  
2. **40 min** — Collect or schedule measurements (or run a paper dry-run if the bench is down).  
3. **20 min** — Draft recommendations (sticky notes → three keep / three change).  
4. **15 min** — Outline the report. Assign who pulls which log excerpt.

## Thursday assignment

**SE-A15 — Virt comparison + lessons-learned.** Due this Thursday (instructor may allow a short extension if the bench demo slips to Friday — ask, do not assume).

## Tools for these artifacts

| Artifact | Simplest clear tool |
|----------|---------------------|
| Test card | One-page markdown |
| Results | Table + pasted `time` / `ps` excerpts (redact secrets) |
| Report | 4–8 page markdown |

## Further reading

| Topic | Source |
|-------|--------|
| Course runtime policy | README — VMs, not Docker as default |
| Daemon lifecycle | **sw-06**, **sw-12** |
| vSphere vocabulary | **admin-07** |
| V&V methods | **se-08** (I/A/D/T against the test card) |

## Next

Integration demo week: bring CONOPS, schema, evidence pack, and the running picture. MIL briefs the operator view. SE chairs the retro.
