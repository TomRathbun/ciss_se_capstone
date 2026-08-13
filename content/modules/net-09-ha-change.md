# HA and Change Control

## Learning outcomes

After this module you can:

- Use **`commit confirmed`**, **rollback**, and **rescue** as a habit, not a rescue fantasy  
- Describe **SRX chassis cluster** pieces: control, fabric, RG0, RG1, `reth`  
- Write a **change window** with verify and backout  
- Know what **not** to touch on a clustered pair  

## Why this module exists

Older branch SRX and EX4200 VC are unforgiving: small flash, shared labs, one bad commit removes management. Selection cares whether you can change a network **without becoming the outage**.

SE link: backout and verify steps are **V&V** for a configuration change.

## The change loop (every time)

```text
1. Capture baseline     show | display set  / show interfaces terse
2. Exclusive configure
3. Minimum delta        show | compare
4. commit check
5. commit confirmed 5   (or 10)
6. Verify               ping, session, neighbor, SSH from jump host
7. commit               (confirm) + commit comment "ticket / lab id"
8. If bad               wait for rollback — or rollback 1 immediately
```

**Rescue** at the start of a lab day (once, known-good):

```text
request system configuration rescue save
```

**Archive** (if permitted):

```text
show configuration | display set | save /var/tmp/srx-a-fw-01-set.txt
```

Copy off-box. Do not fill `/var/tmp` with 50 dumps on a 1 GB SRX100.

### Comments are evidence

```text
commit comment "NET-A09: add junos-https TRUST->VPN"
show system commit
```

Assignments that show `commit comment` history score higher than “I think I committed.”

## What can isolate you

| Change | Risk |
|--------|------|
| Wrong zone on `fxp0` / `me0` | Lose SSH |
| Filter on lo0 | Lose protocol + management |
| Default route to `st0` or `discard` | Blackhole |
| `delete security zones` | Everything dies |
| VC / cluster control-link | Split brain |

Mitigation: **out-of-band console** on lab benches; `commit confirmed`; second window already pinging.

## SRX chassis cluster (awareness + vocabulary)

Two SRXs act as one logical firewall.

```text
        RG1 (data, reth)
   reth0 TRUST -------- users
   reth1 UNTRUST ------ WAN
        |
   node0  +ctrl+fab+  node1
        RG0 (Routing Engine)
```

| Piece | Job |
|-------|-----|
| **Control link** | Heartbeat, config sync (`fxp1` or dedicated) |
| **Fabric (`fab`)** | Data sync / session sync |
| **RG0** | Which node is primary **RE** |
| **RG1+** | Which node is primary for **reth** groups |
| **`reth`** | Redundant Ethernet — members on **both** nodes |
| **Preempt / monitor** | Failover policy; IP / interface monitoring |

Node 1 port offset is **model-specific** (SRX240 often node1 = `ge-5/0/x`). Always `show chassis cluster status` and `show interfaces terse`.

```text
show chassis cluster status
show chassis cluster interfaces
show chassis cluster statistics
```

Healthy: both nodes **present**, RG primary/secondary as designed, no **ineligible** / **disabled**.

Interns **do not**:

- `set chassis cluster cluster-id` on a live pair  
- Recable control/fabric  
- `request chassis cluster failover` without instructor  
- Mix Junos versions on the two nodes  

You **do**: identify `reth`, which node is primary, and whether your change is on the **logical** `reth0.0` (correct) or a child `ge-0/0/1` (usually wrong).

## EX4200 Virtual Chassis (ops note)

From the switching module: two masters = **split**. Do not power-cycle members independently to “fix” a VC. Capture `show virtual-chassis` and escalate.

## Change ticket fields (steal this)

| Field | Example |
|-------|---------|
| Device / version | `srx-a-fw-01` JUNOS 15.1X49-D236 |
| Window | 10 min, console held |
| Intent | Permit TCP/443 USERS → `10.10.20.10` |
| Delta | `show \| compare` attached |
| Verify | session present; curl from jump VM |
| Backout | `rollback 1` + `commit` or wait `confirmed` |
| Risk | low — new policy term only |

This is the same professionalism as admin tickets.

## Common intern mistakes

| Mistake | Result |
|---------|--------|
| `commit` on a path-changing change, no `confirmed` | Truck roll / instructor console |
| Editing `ge-0/0/1` instead of `reth0` | Change disappears on failover |
| No baseline `display set` | Cannot prove what you broke |
| Failover test on a shared pair | Dual outage |

## Drill (30–40 min)

1. `show system commit` — last three comments.  
2. If clustered: `show chassis cluster status` — fill RG0/RG1 primary.  
3. Write a 8-line change plan for adding `junos-https` to an existing policy (no apply unless told).  
4. Explain when you would **wait** vs **`rollback 1`**.  
5. List three changes that require instructor + console.

## Integrity

- No unsupervised failover tests.  
- No deleting rescue.  
- No “cleanup” `delete` of someone else’s candidate — `rollback 0` your own session.

## Further reading

| Topic | Source |
|-------|--------|
| Commit | Junos CLI user guide — committing a configuration |
| Cluster | TechLibrary *Chassis Cluster User Guide for SRX* (model + Junos match) |
| EX VC | EX4200 Virtual Chassis hardware/software guides |

## Next

**Network troubleshooting** — layered method and Junos evidence packs.
