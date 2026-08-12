# Troubleshooting Methodology and Essential Tools

## Learning outcomes

After this module you can:

- Follow a **repeatable troubleshooting method** under pressure  
- Separate **symptom, cause, and fix** in notes and tickets  
- Use **grep, tail, less, journalctl, ps, ss** fluently  
- Build evidence packs others can trust  
- Know when to **stop changing** and escalate  

## Why methodology beats guessing

Random restarts sometimes “work” and teach nothing. Programs need:

| Outcome | How methodology helps |
|---------|----------------------|
| Faster MTTR | Narrow search space |
| Fewer regressions | One change at a time |
| Handoff quality | Next person can continue |
| V&V / audit | Reproducible steps |

SE link: troubleshooting evidence is often the raw material for **defect reports** and verification records.

---

## A practical method (use every time)

```text
1. Define the symptom          (who, what, when, scope)
2. Establish the timeline      (last good / first bad)
3. Freeze the scene            (capture state before big changes)
4. Form hypotheses             (ranked, testable)
5. Test with smallest probe    (read-only first)
6. Change one thing            (record it)
7. Verify + watch for side effects
8. Document resolution         (and prevention)
```

### Symptom template

| Field | Example |
|-------|---------|
| Service / VM / host | `msct-app-02` |
| User-visible error | “Login hangs 30s then 502” |
| Scope | One user / one host / whole cluster |
| Started | 2026-08-11 14:10 GST after deploy |
| Recent changes | Package update, cert renewal, network ACL |

### Golden rules

1. **Read before write** — logs and status before restart.  
2. **One change at a time** — otherwise you cannot attribute the fix.  
3. **Prefer reversible actions** — config bak, snapshot only when policy allows.  
4. **Preserve evidence** — copy logs with timestamps; do not truncate production logs casually.  
5. **Time sync matters** — misaligned clocks destroy timelines (and Kerberos).  

---

## Tool deep dive

### `tail` and `less` — watching and paging logs

```bash
tail -n 100 /var/log/messages
tail -f /var/log/messages              # follow (Ctrl+C)
tail -n 50 -f /var/log/app/*.log      # last 50 then follow

less /var/log/messages                # navigate: /search  n  N  g  G  q
less +F /var/log/messages             # less in follow mode (Ctrl+C then q)
```

| Habit | Why |
|-------|-----|
| Start at the **time of failure** | Not only “latest line” |
| Capture **before** rotation | Logs disappear |
| Prefer `journalctl` on systemd units | Structured, time-bounded |

```bash
journalctl -u sshd --since "2026-08-11 14:00" --until "14:30"
journalctl -u myapp -n 100 --no-pager
journalctl -p err..alert -n 50
```

---

### `grep` — finding signal in noise

```bash
grep ERROR /var/log/app/app.log
grep -n "OutOfMemory" /var/log/app/app.log          # line numbers
grep -i timeout /var/log/app/*.log                   # case-insensitive
grep -R "jdbc:postgresql" /opt/app/conf 2>/dev/null
grep -E "ERROR|FATAL|Exception" app.log | tail
grep -v "healthcheck" access.log | grep 500         # exclude then match
```

| Option | Use |
|--------|-----|
| `-n` | Line numbers for tickets |
| `-i` | Case-insensitive |
| `-R` / `-r` | Recursive |
| `-E` | Extended regex |
| `-A` / `-B` / `-C` | Context lines after/before/around |
| `-v` | Invert match |
| `--include="*.log"` | Limit file types |

```bash
grep -n -C 3 "NullPointerException" app.log
```

Pipe patterns:

```bash
journalctl -u myapp --since today | grep -i error | tail -n 40
ps aux | grep -i java | grep -v grep
```

---

### Processes — `ps`, `top`, and friends

```bash
ps aux | head
ps aux | grep -i java
ps -ef | grep postgres
ps aux --sort=-%mem | head           # top memory
ps aux --sort=-%cpu | head           # top CPU
```

| Column (`ps aux`) | Meaning |
|-------------------|---------|
| USER | Effective user |
| PID | Process ID |
| %CPU / %MEM | Utilization snapshot |
| VSZ / RSS | Virtual / resident memory |
| STAT | State (R, S, Z zombie, D uninterruptible) |
| START / TIME | Start time / CPU time |
| COMMAND | Args — gold for “which jar?” |

```bash
top
# or: htop
free -m
uptime
vmstat 1 5
```

Kill discipline:

```bash
kill <pid>           # SIGTERM first
# wait, re-check
kill -9 <pid>        # last resort; can corrupt data
```

---

### Network path — quick probes

```bash
ss -lntp                 # listening sockets + PIDs
ss -antp | head
ip addr
ip route
ping -c 3 target
curl -vI https://target:8443/health
```

Map failure: DNS → route → TCP → TLS → app HTTP → app logic.

---

### Disk and files

```bash
df -h
du -sh /var/log/* | sort -h | tail
ls -ltr /var/log/app/              # newest last
find /opt/app -name "*.log" -mtime -1
```

---

## Building an evidence pack

Before escalating or closing:

1. Host / VM identity and time (`date`, `timedatectl`)  
2. Symptom statement (template above)  
3. Relevant log **excerpts** with timestamps (not 50 MB dumps)  
4. `systemctl status` for involved units  
5. Resource snapshot (`uptime`, `free -m`, `df -h`)  
6. Changes already tried (and result of each)  
7. Hypothesis still open  

Sanitize secrets: passwords, tokens, personal data.

---

## Anti-patterns

| Anti-pattern | Better |
|--------------|--------|
| Restart first | Capture status + logs, then restart if justified |
| Change three configs at once | One variable |
| “It works on my VM” without versions | Compare package/build IDs |
| Paste entire logs into chat | Curated excerpts + path on server |
| Clear logs to free space mid-incident | Rotate / compress; preserve failure window |

---

## Drill (45 min)

1. Pick a local log file; extract the last 20 lines containing `error` (case-insensitive) with line numbers.  
2. Show the top five processes by memory.  
3. List listening TCP ports with processes (`ss -lntp`).  
4. Write a symptom statement for a fictional “NFS mount hangs on login.”  
5. Produce a mini evidence pack outline (7 bullets) for that incident.  

## Integrity

- Do not run destructive tests on shared systems to “see what breaks.”  
- Do not exfiltrate full production logs off authorized channels.  
- Credit teammates’ findings; do not hide failed attempts in the ticket.  

## Further reading

| Topic | Source |
|-------|--------|
| grep | `man grep` |
| journalctl | `man journalctl` |
| ps | `man ps` |
| ss | `man ss` |
| SRE / ops practice | Your program incident runbooks |

## Next

**Documentation procedures and trouble tickets** — writing so the next person (and future you) can act.
