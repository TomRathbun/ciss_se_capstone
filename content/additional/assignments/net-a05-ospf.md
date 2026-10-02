# NET-A05 — OSPF Neighbor Lab

**Weight:** 10% · **Due:** After net-05-igp-ospf · **Module:** net-05-igp-ospf

## Prompt

Show you can **read and design** OSPF on the lab IGP (SRX-A ↔ PE or two lab routers).

## Deliverables

1. **`show route` excerpt:** identify default (if any), a static, an OSPF route — or state absences.  
2. **Neighbor table:** RID, interface, state, dead time — from `show ospf neighbor` or a provided capture.  
3. **Config shape** (`set` lines): `router-id`, `lo0` **passive**, transit IFL in **area 0**, and (if SRX) **host-inbound** `protocols ospf`.  
4. **Loopback ping:** result of `ping <peer-lo0> source <local-lo0>` or why it was not possible.  
5. **Fault table** (4 rows): Down; ExStart/MTU; Full but missing prefix; static shadowing OSPF — test + first fix direction.  
6. One sentence: why IGP health is a **gate** for BGP and MPLS.

## Quality bar

- Preference/static-shadow is understood.  
- No freelance redistribution.  
- Area 0 unless the instructor drew another area (then document it).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| evidence | 15 | Neighbor + route evidence correctly read |
| design | 10 | Valid Junos OSPF shape including SRX inbound if needed |
| communication | 5 | Fault table usable on a night shift |
