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
Related need(s): As <stakeholder>, we need …, so that …
Vision link: <optional short pointer>
```

*Related need(s) use the same course grammar as module 02: **As** / **we need** / **so that**, with the stakeholder **bold and underlined**.*

### Naming tips

| Prefer | Avoid |
|--------|--------|
| Export quarterly FOSC package | Click export button |
| Correlate dual-feed tracks | Run neural net |
| Request multi-day vacation | Fill form |

## Derive use cases from a need

**Need example** (grammar anchors + stakeholder style from se-02):

> **As** <u>**UAE AFAD Mission Operators**</u>,  
> **we need** AI tools that combine smart learning with proven rules for better tracking, identification, threat prediction, and engagement calculations,  
> **so that** we can handle dense threat environments and asymmetric threats.

**Candidate use cases (examples):**

| UC-ID | Name | Goal |
|-------|------|------|
| UC-TRK-01 | Maintain tracks in clutter | Operator sees stable tracks despite noisy radar |
| UC-ID-01 | Confirm or override track identity | Operator accepts AI ID or corrects it |
| UC-THR-01 | Review threat prediction cues | Operator sees ranked threat cues with rationale hooks |
| UC-ENG-01 | Review engagement calculation aid | Operator gets engagement support with human approval gate |

Each UC must still respect vision principles (e.g. human-in-the-loop on high-stakes act).

**ETAS needs → use cases:**

> **As** <u>**SDC employees**</u>,  
> **we need** a fast PIN-based check-in and clear progress toward the daily target,  
> **so that** we spend time on the mission instead of fighting the timesheet.

→ UC-CI-01 Check in for today; UC-CO-01 Check out

> **As** <u>**FOSC program administrators**</u>,  
> **we need** electronic attendance with TEMPO-aware export under contract schedule rules,  
> **so that** we can produce auditable weekly and quarterly packages without manual rework.

→ UC-EX-01 Export weekly package; UC-EX-02 Export quarterly package

> **As** <u>**SDC employees**</u>,  
> **we need** leave request and approval that respects remaining balance,  
> **so that** time off is fair and auditable without spreadsheet rework.

→ UC-LV-01 Request leave; UC-LV-02 Approve leave

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
| Hybrid human–AI SA | **As** <u>**operators**</u>, **we need** better tracking… | UC-TRK-01 | FR-TRK-… |
| Auditable FOSC export | **As** <u>**FOSC program administrators**</u>, **we need** TEMPO-aware package… | UC-EX-02 | FR-FOSC-…, FR-DISC-… |

Leave the FR column blank until the requirements module — but keep the rows and the relationship names.

## Workshop (20 min)

Take **one** needs statement from A1 or the AFAD example (keep **As** / **we need** / **so that** and the underlined stakeholder).

1. Write **3 use case names** with primary actor + goal  
2. Fully draft **one** use case (main success + ≥ 2 extensions)  
3. Mark which extensions will need IF/THEN requirements  

## What use cases are not

- Not UI wireframes (those are design)  
- Not EARS requirements (those are the next layer)  
- Not the vision paragraph  

> **Reminder:** If you generate any wording with an AI tool, add an in-text citation (e.g., *Generated with ChatGPT, 2026*). The underlying idea and structure must still be yours.

## Tools for these artifacts

**Goal:** readable UC briefs and a trace table — not a UML suite on day one.

| Artifact | Simplest clear tools | Program / enterprise class |
|----------|----------------------|----------------------------|
| Use-case brief | Markdown template (fields above) | DOORS/Jama *text objects*; wiki pages |
| UC index / catalog | Markdown table or Excel | Req DB hierarchy |
| Optional UC diagram | Mermaid or draw.io *after* the text brief | Rhapsody / Cameo use-case diagrams |
| Trace rows (need → UC) | Markdown / Excel table | Live links in req tools |

Write the **text brief first**. A bubble diagram without main success + extensions is incomplete.

| Topic | Link |
|-------|------|
| UML use-case overview | [uml-diagrams.org — use case](https://www.uml-diagrams.org/use-case-diagrams.html) |
| Mermaid | [Mermaid docs](https://mermaid.js.org/) |
| Cockburn-style goal levels | Search “Cockburn use case goal levels” |
| SEBoK scenarios | [SEBoK search — use case](https://sebokwiki.org/wiki/Special:Search?search=use+case) |

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
