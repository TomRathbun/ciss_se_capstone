# PRSAS — Identity & Lab Certificates

> **Phase:** implementation. Combines **admin-05** and **admin-04** for the air-picture path.

## Learning outcomes

After this module you can:

- Stand up or join VMs to **FreeIPA** (preferred) or OpenLDAP + SSSD  
- Create **service principals / users** for daemon, AMQ, and operators  
- Run a **lab CA** and issue TLS certs for AMQ, Postgres (optional), and clients  
- Install trust bundles on every PRSAS VM  
- Diagnose **name mismatch, expired, incomplete chain** without pasting private keys  

## Identity model

| Principal | Purpose |
|-----------|---------|
| `prsas-daemon` | systemd user on `trk-c-01`; JDBC role of the same name |
| `prsas-sim` | optional; sims may use a shared publisher user on AMQ |
| `operator1` … | humans; IPA password or cert mapping |
| `amq-c-01` | host principal if you do Kerberos; else just a TLS server name |

HBAC: operators do not SSH to `pg-c-01`. Daemon does not have `wheel`.

If IPA cannot be fully built this week, document the **gap** and use a local `sssd` stub **plus** a dated ticket to finish it. Do not silently skip TLS.

## Certificate plan

| Cert | SAN / CN | Installed on |
|------|----------|--------------|
| Lab root CA | `CISS-LAB-CA` | trust store **everywhere** |
| `amq-c-01` | DNS `amq-c-01`, IP if needed | AMQ `broker.ks` |
| `pg-c-01` | DNS `pg-c-01` | optional `ssl=require` |
| `trk-c-01` client | clientAuth | daemon trust/key |
| UI / browser | clientAuth or user cert | `ui-c-01` |

ActiveMQ TLS listens on **61617**. Need **server cert + CA**. Mutual TLS is extra credit if the week allows.

```bash
# inspect — never cat the key
openssl x509 -in amq-c-01.crt -noout -subject -issuer -dates -ext subjectAltName
openssl s_client -connect amq-c-01:61617 -CAfile lab-ca.crt </dev/null
```

## Distribution

- Ansible `copy` of the CA is fine.  
- Private keys: mode `0640`, owner service user, **not** in Git.  
- Instructor keeps the CA key offline or on `ca-c-01` with two-person habit.

## Monday workshop (builds ADMIN-A12)

1. **20 min** — Principal / group table.  
2. **30 min** — Issue or inspect AMQ server cert; SAN must match what SW will type.  
3. **20 min** — Trust bundle on `sim-a-01` or a stand-in; `s_client` evidence.  
4. **10 min** — Failure table: expired vs wrong hostname.

## Thursday assignment

**ADMIN-A12 — IDM + cert pack.**

## Next

**Harden and automate** — SELinux, firewalld, auditd, Ansible/PowerCLI.
