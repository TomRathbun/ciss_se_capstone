# SW-A02 — Ticket → Branch → MR Workflow

**Weight:** 10% · **Due:** After sw-02-bitbucket-jira · **Module:** sw-02-bitbucket-jira

## Prompt

Practice the **same discipline** as work (Jira DR → Bitbucket PR → Nexus) using **CISS lab tools** (Issue/stand-in ticket → GitLab MR).

## Deliverables

1. **Ticket** with key `DR-###` (GitLab Issue or written stand-in): title, problem statement, acceptance note (what “done” means).
2. **Branch** named with that key; link to remote branch.
3. **Merge Request** into `main` (or lab default): description maps ticket → changes → how to test.
4. **Review checklist** you would apply as reviewer (≥ 6 items: style, tests, secrets, scope, etc.).
5. **Nexus / artifacts paragraph:** where a built jar would be published at work vs what you use in the lab.
6. Screenshot or URL of the MR (open or merged).

## Quality bar

- Ticket key appears on branch and MR.
- MR description is reviewable without reading every file.
- No secrets in the branch.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| workflow_fidelity | 15 | Ticket → branch → MR chain intact |
| review_quality | 10 | Checklist would catch real defects |
| communication | 5 | MR usable by a peer reviewer |
