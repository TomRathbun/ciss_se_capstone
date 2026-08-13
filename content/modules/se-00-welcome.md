# Welcome & How This Course Works

## Why you are here

This is not a passive lecture series. **CISS Capstone** is how we train interns *and* decide who is ready to join the main engineering project.

You will:

1. Learn core **systems engineering** skills used on real programs.
2. Practice the derivation chain used on real efforts:  
   **Vision → Needs → Use cases → Requirements (EARS)**  
   with typed links: **derives_from**, **traces_to**, **allocated_to** (not a vague “refine”).  
   *We deliberately stop before Design in the first weeks* — jumping to design is the most common intern mistake. Architecture and allocation come later.
3. Learn enough **UAE military context** and **air operations** language (ranks, public systems, CONOPS/AOC, ATO planning/execution) to work around planning products.
4. Practice on a **living case study** — **SDC Time Tracker (ETAS)**, an electronic time-and-attendance system for FOSC support staff that already has requirements, states, sequences, and export interfaces.
5. Produce graded **artifacts**. Scores and professionalism determine selection.

## Learning objectives

By the end of the early SE weeks you will be able to:

- Write a **vision** and derive **needs** in the course grammar  
- Turn needs into **use cases**, then into **testable EARS requirements** with acceptance criteria  
- Later: allocate requirements to design elements, model **states and sequences**, and describe **interfaces**  
- Build a small **traceability matrix** and state how you would **verify** each requirement  
- Show **operational sense** and **professionalism** in workshop and Thursday sessions  
- Choose a **simple tool** that produces a clear, reviewable artifact (not an ambitious tool stack)

## The early derivation chain (memorize this)

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS (EARS)
   │          │           │              │
 shared    who/why     how people     what the system
 picture   benefit     use it         shall do
```

Typed links (same names used on program artifact graphs):

| Relationship   | From → To              | Meaning |
|----------------|------------------------|---------|
| **derives_from** | Need → Vision         | Stakeholder need is justified by the vision |
| **traces_to**    | Need → Use case       | The need is realized by one or more goal-oriented interactions |
| **allocated_to** | Use case → Requirement | The use case is specified by one or more shall-statements |

**Design / architecture comes later.** We allocate requirements to design elements only after the problem is clear. Starting with a solution is the habit this course breaks.

## Where diagrams fit (structural + behavioral)

Once requirements exist, the chain continues into architecture and behavior. Do **not** draw these in the first weeks.

```text
VISION → NEEDS → USE CASES → REQUIREMENTS (EARS)
   │        │         │              │
   │        │         │              │ allocated_to
   │        │         │              ▼
   │        │         │         ARCHITECTURE / STRUCTURE
   │        │         │         (context, containers, components, deployment)
   │        │         │              │
   │        │         │              │ exercised by
   │        │         │              ▼
   │        │         │         BEHAVIOR
   │        │         │         (state machines + sequence diagrams)
   │        │         │              │
   │        │         │              ▼
   │        │         │         INTERFACES / ICDs
   │        │         │              │
   │        │         │              ▼
   │        │         │         MBSE / FRAMEWORK LITERACY (optional depth)
   │        │         │              │
   │        │         │              ▼
   │        │         │         V&V / Trace
```

| Diagram type | Kind | Module | Role in the chain |
|--------------|------|--------|-------------------|
| **Context diagram** | Structural | se-02 (Stakeholders) + **se-05 Architecture** | System boundary and external actors/systems |
| **Container / layer view** (C4-style) | Structural | **se-05 Architecture** | Major pieces and responsibilities; FRs are **allocated_to** these elements |
| **Component view** | Structural | **se-05 Architecture** | Finer-grained allocation of FRs to modules/services |
| **Deployment view** | Structural | **se-05 Architecture** | VMs/processes/network placement (lab standard) |
| **Package / data sketch** | Structural | **se-05 Architecture** | Code ownership and information structure |
| **State machine** | Behavioral | **se-06 Behavior** | *When* and legal/illegal transitions; must stay consistent with governing FRs |
| **Sequence diagram** | Behavioral | **se-06 Behavior** | *Order* of interactions for a use-case scenario |
| **Interface / ICD view** | Structural + behavioral | **se-07 Interfaces** | Message contracts between the pieces defined in architecture |
| **Framework / MBSE map** | Literacy | **se-11 MBSE & frameworks** | How course artifacts relate to UML/SysML/DoDAF-style products |

**Teaching rule:** Early weeks stay on the left side of the chain (Vision → Requirements). Structural diagrams appear in Architecture; behavioral diagrams appear in Behavior. Both must remain traceable to the requirements they implement.

## Overview activities (first Monday)

These short exercises make the chain concrete and expose the “design-first” trap early.

### 1. Design-First Trap (12–15 min) — recommended opener

1. Facilitator gives a vague problem (example: “We need a better way for FOSC staff to track time and leave”).
2. Pairs have **3 minutes** to sketch a *solution* (UI, features, architecture — whatever they want).
3. Quick share of “cool features.”
4. Reveal: almost no one asked who the stakeholders are, what success looks like, or what is out of scope.
5. Show the course chain and say: “This is exactly the habit we are going to break.”

### 2. Traceability Relay (optional, 12–15 min)

Four sequential roles (whiteboard or sticky notes):

1. **Vision writer** — 2–3 sentences.
2. **Need writer** — must **derives_from** the vision (`As <stakeholder>, we need … so that …`).
3. **Use-case writer** — must **traces_to** the need (actor + goal).
4. **Requirement writer** — must be **allocated_to** the use case (one EARS shall-statement).

At the end the group judges whether the final requirement still supports the original vision. Instant demonstration of why the links matter.

### 3. Failure-Mode Spotting (optional, 8–10 min)

Quick card-sort or bingo with classic SE failure modes (no shared vision, gold plating, untestable “shall,” interface surprise, etc.). Teams mark which modes appear in a short story. Reinforces the language used throughout the course.

## Rhythm (typical week)

| Day | What happens |
|-----|----------------|
| **Monday** | **3–4 hours total:** ~1 hour lecture / walkthrough + 2–3 hours hands-on workshop |
| **Thursday** | Questions, peer feedback, grading, short coaching |

Not every Monday is a new SE lecture. Some weeks focus on **military operations** (ATO planning/execution). Some Thursdays are mostly grading.

## What “good” looks like

We use a **rubric to differentiate performance levels** — so strong candidates stand out clearly:

- **Testable** thinking (can someone prove your requirement?)
- **Clear boundaries** (what is in / out of the system?)
- **Traceability** (requirement → design idea → test)
- **Operational sense** (missions are not video games)
- **Professionalism** (attendance, integrity, coachability)
- **Clear artifacts** (a peer can review them without you in the room)

**Approximate weighting** (SE track — see **Assignments** for the live catalog):

| Area | Share | Notes |
|------|-------|--------|
| Thursday take-homes (one per module) | ~93% | SE-A00 through SE-A10 + A1–A4, A7 |
| Professionalism (A6) | 7% | Attendance, Thursday engagement, peer feedback, integrity |

**Cadence:** each SE module is taught **Monday**. The matching assignment is worked **Monday–Wednesday** and checked **Thursday**. Requirements (A2) is the exception — draft Thursday of the requirements week, final Thursday of the architecture week.

Peer feedback on Thursday is scored under A6 and improves the quality of your artifacts.

## Tools — SEs create artifacts

**Systems engineers are paid for artifacts and decisions under evidence**, not for tool loyalty. A requirement pack, a context diagram, a state chart, an ICD, and an RTM are the product. Tools are how you leave that evidence so others can review, test, and maintain it.

### Course stance (memorize)

1. **Artifact first** — know what good looks like (vision, need, UC, EARS, state, ICD, RTM).  
2. **Simplest clear tool** — prefer the easiest medium that a peer can read without special software. Ambition is in the *thinking*, not in the tool stack.  
3. **Polyglot** — real programs mix markdown, Excel, wikis, Jira, DOORS-class databases, MBSE tools, scripts, and LLMs. You will switch.  
4. **LLMs are tools** — allowed for wording help; **cite** them; ideas and structure must be yours.

### Tool classes (illustrative — not a shopping list)

| Kind of work | Example tools | Typical artifacts |
|--------------|---------------|-------------------|
| Write & structure | Markdown, Word, Confluence / wikis | Vision, needs, ICD text, decision records |
| Tables & traces | Excel / Sheets; enterprise: DOORS, Jama, Polarion | RTM, allocation matrix, req lists |
| Diagrams | Mermaid, PlantUML, draw.io, Visio | Context, C4-style containers, deployment, states, sequences |
| MBSE / system model | Rhapsody, Cameo, Capella *(class of tool)* | Model-based architecture & behavior (see **se-11**) |
| Work tracking | Jira, Azure DevOps, GitHub Issues | Tasks, reviews — not a substitute for SE artifacts |
| Scripting / data | Python, bash | Export checks, data shaping, repeatable reports |
| AI assist | LLMs (ChatGPT, Grok, Copilot, …) | Draft wording only — cite; verify yourself |

**In this course:** markdown + tables + Mermaid/PlantUML + Excel-style RTMs are enough. We name enterprise tools so you recognize them on a program — we do **not** require licenses.

Each later module adds a short **Tools for these artifacts** note with links. Course site tools:

- **Website** — modules, schedule, assignments, submissions  
- **Case study** — SDC Time Tracker → **Systems Engineering** page (linked from Home)  
- **Glossary** — top navigation: **Glossary** (`/glossary`)  
- **Offline reading** — longer modules between Monday and Thursday  

## Ground rules

1. Your own work. You may discuss ideas; you may not submit a peer’s text.
2. Cite sources (including AI assist) if used for wording — *ideas and structure must be yours*.  
   **Example citation:** *Generated initial requirement wording using ChatGPT, 2026.*
3. Be on time for Monday sessions.
4. Ask questions on Thursday — confusion early is better than silent failure.  
   **Contact:** use your instructor during Thursday Q&A, or the course contact posted on **Home**.

## Your first actions

1. **Log in** and open **Selection Criteria**.  
2. Open the **Glossary** (nav bar → Glossary) and skim key terms.  
3. **This week:** **SE-A00** (track plan) and **SE-A01** (failure-mode brief) — assigned Monday, due Thursday.  
4. **Read** **What Is Systems Engineering?** before Thursday.  
5. **Note** **A1** (vision / stakeholders / needs) starts Week 2 Monday.

## Thursday assignment (Week 1)

**SE-A00 — SE Track Plan & Artifact Map** (this module) and **SE-A01** (next module). Both are short briefs. Do not start writing shall-statements yet.

## Further reading

Optional background (free / public). Skim; do not let this replace Monday workshop work.

| Topic | Source |
|-------|--------|
| What systems engineering is | [SEBoK — Systems Engineering Overview](https://sebokwiki.org/wiki/Systems_Engineering_\(glossary\)) |
| Body of knowledge map | [Guide to the Systems Engineering Body of Knowledge (SEBoK)](https://sebokwiki.org/) |
| NASA process overview | [NASA Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/) (PDF available from NASA) |
| Professional society | [INCOSE](https://www.incose.org/) — student / community resources |
| Markdown (artifact writing) | [CommonMark](https://commonmark.org/) / [GitHub Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github) |
| Mermaid diagrams | [Mermaid docs](https://mermaid.js.org/) |
| Course terms | In-app **[Glossary](/glossary)** |

## Next

**What Is Systems Engineering?** — the full derivation chain (including later allocation to design), why SE matters, and classic failure modes.
