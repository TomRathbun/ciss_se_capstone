# SW-A07 — JavaFX Mini Console

**Weight:** 10% · **Due:** After sw-07-javafx-gui · **Module:** sw-07-javafx-gui

## Prompt

Build a **thin desktop UI** over a simple service idea (lab tool, not a marketing site).

## Feature choices (pick one)

- **Message viewer:** list last N events (can be mock list if broker unavailable)
- **Inventory desk:** show items + button to adjust qty (can call JDBC repo or mock)
- **Status board:** connection state + last heartbeat time

## Deliverables

1. **JavaFX app** with Stage/Scene, layout, ≥ 2 controls, one table or list.
2. **Event handler** that updates the UI from a clear model/service method (business logic not only inside `onAction`).
3. **Threading note:** what you keep on the FX Application Thread; what you would move off-thread if a call were slow.
4. **Use-case link:** 3–5 bullets mapping screen actions to user goals (and optional `FR-…` ids).
5. Screenshot of the running UI + run instructions.

## Quality bar

- UI stays responsive in design (even if lab uses mock data).
- Labels and validation do not invent hidden business rules.
- Structure is maintainable (package or class split is fine).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| ui_structure | 15 | Working JavaFX UI with real controls |
| se_alignment | 10 | Thin UI; use-case / FR thinking |
| communication | 5 | Screenshot + run notes |
