# NET-A06 — BGP Neighbor & Policy Lab

**Weight:** 10% · **Due:** After net-06-bgp · **Module:** net-06-bgp

## Prompt

Work **BGP** (Border Gateway Protocol — not “BGB”) as an intern would on Site-A edge: neighbor state, what is advertised, and a tight export policy.

## Deliverables

1. **ASN map:** Site-A / core / Site-B ASNs (lab defaults or remaps). eBGP vs iBGP on each link.  
2. **`show bgp summary`** (live or capture): peer, AS, state, prefixes In/Out. If `Active`/`Idle`, interpret — do not call it “working.”  
3. **Export policy** that advertises **only** Site-A user and server prefixes (`10.10.10.0/24`, `10.10.20.0/24` or remaps) and **rejects** the rest. Full `policy-options` + `protocols bgp group` `set` lines.  
4. **Receive/advertise:** `show route receive-protocol bgp` and `advertising-protocol` excerpts **or** a written expected prefix list if BGP is worksheet-only.  
5. **Attribute note:** in 5–8 lines, what **local-pref**, **AS-path**, and **next-hop** mean; when **next-hop-self** appears.  
6. **Two reasons** Established can still mean users cannot pass traffic.

## Quality bar

- Junos **policy-statement**, not IOS route-maps.  
- No “accept all” import.  
- Private ASNs only unless instructor issued otherwise.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| protocol | 15 | States, eBGP/iBGP, attributes used correctly |
| policy | 10 | Tight export; Junos policy shape |
| communication | 5 | Summary a peer can peer-review |
