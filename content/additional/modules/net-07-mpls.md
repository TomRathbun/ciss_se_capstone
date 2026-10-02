# MPLS Tunnels — LDP, RSVP-TE, and L3VPN

## Learning outcomes

After this module you can:

- Explain an **LSP** as a **labeled tunnel** across a core  
- Contrast **LDP** and **RSVP-TE**  
- List the **dependency chain** (IGP → `family mpls` → LDP/RSVP → iBGP → VRF)  
- Read **RD / RT / routing-instance type `vrf`**  
- Be honest about **which older platforms** can be a PE  

## Why MPLS exists in this program

Sites want **separation** (VPN) and **engineered paths** without a full mesh of IPsec. The core forwards **labels**; customer IP stays at the edge.

```text
CE/SRX-A --IPv4-- PE-1 ======= LSP ======= PE-2 --IPv4-- CE/SRX-B
                 push              swap           pop (PHP)
```

SE link: an L3VPN is a **system boundary**. RD/RT are interface identifiers between PEs — treat them like ICD fields.

## Words

| Term | Meaning |
|------|---------|
| **Label** | 20-bit tag (plus TC/TTL) prepended to the packet |
| **FEC** | Forwarding Equivalence Class — packets that share a label path (often a prefix) |
| **LSR** | Label-switch router (P / PE) |
| **LER / PE** | Edge — impose/remove labels |
| **P** | Core — swap labels only |
| **LSP** | Label-switched path — the **tunnel** |
| **PHP** | Penultimate hop popping — last P pops so PE sees IP or VPN label |
| **LDP** | Distributes labels for IGP prefixes; simple |
| **RSVP-TE** | Signals an explicit/TE LSP; can reserve bandwidth |
| **L3VPN** | Per-customer routing table + VPN label + iBGP |

MPLS is **not** encryption. Anyone on the core path who can capture may see customer IP unless an **encryptor** or IPsec sits outside or on the PE.

## Platform honesty (older Juniper)

| Box | MPLS role in *this* course |
|-----|----------------------------|
| EX2200 / EX4200 access | Generally **not** a PE |
| Branch SRX (100–650) | **Not** your L3VPN PE — use as CE |
| SRX1400 / 3600 / 5600 | Maybe; only if instructor confirms license/Junos |
| **MX80 / MX104 / MX240** (or vMX) | Default **PE** |
| No PE hardware | Worksheet + `show mpls lsp` captures |

If you only have SRX240s, you still complete the assignment on **paper configs** and provided outputs. Do not “turn on MPLS” on a branch box and declare victory.

## Dependency chain (memorize)

```text
1. Interfaces up; /30s correct
2. IGP (OSPF) Full; ping PE lo0 sourced from lo0
3. family mpls on core-facing IFLs
4. protocols mpls + ldp (or rsvp + label-switched-path)
5. show ldp neighbor / show mpls lsp  (paths UP)
6. iBGP (inet-vpn unicast) between PEs
7. routing-instance type vrf + RD + vrf-target + CE interface
8. CE routing (static, OSPF, or eBGP) into the VRF
```

Skip a step and the next show command lies.

## LDP vs RSVP-TE

### LDP (usual lab)

```text
set interfaces ge-0/0/0 unit 0 family mpls
set protocols mpls interface ge-0/0/0.0
set protocols ldp interface ge-0/0/0.0
set protocols ldp interface lo0.0
```

LDP builds LSPs to **IGP loopbacks** automatically.

```text
show ldp neighbor
show ldp session
show route table inet.3
show mpls lsp
```

`inet.3` is where BGP looks for a **tunnel** to the BGP next-hop. Empty `inet.3` → VPN routes stay hidden.

### RSVP-TE (constrained tunnel)

```text
set protocols rsvp interface ge-0/0/0.0
set protocols mpls label-switched-path PE1-TO-PE2 to 10.255.255.2
set protocols mpls interface ge-0/0/0.0
```

Use when you need a **named LSP**, bandwidth, or explicit path. Both LDP and RSVP can coexist; do not enable both on a shared PE without a plan.

```text
show rsvp session
show mpls lsp name PE1-TO-PE2 detail
```

## L3VPN (VRF) on a PE

Junos name: **routing-instance** `instance-type vrf`.

```text
set routing-instances VPN-SITE instance-type vrf
set routing-instances VPN-SITE interface ge-0/1/0.0
set routing-instances VPN-SITE route-distinguisher 65000:10
set routing-instances VPN-SITE vrf-target target:65000:10
set routing-instances VPN-SITE routing-options static route 10.10.10.0/24 next-hop 10.0.0.5
```

| Field | Role |
|-------|------|
| **RD** `65000:10` | Makes prefixes unique in BGP (not the selector) |
| **RT** `target:65000:10` | **Import/export** selector — who gets the route |
| CE IFL | **Only** in the VRF, not in `inet.0` |

PE-PE VPN signaling:

```text
set protocols bgp group IBGP type internal
set protocols bgp group IBGP local-address 10.255.255.1
set protocols bgp group IBGP family inet-vpn unicast
set protocols bgp group IBGP neighbor 10.255.255.2
```

```text
show route table VPN-SITE.inet.0
show route advertising-protocol bgp 10.255.255.2 table VPN-SITE.inet.0
```

Mismatched RT = empty remote VRF. Same RD, different RT is legal but confusing — keep them aligned in the lab unless taught otherwise.

## GRE as the simple cousin

`gr-` interfaces encapsulate IP in IP. Useful on **branch SRX** when MPLS is not available. GRE is **not** confidential. If you need both reachability and secrecy: **IPsec** (next module), optionally GRE-over-IPsec.

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| `family mpls` missing on one core hop | LSP down |
| IGP not advertising lo0 | LDP/RSVP has no FEC |
| VRF IFL also in `inet.0` / a zone on a PE-SRX | Commit or leak |
| RT typo (`65000:10` vs `65000:100`) | One-way VPN |
| Debugging VPN before `inet.3` is populated | Wasted hour |
| Calling MPLS “encryption” | Wrong and unsafe assumption |

## Drill (45 min)

1. On PE (or capture): `show ldp neighbor` or `show rsvp session` + `show mpls lsp`.  
2. `show route table inet.3` — do PE loopbacks appear?  
3. List RD and RT from `show routing-instances` (or paper).  
4. Write the 8-step dependency chain in your own words.  
5. One paragraph: why a branch SRX is a **CE**, not this lab’s PE.

## Integrity

- Do not add a second `vrf-target` that imports another intern’s VPN.  
- Do not capture customer payloads on a P router “to see MPLS.”  
- Unclassified RD/RT only.

## Further reading

| Topic | Source |
|-------|--------|
| MPLS architecture | [RFC 3031](https://www.rfc-editor.org/rfc/rfc3031) |
| LDP | [RFC 5036](https://www.rfc-editor.org/rfc/rfc5036) |
| BGP/MPLS IP VPNs | [RFC 4364](https://www.rfc-editor.org/rfc/rfc4364) |
| Junos | TechLibrary MPLS / Layer 3 VPNs for **MX** Junos version |

## Next

**Encryptors and IPsec** — confidentiality the MPLS core does not provide.
