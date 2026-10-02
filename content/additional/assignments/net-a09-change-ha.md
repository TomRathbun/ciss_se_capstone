# NET-A09 — Change Plan & HA Vocabulary

**Weight:** 5% · **Due:** After net-09-ha-change · **Module:** net-09-ha-change

## Prompt

Write a **change plan** for a small, realistic SRX policy add, and show **HA vocabulary** for whatever is actually in the rack.

## Deliverables

1. **Baseline habit:** which commands you capture *before* `configure` (list).  
2. **Change plan** for: add `junos-https` (or instructor app) from USERS to a named server — window, `show | compare` expectation, `commit check`, **`commit confirmed`**, verify (session **and** app port), backout (`rollback 1` vs wait).  
3. **Commit comment** you would use (ticket-style).  
4. **HA vocabulary:**  
   - If chassis cluster: `show chassis cluster status` interpretation (RG0/RG1, `reth` vs child IFL).  
   - If not clustered: say so, and still define control link, fabric, RG0, `reth` in your own words.  
   - If EX VC present: one paragraph on split-VC (do not power-cycle).  
5. **Three changes** that require instructor + console on this bench.

## Quality bar

- Verify is not ping-only if the change is HTTPS.  
- No unsupervised failover.  
- Plan is executable in 10 minutes.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| change_control | 10 | Baseline, confirmed commit, verify, backout |
| operational_judgment | 10 | HA vocabulary; what not to touch |
| communication | 5 | Plan a peer could run |
