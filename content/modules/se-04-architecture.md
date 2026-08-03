# Architecture Views

## Learning outcomes

- Describe a system with **layers / views**
- Allocate requirements to design elements
- Capture a **design decision** with rationale

## Architecture is not decoration

Architecture answers:

- What are the major pieces?
- What are their responsibilities?
- How do they interact?
- What quality attributes does this structure support?

## Useful views for software-heavy systems

1. **Context** — system vs world (from prior module)  
2. **Containers / layers** — UI, application services, data  
3. **Component** — modules inside a layer  
4. **Runtime** — who calls whom for a key scenario  

ETAS example layers:

| Layer | Responsibility | Example module |
|-------|----------------|----------------|
| Presentation | Screens, forms | Jinja templates, routes |
| Application services | Business rules | `time_state`, `time_calc`, `fosc_export` |
| Domain | Entities | `Employee`, `TimeEntry`, `DailySummary` |
| Persistence | Storage | SQLite |

## Allocation (simple RTM column)

| Requirement | Design element |
|-------------|----------------|
| FR-CI-02 | `time_state.can_check_in` |
| FR-BEOD-01 | `time_calc.update_daily_summary` |
| FR-DISC-01 | `fosc_export.write_discrepancy_sheet` |

If you cannot allocate an FR, either the architecture is incomplete or the FR is not real.

## Design decision template

```text
Decision: Keep punch legality in a single service (time_state)
Rationale: Prevent UI and API from diverging on rules
Alternatives considered: Checks only in route handlers
Consequences: Routes stay thin; tests target one module
```

## Workshop

Pick one FR from the case study. Name:

1. The component that enforces it  
2. The data it reads/writes  
3. One risk if that component is wrong  

## Next

**Behavior** — states and sequences for time-dependent rules.
