# What SE is

> **When:** Week 1 · Monday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [se-fa01-what-se-is — SE definition and failure map](/assignments/se-fa01-what-se-is) (~2 hours), due **Week 1 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Explain systems engineering in one paragraph a non-engineer can use
- Name the early chain: Vision → Needs → Use cases → Requirements
- Spot the intern failure mode: jumping to design
- Say what an artifact is (owner, version, date)

## Why this afternoon exists

Every intern on CISS will sit in a room with software, network, and admin work. If you cannot say what problem we are solving, those rooms build the wrong thing. This afternoon is the shared language — not a specialty school.

## Teach

**Systems engineering** is the discipline of making sure we understand the real-world problem, capture what the system must do, design something that can be built and tested, integrate the pieces, and prove we met the need — across hardware, software, people, and process.

It is not “drawing diagrams.” Diagrams are tools. The product is **decisions under evidence**, recorded as **artifacts**.

### Early chain (memorize this)

```text
VISION  →  NEEDS  →  USE CASES  →  REQUIREMENTS
 shared     who/why    how people     what the system
 picture    benefit    use it         shall do
```

| Link | From → To | Meaning |
|------|-----------|---------|
| **derives_from** | Need → Vision | The need is justified by the vision |
| **traces_to** | Need → Use case | The need is realized by a goal-oriented interaction |
| **allocated_to** | Use case → Requirement | The use case is specified by shall-statements |

**Design comes later.** Starting with a solution is the most common intern mistake. Architecture, states, and ICDs wait until the problem is clear.

### Artifacts

Every artifact has an **owner**, a **date**, a **version**, and a **classification** (for us: unclassified). A slide with no owner is not an artifact. A secret sketch in a notebook is not an artifact.

### Why programs fail (the list you will reuse)

| Failure mode | Missing artifact |
|--------------|------------------|
| Built the wrong thing | Vision / needs |
| Nobody agrees who it is for | Stakeholders |
| Happy path only | Use-case extensions |
| “It should be fast” | Testable requirement + AC |
| Two teams, two interfaces | ICD |
| “We tested it” with no mapping | RTM / V&V |

Use **public** failure stories (Therac-25, Mars Climate Orbiter units, 737 MAX MCAS as public reporting). Do not invent classified ones.

## In-class exercise (30–40 min)

In pairs: pick a daily app (maps, badge, banking). Write one sentence each for vision, need, use case, and a shall. Label one design choice *design — not a requirement*. Swap and mark mixed layers.

## Hold for later

Architecture views, state machines, ICDs, MBSE frameworks, and the PRSAS problem. Week 5 opens the project.

## Tomorrow morning

Do **se-fa01-what-se-is** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
