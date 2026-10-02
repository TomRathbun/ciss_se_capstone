# NET-A04 — SRX Zones, Policy & NAT Pack

**Weight:** 10% · **Due:** After net-04-srx-firewall · **Module:** net-04-srx-firewall

## Prompt

Produce a **zone-based firewall pack** for `srx-a-fw-01` (hardware, vSRX, or paper). This is the core firewall assignment.

## Deliverables

1. **Platform:** model, Junos, cluster or standalone.  
2. **Zone table:** zone, interfaces, IP/mask, **host-inbound-traffic** (services + protocols).  
3. **Address book** for Site-A users `10.10.10.0/24` and servers `10.10.20.0/24` (or remapped prefixes).  
4. **Policy set** (`set` lines or hierarchical) that:
   - allows users → servers: `junos-ping` + `junos-https`  
   - allows users → UNTRUST: instructor-approved apps only (not `any`)  
   - does **not** permit UNTRUST → TRUST except an explicit deny or empty (state which)  
5. **NAT note:** source NAT to UNTRUST — `interface` PAT or “not used on this bench” with reason.  
6. **Evidence:** `show security zones`, `show security policies`, and one `show security flow session` excerpt **or** a labeled instructor capture.  
7. **Failure matrix** (3 rows): missing host-inbound ping; missing policy; missing zone — symptom + first command.

## Quality bar

- No `any/any/any` from UNTRUST.  
- Host-inbound is not confused with transit policy.  
- Sets would `commit check` on 12.x / 15.1X49-style syntax.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| correctness | 15 | Zones, host-inbound, first-match policy, NAT story |
| security_judgment | 10 | Least privilege; no lab-breaking permit-all |
| communication | 5 | Tables + sets ticket-ready |
