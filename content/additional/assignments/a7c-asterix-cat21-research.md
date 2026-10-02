# Stretch A7c — Research: ASTERIX Category 021 ICD summary

**Not separately graded.** Optional stretch after **A7** (se-07). Thursday grade for the ICD week is **A7** only.

## Prompt

Locate the **public** EUROCONTROL materials for **ASTERIX Category 021** (ADS-B target reports) and write a **reader’s summary** as if briefing a teammate who must consume Cat 021 on a lab feed.

### Required sources (start here)

- EUROCONTROL CAT021 publication page:  
  [CAT021 — ADS-B Target Reports](https://www.eurocontrol.int/publication/cat021-eurocontrol-specification-surveillance-data-exchange-asterix-part-12-category-21)  
- Optionally: ASTERIX Part 1 (general encoding) and Cat 021 Appendix A (Reserved Expansion Field) from the same site family.  
- Do **not** use controlled or proprietary program ICDs.

### Deliverables

1. **Bibliographic header**  
   - Document title(s)  
   - Edition / version and date **you actually used**  
   - URL(s)  
   - Access date

2. **One-page (or ~400–600 word) summary** covering:  
   - Purpose of Cat 021 (what problem the messages solve)  
   - How it relates to **Cat 062** (sensor report vs system track — your understanding from public text)  
   - High-level message organization (what a “category” and data items mean at overview level)  
   - At least **five** example data concepts/items the spec addresses (e.g. position, time, identity — name them as the public doc does)  
   - Why **edition** matters for implementers

3. **ICD-shaped tables (your extraction, not a full copy of the standard)**  
   - Mini **content** table: ≥5 rows (item/concept, role in ADS-B report)  
   - Mini **consumer notes**: who might Tx vs Rx Cat 021 in a generic ATM architecture (ground station / ADS-B receiver vs tracker vs display) — reasoned from public descriptions, labeled as inference if not explicit

4. **Integrity statement**  
   - Confirm only public sources  
   - No export of restricted material  
   - List any AI tools used and for what

## Rubric

| Dimension | Max | Description |
|-----------|-----|-------------|
| source_quality | 10 | Correct public docs; edition and URL cited |
| understanding | 10 | Purpose, Cat 021 vs 062, edition importance clear |
| communication | 5 | Summary and tables usable by a peer |

## Notes

- Skimming a 100+ page PDF is expected; **do not** paste large copyrighted excerpts — summarize.  
- If a PDF download requires accepting EUROCONTROL terms, follow them.  
- This trains **reading real ICDs**, not memorizing bit fields.
