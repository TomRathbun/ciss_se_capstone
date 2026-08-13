# BGP — External and Internal

## Learning outcomes

After this module you can:

- Explain **BGP** as a **path-vector** protocol between **autonomous systems**  
- Distinguish **eBGP** and **iBGP**  
- Read neighbor **state** (`Idle` … `Established`) and TCP **179**  
- Use Junos **policy-statement** (not IOS route-maps) to advertise a prefix  
- Interpret **AS-path, local-pref, MED, next-hop** at intern level  

## Name and job

The protocol is **BGP** (Border Gateway Protocol). You may hear “BGB” in conversation — write **BGP** in tickets and assignments.

BGP does **not** replace OSPF inside a LAN. OSPF finds **internal** links. BGP advertises **reachability between ASNs** and carries MPLS VPN routes later.

| Lab ASN | Role |
|---------|------|
| `65001` | Site-A (SRX-A / site edge) |
| `65002` | Site-B |
| `65000` | Core / PE pair |

Private ASNs `64512–65534` are the intern default. Do not invent a public ASN.

SE link: a BGP prefix + community/RT is an **interface** between sites. Wrong export = leaking a route (security + ops incident).

## eBGP vs iBGP

```text
   AS 65001                    AS 65000                     AS 65002
   SRX-A --------eBGP--------- PE-1 --------iBGP--------- PE-2 --------eBGP-------- SRX-B
```

| | eBGP | iBGP |
|---|------|------|
| Peer AS | Different | Same |
| Typical hop | Direct `/30` | Often via loopbacks + IGP |
| Next-hop | Usually the peer address | Does **not** change by default → **next-hop-self** on PEs |
| Full mesh / RR | N/A | iBGP cannot re-advertise iBGP-learned to iBGP (split horizon) |

For two PEs you can full-mesh. A route reflector is **awareness only** in this course.

## Neighbor states

BGP runs over **TCP 179**.

```text
Idle → Connect → Active → OpenSent → OpenConfirm → Established
```

`Active` here means **actively trying TCP**, not “working.” Interns mix this with OSPF “Active.”

```text
show bgp summary
show bgp neighbor 10.0.0.6
show route receive-protocol bgp 10.0.0.6
show route advertising-protocol bgp 10.0.0.6
```

| Symptom | First checks |
|---------|----------------|
| Idle / Active | IP reachability, TCP 179, SRX policy **and** `host-inbound` `bgp`, wrong neighbor address |
| Connect | ACL / firewall / wrong TTL (eBGP multihop only if designed) |
| Established, 0 prefixes | **Export policy** missing (Junos does not auto-advertise connected the way people expect) |

## Minimal eBGP (SRX-A toward PE)

```text
set routing-options autonomous-system 65001
set routing-options router-id 10.255.255.11

set policy-options prefix-list PL-SITE-A 10.10.10.0/24
set policy-options prefix-list PL-SITE-A 10.10.20.0/24
set policy-options policy-statement ADV-SITE-A term T1 from prefix-list PL-SITE-A
set policy-options policy-statement ADV-SITE-A term T1 then accept
set policy-options policy-statement ADV-SITE-A term DENY then reject

set protocols bgp group EBGP-CORE type external
set protocols bgp group EBGP-CORE peer-as 65000
set protocols bgp group EBGP-CORE neighbor 10.0.0.6 export ADV-SITE-A
```

**Junos policy default is reject** if no term matches. A group without `export` advertises **nothing** (unless another policy applies). That is the #1 “BGP is up but Site-B cannot ping” bug.

Import: write an explicit `import` that accepts only expected prefixes. Do not accept `0.0.0.0/0` from a lab peer unless designed.

## Attributes you must recognize

| Attribute | Scope | Intern meaning |
|-----------|-------|----------------|
| **AS-path** | eBGP loop prevention | Shorter often preferred; you **prepend** to de-pref |
| **Local Preference** | Inside an AS | Higher wins (default 100) |
| **MED** | Hint to external | Lower wins; optional |
| **Origin** | IGP / EGP / Incomplete | Tie-break |
| **Next hop** | Where to send | Must be resolvable in `inet.0` |
| **Community** | Tag | Later: filter / TE |

Decision process (simplified): prefer highest **local-pref** → shortest **AS-path** → origin → lowest **MED** → eBGP over iBGP → lowest IGP metric to next-hop → RID.

You will not memorize every step. You **will** `show route detail` and name which attribute won.

## iBGP on loopbacks (PE shape)

```text
set protocols bgp group IBGP type internal
set protocols bgp group IBGP local-address 10.255.255.1
set protocols bgp group IBGP neighbor 10.255.255.2 next-hop-self
```

Requires **OSPF** (or other IGP) so `10.255.255.2` is reachable. `local-address` = update source.

## SRX-specific

- `host-inbound-traffic system-services bgp` (or `bgp` under system-services — version wording) on the zone facing the peer.  
- Security **policy** must allow **TCP/179** between the two peer IPs if the session is transit through another SRX.  
- Do not run eBGP on a user VLAN.

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| Wrong `peer-as` | Idle / notification |
| Advertising `/32` of the WAN instead of the user `/24` | Neighbor up, users dark |
| No export policy | 0 prefixes sent |
| Expecting iBGP to change next-hop | Blackhole until `next-hop-self` or IGP to CE |
| Redistributing OSPF ↔ BGP both ways | Loops; lab outage |
| Public ASN or production prefixes | Integrity fail |

## Drill (45 min)

1. `show bgp summary` — for each neighbor: AS, state, prefixes In/Out.  
2. If no live BGP: annotate an instructor capture.  
3. `show route receive-protocol bgp <peer>` — list prefixes (or state why empty).  
4. On paper: export policy for `10.10.10.0/24` and `10.10.20.0/24` only.  
5. Explain in two sentences why **Established ≠ traffic works**.

## Integrity

- Advertise **only** lab prefixes.  
- No `then accept` of all routes in import.  
- No copying production `show route` into public repos.

## Further reading

| Topic | Source |
|-------|--------|
| BGP | [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271) |
| Junos BGP | TechLibrary BGP user guide (your version) |
| Policy | *Junos Policy Framework* / Day One: Routing Policy |

## Next

**MPLS tunnels** — labels, LDP/RSVP, and L3VPN routing-instances on PE routers.
