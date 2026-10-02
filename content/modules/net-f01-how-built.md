# How a network is built

> **When:** Week 1 · Tuesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [net-fa01-how-built — Path and device-roles sheet](/assignments/net-fa01-how-built) (~2 hours), due **Week 1 Wednesday morning**.

## Learning outcomes

After this afternoon you can:

- Describe LAN vs WAN in vendor-neutral language
- Say what a switch, router, and firewall each do
- Use OSI / TCP-IP enough to name which layer is failing
- Draw a path from a user to a service

## Why this afternoon exists

Software and sensors only matter if packets arrive, in order, on the allowed path. Interns who jump to Junos cannot tell a wrong mask from a dead DNS from a blocked port.

## Teach

A **network** is nodes exchanging messages under agreed addresses and rules.

| Word | Meaning |
|------|---------|
| Host | PC, server, VM — source or destination |
| Hop | A router or L3 firewall the packet is forwarded through |
| Path | Ordered hops from source to destination |
| LAN | One site / broadcast-domain family |
| WAN | Links **between** sites |

```text
PC → Switch → Gateway/firewall → WAN → Remote gateway → Server
```

| Role | Forwards on | Job |
|------|-------------|-----|
| Switch (L2) | MAC + VLAN | Many hosts in a LAN |
| Router (L3) | IP prefix | Next hop between subnets |
| Firewall | IP + port + policy | Allow/deny (often NAT too) |

**Layers you need this week:** L2 delivery, L3 hops, L4 ports, application names (DNS, HTTPS). If you cannot draw the path, you cannot debug it.

SE link: host, port, and path are interface / NFR fields. A path sketch is a cheap context diagram.

## In-class exercise (30–40 min)

Draw the path from a laptop on a user VLAN to a database VM on a server VLAN through a firewall. Label switch, router/firewall, WAN-or-not. Name one failure that is L2 vs L3 vs L4.

## Additional lesson

The long-form original is archived as **[net-01-general](/modules/net-01-general)**. Read it after class if you will keep this discipline.

## Hold for later

Junos commit model, OSPF, BGP, MPLS, IPsec. Depth after week 4.

## Tomorrow morning

Do **net-fa01-how-built** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
