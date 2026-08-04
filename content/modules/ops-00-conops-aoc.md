# Military Ops — CONOPS & Air Operations Center (AOC)

> **Source:** Training lecture provided by military SME —  
> *Concept of Operations (CONOPS) · Air Operations Center (AOC) · Voice Communication Systems*  
> (Frequentis VCS context). Classroom / training use. Unclassified operational concepts only.

## Learning outcomes

- Define **CONOPS** and its place relative to needs and design  
- Describe **AOC** role in the C2 chain  
- Sketch detect→assess **operational workflow**  
- Name major **roles** and **voice/data** communication paths  
- Connect CONOPS language to the SE cascade (vision → needs → use cases → requirements)  

## Learning objectives (from the lecture)

1. Define CONOPS  
2. Understand AOC operations  
3. Communication workflow  
4. Operator responsibilities  

---

## What is CONOPS?

**Concept of Operations (CONOPS)** describes **how a system is used** in the real world.

| CONOPS covers | Why it matters for SE |
|---------------|------------------------|
| Users / operators | Stakeholders and needs |
| Missions and operational concepts | Vision + use cases |
| How people and systems interact | Use cases, sequences, interfaces |

### CONOPS bridges requirements and design

```text
VISION / NEED  →  CONOPS (how ops run)  →  USE CASES  →  REQUIREMENTS  →  DESIGN
```

If you skip CONOPS, requirements often describe software features with no operational story.

### Purpose of CONOPS (lecture)

- Standardize operations  
- Improve readiness  
- Enhance decision-making  
- Increase mission success  

---

## Operational environment

An AOC does not sit alone. Typical information and force elements around it:

| Domain | Examples (training level) |
|--------|---------------------------|
| Sensors | Radar |
| Tactical data | Link 16 |
| EW | Electronic warfare feeds / awareness |
| Intelligence | Intel products supporting ID and intent |
| Weather | Mission planning and safety |
| Higher HQ | Strategic / operational direction |

**SE habit:** each of these is a potential **external system** on your context diagram.

---

## AOC architecture (training sketch)

From the lecture stack:

```text
Strategic HQ
      ↓
     AOC
      ↓
  C2 / TEWA / COP
      ↓
 Frequentis VCS + Link 16
      ↓
   SAM / Aircraft
```

| Layer | Role (plain language) |
|-------|------------------------|
| Strategic HQ | Higher command intent and tasking |
| **AOC** | Air operations hub — plan, monitor, direct |
| C2 / TEWA / COP | Command & control, threat evaluation/weapon assignment, common operational picture |
| Frequentis VCS + Link 16 | Voice communications system + tactical datalink |
| SAM / Aircraft | Effectors / airborne assets that execute |

**TEWA** (Threat Evaluation and Weapon Assignment) and **COP** (Common Operational Picture) are key C2 concepts: prioritize threats and assign responses; share one picture of the air situation.

**Frequentis VCS** in this training context is the **voice communication system** (radios, phones, VoIP, recording, redundancy, emergency calls).

---

## Major components

1. Sensors  
2. C2 system  
3. Voice communications  
4. Data links  
5. Mission planning  

Map these to SE:

| Component | Typical SE artifact |
|-----------|---------------------|
| Sensors / links | Interface ICDs, feed use cases |
| C2 / COP / TEWA | Core system boundary, behavior models |
| Voice (VCS) | Human–system interface + recording/audit NFRs |
| Mission planning | ATO planning use cases (see ATO module) |

---

## Operational workflow (kill chain style)

Lecture sequence:

```text
Detect → Track → Identify → Evaluate → Assign → Communicate → Execute → Assess
```

| Step | Meaning for interns |
|------|---------------------|
| Detect | Something is sensed |
| Track | Continuity over time |
| Identify | Friend / foe / unknown (at training level) |
| Evaluate | Threat significance (TEWA) |
| Assign | Weapon / asset / response |
| Communicate | Voice and/or datalink orders |
| Execute | Shooter / aircraft / SAM acts |
| Assess | Did it work? Update picture |

**SE link:** each arrow can become a **use case** or **sequence**; evaluate/assign often involve **human-in-the-loop** requirements (ties to AIC2 vision principles).

---

## Roles and responsibilities

| Role | Focus (training) |
|------|------------------|
| Operator | Execute assigned C2 / console tasks |
| Supervisor | Oversee operators, escalate, quality of COP actions |
| Commander | Authority and decisions |
| Communication Operator | Voice nets, patches, discipline on VCS |

When writing needs:

```text
As AOC operators,
we need a clear COP and reliable voice paths to effectors,
so that we can complete detect-to-assess actions under time pressure.
```

---

## Frequentis Voice Communication System (VCS)

Capabilities called out in the lecture:

- Radio  
- Telephone  
- VoIP  
- Recording  
- Redundancy  
- Emergency calls  

### Communication flow (lecture)

```text
Radar → C2 → TEWA → Supervisor → Frequentis VCS → SAM / Aircraft
```

**SE note:** Voice is not “just a phone.” It is a **mission-critical interface** with recording, failover, and phraseology procedures — good NFR and IF/THEN requirement material (loss of primary net, emergency call, etc.).

### Voice best practices

- Standard phraseology  
- Read-back  
- Clear communication  
- Record critical traffic  

These become **procedure requirements** or training CONOPS, not only software FRs.

---

## Operational scenarios (for exercises)

1. **Normal mission** — routine detect-to-assess with voice + datalink  
2. **Emergency communications** — alternate paths, emergency call, recording  
3. **Multiple threat response** — TEWA prioritization, concurrent assign/communicate  

**Workshop:** pick one scenario → write 1 need + 2 use cases + 3 EARS requirements (at least one IF/THEN for comms failure).

---

## Cybersecurity (lecture)

- Secure credentials  
- Approved channels only  
- Report incidents  

Trace to NFRs: authentication, authorized voice/data paths, audit of critical actions.

---

## Summary (lecture)

```text
People + Procedures + Technology + Communications = Mission Success
```

## Tie-back to CISS SE Capstone

| SE layer | What to take from this CONOPS |
|----------|-------------------------------|
| Vision | Mission success via people + procedures + tech + comms |
| Needs | Operators, supervisors, commanders, comms operators |
| Use cases | Detect…assess chain; emergency comms; multi-threat |
| Requirements | C2, COP, TEWA, VCS, Link 16 interfaces; HITL on assign |
| Design | Out of scope for this module — architecture later |

## Offline reading

- Full SME deck (repo): `content/reference/CONOPS_AOC_Frequentis_Training_Lecture.pptx`  
- Next: **ATO Planning** (missions, loadout, tankers, timing) builds on AOC as the hub that publishes and monitors tasking.

## Next

**Military Ops — Air Tasking Order (Planning)** — how missions are built before execution.
