# TLS Certificate Management

## Learning outcomes

After this module you can:

- Explain what **TLS** provides (encryption, identity, integrity)  
- Identify **certificate**, **private key**, **CSR**, **CA**, and **trust store**  
- Inspect certs with **OpenSSL** (`x509`, dates, SANs, issuer)  
- Describe how apps trust CAs (OS store, Java `cacerts`, custom truststores)  
- Avoid common failures: expired certs, name mismatch, incomplete chain, wrong trust  

## Why admins care

TLS shows up everywhere in integration:

| System | TLS use |
|--------|---------|
| Web / REST | HTTPS |
| Databases | Postgres `sslmode` |
| Brokers | ActiveMQ SSL / AMQPS |
| Git / package | HTTPS to GitLab, Nexus |
| Mutual TLS | Client certs (advanced) |

SE link: TLS endpoints and cipher policy are **interface / NFR** concerns; cert expiry is an **ops risk**.

## Mental model

```text
Client                              Server
  |                                    |
  |  ←── server cert (+ chain) ──────  |
  |  verifies: signatures, dates,      |
  |  hostname (SAN), trust anchor      |
  |                                    |
  |  session keys → encrypted traffic  |
```

| Artifact | Role |
|----------|------|
| **Private key** | Secret; never leave the server / HSM; never commit to Git |
| **Certificate** | Public; binds key to identity (names) via CA signature |
| **CSR** | Certificate Signing Request — public key + names, sent to CA |
| **CA** | Certificate Authority that signs certs |
| **Chain / intermediate** | Links server cert up to a trusted root |
| **Trust store** | Set of root/intermediate CAs the client trusts |

## OpenSSL survival commands

### Inspect a certificate file

```bash
openssl x509 -in server.crt -text -noout
openssl x509 -in server.crt -noout -dates -subject -issuer
openssl x509 -in server.crt -noout -ext subjectAltName
```

Check:

1. **Not Before / Not After** — expired?  
2. **Subject** and **SAN** — does it match the hostname you connect to?  
3. **Issuer** — do you trust that CA?  

### Inspect a remote HTTPS endpoint

```bash
openssl s_client -connect host.example.com:443 -servername host.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -subject -issuer
```

```bash
echo | openssl s_client -connect host.example.com:443 -servername host.example.com 2>/dev/null | openssl x509 -noout -text | head
```

### Verify a chain

```bash
openssl verify -CAfile lab-root.pem server.crt
# or with intermediates:
openssl verify -CAfile root.pem -untrusted intermediate.pem server.crt
```

### Fingerprint (compare out-of-band)

```bash
openssl x509 -in server.crt -noout -fingerprint -sha256
```

## Creating a lab key + CSR (practice only)

```bash
openssl genrsa -out service.key 2048
chmod 600 service.key

openssl req -new -key service.key -out service.csr \
  -subj "/CN=service.ciss-lab.local/O=CISS Lab"
```

For modern hostnames, prefer a config with **subjectAltName** (SAN). Ask the lab for the standard CSR template — programs often require SAN = FQDN.

**Self-signed** (lab only):

```bash
openssl req -x509 -new -nodes -key service.key -sha256 -days 365 \
  -out service.crt -subj "/CN=service.ciss-lab.local"
```

Production uses an organizational CA or public CA — you rarely invent trust roots yourself.

## Where trust lives

| Platform | Typical trust location |
|----------|------------------------|
| RHEL | `/etc/pki/tls/certs/ca-bundle.crt` (update via `ca-certificates` / yum) |
| Java | `$JAVA_HOME/lib/security/cacerts` (or custom truststore) |
| Browser | Own store (not the same as your service account) |
| App config | Explicit path to PEM / JKS / PKCS12 |

### Java truststore (awareness)

```bash
keytool -list -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit | head
# Import lab CA only with explicit process — don't casual-import on shared JDKs
```

Applications may use:

```text
-Djavax.net.ssl.trustStore=/path/truststore.jks
-Djavax.net.ssl.trustStorePassword=...
```

Password handling: env / secrets manager — **not** Git.

## Common failures (debug table)

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| `certificate has expired` | Dates | `openssl x509 -dates` |
| `hostname doesn't match` | SAN/CN ≠ URL host | SAN list vs `https://name` |
| `unable to get local issuer` | Missing intermediate / wrong trust | Chain files; trust store |
| Works in browser, fails in Java | Different trust stores | Import lab CA into Java truststore (process!) |
| Works on one host, not another | Clock skew; old CA bundle | `date -u`; `update-ca-trust` (privileged) |
| Intermittent TLS | LB multi-cert; SNI | `s_client -servername` |

## File formats (recognize)

| Extension | Typical content |
|-----------|-----------------|
| `.pem` / `.crt` | Base64 CERTIFICATE / KEY blocks |
| `.key` | Private key (protect mode `600`) |
| `.csr` | Signing request |
| `.p12` / `.pfx` | PKCS#12 bundle (key + certs) |
| `.jks` | Java keystore |

```bash
# PEM detect
head -1 server.crt
# -----BEGIN CERTIFICATE-----
```

## Operational hygiene

1. **Calendar expiry** — track Not After; renew before ops events.  
2. **Least access to keys** — dedicated service account; restricted directory.  
3. **Backup** private keys only via approved secure process.  
4. **Never commit** keys or full keystores to Bitbucket/GitLab.  
5. **Document** which CN/SAN a service needs (ICD / runbook).  

## Drill (40 min)

1. Use `openssl s_client` against a lab HTTPS endpoint (or `https://example.com`).  
2. Record: subject, issuer, notAfter, SANs.  
3. Generate a **lab-only** key + self-signed cert for `localhost`.  
4. Explain in three bullets why a Java app might not trust a cert the browser accepts.  
5. Optional: list whether Postgres/ActiveMQ lab configs mention SSL (paths only, no secrets).  

## Integrity

- Lab/self-signed certs are for training — not for impersonating real services outside the lab.  
- No production private keys on student laptops without explicit authorization.  
- No classified hostnames in public submissions.

## Further reading

| Topic | Source |
|-------|--------|
| OpenSSL | `man openssl` · `man x509` |
| TLS concepts | [MDN — Transport Layer Security](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) |
| Let’s Encrypt / ACME (public web) | [letsencrypt.org/docs](https://letsencrypt.org/docs/) — conceptual; programs use internal CAs |
| Java JSSE | Search “Java Secure Socket Extension reference guide” |
| RHEL crypto | RHEL security / `update-ca-trust` docs |

## Next

Return to **System Administration & Integration — Track Overview**, or continue Software track services (Postgres, ActiveMQ) using TLS-aware configs when the lab enables them.
