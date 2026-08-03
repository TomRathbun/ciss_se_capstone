# Requirements & Acceptance Criteria

## Learning outcomes

- Write **shall** requirements with IDs
- Separate **functional** and **non-functional** requirements
- Write **Given / When / Then** acceptance criteria
- Spot bad requirements

## Shall language

> The system **shall** reject check-in when the employee is already checked in for that work date.

| Prefer | Avoid (for mandatory behavior) |
|--------|--------------------------------|
| shall | should, might, try to |
| measurable | “user friendly”, “fast enough” without numbers |
| one idea per shall | paragraphs of mixed rules |

## IDs

Use stable IDs for traceability:

- `FR-CI-02` — functional, check-in family  
- `NFR-SEC-01` — non-functional, security  

IDs never change meaning mid-course without a baseline note.

## Functional vs non-functional

| Type | Focus | Example |
|------|--------|---------|
| FR | Behavior / functions | Export quarterly FOSC package |
| NFR | Qualities | PINs stored only as hashes |

## Acceptance criteria

Make requirements **testable**:

```text
AC-CI-02 · FR-CI-02
Given employee E is checked in today
When E submits another check-in for today
Then the system rejects with a clear error and stores no new check-in entry
```

### Quality checklist for ACs

- [ ] Observable result (not “user is happy”)
- [ ] Named preconditions
- [ ] Covers at least one failure path for critical FRs
- [ ] Independent tester could run it without asking you

## Bad → better

| Bad | Better |
|-----|--------|
| System should handle leave | The system shall allow multi-day vacation requests with pending status |
| UI must be modern | Primary check-in shall complete in ≤ 3 interactions from the login list |
| BEOD works correctly | BEOD +1h shall apply only if claimed/approved and raw hours ≥ 6.0 |

## Case study pointer

Open the ETAS **Systems Engineering** page and read section 6–7 (requirements + ACs). Do not copy blindly — understand *why* each FR exists.

## Offline practice (45 min)

Write 5 FRs + 2 NFRs + 3 ACs for a “meeting room booking” system. Self-score with the checklist above.

## Assignment A2

**Requirements Pack** — major graded item (weight 25%). See Assignments.

## Next

**Architecture views** — where requirements live in the design.
