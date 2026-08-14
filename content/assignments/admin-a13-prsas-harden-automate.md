# ADMIN-A13 — Harden & Automate

**Phase:** capstone · **Weight:** 35% of capstone-ADMIN · **Due:** After admin-13 · **Module:** admin-13-prsas-harden-automate

## Prompt

Lock the guests and make rebuild **repeatable**.

## Deliverables

1. firewalld (or nft) rules vs NET allow-list — diff resolved.
2. SELinux: `getenforce`, plus one port/boolean you set.
3. auditd / journal access note for the daemon user.
4. Ansible **or** PowerCLI: inventory + one idempotent role (AMQ or daemon host).
5. Runbook: “from golden image to first SW login.”
6. What is **not** automated (and why).

## Quality bar

- `setenforce 0` is a fail unless a dated exception exists.
- Playbook does more than ping.
- Secrets stay out of Git.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| hardening | 15 | Host firewall + SELinux + audit thought |
| automation | 10 | Idempotent, useful role |
| communication | 5 | Runbook SW-12 can follow |
