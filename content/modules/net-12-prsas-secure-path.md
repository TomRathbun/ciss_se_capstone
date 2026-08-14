# PRSAS — Firewalls & Site-to-Site IPsec

> **Phase:** implementation. Applies **net-04** and **net-08** to the three-site picture.

## Learning outcomes

After this module you can:

- Build **zones** per site (radar, servers, users, vpn, mgmt, untrust/black)  
- Write **least-privilege** security policies for 61617 / 5432 / IPA  
- Stand up **route-based IPsec** (`st0`) Remote A↔Central and Remote B↔Central  
- Keep **IKE/IPsec proposals** in a matrix (no PSK in the write-up)  
- Know when a packet should fail at **policy** vs **IKE** vs **routing**  

## Zone sketch (Central)

| Zone | Interfaces (teaching) | Host-inbound |
|------|----------------------|--------------|
| `trust-servers` | VLAN 20 irb | ssh limited, ike **no** |
| `trust-users` | VLAN 10 irb | ping optional |
| `vpn-a` / `vpn-b` | `st0.1` / `st0.2` | — |
| `black-wan` | uplink | **ike**, ping optional |
| `mgmt` | VLAN 99 / fxp0 | ssh, https to console hosts |

Remote sites: `trust-radar` + `black-wan` + `mgmt` is enough.

## Policy intent

```text
trust-radar  → vpn     permit junos-tcp dest 61617
vpn          → trust-servers  permit 61617 to amq-c-01
trust-users  → trust-servers  permit 61617, 443
trust-servers→ trust-servers  permit 5432 (daemon → pg)
mgmt         → any     (jump host only; document)
deny log     otherwise
```

Source NAT: **usually off** on the lab overlay (you want to see real RFC1918 in logs). If you NAT, write why.

## IPsec (route-based)

Same discipline as NET-A08, twice (A and B).

| Item | Lab default unless the box rejects it |
|------|----------------------------------------|
| IKE | IKEv1 or v2 as supported; DH **group14**; aes-256; sha-256 |
| Auth | PSK from instructor envelope — **redact** |
| IPsec | ESP, PFS on if supported |
| `st0` | numbered /30 from se-12 |
| Routes | remote radar /24 via `st0.x` |
| Proxy-ID | only if a peer is policy-based |

```text
show security ike sa
show security ipsec sa
show security flow session destination-port 61617
```

## Encryptor honesty

Project BOM allows a **virtual** pfSense/VyOS **or** SRX as the encryptor. Dedicated inline encryptors stay **black-box awareness** (net-08). Do not invent fill procedures.

## Monday workshop (builds NET-A12)

1. **20 min** — Zone table + host-inbound.  
2. **25 min** — Policy set list (candidate config, `commit check` if live).  
3. **25 min** — IPsec matrix + `st0` addressing.  
4. **10 min** — Expected `show` output table if the tunnel is not up yet.

## Thursday assignment

**NET-A12 — Secure path pack.**

## Next

**Validate & config guide** — pings are not enough; prove 61617 and produce the runbook.
