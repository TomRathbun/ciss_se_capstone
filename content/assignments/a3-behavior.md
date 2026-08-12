# A3 — State Chart + Sequence (your feature)

**Weight:** 10% · **Due:** Week 4 Thursday · **Module:** se-06 Behavior

## Prompt

Model dynamic behavior for **one** feature area of your system (examples: daily punch, leave approval, alert ack for a future SA app, or a small subsystem from your A2 pack).

## Deliverables

1. **State diagram** using full labeling where needed:  
   `trigger [guard] / activity`  
   Include initial state, at least **one reject/illegal path**, and FR IDs on transitions or in a legend.
2. **Sequence diagram** — happy path **and** one failure/reject path (`alt`).
3. **Mapping table:** each FR used → state-chart element (transition, guard, entry/exit) and sequence messages.

## Quality bar

| Expect | Avoid |
|--------|--------|
| Guards written as booleans | Vague arrows with no events |
| Reject paths visible | Silent illegal events when FR requires feedback |
| Sequence agrees with the chart | Sequence that the chart forbids |
| Same FR IDs as A2 when continuing that system | Untraceable “magic” transitions |

## Rubric

| Dimension | Max | Description |
|-----------|-----|-------------|
| correctness | 15 | Legal/illegal transitions and sequence messages make sense |
| consistency | 10 | Aligns with stated requirements; chart ↔ sequence agree |
| communication | 5 | Labels readable; legend / mapping table usable |

## Notes

- Tools: Mermaid, PlantUML, draw.io, Visio, or SysML export.  
- Hierarchical states optional here (required in **A3c**).  
- Cite AI if used for wording; logic must be yours.
