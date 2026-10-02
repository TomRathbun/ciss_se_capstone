# PRSAS — Host Hardening & Deployment Automation

> **Phase:** implementation close.

## Learning outcomes

After this module you can:

- Apply **firewalld** zones that *match* the NET allow-list (host layer, not a second religion)  
- Keep **SELinux enforcing** with documented booleans/ports for AMQ and Postgres  
- Turn on **auditd** useful rules (auth, privileged, cert dir)  
- Ship an **Ansible** (or PowerCLI) playbook that rebuilds a guest from the golden image  
- Write the **runbook** SW-12 will actually follow  

## Host firewall vs SRX

| Layer | Owner | Example |
|-------|-------|---------|
| SRX policy | NET | VLAN 30 cannot hit 5432 |
| firewalld | ADMIN | on `pg-c-01`, 5432 only from `10.30.20.0/24` |

Both should agree. If they disagree, **the tighter one wins** until you file a change.

```bash
firewall-cmd --permanent --add-rich-rule='rule family=ipv4 source address=10.30.20.0/24 port port=5432 protocol=tcp accept'
firewall-cmd --reload
```

SELinux: `semanage port` if AMQ is non-default; do not `setenforce 0` for the demo.

## Audit and logs

- `auditd` running; rules for `/etc/prsas`, sudo, `useradd`  
- `journalctl -u prsas-daemon` readable by the `systemd-journal` group SW uses  
- logrotate for AMQ  

## Automation (pick one primary)

| Tool | Use |
|------|-----|
| **Ansible** | packages, users, firewalld, copy CA, systemd unit |
| **PowerCLI / govc** | clone from template, set port group, power on |

A playbook that only `ping:`s is not enough. Show one idempotent run that configures `amq-c-01` **or** `trk-c-01`.

Do not automate key fill or production IPA admin passwords into Git.

## Monday workshop (builds ADMIN-A13)

1. **20 min** — firewalld vs NET-A11 allow-list diff (resolve mismatches).  
2. **20 min** — SELinux status + one boolean/port you actually need.  
3. **30 min** — Ansible skeleton: inventory + one role.  
4. **10 min** — Snapshot names for rollback.

## Thursday assignment

**ADMIN-A13 — Harden + automation pack.**

## Next

Integration demo. You own “it boots, it trusts, it is not root.” NET owns the tunnel. SW owns the picture.
