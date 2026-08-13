# A3 — State Chart + Sequence (your feature)

**Weight:** 10% · **Due:** Week 6 Thursday · **Module:** se-06 Behavior  
**Cadence:** Assigned Monday after the behavior lecture. Work Monday–Wednesday. Due Thursday review / grade.

Monday workshop (not separately graded): printer-queue pack (`a3b-ears-state-map.md`) and radio hierarchy (`a3c-hierarchical-state.md`) live in the module. Do them in class if time; they train the same skills A3 grades.

## Prompt

Model dynamic behavior for **one** feature area of **your** A1–A2 system (examples: daily punch, leave approval, alert ack).

Distinguish **state** (mode that changes what is legal) from **status** (label / attribute). Only modes go on the chart.

## Deliverables

1. **State diagram** using full labeling where needed:  
   `trigger [guard] / activity`  
   Include initial state, at least **one reject/illegal path**, and FR IDs on transitions or in a legend.
2. **Sequence diagram** — happy path **and** one failure/reject path (`alt`).
3. **Mapping table:** each FR used → state-chart element (transition, guard, entry/exit) and sequence messages.
4. **State vs status note (≤ 6 lines):** one word in your domain that people call “status” and whether you modeled it as a state — and why.

## Quality bar

| Expect | Avoid |
|--------|--------|
| Guards written as booleans | Vague arrows with no events |
| Reject paths visible | Silent illegal events when FR requires feedback |
| Sequence agrees with the chart | Sequence that the chart forbids |
| Same FR IDs as A2 when continuing that system | Untraceable “magic” transitions |
| Only behavioral modes on the chart | A node for every UI badge |

## Rubric

| Dimension | Max | Description |
|-----------|-----|-------------|
| correctness | 15 | Legal/illegal transitions and sequence messages make sense |
| consistency | 10 | Aligns with stated requirements; chart ↔ sequence agree |
| communication | 5 | Labels readable; legend / mapping table usable |

## Notes

- Tools: Mermaid, PlantUML, draw.io, Visio, or SysML export.  
- Hierarchical states optional on A3. Practice them in the Monday **A3c** workshop.  
- Cite AI if used for wording; logic must be yours.
