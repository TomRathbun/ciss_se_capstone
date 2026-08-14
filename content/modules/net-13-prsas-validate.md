# PRSAS — Path Validation & Network Configuration Guide

> **Phase:** implementation close.

## Learning outcomes

After this module you can:

- Prove **end-to-end** simulator VLAN → Central AMQ **TLS port** (not just ICMP)  
- Produce a **layered evidence pack** (L2, L3, IKE, flow session, port)  
- Run a **bounded** security check (what is open, what must not be)  
- Write a **configuration guide** another intern can replay  
- Hand SW/ADMIN a one-page “how to reach the broker”  

## Validation order (do not skip layers)

| Layer | Command / check | Pass look |
|-------|-----------------|-----------|
| 1 L2 | `show ethernet-switching table` / `show vlans` | sim MAC on VLAN 30 |
| 2 L3 | `ping` / `show route` from sim VRF/zone | prefix via `st0` |
| 3 IKE | `show security ike sa` | SA UP both sites |
| 4 IPsec | `show security ipsec sa` | active ESP |
| 5 Policy | `show security flow session` | 61617 session |
| 6 App | From `sim-a-01`: `openssl s_client` or Java pub | handshake + send |

ICMP across the tunnel is **necessary but not sufficient**.

## Bounded security tests

Allowed:

- `show security policies` hit-counts  
- Nmap **from an agreed jump host** against AMQ **public** VIP — document the command  
- Capture on a **span/lab** port if the instructor says yes  

Not allowed:

- Scanning the whole `10.0.0.0/8`  
- Exploit kits, default-password spraying  
- Pasting captures that include PSKs or TLS private keys  

Record: 8161 and 5432 must **not** be reachable from the radar VLAN.

## Configuration guide (minimum chapters)

1. Addressing & hostnames  
2. VLAN / trunk sets (EX)  
3. Zones, policies, NAT decision (SRX)  
4. IPsec proposals and `st0` (PSK *reference*, not value)  
5. Verification commands  
6. Backout (`rollback`, `commit confirmed` reminder)  
7. Change ticket example  

Write it so a Thursday-absent intern can bring a replacement SRX back to the same state.

## Monday workshop (builds NET-A13)

1. **30 min** — Walk the six-layer table on the live bench (or fill expected-output if down).  
2. **20 min** — Negative test: 5432 from radar VLAN should fail; save the reject.  
3. **30 min** — Draft the guide outline; assign sections.

## Thursday assignment

**NET-A13 — Evidence pack + config guide.**

## Next

Stand by during the SW/ADMIN integration demo. You own the path, not the JSON.
