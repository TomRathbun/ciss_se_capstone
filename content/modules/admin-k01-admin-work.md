# Admin work on the capstone

> **When:** Week 5 · Thursday afternoon · Masdar
> **Who:** All interns this week; elective from week 6
> **Tomorrow morning:** [admin-ka01-admin-work — Admin accomplishment list](/assignments/admin-ka01-admin-work) (~2 hours), due **Week 5 Friday morning**.

## Learning outcomes

After this afternoon you can:

- List VM provision, identity/certs, harden/automate as separate jobs
- See rebuildability as the test of admin work
- Keep keys out of Git

## Why this afternoon exists

If the stack cannot be rebuilt, the demo is a snowflake.

## Teach

**Admin must accomplish**

- VM provisioning on the correct port groups; snapshot discipline
- Identity (FreeIPA/OpenLDAP) and lab certificates for AMQ TLS and clients
- Host hardening (firewalld, SELinux, audit) aligned to the allow-list
- Enough automation (Ansible or PowerCLI) that the stack can be rebuilt

**Admin does not** treat Junos policy as the system of record.

Depth starts bash/TLS/IPA for those who stay. Live modules: [admin-11](/modules/admin-11-prsas-provision) onward.

## In-class exercise (30–40 min)

Inventory the VMs you think exist (sim-a, sim-b, amq, daemon, db, idm, client). Mark who needs a cert. Mark who needs to be on which VLAN — as questions for NET.

## Additional lesson

The long-form original is archived as **[admin-11-prsas-provision](/modules/admin-11-prsas-provision)**. Read it after class if you will keep this discipline.

## Tomorrow morning

Do **admin-ka01-admin-work** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
