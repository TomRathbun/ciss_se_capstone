# ADMIN-A04B — Lab CA: Issue, Break, Fix

**Weight:** 15% · **Due:** After admin-04-tls-certs · **Module:** admin-04-tls-certs

## Prompt

Air-gapped CISS labs do not call Let’s Encrypt. You are the CA for the week. Issue a server certificate with a **SAN the client will actually type** and **serverAuth** EKU, prove a handshake, then **break it three ways and fix it**. Installing onto httpd/AMQ/Postgres and the 30-day watch is **ADMIN-A04C**.

Work in `$HOME/ciss-tls` (or an instructor path). Do not put the CA private key anywhere SW or NET can clone.

## Deliverables

1. **Lab root CA.** Commands to create `lab-ca.key` + `lab-ca.crt` (RSA 4096, `CA:TRUE`, ~10 years). Show `chmod`/umask. State where the CA **key** lives and who may copy it (answer: almost nobody).

2. **Server identity with SAN + EKU.** `genpkey` 2048 + CSR + signed leaf for a lab name. SAN **must** include both the FQDN and the short name (example: `amq-c-01.ciss-lab.local` **and** `amq-c-01`). If you will connect by IP, also `IP:…`. Use `-addext subjectAltName=…` and `-addext extendedKeyUsage=serverAuth` on the CSR, and `-copy_extensions copy` on `x509 -req`. Paste:
   - `openssl x509 -noout -ext subjectAltName`
   - `openssl x509 -noout -purpose` (expect `SSL server : Yes`)

3. **fullchain.** `cat service.crt lab-ca.crt > fullchain.pem`. One sentence: why the **leaf is first**.

4. **Green handshake.** `openssl s_server` (or the real AMQ/httpd if the instructor has it up) + `s_client -CAfile lab-ca.crt -servername … -brief`. Show `Verify return code: 0 (ok)`. Optional: `curl --cacert lab-ca.crt` — **not** `curl -k`.

5. **PKCS#12 command** you *would* use for AMQ `broker.p12` (`pkcs12 -export` with `-passout env:…`). Do not attach the file. Do not put the password in the write-up.

6. **Induced failures (three, with evidence).** Cause, paste the **client** error (redact nothing except secrets — there should be none), then fix and show green again:
   1. **Wrong SAN** (cert for `wrong.example`, connect as `amq-c-01`)
   2. **Missing CA** (omit `-CAfile` / empty truststore)
   3. **Expired leaf** (`-not_before` / `-not_after` in the past on OpenSSL 3.5) **or** incomplete chain (`-untrusted` omitted)

7. **Key handling.** Directory listing (`ls -l`, no `cat` of keys). Confirm `*.key` / `*.p12` are **not** in Git. One paragraph: how SW gets `lab-ca.crt` (the cert) without ever seeing `lab-ca.key`.

8. **SE note.** Four sentences: what a green handshake **verifies**, and what it does **not** prove (authorization, correct radar data, IPsec).

## Quality bar

- SAN matches the hostname in `-servername` / the URL SW will type.
- `-copy_extensions copy` (or an equivalent extfile) is visible — a leaf with an empty SAN is a fail.
- EKU / purpose shows SSL server.
- Fixes re-issue or install trust. They do **not** add `-k`, `trustAll`, or `sslmode=require`.
- CA private key never appears in the write-up, a screenshot, or GitLab.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| issue | 15 | Lab CA + SAN + EKU leaf; copy_extensions; key modes; fullchain order |
| prove | 10 | Green s_client; three induced failures with fix |
| communication | 5 | No secrets; SW can consume lab-ca.crt |
