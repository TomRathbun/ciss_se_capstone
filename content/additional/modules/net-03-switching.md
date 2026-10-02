# EX Switching — VLANs, Trunks, and Virtual Chassis

## Learning outcomes

After this module you can:

- Design **access vs trunk** ports on older **EX** Junos  
- Create **VLANs** and an SVI (`vlan.x` or `irb.x`)  
- Explain **RSTP** enough to find a blocked uplink  
- Describe **EX4200 Virtual Chassis** (member, master, VCP)  
- Capture `show ethernet-switching` / MAC table evidence  

## Why the switch comes before the SRX

Users do not plug into the firewall. They plug into **access EX**. If VLAN 10 is missing on the trunk, the SRX policy will never see the packet.

| Device in the fabric | Switching job |
|----------------------|---------------|
| `ex-a-acc-01` (EX4200/2200) | Access ports, user/server VLANs |
| `ex-a-core-01` (EX4200/4500) | Trunks, SVIs or L3 handoff to SRX |
| `srx-a-fw-01` | L3 / policy — **not** a 48-port closet switch |

SE link: VLAN ID + tagged/untagged is an **L2 ICD** between access and core.

## VLAN mental model

```text
VLAN 10 USERS     10.10.10.0/24
VLAN 20 SERVERS   10.10.20.0/24
VLAN 99 MGMT      10.255.0.0/24
```

A VLAN is a **broadcast domain**. Hosts in VLAN 10 can ARP each other. To reach VLAN 20 they need a **gateway** (core SVI or SRX).

## Older EX syntax (port-mode)

Pre-ELS hardware (EX2200, EX3200, **EX4200**, many EX4500 trains) uses **`port-mode`** and `family ethernet-switching`:

```text
set vlans USERS vlan-id 10
set vlans SERVERS vlan-id 20
set vlans MGMT vlan-id 99

set interfaces ge-0/0/10 unit 0 family ethernet-switching port-mode access
set interfaces ge-0/0/10 unit 0 family ethernet-switching vlan members USERS
set interfaces ge-0/0/10 description "PC lab seat 10"

set interfaces ge-0/0/23 unit 0 family ethernet-switching port-mode trunk
set interfaces ge-0/0/23 unit 0 family ethernet-switching vlan members [ USERS SERVERS MGMT ]
set interfaces ge-0/0/23 description "uplink to ex-a-core-01"
```

**ELS** (newer EX): `interface-mode access` / `interface-mode trunk` and often `irb`. If `set interfaces … port-mode` is rejected, you are on ELS — use `interface-mode` and say so in your notes.

### Native / untagged VLAN on a trunk

Older EX: `native-vlan-id` under ethernet-switching. Only use it when the peer expects untagged frames. Mismatched native VLAN = **asymmetric connectivity** that looks haunted.

## SVI (switch virtual interface)

On older EX, L3 VLAN interface is often `vlan.10`:

```text
set interfaces vlan unit 10 family inet address 10.10.10.2/24
set vlans USERS l3-interface vlan.10
```

On ELS: `irb.10` + `set vlans USERS l3-interface irb.10`.

If the **SRX** is the gateway (`10.10.10.1`), the EX SVI may be **management only** or omitted. Do not put two gateways on one subnet unless VRRP/HSRP is designed (later / instructor).

## Spanning Tree (RSTP)

Loops without STP = broadcast storm. Older EX typically run **RSTP**.

```text
show spanning-tree interface
show spanning-tree bridge
```

| Role | Meaning |
|------|---------|
| Root | Reference bridge |
| Designated (FWD) | Forwarding on that segment |
| Alternate (BLK) | Backup; blocked to break the loop |

Intern job: **know which uplink should be forwarding**. If both uplinks forward and you did not design a LAG, you have a problem.

**LAG / ae** (awareness): `ae0` aggregated Ethernet. Both sides must match member count and LACP. Do not build a casual LAG on a shared core without the instructor.

## EX4200 Virtual Chassis (classic)

EX4200s stack over **VCP** (dedicated rear ports or configured uplinks):

```text
show virtual-chassis
show virtual-chassis vc-port
```

| Idea | Meaning |
|------|---------|
| Member ID | 0, 1, 2… — appears as FPC in `ge-0/0/0` vs `ge-1/0/0` |
| Master / backup RE | Who owns the RE; `request session member n` |
| Line-card member | Forwards only |
| `ge-1/0/5` | Member 1, port 5 |

Cable VCP **before** you invent member IDs. Split VC (two masters) is an incident — do not power-cycle randomly; capture `show virtual-chassis` and escalate.

EX2200 is often **standalone**. EX8200 is a chassis, not a 4200-style VC.

## Discovery commands

```text
show vlans
show ethernet-switching table
show ethernet-switching interfaces
show lldp neighbors
show interfaces ge-0/0/10 extensive | match "Physical|error|VLAN|speed|Duplex"
show arp
```

`show lldp neighbors` is how you confirm **what is actually plugged in**, not what the cable label claims.

## Handoff to the SRX

Typical Site-A pattern:

```text
EX access  --trunk 10,20,99-->  EX core  --access or L3 /30-->  SRX ge-0/0/1 (TRUST)
```

Two clean designs (pick one; do not mix silently):

1. **L2 to the firewall:** trunk or access VLAN 10 to SRX; SRX holds `10.10.10.1/24`.  
2. **L3 on the core:** EX SVI is gateway; `/30` toward SRX; EX needs a default route.

Write the chosen design in the assignment. Most intern benches use **(1)**.

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| Access port in the wrong VLAN | PC ARPs forever |
| VLAN missing on **one** trunk hop | VLAN “exists” on access and not on core |
| Trunk `port-mode` vs ELS `interface-mode` mix | Commit fails or port stays down |
| Two devices both `.1` on VLAN 10 | Duplicate IP / flapping ARP |
| Disabling RSTP “to make it work” | Storm on a looped lab |

## Drill (40–50 min)

On assigned EX (or paper if no switch):

1. `show version` + `show virtual-chassis` (or note standalone).  
2. Table: port, description, access/trunk, VLAN members (from `show ethernet-switching interfaces`).  
3. `show lldp neighbors` — draw the neighbor of the uplink.  
4. `show ethernet-switching table` — find one user MAC and its VLAN/port.  
5. Propose (do not apply unless told) the `set` lines for a new access port in VLAN 10.

## Integrity

- Do not `delete vlans` globally.  
- Do not change VCP or VC member IDs.  
- Do not disable spanning-tree on uplinks.

## Further reading

| Topic | Source |
|-------|--------|
| EX4200 switching | TechLibrary EX4200 software docs (match Junos) |
| ELS vs non-ELS | Search “Understanding Enhanced Layer 2 Software” |
| RSTP | IEEE 802.1w concepts; Junos spanning-tree user guide |

## Next

**SRX firewalls** — zones, policies, NAT, and why ping dies without `host-inbound-traffic`.
