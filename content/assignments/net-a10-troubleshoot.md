# NET-A10 — Layered Junos Troubleshooting Case

**Weight:** 5% · **Due:** After net-10-troubleshoot · **Module:** net-10-troubleshoot

## Prompt

Run (or carefully reconstruct) one fault with the **layered method**. Prefer a real lab issue or instructor inject. If nothing is broken, use the module’s HTTPS-vs-ping mini-case **and** apply the same template to a **second** hypothetical on *your* fabric (IPsec or VLAN).

## Deliverables

1. **Symptom statement:** who, source/dest IP, port/app, when, last-known-good.  
2. **Freeze:** version, `interfaces terse` highlights, last commit, cluster/VC if any.  
3. **Path sketch** with the layer you will test first.  
4. **Hypotheses (≥ 3)** ranked, each with a **read-only** test.  
5. **Evidence:** excerpts from at least **five** commands spanning **at least two** layers (L1–L2, L3, POL, OVLY).  
6. **Change log** (even “none — escalate”).  
7. **Cause, fix, prevention.**  
8. **Honesty note** if you used a capture or the worked example rather than a live break.

## Quality bar

- No shotgun reboot or global session clear.  
- Application port is tested when the symptom is an app.  
- Redaction correct (PSK, extra-lab prefixes).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| method | 15 | Ordered layers; hypothesis-driven |
| tooling | 10 | Right Junos shows; useful excerpts |
| communication | 5 | Handoff-quality pack |
