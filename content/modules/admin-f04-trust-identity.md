# Trust and identity

> **When:** Week 4 · Thursday afternoon · Masdar
> **Who:** All interns (weeks 1–4)
> **Tomorrow morning:** [admin-fa04-trust-identity — Certificate one-pager](/assignments/admin-fa04-trust-identity) (~2 hours), due **Week 4 Friday morning**.

## Learning outcomes

After this afternoon you can:

- Explain a certificate, a key, and a chain in one page
- Say why every box should not have its own password file
- Connect admin trust work to SE V&V
- Hold FreeIPA, vSAN, and Ansible for depth

## Why this afternoon exists

PRSAS will use TLS on the broker and logins for the client. If ‘certificate’ is a magic word, you will block Software next month.

## Teach

A **certificate** binds a **public key** to a name (and SANs), signed by a **CA**. The **private key** stays private. A **chain** is leaf → intermediates → trust anchor.

When TLS fails, look at: names, clocks (expiry), and whether the client **trusts** the CA — before you regenerate everything.

**Identity:** people and services should come from a **central** source (AD / FreeIPA in depth) so sudo, groups, and offboarding work. Local `root` passwords on twelve VMs is how intern labs rot.

SE V&V: “clients authenticate” is a shall. Admin produces the **evidence** (login works with the issued cert; `openssl` inspect).

Hold: issuing a lab CA, IPA replicas, HBAC design.

## In-class exercise (30–40 min)

On paper: leaf cert for `amq-c-01`. What SAN must it have? Who trusts it? What shall does that prove?

## Additional lesson

The long-form original is archived as **[admin-04-tls-certs](/modules/admin-04-tls-certs)**. Read it after class if you will keep this discipline.

## Hold for later

FreeIPA, vSAN, Ansible, NFS Kerberos — week 6+ for those who stay in Admin.

## Tomorrow morning

Do **admin-fa04-trust-identity** before the next afternoon lecture. Time-box **two hours**. Stop and turn in what you have. Do not start tomorrow’s discipline homework until this one is in.

## Integrity

Unclassified work only. No production credentials, no classified topologies, no secrets in Git. Cite public sources.
