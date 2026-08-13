# Encryptors and IPsec

## Learning outcomes

After this module you can:

- Separate **dedicated inline encryptors** from **SRX IPsec** (both appear in older racks)  
- Build a **route-based** VPN (`st0`) with IKE + IPsec proposals on older Junos  
- Match **proxy-IDs / traffic selectors** when a peer is policy-based  
- Read **`show security ike sa`** and **`show security ipsec sa`**  
- Apply **red / black** discipline without inventing COMSEC procedure  

## Two devices people call “the encryptor”

| Kind | What it is in this course | Hands-on? |
|------|---------------------------|-----------|
| **SRX IPsec** | Junos `security ike` + `security ipsec` + `st0` | Yes — primary lab |
| **Dedicated inline encryptor** | Bump-in-the-wire box (HAIPE / TACLANE-class *concept*) between red router and black WAN | Awareness + cabling worksheet only |
| **MACsec** | Hop-by-hop Ethernet encryption on some EX/MX | Awareness |
| **TLS** | Session crypto for apps | **Admin** track, not this module |

MPLS labels are **not** encryption. If the requirement is confidentiality, you need **crypto**, not just a VPN routing-instance.

SE link: algorithms, lifetimes, and peer IPs belong in an **ICD / security agreement**. Key handling is an **ops + integrity** constraint.

## Red / black (unclassified model)

```text
  RED (site, clear)     ENCRYPTOR or SRX IPsec      BLACK (WAN, ciphertext)
  users, EX, TRUST   →  encrypt / decrypt        →  PE, Internet, leased line
```

Rules you *will* follow:

1. Do not bridge red and black Ethernet “to test.”  
2. Do not put a red user VLAN on a black-only switch.  
3. Do not photograph key fill ports, CIKs, or key labels.  
4. Do not ask classmates to share **live** PSKs or production proposals in chat.  
5. Dedicated devices: **instructor + two-person** control if any keying is demonstrated. Interns do **not** invent fill procedures.

If a dedicated encryptor is in path, treat it as a **black box**: confirm power, sync/alarm LEDs per the local runbook, and that red/black cables are in the **correct** ports. Troubleshooting is **cabling + power + ticket**, not “debug the algorithm.”

## IPsec building blocks

```text
IKE (Phase 1)     authenticate peers, build IKE SA (control)
     ↓
IPsec (Phase 2)   ESP (usual) protects user packets; IPsec SA (data)
     ↓
st0.x             route-based virtual point-to-point (Juniper-preferred)
```

| Item | Lab guidance on older SRX (12.1X46 / 15.1X49) |
|------|-----------------------------------------------|
| IKE version | **IKEv1** still common; IKEv2 if both peers support it |
| DH | Prefer **group14**; very old peers may only do group2 (document it) |
| Encryption | **aes-256-cbc** (or aes-128-cbc); 3DES is legacy |
| Integrity | **sha-256**; sha1 is legacy |
| ESP vs AH | **ESP**; AH is rare |
| Auth | Lab **PSK**; certificates if the instructor issued them |

Write the **proposal matrix** in the assignment. Both sides must match or Phase 1 never completes.

## Route-based vs policy-based

| | Route-based (`st0`) | Policy-based |
|--|---------------------|--------------|
| Juniper default | Yes | Legacy / interop |
| Traffic selection | **Route** to `st0` + policy TRUST→VPN | Interesting traffic in the policy |
| Proxy-ID | Often `0.0.0.0/0` ↔ `0.0.0.0/0` | Must match peer subnets **exactly** |
| Good for | OSPF/BGP over tunnel, many prefixes | One or two subnets to a Cisco/policy peer |

**Proxy-ID mismatch** is the #1 interop failure: Site-A thinks `10.10.10.0/24` ↔ `10.20.10.0/24`; Site-B thinks `/16` or reversed.

```text
set security ipsec vpn VPN-B ike proxy-identity local 10.10.10.0/24
set security ipsec vpn VPN-B ike proxy-identity remote 10.20.10.0/24
```

(Exact knobs vary slightly by Junos — `show security ipsec` help / version doc.)

## Shape: Site-A SRX to Site-B SRX

Addresses from the welcome plan: WAN peers on the `/30` toward the PE or a simulated Internet; overlay `10.255.100.0/30` on `st0`.

```text
# IKE
set security ike proposal IKE-LAB authentication-method pre-shared-keys
set security ike proposal IKE-LAB dh-group group14
set security ike proposal IKE-LAB authentication-algorithm sha-256
set security ike proposal IKE-LAB encryption-algorithm aes-256-cbc
set security ike policy IKE-LAB-POL mode main
set security ike policy IKE-LAB-POL proposals IKE-LAB
set security ike policy IKE-LAB-POL pre-shared-key ascii-text "USE-LAB-SHEET-ONLY"
set security ike gateway GW-B ike-policy IKE-LAB-POL
set security ike gateway GW-B address 10.0.1.2
set security ike gateway GW-B external-interface ge-0/0/0.0

# IPsec + bind st0
set security ipsec proposal IPSEC-LAB protocol esp
set security ipsec proposal IPSEC-LAB authentication-algorithm hmac-sha-256-128
set security ipsec proposal IPSEC-LAB encryption-algorithm aes-256-cbc
set security ipsec policy IPSEC-LAB-POL proposals IPSEC-LAB
set interfaces st0 unit 0 family inet address 10.255.100.1/30
set security ipsec vpn VPN-B bind-interface st0.0
set security ipsec vpn VPN-B ike gateway GW-B
set security ipsec vpn VPN-B ike ipsec-policy IPSEC-LAB-POL
set security ipsec vpn VPN-B establish-tunnels immediately

# Zones: st0 in a VPN zone (cleanest)
set security zones security-zone VPN interfaces st0.0
set security zones security-zone UNTRUST host-inbound-traffic system-services ike

# Route interesting traffic into the tunnel
set routing-options static route 10.20.10.0/24 next-hop st0.0
```

Still required: **security policies** TRUST→VPN and VPN→TRUST for the real applications (not only ping).

On 12.1X46 some algorithm names differ slightly (`sha-256` vs older `sha256`). If commit rejects a proposal, `help topic security ike` on **that** box — do not copy 21.x docs blindly.

**Never commit the lab PSK into Git.** Write `ascii-text <redacted>` in deliverables.

## Evidence

```text
show security ike sa
show security ipsec sa
show security ipsec statistics
show interfaces st0.0
show route 10.20.10.0/24
ping 10.255.100.2
```

| Observation | Meaning |
|-------------|---------|
| No IKE SA | Peer IP, ike host-inbound, UDP/500 (and 4500 NAT-T), proposal mismatch, PSK |
| IKE up, no IPsec SA | Phase 2 proposal or proxy-ID |
| SAs up, ping fail | Route not via `st0`, zone/policy, wrong source address |
| SA bounce every few seconds | Lifetime mismatch or flapping route / DPD |

## Dedicated encryptor worksheet (no keys)

When `enc-a-01` is in rack:

| Check | Pass looks like |
|-------|-----------------|
| Placement | Red cable to SRX/EX, black cable to WAN/PE — labels match |
| Power / alarm | Green/sync per local card; any alarm = ticket, not reset spam |
| Bypass | Know whether fail-open is **forbidden** (usually yes on classified-adjacent systems) |
| Addressing | Encryptor may be L2 bump (same subnet) or L3 — copy the runbook, do not guess |
| Your job | Path documentation + escalate; no “debug crypto” |

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| Policy-based one side, route-based the other, ignore proxy-ID | Phase 2 fail |
| Missing `ike` host-inbound on UNTRUST | No SA |
| `st0` not in a zone | Junos commit or silent drop |
| Default route into `st0` by accident | Management blackhole |
| Pasting PSK into a screenshot | Integrity fail |
| Calling the PE “the encryptor” | Wrong device, wrong ticket |

## Drill (45 min)

1. Draw red vs black for Site-A including SRX, optional `enc-a-01`, and PE.  
2. Proposal table: IKE and IPsec algorithms you would use on 15.1X49.  
3. On SRX or capture: `show security ike sa` + `show security ipsec sa`.  
4. Write `set` lines for `st0.0` + static to `10.20.10.0/24` (redact PSK).  
5. Three-row fault table: no IKE / IKE-no-IPsec / SA-up-no-ping.

## Integrity

- Lab PSK from the **instructor sheet** only; rotate if leaked.  
- No real COMSEC material.  
- No photos of dedicated encryptor key ports.  
- No attempts to break or weaken crypto.

## Further reading

| Topic | Source |
|-------|--------|
| IPsec architecture | [RFC 4301](https://www.rfc-editor.org/rfc/rfc4301) |
| IKEv2 (concepts) | [RFC 7296](https://www.rfc-editor.org/rfc/rfc7296) |
| Junos VPN | TechLibrary *IPsec VPN Feature Guide* for **15.1X49 / 12.1X46** |
| Dedicated devices | Local unclassified runbook only |

## Next

**HA and change control** — chassis cluster awareness and commits that do not take the site down.
