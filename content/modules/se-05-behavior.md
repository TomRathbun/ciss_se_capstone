# Behavior — States & Sequences

## Learning outcomes

- Model a **state machine** with legal/illegal transitions  
- Draw a **sequence diagram** for a scenario  
- Align behavior models with requirements  

## Why behavior models?

Requirements say *what*. Behavior models show *when* and *in what order*. Bugs hide in illegal sequences (“checkout without check-in”).

## State machines

**State** = meaningful condition that lasts until an event.  
**Transition** = event + optional guard → new state.

### ETAS daily punch states (UML style)


```text
[*] --> NotStarted NotStarted --> CheckedIn : check_in CheckedIn --> CheckedOut : check_out [declared ≥ check_in] CheckedOut --> CheckedIn : check_in (split shift) CheckedIn --> CheckedIn : check_in [already_checked_in] // illegal, reject
```
>"Tip: Use a red dashed arrow or a guard [already_checked_in] to denote the illegal transition.

Ask for every state: *What events are legal?*

### Leave request states

`Pending --> Approved : approve Pending --> Rejected : reject`  

* When entering **Pending**, the system **reserves** the requested leave balance (policy choice – document the reservation rule).  


## Sequence diagrams

Show actors and components exchanging messages over time.

Good for:

- Login / quick check-in  
- Leave approve → summary sync  
- Export with TEMPO import  

### Sequence diagram tip
- Keep the diagram to **5–12 messages**.  
- Use `alt` blocks for alternative paths (e.g., success vs. failure).  
- Limit the diagram to **one primary scenario**; add separate diagrams for other use cases if needed.


## Consistency rules

1. Every message in a sequence should be allowed by some requirement or interface.  
2. Every **critical FR** *and* at least one **non‑functional FR** should appear in a behavior view.
3. Illegal transitions should be explicit (reject paths).  

## Assignment A3

Deliver **one state chart** and **one sequence diagram** (any valid tool – PlantUML, draw.io, Visio).  
- **Annotate** each diagram with the supporting requirement ID(s) (e.g., `FR‑CI‑02`).  
- Use a **trace column** in the caption or a legend on the diagram.


## Offline drill (10 min)

Model the states for a library book:
`Available → Borrowed → Overdue → Available`

1. List **legal transitions** (e.g., *borrow*, *return*, *renew*).  
2. List **illegal events** (e.g., *return* when already *Available*).  

**Peer review** – swap diagrams with a neighbor and verify that each illegal event is explicitly shown as a reject path.

> **Reminder:** If you generate any diagram labels or wording with an AI tool, add an in‑text citation (e.g., *Generated with ChatGPT, 2026*). The underlying logic must be yours.

## Next

**Interfaces & ICDs** – you will define how your system talks to external services (message formats, protocol contracts, versioning).

