# Addressing

> **When:** Week 2 · Tuesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [net-fa02-addressing — Readable address plan](/assignments/net-fa02-addressing) (~2 hours), due **Week 2 Wednesday morning**.

## Learning outcomes

After this afternoon you can:

- Read an IPv4 address, mask, and default gateway
- Explain DHCP and DNS in operational terms
- Say what a subnet is *for*
- Write a tiny address plan a peer can implement

## Why this afternoon exists

Most intern outages are addressing: wrong gateway, overlapping subnets, DNS that lies. You will not design OSPF this week. You will write a plan someone else can type.

## Teach

**IPv4** `10.10.20.15/24` means host `.15` on network `10.10.20.0`, 256 addresses, typical gateway `10.10.20.1`.

| Piece | Job |
|-------|-----|
| Address | Who I am |
| Mask / prefix | Who is “local” |
| Default gateway | Who I send to when it is not local |
| DHCP | Hands out address + gateway + DNS |
| DNS | Names → addresses |

A **subnet** exists to bound a broadcast domain, apply policy, and make plans readable — not to look clever.

**Write plans as tables**, not paragraphs:

| VLAN | Subnet | Gateway | Use |
|------|--------|---------|-----|
| 10 | 10.10.10.0/24 | .1 | Users |
| 20 | 10.10.20.0/24 | .1 | Servers |

CISS labs reuse teaching blocks (management `10.255.0.0/24`, site users, site servers). Instructor may remap — **write the live values in your notebook**.

## In-class exercise (30–40 min)

Fill a three-row plan (users, servers, management) for a fictional Masdar lab closet. Pick gateways. List three hosts with names and IPs. Peer tries to find an overlap or a missing gateway.

## Additional lesson

The long-form original is archived as **[net-01-foundations](/modules/net-01-foundations)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **net-fa02-addressing** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
