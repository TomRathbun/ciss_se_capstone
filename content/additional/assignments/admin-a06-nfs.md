# ADMIN-A06 — NFS Export / Mount Worksheet

**Weight:** 10% · **Due:** After admin-06-nfs · **Module:** admin-06-nfs

## Prompt

Document an NFS share end-to-end (lab real or fully specified design if mounts are restricted).

## Deliverables

1. **Share design table:** server path, client mountpoint, version (v3/v4), options (`rw`/`ro`, `sec=`), who needs access.
2. **Server side:** example `exports` line + how you would export/refresh (`exportfs` notes).
3. **Client side:** mount command/fstab sketch + `df`/`mount` verification.
4. **UID map risk:** one paragraph on numeric UID mismatch symptoms.
5. **Failure matrix (≥ 3 rows):** permission denied, stale file handle, firewall — check commands.
6. If you cannot mount in lab: still complete design + what evidence you would capture for a ticket.

## Quality bar

- Auth flavor (`sys` vs `krb5`) is chosen deliberately.
- Firewall/port thinking present for the version chosen.
- No “chmod 777 to make NFS work” as the solution.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| design | 15 | Coherent export/mount design |
| ops_checks | 10 | Verification + failure matrix |
| communication | 5 | Ticket-ready worksheet |
