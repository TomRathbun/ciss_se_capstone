# SRX firewalls — zones, policy, NAT

> **When:** Week 8 · Tuesday afternoon · Masdar
> **Who:** Networking elective + anyone still attending
> **Tomorrow morning:** [net-da03-srx — Zone and policy sketch](/assignments/net-da03-srx) (~2 hours), due **Week 8 Wednesday morning**.

## Learning outcomes

After this afternoon you can:

- Apply SRX firewalls at intern level on older Junos
- Leave evidence, not folklore
- Keep PRSAS path in view

## Why this afternoon exists

Foundation taught packets. This afternoon is the vendor craft on the gear this program still runs.

## Teach

Zones, host-inbound-traffic, first-match policy, source NAT, `show security flow session`. Least privilege.

Tie every example back to the three-site PRSAS fabric when you can. If the bench cannot do it, worksheet + instructor captures.

## In-class exercise (30–40 min)

Three zones (trust, untrust, vpn). One allow-list for 61617. What you `show` to prove it.

## Additional lesson

The long-form original is archived as **[net-04-srx-firewall](/modules/net-04-srx-firewall)**. Read it after class if you will keep this discipline.

## Hold for later

Do not paste production configs. Redact PSKs.

## Tomorrow morning

Do **net-da03-srx** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
