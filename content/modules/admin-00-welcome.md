# System Administration & Integration — Track Overview

> **Track status:** active foundation path — Linux/RHEL, bash, packages, and TLS.  
> Integration skills bridge **Software** builds to running systems (and support **Military** / SE labs).

## Learning outcomes

After this overview you can:

- Explain **system administration and integration** as a selection-relevant craft  
- Distinguish build-time software work from **run-time** environments and glue  
- Navigate the **admin module path** (RHEL → bash → packages → TLS)  
- Relate admin work to **V&V**, **ICDs**, and operational readiness  

## Why this track exists

Programs fail when software “works on my laptop” but not in the **integrated environment**. This track develops:

| Theme | What “good” looks like |
|-------|------------------------|
| **Host literacy** | RHEL 7 commands, processes, logs, services |
| **Automation** | Small, safe bash scripts |
| **Dependencies** | yum, npm, pip/uv, Maven — and Nexus |
| **Trust** | TLS certs, chains, expiry, trust stores |
| **Integrity** | Least privilege, no secrets in Git, change control |

## Module path (this track)

| Order | Module | You will… |
|-------|--------|-----------|
| 1 | **RHEL 7 and Essential Linux Commands** | Navigate hosts, logs, processes, `systemctl` |
| 2 | **Bash programming** | Scripts, errors, quoting, admin patterns |
| 3 | **Package management** | yum, npm, pip/uv, Maven, Nexus |
| 4 | **TLS certificate management** | Inspect certs, chains, trust, common failures |

Register more modules in `content/catalog.yaml` with `track: admin`.

## Lab assumptions

| Item | Typical |
|------|---------|
| OS | **RHEL 7** or compatible clone (note RHEL 8/9 differences when relevant) |
| Shell | **bash** |
| Privilege | User account + limited `sudo` |
| Artifacts | **Nexus** when configured (same as SW track) |
| Git | **GitLab** for CISS labs; program uses Bitbucket + Jira DRs |

## Relationship to other tracks

| Track | Overlap with admin / integration |
|-------|----------------------------------|
| **Systems Engineering** | V&V evidence, environments as system boundary |
| **Software** | Deploy jars/workers; Jenkins; ActiveMQ; Postgres |
| **Networking** | Ports, DNS, firewall, TLS on the wire |
| **Military** | Training systems and C2-adjacent labs must stay usable |

## Integrity

- No unauthorized scanning, privilege escalation “for fun,” or disabling SELinux/firewall on shared hosts.  
- No production credentials or private keys in course repos.  
- Same professionalism (A6) as SE and Software tracks.

## Further reading

| Topic | Source |
|-------|--------|
| RHEL admin | Red Hat product documentation (version-matched) |
| Bash | [GNU Bash manual](https://www.gnu.org/software/bash/manual/) |
| TLS | [MDN TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) |

## Next

**RHEL 7 and Essential Linux Commands** — survival kit for every later admin module.
