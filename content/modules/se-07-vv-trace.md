# Verification, Validation & Traceability

## Learning outcomes

- Distinguish **verification** and **validation**  
- Build a small **RTM**  
- Choose a verification method per requirement  

## Verify vs validate

### Table 1 — Verification vs validation

| | Verification | Validation |
|-|--------------|------------|
| **Question** | Did we build it **right**? | Did we build the **right thing**? |
| **Against** | Requirements & design | Operational need / stakeholders |
| **Example** | Unit test rejects double check-in | Manager dry-run of quarterly export matches contract expectations |

Both are required. Perfect unit tests on the wrong product still fail validation.

**Verification is against the requirement text** (the shall), not against a private reading of a test script. Acceptance criteria and tests are **how** you check the FR; they do not rewrite contractual meaning. If a test and an FR disagree, fix the baseline under change control — do not treat the AC as the “real” requirement.

```mermaid
graph LR
    R[Requirement] --> D[Design element]
    D --> V["Verification (inspection, analysis, demo, test)"]
    R --> VLD["Validation (ops demo, stakeholder walkthrough)"]
```

*Alt text: Requirement links to design then verification; requirement also links to validation against operational need.*

### Verification methods (classic)

- **Inspection** — review documents, diagrams, and code artifacts  
- **Analysis** — models, calculations, or static analysis  
- **Demo** — show the system running in a realistic environment  
- **Test** — controlled inputs and expected outputs (unit, integration, system)  

*Pick the cheapest method that still provides the needed confidence level.*

## Traceability matrix (minimum columns)

| Req ID | Description | Design element | Verification method | Status* |
|--------|-------------|----------------|---------------------|---------|
| FR-CI-02 | No double check-in | `time_state.can_check_in` | Test | Planned |
| FR-BEOD-01 | Apply BEOD credit logic | `time_calc.update_daily_summary` | Test (unit) | Planned |
| NFR-SEC-01 | Store PINs as one-way hashes | `auth.encrypt_pin` | Inspection (code review) | Planned |

\*Status values: **Planned**, **In progress**, **Completed**, **Failed**. Update throughout the project.

### Rules of thumb

- Every FR has ≥ 1 verification method  
- Critical safety/money FRs need stronger evidence  
- Every FR should still walk the chain: vision ← **derives_from** need ← **traces_to** use case ← **allocated_to** FR ← **allocated_to** design  
- **Orphan design** (nothing **allocated_to** it from an FR) → may indicate gold plating  
- **Orphan FR** (FR with no design **allocated_to**) → likely not implemented; create a design or remove the requirement  

## Validation activities (examples)

- **Stakeholder walkthrough** of the Excel package — checks operational expectations (validation)  
- **Timed usability test** of quick check-in — confirms speed for real use  
- **Ops SME review** of mission-card language — terminology aligns with mission planning  

## Assignment A4

Produce a **traceability matrix (RTM)** that includes **all functional requirements** from Assignment A2 (IDs, design elements, verification method, and status).

Also submit a **short V&V plan** (~½ page) that outlines verification methods per requirement and at least one validation activity for the overall system.

See **Assignments** for weight and rubric.

## Selection signal

Candidates who **cannot** say how they would prove a requirement rarely pass selection. Practice saying: “We would test it by…”

> **Reminder:** If any text in the RTM or V&V plan is generated with an AI tool, add an in-text citation (e.g., *Generated with ChatGPT, 2026*). The underlying logic must be yours.

## Next

**Case Study — SDC Time Tracker (ETAS)** — walk the living system end-to-end, then move into **military ops** modules that map SE artifacts to operational concepts.
