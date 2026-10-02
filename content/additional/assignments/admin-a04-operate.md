# ADMIN-A04C — Install, Watch, Renew

**Weight:** 10% · **Due:** After admin-04-tls-certs · **Module:** admin-04-tls-certs

## Prompt

Issuing a cert into `$HOME/ciss-tls` is not operations. **Install** the A04B identity on a listener, **watch** expiry, and **dry-run a renewal**. Air-gapped CISS does not grow a public CRL this week.

If httpd / AMQ / Postgres are not on your VM, `openssl s_server` is an accepted listener — still write the **paths and unit names** you would use on `amq-c-01`.

Reuse the lab CA from **ADMIN-A04B**. Do not mint a second root.

## Deliverables

1. **Install pack.** Commands that copy `service.crt` / `service.key` / `lab-ca.crt` (or `broker.p12`) into place with modes (`install -m 600` for the key). Name the process that reads them (`s_server`, `httpd`, AMQ unit, `postgres`). `reload` vs `restart` — pick one and say why.

2. **Green after install.** `s_client -connect … -servername … -CAfile lab-ca.crt -brief` with `Verify return code: 0 (ok)` **against the installed listener**, not only against files in `$HOME`. If you used `s_server`, say the port and that this stands in for 61617.

3. **Trust distribution.** How every client (sim, daemon, intern laptop `curl`) gets `lab-ca.crt` without ever seeing `lab-ca.key`. One of: GitLab repo of **public** PEMs, Nexus, Ansible `copy`, `update-ca-trust` on a disposable guest. Explicit: Java does not read the OS bundle unless you import.

4. **30-day watch.** The `ciss-cert-watch.sh` script from the module (or equivalent) **and** either:
   - a systemd **timer** (`list-timers` excerpt), **or**
   - `bash -n` on the script plus a cron line you would install.
   Show a **failing** run against the expired demo cert from A04B (`checkend` exit 1) and a **passing** run against the live leaf.

5. **Renewal dry-run.** New CSR, **same SAN + EKU**, sign, stage (`service.crt.new`), swap, prove green again. Two sentences: why you issue before `notAfter`, and whether this service reloads or restarts.

6. **Air-gap revocation note.** Four sentences: you will not fetch a public CRL/OCSP; how you retire a leaked **leaf** (replace + remove old PEM/PKCS#12); who holds the CA key if the CA itself is burned.

7. **Runbook stub** (½ page) another intern can follow at 02:00: paths, unit, verify command, rollback (previous PEM). No passwords.

## Quality bar

- Key mode `600`/`640`; no world-readable `.key` / `.p12`.
- Verify command uses `-CAfile` or the real app truststore — not `curl -k`.
- Timer/script uses `checkend`, not “I will remember.”
- Renewal keeps the SAN list; a “renewal” that changes the hostname is a re-issue with a different identity — say so if you did that.
- No keys, PKCS#12, or store passwords in GitLab.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| install | 15 | Files in place; modes; reload/restart; green s_client on the listener |
| operate | 10 | Watch script + failing and passing checkend; renewal dry-run |
| communication | 5 | Runbook; trust distribution; no secrets |
