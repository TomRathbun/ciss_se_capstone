# Architecture Frameworks & MBSE Literacy

## Learning outcomes

After this module you can:

- Explain **MBSE** vs document-centric SE in one paragraph  
- Contrast **UML** and **SysML** at a practical level  
- Describe what an **architecture framework** is (DoDAF, MODAF, NAF, UAF)  
- Map **course artifacts** to common framework-style products (e.g. OV-1)  
- Know when a program expects framework views vs when C4/markdown is enough  

**Prerequisite:** Architecture views (se-05), Behavior (se-06), and Interfaces (se-07) — or equivalent familiarity with context/structure, state/sequence, and ICDs.

## Why this module exists

On defense and large enterprise programs you will hear: “Send me the OV-1,” “Is this in the SysML model?,” “We’re doing MBSE.” Interns who only know Mermaid still succeed — if they know **what is being asked** and how it relates to vision, needs, requirements, and tests.

This module is **literacy**, not tool certification. You will not be graded on Cameo proficiency here.

---

## Document-centric SE vs MBSE

| | Document-centric | MBSE (model-based) |
|--|-------------------|---------------------|
| Primary authority | Specs, ICDs, drawings as files | Integrated **model** (plus generated views/reports) |
| Change | Edit many documents; hope traces hold | Change elements and relationships in one model |
| Review | Read Word/PDF packages | Navigate model + selected diagrams |
| Risk | Copy/paste drift between docs | Model skill + tool lock-in; still need clear views for non-modelers |

**MBSE** means the system model is a primary engineering artifact — structure, behavior, requirements links, and sometimes parametrics — not that “we drew a diagram in a model tool once.”

Course stance remains: **artifact first, simplest clear tool.** MBSE is how many programs scale those artifacts.

```text
Vision / needs / UCs / FRs  ──traces──►  Model elements
                              │
                              ├── structure (blocks, components)
                              ├── behavior (states, activities, sequences)
                              └── interfaces & allocations
```

---

## UML vs SysML

| | **UML** | **SysML** |
|--|---------|-----------|
| Origin | Software modeling (OMG) | Systems engineering profile of UML |
| Strength | Classes, components, sequence, state, deployment | Blocks, requirements diagram, parametrics, continuous systems |
| Typical user | Software architects, developers | Systems engineers, integrated HW/SW/ops teams |

**What you already practiced (UML-shaped):**

| Course work | UML-ish diagram |
|-------------|-----------------|
| se-06 state chart | State machine diagram |
| se-06 sequence | Sequence diagram |
| se-05 component / package | Component / package ideas |
| se-05 deployment | Deployment diagram |

**SysML adds (recognize the names):**

| SysML diagram | Intent |
|---------------|--------|
| **Block Definition (BDD)** | Types of blocks and relationships (composition, inheritance) |
| **Internal Block (IBD)** | Parts and connectors *inside* a block |
| **Requirement diagram** | Req elements linked to design/test |
| **Activity diagram** | Flows of control/data (business or system process) |
| **Parametric diagram** | Constraints / engineering analysis (advanced) |
| **Use case diagram** | Actors and goals (overlaps se-03) |

You do **not** need to draw BDD/IBD in this course. Know that “SysML block” ≈ structured system element with ports/interfaces — cousin to your component boxes.

## Thursday assignment

**SE-A11 — Frameworks & MBSE Literacy Brief** (see Assignments). Assigned this Monday. Due Thursday.

Literacy, not Cameo certification. Map **your** artifacts — do not invent DoDAF product codes you cannot explain.

---

## Architecture frameworks (DoDAF, MODAF, NAF, UAF)

An **architecture framework** is a **convention**: named viewpoints and products so large organizations share a vocabulary.

| Framework | Community (simplified) |
|-----------|------------------------|
| **DoDAF** | U.S. Department of Defense architecture framework |
| **MODAF** | UK Ministry of Defence (historical; much migrated toward unified approaches) |
| **NAF** | NATO architecture framework |
| **UAF** | OMG Unified Architecture Framework — consolidates ideas from the above for broader use |

Frameworks organize views such as:

| Concern | Example product codes (DoDAF-flavored names you will hear) |
|---------|----------------------------------------------------------------|
| Operational concept | **OV-1** High-level operational concept graphic |
| Operational nodes / needlines | **OV-2** Operational resource flow |
| Activities | **OV-5** Operational activity model |
| Systems and their links | **SV-1** Systems interface description |
| Functions | **SV-4** Systems functionality description |
| Standards | **StdV** / technical standards views |

Exact product lists differ by framework version. **Memorize the idea**, not every code.

### OV-1 in plain language

An **OV-1** is the “movie poster” of the operational architecture: one picture stakeholders use to orient — forces, sensors, C2, links — without software class names.

You already met this spirit in **UAE Military Context** / CONOPS materials (layered AD, radars, C2). That is operational architecture storytelling — the same job as a context + mission graphic.

```text
OV-1 style picture
  └── answers: what mission world looks like
Context diagram (se-05)
  └── answers: what is inside our system boundary for *this* product
```

Both are useful; they are not interchangeable.

---

## Map: course artifacts → framework-style products

| Course artifact | Framework-style cousin | Notes |
|-----------------|------------------------|-------|
| Vision + CONOPS narrative | Operational concept / OV-1 story | Shared picture |
| Context diagram | Operational context / boundary | System vs world |
| Stakeholder needs + UCs | Operational activities & use | Who does what |
| EARS requirements + RTM | Requirements views / matrices | Trace still required in MBSE |
| Container + component | System / service structure views | SV-ish |
| Deployment (VMs) | Resource / deployment views | Where it runs |
| State + sequence | Behavioral views | Dynamic architecture |
| ICD | Interface products | Contracts at boundaries |
| Design decision (ADR) | Architecture decision records | Often outside formal view codes |

**Takeaway:** frameworks rename and formalize work you already do. They rarely replace the need for clear requirements and tests.

---

## When programs require what

| Situation | Typical expectation |
|-----------|---------------------|
| Intern / course project | Markdown, Mermaid/PlantUML, Excel RTM |
| Software service team | C4 + ADRs + OpenAPI/ICD |
| Defense enterprise / C2 program | Framework views (OV/SV/…) + often SysML/MBSE tool |
| Mixed hardware-software system | SysML structure + interfaces + safety/assurance artifacts |

If a lead asks for “the OV-1,” deliver a **high-level operational graphic** with a short legend — not a class diagram.

If they ask for “the SysML model,” clarify **which views** and **tool** — then use the program standard, not a personal Mermaid-only repo, as the authority.

---

## Tool classes (recognition)

| Class | Examples | Role |
|-------|----------|------|
| Lightweight diagram | Mermaid, PlantUML, draw.io | Course default |
| MBSE / SysML | Cameo, Rhapsody, Capella | Model authority on many programs |
| Requirements DB | DOORS, Jama, Polarion | Spec & trace databases |
| Enterprise architecture | Sparx EA, UAF-capable suites | Framework repositories |

Course rule: **recognize the class**; do not pirate licenses or fake tool experience on a résumé.

---

## Workshop (20 min)

1. Take your **context** or **container** diagram from se-05.  
2. Label each external node as operational actor, external system, or data source.  
3. Write three bullets: “If a program lead asked for an **OV-1**, I would add/remove …”  
4. Write one bullet: “If they asked for **SysML IBDs**, I would need …”  
5. Optional: map one FR → component (se-05) → verification idea (se-08) and say whether that chain lives in documents, a requirements DB, or an MBSE tool on a real program.

---

## Integrity

- Do not claim framework or Cameo expertise you do not have.  
- Do not reproduce controlled program architecture products into public Git.  
- Public OV-1-style teaching graphics only from allowed open sources.

## Further reading

| Topic | Source |
|-------|--------|
| MBSE | [SEBoK — Model-Based Systems Engineering](https://sebokwiki.org/wiki/Model-Based_Systems_Engineering) |
| SysML | [OMG SysML](https://www.omgsysml.org/) |
| UML | [OMG UML](https://www.uml.org/) |
| DoDAF | Search “DoDAF Viewpoints” on official U.S. DoD CIO / guidance sites (version matters) |
| UAF | [OMG UAF](https://www.omg.org/uaf/) |
| C4 (software views) | [c4model.com](https://c4model.com/) |
| Course practice | **se-05 Architecture Views**, **se-06 Behavior**, **se-07 Interfaces** |
| Operational pictures | **UAE Military Context**, **CONOPS & AOC** |

## Next

**Verification, Validation & Traceability** — prove the architecture and behavior satisfy the requirements, with an RTM others can execute.
