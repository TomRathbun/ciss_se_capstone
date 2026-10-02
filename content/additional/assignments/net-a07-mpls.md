# NET-A07 — MPLS Tunnel & L3VPN Worksheet

**Weight:** 10% · **Due:** After net-07-mpls · **Module:** net-07-mpls

## Prompt

Explain **MPLS LSPs** and a **single L3VPN** between Site-A and Site-B. Use PE show commands if an MX/vMX exists; otherwise a **complete paper PE design** plus any instructor captures.

## Deliverables

1. **Platform honesty:** what is PE on your bench (MX / vMX / mid-SRX / **worksheet**). Why a branch SRX is a **CE**.  
2. **Dependency chain:** the 8 steps from the module, checked against *your* lab (done / missing / N/A).  
3. **Tunnel evidence:** `show ldp neighbor` **or** `show rsvp session` **and** `show mpls lsp` **and** whether PE loopbacks sit in `inet.3` — or annotated captures.  
4. **VRF sketch:** routing-instance name, CE interface, **RD**, **RT**, how CE prefixes get in (static / OSPF / eBGP).  
5. **`set` list** for one PE VRF + `family inet-vpn unicast` iBGP neighbor (loopback).  
6. **One paragraph:** why MPLS is **not** an encryptor; what you would add if confidentiality is required.

## Quality bar

- LDP vs RSVP not mixed up.  
- RD vs RT roles are distinct.  
- No claim that EX4200 access is a PE.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| concepts | 15 | LSP, LDP/RSVP, VRF, RD/RT, inet.3 |
| design | 10 | Coherent PE `set` list / chain |
| communication | 5 | Worksheet a second intern could implement |
