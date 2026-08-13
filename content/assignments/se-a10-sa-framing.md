# SE-A10 — Radar SA Framing Pack (Capstone Preview)

**Weight:** 5% · **Due:** Week 13 Thursday · **Module:** se-10 Capstone Preview  
**Cadence:** Assigned Monday of the preview session. Due Thursday. Unclassified only.

## Prompt

Frame a **classroom radar situational-awareness** problem using the **full SE chain**. This is a **starter pack**, not the later full capstone prototype.

You may invent a lab-scale picture (two feeds, one operator, one supervisor). Do **not** use real classified tracks, sites, or unit tasking.

## Intended problem (teaching)

A small SA capability that:

- Ingests **two** track feeds (e.g. local radar + a second source)
- Presents a **situation picture** to an operator
- Raises **alerts** (zone entry, lost track, or dual-feed conflict)
- Supports **operator** and **supervisor** roles

## Deliverables

1. **Vision** (½ page) + ≥ 2 principles (include human-in-the-loop or similar).
2. **Stakeholders** ≥ 4 and **2 needs** in course grammar, each linked to the vision.
3. **Scope:** ≥ 3 in / ≥ 3 out; one-sentence assumption about feeds (simulated, not live AD).
4. **2 use-case briefs** (actor, goal, main success, ≥ 1 extension each) — e.g. correlate dual-feed tracks; acknowledge a conflict alert.
5. **4 EARS FRs** (must include at least one **WHEN** and one **IF/THEN**) + **2 ACs** in Given/When/Then.
6. **Context diagram** + **one** behavior sketch (state *or* sequence) for the alert/conflict path.
7. **Lightweight feed ICD cover** (one table): 6 fields with **units**; producer/consumer; rate note.
8. **Mini RTM** (4 rows): FR → design idea → verification method.

## Quality bar

- Chain is complete enough that a later capstone can *expand* it, not replace it.
- No classified or unit-sensitive content.
- IF/THEN covers a dual-feed conflict or lost-track path — not only the happy picture.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| chain_completeness | 15 | Vision through RTM present and linked |
| testability | 10 | EARS + ACs + verify method are objective |
| communication | 5 | Unclassified; peer could continue the pack |
