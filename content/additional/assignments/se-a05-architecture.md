# SE-A05 — Architecture Views & Allocation

**Weight:** 8% · **Due:** Week 5 Thursday · **Module:** se-05 Architecture Views  
**Cadence:** Assigned Monday of the architecture week. Due Thursday (same week as **A2** final — keep views coarse).

## Prompt

Draw **multiple views** of the same system (prefer the system from A1–A2). One mega-diagram is a fail.

Assume **VM-based** lab deployment (not Docker) unless you explicitly justify otherwise.

## Deliverables

1. **Context diagram** — system vs world; labeled flows. ≥ 3 actors/externals.
2. **Container / layer *or* component view** — major pieces and responsibilities (table + diagram).
3. **Deployment view** — at least **two VMs** (e.g. app + DB). Note what ops would restart (`systemctl` / guest).
4. **Allocation table** — at least **5** of your A2 FRs (or declared teaching FRs if A2 is still in draft):

   | FR ID | **allocated_to** (component / service) | Parent UC |
   |-------|----------------------------------------|-----------|
   | | | |

5. **One design decision** using the module template (decision, status, rationale, alternatives, consequences).
6. **Anti-diagram note (≤ 6 lines):** what you *refused* to put on one of the views (UI widgets, SQL columns, sequence arrows, ICD fields) and which later module owns that.

## Quality bar

- Views do not mix levels (no VM names on the context diagram; no REST paths on the deployment boxes).
- Every allocated FR has a home; if you cannot place an FR, say whether the architecture or the FR is incomplete.
- Decision rationale is yours (cite AI if used for wording).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| views | 15 | Distinct context + structure + deployment |
| allocation | 10 | FRs mapped to real elements; decision recorded |
| communication | 5 | Peer can brief the structure in 3 minutes |
