# A2 — Requirements Pack (EARS + acceptance)

**Weight:** 16% · **Due:** Week 5 Thursday (draft coaching Week 4 Thursday) · **Module:** se-04 Requirements  
**Cadence:** Assigned Monday of the requirements week. Bring a **draft** (at least 4 FRs + 2 ACs) to Thursday coaching. Finish Monday–Wednesday of the **architecture** week. Final due that Thursday.

This is the heaviest SE artifact. You get **two** Thursday touchpoints, not three evenings.

## Prompt

Write a **system-level** requirements baseline for the system you started in A1 / SE-A03 (ETAS subset or other — state the scope).

**Functional requirements must use EARS grammar** (see module *Requirements & Acceptance Criteria*).

## Deliverables

1. Scope statement (½ page max)  
2. **8–12 functional requirements** with IDs (`FR-…`) in **EARS form** (`WHEN` / `WHILE` / `IF…THEN` / `WHERE` / ubiquitous)  
3. For each FR, note the **EARS pattern** and the parent **UC-ID** (`allocated_to`)  
4. **≥ 3 NFRs** with IDs (`NFR-…`) and measurable criteria  
5. **≥ 5 acceptance criteria** in Given/When/Then, each tracing to an FR ID  
6. **Definition library** — terms a tester would otherwise guess  
7. **TBD/TBR register** if any placeholder number appears  
8. List of explicitly **out-of-scope** items  
9. **Coverage check:** at least one FR of each: event-driven (WHEN), state-driven (WHILE), unwanted (IF/THEN)  

## Quality bar

- A smart peer can identify the EARS pattern without guessing.  
- Each **FR stands alone** — thresholds, rejects, and triggers are in the shall, not only in the AC.  
- A smart peer can test each AC without asking you questions.  
- Each AC is **faithful** to its FR: it proves the shall; it does not add new rules or paper over vague wording.  
- Rejects and error paths are first-class FRs (IF/THEN), not only happy-path WHEN.  

**Common fail:** Vague FR + detailed AC that “really means” the requirement. On real contracts the customer can demand *their* reading of the FR. Fix the FR; do not hide meaning in ACs.

## Rubric

testability · shall_quality · coverage · communication  

*shall_quality includes correct EARS structure, use of shall, and FRs that do not depend on ACs to be understandable.*  
*testability includes ACs that align with FRs (cover + no-extra).*
