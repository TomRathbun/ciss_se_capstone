# NET-A03 — EX VLAN / Trunk Worksheet

**Weight:** 10% · **Due:** After net-03-switching · **Module:** net-03-switching

## Prompt

Document the **access switch** path for Site-A users (VLAN 10) and how it trunks toward core / SRX.

## Deliverables

1. **Platform note:** model + Junos; **ELS vs non-ELS** (did `port-mode` or `interface-mode` apply?). VC or standalone (`show virtual-chassis` or “n/a”).  
2. **Port table** (≥ 4 ports): name, description, access/trunk, VLAN members — from the box or a complete paper design if no EX.  
3. **Uplink / LLDP:** neighbor of the uplink (`show lldp neighbors` or cable map).  
4. **MAC evidence:** one line from `show ethernet-switching table` **or** a filled example the instructor provided.  
5. **Proposed `set` list** (do not apply unless told) for a new access port in VLAN **USERS / 10**.  
6. **Handoff sentence:** is the **SRX** or the **EX SVI** the user default gateway in *your* bench design?

## Quality bar

- Syntax matches the OS generation (no ELS commands on EX4200).  
- VLAN 10 exists on **both** access and trunk in the design.  
- No STP disable advice.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| design | 15 | Coherent access/trunk/VLAN/handoff |
| evidence | 10 | Real show output or honest worksheet + source |
| communication | 5 | Table + sets a peer could apply |
