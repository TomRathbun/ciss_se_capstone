# SE-A01 — What Is SE? Failure-Mode Brief

**Weight:** 5% · **Due:** Week 1 Thursday · **Module:** se-01 What Is Systems Engineering?  
**Cadence:** Assigned Monday. Offline reading + this brief Monday–Wednesday. Due Thursday.

## Prompt

Prove you can explain SE, walk the **early** derivation chain, and map a public failure to a **missing artifact**.

Use **only public, unclassified** sources. Cite URLs.

## Deliverables

1. **One-paragraph definition** of systems engineering in your own words (≤ 120 words). A non-engineer should understand it.
2. **Chain walk for a daily app** you use (banking, maps, chat, campus badge, …) — **not** a design:

   | Layer | Your artifact (one sentence each) |
   |-------|-----------------------------------|
   | Vision | |
   | Need (`As …, we need …, so that …`) | |
   | Use case (name + actor + goal) | |
   | One EARS shall | |
   | One **design** choice, labeled *design — not a requirement* | |

3. **Aerospace (or Therac-25) case map** — pick **one** case from the module table:

   | Field | Your answer |
   |-------|-------------|
   | Case | |
   | Public source (URL) | |
   | What went wrong (4–6 lines) | |
   | Course failure mode (from se-01 list) | |
   | Missing or weak artifact (vision, need, UC extension, EARS IF/THEN, ICD, state, validation, authority) | |
   | What that artifact would have forced into the open | |

4. **Trace sentence:** write one sentence that uses the course link names: *need **derives_from** vision; need **traces_to** use case; use case **allocated_to** requirement.* Apply it to *your* daily-app example (not the aerospace case).

## Quality bar

- Layers are not mixed (no “shall” in the vision; no UI widget as a need).
- The case map cites a real public source — not a memory of a documentary.
- Design is explicitly labeled so it cannot be mistaken for a requirement.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| literacy | 10 | Accurate SE definition and chain |
| case_analysis | 10 | Failure mapped to a real missing artifact |
| communication | 5 | Tables a peer can grade in 5 minutes |
