# ADMIN-A02 — Safe Admin Bash Script

**Weight:** 15% · **Due:** After admin-02-bash · **Module:** admin-02-bash

## Prompt

Write a **small admin script** that automates a real check or report — not a toy `echo Hello`.

## Suggested scripts (pick one)

- Disk usage report over threshold
- Service health check (active/failed) with non-zero exit on failure
- Log grepping helper for a known error pattern
- User/process inventory for a lab host

## Deliverables

1. **Script file** with `set -euo pipefail` (or justified subset), quoting discipline, and `--help` or usage comment.
2. **Sample run** (stdout/stderr) on a lab host.
3. **Failure demo:** force a failure path; show exit code and message.
4. **Design notes:** args, exit codes, what is *not* automated (and why).
5. Optional: `shellcheck` notes if available.

## Quality bar

- Safe defaults (no `rm -rf` surprises; no unquoted expansions).
- Useful to another admin at 02:00.
- Idempotent or clearly stateful.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| correctness | 15 | Script works; failure path clear |
| safety | 10 | Quoting, set flags, no foot-guns |
| communication | 5 | Help text and notes usable |
