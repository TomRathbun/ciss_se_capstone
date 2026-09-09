# System Administration & Integration — Track Overview

> **Track status:** active path — Linux/RHEL 10.2 through identity, storage, virtualization, data, and ops process.  
> Integration skills bridge **Software** builds to running systems (and support **Military** / SE labs).  
> **Lab standard:** work is done on **VMs** (vSphere / ESXi guests running **RHEL 10.2**), not Docker containers.

## Learning outcomes

After this overview you can:

- Explain **system administration and integration** as a selection-relevant craft  
- Distinguish build-time software work from **run-time** environments and glue  
- Navigate the **admin module path** from host literacy through tickets  
- Relate admin work to **V&V**, **ICDs**, and operational readiness  
- Name the **RHEL 7 → 10.2** breaks that will otherwise poison later labs  

## Why this track exists

Programs fail when software “works on my laptop” but not in the **integrated environment**. This track develops:

| Theme | What “good” looks like |
|-------|------------------------|
| **Host literacy** | RHEL 10.2 commands, NetworkManager, processes, journald, systemd **on VMs** |
| **Automation** | Small, safe bash scripts (Python 3 shebangs; no Python 2) |
| **Dependencies** | dnf, npm, pip/uv, Maven — and Nexus |
| **Trust** | TLS certs, chains, expiry, trust stores, crypto-policies |
| **Identity** | AD / FreeIPA, SSSD, groups, HBAC, `authselect` |
| **Shared storage** | NFS exports, mounts, UID mapping |
| **Virtualization** | ESXi / vSphere / vSAN / VDI awareness |
| **Data platform** | Postgres 18 admin SQL and safe maintenance |
| **Ops process** | Troubleshooting method, tickets, runbooks |
| **Integrity** | Least privilege, no secrets in Git, change control |

## Lab OS change (read this)

The previous edition of this track assumed **RHEL 7**. The lab is now **RHEL 10.2** (kernel 6.12, systemd 257, DNF 5, NetworkManager-only, nftables firewalld, Python 3.12+ / AppStream 3.14, OpenJDK 21/25, Podman, chrony, cgroup v2).

Teaching implications for every later module:

1. Type **`dnf`**, not `yum`.  
2. Configure NICs with **`nmcli`**, not `ifcfg-*` / `network-scripts`.  
3. Discover sockets with **`ss`**, addresses with **`ip`**. Do not install `net-tools` to keep `ifconfig`.  
4. Time is **chrony** (`chronyc tracking`). `ntpd` is gone.  
5. Logs start at **`journalctl`**. `/var/log/messages` is optional.  
6. There is **no in-place upgrade** from RHEL 7 to 10. Golden images are built fresh (admin-11).  
7. Program Java 8, if still required for JBoss/AMQ labs, is an **explicit alternative JDK** — it is not `dnf install java-1.8.0-openjdk` on 10.2. Document `JAVA_HOME`.

Module **admin-01** opens with the full delta table. Instructors: project it. Interns: copy it into the lab notebook.

## Module path (this track)

| Order | Module | You will… |
|-------|--------|-----------|
| 1 | **RHEL 10.2 and Essential Linux Commands** | Navigate hosts, NetworkManager, DNF 5, `systemctl`/`journalctl`, translate RHEL 7 habits |
| 2 | **Bash programming** | Scripts, errors, quoting, admin patterns |
| 3 | **Package management** | dnf/rpm, npm, pip/uv, Maven, Nexus |
| 4 | **TLS certificate management** | Inspect certs, chains, trust, crypto-policies, common failures |
| 5 | **Identity Management — AD and FreeIPA** | Central identity, Kerberos, SSSD, HBAC |
| 6 | **NFS setup and configuration** | Exports, mounts, permissions, Kerberos shares |
| 7 | **vSphere, vSAN, VDI, and ESXi** | Hypervisor vocabulary, VM lifecycle, storage |
| 8 | **PostgreSQL for admins** | Roles, activity, size, locks, backup awareness (PG 18 on 10.2) |
| 9 | **Troubleshooting methodology** | Systematic diagnosis; grep/tail/ps/ss/journalctl deep dive |
| 10 | **Documentation and trouble tickets** | Ticket quality, runbooks, resolution notes |

Register more modules in `content/catalog.yaml` with `track: admin`.

## Lab assumptions

| Item | Typical |
|------|---------|
| **Compute** | **Virtual machines** under vSphere/ESXi (not Docker as the course default) |
| OS | **RHEL 10.2** or compatible clone (Rocky/Alma 10) on the guest |
| Shell | **bash** |
| Privilege | User account + limited `sudo` |
| Artifacts | **Nexus** when configured (same as SW track) |
| Identity | Lab may use FreeIPA, AD, or local accounts — follow instructor |
| Services | Postgres 18, ActiveMQ, JBoss, etc. installed **on VMs** or reached by host/IP from the lab sheet |
| Virtualization access | Read-only or supervised access to vSphere when available |
| Git | **GitLab** for CISS labs; program uses Bitbucket + Jira DRs |
| `/boot` | Golden image **2 GiB** (RHEL 10.2 default; 1 GiB templates will fail firmware-heavy initramfs) |

If an external tutorial shows `docker run`, translate it to: **service on the assigned VM**, `systemctl status …`, and the correct hostname/port. If it shows `podman run`, that *is* the 10.2-native container tool — still not the default runtime for CISS services.

## Relationship to other tracks

| Track | Overlap with admin / integration |
|-------|----------------------------------|
| **Systems Engineering** | V&V evidence, environments as system boundary |
| **Software** | Deploy jars/workers on VMs; Jenkins; ActiveMQ; Postgres; JDK location on 10.2 |
| **Networking** | Ports, DNS, firewalld/nft, TLS on the wire, NFS |
| **Military** | Training systems and C2-adjacent labs must stay usable |

## Integrity

- No unauthorized scanning, privilege escalation “for fun,” or disabling SELinux/firewalld/fapolicyd on shared hosts.  
- No production credentials, keytabs, or private keys in course repos.  
- Same professionalism (A6) as SE and Software tracks.

## Further reading

| Topic | Source |
|-------|--------|
| RHEL 10.2 | [10.2 Release Notes](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/10.2_release_notes/index) |
| RHEL admin | Red Hat product documentation (version-matched **10**, not 7) |
| Bash | [GNU Bash manual](https://www.gnu.org/software/bash/manual/) |
| TLS | [MDN TLS](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) |
| FreeIPA / SSSD | [freeipa.org](https://www.freeipa.org/) · [sssd.io](https://sssd.io/) |
| PostgreSQL | [postgresql.org/docs](https://www.postgresql.org/docs/) |

## Next

**RHEL 10.2 and Essential Linux Commands** — survival kit plus the RHEL 7 → 10.2 translation table.
