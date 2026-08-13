# Requirements & Acceptance Criteria

## Learning outcomes

- Write **shall** requirements with stable IDs  
- Use **EARS grammar** patterns so requirements are clear and consistent  
- **See** the EARS keywords (**WHEN** / **WHILE** / **IF** / **THEN** / **WHERE** / **shall**) at a glance  
- Recognize **requirement levels**: stakeholder → system → subsystem  
- Expect the **count of requirements to expand** as you decompose downward  
- Keep **traceability between levels** (parent ↔ child)  
- Derive FRs from **use cases** (which come from needs and vision)  
- Separate **functional** and **non-functional** requirements  
- Handle unknown numbers with **TBD** / **TBR** without writing fake precision  
- Keep a **definition library** for acronyms and ambiguous terms  
- Write **Given / When / Then** acceptance criteria that **prove** EARS FRs without rewriting them  
- Spot when ACs are **papering over** a vague requirement — and fix the requirement instead  

## From vision → needs → use cases → requirements

**Full cascade (do not skip)** — skipping any upstream artifact breaks traceability and makes validation impossible.

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS (this module)
              derives_from   traces_to    allocated_to
```

| Layer | Form | Link |
|-------|------|------|
| Vision | Shared future state + principles | (system vision may **derives_from** global vision) |
| Needs | `As <stakeholder>, we need …, so that …` | **derives_from** vision |
| Use cases | Actor + goal + main success + extensions | Need **traces_to** use case |
| Requirements | **EARS + shall** + IDs + acceptance criteria | Use case **allocated_to** this FR |

Requirements answer: **What shall the system do** so each use case works (including failures)?  
Do **not** paste a need or vision paragraph as a requirement. The FR is **allocated_to** from a use case — not a free-floating shall.

| Source (UC) | System requirement (EARS) | EARS pattern |
|-------------|---------------------------|--------------|
| Check in / already checked in | **IF** an employee submits check-in **WHILE** already checked in that date, **THEN** the ETAS **shall** reject … | **IF**/**THEN** + **WHILE** |
| Export quarterly package | **WHEN** an authorized user exports a quarter, the ETAS **shall** include a Discrepancy Tracker sheet | **WHEN** |
| Maintain tracks in clutter | **WHEN** a new plot is associated to a track, the SA system **shall** update track kinematics within *T* seconds | **WHEN** |

**Habit:** Every FR lists its parent use case (`UC-…` via **allocated_to**) and, when known, the need/vision chain (**traces_to** / **derives_from**).

## Requirements levels (stakeholder → system → subsystem)

EARS tells you *how to word* a shall. **Levels** tell you *whose problem* the shall is solving and *which product element* is obligated.

```text
Stakeholder requirements  (customer / user intent — often loose)
        │  refined / decomposed  (trace parent → children)
        ▼
System requirements       ("The <System> shall …")
        │  refined / decomposed  (trace parent → children)
        ▼
Subsystem / component requirements  ("The <Subsystem> shall …")
        │
        ▼
(further allocation to design, interfaces, tests)
```

| Level | Who typically writes it | What it sounds like | Naming habit |
|-------|-------------------------|---------------------|--------------|
| **Stakeholder requirements** | Customer, ops, user reps (sometimes a contractor writing *for* them) | Capability, outcome, constraint in stakeholder language — often **not** tight EARS | May say “the system shall support operators…” or even “users need…” |
| **System requirements** | SE / contractor after analysis | Testable **shall** on the **whole system** | Subject is the **system name** (e.g. *The ETAS*, *The SA system*) |
| **Subsystem requirements** | SE + subsystem owners | Testable **shall** on a **piece** of the system | Subject is the **subsystem / component name** (e.g. *The time_state service*, *The export module*, *The track correlator*) |

### Stakeholder requirements — expect looseness

Customers usually produce **stakeholder requirements** (sometimes called user requirements, operational requirements, or “customer shalls”). Unless a disciplined contractor wrote them, they are often:

- Outcome-oriented but **vague** (“timely,” “user-friendly,” “secure enough”)  
- Mixed with needs, wishes, and design preferences  
- Missing exception paths and measurable thresholds  

**Your job as SE is not to mock the customer** — it is to **refine** stakeholder intent into system (then subsystem) requirements that *can* be verified, while **tracing** every child back to a parent stakeholder requirement (or an explicit derived need).

### System vs subsystem — the subject of the sentence

- **System requirement:** the **system** is the actor of **shall**.  
  - **WHEN** an authorized user exports a quarter, **the ETAS** **shall** include a Discrepancy Tracker sheet.  
- **Subsystem requirement:** a **named part** is the actor of **shall**.  
  - **WHEN** an authorized user exports a quarter, **the FOSC export module** **shall** write a Discrepancy Tracker sheet into the package workbook.  

If the subject is wrong, allocation and test ownership will be wrong.

### Decomposition expands the count

**One** stakeholder requirement usually becomes **several** system requirements; **one** system requirement usually becomes **several** subsystem requirements (and interface requirements).

```text
1 stakeholder req  →  N system reqs  →  M subsystem reqs   (N, M ≥ 1; often M ≫ N)
```

**Example (teaching sketch)**

| Level | ID | Statement (condensed) |
|-------|-----|------------------------|
| Stakeholder | StR-EXP-01 | Program staff can produce an auditable quarterly attendance package without rebuilding spreadsheets by hand. |
| System | FR-EXP-01 | **WHEN** an authorized user exports a quarter, **the ETAS** **shall** generate a workbook with weekly sheets and a Discrepancy Tracker. |
| System | FR-EXP-02 | **IF** TEMPO data for the quarter is incomplete, **THEN** **the ETAS** **shall** still export and flag missing weeks. |
| Subsystem | FR-EXP-01-A | **WHEN** export is requested, **the FOSC export module** **shall** assemble weekly timekeeping sheets. |
| Subsystem | FR-EXP-01-B | **WHEN** export is requested, **the FOSC export module** **shall** write the Discrepancy Tracker sheet. |
| Subsystem | FR-EXP-02-A | **IF** a week has no TEMPO import, **THEN** **the FOSC export module** **shall** mark that week’s variance as unavailable. |

Count went **1 → 2 → 3+**. That expansion is normal. What is *not* normal is children with **no parent** (gold plating) or parents with **no children** when the architecture already has real pieces that must behave.

### Traceability between levels is mandatory

| Link | Meaning |
|------|---------|
| Stakeholder req → system req | System shalls that **implement** the stakeholder intent |
| System req → subsystem req | Subsystem shalls that **implement** the system shall |
| Any req → test / AC | Evidence that the shall is met |

**Rules**

1. Every system/subsystem FR has a **parent** (stakeholder or system req, or an explicit derived justification).  
2. Every parent that remains in scope has **enough children** to cover it (or an explicit “satisfied by design constraint X”).  
3. IDs should make parentage obvious when possible (`FR-EXP-01` → `FR-EXP-01-A`).  
4. Changing a parent without reviewing children is a baseline error.  

In this course, A2 focuses mainly on **system-level** EARS FRs for ETAS-style scope. Know the level model so you do not confuse a stakeholder wish with a subsystem design constraint.

## Shall language

Mandatory behavior uses **shall** (not should / might / try to).

| Prefer | Avoid (for mandatory behavior) |
|--------|--------------------------------|
| **shall** | should, might, try to |
| measurable | “user friendly”, “fast enough” without numbers or TBD |
| one idea per shall | paragraphs of mixed rules |

## EARS grammar (primary method in this course)

**EARS** = *Easy Approach to Requirements Syntax* (Mavin et al.).  
It is a small set of sentence patterns that force you to name **when** a requirement applies. Interns in this course **shall** write functional requirements in EARS form.

**Highlight convention in this module:** EARS keywords appear in **bold** so the structure is obvious:

| Keyword | Role |
|---------|------|
| **WHEN** | Event / trigger |
| **WHILE** | State / mode that holds |
| **IF** … **THEN** | Unwanted condition / exception path |
| **WHERE** | Optional feature / configuration is present |
| **shall** | Mandatory system response |

### Building blocks

| Piece | Meaning |
|-------|---------|
| **Precondition / trigger** | Event, state, or unwanted condition (optional for ubiquitous) |
| **System name** | Usually “The <system>” (e.g. The ETAS, The SA display) — at subsystem level, use the **subsystem** name |
| **shall** | Mandatory |
| **response** | Observable system behavior (not design code) |

### The five core EARS patterns

#### 1. Ubiquitous (always true)

No special trigger — the system always has this property or behavior.

> The <system> **shall** <system response>.

**Examples**

- The ETAS **shall** store employee PINs only as one-way hashes.  
- The SA display **shall** show time in the operator’s configured timezone.  

Use sparingly for true always-on rules. If it only applies after an event, do **not** force ubiquitous.

#### 2. Event-driven (**WHEN**)

Something happens → system responds.

> **WHEN** <optional preconditions> <trigger>, the <system> **shall** <system response>.

**Examples**

- **WHEN** an employee submits a check-in and the employee is not already checked in for that work date, the ETAS **shall** create a check-in time entry.  
- **WHEN** the operator selects a track on the map, the SA display **shall** show that track’s detail panel.  

#### 3. State-driven (**WHILE**)

While a condition/state holds, the system maintains a behavior.

> **WHILE** <in a specific state / preconditions>, the <system> **shall** <system response>.

**Examples**

- **WHILE** an employee is in the checked-in state for the current work date, the ETAS **shall** offer check-out and **shall** not accept a second check-in for that date.  
- **WHILE** a track is in Lost status, the SA display **shall** render that track with the Lost symbology.  

#### 4. Unwanted condition (**IF** … **THEN**)

Handle faults, exceptions, illegal inputs, failures.

> **IF** <unwanted condition / optional preconditions>, **THEN** the <system> **shall** <system response>.

**Examples**

- **IF** an employee attempts check-out without an open check-in for that work date, **THEN** the ETAS **shall** reject the request and display an error that check-in is required first.  
- **IF** a feed message fails schema validation, **THEN** the SA ingest service **shall** discard the message and increment the invalid-message counter.  

#### 5. Optional feature (**WHERE**)

Only when a feature or configuration is included.

> **WHERE** <feature is included>, the <system> **shall** <system response>.

**Examples**

- **WHERE** BEOD blanket approval is enabled, the ETAS **shall** treat claimed BEOD as approved without a separate manager action.  
- **WHERE** dual-feed correlation is enabled, the SA system **shall** attempt to merge tracks that share the same identity within the configured gate.  

### Complex EARS — stack carefully; protect readability

Real requirements often **stack** keywords. That is allowed — and dangerous if the sentence becomes a novel.

**Allowed stack shapes (keep short):**

> **WHILE** <state> **WHEN** <trigger>, the <system> **shall** <response>.  
> **WHEN** <trigger> **IF** <unwanted>, **THEN** the <system> **shall** <response>.  
> **WHERE** <feature> **WHEN** <trigger>, the <system> **shall** <response>.

**Key point (readability):**

1. **One primary response** per FR — if tests would diverge, split into two FRs.  
2. **One unwanted path per IF/THEN** when possible — do not nest three exceptions in one sentence.  
3. Prefer **two clear shalls** over one dense paragraph a reviewer cannot parse in 10 seconds.  
4. Stack order should match how a tester thinks: state → event → exception → response.  
5. If you need more than ~25–30 words after **shall**, you are probably smuggling design or multiple requirements.

**Example (ETAS BEOD) — stacked but still scannable**

- **WHEN** daily hours are recalculated, **IF** BEOD is claimed and approved and raw work hours are less than 6.0, **THEN** the ETAS **shall** set BEOD credit hours to 0.  
- **WHEN** daily hours are recalculated, **IF** BEOD is claimed and approved and raw work hours are greater than or equal to 6.0, **THEN** the ETAS **shall** set BEOD credit hours to 1.0.  

*Note the split into two FRs instead of one “if … else …” essay inside a single shall.*

### EARS quality rules

1. **Name the system** (or subsystem) consistently — subject must match the **level**.  
2. **One primary response** per requirement (split compound “and also…” if tests diverge).  
3. **Triggers and states are testable** — avoid vague “when appropriate”.  
4. **Response is observable** — UI message, stored record, exported field, rejected action.  
5. **No design smuggling** — “shall use React” is design unless the customer constrained the how.  
6. **Prefer IF/THEN for rejects** — illegal paths are first-class requirements.  
7. **Bold the EARS keywords** in drafts so peers can scan structure quickly.  
8. **Trace to parent level** — system FR → stakeholder (or need/UC); subsystem FR → system FR.  

### EARS pattern cheat sheet

| Keyword | Use when… | Skeleton | Example pattern |
|---------|-----------|----------|-----------------|
| *(none)* | Always true | The system **shall** … | Ubiquitous |
| **WHEN** | Event / trigger | **WHEN** … the system **shall** … | Event-driven |
| **WHILE** | State / mode | **WHILE** … the system **shall** … | State-driven |
| **IF** / **THEN** | Unwanted / exception | **IF** … **THEN** the system **shall** … | Unwanted condition |
| **WHERE** | Optional feature enabled | **WHERE** … the system **shall** … | Optional feature |

### Workshop — rewrite into EARS (10 min)

Convert each line. Identify the pattern you used. **Bold** the keywords.

| Informal | Your EARS rewrite |
|----------|-------------------|
| Users can’t check in twice | |
| Export the quarterly package | |
| Bad TEMPO file shouldn’t crash the app | |
| Only if phone support feature is on, log hours | |
| While on leave approval pending, days are reserved | |

**Suggested answers (check after you try)**

- **IF** an employee submits check-in **WHILE** already checked in for that date, **THEN** the ETAS **shall** reject the check-in and **shall** not create a new entry. *(**WHILE** + **IF**, or pure **IF**)*  
- **WHEN** an authorized manager requests a quarterly FOSC export, the ETAS **shall** generate an Excel package containing one timekeeping sheet per week in the quarter and a Discrepancy Tracker sheet. *(**WHEN**)*  
- **IF** an uploaded TEMPO file is not valid CSV, **THEN** the ETAS **shall** reject the import and display an error without modifying existing TEMPO weekly hours. *(**IF**/**THEN**)*  
- **WHERE** phone support logging is enabled, **WHEN** an employee submits phone-support hours for a date, the ETAS **shall** store those hours and include them in that day’s FOSC total. *(**WHERE** + **WHEN**)*  
- **WHILE** a leave request is pending, the ETAS **shall** reserve the requested vacation or sick days against the employee’s remaining balance. *(**WHILE**)*  

## TBD and TBR (when the number is not known yet)

Early requirements often need a **placeholder** for a performance value, threshold, or external decision that is not fixed. Use formal markers — do **not** invent a fake number and hope nobody notices.

| Marker | Meaning | Typical use |
|--------|---------|-------------|
| **TBD** | *To Be Determined* | Value not yet chosen; analysis, measurement, or stakeholder decision still open |
| **TBR** | *To Be Resolved* / *To Be Reviewed* | Value proposed or provisional; must be confirmed before baseline or verification |

**Good examples**

- **WHEN** a new plot is associated to a track, the SA system **shall** update track kinematics within **TBD** seconds.  
- The ETAS **shall** complete primary check-in API handling in under **TBR-2** seconds under normal demo load.  

**Rules**

1. Every **TBD** / **TBR** has an **owner** and a **resolve-by** (date or milestone).  
2. Keep a **TBD/TBR register** (table) in the requirements pack — ID, placeholder text, owner, due, status.  
3. Prefer **TBR** when you have a working assumption (e.g. “2 s”) that is not yet contractual.  
4. ACs may exercise a **provisional** value labeled TBR; they must not pretend the number is final.  
5. Closing a TBD/TBR is a **baseline change** — update the FR text, not only a comment in a test.  
6. Do **not** leave TBD forever; open TBDs at gate reviews are a risk signal.

| TBD/TBR ID | Appears in | Placeholder | Owner | Resolve by | Status |
|------------|------------|-------------|-------|------------|--------|
| TBD-SA-01 | FR-TRK-05 | kinematics update latency (s) | SA lead | before PDR | Open |
| TBR-ETAS-02 | NFR-PERF-01 | check-in API < 2 s | ETAS owner | Week 4 Thursday | Proposed |

## Definition library (kill ambiguity)

Any word or acronym in a requirement that is **not widely known** or could mean two things must be defined **once** in a shared **definition library** (glossary for the requirements pack).

**Why this is mandatory**

- Reviewers and testers will invent private meanings if you do not.  
- Contract and ops language (BEOD, TEMPO, FOSC, Lost track, “authorized user”) is not common English.  
- Stacked EARS sentences get unreadable when undefined terms multiply.

**What belongs in the library**

| Put it in the library if… | Examples |
|---------------------------|----------|
| Acronym or program term | BEOD, TEMPO, FOSC, ETAS, SA, MOSA |
| State or mode name | checked-in, Lost, pending leave |
| Role that grants permission | authorized manager, mission operator |
| Unit or threshold label | “work date”, “raw work hours”, “configured gate” |
| Anything a new intern would ask “what is that?” about | Discrepancy Tracker sheet, PIN |

**Format (simple table is enough)**

| Term | Definition (one sentence) | Source / owner |
|------|---------------------------|----------------|
| BEOD | Blanket Early Out Day credit under FOSC rules | Program / ETAS |
| TEMPO | External weekly hours source imported as CSV | Program interface |
| Lost (track) | Track status when association quality falls below gate | SA CONOPS |

**Rules**

1. Requirements **use** the term; the library **defines** it — do not redefine the same acronym five different ways in five FRs.  
2. If two teams disagree on a definition, fix the library under change control before arguing about the shall.  
3. ACs and ICDs must use the **same** definitions.  
4. Keep the library with the requirements pack (same markdown/Excel file or a linked glossary page).

## IDs

Use stable IDs for traceability:

- `FR-CI-02` — functional, check-in family  
- `NFR-SEC-01` — non-functional, security  
- Optional child pattern: `FR-EXP-01-A` for a subsystem FR under `FR-EXP-01`  

IDs never change meaning mid-course without a baseline note. If content must change, note the revision (e.g. `FR-CI-02` rev 2, or a change log line) so reviewers know the baseline.

Tag the EARS pattern in a column or footnote if helpful: `FR-CI-02 [IF/THEN]`.

## Functional vs non-functional

| Type | Focus | EARS? |
|------|--------|--------|
| FR | Behavior / functions | **Yes — use EARS** |
| NFR | Qualities (security, performance, usability) | Often ubiquitous form is enough; still use **shall** + measurable criteria (or **TBD**/**TBR**) |

**NFR example (ubiquitous style)**  
The ETAS **shall** complete primary check-in API handling in under **TBR-2** seconds under normal demo load.

## Acceptance criteria

ACs **prove** an EARS requirement. Prefer **Given / When / Then** — it aligns naturally with **WHEN** / **WHILE** / **IF**.

They are **not** a second requirements document. On real programs (especially when FRs are **on contract**), the customer is entitled to the **shall-language**, not your favorite reading of an AC.

### Requirements vs acceptance criteria

| Artifact | Role | What it must not do |
|----------|------|---------------------|
| **Requirement (shall / EARS)** | Obligates the system — *what must be true* | Hide meaning that only appears in a test |
| **Acceptance criterion** | Shows *how we will check* that the shall is met | Add, drop, or reinterpret obligations that are not in the FR |

**Rule of thumb:** If you need the AC to understand what the requirement means, the **requirement is incomplete**. Fix the FR under change control; do not “clarify” it only in the AC.

### Why this bites on contract work

Programs sometimes write vague FRs and then lean on detailed ACs so the team can build something. That often **backfires**:

1. The team implements what the **AC** says.  
2. The customer (or inspector) points at the **contractual requirement** and demands *their* interpretation.  
3. The AC does not protect you — it is usually a **verification artifact**, not the binding obligation.  

So: make the **shall** testable and unambiguous *on its own*. Use ACs to exercise that meaning, not to replace it.

### Aligned example (AC faithful to FR)

```text
FR-CI-02 [IF/THEN]
IF an employee attempts check-in WHILE already checked in for that work date,
THEN the ETAS shall reject the request and shall not create a new time entry.

AC-CI-02 · FR-CI-02
Given employee E is checked in today
When E submits another check-in for today
Then the system rejects the request and stores no new check-in entry
```

*(In published module text, the FR above is written with bold keywords: **IF** … **WHILE** … **THEN** … **shall** …)*

The AC checks **reject** and **no new entry** — what the shall already states. It does not invent a specific UI message unless the FR requires one (that would be an extra obligation).

### Anti-pattern — AC papers over a bad FR

| Bad FR (vague) | Tempting AC (sneaks in the real rule) | What went wrong |
|----------------|----------------------------------------|-----------------|
| The ETAS **shall** handle BEOD correctly. | Given raw hours ≥ 6.0 and BEOD claimed… Then credit = 1.0 h | The **6.0 h / 1.0 h** rule only lives in the AC. Customer can still argue “correctly” means something else. |
| The SA system **shall** update tracks in a timely manner. | Given a new plot… Then kinematics update within 2 s | Timeliness was never in the shall. Fix the FR: “within **TBD** seconds” or a real number. |
| The export **shall** be contract-compliant. | Given TEMPO import… Then column M variance is zeroed above TEMPO | “Compliant” is undefined. Put TEMPO shortfall rules in the **shall** (and define terms in the library), not only the AC. |

**Repair path:** rewrite the FR in EARS with the numbers (or TBD/TBR) and conditions, *then* write ACs that only demonstrate that FR.

### Alignment checks (before you submit)

1. **Cover test** — Every obligation in the FR (triggers, states, responses, thresholds) is exercised by at least one AC.  
2. **No-extra test** — Nothing in the AC is a new obligation the FR does not state (no new thresholds, roles, or reject reasons).  
3. **Stand-alone FR** — A peer who never sees the AC can still pass/fail the FR in principle.  
4. **Conflict** — If AC and FR disagree, **the FR wins** until the baseline is changed. Do not “win the argument” with a cleverer AC.  
5. **Definitions** — Every non-obvious term in the FR appears in the definition library.  

### Quality checklist for ACs

- [ ] Observable result (not “user is happy”)  
- [ ] Named preconditions (match EARS **WHEN**/**WHILE**/**IF**)  
- [ ] Faithful to the FR — no new rules, no dropped thresholds  
- [ ] Covers at least one failure path for critical FRs  
- [ ] Independent tester could run it without asking you  
- [ ] If the FR is vague, you **fixed the FR** instead of only writing a better AC  

## Bad → better (EARS)

| Bad | Better (EARS) | EARS pattern |
|-----|---------------|--------------|
| System should handle leave | **WHEN** an employee submits a leave request with valid dates and sufficient balance, the ETAS **shall** create a leave request in pending status. | **WHEN** |
| UI must be modern | **WHEN** an employee starts check-in from the login list, the ETAS **shall** complete the primary check-in flow in ≤ 3 user interactions. | **WHEN** |
| BEOD works correctly | **WHEN** daily hours are recalculated, **IF** BEOD is claimed and approved and raw hours ≥ 6.0, **THEN** the ETAS **shall** apply 1.0 h BEOD credit. | **WHEN** + **IF**/**THEN** |
| Don’t allow bad check-out | **IF** an employee requests check-out and there is no open check-in for that date, **THEN** the ETAS **shall** reject the check-out. | **IF**/**THEN** |

**NFR example (security – ubiquitous style)**  
The ETAS **shall** store all employee PINs as one-way SHA-256 hashes and **shall** reject any login attempt that supplies a PIN not matching the stored hash.

## Acceptance-criteria mapping table

| FR ID | AC ID(s) |
|-------|----------|
| FR-CI-02 | AC-CI-02 |
| FR-EXP-01 | AC-EXP-01, AC-EXP-02 |
| FR-TRK-05 | AC-TRK-05 |

## Case study pointer

Open the ETAS app → **Systems Engineering** page (linked from course Home; path often `/systems-engineering`) → requirements section. Rewrite 3 listed FRs into strict EARS form, **bold** the keywords, and note which pattern you used. Do not copy blindly — understand *why* each FR exists.

## Offline practice (45 min)

*Work in 20-minute blocks with a 5-minute stretch break to keep focus.*

1. **5 FRs in EARS** — at least one of each pattern (**WHEN**, **WHILE**, **IF**/**THEN**, **WHERE**, ubiquitous); bold the keywords; use the **system** name as subject (system level).  
2. **2 NFRs** with measurable criteria or **TBD**/**TBR**.  
3. **3 ACs** in Given/When/Then, each linked to an FR ID.  
4. A mini **definition library** (≥ 5 terms used in your FRs).  
5. A **TBD/TBR register** if any placeholder appears.  
6. **Optional stretch:** take one system FR and write **two** subsystem children with parent ID links.  

Self-score:

- Every FR matches an EARS skeleton from the cheat sheet.  
- Keywords are easy to scan (**WHEN** / **WHILE** / **IF** / **THEN** / **WHERE** / **shall**).  
- Subject of each shall matches the **level** (system vs subsystem).  
- Every AC references the exact FR ID it validates.  
- For each AC: cover test + no-extra test (see **Alignment checks** above).  
- No AC is the only place a threshold or reject rule appears.  
- Every non-obvious term is in the definition library.  

## Assignment A2

**Requirements Pack** — heaviest SE take-home (**16%**).  
Assigned Monday of this week. **Draft** (4 FRs + 2 ACs) due this Thursday for coaching. **Final** due Thursday of the architecture week (Week 5), same day as **SE-A05**.

Functional requirements **must** use EARS grammar at **system level** unless the assignment asks otherwise. Include a short **definition library**. Use **TBD**/**TBR** only with a register entry. See Assignments.

> **Reminder:** If you generate any wording with an AI tool, add an in-text citation (e.g., *Generated with ChatGPT, 2026*). The underlying idea and structure must remain your own.

## Tools for these artifacts

**Goal:** a reviewable FR/AC pack with stable IDs — not a DOORS project for interns.

| Artifact | Simplest clear tools | Program / enterprise class |
|----------|----------------------|----------------------------|
| FR list (EARS + IDs) | Markdown table or Excel | DOORS, Jama, Polarion, Azure DevOps Boards |
| Level + parent links | Columns: Level, Parent ID | Hierarchical req modules / folders |
| Acceptance criteria | Same file; Given/When/Then rows linked by FR ID | Test tools (Xray, TestRail, …) linked to FRs |
| Definition library | Table in same pack or linked glossary | Shared glossary object in req DB |
| TBD/TBR register | Excel / markdown table | Risk or action register linked to FRs |
| Parent UC / need links | Extra columns (`UC-…`, `Need-…`) | Live trace links in req DB |
| Pattern tags | Column or footnote `[WHEN]`, `[IF/THEN]` | Attributes in req tool |

Excel is excellent for sorting by pattern and checking coverage. Markdown is excellent for review comments. Use either; keep IDs stable.

| Topic | Link |
|-------|------|
| EARS (Mavin et al.) | Search “Mavin EARS INCOSE” · [ResearchGate EARS paper](https://www.researchgate.net/publication/224157532_Easy_Approach_to_Requirements_Syntax_EARS) |
| System requirements (SEBoK) | [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition) |
| Given/When/Then (syntax inspiration) | [Cucumber — Gherkin](https://cucumber.io/docs/gherkin/reference/) |
| Req management (SEBoK) | [Requirements Management](https://sebokwiki.org/wiki/Requirements_Management) |

## Further reading

| Topic | Source |
|-------|--------|
| **EARS** (Easy Approach to Requirements Syntax) | Mavin et al., INCOSE — [EARS overview](https://www.researchgate.net/publication/224157532_Easy_Approach_to_Requirements_Syntax_EARS) · also search “Mavin EARS INCOSE” |
| System requirements | [SEBoK — System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition) |
| Requirements management | [SEBoK — Requirements Management](https://sebokwiki.org/wiki/Requirements_Management) |
| Acceptance / verification criteria | [SEBoK — System Verification](https://sebokwiki.org/wiki/System_Verification) |
| NASA requirements practice | [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/) |
| Given/When/Then (BDD style) | [Cucumber — Given When Then](https://cucumber.io/docs/gherkin/reference/) (syntax inspiration for ACs, not a mandate) |

## Next

**Architecture Views** — map each requirement to a design element (layers, allocation matrix, and decision records). This shows where requirements live in the system architecture.
