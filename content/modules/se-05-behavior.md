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

### ETAS daily punch states

```text
[*] → NotStarted
NotStarted → CheckedIn   : check_in
CheckedIn  → CheckedOut  : check_out [declared ≥ check-in]
CheckedOut → CheckedIn   : check_in (split shift)
CheckedIn  → CheckedIn   : reject double check-in
```

Ask for every state: *What events are legal?*

### Leave request states

`Pending → Approved | Rejected`  
Pending **reserves** leave balance (policy choice — document it).

## Sequence diagrams

Show actors and components exchanging messages over time.

Good for:

- Login / quick check-in  
- Leave approve → summary sync  
- Export with TEMPO import  

**Keep them readable:** 5–12 messages, not the whole codebase.

## Consistency rules

1. Every message in a sequence should be allowed by some requirement or interface.  
2. Every critical FR should appear in at least one behavior view.  
3. Illegal transitions should be explicit (reject paths).  

## Assignment A3

Deliver one state chart + one sequence. ETAS punch/leave is allowed as the subject if you annotate which FRs they support.

## Offline drill

Model states for a library book: Available → Borrowed → Overdue → Available. List illegal events.

## Next

**Interfaces & ICDs** — talking to systems outside the box.
