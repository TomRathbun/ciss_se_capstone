# ADMIN-A01 — RHEL 10.2/Linux Discovery Lab

**Weight:** 10% · **Due:** After admin-01-rhel10-linux · **Module:** admin-01-rhel10-linux

## Prompt

On a lab **RHEL 10.2** (or compatible Rocky/Alma 10) host, produce an **evidence pack** that proves you can discover system state safely *and* that you will not paste RHEL 7 commands onto this guest.

## Deliverables

1. **Host identity sheet:** hostname (`hostnamectl`), OS release (`/etc/os-release` — quote `NAME` and `VERSION_ID`), kernel (`uname -r`), uptime, primary IP(s) from `ip -br addr` or `nmcli`.
2. **Network stack proof:** `nmcli device status`; listing of `/etc/NetworkManager/system-connections/`; explicit confirmation that `/etc/sysconfig/network-scripts/ifcfg-*` is **absent**.
3. **Command evidence** (paste outputs, redact secrets) for: filesystem (`df -hT`), processes (`ps` top consumers), users/groups relevant to you, listening ports (`ss -lntp` — not `netstat`), service status (`systemctl status` on `sshd` and one of `firewalld` / `chronyd` / `NetworkManager`).
4. **Packages:** `dnf --version`, `rpm -q bash`, `command -v python3` and `python3 --version`. Note whether `java` exists and which vendor/version.
5. **Logs:** one `journalctl -b` excerpt you used to answer “what happened this boot?”
6. **Awareness notes:** SELinux mode (`getenforce`) and firewall state (`firewall-cmd --state`) — what you observed, not a lecture rewrite. Chrony: `chronyc tracking` or `timedatectl`.
7. **RHEL 7 anti-pattern list:** 5 commands you must **not** type on 10.2 (`yum`, `ifconfig`, `netstat`, `chkconfig`, `ifup`/`service network`, `ntpq`, `iptables -A`, …) and the 10.2 replacement for each.
8. **Risk list:** 3 things you would *not* run on a shared host without approval.

## Quality bar

- Read-only first; no destructive “fixes.”
- Outputs are labeled so a peer can re-run the same checks on RHEL 10.2.
- Redaction is correct (passwords, tokens, personal data).
- No `ifconfig` / `netstat` / `yum` in the evidence unless you are *showing they failed* and then showing the replacement.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| discovery | 15 | Broad, correct 10.2 evidence pack (nmcli, dnf, journalctl) |
| safety | 10 | Non-destructive; good redaction; RHEL 7 anti-patterns named |
| communication | 5 | Labeled, reproducible |
