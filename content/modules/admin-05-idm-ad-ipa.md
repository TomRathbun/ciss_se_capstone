# Identity Management — Active Directory and FreeIPA

## Learning outcomes

After this module you can:

- Explain **centralized identity** and why programs use it  
- Distinguish **Active Directory (AD)** and **FreeIPA** (and how Linux hosts join each)  
- Use common **lookup and auth** commands (`id`, `getent`, `realm`, `ipa`)  
- Recognize **SSO, groups, sudo rules, and HBAC** patterns  
- Troubleshoot basic “can’t log in / wrong groups” failures with evidence  

## Why identity management matters

Scattered local accounts do not scale. Central identity gives:

| Need | What IDM provides |
|------|-------------------|
| One account, many hosts | Central user/group directory |
| Access control | Groups, HBAC, sudo policies |
| Audit | Who authenticated, when |
| Integration | Apps (LDAP/Kerberos) and file shares (NFS + Kerberos) |

SE link: identity and authorization boundaries are part of the **system security architecture** and appear in ICDs (who may call what).

## Two common stacks

| Feature | **Active Directory** (Microsoft) | **FreeIPA** (Red Hat identity) |
|---------|----------------------------------|--------------------------------|
| Core protocol | LDAP + Kerberos (+ SMB/GPO world) | LDAP + Kerberos + DNS + certs (Dogtag) |
| Typical domain | `corp.example.com` | `ipa.example.com` |
| Linux join tool | `realm` / `sssd` / `adcli` | `ipa-client-install` / `realm` |
| Admin UI / CLI | ADUC, PowerShell, RSAT | Web UI, `ipa` CLI |
| Common in | Windows-heavy enterprises, mixed estates | RHEL-centric labs and many defense/gov Linux fleets |

Many programs run **both**: AD as the corporate directory, FreeIPA or SSSD for Linux hosts (sometimes with trust).

---

## Core concepts (shared vocabulary)

| Term | Meaning |
|------|---------|
| **Directory** | Hierarchical store of users, groups, hosts, policies (LDAP) |
| **Kerberos** | Ticket-based authentication (TGT, service tickets) |
| **Realm / domain** | Administrative Kerberos/AD boundary (e.g. `EXAMPLE.COM`) |
| **SSSD** | System Security Services Daemon — caches and brokers identity on the host |
| **Bind DN** | LDAP identity used by a service to query the directory |
| **Group** | Authorization unit — map to sudo, file ACLs, app roles |
| **HBAC** (IPA) | Host-based access control — which users may log into which hosts |
| **sudo rules** | Central “who may run what as root” |

```text
User → Kerberos auth → TGT
                 ↓
        Service ticket (host/nfs/http)
                 ↓
        Host/app checks groups + policy (SSSD / IPA / AD)
```

---

## Linux client: discovery commands

```bash
id
id username
getent passwd username
getent group developers
hostname -f
realm list                    # if realmd present
```

SSSD status and cache:

```bash
systemctl status sssd
sssctl domain-list            # if sssctl available
sssctl user-checks username   # auth path diagnostics
# Clear cache only when instructed:
# sudo sss_cache -E
```

Kerberos tickets:

```bash
klist
kinit username@REALM.COM
kdestroy
```

---

## Active Directory — admin view for Linux operators

### Join pattern (awareness)

```bash
# Typical high-level flow (do not run on shared lab without approval)
sudo yum install realmd sssd oddjob oddjob-mkhomedir adcli
sudo realm discover corp.example.com
sudo realm join corp.example.com -U join-account
```

After join, logins use domain accounts; home dirs may be created via `oddjob-mkhomedir`.

### What you usually verify

| Check | Command / place |
|-------|-----------------|
| Domain seen | `realm list` |
| User resolves | `getent passwd 'DOMAIN\user'` or `user@domain` |
| Groups | `id user` |
| Time sync | Kerberos is **time-sensitive** — `chronyc tracking` / `ntpq` |
| DNS | SRV records for `_ldap._tcp`, `_kerberos._tcp` |

### Common AD-side failures

1. Clock skew > ~5 minutes  
2. DNS not pointing at domain controllers  
3. Computer account disabled or OU policy blocking  
4. SSSD misconfigured (`/etc/sssd/sssd.conf` — root-only, mode `0600`)  
5. Firewall blocking 88/389/636/464 to DCs  

---

## FreeIPA — admin view

### Client install (awareness)

```bash
# Example only — needs IPA server, credentials, and approval
sudo ipa-client-install --domain=ipa.example.com --server=ipa1.ipa.example.com \
  --realm=IPA.EXAMPLE.COM --mkhomedir
```

### Useful `ipa` commands (on a enrolled host or admin workstation)

```bash
ipa user-find alice
ipa user-show alice
ipa group-find
ipa group-show developers --all
ipa host-show $(hostname -f)
ipa hbacrule-find
ipa sudorule-find
```

### HBAC and sudo (concept)

| Policy | Question it answers |
|--------|---------------------|
| **HBAC** | May user *U* log into host *H* via service *S*? |
| **sudo rule** | May user *U* run command *C* as root (or other) on host *H*? |

When “SSH works on host A but not B,” compare HBAC allow rules and host groups — not only local `sshd_config`.

---

## Integration touchpoints you will see

| System | How IDM shows up |
|--------|------------------|
| **SSH** | SSSD + pam_sss; key vs password vs GSSAPI |
| **NFS** | Often Kerberos (`sec=krb5`) — needs keytabs and time sync |
| **Postgres / apps** | LDAP auth or app-level group mapping |
| **Jenkins / GitLab** | SSO or group-based project access |
| **Sudo** | Central rules vs local `/etc/sudoers.d` |

---

## Troubleshooting methodology (IDM slice)

1. **Does the user exist in the directory?** `getent passwd` / `ipa user-show` / AD lookup  
2. **Does the host trust the realm?** `realm list`, keytab present (`klist -k`)  
3. **Can Kerberos work?** time sync, `kinit`, `klist`  
4. **Is policy denying access?** HBAC, AD group, deny rules, `AllowGroups` in sshd  
5. **Is SSSD healthy?** `systemctl status sssd`, logs in journal / `/var/log/sssd/`  

Capture: hostname, realm, exact username format used, error string, time offset, and `id` output.

---

## Drill (40–50 min)

On a lab host (read-only unless told otherwise):

1. Report whether the host is domain/IPA-joined (`realm list` or equivalent).  
2. Resolve your account with `id` and `getent passwd $(whoami)`.  
3. List group memberships; identify which groups look like authorization groups.  
4. Check time sync status (chrony/ntp).  
5. Attempt `klist`; if no tickets, note that (do not force `kinit` with shared passwords).  
6. Write a short note: “If SSH failed for a domain user, I would check … (5 bullets).”  

## Integrity

- Do not dump directory contents or user lists into public repos.  
- Do not store keytabs, bind passwords, or `sssd.conf` secrets in Git.  
- Do not join/leave domains on shared infrastructure without change control.  

## Further reading

| Topic | Source |
|-------|--------|
| SSSD | `man sssd` · [sssd.io](https://sssd.io/) |
| realmd | `man realm` |
| FreeIPA | [freeipa.org](https://www.freeipa.org/) · `man ipa` |
| AD for Linux | Red Hat “Integrating RHEL systems directly with AD” docs |
| Kerberos | `man kinit` · `man klist` |

## Next

**NFS setup and configuration** — shared filesystems, exports, mounts, and Kerberos-aware shares.
