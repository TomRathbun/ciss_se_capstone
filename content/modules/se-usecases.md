# Use Cases from Needs

## Learning outcomes

- Derive **use cases** from needs (and ultimately from vision)  
- Write a lightweight use-case brief (actor, goal, main success, extensions)  
- Trace **use case → EARS requirements** without skipping layers  

## Place in the chain

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS (EARS)
              derives_from   traces_to    allocated_to
```

| Layer | Focus | Link |
|-------|--------|------|
| Need | Capability + benefit for a stakeholder | **derives_from** vision |
| Use case | A **goal-oriented interaction** that delivers part of that benefit | Need **traces_to** use case |
| Requirement | System rules that make the use case work in all relevant conditions | Use case **allocated_to** requirement |

One need → **several** use cases (`traces_to`). One use case → **several** requirements (`allocated_to`).

## What is a use case?

A use case describes **how an actor achieves a goal** using the system (and sometimes external systems).

Minimum fields in this course:

```text
UC-ID: UC-…
Name: <verb phrase, goal-oriented>
Primary actor: <who>
Goal: <what success looks like for the actor>
Precondition: <state before start>
Main success scenario: <numbered steps>
Extensions / alternate paths: <failures, rejects, exceptions>
Related need(s): <As … we need …>
Vision link: <optional short pointer>
```

### Naming tips

| Prefer | Avoid |
|--------|--------|
| Export quarterly FOSC package | Click export button |
| Correlate dual-feed tracks | Run neural net |
| Request multi-day vacation | Fill form |

## Derive use cases from a need

**Need example:**

```text
As UAE AFAD Mission Operators,
we need AI tools that combine smart learning with proven rules for better tracking,
identification, threat prediction, and engagement calculations,
so that we can handle dense threat environments and asymmetric threats.
```

**Candidate use cases (examples):**

| UC-ID | Name | Goal |
|-------|------|------|
| UC-TRK-01 | Maintain tracks in clutter | Operator sees stable tracks despite noisy radar |
| UC-ID-01 | Confirm or override track identity | Operator accepts AI ID or corrects it |
| UC-THR-01 | Review threat prediction cues | Operator sees ranked threat cues with rationale hooks |
| UC-ENG-01 | Review engagement calculation aid | Operator gets engagement support with human approval gate |

Each UC must still respect vision principles (e.g. human-in-the-loop on high-stakes act).

**ETAS need → use cases:**

| Need fragment | Use cases |
|---------------|-----------|
| Employees check in fast | UC-CI-01 Check in for today; UC-CO-01 Check out |
| Program TEMPO-aware export | UC-EX-01 Export weekly package; UC-EX-02 Export quarterly package |
| Leave with balance | UC-LV-01 Request leave; UC-LV-02 Approve leave |

## Main success vs extensions

Extensions are where **IF/THEN** requirements are born.

**UC-CI-01 Check in for today** (sketch)

1. Employee selects identity and authenticates  
2. Employee declares check-in time / location as required  
3. System records check-in and shows confirmed status  

**Extensions:**

- 2a. Already checked in → system rejects and explains  
- 2b. Declared time offset beyond threshold → mark for manager approval  

Those extensions become EARS requirements in the next module.

## Traceability table (required habit)

Record the **link types**, not only the IDs:

| Vision (parent) | Need **derives_from** | Use case **traces_to** | Later FR **allocated_to** |
|-----------------|----------------------|------------------------|---------------------------|
| Hybrid human–AI SA | Operators need better tracking… | UC-TRK-01 | FR-TRK-… |
| Auditable FOSC export | Admins need TEMPO-aware package… | UC-EX-02 | FR-FOSC-…, FR-DISC-… |

Leave the FR column blank until the requirements module — but keep the rows and the relationship names.

## Workshop (20 min)

Take **one** needs statement from A1 or the AFAD example.

1. Write **3 use case names** with primary actor + goal  
2. Fully draft **one** use case (main success + ≥ 2 extensions)  
3. Mark which extensions will need IF/THEN requirements  

## What use cases are not

- Not UI wireframes (those are design)  
- Not EARS requirements (those are the next layer)  
- Not the vision paragraph  

> **Reminder:** If you generate any wording with an AI tool, add an in-text citation (e.g., *Generated with ChatGPT, 2026*). The underlying idea and structure must still be yours.

## Further reading

| Topic | Source |
|-------|--------|
| Use cases / scenarios in SE | [SEBoK search — use case / scenario](https://sebokwiki.org/wiki/Special:Search?search=use+case) |
| Classic use-case craft | Cockburn, *Writing Effective Use Cases* — search “Cockburn use case goal levels” for free primers |
| Operational / mission analysis | [SEBoK — Business or Mission Analysis](https://sebokwiki.org/wiki/Business_or_Mission_Analysis) |
| From scenarios to requirements | [SEBoK — System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition) |
| UML use-case diagram overview | [UML Use Case Diagrams (OMG / community primers)](https://www.uml-diagrams.org/use-case-diagrams.html) |

## Next

**Requirements & Acceptance Criteria** — write EARS shall-statements that make each use case succeed and fail safely, with Given/When/Then acceptance criteria.
