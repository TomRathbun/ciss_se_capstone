# SE-A14 — PRSAS MBSE Pack & Track Schema

**Phase:** capstone · **Weight:** 35% of capstone-SE · **Due:** Week 16 Thursday · **Module:** se-14

## Prompt

Produce the **design baseline**: sequence, hybrid track lifecycle, logical components, allocation, and Postgres DDL.

## Deliverables

1. **Sequence** for ingest → correlate → persist → publish → display, plus **one `alt`** (CONFLICT or broker down).
2. **Hybrid state** for the system track with triggers, guards, activities; numbers for N and T.
3. **Logical component** diagram and **allocation table ≥ 6 FRs**.
4. **`schema.sql`** — `system_track` + `track_history`; Mode 3/A indexed; roles note (daemon vs client).
5. **Gate formula** for fallback correlation (units).
6. **Consistency note** — one paragraph: how sequence, state, and schema agree.

## Quality bar

- SW can implement the daemon from this pack without a meeting.
- State vs status is not mixed.
- No official-ASTERIX binary claim unless you actually cite an edition and still keep CISS-TEACH-1.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| model_quality | 15 | Sequence + hybrid state + components coherent |
| schema | 10 | Implementable DDL; key and history exist |
| allocation | 5 | FRs land on real elements |
