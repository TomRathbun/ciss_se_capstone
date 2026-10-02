# Interfaces & ICDs

> **When:** Week 8 · Monday afternoon · Masdar
> **Who:** All interns (SE is mandatory for the full program)
> **Tomorrow morning:** [se-da03-icd — Partial messaging + API ICD](/assignments/se-da03-icd) (~2 hours), due **Week 8 Tuesday morning**.

## Learning outcomes

After this afternoon you can:

- Write a messaging ICD slice (content, Tx/Rx, rates)
- Write an API ICD slice (ops, params, errors)
- Refuse unofficial ASTERIX claims

## Why this afternoon exists

Parsers written without ICDs become folklore. CISS-TEACH-1 is the lab contract.

## Teach

Messaging ICD: fields, units, who sends, who receives, rate, late/drop policy, version.

API ICD: operations, parameters, errors, auth.

PRSAS teaching payload is **JSON labeled CISS-TEACH-1**, ASTERIX-*like*, not edition-certified binary Cat 062. Read se-12 for the frozen fields.

## In-class exercise (30–40 min)

Fill six fields of radar.input (from CISS-TEACH-1). Write one API op for bulk load from Postgres.

## Additional lesson

The long-form original is archived as **[se-07-interfaces](/modules/se-07-interfaces)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **se-da03-icd** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
