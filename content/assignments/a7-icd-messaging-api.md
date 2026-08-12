# A7 — Messaging ICD + API ICD (partial)

**Weight:** 5% · **Due:** Week 5 Thursday · **Module:** se-07 Interfaces

## Prompt

Produce **two** partial ICDs for a small **lab situational-awareness** context (unclassified, invented data is fine).

### Part A — Messaging ICD (radar-style)

Assume a **system track** message on a lab LAN (ASTERIX-*style* thinking; you may invent field names if you mark them **teaching-only**).

Deliver:

1. Cover sheet (name, version, type=messaging, provider, consumer, purpose, owner).  
2. **Message content** table — at least **8 fields** (name, meaning, type/units note).  
3. **Tx/Rx matrix** — at least **4 nodes** (e.g. tracker, display, recorder, gateway) × this message: Tx / Rx / process / drop.  
4. **Rate table** — at least **3 rows** (periodic update, begin/end or event, heartbeat or status).

### Part B — REST API ICD

Same domain: a **client** queries or commands a **track service**.

Deliver:

1. Cover sheet (type=API, base URL fictional, versioning note).  
2. **Operations table** — at least **3** operations (method, path, purpose).  
3. For **one** operation: parameters, success response (code + body fields), and **at least 4 error** rows (HTTP + app code + when).  

## Quality bar

| Expect | Avoid |
|--------|--------|
| Clear process vs drop | “Everyone processes everything” with no policy |
| Units or encoding notes on position/time fields | Unitless lat/lon “numbers” |
| Errors tied to real failure modes | Only `500 Generic error` |
| Teaching fields labeled if not from a real edition | Claiming unofficial fields are official ASTERIX |

## Rubric

| Dimension | Max | Description |
|-----------|-----|-------------|
| messaging_completeness | 10 | Content + Tx/Rx + rates present and coherent |
| api_completeness | 10 | Operations + detailed op + errors present |
| communication | 5 | Tables readable; version/owner clear |

## Notes

- Markdown or Word/Excel exports OK.  
- OpenAPI YAML optional extra for Part B — not required.  
- Cite AI if used for wording.
