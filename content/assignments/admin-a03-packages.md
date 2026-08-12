# ADMIN-A03 — Package & Artifact Hygiene

**Weight:** 10% · **Due:** After admin-03-package-management · **Module:** admin-03-package-management

## Prompt

Show you can work across **OS packages** and **language/org artifacts** without polluting systems.

## Deliverables

1. **RPM/yum evidence:** query an installed package; show version; explain one dependency or what provides a binary you care about.
2. **Language ecosystem note (pick two of: pip/uv, npm, Maven):** where installs land, what not to commit, how you isolate projects.
3. **Nexus paragraph:** role of an org artifact hub vs public PyPI/npm/Maven Central.
4. **Change mini-plan:** install or upgrade *one* lab package (or dry-run): pre-check, command, verify, rollback idea.
5. **Bad practice hit list:** ≥ 5 anti-patterns (global `chmod 777`, `curl | sudo bash` without review, committing `node_modules`, etc.).

## Quality bar

- Distinguishes system packages vs app-level deps.
- Rollback thinking present.
- No blind copy-paste install from untrusted sources.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| coverage | 15 | OS + language + Nexus thinking |
| change_control | 10 | Plan with verify/rollback |
| communication | 5 | Clear anti-pattern list |
