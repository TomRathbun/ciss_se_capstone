# SE-A15 — Virtualization Comparison & Lessons-Learned

**Phase:** capstone · **Weight:** 30% of capstone-SE · **Due:** Week 17 Thursday · **Module:** se-15

## Prompt

Compare the **VM baseline** to a **two-component container PoC** and write the close-out report.

## Deliverables

1. **Test card** signed off with SW/ADMIN (scenario, host class, fault).
2. **Results table** — start time, RSS/CPU, recover, step count. Medians, not single magical runs.
3. **Lessons-learned** with the seven sections in se-15.
4. **Numbered recommendations** with owner tracks.
5. **Migration verdict** on the daemon (yes / not yet / no) and why.
6. **What you did not measure** (honest).

If minikube/Docker is unavailable, submit the card + constraint + a paper estimate labelled **unverified**.

## Quality bar

- Same TLS posture both sides, or a labelled limitation.
- No “containers are always better” without numbers.
- Unclassified logs only.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| evidence | 15 | Fair, labelled measurements or honest gap |
| judgment | 10 | Recommendations a program lead could act on |
| communication | 5 | Report a hiring panel can skim |
