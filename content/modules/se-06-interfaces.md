# Interfaces & ICDs

## Learning outcomes

- Identify external interfaces  
- Write a lightweight **interface description**  
- Explain why formula/layout changes are interface changes  

## Interfaces are contracts

When two systems (or human + system) meet, you need agreement on:

| Topic | Questions |
|-------|-----------|
| Purpose | Why does this exchange exist? |
| Parties | Who is producer / consumer? |
| Content | What data / commands? |
| Format | File, API, radio voice, message type? |
| Timing | On demand, daily, real-time? |
| Errors | What if missing / late / invalid? |
| Security | Who is allowed? |

That agreement is the heart of an **ICD** (Interface Control Document), even if yours is one page.

## ETAS examples

| Interface | Producer → Consumer | Notes |
|-----------|---------------------|--------|
| TEMPO import | Manager enters TEMPO hours → ETAS | Weekly Monday-keyed hours |
| FOSC Excel export | ETAS → Program / contract package | Sheet names, column M variance |
| SMTP email | ETAS → employee/manager mail | Optional if SMTP configured |
| Human PIN UI | Employee → ETAS | Session cookie after verify |

### Teaching example — Discrepancy Tracker

The contract workbook expects:

- Week tabs named like `Time Keeping Sheet (WkN)`  
- Variance in **column M**  
- Tracker cells = INDEX/MATCH + row offset  

If you move variance to column N, that is an **interface change**: code, tests, and training must update together.

## Lightweight ICD template (use this)

```text
Interface name:
Provider:
Consumer:
Operation / data:
Format / schema:
Frequency:
Success criteria:
Error handling:
Security / auth:
Owner:
```

## Workshop

Write a mini-ICD for either:

- TEMPO weekly import, or  
- FOSC weekly export  

## Next

**V&V and traceability** — proving you did the right things.
