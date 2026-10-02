# Test before you guess

> **When:** Week 4 · Tuesday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [net-fa04-test-path — Evidence pack for a dead path](/assignments/net-fa04-test-path) (~2 hours), due **Week 4 Wednesday morning**.

## Learning outcomes

After this afternoon you can:

- Order tests: local → gateway → name → port → application
- Say what ping and traceroute actually prove
- Write an evidence pack a peer can reuse
- Treat change control as part of networking

## Why this afternoon exists

‘It doesn’t work’ is not a ticket. Guessing OSPF on a week-4 intern is how labs burn down. This afternoon is the method you will still use on Junos in week 12.

## Teach

**Test order (default):**

1. Is *my* interface up and addressed?
2. Can I reach the **gateway**?
3. Does the **name** resolve (if we used a name)?
4. Does the **port** answer (not just ICMP)?
5. Does the **application** complete?

**Ping** proves ICMP to an address, not that 61617 works. **Traceroute** shows hops that *answer traceroute*, not the full policy.

Evidence pack: command, timestamp, excerpt, what you conclude, what you will try next. One hypothesis at a time.

**Change control:** even in a lab, write what you will change, how you will know, and how you will undo. `commit confirmed` is a depth skill; the *habit* starts now.

Hold: Junos `show` cheatsheets, traceoptions, blast-radius clears.

## In-class exercise (30–40 min)

Symptom: ‘the web page never loads, ping to the server IP works.’ Write the ordered tests. Peer adds the test you skipped.

## Hold for later

Junos, OSPF, BGP, MPLS, IPsec — week 6+ for those who stay in Networking.

## Tomorrow morning

Do **net-fa04-test-path** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
