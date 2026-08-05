# A2 — Requirements Pack

**Weight:** 25% · **Due:** Week 4 Thursday (draft feedback Week 3)

## Prompt

Write a requirements baseline for a system scope you define (ETAS subset or other — state the scope).

**Functional requirements must use EARS grammar** (see module *Requirements & Acceptance Criteria*).

## Deliverables

1. Scope statement (½ page max)  
2. **8–12 functional requirements** with IDs (`FR-…`) in **EARS form** (`WHEN` / `WHILE` / `IF…THEN` / `WHERE` / ubiquitous)  
3. For each FR, note the **EARS pattern** used (e.g. `[WHEN]`, `[IF/THEN]`)  
4. **≥ 3 NFRs** with IDs (`NFR-…`) and measurable criteria  
5. **≥ 5 acceptance criteria** in Given/When/Then, each tracing to an FR ID  
6. List of explicitly **out-of-scope** items  
7. **Coverage check:** at least one FR of each: event-driven (WHEN), state-driven (WHILE), unwanted (IF/THEN)  

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
