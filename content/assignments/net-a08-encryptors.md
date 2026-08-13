# NET-A08 — IPsec / Encryptor Pack

**Weight:** 10% · **Due:** After net-08-encryptors · **Module:** net-08-encryptors

## Prompt

Design (and, if the bench allows, evidence) a **route-based IPsec** tunnel for Site-A ↔ Site-B, plus a **red/black** note for any dedicated encryptor.

## Deliverables

1. **Red/black diagram:** users/EX/SRX (red), SRX IPsec and/or `enc-a-01` (boundary), PE/WAN (black).  
2. **Proposal matrix:** IKE and IPsec (auth method, DH, encryption, integrity, IKE version). Choose values that fit **12.1X46 / 15.1X49** unless the box rejects them — then document what committed.  
3. **Route-based design:** `st0` address, bind, `establish-tunnels`, static or routing into `st0`, zones (including **`ike` host-inbound** on the black zone), TRUST↔VPN policies (not ping-only if HTTPS is in scope). **PSK redacted.**  
4. **Proxy-ID note:** what you would set if the far end is policy-based with `10.10.10.0/24` ↔ `10.20.10.0/24`.  
5. **Evidence:** `show security ike sa` and `show security ipsec sa` **or** a three-row expected-output table if no tunnel is live.  
6. **Dedicated encryptor:** five operational checks you would perform **without** key fill (or “not in rack”).  
7. **Fault table:** no IKE; IKE but no IPsec; SA up but no user traffic.

## Quality bar

- No PSK, certificate, or key-fill material in the submission.  
- Route-based vs policy-based is explicit.  
- No invented COMSEC procedure.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| design | 15 | Matching proposals, st0, zones, routes, policies |
| ops_discipline | 10 | Red/black, redaction, dedicated-box restraint |
| communication | 5 | Diagram + matrix + sets |
