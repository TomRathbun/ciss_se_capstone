# NET-A02 — Junos CLI & Commit Lab

**Weight:** 10% · **Due:** After net-02-junos-cli · **Module:** net-02-junos-cli

## Prompt

On an assigned **EX or SRX** (or instructor terminal server), show you can operate the **candidate / commit** model safely.

## Deliverables

1. **Box identity:** hostname, **model**, **Junos version** (`show version`), uptime.  
2. **Interface inventory:** `show interfaces terse` excerpt — identify management, one access/LAN, one uplink/WAN (labels).  
3. **Commit model notes:** distinguish operational vs config mode; candidate vs active; what `commit confirmed 5` does.  
4. **Safe change evidence** (pick one, instructor-approved):
   - add/change an **interface description** on an unused or assigned port, **or**  
   - `show | compare` of a change you then **`rollback 0`** (discard)  
   Include `show | compare` and `show system commit` (or a clear discard story).  
5. **Rollback story:** how you would undo the last commit (`rollback 1`) vs discard an uncommitted candidate (`rollback 0`).  
6. Redact secrets / `$9$` hashes if present.

## Quality bar

- No IP/zone/VLAN changes on shared uplinks.  
- `configure exclusive` mentioned if the box is shared.  
- Version is recorded — not “some Junos.”

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| process | 15 | Modes, compare, commit/rollback understood |
| safety | 10 | Exclusive/confirmed/rescue thinking; no blast radius |
| communication | 5 | Labeled excerpts a peer can repeat |
