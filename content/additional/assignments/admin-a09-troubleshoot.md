# ADMIN-A09 — Structured Troubleshooting Case

**Weight:** 10% · **Due:** After admin-09-troubleshooting · **Module:** admin-09-troubleshooting

## Prompt

Solve (or carefully re-analyze) a real lab problem using the **symptom → hypothesis → test** method. If nothing is broken, use an instructor inject or a controlled self-break you can restore.

## Deliverables

1. **Symptom statement:** who, what, when, scope, last-known-good.
2. **Timeline.**
3. **Hypotheses ranked** (≥ 3) with how each could be tested **read-only first**.
4. **Tool evidence:** use at least **four** of: `grep`, `tail`/`less`, `journalctl`, `ps`, `ss` (paste excerpts).
5. **Change log:** every change you made (one at a time).
6. **Resolution + prevention** notes.
7. **Evidence pack** summary a peer could continue from.

## Quality bar

- No shotgun restarts without a hypothesis.
- Evidence is primary.
- Prevention is specific.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| method | 15 | Structured, hypothesis-driven |
| tooling | 10 | Right tools, good excerpts |
| communication | 5 | Handoff-quality pack |
