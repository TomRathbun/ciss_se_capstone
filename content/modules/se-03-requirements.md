# Requirements & Acceptance Criteria

## Learning outcomes

- Write **shall** requirements with stable IDs  
- Use **EARS grammar** patterns so requirements are clear and consistent  
- Derive FRs from **use cases** (which come from needs and vision)  
- Separate **functional** and **non-functional** requirements  
- Write **Given / When / Then** acceptance criteria that map to EARS FRs  
- Spot bad requirements and rewrite them into EARS form  

## From vision → needs → use cases → requirements

Full cascade (do not skip):

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS (this module)
```

| Layer | Form |
|-------|------|
| Vision | Shared future state + principles |
| Needs | `As <stakeholder>, we need …, so that …` |
| Use cases | Actor + goal + main success + extensions |
| Requirements | **EARS + shall** + IDs + acceptance criteria |

Requirements answer: **What shall the system do** so each use case works (including failures)?  
Do **not** paste a need or vision paragraph as a requirement.

| Source | System requirement (EARS) |
|--------|---------------------------|
| UC: Check in / already checked in | IF an employee submits check-in WHILE already checked in that date, THEN the ETAS shall reject … |
| UC: Export quarterly package | WHEN an authorized user exports a quarter, the ETAS shall include a Discrepancy Tracker sheet |
| UC: Maintain tracks in clutter (from AFAD-style need) | WHEN a new plot is associated to a track, the SA system shall update track kinematics within T seconds |

**Habit:** Every FR should list `UC-…` (and ideally need/vision) in a trace column.

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

| Keyword | Use when… | Skeleton |
|---------|-----------|----------|
| *(none)* | Always true | The system shall … |
| **WHEN** | Event / trigger | WHEN … the system shall … |
| **WHILE** | In a state / mode | WHILE … the system shall … |
| **IF / THEN** | Unwanted / exception | IF … THEN the system shall … |
| **WHERE** | Optional feature on | WHERE … the system shall … |

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

IDs never change meaning mid-course without a baseline note.

Tag the EARS pattern in a column or footnote if helpful: `FR-CI-02 [IF/THEN]`.

## Functional vs non-functional

| Type | Focus | EARS? |
|------|--------|--------|
| FR | Behavior / functions | **Yes — use EARS** |
| NFR | Qualities (security, performance, usability) | Often ubiquitous form is enough; still use shall + measurable criteria |

**NFR example (ubiquitous style)**  
The ETAS shall complete primary check-in API handling in under 2 seconds under normal demo load.

## Acceptance criteria

ACs prove an EARS requirement. Prefer **Given / When / Then** — it aligns naturally with WHEN / WHILE / IF.

```text
FR-CI-02 [IF/THEN]
IF an employee attempts check-in WHILE already checked in for that work date,
THEN the ETAS shall reject the request and shall not create a new time entry.

AC-CI-02 · FR-CI-02
Given employee E is checked in today
When E submits another check-in for today
Then the system rejects with a clear error and stores no new check-in entry
```

### Quality checklist for ACs

- [ ] Observable result (not “user is happy”)  
- [ ] Named preconditions (match EARS WHEN/WHILE/IF)  
- [ ] Covers at least one failure path for critical FRs  
- [ ] Independent tester could run it without asking you  

## Bad → better (EARS)

| Bad | Better (EARS) |
|-----|----------------|
| System should handle leave | WHEN an employee submits a leave request with valid dates and sufficient balance, the ETAS shall create a leave request in pending status. |
| UI must be modern | WHEN an employee starts check-in from the login list, the ETAS shall complete the primary check-in flow in ≤ 3 user interactions. |
| BEOD works correctly | WHEN daily hours are recalculated, IF BEOD is claimed and approved and raw hours ≥ 6.0, THEN the ETAS shall apply 1.0 hour of BEOD credit. |
| Don’t allow bad check-out | IF an employee requests check-out and there is no open check-in for that date, THEN the ETAS shall reject the check-out. |

## Case study pointer

Open the ETAS **Systems Engineering** page (requirements section). Rewrite 3 listed FRs into strict EARS form and note which pattern you used. Do not copy blindly — understand *why* each FR exists.

## Offline practice (45 min)

For a “meeting room booking” system, write:

1. **5 FRs in EARS** — at least one of each: WHEN, WHILE, IF/THEN, WHERE, and one ubiquitous  
2. **2 NFRs** with measurable criteria  
3. **3 ACs** in Given/When/Then, each linked to an FR ID  

Self-score: every FR must match an EARS skeleton from the cheat sheet.

## Assignment A2

**Requirements Pack** — major graded item (weight 25%).  
Functional requirements **must** use EARS grammar. See Assignments.

## Next

**Architecture views** — where requirements live in the design.
