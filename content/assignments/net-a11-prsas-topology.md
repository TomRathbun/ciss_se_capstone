# NET-A11 — PRSAS Topology & Addressing

**Phase:** capstone · **Weight:** 30% of capstone-NET · **Due:** After net-11 · **Module:** net-11-prsas-topology

## Prompt

Publish the **three-site** logical network SW and ADMIN will build on.

## Deliverables

1. Logical diagram (Mermaid or equivalent) with hostnames.
2. VLAN / subnet workbook including gateways.
3. Example host IPs for sim-a, sim-b, amq, trk, pg, ui.
4. Allow-list table (src/dst/port/why) — default deny.
5. Mgmt vs data vs overlay (`st0`) called out.
6. Lab-vs-BOM honesty (physical EX/SRX vs virtual).

## Quality bar

- Extends net-00; does not renumber the academy without cause.
- 8161/5432 not open to radar VLAN in the intent table.
- Peer could cable/clone from the pack.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| design | 15 | Three sites, VLANs, overlays coherent |
| security_intent | 10 | Least privilege allow-list |
| communication | 5 | ADMIN-usable addressing |
