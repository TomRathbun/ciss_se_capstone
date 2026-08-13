# Capstone Preview — Radar Situational Awareness

## Learning outcomes

After this module you can:

- Frame a **multi-feed radar SA** problem with the **same SE chain** used all term  
- Write unclassified vision, needs, use cases, and EARS for a **two-feed picture**  
- Name the hard cases (lost track, dual-feed conflict, zone entry) as **IF/THEN** work  
- Sketch a **feed ICD** with units and rates before anyone codes a parser  
- Produce a **starter pack** another intern could expand — not a throwaway slide deck  

## Status

This is a **real framing week**, not a teaser slide. The later prototype / full capstone (feeds, scoring, UI) opens after this pack exists. **SE-A10** is the Thursday artifact.

Do **not** use real classified tracks, site names, unit tasking, or controlled ICDs.

## Why this problem

Radar situational awareness is the program-shaped problem this course has been aiming at:

| Course habit | SA version |
|--------------|------------|
| Shared **vision** | Operator + supervisor see one defensible picture |
| **Needs** | Who needs what from the picture, so that what mission outcome? |
| **Use cases** | Correlate feeds, acknowledge conflict, supervise alerts |
| **EARS** | WHEN a plot arrives… IF two feeds disagree… |
| **Architecture** | Ingest, correlate, display, alert — allocated FRs |
| **Behavior** | Alert / ack / conflict states; sequence for a conflict |
| **ICD** | Each feed is a contract (units, rate, drop policy) |
| **RTM / V&V** | How you would test 5.99 vs the rule — same as BEOD |

ETAS taught the *discipline* on a living timekeeper. SA is the *same chain* with sensors and operators.

## Intended lab problem (unclassified)

Specify a **classroom SA** capability that:

1. Ingests **two** track feeds (e.g. local radar + a second source — ADS-B-style or a second simulated radar)  
2. Presents a **situation picture** to an **operator**  
3. Raises **alerts** when a rule fires: zone entry, lost track, or **dual-feed conflict**  
4. Supports a **supervisor** who can acknowledge / override display of an alert  

Feeds may be **simulated files or lab messages**. You are not connecting to live air-defense sensors.

### Teaching picture

```text
Feed A (local radar-style) ──┐
                             ├──►  Correlator / picture  ──► Operator display
Feed B (second source)     ──┘              │
                                            └──► Alert rules ──► Supervisor
```

If you cannot say **what “same track” means** (ID? position gate? time?), you do not have a requirement yet — you have a hope.

## Integrity (non-negotiable)

| Allowed | Not allowed |
|---------|-------------|
| Invented lab tracks, fictional lat/lon, teaching field names | Real tracks, real sites, real ATO / unit tasking |
| Public EUROCONTROL / ATC vocabulary (ASTERIX *style*) | Controlled program ICDs or screenshots |
| Human-in-the-loop on engagement-adjacent decisions | Auto-engage / auto-prosecute as a use case |

If you are unsure whether a fact is open-source, **leave it out**.

## Apply the chain (starter example)

Use this only as a **shape**. Your SE-A10 pack must be yours.

### Vision (sketch)

A lab situational-awareness picture that fuses two unclassified feeds so an operator can see tracks, conflicts, and simple alerts in seconds — with a supervisor in the loop — without pretending the classroom system is a live air-defense C2.

**Principles (examples):** human-in-the-loop on conflict disposition; units and time on every feed field; no silent drop of a second-source track.

### Need (course grammar)

> **As** <u>**lab operators**</u>,  
> **we need** a single picture that shows when two feeds disagree on the same track,  
> **so that** we do not brief a false position as truth.

### Use cases (names)

| UC-ID | Name | Extension that will become IF/THEN |
|-------|------|-------------------------------------|
| UC-COR-01 | Correlate dual-feed tracks | Feeds disagree beyond gate |
| UC-ALR-01 | Acknowledge conflict alert | Already acked; supervisor override |

### EARS (examples — write your own IDs)

- **WHEN** feed A reports a track update, the SA system **shall** display that track with source, time, and position **units**.  
- **IF** feed A and feed B associate to the same track **AND** position difference exceeds the correlation gate, **THEN** the SA system **shall** raise a dual-feed conflict alert and **shall not** silently pick one feed.  

### Architecture / behavior / ICD (minimum)

- **Context:** operator, supervisor, feed A, feed B, SA system.  
- **State or sequence:** conflict raised → displayed → acked (or expired).  
- **Feed ICD cover:** ≥ 6 fields with **units**; producer/consumer; update rate.  
- **Mini RTM:** each FR → design idea → I / A / D / T.

## Monday workshop (builds SE-A10)

Work in pairs on **your** starter pack (not a shared class fiction unless the instructor assigns one).

1. **15 min** — Vision + 2 principles + 4 stakeholders.  
2. **15 min** — 2 needs in grammar; 2 UC names with one extension each.  
3. **20 min** — 2 EARS (one WHEN, one IF/THEN) + 1 AC.  
4. **15 min** — Context sketch + 6-field feed table with units.  
5. Peer swap: can they restate your vision in 60 seconds? Can they test your IF/THEN?

Finish the remaining deliverables Monday–Wednesday. Thursday is review / grade.

## Thursday assignment

**SE-A10 — Radar SA Framing Pack** (see Assignments). Assigned this Monday. Due this Thursday.

This pack is the **seed** for the later full capstone. A strong pack is one a later intern can *expand*, not replace.

## How to prepare if this week is later

If ops and ETAS already ran:

1. Steal your **SE-A09** bullets (ICD units, reject paths, AC alignment).  
2. Reuse ops vocabulary (picture, track, alert) without copying classified CONOPS.  
3. Keep A2-quality EARS — do not regress to “the UI shall be intuitive.”

## Instructor

Grade **SE-A10** on the catalog rubric (chain completeness, testability, communication). Do not grade a full prototype until the later capstone problem statement is published.

> **Reminder:** If you generate any wording with an AI tool, add an in-text citation (e.g., *Generated with ChatGPT, 2026*). The chain and numbers must be yours.

## Tools for these artifacts

Same course stance: markdown + tables + Mermaid. A feed ICD is a **table**, not a parser.

| Artifact | Simplest clear tool |
|----------|---------------------|
| Vision / needs / UCs / EARS | One markdown pack |
| Context / alert state | Mermaid |
| Feed ICD | Markdown or Excel table with units |
| Mini RTM | Excel / markdown table |

## Further reading

| Topic | Source |
|-------|--------|
| Situational awareness | Endsley, “Toward a Theory of Situation Awareness in Dynamic Systems” — search author + title |
| Multi-sensor fusion (intro) | [SEBoK](https://sebokwiki.org/) + survey articles on “sensor fusion architecture” |
| Civil surveillance analogue | [FAA — Surveillance](https://www.faa.gov/air_traffic/technology) |
| Messaging ICDs | Course **Interfaces & ICDs** · public ASTERIX Cat 021 / 062 pages |
| Ops picture vocabulary | **UAE Military Context** OV-1 (open-source only) |
| Living-system habits | **Case Study — ETAS** (SE-A09 steal-list) |

## Next

When the full capstone opens: feeds, scoring, and (optional) a thin UI. Until then, this pack plus remaining **military ops** work is the close of the SE spine.
