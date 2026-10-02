# Software on the host

> **When:** Week 3 · Thursday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [admin-fa03-software-host — Install and secret-handling note](/assignments/admin-fa03-software-host) (~2 hours), due **Week 3 Friday morning**.

## Learning outcomes

After this afternoon you can:

- Explain how a package gets onto a RHEL-class VM
- Reject ‘works on my laptop’ as a deployment
- Keep secrets out of Git and screenshots
- Treat snapshots as a rollback idea

## Why this afternoon exists

Software builds jars. Admin makes them run tomorrow after a reboot. If you cannot say where the bits came from, you cannot rebuild the lab.

## Teach

**Packages:** `yum`/`rpm` on the guest; language ecosystems (Maven, pip, npm) still land *on the VM*. Nexus is the org hub when configured.

Deployment means: bits on the **assigned host**, service enabled, config outside the jar, secrets not in Git.

**Snapshots** (vSphere) are a rollback idea, not a backup strategy. Know when a snapshot is allowed; do not snapshot a full database as folklore.

Hold: writing Ansible roles, vSAN design, FreeIPA.

## In-class exercise (30–40 min)

Trace ‘install PostgreSQL’ from package source → files on disk → systemd unit → who owns the data directory. Where would a password accidentally get committed?

## Additional lesson

The long-form original is archived as **[admin-03-package-management](/modules/admin-03-package-management)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **admin-fa03-software-host** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
