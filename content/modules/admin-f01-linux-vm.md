# Linux on a VM

> **When:** Week 1 · Thursday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [admin-fa01-linux-vm — Host literacy sheet](/assignments/admin-fa01-linux-vm) (~2 hours), due **Week 1 Friday morning**.

## Learning outcomes

After this afternoon you can:

- Treat the lab runtime as a RHEL-class VM, not a laptop container
- Navigate filesystem, users, processes
- Use systemctl to ask whether a service is up
- Practice least privilege

## Why this afternoon exists

Software ‘works on my laptop’ and then dies on the guest. Admin is the runtime. Everyone needs enough Linux to not be helpless at 16:00 on a Thursday.

## Teach

CISS labs: **virtual machines** under vSphere / ESXi, typically **RHEL 7-class** or compatible. `docker run` in an external tutorial translates to: service on the assigned VM, `systemctl status`, correct hostname.

| You must be able to | Commands (examples) |
|---------------------|---------------------|
| Where am I | `pwd`, `ls`, `cd` |
| Who am I | `id`, `whoami` |
| What is running | `ps`, `systemctl status …` |
| What just happened | `journalctl -u … -n 50` |

Least privilege: your user + limited `sudo`. Do not disable SELinux “to see if it helps” on a shared host.

SE link: the VM *is* a deployment-view element.

## In-class exercise (30–40 min)

On the assigned VM (or a documented equivalent): `id`, `hostname`, `systemctl status` for one service, `df -h`. Write the four answers in your notebook.

## Additional lesson

The long-form original is archived as **[admin-01-rhel7-linux](/modules/admin-01-rhel7-linux)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **admin-fa01-linux-vm** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
