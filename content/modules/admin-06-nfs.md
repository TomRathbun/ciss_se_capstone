# NFS Setup and Configuration

## Learning outcomes

After this module you can:

- Explain **NFS** roles (server vs client) and common versions (v3 / v4)  
- Read and modify **exports** and **mount** options safely  
- Use `showmount`, `exportfs`, `mount`, and `df` for verification  
- Recognize **permissions, UID mapping, and firewall** failure modes  
- Relate NFS to **IDM/Kerberos** when `sec=krb5` is required  

## Why NFS shows up

Programs share:

| Use case | Example |
|----------|---------|
| Home directories | Central homes for lab users |
| Application data | Shared config, reports, media  |
| Build artifacts | Read-only mirrors (sometimes) |
| Integration labs | Multiple VMs reading the same dataset |

SE link: a network filesystem is an **external interface** — availability, latency, and auth belong in NFRs and ICDs.

## Concepts

| Term | Meaning |
|------|---------|
| **Export** | Directory the server offers to clients |
| **Mount** | Client attaches a remote export to a local path |
| **NFSv3** | Older; often UDP/TCP; relies more on host-based trust + UIDs |
| **NFSv4** | Single port (2049), better firewall story, pseudo-fs, stronger ID mapping |
| **UID/GID** | Numeric identity on disk — must match (or be mapped) across hosts |
| **sec=** | Security flavor: `sys` (AUTH_SYS), `krb5`, `krb5i`, `krb5p` |

```text
NFS server                         NFS client
/export/data  ──exportfs──►  network  ──mount──►  /mnt/data
```

---

## Server side (RHEL-style)

### Packages / services

```bash
rpm -q nfs-utils
systemctl status nfs-server      # or nfs on some layouts
# rpcbind often required for v3
systemctl status rpcbind
```

### `/etc/exports`

```bash
# Example patterns (illustrative)
/export/data   10.10.20.0/24(rw,sync,no_root_squash)
/export/public *(ro,sync,root_squash)
/export/homes  *.lab.example.com(rw,sync,root_squash)
```

| Option | Meaning |
|--------|---------|
| `rw` / `ro` | Read-write or read-only |
| `sync` | Stable writes before reply (safer; slower) |
| `async` | Faster; risk on crash |
| `root_squash` | Remote root → `nobody` (default good practice) |
| `no_root_squash` | Remote root stays root — **dangerous**; justify tightly |
| `all_squash` | All users map to anonymous |

Apply and review:

```bash
sudo exportfs -ra
sudo exportfs -v
showmount -e localhost
```

### Firewall (awareness)

NFSv4 often needs **TCP 2049**. NFSv3 adds portmapper and dynamic ports (or fixed ports via config). Coordinate with the networking track and do not open wide ranges on shared labs without approval.

---

## Client side

### Discover

```bash
showmount -e nfs-server.example.com
```

### Temporary mount

```bash
sudo mkdir -p /mnt/data
sudo mount -t nfs nfs-server.example.com:/export/data /mnt/data
df -h /mnt/data
mount | grep nfs
```

### Persistent mount — `/etc/fstab`

```bash
# NFSv4 example
nfs-server.example.com:/export/data  /mnt/data  nfs  defaults,_netdev,rw  0  0
```

| fstab flag | Why |
|------------|-----|
| `_netdev` | Wait for network before mount |
| `ro` | Enforce read-only on client |
| `vers=4.1` | Pin protocol version when required |
| `sec=krb5` | Kerberos auth (needs keytab + IDM) |

```bash
sudo mount -a
sudo umount /mnt/data
```

---

## Permissions and UID mapping

NFS with `sec=sys` trusts the **numeric UID/GID** the client sends.

| Symptom | Likely cause |
|---------|--------------|
| Files owned by `nobody` | Squash options or unknown UID |
| Can read on server, not client | Export `ro`, mount options, or POSIX mode |
| User A on host1 ≠ user A on host2 | Different UID for same name — use IDM |

**Mitigation:** central identity (AD/IPA) so UIDs match, or explicit idmap configuration for NFSv4.

---

## Kerberos-secured NFS (awareness)

When exports require `sec=krb5*`:

1. Hosts enrolled in realm (AD or IPA)  
2. NFS service principal / keytab on server  
3. Client has valid TGT (`kinit` / SSSD)  
4. Time sync healthy  

```bash
klist
mount -o sec=krb5 ...
```

Failures often look like “Permission denied” with little else — check tickets and keytabs before rewriting exports.

---

## Troubleshooting checklist

1. **Reachability:** `ping`, `traceroute`, firewall  
2. **Export visible:** `showmount -e server`  
3. **Server service up:** `systemctl status nfs-server`, `exportfs -v`  
4. **Mount error text:** `dmesg | tail`, `journalctl -xe`  
5. **Permissions:** `ls -l` on server and after mount; compare UIDs  
6. **Stale handle:** server re-exported or file deleted under client — `umount` / remount  
7. **Performance:** `nfsstat`, network latency, `sync` vs `async`  

Useful tools:

```bash
rpcinfo -p nfs-server.example.com
nfsstat -c          # client stats
nfsstat -s          # server stats
```

---

## Operator discipline

| Do | Don’t |
|----|-------|
| Prefer `root_squash` | Casual `no_root_squash` on open networks |
| Document export + mount options | Rely on tribal memory of “the share” |
| Use `_netdev` in fstab | Silent boot hangs waiting for NFS |
| Align UIDs via IDM | Hand-edit UIDs on many hosts |

---

## Drill (40 min)

1. On a lab client: run `showmount -e` against the instructor-provided NFS server (or note if none).  
2. Read any existing NFS mounts: `mount | grep nfs` and matching `fstab` lines.  
3. Sketch an `/etc/exports` line for a read-only dataset limited to a /24 lab subnet.  
4. Explain in 5 sentences what goes wrong if two hosts disagree on UID for `alice`.  
5. List three evidence items you would capture before asking for `no_root_squash`.  

## Integrity

- Do not export `/` or sensitive paths to `*`.  
- Do not weaken squash or security flavors to bypass broken IDM without approval.  
- Treat NFS content as potentially sensitive — same rules as local data.  

## Further reading

| Topic | Source |
|-------|--------|
| exports | `man exports` · `man exportfs` |
| nfs | `man nfs` · `man mount` |
| RHEL NFS | Red Hat Storage / System Admin guides (version-matched) |
| rpcinfo | `man rpcinfo` |

## Next

**vSphere, vSAN, VDI, and ESXi** — virtualization platform literacy for labs and ops hosts.
