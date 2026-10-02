# Junos CLI and the Commit Model

## Learning outcomes

After this module you can:

- Navigate **operational** vs **configuration** mode on Junos  
- Explain **RE vs PFE**, and **candidate vs active** configuration  
- Use **`set` / `delete` / `edit` / `show \| display set`**  
- Run **`commit check`**, **`commit confirmed`**, **`rollback`**, and **rescue**  
- Decode **interface names** on older EX and SRX (`ge-0/0/0`, `fe-`, `reth`, `st0`, `me0` / `fxp0`)  

## Why Junos feels different from Cisco

Many interns arrive with IOS muscle memory (`conf t`, `wr mem`, one running-config). Junos is a **database with a commit**.

| Idea | Junos | Typical IOS habit |
|------|-------|-------------------|
| Edit buffer | **Candidate** (not live until commit) | Often live as you type |
| Activate | `commit` | implicit / `wr` |
| Undo | `rollback n` | hope you have a backup |
| Syntax | Hierarchical stanzas | linear commands |
| Show as set | `show \| display set` | `show run` |

This is a **safety feature**. Treat it that way: you can build a change, review `show | compare`, then commit.

SE link: candidate → commit is a tiny **change-control** loop. `commit comment` is evidence.

## Two planes

```text
Routing Engine (RE)          Packet Forwarding Engine (PFE)
  Junos CLI / daemons          ASICs / flow (especially SRX)
  candidate + active config    forwarding tables
  SSH, SNMP, commit            actual packets
```

If the RE is busy or the disk is full, **commits fail** and control-plane SSH gets ugly. On old branch boxes this happens more than you expect (logs, traceoptions).

## Modes

```text
user@srx-a-fw-01>          operational mode   (show, ping, request)
user@srx-a-fw-01#          configuration mode (set, delete, commit)
```

```text
cli                         # if you landed in a root unix shell
configure                   # or: configure exclusive
exit                        # leave config
quit
```

**`configure exclusive`** — you hold the candidate; others wait. Prefer this on a shared lab box.

**`configure private`** — your own candidate; merge on commit. Know it exists.

## Hierarchy and the four verbs

```text
edit interfaces ge-0/0/1 unit 0 family inet
set address 10.10.10.1/24
up
up
show
top
show | compare
show | display set
```

| Verb | Meaning |
|------|---------|
| `edit` | Move into a stanza |
| `set` | Add / change a leaf |
| `delete` | Remove a leaf or subtree (**dangerous** if too high) |
| `deactivate` / `activate` | Comment out without deleting |
| `rename` / `replace pattern` | Refactor |
| `insert` | Reorder (policies, terms) |

**Always review before commit:**

```text
show | compare
show | display set | match ge-0/0/1
```

## Commit toolkit (memorize)

```text
commit check              # syntax + commit scripts; not a full design review
commit comment "NET-lab VLAN10 SVI"
commit confirmed 5        # auto-rollback in 5 minutes unless you commit again
commit                    # make it stay
commit and-quit
```

If you `commit confirmed 5` and then lose SSH because you broke management — **wait**. The box rolls back. That is the point.

```text
rollback 1                # candidate becomes previous commit
rollback 0                # discard candidate; back to active
show system commit
show system rollback 1 compare
```

Junos keeps a **rollback history** (commonly 50). `rollback 1` is “undo last commit,” not “undo last set.”

**Rescue configuration** (save a known-good once per lab day):

```text
request system configuration rescue save
rollback rescue
commit
```

## Load and annotate

```text
load set terminal         # paste set lines, then Ctrl-D
load merge terminal       # paste hierarchical text
load override             # replaces entire candidate — lab only, never casually
```

Do **not** `load override` on a shared device unless the instructor says so.

## Interface naming on older boxes

`type-fpc/pic/port` — then **unit** (subinterface). IPv4 lives under `unit … family inet`.

| Name | Meaning |
|------|---------|
| `ge-0/0/0` | Gigabit Ethernet |
| `fe-0/0/0` | Fast Ethernet (SRX100/210-class) |
| `xe-0/0/0` | 10 Gigabit |
| `lo0` | Loopback (often `.0` with `/32`) |
| `st0` | Secure tunnel (IPsec) |
| `reth0` | Redundant Ethernet (chassis cluster) |
| `vlan.10` or `irb.10` | SVI — **older EX** often `vlan`; newer ELS uses `irb` |
| `fxp0` | Out-of-band RE management (many SRX/MX) |
| `me0` | Management on many **EX** |
| `vme` | Virtual-management on EX Virtual Chassis |

**Unit 0** is not optional in thinking: `ge-0/0/1` is the port; `ge-0/0/1.0` is the logical interface you put in a zone or VLAN.

### Chassis cluster port numbers

On clustered SRX, node 1 ports are **offset** (model-specific): SRX240 often `ge-0/0/x` (node0) and `ge-5/0/x` (node1). Always `show interfaces terse` — do not memorize offsets from a blog for the wrong model.

## Daily operational show commands

```text
show version
show chassis hardware
show interfaces terse
show interfaces ge-0/0/0 extensive | match "Physical|error|rate|Duplex"
show configuration
show configuration | display set
show system users
show system storage
show log messages | last 30
```

Ping / traceroute from the box:

```text
ping 10.10.10.50 rapid count 20
ping 10.10.10.50 source 10.10.10.1
traceroute 10.20.10.1
```

`source` matters: the box may have many addresses; pick the one the peer expects.

## Minimal first config (shape only)

```text
set system host-name srx-a-fw-01
set system services ssh
set system services ping
set interfaces ge-0/0/1 unit 0 family inet address 10.10.10.1/24
set interfaces lo0 unit 0 family inet address 10.255.255.11/32
```

On **SRX**, an interface also needs a **security zone** and **host-inbound-traffic** or ping/SSH die even when the IP is correct. That is the next firewall module — do not “fix” it by turning off security.

## Older Junos notes

| Topic | 12.x / 15.1X49 lab boxes |
|-------|---------------------------|
| Space | Small flash — avoid heavy `traceoptions`; `request system storage cleanup` only when taught |
| User | `class super-user` for lab admin; do not create extra root-equivalent accounts |
| ScreenOS | SSG uses `get system` / `set interface` — **different OS** |
| ELS | Newer EX: `interface-mode access` instead of `port-mode access` |

`show version` first. Write the version in every evidence pack.

## Common intern mistakes

| Mistake | Consequence |
|---------|-------------|
| Typing IOS `wr` / `conf t` | Syntax errors; nothing saved |
| `commit` without `show \| compare` | Silent extra deletes |
| Forgetting `unit 0` | Interface has no family |
| `delete interfaces` | You just removed every port |
| Leaving a failed candidate | Next person inherits your mess — `rollback 0` |
| `commit` on management path without `confirmed` | Lock yourself out |

## Drill (40 min)

On the assigned EX or SRX (or instructor terminal server):

1. Record `show version` (model + Junos).  
2. `show interfaces terse` — identify mgmt, uplinks, down ports.  
3. Enter `configure exclusive`, `show | compare` (should be empty), exit.  
4. In a **lab sandbox prefix the instructor names**, add a description to one unused interface; `show | compare`; `commit check`; `commit comment "NET-02 drill"` **or** discard with `rollback 0`.  
5. `show system commit` — paste the last two comments (redact users if asked).

Do not change IP addresses on shared uplinks.

## Integrity

- Exclusive configure on shared boxes.  
- No `load override` of a classmate’s rescue.  
- No passwords in `display set` pasted to public Git — redact `secret` / `$9$` hashes if the instructor wants hashes out of tickets too.

## Further reading

| Topic | Source |
|-------|--------|
| CLI | TechLibrary: *Junos OS CLI User Guide* for your version |
| Commit | `help commit` / Day One: Exploring the Junos CLI |
| Interfaces | `help topic interfaces` on the box |

## Next

**EX switching** — VLANs, trunks, RSTP, and EX4200 Virtual Chassis.
