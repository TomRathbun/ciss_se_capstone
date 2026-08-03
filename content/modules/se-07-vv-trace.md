# Verification, Validation & Traceability

## Learning outcomes

- Distinguish **verification** and **validation**  
- Build a small **RTM**  
- Choose a verification method per requirement  

## Verify vs validate

| | Verification | Validation |
|---|--------------|------------|
| Question | Did we build it **right**? | Did we build the **right thing**? |
| Against | Requirements & design | Operational need / stakeholders |
| Example | Unit test rejects double check-in | Manager dry-run of quarterly export matches contract expectations |

Both are required. Perfect unit tests on the wrong product still fail validation.

## Verification methods (classic)

- **Inspection** — review documents/diagrams  
- **Analysis** — models, calculations  
- **Demo** — show the system running  
- **Test** — controlled inputs/outputs  

Pick the cheapest method that still gives confidence.

## Traceability matrix (minimum columns)

| Req ID | Description | Design element | Verification method | Status |
|--------|-------------|----------------|---------------------|--------|
| FR-CI-02 | No double check-in | time_state.can_check_in | Test | Planned |

Rules of thumb:

- Every FR has ≥ 1 verification method  
- Critical safety/money FRs need stronger evidence  
- Orphan design (no FR) = suspect gold plating  
- Orphan FR (no design) = not implemented  

## Validation activities (examples)

- Stakeholder walkthrough of Excel package  
- Timed usability of quick check-in  
- Ops SME review of mission card language  

## Assignment A4

Produce an RTM for your A2 requirements + a short V&V plan (half page).

## Selection signal

Candidates who **cannot** say how they would prove a requirement rarely pass selection. Practice saying: “We would test it by…”

## Next

**Case study walkthrough** of the living ETAS system — then military ops modules.
