# Network Foundations

## Learning outcomes

After this module you can:

- Map a conversation onto **OSI / TCP-IP** layers without mythology  
- Calculate **IPv4** networks, hosts, and default gateways from a CIDR prefix  
- Explain **Ethernet, VLAN, MAC, ARP** well enough to read a `show arp`  
- Distinguish **TCP and UDP** and say why a port number is an interface field  
- Use **ping** and **traceroute** as tests, not as “the fix”  

## Why foundations before Junos

**General networking** already covered roles, DHCP/DNS, and ports. This module is the **math and path** drill: interns fail SRX labs because they cannot tell **L2 miss** from **wrong mask** from **firewall drop**. Junos syntax cannot rescue a broken mental model.

| Symptom | Layer to inspect first |
|---------|------------------------|
| No link light / `down` | Physical / L1 |
| Ping same VLAN fails, ARP empty | L2 / VLAN / access port |
| ARP works, ping to other subnet fails | Gateway / routing |
| Ping works, app times out | TCP port / firewall / NAT |
| App connects then stalls | Path MTU, loss, policy, crypto |

SE link: an address, VLAN, and TCP port are **interface contract** fields — the same idea as an ICD.

## Two models (use both)

```text
OSI (7)                 TCP/IP (4)              What you actually touch
Application             Application             HTTP, DNS, BGP messages
Presentation            Application
Session                 Application
Transport               Transport               TCP / UDP ports
Network                 Internet                IP, ICMP, OSPF, BGP
Data link               Link                    Ethernet, VLAN, MAC, ARP
Physical                Link                    Cable, SFP, clock
```

You do not need to recite all seven layers in a briefing. You **do** need to say whether the failure is **link, IP, transport, or application**.

## IPv4 addressing (must be fluent)

An address is 32 bits. A **prefix** (CIDR) says how many bits are the network.

| Prefix | Mask | Hosts (usable, typical Ethernet) |
|--------|------|----------------------------------|
| `/30` | `255.255.255.252` | 2 — point-to-point WAN |
| `/29` | `255.255.255.248` | 6 |
| `/24` | `255.255.255.0` | 254 — common user VLAN |
| `/32` | `255.255.255.255` | 1 — loopback or host route |
| `/16` | `255.255.0.0` | large site block |

### Worked example (Site-A users)

- Prefix: `10.10.10.0/24`  
- Network: `10.10.10.0`  
- First host: `10.10.10.1` (usually the SVI / SRX)  
- Last host: `10.10.10.254`  
- Broadcast: `10.10.10.255`  
- A PC at `10.10.10.50` with mask `/24` and gateway `10.10.10.1` can ARP for `.50–.254` on-link; anything else goes to the gateway.

**Wrong mask** is the classic intern bug: host `/24`, gateway configured as `/30` on the same octets → “sometimes ping works.”

### Special ranges (do not confuse)

| Range | Use in this course |
|-------|--------------------|
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | RFC 1918 lab addresses |
| `127.0.0.0/8` | Host loopback — not a site loopback |
| `169.254.0.0/16` | Link-local (DHCP failed) |
| `224.0.0.0/4` | Multicast (OSPF hellos live here) |

Documentation ranges (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`) appear in public examples. Our shared fabric uses **10.x** — see the welcome module.

## Ethernet, MAC, VLAN, ARP

**MAC** = 48-bit link address burned (or assigned) on the NIC. Switches forward on MAC tables, not on IP.

**VLAN** = a broadcast domain tagged with an 802.1Q ID (1–4094). Same VLAN = same L2 segment. Different VLAN = need a **router / L3 interface** (EX IRB/`vlan` unit or SRX).

**Access vs trunk** (detail in the switching module):

| Port type | Frames |
|-----------|--------|
| Access | Untagged; belongs to one VLAN |
| Trunk | Tagged; carries many VLANs |

**ARP** binds IPv4 → MAC **on the local subnet only**. You never ARP for an address that is not on-link.

```text
PC 10.10.10.50  →  wants 10.10.20.10
  1. 10.10.20.10 is not on 10.10.10.0/24
  2. PC ARPs for its gateway 10.10.10.1
  3. Gateway routes toward 10.10.20.0/24
```

If `show arp` on the gateway has no entry for the PC, the problem is **not BGP**.

## TCP, UDP, ICMP

| Protocol | Connection | Typical use |
|----------|------------|-------------|
| **TCP** | Handshake (SYN/SYN-ACK/ACK); reliable | SSH (22), BGP (179), HTTPS (443), JDBC |
| **UDP** | No handshake | DNS (53), some voice, DHCP |
| **ICMP** | Control / error | Echo (ping), unreachable, TTL expired (traceroute) |

A **port** is a transport address. “Permit HTTP” means **TCP/80** (and usually **TCP/443**), not “the web vibe.”

**Ping success is not application success.** ICMP may be allowed while TCP/443 is denied — especially on SRX.

## Two tests you will live in

### ping

Asks: *does ICMP echo return?*

```bash
# From a Linux jump VM
ping -c 4 10.10.10.1
ping -c 4 -s 1472 10.10.10.1    # size probe (path MTU later)
```

On Junos (next module): `ping 10.10.10.1 rapid count 20`.

Interpret:

| Result | Meaning (first guess) |
|--------|------------------------|
| 0% loss | Reachability for ICMP — only that |
| 100% loss | L1/L2/IP/policy/ICMP denied — need more tests |
| Intermittent loss | Duplex, error, congestion, flapping link |

### traceroute

Asks: *which hops decrement TTL?*

```bash
traceroute -n 10.20.10.1
```

A hop of `* * *` is not always “down” — many firewalls **drop TTL-expired**. Read it with `ping` and routing tables.

## Path of a packet (keep this picture)

```text
PC --access VLAN10-- EX-acc --trunk-- EX-core --L3-- SRX (zone TRUST)
                                              |
                                         policy + NAT
                                              |
                                         WAN / IPsec / MPLS
```

Every later module adds one box in that path. Troubleshooting walks the path **left to right**, then **policy**, then **overlay**.

## Common intern mistakes

| Mistake | What to do instead |
|---------|-------------------|
| “The network is down” | Name the pair of addresses and the test that failed |
| Using public 8.8.8.8 as the only ping | Test the **next hop** first |
| Mixing decimal mask and CIDR casually | Write both: `10.0.0.1/30` (`255.255.255.252`) |
| Assuming VLAN 1 is fine | Lab uses named VLANs; VLAN 1 is often leftover |
| Treating ping as V&V for an app ICD | Test the **actual port** (SSH, 443, 61616, …) |

## Drill (30–40 min)

On paper or a jump VM (no device changes):

1. For `10.0.0.4/30`, list network, two usable hosts, broadcast.  
2. Host `10.10.10.50/24`, gateway `10.10.10.1` — will it ARP for `10.10.20.10`? For `10.10.10.20`?  
3. Write one sentence: why ping to a server can succeed while a browser to `https://…` fails.  
4. Sketch Site-A user → Site-B user using the welcome topology; label VLAN, L3 hop, WAN.  
5. Convert `255.255.255.248` to prefix length.

## Integrity

- Do not scan address space you were not given.  
- Do not treat campus Wi-Fi as a lab.  
- Unclassified notes only.

## Further reading

| Topic | Source |
|-------|--------|
| CIDR | [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632) |
| ARP | [RFC 826](https://www.rfc-editor.org/rfc/rfc826) |
| ICMP | [RFC 792](https://www.rfc-editor.org/rfc/rfc792) |
| TCP | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) (modern TCP spec) |

## Next

**Junos CLI and the commit model** — how older Juniper boxes store and activate configuration.
