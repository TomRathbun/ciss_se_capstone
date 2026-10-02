# SRX Firewalls — Zones, Policies, and NAT

## Learning outcomes

After this module you can:

- Place the older **SRX** families (branch vs mid/high) in the lab fabric  
- Put an IFL in a **security zone** and allow **host-inbound-traffic**  
- Write a **first-match** security policy (address book + application)  
- Explain **source / destination / static NAT** at intern level  
- Read **`show security flow session`** as evidence  

## What an SRX is

Juniper **SRX** is a **zone-based stateful firewall** running Junos. It replaced many **ScreenOS SSG** boxes. It is **not** “a router that happens to have ACLs” — if the interface is not in a zone, **traffic does not flow**.

| Class | Older models you may see | Notes |
|-------|--------------------------|--------|
| Branch | SRX100/110, 210/220, **240**, 550, 650 | Small flash; `fe-` on low end; IPsec yes; MPLS generally **no** |
| Mid | SRX1400, 3400, 3600 | IOC / SPC language; more sessions |
| High-end | SRX5600 / 5800 | SPC2/SPC3, NPCs — treat as a different scale class |
| Legacy | SSG5 / SSG140 / ISG | **ScreenOS** — different CLI |

Common lab Junos: **12.1X46-Dxx**, **12.3X48**, **15.1X49-Dxx**. Quote `show version` in every lab.

SE link: zones and policies are the **security architecture** of the enclave; they implement NFRs and ICD allow-lists.

## Flow vs “the packet just routes”

SRX (inet flow) builds a **session**:

```text
first packet → screens → route lookup → zone/policy → NAT → install session
return packets → existing session (unless policy/NAT/route broke)
```

```text
show security flow session
show security flow session destination-prefix 10.10.20.10
show security policies
show security zones
```

No session + ICMP blocked? Policy or zone. Session exists + app fails? Port/NAT/ALG/MSS — not “routing is down.”

## Zones (the intern-killer)

Every transit IFL lives in **exactly one** security zone.

```text
set security zones security-zone TRUST interfaces ge-0/0/1.0
set security zones security-zone UNTRUST interfaces ge-0/0/0.0
```

### host-inbound-traffic

This allows traffic **to the SRX itself** (SSH, ping, IKE, BGP, OSPF), **not** transit.

```text
set security zones security-zone TRUST host-inbound-traffic system-services ssh
set security zones security-zone TRUST host-inbound-traffic system-services ping
set security zones security-zone TRUST host-inbound-traffic system-services ike
set security zones security-zone TRUST host-inbound-traffic protocols ospf
```

| Symptom | Typical miss |
|---------|----------------|
| Cannot ping the SRX address | `ping` not in host-inbound on that zone |
| Cannot SSH | `ssh` not allowed on that zone / from that source |
| OSPF stays Down | `protocols ospf` not in host-inbound |
| IPsec never starts | `ike` not in host-inbound on the **WAN zone** |

**Do not** `set security zones security-zone TRUST host-inbound-traffic system-services all` on UNTRUST in a shared lab.

`fxp0` / dedicated management is often in a **functional zone** (`management`) — do not casually move it.

## Policies

Policies are **from-zone → to-zone**, **first match wins**, implicit **deny** at the end.

```text
set security address-book global address NET-USERS-A 10.10.10.0/24
set security address-book global address NET-SERVERS-A 10.10.20.0/24

set security policies from-zone TRUST to-zone TRUST policy allow-users-to-servers match source-address NET-USERS-A
set security policies from-zone TRUST to-zone TRUST policy allow-users-to-servers match destination-address NET-SERVERS-A
set security policies from-zone TRUST to-zone TRUST policy allow-users-to-servers match application [ junos-http junos-https junos-ping ]
set security policies from-zone TRUST to-zone TRUST policy allow-users-to-servers then permit
```

Intra-zone traffic still needs a policy if `default-policy` is deny (normal).

### Applications

Use Junos defaults when they match (`junos-ssh`, `junos-http`, `junos-https`, `junos-dns-udp`, `junos-ping`). Custom app = port + protocol:

```text
set applications application APP-AMQP protocol tcp
set applications application APP-AMQP destination-port 61616
```

That is an **ICD port** becoming a firewall object.

### Default policy

```text
show security policies default-policy
```

Lab should be **deny-all** implicit. A `permit-all` default is a finding, not a convenience.

## NAT

NAT rewrites addresses. On SRX it is its own stanza, **plus** the security policy (policy sees **pre- or post-NAT** addresses depending on type — be consistent in notes).

### Source NAT (typical users → WAN)

```text
set security nat source rule-set RS-OUT from zone TRUST
set security nat source rule-set RS-OUT to zone UNTRUST
set security nat source rule-set RS-OUT rule R1 match source-address 10.10.10.0/24
set security nat source rule-set RS-OUT rule R1 then source-nat interface
```

`source-nat interface` uses the egress IFL address (old-school PAT).

### Destination / static NAT (awareness)

Publish an internal server: destination NAT (or static) plus a policy from UNTRUST to TRUST **to the correct address** (the one the policy looks up). Interns often NAT one way and policy the other.

```text
show security nat source summary
show security nat destination summary
show security flow session protocol tcp destination-port 443
```

## Screens and ALGs (awareness)

**Screens** = DoS / reconnaissance protections per zone (`icmp-flood`, `syn-flood`, …). A leftover screen can drop lab traffic. `show security screen statistics zone TRUST`.

**ALGs** rewrite payloads (FTP, SIP). They surprise people. If a lab app breaks only for “helper” protocols, check `show security alg status`. Do not disable ALGs globally as a reflex.

## Model-specific habits (older branch)

| Habit | Why |
|-------|-----|
| `show system storage` before traces | 1–2 GB flash fills; box hangs |
| Prefer `ge-` vs `fe-` from `show interfaces terse` | SRX210 has both stories |
| Mini-PIM / uPIM slots | Port names jump (`ge-0/0/0` then `ge-2/0/0`) |
| Flow vs packet mode | MPLS/transparent tricks on higher platforms — not branch default |

## What “good” looks like on `srx-a-fw-01`

```text
TRUST   ge-0/0/1.0   10.10.10.1/24    users + servers (or only users)
UNTRUST ge-0/0/0.0   10.0.0.5/30      toward PE / WAN
lo0.0   10.255.255.11/32
```

Policies: TRUST→TRUST as needed; TRUST→UNTRUST for approved apps; UNTRUST→TRUST **default deny** plus any explicit publish.

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| IP on IFL, no zone | Interface does not pass traffic |
| Zone but no policy | Drops; no session |
| Policy without `junos-ping` | “Routing is down” (it is not) |
| host-inbound missing | Cannot manage/ping the box |
| `any/any/any permit` UNTRUST→TRUST | Lab finding; automatic grade hit |
| Clearing all sessions | Outage for everyone on the box |

## Drill (50 min)

Read-only unless the instructor opens a sandbox zone:

1. `show version` and `show chassis hardware`.  
2. Table: interface, IP, zone (`show security zones`).  
3. `show security policies` — count TRUST→UNTRUST rules; note default.  
4. `show security flow session | match 10.10.` (or instructor prefix) — paste **two** sessions, redact user IPs if asked.  
5. Write the `set` lines (do not apply) for: allow Site-A users to ping `10.10.20.10` and TCP/443.

## Integrity

- No `permit any any` from UNTRUST.  
- No `clear security flow session` without a prefix and permission.  
- No production address books in Git.

## Further reading

| Topic | Source |
|-------|--------|
| SRX policy | TechLibrary *Security Policies Feature Guide* (version-match) |
| NAT | *Juniper SRX Series* (O’Reilly) or TechLibrary NAT guide |
| Flow | `show security flow session` help on box |

## Next

**Interior routing (OSPF)** — how the SRX and PE learn reachability inside the site/core.
