# RHEL 7 and Essential Linux Commands

## Learning outcomes

After this module you can:

- Navigate a **RHEL 7** (or compatible) host with confidence  
- Use core **filesystem, process, user, and network** commands  
- Read **logs** and basic **service** status (`systemctl`, `journalctl`)  
- Apply **least privilege** habits (`sudo`, file modes)  
- Document what you ran so integration work is repeatable  

## Why RHEL 7 here

Many program and lab systems still run **RHEL 7** (or CentOS 7 / compatible clones). Commands transfer to RHEL 8/9 with small differences (notably packaging — see the package-management module).

| Admin need | Linux skill |
|------------|-------------|
| Deploy a jar / broker | Paths, users, permissions, services |
| “Is it up?” | Processes, ports, logs |
| Integrate two hosts | Connectivity checks, DNS, firewall basics |
| Evidence for V&V | Commands + outputs you can re-run |

SE link: the **host environment** is part of the system boundary — config and OS packages are design constraints, not afterthoughts.

## Lab assumptions

- Shell: **bash**  
- Privilege: normal user + `sudo` when allowed  
- Distro: **RHEL 7.x** or close clone  
- Always prefer **read-only** discovery before changes  

> **Caution:** On shared lab hosts, do not stop services, open firewall holes, or install packages without instructor approval.

## Survival kit (memorize)

### Where am I / what’s here?

```bash
pwd
ls -la
cd /path && cd -
tree -L 2        # if installed
file some.bin
du -sh *
df -h
```

### Read and search text

```bash
less /var/log/messages
tail -n 50 /var/log/messages
tail -f /var/log/messages      # follow (Ctrl+C to stop)
grep -n "ERROR" app.log
grep -R "jdbc" /etc --include="*.xml" 2>/dev/null | head
```

### Processes and resources

```bash
ps aux | head
ps aux | grep -i java
top                 # or htop if installed
free -m
uptime
```

### Kill carefully

```bash
kill <pid>          # SIGTERM — prefer first
kill -9 <pid>       # SIGKILL — last resort
```

### Network discovery

```bash
ip addr             # or: ifconfig (if net-tools installed)
ip route
hostname -f
ping -c 3 8.8.8.8
curl -I https://example.com
ss -lntp            # listening TCP (RHEL 7 has ss)
# netstat -lntp     # older style, if available
```

### Users, groups, permissions

```bash
id
whoami
sudo -l             # what can I run?
ls -l file
chmod 640 file      # know what this means
chown user:group file   # needs privilege
```

| Mode digit | rwx meaning |
|------------|-------------|
| 7 | rwx |
| 6 | rw- |
| 5 | r-x |
| 4 | r-- |
| 0 | --- |

Order: **owner / group / other** (e.g. `640` = rw- r-- ---).

### Copy, move, archive

```bash
cp -a src dest
mv old new
mkdir -p /opt/ciss/app
tar czf backup.tgz dir/
tar xzf backup.tgz
```

### Finding things

```bash
find /opt -name "*.jar" 2>/dev/null
which java
type java
rpm -q bash         # is package installed? (yum module next)
```

## systemd on RHEL 7 (services)

RHEL 7 uses **systemd**.

```bash
systemctl status sshd
systemctl is-active firewalld
systemctl list-units --type=service --state=running
journalctl -u sshd -n 50 --no-pager
journalctl -xe                  # recent priority issues
```

| Command | Use |
|---------|-----|
| `systemctl status NAME` | Running? failed? last lines |
| `systemctl start/stop/restart NAME` | Change state (privileged) |
| `systemctl enable/disable NAME` | Start on boot |
| `journalctl -u NAME` | Unit logs |

Do **not** restart production-like services in class without permission.

## Firewall (awareness)

RHEL 7 often uses **firewalld**:

```bash
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

Opening ports is an **interface / security** decision — coordinate with networking and leads.

## SELinux (awareness)

RHEL enables **SELinux**. If something “permission denied” despite chmod:

```bash
getenforce
ls -Z /path/to/file     # SELinux context
```

Do not casually `setenforce 0` on shared systems. Escalate with evidence instead.

## Operator discipline

1. **Read before write** — `cat`/`less` configs before editing.  
2. **Copy then edit** — `cp file file.bak.$(date +%F)`.  
3. **One change at a time** — easier to bisect failures.  
4. **Record commands** — lab notebook or script (next: bash).  
5. **Least privilege** — root only when required.  

## Drill (30–40 min)

On a lab host (or VM):

1. Report: hostname, OS (`cat /etc/redhat-release`), kernel (`uname -r`), disk (`df -h`), memory (`free -m`).  
2. List listening ports (`ss -lntp`).  
3. Find whether `java` and `python` exist (`which` / `rpm -q`).  
4. Show last 20 lines of a log you are allowed to read.  
5. Create `~/ciss-lab/notes.txt` with those findings (no secrets).  

Optional: paste a sanitized command list into your Git notes on a `DR-###` branch.

## Integrity

- No scanning or attacking systems outside the lab scope.  
- No password guessing; no disabling security controls for convenience.  
- Do not store classified host details in public repos.

## Further reading

| Topic | Source |
|-------|--------|
| RHEL 7 docs (archive) | [access.redhat.com](https://access.redhat.com/) — search “RHEL 7 system administrator’s guide” |
| systemd | `man systemctl` · `man journalctl` |
| ss / ip | `man ss` · `man ip` |
| Permissions | Search “Linux file permissions chmod tutorial” |

## Next

**Bash programming** — turn repeated commands into safe, reviewable scripts.
