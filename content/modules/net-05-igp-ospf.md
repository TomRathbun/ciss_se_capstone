# Interior Routing — Static Routes and OSPF

## Learning outcomes

After this module you can:

- Read **`show route`** and explain **preference** (Junos administrative distance)  
- Write a **static** route with a correct next hop  
- Bring up **OSPF** on a point-to-point and on `lo0`  
- Use **`show ospf neighbor`** / **database** as evidence  
- State why **IGP must be healthy before BGP or MPLS**  

## Routing table vs “the firewall”

The SRX still **routes**. Policy decides if a flow is allowed; the routing table decides **where the first packet goes**.

```text
show route
show route 10.20.10.1
show route protocol static
show route protocol ospf
show route forwarding-table
```

| Preference (common Junos) | Source |
|---------------------------|--------|
| 5 | Static (default) |
| 10 | OSPF internal |
| 150 | OSPF AS-external |
| 170 | BGP |

Lower preference wins. A leftover static will **shadow** OSPF — classic lab ghost.

SE link: reachability is an **availability NFR**. The route is also an interface: if Site-B’s prefix changes, the ICD/runbook must change.

## Static routes

```text
set routing-options static route 10.20.10.0/24 next-hop 10.0.0.6
set routing-options static route 0.0.0.0/0 next-hop 10.0.0.6
```

| Rule | Why |
|------|-----|
| Next hop must be **on-link** | Junos will not recursively guess unless you designed it |
| Prefer `/32` loopbacks in diagrams | Stable target for ping/iBGP later |
| Qualified next-hop | Floating static (backup preference) — only when taught |

**Discard / reject:** `discard` silently drops; `reject` sends ICMP unreachable. Do not point a default at `discard` “to be safe” on a shared SRX.

## OSPF — the lab IGP

**OSPF** floods link-state advertisements (LSAs) inside an **autonomous system**. Neighbors form on a link, then the SPF tree builds.

```text
                    area 0.0.0.0 (backbone)
   lo0 .11                 lo0 .1                 lo0 .2
   SRX-A ------/30------  PE-1 ------/30------  PE-2 ------ SRX-B
```

For this course: **single area 0** unless the instructor draws another area.

### Why loopbacks

Set `router-id` from `lo0` `/32`. Neighbors and LSPs stay stable when a transit link flaps.

```text
set interfaces lo0 unit 0 family inet address 10.255.255.11/32
set routing-options router-id 10.255.255.11
set protocols ospf area 0.0.0.0 interface lo0.0 passive
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0
```

`passive` on `lo0` advertises the `/32` without sending hellos on loopback.

### Network types (what you will see)

| Type | Typical | Neighbor count |
|------|---------|----------------|
| p2p | `/30` WAN, many Junos defaults on p2p | 1 |
| broadcast | Ethernet LAN, DR/BDR | many |

```text
set protocols ospf area 0.0.0.0 interface ge-0/0/0.0 interface-type p2p
```

Mismatched hello/dead or p2p vs broadcast → stuck in **Init / 2Way / ExStart**.

### SRX extras

On SRX, OSPF hellos are **to the box** → zone **host-inbound-traffic protocols ospf** on that interface’s zone.

If the link is in UNTRUST, you still need OSPF inbound on that zone (lab WAN). Do not open OSPF on a real untrusted Internet zone.

## Evidence commands

```text
show ospf neighbor
show ospf interface
show ospf overview
show ospf database
show route protocol ospf
show ospf log
```

Healthy neighbor: **Full** (and `PtToPt` or `DR`/`BDR` as designed).

| State | First checks |
|-------|----------------|
| Down | Link, IP/mask, OSPF enabled, host-inbound |
| Init / 2Way | Hello mismatch, area mismatch, authentication |
| ExStart / Exchange | MTU mismatch (very common on tunnels) |
| Full but no route | Stub/NSSA, policy, different subnet not advertised |

## Authentication (awareness)

Older labs sometimes use OSPF simple or MD5 keys. Treat the key like a password. Do not paste it into Git. If neighbors will not form and configs “look the same,” ask whether **auth** is configured.

## Redistribution (do not freelance)

`set policy-options …` + `export` into OSPF redistributes statics/BGP. One wrong export can dump a default into the whole lab. **No redistribution unless the assignment says so.**

## IGP before overlays

```text
Need reachability to neighbor lo0
        ↓
     OSPF Full + lo0 in show route
        ↓
   then BGP / LDP / RSVP / IPsec interesting traffic
```

If `ping 10.255.255.2 source 10.255.255.1` fails, **stop** and fix IGP. Do not debug BGP.

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| OSPF on the wrong unit | Neighbor Down |
| Different area IDs (`0` vs `0.0.0.0` is OK; `1` vs `0` is not) | No adjacency |
| Missing `passive` on LAN + extra neighbors | Accidental adjacency to a PC (rare) / messy LSDB |
| Static + OSPF same prefix | Static wins (pref 5); “OSPF is broken” |
| Forgetting host-inbound on SRX | Eternal Down |

## Drill (40 min)

1. `show route` — identify default, one static (if any), one OSPF.  
2. `show ospf neighbor` — state, RID, interface.  
3. Ping peer **loopback** sourced from local loopback (if addresses exist).  
4. On paper: `set` lines for OSPF area 0 on `ge-0/0/0.0` + passive `lo0.0` for `srx-a-fw-01`.  
5. Write a 4-row fault table: Down / ExStart / Full-no-route / static-shadow.

## Integrity

- Do not change `router-id` on a shared PE.  
- Do not add a second default.  
- Do not enable OSPF on user access VLANs unless designed.

## Further reading

| Topic | Source |
|-------|--------|
| OSPF | [RFC 2328](https://www.rfc-editor.org/rfc/rfc2328) (concepts; you will not memorize the RFC) |
| Junos OSPF | TechLibrary OSPF feature guide for your Junos |
| Preference | Search “Junos route preference” |

## Next

**BGP** — the exterior (and often iBGP overlay) protocol. The name is **BGP**, not “BGB.”
