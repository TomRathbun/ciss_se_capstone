# Architecture views & allocation

> **When:** Week 6 · Monday afternoon · Masdar
> **Who:** All interns (SE is mandatory for the full program)
> **Tomorrow morning:** [se-da01-architecture — Architecture views pack](/assignments/se-da01-architecture) (~2 hours), due **Week 6 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Keep context, structure, and deployment as three views
- Allocate FRs to real elements
- Record one design decision

## Why this afternoon exists

PRSAS now has a problem statement. Allocation is how Software, Network, and Admin receive work.

## Teach

Context = boundary. Structure = pieces and responsibilities. Deployment = VMs/processes/networks.

FRs are **allocated_to** structure elements, not to 'the cloud.' A design decision records *what we chose, what we rejected, why*.

PRSAS structure you should expect to see: simulators, broker, daemon, DB, client, firewall/encryptor, identity/CA.

## In-class exercise (30–40 min)

On the board: three views of PRSAS. Allocate FR 'WHEN a Cat062-like message arrives the daemon shall persist a track' to an element.

## Additional lesson

The long-form original is archived as **[se-05-architecture](/modules/se-05-architecture)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **se-da01-architecture** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
