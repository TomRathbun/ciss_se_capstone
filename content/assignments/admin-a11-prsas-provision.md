# ADMIN-A11 — PRSAS VM Provision Pack

**Phase:** capstone · **Weight:** 30% of capstone-ADMIN · **Due:** After admin-11 · **Module:** admin-11-prsas-provision

## Prompt

Provision (or fully specify) the **PRSAS guest set** from a golden image.

## Deliverables

1. Inventory: hostname, role, vCPU/RAM/disk, port group, IP.
2. Golden image notes (OS, chrony, ssh, firewalld, SELinux enforcing).
3. Clone procedure (UI steps or PowerCLI/govc).
4. Evidence from ≥ 2 live VMs (`hostnamectl`, `ip -br a`, `timedatectl`) **or** honest bench constraint.
5. Snapshot plan (when, who may revert).
6. What you did **not** put on the radar VLAN.

## Quality bar

- Sizes are justified, not maximal.
- SELinux left enforcing.
- IPs match NET-A11 or teaching defaults with a note.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| inventory | 15 | Complete, placed on correct VLANs |
| image_discipline | 10 | Golden image + snapshots thought through |
| communication | 5 | SW can SSH from the table |
