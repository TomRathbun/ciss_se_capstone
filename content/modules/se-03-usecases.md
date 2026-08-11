# Use Cases from Needs

## Learning outcomes

- Derive **use cases** from needs (and ultimately from vision)  
- Write a lightweight use-case brief (actor, goal, main success, extensions)  
- Trace **use case → EARS requirements** without skipping layers  
- Check that each use case still **respects the parent vision principles**  

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

**Important:** A use case that satisfies a need but **violates a vision principle** is still wrong. Keep the vision (especially principles) in view while you name UCs.

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
Vision link: <which vision line / principle this UC must respect>
```

*Related need(s) use the same course grammar as module 02: **As** / **we need** / **so that**, with the stakeholder **bold and underlined**.*

### Naming tips

| Prefer | Avoid |
|--------|--------|
| Export quarterly FOSC package | Click export button |
| Correlate dual-feed tracks | Run neural net |
| Request multi-day vacation | Fill form |

## Derive use cases from a need (with vision in view)

Work **top-down**: vision → need → use cases. Do not invent UCs from a need alone.

### 1. Parent vision (AIC2 teaching example — condensed)

*Same classroom vision as se-02; not a live program document.*

**Title:** AI-Augmented Command and Control (AIC2) Vision for Tech Refresh Phase 2

**Vision body (condensed):**  
The AIC2 vision for Tech Refresh Phase 2 (TR2) extends Phase 1 foundations into a **hybrid human–AI ecosystem** that augments UAE AFAD command and control. It prioritizes **resilient, ethical AI** for decision superiority in multi-domain operations, **Combat Cloud–style** flexibility where appropriate, and **operator oversight**, modularity, and adaptability in crowded UAE airspace. AIC2 incorporates a **Modular Open Systems Approach (MOSA)** so modules can be upgraded with loose coupling and open standards.

**Key principles (must constrain use cases):**

1. **Hybrid algorithmic approaches** — Blend learning-based methods with physics-based / rule-based methods.  
2. **Graduated autonomy (OODA)** — Assisted observe/orient → recommended decide → configurable act; **human-in-the-loop for high-stakes actions**.  
3. **Open standards for AI lifecycle** — Portable models, vendor-agnostic integration, continuous improvement without locking the enterprise to one stack.

### 2. Need that **derives_from** this vision

> **As** <u>**UAE AFAD Mission Operators**</u>,  
> **we need** AI tools that combine smart learning with proven rules for better tracking, identification, threat prediction, and engagement calculations,  
> **so that** we can handle dense threat environments and asymmetric threats.

*(Supports vision: hybrid algorithms + decision superiority in dense airspace.)*

### 3. Candidate use cases (**traces_to** the need — and checked against principles)

| UC-ID | Name | Goal | Vision principle check |
|-------|------|------|------------------------|
| UC-TRK-01 | Maintain tracks in clutter | Operator sees stable tracks despite noisy radar | Hybrid methods OK; operator still owns SA picture |
| UC-ID-01 | Confirm or override track identity | Operator accepts AI ID or **corrects** it | **Graduated autonomy** — human can override |
| UC-THR-01 | Review threat prediction cues | Operator sees ranked threat cues with rationale hooks | Aids decide; does not auto-prosecute |
| UC-ENG-01 | Review engagement calculation aid | Operator gets engagement support with **human approval gate** | **Human-in-the-loop** on high-stakes act — required |

**Anti-pattern:** a use case named “Auto-engage threat without operator confirmation” might help speed, but it **breaks principle 2**. Reject it even if the need mentioned engagement calculations.

**Habit:** every UC brief lists a **Vision link** (principle or vision phrase). If you cannot name one, the UC may be gold plating or out of spirit.

---

### ETAS path (same discipline, shorter vision)

**Vision (mini):** A single, trustworthy electronic time and attendance system for FOSC support staff — fast check-in, audited leave, TEMPO-aware export without hand-built spreadsheets.

> **As** <u>**SDC employees**</u>,  
> **we need** a fast PIN-based check-in and clear progress toward the daily target,  
> **so that** we spend time on the mission instead of fighting the timesheet.

→ UC-CI-01 Check in for today; UC-CO-01 Check out  
*(Vision: fast, trustworthy capture — not “skip PIN for speed.”)*

> **As** <u>**FOSC program administrators**</u>,  
> **we need** electronic attendance with TEMPO-aware export under contract schedule rules,  
> **so that** we can produce auditable weekly and quarterly packages without manual rework.

→ UC-EX-01 Export weekly package; UC-EX-02 Export quarterly package  
*(Vision: auditable package — not “email a private spreadsheet.”)*

> **As** <u>**SDC employees**</u>,  
> **we need** leave request and approval that respects remaining balance,  
> **so that** time off is fair and auditable without spreadsheet rework.

→ UC-LV-01 Request leave; UC-LV-02 Approve leave  
*(Vision: audited leave — manager approval stays in the chain.)*

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

| Vision (parent) / principle | Need **derives_from** | Use case **traces_to** | Later FR **allocated_to** |
|-----------------------------|----------------------|------------------------|---------------------------|
| AIC2 · graduated autonomy | **As** <u>**UAE AFAD Mission Operators**</u>, **we need** better tracking… | UC-ID-01, UC-ENG-01 | FR-… |
| AIC2 · hybrid algorithms | same need | UC-TRK-01 | FR-TRK-… |
| ETAS · auditable FOSC export | **As** <u>**FOSC program administrators**</u>, **we need** TEMPO-aware package… | UC-EX-02 | FR-FOSC-…, FR-DISC-… |

Leave the FR column blank until the requirements module — but keep the rows and the relationship names.

## Workshop (20 min)

Take **one** needs statement from A1 (or the AFAD example). Keep the parent **vision + principles** visible.

1. Write **3 use case names** with primary actor + goal  
2. For each UC, write which **vision principle** it must respect (or “none — reject UC”)  
3. Fully draft **one** use case (main success + ≥ 2 extensions)  
4. Mark which extensions will need IF/THEN requirements  

## What use cases are not

- Not UI wireframes (those are design)  
- Not EARS requirements (those are the next layer)  
- Not the vision paragraph  
- Not a license to ignore vision principles  

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
