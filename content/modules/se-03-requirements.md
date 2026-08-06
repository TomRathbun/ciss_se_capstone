# Requirements & Acceptance Criteria

## Learning outcomes

- Write **shall** requirements with stable IDs  
- Use **EARS grammar** patterns so requirements are clear and consistent  
- Derive FRs from **use cases** (which come from needs and vision)  
- Separate **functional** and **non-functional** requirements  
- Write **Given / When / Then** acceptance criteria that **prove** EARS FRs without rewriting them  
- Spot when ACs are **papering over** a vague requirement — and fix the requirement instead  
- Spot bad requirements and rewrite them into EARS form  

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

| Source (UC)                              | System requirement (EARS)                                                                                     | EARS pattern |
|------------------------------------------|----------------------------------------------------------------------------------------------------------------|--------------|
| Check in / already checked in            | IF an employee submits check‑in WHILE already checked in that date, THEN the ETAS shall reject …               | IF/THEN + WHILE |
| Export quarterly package                  | WHEN an authorized user exports a quarter, the ETAS shall include a Discrepancy Tracker sheet                | WHEN |
| Maintain tracks in clutter (AFAD need)  | WHEN a new plot is associated to a track, the SA system shall update track kinematics within *T* seconds     | WHEN |


**Habit:** Every FR lists its parent use case (`UC-…` via **allocated_to**) and, when known, the need/vision chain (**traces_to** / **derives_from**).

## Shall language

Mandatory behavior uses **shall** (not should / might / try to).

| Prefer | Avoid (for mandatory behavior) |
|--------|--------------------------------|
| shall | should, might, try to |
| measurable | “user friendly”, “fast enough” without numbers |
| one idea per shall | paragraphs of mixed rules |

## EARS grammar (primary method in this course)

**EARS** = *Easy Approach to Requirements Syntax* (Mavin et al.).  
It is a small set of sentence patterns that force you to name **when** a requirement applies. Interns in this course **shall write functional requirements in EARS form**.

### Building blocks

| Piece | Meaning |
|-------|---------|
| **Precondition / trigger** | Event, state, or unwanted condition (optional for ubiquitous) |
| **System name** | Usually “The &lt;system&gt;” (e.g. The ETAS, The SA display) |
| **shall** | Mandatory |
| **response** | Observable system behavior (not design code) |

### The five core EARS patterns

#### 1. Ubiquitous (always true)

No special trigger — the system always has this property or behavior.

```text
The <system> shall <system response>.
```

**Examples**

- The ETAS shall store employee PINs only as one-way hashes.  
- The SA display shall show time in the operator’s configured timezone.  

Use sparingly for true always-on rules. If it only applies after an event, do **not** force ubiquitous.

#### 2. Event-driven (WHEN)

Something happens → system responds.

```text
WHEN <optional preconditions> <trigger> the <system> shall <system response>.
```

**Examples**

- WHEN an employee submits a check-in and the employee is not already checked in for that work date, the ETAS shall create a check-in time entry.  
- WHEN the operator selects a track on the map, the SA display shall show that track’s detail panel.  

#### 3. State-driven (WHILE)

While a condition/state holds, the system maintains a behavior.

```text
WHILE <in a specific state / preconditions> the <system> shall <system response>.
```

**Examples**

- WHILE an employee is in the checked-in state for the current work date, the ETAS shall offer check-out and shall not accept a second check-in for that date.  
- WHILE a track is in Lost status, the SA display shall render that track with the Lost symbology.  

#### 4. Unwanted condition (IF … THEN)

Handle faults, exceptions, illegal inputs, failures.

```text
IF <unwanted condition / optional preconditions> THEN the <system> shall <system response>.
```

**Examples**

- IF an employee attempts check-out without an open check-in for that work date, THEN the ETAS shall reject the request and display an error that check-in is required first.  
- IF a feed message fails schema validation, THEN the SA ingest service shall discard the message and increment the invalid-message counter.  

#### 5. Optional feature (WHERE)

Only when a feature or configuration is included.

```text
WHERE <feature is included> the <system> shall <system response>.
```

**Examples**

- WHERE BEOD blanket approval is enabled, the ETAS shall treat claimed BEOD as approved without a separate manager action.  
- WHERE dual-feed correlation is enabled, the SA system shall attempt to merge tracks that share the same identity within the configured gate.  

### Complex EARS (combine patterns)

Real requirements often stack keywords. Keep them readable; do not write novels.

```text
WHILE <state> WHEN <trigger> the <system> shall <response>.
WHEN <trigger> IF <unwanted> THEN the <system> shall <response>.
WHERE <feature> WHEN <trigger> the <system> shall <response>.
```

**Example (ETAS BEOD)**

- WHEN daily hours are recalculated, IF BEOD is claimed and approved and raw work hours are less than 6.0, THEN the ETAS shall set BEOD credit hours to 0.  
- WHEN daily hours are recalculated, IF BEOD is claimed and approved and raw work hours are greater than or equal to 6.0, THEN the ETAS shall set BEOD credit hours to 1.0.  

### EARS quality rules

1. **Name the system** consistently (`The ETAS`, `The SA system`).  
2. **One primary response** per requirement (split compound “and also…” if tests diverge).  
3. **Triggers and states are testable** — avoid vague “when appropriate”.  
4. **Response is observable** — UI message, stored record, exported field, rejected action.  
5. **No design smuggling** — “shall use React” is design unless the customer constrained the how.  
6. **Prefer IF/THEN for rejects** — illegal paths are first-class requirements.  

### EARS pattern cheat sheet

| Keyword | Use when…                     | Skeleton                              | Example pattern |
|----------|------------------------------|--------------------------------------|-----------------|
| *(none)* | Always true                  | The system shall …                   | Ubiquitous      |
| **WHEN** | Event / trigger              | WHEN … the system shall …            | Event‑driven    |
| **WHILE**| State / mode                 | WHILE … the system shall …            | State‑driven    |
| **IF / THEN** | Unwanted / exception     | IF … THEN the system shall …         | Unwanted condition |
| **WHERE**| Optional feature enabled      | WHERE … the system shall …            | Optional feature |


### Workshop — rewrite into EARS (10 min)

Convert each line. Identify the pattern you used.

| Informal | Your EARS rewrite |
|----------|-------------------|
| Users can’t check in twice | |
| Export the quarterly package | |
| Bad TEMPO file shouldn’t crash the app | |
| Only if phone support feature is on, log hours | |
| While on leave approval pending, days are reserved | |

**Suggested answers (check after you try)**

- IF an employee submits check-in WHILE already checked in for that date, THEN the ETAS shall reject the check-in and shall not create a new entry. *(WHILE + IF, or pure IF)*  
- WHEN an authorized manager requests a quarterly FOSC export, the ETAS shall generate an Excel package containing one timekeeping sheet per week in the quarter and a Discrepancy Tracker sheet. *(WHEN)*  
- IF an uploaded TEMPO file is not valid CSV, THEN the ETAS shall reject the import and display an error without modifying existing TEMPO weekly hours. *(IF/THEN)*  
- WHERE phone support logging is enabled, WHEN an employee submits phone-support hours for a date, the ETAS shall store those hours and include them in that day’s FOSC total. *(WHERE + WHEN)*  
- WHILE a leave request is pending, the ETAS shall reserve the requested vacation or sick days against the employee’s remaining balance. *(WHILE)*  

## IDs

Use stable IDs for traceability:

- `FR-CI-02` — functional, check-in family  
- `NFR-SEC-01` — non-functional, security  

IDs never change meaning mid-course without a baseline note. If content must change, note the revision (e.g. `FR-CI-02` rev 2, or a change log line) so reviewers know the baseline.

Tag the EARS pattern in a column or footnote if helpful: `FR-CI-02 [IF/THEN]`.

## Functional vs non-functional

| Type | Focus | EARS? |
|------|--------|--------|
| FR | Behavior / functions | **Yes — use EARS** |
| NFR | Qualities (security, performance, usability) | Often ubiquitous form is enough; still use shall + measurable criteria |

**NFR example (ubiquitous style)**  
The ETAS shall complete primary check-in API handling in under 2 seconds under normal demo load.

## Acceptance criteria

ACs **prove** an EARS requirement. Prefer **Given / When / Then** — it aligns naturally with WHEN / WHILE / IF.

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

The AC checks **reject** and **no new entry** — what the shall already states. It does not invent a specific UI message unless the FR requires one (that would be an extra obligation).

### Anti-pattern — AC papers over a bad FR

| Bad FR (vague) | Tempting AC (sneaks in the real rule) | What went wrong |
|----------------|----------------------------------------|-----------------|
| The ETAS shall handle BEOD correctly. | Given raw hours ≥ 6.0 and BEOD claimed… Then credit = 1.0 h | The **6.0 h / 1.0 h** rule only lives in the AC. Customer can still argue “correctly” means something else. |
| The SA system shall update tracks in a timely manner. | Given a new plot… Then kinematics update within 2 s | Timeliness was never in the shall. Fix the FR: “within *T* seconds.” |
| The export shall be contract-compliant. | Given TEMPO import… Then column M variance is zeroed above TEMPO | “Compliant” is undefined in the FR. Put TEMPO shortfall rules in the **shall** (or an ICD + FR), not only the AC. |

**Repair path:** rewrite the FR in EARS with the numbers and conditions, *then* write ACs that only demonstrate that FR.

### Alignment checks (before you submit)

1. **Cover test** — Every obligation in the FR (triggers, states, responses, thresholds) is exercised by at least one AC.  
2. **No-extra test** — Nothing in the AC is a new obligation the FR does not state (no new thresholds, roles, or reject reasons).  
3. **Stand-alone FR** — A peer who never sees the AC can still pass/fail the FR in principle.  
4. **Conflict** — If AC and FR disagree, **the FR wins** until the baseline is changed. Do not “win the argument” with a cleverer AC.

### Quality checklist for ACs

- [ ] Observable result (not “user is happy”)  
- [ ] Named preconditions (match EARS WHEN/WHILE/IF)  
- [ ] Faithful to the FR — no new rules, no dropped thresholds  
- [ ] Covers at least one failure path for critical FRs  
- [ ] Independent tester could run it without asking you  
- [ ] If the FR is vague, you **fixed the FR** instead of only writing a better AC  

## Bad → better (EARS)

| Bad                                               | Better (EARS)                                                                                                                       | EARS pattern |
|---------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|--------------|
| System should handle leave                        | WHEN an employee submits a leave request with valid dates and sufficient balance, the ETAS shall create a leave request in pending status. | WHEN |
| UI must be modern                                 | WHEN an employee starts check‑in from the login list, the ETAS shall complete the primary check‑in flow in ≤ 3 user interactions.       | WHEN |
| BEOD works correctly                             | WHEN daily hours are recalculated, IF BEOD is claimed and approved and raw hours ≥ 6.0, THEN the ETAS shall apply 1.0 h BEOD credit.       | WHEN + IF/THEN |
| Don’t allow bad check‑out                         | IF an employee requests check‑out and there is no open check‑in for that date, THEN the ETAS shall reject the check‑out.               | IF/THEN |

**NFR example (security – ubiquitous style)**  
The ETAS shall store all employee PINs as one‑way SHA‑256 hashes and shall reject any login attempt that supplies a PIN not matching the stored hash.

## Acceptance‑criteria mapping table

| FR ID      | AC ID(s)          |
|------------|-------------------|
| FR‑CI‑02   | AC‑CI‑02          |
| FR‑EXP‑01 | AC‑EXP‑01, AC‑EXP‑02 |
| FR‑TRK‑05 | AC‑TRK‑05        |


## Case study pointer

Open the ETAS app → **Systems Engineering** page (linked from course Home; path often `/systems-engineering`) → requirements section. Rewrite 3 listed FRs into strict EARS form and note which pattern you used. Do not copy blindly — understand *why* each FR exists.

## Offline practice (45 min)

*Work in 20‑minute blocks with a 5‑minute stretch break to keep focus.*

1. **5 FRs in EARS** — at least one of each pattern (WHEN, WHILE, IF/THEN, WHERE, ubiquitous).  
2. **2 NFRs** with measurable criteria.  
3. **3 ACs** in Given/When/Then, each linked to an FR ID.  

Self-score:

- Every FR matches an EARS skeleton from the cheat sheet.  
- Every AC references the exact FR ID it validates.  
- For each AC: cover test + no-extra test (see **Alignment checks** above).  
- No AC is the only place a threshold or reject rule appears.  


## Assignment A2

**Requirements Pack** — major graded item (weight 25%).  
Functional requirements **must** use EARS grammar. See Assignments.

> **Reminder:** If you generate any wording with an AI tool, add an in‑text citation (e.g., *Generated with ChatGPT, 2026*). The underlying idea and structure must remain your own.


## Further reading

| Topic | Source |
|-------|--------|
| **EARS** (Easy Approach to Requirements Syntax) | Mavin et al., INCOSE — [EARS overview (INCOSE paper index / author materials)](https://www.researchgate.net/publication/224157532_Easy_Approach_to_Requirements_Syntax_EARS) · also search “Mavin EARS INCOSE” |
| System requirements | [SEBoK — System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition) |
| Requirements management | [SEBoK — Requirements Management](https://sebokwiki.org/wiki/Requirements_Management) |
| Acceptance / verification criteria | [SEBoK — System Verification](https://sebokwiki.org/wiki/System_Verification) |
| NASA requirements practice | [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/) |
| Given/When/Then (BDD style) | [Cucumber — Given When Then](https://cucumber.io/docs/gherkin/reference/) (syntax inspiration for ACs, not a mandate) |

## Next

**Architecture views** — map each requirement to a design element (layers, allocation matrix, and decision records). This shows where requirements live in the system architecture.
