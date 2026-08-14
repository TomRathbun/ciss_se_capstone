# PRSAS — VM Provisioning

> **Phase:** implementation. vSphere/ESXi guests are the runtime. **admin-07** vocabulary applies.

## Learning outcomes

After this module you can:

- Build a **golden image** (Rocky / RHEL-class) and clone it per role  
- Place VMs on the **correct port group / VLAN** from the NET plan  
- Size CPU/RAM/disk without “give everyone 16 vCPU”  
- Deliver a **host inventory** SW can SSH to  
- Snapshot **before** first software install, not after a broken week  

## Minimum VM set

| VM | vCPU | RAM | Disk | Network |
|----|------|-----|------|---------|
| `sim-a-01` / `sim-b-01` | 2 | 4 GB | 40 GB | VLAN 30 site-local |
| `amq-c-01` | 2 | 4 GB | 40 GB | VLAN 20 |
| `trk-c-01` | 2 | 4 GB | 40 GB | VLAN 20 |
| `pg-c-01` | 2 | 8 GB | 80 GB | VLAN 20 |
| `ipa-c-01` | 2 | 6 GB | 40 GB | VLAN 20 |
| `ca-c-01` | 1 | 2 GB | 20 GB | VLAN 20 (may collapse into IPA) |
| `ui-c-01` | 2 | 4 GB | 40 GB | VLAN 10 |

Add a jump / bastion on mgmt if the instructor wants one. Do **not** put AMQ on the radar VLAN.

## Golden image checklist

- Time sync (chrony) to lab NTP  
- `sshd` key-only for intern accounts  
- `firewalld` on, ssh allowed from mgmt  
- SELinux **enforcing** (do not set permissive “to save time”)  
- Cloud-init or a first-boot hostname script  
- No leftover `/etc/prsas` secrets from a previous cohort  

Document: template name, snapshot name, clone procedure (UI or PowerCLI/govc).

## Monday workshop (builds ADMIN-A11)

1. **15 min** — Inventory table from NET-A11 IPs (or teaching IPs if NET is late).  
2. **40 min** — Clone or specify the three remote/central guests you can actually touch this week.  
3. **25 min** — Evidence: `hostnamectl`, `ip -br a`, `timedatectl` from each live VM.

## Thursday assignment

**ADMIN-A11 — Provision pack.**

## Next

**Identity and certificates** — IPA plus the lab CA that AMQ TLS will trust.
