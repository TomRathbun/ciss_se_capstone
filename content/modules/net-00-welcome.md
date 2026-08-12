# Networking — Track Overview

> **Track status:** scaffolding. Core lessons and graded assignments will be added as the networking path is authored. This page defines how the track fits the capstone.

## Learning outcomes

After this overview you can:

- Explain why **networking** matters on CISS-type systems and missions  
- Name themes this track will cover (protocols, topology, security, mission links)  
- Connect network ideas to **interfaces / ICDs** and the military **Link 16 / VCS** vocabulary  

## Why this track exists

Sensors, C2, and software only work if **bits move reliably and securely**. This track builds literacy for:

| Theme | What “good” looks like |
|-------|------------------------|
| **Fundamentals** | Addressing, routing, layers — enough to debug conversations |
| **Protocols** | TCP/UDP, TLS, common app protocols used on the program |
| **Topology & HA** | Paths, redundancy, failure modes |
| **Security** | AuthN/Z, segments, least privilege (unclassified) |
| **Mission relevance** | Datalinks, voice paths, feed interfaces (with **Military** track) |

## How modules will be organized

Register modules in `content/catalog.yaml` with `track: net` and Markdown under `content/modules/` (e.g. `net-01-…md`). Assignments use `track: net`.

Suggested growth path (not yet all written):

1. Network models & vocabulary  
2. Host-to-host and service design  
3. Observability (what to measure)  
4. Secure segmentation  
5. Integration with SA / C2 feeds (ICD thinking)  

## Relationship to other tracks

| Track | Overlap with networking |
|-------|-------------------------|
| **Systems Engineering** | Interfaces, NFRs (latency, availability), context diagrams |
| **Software** | Services, APIs, client/server design |
| **SysAdmin & Integration** | Deployed paths, DNS, firewalls, certs |
| **Military** | Link 16 concepts, VCS, COP data paths |

## Further reading

| Topic | Source |
|-------|--------|
| Internet layers (classic) | [RFC 1122](https://www.rfc-editor.org/rfc/rfc1122) / community TCP/IP primers |
| TLS overview | [MDN — Transport Layer Security](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) |
| SE interfaces | Course **Interfaces & ICDs** (SE track) |

## Next

When new **net-** modules are published, they appear under **Modules → Networking**. Pair early SE interface habits with the **Military** track’s voice/datalink planning notes.
