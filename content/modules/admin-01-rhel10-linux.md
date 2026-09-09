# RHEL 10.2 and Essential Linux Commands

## Learning outcomes

After this module you can:

- Navigate a **RHEL 10.2** (or compatible Rocky/Alma 10) guest with confidence  
- Use core **filesystem, process, user, and NetworkManager** commands  
- Read **logs** and **service** status (`journalctl`, `systemctl`)  
- Query and install OS packages with **DNF 5** (`dnf`, not `yum`)  
- Apply **least privilege** habits (`sudo`, file modes, SELinux, firewalld/nft)  
- Translate **RHEL 7 muscle memory** into the 10.2 equivalents so old runbooks do not break the lab  
- Document what you ran so integration work is repeatable  

## Why RHEL 10.2 here

CISS labs now run **RHEL 10.2** guests under vSphere/ESXi (or a binary-compatible clone such as Rocky Linux 10). RHEL 7 reached end of maintenance in June 2024. Commands you memorized on RHEL 7 still *look* familiar — systemd, `ss`, SELinux — but several daily tools are gone or renamed. Teaching 10.2 without the delta produces intern tickets that say `yum: command not found` and `ifcfg-eth0 does not exist`.

| Admin need | Linux skill on 10.2 |
|------------|---------------------|
| Deploy a jar / broker | Paths, users, permissions, systemd units |
| “Is it up?” | `systemctl`, `journalctl`, `ss`, `podman` (not Docker) |
| Integrate two hosts | `nmcli`, DNS, firewalld (nft backend), TLS |
| Evidence for V&V | Commands + outputs you can re-run |

SE link: the **host environment** is part of the system boundary — OS release, crypto policy, and package versions are design constraints, not afterthoughts.

> **Instructor note:** Spend the first 15 minutes on the delta table below. Interns who “already know Linux” fail this module on RHEL 7 habits, not on `ls`.

## Lab assumptions

- Shell: **bash**  
- Privilege: normal user + `sudo` when allowed  
- Distro: **RHEL 10.2** (kernel 6.12, systemd 257) or close clone  
- Identity of the box: `cat /etc/os-release` — look for `VERSION_ID="10.2"` (or `10`)  
- Always prefer **read-only** discovery before changes  

> **Caution:** On shared lab hosts, do not stop services, open firewall holes, or install packages without instructor approval.

---

## Teach this first — RHEL 7 muscle memory vs RHEL 10.2

Print this table. Put it on the projector. Interns keep it in their lab notebook.

| Job | RHEL 7 (do **not** type this) | RHEL 10.2 (type this) | What breaks if you use the old one |
|-----|-------------------------------|------------------------|------------------------------------|
| Who am I running? | `cat /etc/redhat-release` | `cat /etc/os-release` **and** `/etc/redhat-release` | You miss `VERSION_ID`, ID_LIKE, and CPE |
| Packages | `yum install tree` | `sudo dnf install -y tree` | `yum` is a thin DNF 5 wrapper; teach `dnf`. Repos live in `/etc/yum.repos.d/` still |
| Package info | `yum info httpd` | `dnf info httpd` | Same idea; DNF 5 output is structured differently |
| What owns this file? | `rpm -qf $(which sshd)` | `rpm -qf $(command -v sshd)` / `dnf provides /usr/sbin/sshd` | `which` is optional; `command -v` is POSIX |
| Network config | `/etc/sysconfig/network-scripts/ifcfg-*` | `/etc/NetworkManager/system-connections/*.nmconnection` | **network-scripts are gone.** `ifup eth0` fails |
| Bring a NIC up | `ifup eth0` / `service network restart` | `nmcli con up <name>` / `nmcli device connect <dev>` | `network.service` does not exist |
| Addresses | `ifconfig` | `ip -br addr` / `nmcli device show` | `ifconfig` is not installed (`net-tools` is not default) |
| Listening ports | `netstat -lntp` | `ss -lntp` | `netstat` is not installed |
| Firewall | `iptables -L` / firewalld-iptables backend | `sudo firewall-cmd --list-all` (nftables backend) | `iptables-nft-services` is **deprecated in 10.2**. Do not write raw iptables runbooks |
| Time sync | `ntpd` / `ntpq` | `chronyc tracking` / `timedatectl` | `ntp` package is gone; Kerberos dies if clocks drift |
| Python | `python` → 2.7 | `python` / `python3` → 3.12+ (AppStream 3.14) | Python 2 is **gone**. Shebang `#!/usr/bin/python` must be 3 |
| Java (OS) | OpenJDK 8 | OpenJDK 21 LTS; AppStream OpenJDK 25 | Java 8 is not the OS default. Program Java 8 lives in a documented alternative if needed |
| Containers | Docker (extras) | **Podman** | `docker` is not the lab default. `podman run` / `podman ps` |
| Init remnants | `chkconfig`, `/etc/init.d/` | `systemctl enable --now` | `chkconfig` is gone |
| Identity join knobs | `authconfig` | `authselect` + SSSD | `authconfig` is gone |
| Logs | `/var/log/messages` first | `journalctl -b` first; rsyslog optional | `/var/log/messages` may not exist |
| cgroups | v1 | **v2 only** | Old Docker/java heap recipes that poke `/sys/fs/cgroup/memory/` fail |
| Crypto | OpenSSL 1.0.2, TLS 1.0 still around | OpenSSL 3.5, crypto-policies, **PQC (ML-KEM) in OpenSSH** | Old `ssl_protocols TLSv1` configs fail. `update-crypto-policies --show` |
| Hostname | `hostname` only | `hostnamectl` | Persist hostname via systemd, not `/etc/sysconfig/network` |

**Hard teaching rule:** if a blog, old ticket, or program runbook says `yum`, `ifconfig`, `chkconfig`, `service network`, `ntpd`, or `iptables -A`, rewrite it on 10.2 *before* you paste it into a lab VM.

```text
RHEL 7  ──Leapp──►  RHEL 8  ──Leapp──►  RHEL 9  ──Leapp──►  RHEL 10.2
There is NO in-place path from 7 → 10. Lab images are built fresh (golden image),
not upgraded in place. See admin-11 (PRSAS provisioning).
```

RHEL 10.2 itself (May 2026) adds, on top of RHEL 10.0:

- Kernel **livepatch** support  
- OpenSSH / libssh **ML-KEM post-quantum** key exchange (FIPS mode)  
- PostgreSQL **18**, MariaDB 11.8, Python **3.14** AppStream, Node.js 24, OpenJDK 25  
- Image Mode (`bootc`) fleet download-without-apply  
- Default `/boot` size **2 GiB** (was 1 GiB — golden images must match)  
- Optional CLI assistant (`rhel-system-roles` / Lightspeed; `goose` in Extensions) — **not** a substitute for evidence in this course  
- `iptables-nft-services` and `ipset` **deprecated** — stay on firewalld  

---

## Survival kit (memorize)

### Where am I / what’s here?

```bash
pwd
ls -la
cd /path && cd -
tree -L 2        # install with: sudo dnf install -y tree
file some.bin
du -sh *
df -hT           # 10.2 default root is XFS
cat /etc/os-release
uname -r         # expect 6.12.x on 10.2
hostnamectl
```

### Read and search text

```bash
journalctl -b -n 50 --no-pager          # this boot, last 50
journalctl -p err..alert -n 50 --no-pager
less +G /var/log/messages               # only if rsyslog is installed
tail -n 50 /var/log/secure              # may be a journald symlink on some images
grep -n "ERROR" app.log
grep -R "jdbc" /etc --include="*.xml" 2>/dev/null | head
```

Prefer `journalctl` over hunting files. Unit logs live in the journal even when `/var/log/messages` is empty.

### Processes and resources

```bash
ps aux | head
ps aux | grep -i java
ps aux --sort=-%mem | head
top                 # or htop if installed
free -h             # 10.2 `free` defaults to human units; -h is still fine
uptime
```

### Kill carefully

```bash
kill <pid>          # SIGTERM — prefer first
kill -9 <pid>       # SIGKILL — last resort
```

### Network discovery (NetworkManager + iproute2)

```bash
ip -br addr
ip route
nmcli device status
nmcli connection show
hostname -f
ping -c 3 8.8.8.8
curl -I https://example.com
ss -lntp            # listening TCP + processes
# Do NOT reach for ifconfig / netstat.
```

Persistent config is a **keyfile**, not `ifcfg-*`:

```bash
ls /etc/NetworkManager/system-connections/
# Edit with nmcli, not a text editor, unless you know the keyfile syntax.
sudo nmcli con show <name>
sudo nmcli con mod <name> ipv4.addresses 10.20.30.40/24
sudo nmcli con mod <name> ipv4.gateway 10.20.30.1
sudo nmcli con mod <name> ipv4.method manual
sudo nmcli con up <name>
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
command -v java
type java
rpm -q bash
dnf provides /usr/bin/ss          # which package owns this path?
```

### Flags in the survival kit

Every clustered flag in the examples above is in this table. Do not leave interns decoding `ss -lntp` by guesswork.

| Example | Decode |
|---------|--------|
| `ls -la` | **l**ong listing, **a**ll (including dotfiles) |
| `tree -L 2` | **L**evels — depth 2 |
| `du -sh` | **s**ummary of this path, **h**uman sizes |
| `df -hT` | **h**uman sizes, filesystem **T**ype (10.2 root is XFS) |
| `journalctl -b -n 50 --no-pager` | this **b**oot, last **n** 50 lines, do not invoke `less` |
| `journalctl -p err..alert` | **p**riority from err through alert |
| `tail -n 50` | last **n** 50 lines |
| `grep -n` | print line **n**umbers |
| `grep -R` | **R**ecursive |
| `ps aux` | BSD form: all users, with CPU/MEM |
| `ps aux --sort=-%mem` | sort by memory, highest first (`-` = descending) |
| `kill -9` | SIGKILL — last resort (default `kill` is SIGTERM) |
| `ip -br addr` | **br**ief, one line per NIC |
| `ss -lntp` | **l**istening, **n**umeric ports, **t**cp, **p**rocess/PID |
| `ping -c 3` | **c**ount 3, then stop |
| `curl -I` | headers only (HTTP HEAD) |
| `chmod 640` | owner rw-, group r--, other --- (table above) |
| `cp -a` | **a**rchive — recurse and preserve mode, owner, timestamps, links |
| `mkdir -p` | create **p**arents; no error if the directory exists |
| `tar czf` / `tar xzf` | **c**reate / e**x**tract, g**z**ip, **f**ile |
| `find -name` | match basename against glob |

---

## systemd on RHEL 10.2 (services)

RHEL 10.2 uses **systemd 257**. The verbs you learned on RHEL 7 still work. The *units* and cgroup layout changed.

```bash
systemctl status sshd
systemctl is-active firewalld NetworkManager chronyd
systemctl list-units --type=service --state=running
journalctl -u sshd -n 50 --no-pager
journalctl -xe --no-pager
systemctl cat sshd                 # show the unit file actually in use
```

| Command | Use |
|---------|-----|
| `systemctl status NAME` | Running? failed? last lines |
| `systemctl start/stop/restart NAME` | Change state (privileged) |
| `systemctl enable --now NAME` | Start now **and** on boot (prefer this over separate enable + start) |
| `systemctl disable --now NAME` | Stop and don’t start on boot |
| `journalctl -u NAME` | Unit logs |

Do **not** restart production-like services in class without permission.

cgroup **v2** is the only hierarchy. If a Java/JBoss note tells you to write `/sys/fs/cgroup/memory/memory.limit_in_bytes`, that is RHEL 7. On 10.2 the knobs are under the unified tree (`memory.max`). Prefer systemd unit `MemoryMax=` instead of poking sysfs.

---

## DNF 5 (packages) — preview of the next module

```bash
dnf --version
rpm -q bash
dnf info chrony
dnf list installed | head
sudo dnf install -y tree
sudo dnf upgrade -y tree
sudo dnf remove -y tree
dnf history
dnf needs-restarting -r          # reboot needed after glibc/kernel?
ls /etc/yum.repos.d/
```

| Habit | Why |
|-------|-----|
| Type `dnf`, not `yum` | Course standard on 10.2 |
| Read `dnf info` before install | Size, repo, version |
| Don’t disable GPG checks | Supply-chain safety |
| Record `dnf history` | Evidence for the ticket |

Program hosts may point at **internal mirrors / Nexus**. If `dnf` fails, check repo URLs and subscription/mirror access — same class of problem as Maven + Nexus.

---

## Firewall (firewalld + nftables)

RHEL 10.2 firewalld uses the **nftables** backend. `iptables -L` is not a teaching command here; `iptables-nft-services` is deprecated in 10.2.

```bash
sudo firewall-cmd --state
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --list-all
sudo nft list ruleset | head     # awareness only; do not hand-edit
```

Opening ports is an **interface / security** decision — coordinate with networking and leads. Persistent:

```bash
# Example only — do not run on shared lab without approval
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## SELinux (enforcing is the lab default)

RHEL 10.2 enables **SELinux** in enforcing mode on the golden image. If something is “permission denied” despite chmod:

```bash
getenforce
ls -Z /path/to/file     # SELinux context
ausearch -m avc -ts recent   # if auditd is running
```

Do not casually `setenforce 0` on shared systems. Escalate with evidence instead. `fapolicyd` may also block execution of unexpected binaries — another 10.x control RHEL 7 did not run by default.

---

## Time, crypto, identity (awareness)

```bash
timedatectl
chronyc tracking                 # NOT ntpq
update-crypto-policies --show    # DEFAULT / FUTURE / …
update-ca-trust extract          # after dropping a CA into /etc/pki/ca-trust/source/anchors/
authselect current               # NOT authconfig
```

RHEL 10.2 OpenSSH speaks **ML-KEM** hybrid key exchange. Old clients that only offer `ssh-rsa` / SHA-1 may fail to connect. Lab jump hosts should be 10.2-current; if a legacy tool cannot connect, collect `ssh -vvv` evidence rather than weakening `CRYPTO_POLICY`.

---

## Operator discipline

1. **Read before write** — `cat`/`less`/`nmcli con show` before editing.  
2. **Copy then edit** — `cp file file.bak.$(date +%F)`.  
3. **One change at a time** — easier to bisect failures.  
4. **Record commands** — lab notebook or script (next: bash).  
5. **Least privilege** — root only when required.  
6. **Rewrite RHEL 7 runbooks** — never paste `yum` / `ifcfg` / `chkconfig` onto 10.2.

---

## Drill (35–45 min)

On a lab RHEL 10.2 host (or VM):

1. Report: hostname (`hostnamectl`), OS (`/etc/os-release` — quote `VERSION_ID`), kernel (`uname -r`), disk (`df -hT`), memory (`free -h`).  
2. Prove NetworkManager is the network stack: `nmcli device status` and `ls /etc/NetworkManager/system-connections/`. Confirm **no** `/etc/sysconfig/network-scripts/ifcfg-*`.  
3. List listening ports (`ss -lntp`).  
4. Package literacy: `dnf --version`, `rpm -q bash`, `command -v python3`, `java -version` (or “not installed”).  
5. Show last 20 journal lines from this boot (`journalctl -b -n 20 --no-pager`) and the status of `sshd`, `firewalld`, `chronyd`.  
6. SELinux mode (`getenforce`) and firewall state (`firewall-cmd --state`).  
7. Create `~/ciss-lab/notes.txt` with those findings (no secrets). Include a 5-line “RHEL 7 commands I will not type” list.

Optional: paste a sanitized command list into your Git notes on a `DR-###` branch.

## Integrity

- No scanning or attacking systems outside the lab scope.  
- No password guessing; no disabling SELinux, fapolicyd, or firewalld for convenience.  
- Do not store classified host details in public repos.  
- Do not install `net-tools` just to keep using `ifconfig`. Learn `ip`/`ss`.

## Further reading

| Topic | Source |
|-------|--------|
| RHEL 10.2 Release Notes | [docs.redhat.com — 10.2 Release Notes](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/10.2_release_notes/index) |
| Considerations in adopting RHEL 10 | [docs.redhat.com — adopting RHEL 10](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/considerations_in_adopting_rhel_10/index) |
| Configuring and managing networking | `man nmcli` · RHEL 10 Networking guide |
| systemd | `man systemctl` · `man journalctl` |
| DNF 5 | `man dnf` |
| ss / ip | `man ss` · `man ip` |
| Permissions | Search “Linux file permissions chmod tutorial” |

## Next

**Bash programming** — turn repeated 10.2 discovery commands into safe, reviewable scripts.
