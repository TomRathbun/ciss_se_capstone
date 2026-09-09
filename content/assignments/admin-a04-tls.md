# ADMIN-A04 — TLS Certificate Inspection Lab

**Weight:** 10% · **Due:** After admin-04-tls-certs · **Module:** admin-04-tls-certs

## Prompt

Inspect a real or lab TLS endpoint the way an admin writes a ticket: commands, SAN, chain, crypto-policy, and what actually breaks when trust fails. This assignment is **read/inspect**. Issuing certs is **ADMIN-A04B**.

## Deliverables

1. **Platform note.** On the RHEL 10.2 (or Rocky/Alma 10) guest: `openssl version` (expect 3.5.x) and `update-crypto-policies --show`. One sentence on why a RHEL 7 `ssl_protocols TLSv1` snippet would fail here.

2. **Certificate report** for one endpoint **or** a PEM the instructor dropped. Include **commands** (not just answers):
   - subject, issuer
   - `notBefore` / `notAfter`
   - **SAN** (`-ext subjectAltName`)
   - SHA-256 fingerprint
   - `-checkend 0` and `-checkend $((30*86400))` with the exit status interpreted

3. **Live handshake** (`s_client`) against that name:port (or `s_server` if no lab service). Show:
   - `-connect` and `-servername` (SNI)
   - `Verify return code`
   - whether you used `-CAfile` or the OS bundle

4. **Chain check.** `openssl verify -CAfile …` (and `-untrusted` if there is an intermediate). State which trust store this client is using (OS bundle / `-CAfile` / Java PKCS#12). Define `-untrusted` in one sentence (it is **not** “do not trust”).

5. **Failure table (four rows, not three):** symptom, likely cause, first command. Must include **expiry**, **SAN/name mismatch**, **incomplete chain / missing CA**, and **Java vs OS trust** (or crypto-policy / TLS 1.0).

6. **Ops impact.** What breaks for **HTTPS**, **Postgres `sslmode`**, and **AMQ 61617** when trust fails. Explicitly contrast `sslmode=require` vs `verify-full`.

7. **Anti-pattern list (five).** Include `curl -k`, Java `trustAll`, Let’s Encrypt on an air-gapped guest, and committing a `.p12`.

Redacted outputs only. **No private keys, no PKCS#12, no store passwords.**

## Quality bar

- Every OpenSSL flag you use appears in your notes with a meaning (course rule: flags in examples are in a table).
- SAN is discussed; CN-only reasoning is a fail.
- Advice is actionable in a ticket (command + expected result).
- Honest if the lab endpoint was down: use `s_server` or a PEM and say so.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| inspection | 15 | OpenSSL 3.5 evidence: dates, SAN, s_client, verify, checkend |
| diagnosis | 10 | Four failure rows accurate; require vs verify-full |
| communication | 5 | Ticket-ready; flags named; no secrets |
