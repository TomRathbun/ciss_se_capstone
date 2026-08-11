# What Is Systems Engineering?

## Learning outcomes

After this module you can:

- Explain SE in one paragraph to a non-engineer  
- Follow the **early** derivation chain: **Vision → Needs → Use cases → Requirements (EARS)**  
- Know that **Design / architecture / behavior** come **later** (allocation after the problem is clear)  
- Trace each requirement back to a vision, need, and use case (traceability)  
- Separate those layers without mixing them  
- Name why projects fail without SE discipline  
- Map a famous aerospace (or related) failure to a missing SE artifact  

## The one-paragraph definition

**Systems engineering** is the discipline of making sure we understand the real-world problem, capture what the system must do (and not do), design a solution that can be built and tested, integrate the pieces, and prove we met the need — across hardware, software, people, and process.

It is *not* only drawing diagrams. Diagrams are tools. The product of SE is **decisions under evidence** — recorded as **artifacts** (vision, needs, use cases, requirements, architecture views, behavior models, ICDs, RTMs). Use the **simplest clear tool** that makes each artifact reviewable; see **Welcome → Tools** for the course stance and tool classes (markdown, Excel, Mermaid, wikis, DOORS-class databases, MBSE tools, LLMs, …).

## The course derivation chain (memorize this)

In practice, strong teams get **everyone on the same perspective** before writing shall-statements. This course uses a cascade that works well on real programs (including prior CISS-style SE efforts).

Layers are not connected by a vague “refine” link. Use the **same relationship names** you will see on program artifact graphs.

### Early cascade (first weeks — stop here)

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS (EARS)
   │          │           │              │
 shared    who/why     how people     what the system
 picture   benefit     use it         shall do
```

| Relationship   | From → To                | Meaning |
|----------------|--------------------------|---------|
| **derives_from** | Need → Vision           | Stakeholder need is justified by the vision |
| **traces_to**    | Need → Use case         | The need is realized by one or more goal-oriented interactions |
| **allocated_to** | Use case → Requirement  | The use case is specified by one or more shall-statements (EARS) |

**Do not jump to Design yet.** Starting with a solution is the most common intern mistake. Architecture, behavior models, and interfaces come after requirements are clear.

### Full cascade (later modules)

Once requirements exist, continue:

```text
REQUIREMENTS (EARS)
        │ allocated_to
        ▼
ARCHITECTURE / STRUCTURE
(context, containers, components)
        │ exercised by
        ▼
BEHAVIOR
(state machines + sequence diagrams)
        │
        ▼
INTERFACES / ICDs  →  V&V / Trace
```

| Relationship   | From → To                    | Meaning |
|----------------|------------------------------|---------|
| **allocated_to** | Requirement → Design element | The FR is allocated to a service, module, ICD, etc. |

One parent can fan out: one vision → many needs; one need → many use cases; one use case → many FRs.

### Teaching example (AIC2-style graph)

Program tools often show **IDs on every node** and the link type on the edge — e.g. global vision → AIC2 vision → need → use case → requirement:

![Artifact relationship graph: global vision derives_from system vision derives_from need traces_to use case allocated_to requirement](/static/images/artifact-graph.png)

*Example chain (labels match the edges above):*  
`TR2-GLOBAL-VISION-…` → **derives_from** → `TR2-AIC2-VISION-…` → **derives_from** → `TR2-AIC2-NEED-…` → **traces_to** → `TR2-AIC2-UC-…` → **allocated_to** → `TR2-AIC2-REQ-…`

### Course cascade (compact)

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS  →  (later) DESIGN / ARCHITECTURE / BEHAVIOR
   │          │           │              │                         │
 shared    who/why     how people     what the system         how we structure
 picture   benefit     use it         shall do (EARS)         and exercise it
```

```mermaid
flowchart LR
    GV[Global vision] -->|derives_from| V[System / phase vision]
    V -->|derives_from| N[Need]
    N -->|traces_to| U[Use case]
    U -->|allocated_to| R[Requirement EARS]
    R -->|allocated_to| D[Design / Architecture]
```

*Alt text: Artifact chain with link types derives_from (visions and need), traces_to (need to use case), allocated_to (use case to requirement to design). Design is a later step.*

Optional display math (KaTeX) when you need formal models later:

$$
R_{\mathrm{trace}} = \frac{\\#\{\mathrm{FR\ with\ UC\ and\ test}\}}{\\#\{\mathrm{FR}\}}
$$

*R_trace* is the proportion of functional requirements that are traceable to a use case **and** an acceptance test — a simple coverage habit for later RTMs.

| Layer | Question | Artifact form (this course) | Typical tool / file type |
|-------|----------|------------------------------|--------------------------|
| **Vision** (global and/or system) | What future are we building toward together? | Short vision statement + optional key principles; child vision **derives_from** parent when both exist | .md or Confluence page |
| **Needs** | Who needs what, so that what benefit? | `As <stakeholder>, we need …, so that …` — need **derives_from** vision | .md, .txt |
| **Use cases** | How does a stakeholder achieve value with the system? | Named use case: actor, goal, main flow, extensions — need **traces_to** use case | .md, .xlsx |
| **Requirements** | What shall the system do in each situation? | EARS + shall, IDs, acceptance criteria — use case **allocated_to** requirement | .md, .reqs |
| **Design** (later) | How will we structure and implement it? | Architecture, modules, algorithms, UI — requirement **allocated_to** design | .md, .drawio, .py |
| **Behavior** (later) | When and in what order? | State machines, sequence diagrams | PlantUML, draw.io |
| **Interfaces** (later) | What contracts exist at boundaries? | Lightweight ICD | .md, schema |

**Common intern mistake:** jumping straight to design or to shall-language without a shared vision and named stakeholders — missing **derives_from** / **traces_to** links entirely.

### Why start with vision?

Vision is not always labeled as a formal “SE process step” in every textbook, but it is **widely used** and extremely useful:

- Aligns leadership, ops, and engineers on **one picture**  
- Frames phase boundaries (e.g. Tech Refresh Phase 2 vs Phase 1)  
- Gives criteria for “in spirit of the program” when requirements conflict  
- Becomes the north star for **validation** (“did we move toward this vision?”)  

Every need **derives_from** a vision (or principle). Each need **traces_to** one or more use cases; each use case is **allocated_to** requirements. If an FR cannot walk back through those links, question it (gold plating risk).

### Tiny example (time tracker)

| Layer | Example |
|-------|---------|
| Vision | A single, auditable FOSC attendance system that staff can use in seconds and program can export without rework |
| Need | As FOSC admins, we need TEMPO-aware export … so that packages are defensible |
| Use case | Manager exports quarterly FOSC package |
| Requirement | WHEN an authorized user exports a quarter, the ETAS shall include a Discrepancy Tracker sheet |
| Design *(later)* | `fosc_export.build_fosc_quarterly_workbook` |

### Larger example (mission C2 — teaching style)

A real program vision might describe **hybrid human-AI command and control**, open standards (e.g. MOSA), levels of autonomy, and resilient ops in dense airspace. From that vision you derive operator **needs**, then **use cases** (e.g. correlate tracks, recommend COA, engage with oversight), then **EARS requirements**. Full vision craft is in the next module.

## Why SE matters here

On CISS-type work you will touch:

- **Multiple users and roles** — you coordinate disparate stakeholder needs  
- **External systems** — feeds, exports, and other apps with real contracts  
- **Defensible rules** — decisions must survive review and audit  
- **Ops people** — planners and operators, not only developers  

SE gives a shared language so software, ops, and leadership do not talk past each other. **Vision is the first shared language.**

## Classic failure modes (watch for these in your work)

1. **No shared vision** – every team invents a different product.  
2. **Unstated assumptions** – “obvious” to you, invisible to the tester.  
3. **Gold plating** – features nobody needed (no path to vision/need).  
4. **Interface surprises** – two teams meet at a boundary with different formats.  
5. **Untestable “requirements”** – “the UI shall be intuitive.”  
6. **No validation** – built the wrong thing correctly.  
7. **AC papers over a bad FR** – thresholds live only in acceptance criteria; customer later enforces *their* reading of the contractual shall.  

## SE in aerospace history (why the discipline exists)

Modern systems engineering grew up in large aerospace and defense programs: many contractors, strict safety, and complex interfaces. The cases below are **public, open-source accounts**. Map each one to a course failure mode and to a missing artifact (need, UC extension, EARS IF/THEN, ICD, state machine, validation, go/no-go authority).

| Case | What went wrong (public summary) | SE lesson for this course | Read / watch |
|------|----------------------------------|---------------------------|--------------|
| **Challenger (STS-51-L, 1986)** | O-ring seal failed in cold launch conditions; known temperature risk was not treated as a hard constraint | Environment as **NFR**; independent challenge of “acceptable risk”; **validation** against real conditions; clear launch authority | [Rogers Commission report (NASA)](https://history.nasa.gov/rogersrep/genindex.htm) · [NASA investigation film (YouTube)](https://www.youtube.com/watch?v=MKG4bvZGWag) · [Photo/TV analysis team report (YouTube)](https://www.youtube.com/watch?v=6JlSfB32sJo) |
| **Ariane 5 Flight 501 (1996)** | Software reused from Ariane 4; horizontal velocity overflowed a 16-bit integer; both inertial systems failed | **Reuse** needs new **context** and **requirements**; exception paths as first-class FRs; system-level test of the flight-control chain | [ESA Inquiry Board summary](https://www.esa.int/Newsroom/Press_Releases/Ariane_501_-_Presentation_of_Inquiry_Board_report) · [Inquiry report (PDF mirror)](https://zoo.cs.yale.edu/classes/cs422/2010/bib/lions96ariane5.pdf) |
| **Mars Climate Orbiter (1999)** | Ground software provided thruster data in pound-seconds; navigation assumed newton-seconds | **ICD** with units and schemas; end-to-end **interface verification**; do not assume the other team “converted” | [NASA MCO Mishap Investigation Board Phase I (PDF)](https://www.dcs.gla.ac.uk/~johnson/Mars/MCO_MIB_Report.pdf) · [WIRED summary](https://www.wired.com/2010/11/1110mars-climate-observer-report/) |
| **Columbia (STS-107, 2003)** | Foam strike damaged wing; culture treated debris as non-critical; on-orbit imaging not obtained | Anomalies must **trace** to mission-critical requirements; clear go/no-go **authority**; debris as a real hazard in the **hazard/need** picture | [Columbia Accident Investigation Board (CAIB)](https://www.nasa.gov/columbia/caib/) · [CAIB findings / foam clip context (YouTube)](https://www.youtube.com/watch?v=V7UWCBNRr4s) |
| **Therac-25 (1985–87)** *(medical accelerator — classic software safety case)* | Race conditions + removed hardware interlocks → massive radiation overdoses | Safety interlocks as **FRs**, not optional design; **state machines** for illegal transitions; independent safety analysis | [Leveson & Turner, *IEEE Computer* (1993)](https://ieeexplore.ieee.org/document/274940) · search “Leveson Therac-25” for open PDF mirrors |
| **Boeing 737 MAX / MCAS (2018–19)** | Single AoA sensor path; pilots under-informed; certification and training assumptions failed | **Stakeholders** include operators; **use cases** for sensor failure; human-in-the-loop as requirement, not assumption | [U.S. House T&I Committee final report (2020)](https://transportation.house.gov/committee-activity/boeing-737-max-investigation) · Seattle Times investigative series (search “Seattle Times 737 MAX”) |

**One-line takeaway:** Aerospace did not invent SE after these accidents — it needed SE *because* these systems are too complex to succeed on heroics alone. Our chain (vision → needs → use cases → requirements → later architecture / behavior / ICDs / V&V) is the same discipline at classroom scale.

### Facilitator notes (optional classroom use)

- Pick **three** cases for a 15-minute discussion: Mars Climate Orbiter (interfaces), Ariane 5 (reuse + context), Challenger or Columbia (validation / authority).  
- Ask: *Which row in our failure-mode list does this match?* and *Which artifact would have forced the issue into the open?*  
- Videos are optional homework, not required viewing for graded work.

## Offline exercise (30 min)

Pick any app you use daily (banking, maps, chat). Write:

1. **Vision** – 2–4 sentences describing the next‑version goal.  
2. **Need** – One stakeholder statement: `As <stakeholder>, we need …, so that …`.  
3. **Use case** – Name, actor, and goal (one sentence each).  
4. **EARS requirement** – One shall‑statement supporting the use case.  
5. **Design choice** – One concrete implementation decision *not* phrased as a requirement (label it clearly as design, not requirement).

Bring the worksheet to Thursday; you may submit electronically if you’re unsure.

> **Reminder:** If you generate any wording with an AI tool, add an in-text citation (e.g., *Generated with ChatGPT, 2026*). The underlying idea and structure must still be yours.

## Later link (ops track)

When you reach **UAE Military Context**, study the training **OV-1** (layered AD, radars, weapons, C2/comms). That picture is the operational “shared view” that vision, needs, and ICDs hang from — same cascade, richer domain.

## Further reading

| Topic | Source |
|-------|--------|
| SE definition & value | [SEBoK — Systems Engineering](https://sebokwiki.org/wiki/Systems_Engineering) |
| Lifecycle context | [SEBoK — Life Cycle Models](https://sebokwiki.org/wiki/Life_Cycle_Models) |
| NASA fundamentals | [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/) |
| Practical guide (industry) | [MITRE Systems Engineering Guide](https://www.mitre.org/publications/systems-engineering-guide) |
| Failure modes / risk thinking | [SEBoK — Risk Management](https://sebokwiki.org/wiki/Risk_Management) |
| Aerospace cases (this module) | Links in the **SE in aerospace history** table above |
| Tools / artifacts (course stance) | **Welcome** module — Tools section |

## Next

**Vision, Stakeholders & Needs** — how to write a vision statement, list stakeholders, and derive needs in the course grammar.
