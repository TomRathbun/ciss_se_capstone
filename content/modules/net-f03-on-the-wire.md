# Conversations on the wire

> **When:** Week 3 · Tuesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [net-fa03-on-the-wire — Ports and allowed-path table](/assignments/net-fa03-on-the-wire) (~2 hours), due **Week 3 Wednesday morning**.

## Learning outcomes

After this afternoon you can:

- Choose TCP vs UDP for a given conversation
- Name common ports (SSH, HTTPS, DNS, AMQP)
- Explain VLAN and NAT as ideas, not configs
- State the allowed-path mindset

## Why this afternoon exists

Firewalls and brokers fail in port language. If you cannot say ‘ActiveMQ TLS is 61617 on the allowed path,’ you cannot help Software or Admin.

## Teach

**TCP** is a conversation with setup and acknowledgment. **UDP** is a datagram — DNS questions often live here; streaming and some tunnels too.

| Service | Typical port | Transport |
|---------|--------------|-----------|
| SSH | 22 | TCP |
| HTTPS | 443 | TCP |
| DNS | 53 | UDP (and TCP) |
| PostgreSQL | 5432 | TCP |
| ActiveMQ OpenWire TLS (PRSAS later) | **61617** | TCP |

**VLAN:** a LAN sliced into separate L2 domains. **NAT:** rewriting addresses so private hosts can talk out (or, badly, hiding too much).

**Allowed-path mindset:** the path that is *permitted* is the one we document. Everything else is deny. “It works if we disable the firewall” is not a design.

Hold Junos `set security policies` until depth. Today is the *idea*.

## In-class exercise (30–40 min)

For SSH, DNS, HTTPS, and a message broker: transport, port, and whether a user VLAN should reach it. Draw one allowed path and one path you would deny.

## Tomorrow morning

Do **net-fa03-on-the-wire** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
