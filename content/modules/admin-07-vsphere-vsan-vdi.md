# vSphere, vSAN, VDI, and ESXi

## Learning outcomes

After this module you can:

- Map the **VMware stack** vocabulary (ESXi, vCenter, vSphere, vSAN, VDI)  
- Explain what an admin does day-to-day in **vSphere Client** vs on an **ESXi host**  
- Describe **VM lifecycle** actions (power, snapshot, clone, template) and risks  
- Recognize **storage (vSAN / datastores)** and **network** objects at a high level  
- Know when to escalate vs what evidence to gather for virtualization tickets  

## Why this module exists

Most lab and many production workloads run as **virtual machines**. Integration work fails when the VM layer is opaque: wrong network, full datastore, snapshot sprawl, or a host in maintenance mode.

| Layer | What it is |
|-------|------------|
| **ESXi** | Hypervisor installed on physical bare metal |
| **vCenter Server** | Central management for many ESXi hosts/clusters |
| **vSphere** | Product family / umbrella (ESXi + vCenter + features) |
| **vSAN** | Software-defined shared storage across ESXi hosts |
| **VDI** | Virtual Desktop Infrastructure (e.g. Horizon) — desktop VMs at scale |

SE link: the virtualization platform is part of the **deployment environment** — capacity, HA, and isolation constraints belong in architecture and NFRs.

```text
Physical hosts (ESXi)
        │
   vCenter / cluster
        │
   ┌────┼────┐
  VMs  vSAN  Networks (vSwitches / port groups)
        │
   Optional: VDI brokers → end-user desktops
```

---

## ESXi host essentials

| Concept | Admin meaning |
|---------|---------------|
| **Host** | One hypervisor instance on a server |
| **VM** | Guest OS + virtual hardware definition |
| **Datastore** | Storage container for VMDKs and files (VMFS, NFS, vSAN) |
| **vSwitch / port group** | Virtual networking — VMs attach NICs to port groups |
| **vmkernel** | Hypervisor network stack (mgmt, vMotion, storage) |
| **DCUI** | Direct Console User Interface on the physical host |

Typical host checks (via UI or SSH if enabled and authorized):

- Host connection state (Connected / Not responding / Maintenance)  
- CPU / memory pressure  
- Datastore free space  
- Recent tasks and events  

> SSH to ESXi is often disabled by policy. Prefer vSphere Client unless break-glass procedures apply.

---

## vCenter and vSphere Client

**vCenter** aggregates hosts into **datacenters** and **clusters**.

| Object | Role |
|--------|------|
| Datacenter | Organizational boundary |
| Cluster | HA / DRS pool of hosts |
| Resource pool | CPU/memory shares and limits |
| Folder | Inventory organization |
| Template | Golden image for new VMs |

**Day-2 admin actions** you will see or perform under supervision:

| Action | Caution |
|--------|---------|
| Power on / off / reset VM | Reset ≈ hard power loss |
| Install VMware Tools / open-vm-tools | Better time sync, clean shutdown, drivers |
| Snapshot | Short-term only; growth hurts performance |
| Clone | Linked vs full; storage impact |
| Migrate (vMotion / Storage vMotion) | Needs shared storage / correct licensing / healthy cluster |
| Put host in Maintenance Mode | Evacuate VMs first |

---

## Storage: datastores and vSAN

### Traditional datastores

- **VMFS** on local or SAN LUNs  
- **NFS** datastores (ties to the NFS module)  

### vSAN (conceptual)

| Idea | Meaning |
|------|---------|
| Shared pool | Local disks from each host form a cluster datastore |
| Disk groups | Cache + capacity devices per host |
| Policies | FTT (failures to tolerate), RAID-1/RAID-5/6 equivalents, thin/thick |
| Health | Must watch disk / host failures — data is distributed |

Admin symptoms of storage pain:

- Datastore **>80–90% full**  
- VMs paused / stunned on space exhaustion  
- Snapshot files consuming unexpected capacity  
- vSAN health alarms (disk failed, not enough fault domains)  

---

## Networking (VM perspective)

| Object | What VMs care about |
|--------|---------------------|
| Port group | VLAN / security policy / which network |
| Connected / disconnected NIC | “No network” in the guest |
| Wrong port group | VM up but unreachable from peers |

Always verify **guest IP, port group name, and uplink health** before blaming the application.

---

## VDI (Virtual Desktop Infrastructure)

VDI delivers full desktops (Windows/Linux) from the datacenter to endpoints.

| Component | Role |
|-----------|------|
| Broker / connection server | Authenticates users, assigns desktops |
| Pool | Set of desktop VMs (persistent vs non-persistent) |
| Golden image / parent VM | Source for linked clones or instant clones |
| AppVolumes / FSLogix (examples) | App and profile layers (vendor-specific) |

Intern-relevant failure modes:

- Pool depleted (no available desktops)  
- Image update left pool in bad state  
- User profile / permissions issues  
- Capacity (CPU/RAM/storage) on the desktop cluster  

You rarely “fix ESXi” for a single VDI complaint — you gather user ID, pool name, desktop VM name, and broker errors first.

---

## Snapshots — operational rules

| Rule | Why |
|------|-----|
| Short-lived | Delta disks grow; performance drops |
| Not backup | Snapshots are not a substitute for backup products |
| Delete (consolidate) carefully | Needs free space to merge |
| One or few layers | Deep chains are fragile |

Before large changes: snapshot **with memory** only when instructed; otherwise prefer powered-off snapshots or backup tooling.

---

## Troubleshooting evidence for virtualization tickets

Capture:

1. **VM name** and UUID / MoRef if available  
2. **Host** and **cluster**  
3. Power state and recent **Tasks/Events**  
4. Datastore name and **free space**  
5. Port group / IP / whether VMware Tools is running  
6. Exact error dialog or event text  
7. Timeline (when it last worked)  

Guest-level tools still apply once the VM is up: `ip`, `journalctl`, app logs (other admin modules).

---

## Drill (40–50 min)

1. Label a diagram: ESXi, vCenter, cluster, datastore, VM, port group.  
2. List five VM actions that are disruptive (need change windows).  
3. Explain why a snapshot left for 3 months is a problem.  
4. Given “VM cannot be reached on the network,” write an ordered check list (virtualization + guest).  
5. Differentiate: host storage full vs vSAN policy compliance alarm (one paragraph each).  

## Integrity

- No experimental power-offs, storage deletes, or network changes on shared clusters.  
- No copying VM disks or snapshots off-platform without authorization.  
- Treat vCenter credentials like production secrets.  

## Further reading

| Topic | Source |
|-------|--------|
| vSphere overview | Broadcom / VMware vSphere documentation (version-matched) |
| ESXi | Host Client help · vendor admin guides |
| vSAN | vSAN planning and health docs |
| Horizon / VDI | Vendor VDI admin overview (if your lab uses it) |

## Next

**PostgreSQL database management** — admin SQL, roles, maintenance, and safe operational habits.
