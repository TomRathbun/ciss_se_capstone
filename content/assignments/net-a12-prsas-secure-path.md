# NET-A12 — PRSAS Firewalls & IPsec

**Phase:** capstone · **Weight:** 40% of capstone-NET · **Due:** After net-12 · **Module:** net-12-prsas-secure-path

## Prompt

Implement (or fully specify) **zones, policies, and two IPsec tunnels**.

## Deliverables

1. Zone / host-inbound table per site.
2. Policy set list matching NET-A11 allow-list.
3. NAT decision (probably none) with rationale.
4. IKE/IPsec proposal matrix; `st0` addressing; routes.
5. Evidence: `ike sa` / `ipsec sa` **or** expected-output table.
6. PSK redacted. Dedicated-encryptor note if applicable.

## Quality bar

- Route-based vs policy-based is explicit.
- No permit-any “for the demo.”
- Same proposal both tunnels unless a box forces a documented downgrade.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| design | 15 | Zones, policies, both tunnels |
| ops_discipline | 10 | Redaction, red/black, commit safety |
| communication | 5 | Sets a peer could commit-check |
