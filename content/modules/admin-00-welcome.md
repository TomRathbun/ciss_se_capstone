# System Administration & Integration — Track Overview

> **Track status:** active path — Linux/RHEL through identity, storage, virtualization, data, and ops process.  
> Integration skills bridge **Software** builds to running systems (and support **Military** / SE labs).  
> **Lab standard:** work is done on **VMs** (vSphere / ESXi guests), not Docker containers.

## Learning outcomes

After this overview you can:

- Explain **system administration and integration** as a selection-relevant craft  
- Distinguish build-time software work from **run-time** environments and glue  
- Navigate the **admin module path** from host literacy through tickets  
- Relate admin work to **V&V**, **ICDs**, and operational readiness  

## Why this track exists

Programs fail when software “works on my laptop” but not in the **integrated environment**. This track develops:

| Theme | What “good” looks like |
|-------|------------------------|
| **Host literacy** | RHEL 7 commands, processes, logs, services **on VMs** |
| **Automation** | Small, safe bash scripts |
| **Dependencies** | yum, npm, pip/uv, Maven — and Nexus |
| **Trust** | TLS certs, chains, expiry, trust stores |
| **Identity** | AD / FreeIPA, SSSD, groups, HBAC |
| **Shared storage** | NFS exports, mounts, UID mapping |
| **Virtualization** | ESXi / vSphere / vSAN / VDI awareness |
| **Data platform** | Postgres admin SQL and safe maintenance |
| **Ops process** | Troubleshooting method, tickets, runbooks |
| **Integrity** | Least privilege, no secrets in Git, change control |

## Module path (this track)

| Order | Module | You will… |
|-------|--------|-----------|
| 1 | **RHEL 7 and Essential Linux Commands** | Navigate hosts, logs, processes, `systemctl` |
| 2 | **Bash programming** | Scripts, errors, quoting, admin patterns |
| 3 | **Package management** | yum, npm, pip/uv, Maven, Nexus |
| 4 | **TLS certificate management** | Inspect certs, chains, trust, common failures |
| 5 | **Identity Management — AD and FreeIPA** | Central identity, Kerberos, SSSD, HBAC |
| 6 | **NFS setup and configuration** | Exports, mounts, permissions, Kerberos shares |
| 7 | **vSphere, vSAN, VDI, and ESXi** | Hypervisor vocabulary, VM lifecycle, storage |
| 8 | **PostgreSQL for admins** | Roles, activity, size, locks, backup awareness |
| 9 | **Troubleshooting methodology** | Systematic diagnosis; grep/tail/ps/ss deep dive |
| 10 | **Documentation and trouble tickets** | Ticket quality, runbooks, resolution notes |

Register more modules in `content/catalog.yaml` with `track: admin`.

## Lab assumptions

| Item | Typical |
|------|---------|
| **Compute** | **Virtual machines** under vSphere/ESXi (not Docker as the course default) |
| OS | **RHEL 7** or compatible clone on the guest (note RHEL 8/9 differences when relevant) |
| Shell | **bash** |
| Privilege | User account + limited `sudo` |
| Artifacts | **Nexus** when configured (same as SW track) |
| Identity | Lab may use FreeIPA, AD, or local accounts — follow instructor |
| Services | Postgres, ActiveMQ, JBoss, etc. installed **on VMs** or reached by host/IP from the lab sheet |
| Virtualization access | Read-only or supervised access to vSphere when available |
| Git | **GitLab** for CISS labs; program uses Bitbucket + Jira DRs |

If an external tutorial shows `docker run`, translate it to: **service on the assigned VM**, `systemctl status …`, and the correct hostname/port.

## Relationship to other tracks

| Track | Overlap with admin / integration |
|-------|----------------------------------|
| **Systems Engineering** | V&V evidence, environments as system boundary |
| **Software** | Deploy jars/workers on VMs; Jenkins; ActiveMQ; Postgres |
| **Networking** | Ports, DNS, firewall, TLS on the wire, NFS |
| **Military** | Training systems and C2-adjacent labs must stay usable |

## Integrity

- No unauthorized scanning, privilege escalation “for fun,” or disabling SELinux/firewall on shared hosts.  
- No production credentials, keytabs, or private keys in course repos.  
- Same professionalism (A6) as SE and Software tracks.

## Further reading

| Topic | Source |
|-------|--------|
| RHEL admin | Red Hat product documentation (version-matched) |
| Bash | [GNU Bash manual](https://www.gnu.org/software/bash/manual/) |
| TLS | [MDN TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) |
| FreeIPA / SSSD | [freeipa.org](https://www.freeipa.org/) · [sssd.io](https://sssd.io/) |
| PostgreSQL | [postgresql.org/docs](https://www.postgresql.org/docs/) |

## Next

**RHEL 7 and Essential Linux Commands** — survival kit for every later admin module.
