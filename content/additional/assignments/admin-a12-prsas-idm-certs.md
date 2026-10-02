# ADMIN-A12 — PRSAS Identity & Certificates

**Phase:** capstone · **Weight:** 35% of capstone-ADMIN · **Due:** After admin-12 · **Module:** admin-12-prsas-idm-certs

## Prompt

Give the picture a **directory** and a **lab CA** AMQ will trust.

## Deliverables

1. Principal/group/HBAC table (daemon, operators, no-root-daemon).
2. IPA or OpenLDAP architecture note (what is live vs stub).
3. Cert inventory: CA, AMQ server, any client certs; SANs listed.
4. `openssl` inspect + `s_client` to 61617 (or expected failure if AMQ not up).
5. Three trust-failure scenarios (expiry, name, chain).
6. Key handling: where private keys live; confirmation they are **not** in Git.

## Quality bar

- SAN matches the hostname SW will type.
- No private keys in the submission.
- Stub identity is labelled and ticketed, not hidden.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| identity | 15 | Sensible principals and access |
| tls | 10 | Real inspect evidence; SAN thinking |
| communication | 5 | SW/NET can trust the bundle |
