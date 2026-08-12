# Documentation Procedures and Trouble Tickets

## Learning outcomes

After this module you can:

- Write **clear, actionable** trouble tickets  
- Keep **runbooks and change notes** that others can execute  
- Distinguish **incident, request, change, and problem** records  
- Apply **evidence and sanitization** rules  
- Close work with **resolution notes** that prevent repeats  

## Why documentation is an admin skill

If it is not written down, the system only works while you are awake. Selection-relevant admins:

| Habit | Result |
|-------|--------|
| Precise tickets | Faster routing and fewer ping-pong messages |
| Runnable runbooks | Night-shift can execute without heroics |
| Change records | Bisect regressions after deploys |
| Resolution notes | Same incident does not recur weekly |

SE link: operational docs and tickets often feed **V&V evidence**, configuration baselines, and lessons learned.

---

## Work item types (know which you are writing)

| Type | When to use |
|------|-------------|
| **Incident** | Something is broken or degraded *now* |
| **Service request** | Access, new account, standard install |
| **Change** | Planned modification (window, risk, backout) |
| **Problem** | Root-cause track for recurring incidents |

Using “incident” for a new-user request hides real outages. Use the right type when the tracker supports it (Jira, ServiceNow, etc.).

---

## Anatomy of a good trouble ticket

### Title

Bad: `Help` · `DB issue` · `URGENT!!!`  
Good: `Postgres appdb: cannot connect from msct-app-02 after 14:10 GST`

Pattern: **object + symptom + scope/time**

### Body template

```markdown
## Summary
One or two sentences.

## Impact
Who/what is affected; user-visible behavior; severity.

## Environment
- Host / VM:
- Service / unit:
- Version / build (if known):
- Timezone for all times:

## Timeline
- Last known good:
- First observed:
- Relevant changes (deploy, cert, network, package):

## Evidence
- Commands run and key outputs (sanitized)
- Log excerpts with timestamps
- Screenshots only if text is insufficient

## What we tried
| Step | Result |
|------|--------|
| Restarted unit X | No change |

## Ask
What you need from the assignee (investigate / change window / access).
```

### Severity (program-specific — align to local definitions)

| Level | Typical meaning |
|-------|-----------------|
| Critical | Outage of core capability; safety/mission impact |
| High | Major feature down; no workaround |
| Medium | Degraded or partial; workaround exists |
| Low | Cosmetic, single user, or non-prod |

Do not inflate severity to jump the queue — it destroys trust.

---

## Evidence standards

| Include | Exclude |
|---------|---------|
| Hostnames, service names, versions | Passwords, tokens, private keys |
| Timestamps with timezone | Entire multi-GB log files |
| Exact error strings | Unrelated personal data |
| Sanitized command output | Secrets in screenshots |

```bash
# Good excerpt style in a ticket
# 2026-08-11T14:12:03+04:00 msct-app-02 journalctl -u myapp -n 20
# ... NullPointerException at com.example.Service.start(Service.java:88)
```

Link to log paths on controlled systems when the audience has access: “Full log: `/var/log/myapp/app.log` on `msct-app-02`.”

---

## Change documentation (short form)

Even small changes deserve a note:

| Field | Example |
|-------|---------|
| Why | Cert expiring 2026-08-15 |
| What | Replaced `app.example.com` cert on `lb-01` |
| Where | Path / vCenter object / package NEVRA |
| When | 2026-08-12 02:00–02:20 GST |
| Backout | Revert to `cert-old.pem` from `/root/backup/` |
| Verify | `curl -vI https://app.example.com` → 200; expiry date check |
| Ticket / DR | `DR-1234` / `CHG012345` |

Pair with Git history when config is in repo form (Infrastructure as Code).

---

## Runbooks

A runbook is a **procedure a trained peer can follow** under stress.

| Section | Content |
|---------|---------|
| Purpose | When to use this runbook |
| Preconditions | Access, tools, health checks before starting |
| Steps | Numbered, copy-pasteable commands |
| Expected output | What “good” looks like |
| Backout | How to undo |
| Escalation | Who/what if step N fails |

Bad runbook: “Restart the cluster until it works.”  
Good runbook: exact unit names, order, verification after each step.

Store runbooks where on-call can find them (wiki, Git, approved share) — not only in personal notes.

---

## Updates and closure

### While work is open

- Time-stamped comments: what you saw, what you did, next step  
- Reassign with context, not silence  
- If blocked, state the blocker explicitly  

### Resolution note

```markdown
## Resolution
Root cause: exhausted Postgres `max_connections` after pool misconfig on app v2.3.1.
Fix: reduced app pool size; added alert on connection count.
Verify: error rate back to baseline 15:40 GST; no recurrence 24h.
Follow-up: problem ticket for pool defaults in template.
```

Close only when **verify** is done — not when you hope it is fixed.

---

## Communication tone

| Prefer | Avoid |
|--------|-------|
| Facts and timestamps | Blame (“dev broke it”) |
| Specific asks | “Please look ASAP” with no data |
| “Blocked on X” | Silence for two days |
| Own mistakes in the record | Hiding failed changes |

---

## Drill (40 min)

1. Rewrite this title into a good one: `nfs broken`.  
2. Draft a full ticket body for: “Users cannot kinit after clock skew on lab host.”  
3. Write a 6-step runbook outline for “remount NFS share X on client Y.”  
4. List five items that must never appear in a ticket comment.  
5. Write a resolution note for a fictional disk-full incident that was fixed by log rotation + root-cause ticket.  

## Integrity

- No classified or export-controlled detail in tools that lack proper accreditation.  
- No credentials in tickets, wiki pages, or Git.  
- Do not open public issues for internal infrastructure.  

## Further reading

| Topic | Source |
|-------|--------|
| Program tracker | Local Jira / ServiceNow field guide |
| ITIL-inspired types | Incident vs problem vs change (conceptual) |
| Writing for operators | Your team’s wiki style guide |
| Related module | **Troubleshooting methodology** |

## Next

Return to **track overview** or deepen a prior module with lab time. New admin modules land in `content/catalog.yaml` as the path grows.
