# Behavior — states & sequences

> **When:** Week 7 · Monday afternoon · Masdar
> **Who:** All interns (SE is mandatory for the full program)
> **Tomorrow morning:** [se-da02-behavior — State + sequence](/assignments/se-da02-behavior) (~2 hours), due **Week 7 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Separate state from status
- Write trigger/guard/activity
- Draw one sequence that matches the state machine

## Why this afternoon exists

Track lifecycle (init / live / coast / drop / conflict) is a state machine whether anyone draws it or not.

## Teach

**State** is a mode with legal transitions. **Status** is a field.

Transitions: trigger [guard] / activity.

PRSAS track lifecycle (teaching): no-track → live (on first plot) → coast (missed updates) → drop; conflict when two feeds disagree on Mode 3/A vs kinematics.

Sequence: plot in → daemon → DB write → output topic → client.

## In-class exercise (30–40 min)

Sketch hybrid state for one track. Peer names an illegal transition.

## Additional lesson

The long-form original is archived as **[se-06-behavior](/modules/se-06-behavior)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **se-da02-behavior** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
