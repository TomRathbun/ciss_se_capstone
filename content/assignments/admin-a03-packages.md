# ADMIN-A03 — Package & Artifact Hygiene

**Weight:** 10% · **Due:** After admin-03-package-management · **Module:** admin-03-package-management

## Prompt

Show you can work across **OS packages** and **language/org artifacts** without polluting systems — including when the guest **cannot reach the public internet**.

## Deliverables

1. **RPM/dnf evidence:** on RHEL 10.2, query an installed package with `dnf info` / `rpm -q`; show version; explain one dependency or `dnf provides` for a binary you care about. Record `dnf --version`.
2. **Language ecosystem note (pick two of: pip/uv, npm, Maven):** where installs land, what not to commit, how you isolate projects.
3. **Nexus paragraph:** role of an org artifact hub vs public PyPI/npm/Maven Central.
4. **Change mini-plan:** install or upgrade *one* lab package (or dry-run): pre-check, command, verify, rollback idea.
5. **Bad practice hit list:** ≥ 5 anti-patterns (global `chmod 777`, `curl | sudo bash` without review, committing `node_modules`, `gpgcheck=0` to “make the ISO work”, leaving a CDN repo enabled on an air-gapped guest, etc.).
6. **Air-gap plan:** one page. Guest cannot reach cdn.redhat.com. How do you install `tree` (or one lab package) with DNF 5? Name the source (program Nexus / 10.2 ISO / USB bag), the repo file or `dnf install --disablerepo='*'` command, and how GPG still checks. Explicitly say why `dnf offline reboot` is the wrong tool for this.

## Quality bar

- Distinguishes system packages vs app-level deps.
- Rollback thinking present.
- Air-gap plan uses a real source (ISO / USB repo / Nexus) and does **not** disable GPG or confuse `dnf offline reboot` with “no internet.”
- No blind copy-paste install from untrusted sources.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| coverage | 15 | OS + language + Nexus thinking |
| change_control | 10 | Plan with verify/rollback |
| communication | 5 | Clear anti-pattern list |
