# NET-A01 — Addressing & Path Worksheet

**Weight:** 5% · **Due:** After net-01-foundations · **Module:** net-01-foundations

## Prompt

Prove you can **do IPv4 math** and describe a packet path **without Junos syntax**.

## Deliverables

1. **Subnet sheet** for all of:
   - `10.10.10.0/24` — network, first/last host, broadcast, example PC + gateway  
   - `10.0.0.4/30` — both usable addresses and who (SRX vs PE) should own each  
   - `10.255.255.11/32` — what this kind of prefix is for  
2. **Mask conversion:** write prefix and dotted mask for `/24`, `/30`, `/29`, `/16`.  
3. **ARP vs route:** for PC `10.10.10.50/24` gw `10.10.10.1`, state whether the PC ARPs for `10.10.10.20` and for `10.20.10.20` — and why.  
4. **Path sketch** (Mermaid or labeled ASCII): Site-A user → Site-B user using the welcome fabric. Mark VLAN, L3 hop, WAN/overlay.  
5. **TCP vs ICMP:** one paragraph — why ping success does not verify HTTPS.

## Quality bar

- Arithmetic is correct.  
- Sketch matches the shared fabric (or an instructor remap you document).  
- No device commits required.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| correctness | 15 | Subnet math and ARP/on-link reasoning |
| path_clarity | 10 | Sketch a peer can brief |
| communication | 5 | Tables readable; units labeled |
