# Network Troubleshooting on Junos

## Learning outcomes

After this module you can:

- Walk a **symptom → hypothesis → smallest probe** loop on EX/SRX/PE  
- Choose **show / ping / traceroute / session** before any `delete`  
- Build an **evidence pack** a peer can continue  
- Avoid **traceoptions** and session-clears that take down a shared old box  

## Method (same spine as the admin track)

```text
1. Symptom     who, two addresses, application, when, last-good
2. Timeline    last commit / cable move / power
3. Freeze      show version, interfaces terse, cluster/VC, commit list
4. Hypotheses  ranked; each has a read-only test
5. Probe       one test
6. Change      one, recorded
7. Verify      original user test — not only ping
8. Write       cause, fix, prevention
```

SE link: this pack is **verification evidence** and a defect report.

## Layered fault tree (use in order)

```text
L1   light / SFP / `Physical link is down` / errors increasing
L2   VLAN, trunk membership, MAC table, STP blocked, ARP
L3   address/mask, gateway, `show route`, OSPF/BGP state
POL  SRX zone, host-inbound, policy, NAT, screens
OVLY MPLS inet.3 / LSP; IPsec IKE/IPsec SA; encryptor alarms
APP  correct TCP/UDP port, MSS/PMTU, ALG
```

Do not start at BGP because it is interesting.

## Junos probes (read-only first)

### Identity and change

```text
show version
show system commit
show system uptime
show chassis cluster status          # if SRX cluster
show virtual-chassis                 # if EX VC
```

### Link and Ethernet

```text
show interfaces terse
show interfaces ge-0/0/1 extensive | match "Physical|link|error|rate|Duplex|CRC"
show ethernet-switching table
show ethernet-switching interfaces
show lldp neighbors
show arp
show spanning-tree interface
```

Rising **input errors / CRC / discards** = cabling, duplex, bad SFP — not a policy problem.

### Route and protocol

```text
show route <dest>
show ospf neighbor
show bgp summary
show route receive-protocol bgp <peer>
```

### SRX policy / session

```text
show security zones
show security policies from-zone TRUST to-zone UNTRUST
show security flow session destination-prefix 10.10.20.10
show security nat source summary
```

Session **present** → L3/policy already succeeded. Debug the **port**, NAT, or app.

Session **absent** + ping fail → zone/policy/route/NAT.

### Overlay

```text
show security ike sa
show security ipsec sa
show mpls lsp
show ldp neighbor
show route table inet.3
show route table VPN-SITE.inet.0
```

### Traffic on the box (careful)

```text
monitor traffic interface ge-0/0/1 no-resolve count 20
```

Use a **count** or matching filter. Unfiltered `monitor traffic` on a core port floods your SSH session.

`ping` / `traceroute` with **`source`**:

```text
ping 10.20.10.1 source 10.10.10.1 rapid count 20
```

## What not to do on older lab gear

| Action | Why not |
|--------|---------|
| `traceoptions` to `/var/log` without a plan | Fills flash; SRX100/210 become unbootable-ish |
| `clear security flow session` (all) | Drops every user |
| `request system reboot` to “fix BGP” | Hides the cause |
| `delete` a stanza you did not `show` first | Shared-box vandalism |
| Disable RSTP / screens / cluster | Creates a bigger incident |

If you need traces: instructor-approved file, `flag error` only, **delete traceoptions in the same window**.

## Hypothesis table (steal this)

| # | Hypothesis | Read-only test | Expected if true |
|---|------------|----------------|------------------|
| 1 | Access VLAN wrong | `show ethernet-switching interfaces ge-0/0/10` | Wrong VLAN / no membership |
| 2 | Trunk missing VLAN | `show vlans USERS` | VLAN not on uplink |
| 3 | No route | `show route 10.20.10.0/24` | no-entry or discard |
| 4 | SRX policy | `show security flow session` + policies | no session |
| 5 | IPsec down | `show security ike sa` | no SA |
| 6 | Proxy-ID | IPsec SA / peer log | Phase 2 fail |

## Worked mini-case (pattern)

**Symptom:** User `10.10.10.50` cannot reach `https://10.20.10.20`. Ping to `10.20.10.20` works.

| Step | Result |
|------|--------|
| ARP for gateway | OK |
| `show route 10.20.10.20` on SRX | via `st0.0` |
| IKE/IPsec SA | UP |
| `show security flow session destination-prefix 10.20.10.20 destination-port 443` | **empty** |
| Policy TRUST→VPN | `junos-ping` only |

**Cause:** policy allows ICMP, not TCP/443. **Fix:** add `junos-https`. **Prevention:** policies follow the ICD port list, not “pinged so it’s fine.”

## Evidence pack template

1. Symptom sentence (two IPs, port, time).  
2. `show version` + last commit.  
3. Path sketch (EX → SRX → overlay → far CE).  
4. Hypotheses (3+).  
5. Command excerpts (labeled).  
6. One change or “no change — escalate.”  
7. Verify / remaining risk.

Redact PSKs, user identifiers if asked, and any non-lab prefixes.

## Common intern mistakes

| Mistake | Better |
|---------|--------|
| Restart first | Show first |
| Ping-only V&V | Test the **application port** |
| Pasting 4000-line `extensive` | Match-filter the relevant lines |
| Three simultaneous `set`s | You will not know which fixed it |

## Drill (50 min)

Use a real lab fault, an instructor inject, or a **documented** historical incident:

1. Fill the symptom template.  
2. Freeze: version, interfaces terse, commit.  
3. Three hypotheses with read-only tests.  
4. Run at least **five** commands from two layers.  
5. Write cause / fix / prevention (even if the fix was not applied).

## Integrity

- Stay inside the lab prefix list.  
- No attacking tools (`nmap` sweeps, crafted floods) unless the assignment explicitly opens a range.  
- Honest captures — do not edit `show` output.

## Further reading

| Topic | Source |
|-------|--------|
| Flow | Juniper KB: troubleshooting SRX flow sessions |
| MPLS | `show mpls lsp extensive` fields (TechLibrary) |
| Method | Course **admin-09-troubleshooting** (same spine, Linux tools) |

## Next

You have the full NET path. Complete remaining assignments; pair with **admin** for Linux-side `ss`/`tcpdump` and **SE** for ICD/NFR write-ups.
