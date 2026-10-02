# SW-FA04 — Service conversation sketch

**Time box:** 2 hours. Stop at 2 hours and turn in what you have.
**Due:** Week 4 Thursday morning, before the Admin lecture
**Module:** sw-f04-services
**Weight:** 8% of this track’s intern-selection score.

## Prompt

Draw the shape of a small lab system. You may preview PRSAS names (radar.input) but do not invent classified fields.

## Deliverables

1. **Diagram:** at least producer, broker, consumer, database, client.
2. **ICD table** (six fields): name, meaning, who Tx, who Rx, rate or ‘on change’, drop policy.
3. **DB sentence:** what is stored vs what is only in the live message.
4. **VM note:** which processes share a VM vs need their own (your call, with a reason).
5. **Owner map:** SE / SW / NET / ADMIN for each box.

## Quality bar

ICD is a contract, not a Java class. No Docker-first default. Owners do not all say ‘software.’

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| completeness | 10 | All required artifacts present |
| accuracy | 10 | Technically right at intern level |
| communication | 5 | A peer can grade it in five minutes |
