# ADMIN-A01 — RHEL/Linux Discovery Lab

**Weight:** 10% · **Due:** After admin-01-rhel7-linux · **Module:** admin-01-rhel7-linux

## Prompt

On a lab Linux host (RHEL-class preferred), produce an **evidence pack** that proves you can discover system state safely.

## Deliverables

1. **Host identity sheet:** hostname, OS release, kernel, uptime, primary IP(s).
2. **Command evidence** (paste outputs, redact secrets) for: filesystem (`df -h` or similar), processes (`ps` top consumers), users/groups relevant to you, listening ports (`ss`/`netstat`), service status (`systemctl status` on 2 services).
3. **Logs:** one `journalctl` (or `/var/log`) excerpt you used to answer “what happened recently?”
4. **Awareness notes:** SELinux mode (if present) and firewall state — what you observed, not a lecture rewrite.
5. **Risk list:** 3 things you would *not* run on a shared host without approval.

## Quality bar

- Read-only first; no destructive “fixes.”
- Outputs are labeled so a peer can re-run the same checks.
- Redaction is correct (passwords, tokens, personal data).

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| discovery | 15 | Broad, correct evidence pack |
| safety | 10 | Non-destructive; good redaction |
| communication | 5 | Labeled, reproducible |
