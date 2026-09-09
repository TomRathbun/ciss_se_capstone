# TLS Certificate Management

## Learning outcomes

After this module you can:

- Explain what **TLS** provides (encryption, identity, integrity) and what it does **not** (authorization, “the app is correct”)
- Identify **private key**, **certificate**, **CSR**, **CA**, **chain**, **SAN** (DNS and IP), **EKU**, **trust store**, **fullchain**, and **PKCS#12**
- Inspect certs and live endpoints with **OpenSSL 3.5** on RHEL 10.2 (`x509`, `s_client`, `verify`, `checkend`, `purpose`)
- Issue a **lab CA** leaf whose **SAN** matches the name (or IP) clients type, with **serverAuth** EKU
- **Install** that identity on a listener (`s_server`, httpd, AMQ PKCS#12, Postgres) and prove a green handshake
- Put trust in the **right store** (`update-ca-trust` vs Java PKCS#12 vs an app PEM)
- **Renew** before expiry (`checkend` + a weekly timer) instead of discovering it during an exercise
- Read **crypto-policies** and why `ssl_protocols TLSv1` dies on 10.2
- Diagnose expiry, name mismatch, incomplete chain, wrong store, **clock skew**, and “connect-by-IP” without pasting private keys
- Refuse `curl -k`, Java `trustAll`, Let’s Encrypt on an air-gapped guest, and “just disable TLS”

Three assignments: **ADMIN-A04** (inspect) · **ADMIN-A04B** (issue, break, fix) · **ADMIN-A04C** (install, watch, renew).

## Why admins care

TLS shows up on every integration path this course actually ships:

| System | TLS use on CISS |
|--------|-----------------|
| Web / REST | HTTPS (GitLab, Nexus, operator UI) |
| Databases | Postgres `sslmode` (want `verify-full`, not “SSL on”) |
| Brokers | ActiveMQ OpenWire TLS **61617** (clear 61616 is off in the hardened picture) |
| Git / packages | HTTPS to GitLab and Nexus — same CA story as the app |
| Mutual TLS | Client certs — awareness here; PRSAS detail in **admin-12** |

SE link: TLS endpoints, names, and cipher policy are **interface / NFR** concerns. Cert expiry is an **ops risk** with a calendar, not a surprise. A green handshake is **verification** (“the name and CA check”). It is not validation of the radar picture.

```text
IPsec (NET)  =  the pipe between sites
TLS  (ADMIN) =  the identity of the process on the pipe
```

NET encryptors do not replace AMQ/Postgres certificates. Both layers can be up and the Java client still fails on SAN.

```text
Issue  →  Install  →  Trust  →  Prove  →  Watch  →  Renew
 A04B      A04C      A04C      A04/C     A04C      A04C
Inspect is A04 — you cannot ticket what you cannot read.
```

---

## Mental model

```text
Client                              Server
  |                                    |
  |  ClientHello  (+ SNI server name)  |
  |  ←── server cert (+ chain) ──────  |
  |  verifies, in order:
  |    1. dates (Not Before / Not After)  ← also: is THIS host's clock sane?
  |    2. signatures up to a trust anchor
  |    3. hostname vs SAN (not CN); IP vs IP SAN if you connected by address
  |    4. key usage / EKU (serverAuth)
  |                                    |
  |  session keys → encrypted traffic  |
```

TLS gives you three properties:

| Property | Meaning |
|----------|---------|
| **Confidentiality** | Eavesdropper cannot read the bytes |
| **Integrity** | Tampering is detected |
| **Server identity** | You are talking to the name you intended, signed by a CA you trust |

It does **not** decide who may publish on `radar.input`. That is identity / HBAC / broker auth (**admin-05**, **admin-12**).

| Artifact | Role | Public? |
|----------|------|---------|
| **Private key** | Proves the server is the cert’s subject. Mode `600` or `640`. Never Git. | No |
| **Certificate** | Public. Binds the key to **names** (SAN) via a CA signature | Yes |
| **CSR** | Certificate Signing Request — public key + names, sent to the CA | Yes |
| **CA (root)** | Trust anchor. Clients must have this (or a public CA already in the bundle) | Cert yes, key **no** |
| **Intermediate** | Links server cert up to the root. Must be sent by the server or `-untrusted` | Yes |
| **fullchain** | Leaf PEM **then** CA/intermediates — what httpd/nginx often want | Yes (no key) |
| **Trust store** | Set of roots (and sometimes intermediates) **this client** will accept | Yes |
| **PKCS#12** (`.p12` / `.pfx`) | Bag: key + cert + chain. What Java / AMQ usually want | Treat as a key |

---

## RHEL 10.2 crypto (read this before pasting RHEL 7 TLS notes)

| Item | RHEL 7 | RHEL 10.2 | What breaks |
|------|--------|-----------|-------------|
| OpenSSL | 1.0.2 | **3.5** | `openssl genrsa` still works; prefer `genpkey`. Some 1.0.2 ciphers are gone |
| TLS floor | 1.0 often still accepted | **TLS 1.2+** via crypto-policies | `ssl_protocols TLSv1;` in nginx/httpd fails |
| Policy knob | Per-app config files | `update-crypto-policies --show` | DEFAULT / FUTURE / FIPS. FUTURE prefers modern suites |
| OpenSSH | `ssh-rsa` accepted | ML-KEM hybrid in 10.2 | Old clients that only offer `ssh-rsa` may not connect |
| CA bundle | `update-ca-trust` already existed | Same path, still the OS store | Java **does not** read this unless you import |

```bash
openssl version
update-crypto-policies --show
```

| Command | Meaning |
|---------|---------|
| `openssl version` | Expect **3.5.x** on 10.2. Quote it in the evidence pack |
| `update-crypto-policies --show` | Active policy name (`DEFAULT`, `FUTURE`, `FIPS`, …) |
| `update-crypto-policies --set NAME` | Privileged. Do **not** set `LEGACY` to “make the old client work” without an instructor ticket |

Course default: leave **DEFAULT**. If a Java 8 client cannot handshake, the ticket is “client too old or cipher list wrong,” not “weaken the OS.” RSA-2048 remains the lab default because program AMQ/Java 8 still sees it. ECDSA P-256 is what FUTURE prefers — optional extra, not the A04B leaf.

```bash
# optional extra — do not use as the AMQ key unless the instructor says Java can
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ec.key
```

| Flag | Meaning |
|------|---------|
| `-algorithm EC` | Elliptic-curve key instead of RSA |
| `-pkeyopt ec_paramgen_curve:P-256` | NIST P-256. Fine for 10.2 DEFAULT; confirm the Java stack before AMQ |

---

## Inspect a certificate file

```bash
openssl x509 -in server.crt -text -noout
openssl x509 -in server.crt -noout -dates -subject -issuer -serial
openssl x509 -in server.crt -noout -ext subjectAltName
openssl x509 -in server.crt -noout -purpose | head
openssl x509 -in server.crt -noout -fingerprint -sha256
openssl x509 -in server.crt -noout -checkend 0; echo "expired_now_exit=$?"
openssl x509 -in server.crt -noout -checkend $((30 * 86400)); echo "expires_in_30d_exit=$?"
chronyc tracking
timedatectl
```

| Flag | Meaning |
|------|---------|
| `-in FILE` | Read this certificate |
| `-text` | Human dump: subject, SAN, dates, extensions, signature |
| `-noout` | Do **not** reprint the PEM — inspect only |
| `-dates` | `notBefore=` / `notAfter=` |
| `-subject` / `-issuer` | Who it names / who signed it |
| `-serial` | Serial the CA assigned — quote it in the ticket so two certs are not confused |
| `-ext subjectAltName` | **SAN** — the names **and IPs** clients actually check |
| `-purpose` | OpenSSL’s view of EKU / CA bits. Look for `SSL server : Yes` |
| `-fingerprint -sha256` | SHA-256 fingerprint for out-of-band compare |
| `-checkend N` | Exit **1** if the cert expires within N seconds (0 = already expired). Use this in expiry calendars |

Read, in order:

1. **Clock** — `chronyc tracking` / `timedatectl`. A host stuck in 2020 makes every current cert look not-yet-valid.
2. **Not Before / Not After** — expired? not yet valid?
3. **SAN** — does it contain the hostname **or IP** you type in the URL / JMS URL?
4. **Issuer** — is that CA in **this client’s** trust store?
5. **Purpose / EKU** — `SSL server : Yes`. A clientAuth-only cert will fail on AMQ 61617.

CN is a label. Modern TLS stacks match **SAN**. A cert with `CN=amq-c-01` and no SAN fails when the client checks DNS names.

```text
Wrong:  "CN matches, so it is fine"
Right:  openssl x509 -noout -ext subjectAltName
        — and the name (or IP) you connect to is on that list
```

---

## Inspect a live endpoint

```bash
echo | openssl s_client -connect amq-c-01.ciss-lab.local:61617 \
  -servername amq-c-01.ciss-lab.local \
  -CAfile lab-ca.crt \
  -showcerts \
  -brief
```

Pipe the leaf into `x509` when you need dates/SAN from the wire:

```bash
echo | openssl s_client -connect git.ciss-lab.local:443 \
  -servername git.ciss-lab.local 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer -ext subjectAltName
```

| Flag | Meaning |
|------|---------|
| `-connect host:port` | TCP target. Use the **same name** the app will use |
| `-servername NAME` | **SNI** — tell the server which cert to present (one IP, many names) |
| `-CAfile FILE` | Trust this PEM for **this** command (does not change the OS store) |
| `-showcerts` | Print the whole chain the server sent, not just the leaf |
| `-brief` | One-screen handshake summary (OpenSSL 1.1+) |
| `-tls1_2` / `-tls1_3` | Force a version when you are proving policy |
| `echo \|` or `</dev/null` | Close stdin so `s_client` does not wait for you to type |

Trap: omitting `-servername` against a load balancer is how you get “works on one name, fails on the other” with a **different cert**.

Verify return at the end of `s_client` output: `Verify return code: 0 (ok)`. Non-zero is the ticket.

If the app URL is `ssl://10.50.1.17:61617`, `-connect 10.50.1.17:61617` and the SAN must list `IP:10.50.1.17`. A DNS-only SAN fails that client even if the PTR is perfect.

---

## Verify a chain (files, not the wire)

```bash
openssl verify -CAfile lab-ca.crt server.crt
openssl verify -CAfile lab-ca.crt -verify_hostname amq-c-01.ciss-lab.local server.crt

# chain with an intermediate:
openssl verify -CAfile root.pem -untrusted intermediate.pem server.crt
```

| Flag | Meaning |
|------|---------|
| `-CAfile FILE` | This PEM is the **trust anchor** (root) |
| `-untrusted FILE` | Intermediates that complete the chain. **Not** “do not trust this.” The name is historical and terrible |
| `-verify_hostname NAME` | Also check SAN/CN against this name (OpenSSL 1.1.1+) |

Say `-untrusted` out loud as **“here are the intermediates.”** Interns who skip the intermediate get `unable to get local issuer certificate` and then disable TLS.

---

## Create a key and a CSR (SAN + EKU on the request)

Course standard on 10.2 is `genpkey` (OpenSSL 3). `genrsa` still works; tickets should show `genpkey`.

```bash
umask 077
mkdir -p "$HOME/ciss-tls" && cd "$HOME/ciss-tls"

openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 \
  -out service.key

openssl req -new -key service.key -out service.csr \
  -subj "/CN=amq-c-01.ciss-lab.local/O=CISS Lab" \
  -addext "subjectAltName=DNS:amq-c-01.ciss-lab.local,DNS:amq-c-01,DNS:localhost" \
  -addext "extendedKeyUsage=serverAuth"
```

If SW or the browser will connect **by IP**, add `IP:10.50.1.17` (use the lab address from the sheet) on the same SAN line. DNS SAN does not cover a literal IP in the URL.

```bash
# same CSR, plus IP SAN — only when the client URL is an address
-addext "subjectAltName=DNS:amq-c-01.ciss-lab.local,DNS:amq-c-01,IP:10.50.1.17"
```

| Flag / bit | Meaning |
|------------|---------|
| `umask 077` | New files are mode `600` — private key never born world-readable |
| `genpkey -algorithm RSA` | OpenSSL 3 keygen (replaces teaching `genrsa` as the headline) |
| `-pkeyopt rsa_keygen_bits:2048` | 2048-bit RSA. Lab CA root may be 4096 |
| `-out FILE` | Write here |
| `req -new` | Build a CSR from that key |
| `-key FILE` | Use this private key |
| `-subj /CN=…` | Subject on the command line (no interactive prompt) |
| `-addext "subjectAltName=…"` | Put SAN **on the CSR** so the CA can copy it. `DNS:` for names, `IP:` for addresses |
| `-addext "extendedKeyUsage=serverAuth"` | This leaf is a **TLS server**. AMQ 61617 / httpd need this |

DNS names the Java client will type must be on that SAN list. If SW connects to `amq-c-01` (short) and you only put the FQDN, the handshake fails. Put **both**.

---

## Mini lab CA (this week’s skill; Dogtag/IPA is admin-12)

Air-gapped labs **cannot** use Let’s Encrypt. HTTP-01/DNS-01 needs the public ACME service. Course CA is a PEM pair you control.

```bash
cd "$HOME/ciss-tls"

# Root CA (lab only). 4096-bit, 10 years. Key stays here.
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out lab-ca.key
openssl req -x509 -new -key lab-ca.key -sha256 -days 3650 \
  -out lab-ca.crt \
  -subj "/CN=CISS-LAB-CA/O=CISS Lab" \
  -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"
```

Sign the CSR. OpenSSL 3 copies SAN (and EKU) from the CSR when you pass `-copy_extensions copy`:

```bash
openssl x509 -req -in service.csr \
  -CA lab-ca.crt -CAkey lab-ca.key -CAcreateserial \
  -out service.crt -days 825 -sha256 \
  -copy_extensions copy

openssl verify -CAfile lab-ca.crt service.crt
openssl x509 -in service.crt -noout -ext subjectAltName
openssl x509 -in service.crt -noout -purpose | head
```

| Flag | Meaning |
|------|---------|
| `req -x509` | Emit a cert directly (self-signed CA) — skip an external CA |
| `-sha256` | Sign with SHA-256 |
| `-days N` | Validity. 825 ≈ 27 months (common public-CA cap). Lab CA root 3650. Leaves you will **watch** can be 90 |
| `-addext basicConstraints=CA:TRUE` | This cert is allowed to sign other certs |
| `x509 -req` | Sign a CSR |
| `-CA` / `-CAkey` | CA cert and its private key |
| `-CAcreateserial` | Write `lab-ca.srl` so serials increment |
| `-copy_extensions copy` | Copy SAN **and** EKU from the CSR into the cert. Without this, SAN is silently dropped |
| `-nodes` | On `req`: **no DES** — do not passphrase-encrypt the key. Not “Kubernetes nodes.” systemd cannot type a passphrase at boot |

**Self-signed server cert** (`req -x509` on the *service* key) is a classroom demo only. Programs use an org CA or this lab CA. Do not invent a new trust root per intern.

**fullchain** — leaf first, then the CA (then any intermediate). httpd `SSLCertificateFile` and nginx `ssl_certificate` often want this one file:

```bash
cat service.crt lab-ca.crt > fullchain.pem
chmod 644 fullchain.pem service.crt lab-ca.crt
chmod 600 service.key lab-ca.key
```

| Piece | Order in `fullchain.pem` |
|-------|--------------------------|
| 1 | Leaf (`service.crt`) — the name the client came for |
| 2 | Issuing CA / intermediates |
| Last | Root is optional in the file the server sends; the **client** must already trust it |

Prove the handshake without httpd — `s_server` is OpenSSL’s tiny TLS listener:

```bash
# terminal 1
openssl s_server -accept 8443 -www \
  -key service.key -cert service.crt -CAfile lab-ca.crt

# terminal 2
echo | openssl s_client -connect 127.0.0.1:8443 \
  -servername amq-c-01.ciss-lab.local \
  -CAfile lab-ca.crt -brief
```

| Flag | Meaning |
|------|---------|
| `s_server -accept PORT` | Listen on this TCP port |
| `-www` | Serve a one-line HTTP response so `curl` also works |
| `-key` / `-cert` | The service identity |
| `-CAfile` on the **server** | CA the server will use if it requests a client cert |

`curl --cacert lab-ca.crt -v --resolve amq-c-01.ciss-lab.local:8443:127.0.0.1 https://amq-c-01.ciss-lab.local:8443/` — same idea, and the name in the URL matches SAN. **`curl -k` is a grading fail.**

| Flag | Meaning |
|------|---------|
| `--cacert FILE` | Trust this CA for this curl |
| `--resolve name:port:addr` | Fake DNS so the URL name matches SAN while you talk to 127.0.0.1 |
| `-k` / `--insecure` | Skip verify. **Never** in a CISS ticket |

---

## Where trust lives (three stores)

| Platform | Typical location | How you add a lab CA |
|----------|------------------|----------------------|
| RHEL 10.2 OS | `/etc/pki/tls/certs/ca-bundle.crt` (built by `update-ca-trust`) | Drop PEM in `/etc/pki/ca-trust/source/anchors/` then `sudo update-ca-trust extract` |
| Java | `$JAVA_HOME/lib/security/cacerts` **or** an app PKCS#12 | `keytool -importcert` into a **dedicated** truststore, not casual-import on a shared JDK |
| Browser | Its own store | Not the same as `curl` and not the same as the daemon’s systemd user |
| App config | Explicit PEM / PKCS#12 path (AMQ `broker.ts`, Postgres `sslrootcert`) | Prefer app-local files you can ticket |

OS install (privileged):

```bash
sudo cp lab-ca.crt /etc/pki/ca-trust/source/anchors/ciss-lab-ca.crt
sudo update-ca-trust extract
# curl and openssl now trust it without -CAfile
trust list | grep -A2 CISS || true
```

| Command | Meaning |
|---------|---------|
| `update-ca-trust extract` | Rebuild `ca-bundle.crt` from anchors + the Red Hat bundle |
| `trust list` | Show anchors the OS actually has |

Java (PKCS#12 is the course format; JKS is legacy):

```bash
keytool -importcert -noprompt \
  -alias ciss-lab-ca \
  -file lab-ca.crt \
  -keystore trust.p12 -storetype PKCS12 \
  -storepass "$TRUSTSTORE_PASS"
```

| Flag | Meaning |
|------|---------|
| `-importcert` | Add a **CA or cert**, not a private key |
| `-noprompt` | Do not ask “trust this CA?” — you already decided |
| `-alias NAME` | Nickname inside the store |
| `-file FILE` | PEM to import |
| `-keystore FILE` | The store you are writing |
| `-storetype PKCS12` | Course default. Do not create new JKS stores |
| `-storepass` | Unlock the store. From env / secret manager — **not Git**, not the ticket body |

Apps often take:

```text
-Djavax.net.ssl.trustStore=/opt/ciss/tls/trust.p12
-Djavax.net.ssl.trustStorePassword=...
-Djavax.net.ssl.trustStoreType=PKCS12
```

Password handling: environment or a root-only file the unit loads. **Never** the YAML, the runbook committed to GitLab, or a screenshot.

Distribute `lab-ca.crt` (the **cert**) via the lab GitLab project of public PEMs, Nexus, or Ansible `copy`. The CA **key** never leaves `ca-c-01` / the instructor. SW clones the cert; they do not clone the key.

---

## PKCS#12 for ActiveMQ / Java

AMQ on the PRSAS path wants a keystore (server identity) and a truststore (CA). Build the keystore from the PEM pair:

```bash
openssl pkcs12 -export \
  -in service.crt -inkey service.key \
  -certfile lab-ca.crt \
  -name amq-c-01 \
  -out broker.p12 \
  -passout env:BROKER_P12_PASS
```

| Flag | Meaning |
|------|---------|
| `-export` | Write a `.p12` |
| `-in` | Leaf certificate |
| `-inkey` | Matching private key |
| `-certfile` | Extra certs to stuff in the bag (the CA / chain) |
| `-name` | Alias Java will see |
| `-out` | The bag. Mode `600`. This **is** a key |
| `-passout env:VAR` | Read the export password from environment `VAR`. Avoid `-passout pass:secret` in a history file |

`broker.p12` goes on `amq-c-01`. `lab-ca.crt` (or `trust.p12`) goes on **every** client: sims, daemon, UI. The CA **key** stays on `ca-c-01` / the instructor.

---

## Install on a service (A04C)

`s_server` proves you can issue. **Management** is putting the files where the real process reads them and reloading it.

### httpd (mod_ssl)

```apache
# /etc/httpd/conf.d/ssl.conf  — knobs only; do not paste a whole vendor file
SSLEngine on
SSLCertificateFile      /etc/pki/tls/certs/service.crt
SSLCertificateKeyFile   /etc/pki/tls/private/service.key
SSLCertificateChainFile /etc/pki/tls/certs/lab-ca.crt
# RHEL 10.2 crypto-policies already floors TLS. Do NOT add:
# SSLProtocol all -SSLv3
# ssl_protocols TLSv1;
```

```bash
sudo install -m 644 service.crt lab-ca.crt /etc/pki/tls/certs/
sudo install -m 600 -o root -g apache service.key /etc/pki/tls/private/service.key
sudo apachectl configtest && sudo systemctl reload httpd
```

| Command | Meaning |
|---------|---------|
| `install -m MODE` | Copy and set mode in one step (better than `cp` + hope) |
| `apachectl configtest` | Parse conf **before** reload |
| `systemctl reload httpd` | New cert, keep connections where the unit allows. Restart only if reload is not enough |

### ActiveMQ 61617

Transport connector on **61617** with the PKCS#12 from above. Cleartext **61616** stays off in the hardened picture.

```xml
<!-- knobs you must recognize; exact schema follows the lab AMQ version -->
<transportConnector name="ssl"
  uri="ssl://0.0.0.0:61617?needClientAuth=false"/>
```

Broker JVM:

```text
-Djavax.net.ssl.keyStore=/opt/ciss/tls/broker.p12
-Djavax.net.ssl.keyStorePassword=...
-Djavax.net.ssl.keyStoreType=PKCS12
-Djavax.net.ssl.trustStore=/opt/ciss/tls/trust.p12
-Djavax.net.ssl.trustStorePassword=...
-Djavax.net.ssl.trustStoreType=PKCS12
```

Then `systemctl restart <amq-unit>` (AMQ typically cannot reload a keystore in place — say so in the ticket). Prove with `s_client -connect amq-c-01:61617 -servername amq-c-01 -CAfile lab-ca.crt -brief`.

### Postgres

```text
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file  = 'server.key'
ssl_ca_file   = 'lab-ca.crt'
```

| `sslmode` | Encrypts? | Verifies CA + hostname? |
|-----------|-----------|-------------------------|
| `disable` | No | No |
| `require` | Yes | **No** — this is “TLS theatre” |
| `verify-ca` | Yes | CA only |
| `verify-full` | Yes | CA **and** SAN/hostname — **course default** when TLS is on |

```bash
PGSSLMODE=verify-full PGSSLROOTCERT=/etc/pki/ca-trust/source/anchors/ciss-lab-ca.crt \
  psql "host=pg-c-01.ciss-lab.local dbname=radar user=prsas-daemon"
```

| Variable | Meaning |
|----------|---------|
| `PGSSLMODE` | libpq mode. Course: `verify-full` |
| `PGSSLROOTCERT` | PEM of the lab CA (or a bundle that contains it) |

A04C may use **`s_server` as the service** if httpd/AMQ/Postgres are not on the intern VM. Write the paths you *would* use on `amq-c-01` anyway.

---

## What apps actually configure (paths only)

| App | Knobs you should recognize | Course bar |
|-----|----------------------------|------------|
| **httpd** | `SSLCertificateFile`, `SSLCertificateKeyFile`, `SSLCertificateChainFile` | Chain file present; no `SSLProtocol` leftovers that re-enable TLS 1.0 |
| **nginx** | `ssl_certificate` (often fullchain), `ssl_certificate_key` | No `ssl_protocols TLSv1;` |
| **Postgres** | `ssl=on`, server cert/key; client `sslmode` | Client **`verify-full`** |
| **ActiveMQ** | `broker.p12` / `trust.p12`, transportConnector **61617** | No `trustAll`; SAN matches `ssl://hostname:61617` |
| **curl** | `--cacert lab-ca.crt` or the OS bundle after `update-ca-trust` | No `-k` / `--insecure` |
| **GitLab / Nexus** | HTTPS server cert + clients using the lab CA | Same CA as the apps — do not mint a second root “for the web tools” |

---

## Common failures (debug table)

| Symptom | Likely cause | First command |
|---------|--------------|---------------|
| `certificate has expired` / `not yet valid` | Dates, or the **clock** | `openssl x509 -dates`; `chronyc tracking`; `timedatectl` |
| `Hostname mismatch` / `No subject alternative names matching` | SAN ≠ URL / JMS host | `openssl x509 -noout -ext subjectAltName` vs the string in the client URL |
| Connect-by-IP fails, name works | No `IP:` SAN | Same SAN dump; look for `IP Address:` |
| `unable to get local issuer certificate` | Missing intermediate, or client has the wrong store | `openssl verify -CAfile … -untrusted …`; `s_client -showcerts` |
| `self signed certificate` | Client does not have the lab CA | `-CAfile lab-ca.crt` or `update-ca-trust` / Java import |
| Works in browser, fails in Java | Different trust stores | Import lab CA into the **app** PKCS#12; do not “fix” with `trustAll` |
| Works on host A, fails on host B | Clock skew; old bundle; different `JAVA_HOME` | `date -u` both sides; `update-crypto-policies --show` |
| Intermittent | LB / two certs; SNI missing | `s_client -servername` with each name |
| `handshake failure` / `no protocols available` | Crypto-policy vs old client (TLS 1.0) | `openssl s_client -tls1_2 -brief`; do not `--set LEGACY` |
| Java `PKIX path building failed` | Truststore does not contain the lab CA | `keytool -list -keystore trust.p12` |
| `Permission denied` reading `.key` | Mode / SELinux | `ls -lZ`; mode `600` or `640`, owner the service user |
| httpd fails after “I concatenated the chain wrong” | Root/leaf order | Leaf **first** in `fullchain.pem` |

Layer map (same idea as admin-09): DNS → route → TCP (`ss` / `nc`) → **TLS** → app protocol. Do not restart AMQ because `ping` worked.

---

## Induced failures (practice these)

You cannot claim the debug table until you have **caused** three of the rows. Use `s_server` + `s_client` so you do not need a broker yet.

| Drill | How | What the client should say |
|-------|-----|----------------------------|
| **Wrong SAN** | Issue a cert with `DNS:wrong.example` only; connect with `-servername amq-c-01` and `-verify_hostname amq-c-01` | hostname mismatch |
| **Missing CA** | Same good cert; omit `-CAfile` | self signed / unable to get local issuer |
| **Expired** | OpenSSL 3.5: `-not_before 20200101000000Z -not_after 20200102000000Z` on the leaf | certificate has expired |
| **Crypto floor** (demo) | `s_client -tls1` against a DEFAULT-policy 10.2 listener | protocol version / handshake failure |
| **Clock** (demo) | `timedatectl set-ntp false` then set a date in 2019 on a **disposable** VM only | not yet valid / expired — then `chronyc tracking` |

Expired leaf (OpenSSL 3.4+; RHEL 10.2 is 3.5):

```bash
openssl req -new -x509 -key service.key -sha256 \
  -out expired.crt \
  -subj "/CN=expired.ciss-lab.local" \
  -addext "subjectAltName=DNS:expired.ciss-lab.local" \
  -not_before 20200101000000Z \
  -not_after 20200102000000Z

openssl x509 -in expired.crt -noout -dates -checkend 0; echo "exit=$?"
```

| Flag | Meaning |
|------|---------|
| `-not_before YYYYMMDDHHMMSSZ` | Validity start (Zulu). OpenSSL 3.4+ |
| `-not_after YYYYMMDDHHMMSSZ` | Validity end. Set in the past to manufacture an expired cert |

Fix means: **re-issue with the right SAN / dates / chain**, then show `Verify return code: 0 (ok)`. It does not mean `curl -k`.

---

## Watch and renew (A04C)

Expiry during an exercise is an admin failure, not a surprise.

```bash
# /usr/local/libexec/ciss-cert-watch.sh
#!/bin/bash
set -euo pipefail
CERT=${1:?usage: ciss-cert-watch.sh /path/to.crt}
DAYS=${2:-30}

if openssl x509 -in "$CERT" -noout -checkend $((DAYS * 86400)); then
  echo "ok: $CERT has more than ${DAYS}d left"
  openssl x509 -in "$CERT" -noout -dates -subject -ext subjectAltName
  exit 0
fi

echo "WARN: $CERT expires within ${DAYS} days" >&2
openssl x509 -in "$CERT" -noout -dates -subject -issuer -serial
exit 1
```

| Bit | Meaning |
|-----|---------|
| `${1:?…}` | Fail if the cert path was omitted |
| `DAYS=${2:-30}` | Default 30-day warning. Override for a 7-day panic check |
| `checkend $((DAYS * 86400))` | Exit 1 when remaining life is under that many seconds |
| `set -euo pipefail` | Script dies on error / unset / failed pipe — not a file test |

systemd timer (weekly is enough for lab; production may be daily):

```ini
# /etc/systemd/system/ciss-cert-watch.service
[Unit]
Description=Warn if a CISS TLS cert is inside 30 days of expiry
[Service]
Type=oneshot
ExecStart=/usr/local/libexec/ciss-cert-watch.sh /etc/pki/tls/certs/service.crt 30
```

```ini
# /etc/systemd/system/ciss-cert-watch.timer
[Unit]
Description=Weekly CISS cert watch
[Timer]
OnCalendar=weekly
Persistent=true
[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ciss-cert-watch.timer
systemctl list-timers ciss-cert-watch.timer
```

| Flag / directive | Meaning |
|------------------|---------|
| `Type=oneshot` | Run, then exit — this is not a daemon |
| `OnCalendar=weekly` | systemd calendar (see `man systemd.time`) |
| `Persistent=true` | Catch up if the VM was off |
| `enable --now` | Enable and start the timer in one shot |
| `list-timers` | Next elapse — quote this in A04C |

**Renewal dry-run** (do not wait for `checkend` to fail in week 12):

1. New CSR, **same SAN list** (and EKU). New key is cleaner; same key is allowed if the old key was never exposed.
2. Sign with the lab CA (`-copy_extensions copy`).
3. Install next to the live files (`service.crt.new`), `apachectl configtest` / AMQ staging.
4. Swap + `reload` (httpd) or `restart` (AMQ).
5. `s_client` green. Keep the previous PEM for one change window.

Overlapping validity (issue 14 days before `notAfter`) is how you avoid a hard cut.

---

## Clock skew

TLS dates are compared to **this host’s** clock, not GitLab’s, not yours.

```bash
chronyc tracking
timedatectl
date -u
```

| Command | Meaning |
|---------|---------|
| `chronyc tracking` | Is chronyd in sync? Leap status, last offset |
| `timedatectl` | NTP on? timezone? |
| `date -u` | Compare two hosts in UTC |

If `timedatectl` says NTP is off and the date is 2019, **fix time first**. Re-issuing a “broken” cert will not help. Do not `timedatectl set-time` on a shared lab VM without the instructor — you will break Kerberos (**admin-05**) for everyone.

---

## Revocation on an air-gap

Public CAs publish CRLs and OCSP. An air-gapped guest **cannot** fetch `crl.rhel.example` or Let’s Encrypt OCSP. If an app “must check CRL” and the guest has no path, that is a design bug, not a `curl -k` moment.

Course bar for lab:

| Need | Do |
|------|----|
| Stop trusting a leaked leaf | Re-issue, install the new leaf, **remove** the old `.p12` / PEM from the service. Short-lived leaves beat a CRL you cannot fetch |
| Stop trusting a leaked **CA** | That is an incident. New lab CA, redistribute `lab-ca.crt`, re-issue every leaf. Instructor-held |
| Prove a leaf is current | Serial + fingerprint in the ticket; `s_client -showcerts` |

Do not build a CRL infrastructure this week. Do not point a lab service at a public OCSP URL.

---

## Worked ticket (copy this shape)

**Bad**

> TLS is broken on AMQ please disable 61617 or we cannot demo.

**Good**

```text
Host: amq-c-01.ciss-lab.local:61617
Name the client types: ssl://amq-c-01:61617
openssl version: OpenSSL 3.5.x
crypto-policies: DEFAULT
clock: chronyc tracking  — Leap status: Normal
SAN: DNS:amq-c-01.ciss-lab.local, DNS:amq-c-01   (no IP SAN; we do not connect by IP)
notAfter: 2027-03-01   checkend 30d: exit 0
s_client -servername amq-c-01 -CAfile lab-ca.crt -brief
  Verify return code: 19 (self signed certificate in certificate chain)
Cause: sim-a-01 Java truststore does not contain CISS-LAB-CA
Fix: keytool -importcert of lab-ca.crt into /opt/ciss/tls/trust.p12; restart sim
Not done: curl -k, trustAll, sslmode=require, --set LEGACY
```

That paragraph is the A04 quality bar.

---

## Operational hygiene

1. **Calendar** — `ciss-cert-watch.sh` weekly; renew before exercises, not during them.
2. **Least access to keys** — service account owner; directory `700`; key `600`/`640`.
3. **Backup** of private keys only via the approved secure process. Lab CA key is two-person / instructor-held on `ca-c-01`.
4. **Never commit** keys, PKCS#12, or `storepass` to GitLab. `.gitignore` `*.key` `*.p12` `*.jks`.
5. **Document SAN/CN** in the ICD / runbook so SW types the same string you signed.
6. **One lab CA**, not a root per intern. Distribute `lab-ca.crt` (the cert) everywhere; never the CA key.
7. **Air-gap** — no Let’s Encrypt, no public CRL fetch required for lab.
8. **Reload vs restart** — httpd can often reload; AMQ usually restart. Write which, and the verify command.

## Anti-patterns (grade down)

| Don’t | Do |
|-------|----|
| `curl -k` / `--insecure` | `--cacert lab-ca.crt` or OS anchors |
| Java `trustAll` / `InsecureTrustManager` | PKCS#12 truststore with the lab CA |
| `sslmode=require` and call it “verified” | `verify-full` |
| `update-crypto-policies --set LEGACY` | Fix the client or document a waiver |
| Let’s Encrypt on an air-gapped guest | Lab CA |
| SAN empty, hope CN is enough | `-addext subjectAltName=…` and `-copy_extensions copy` |
| Connect by IP with a DNS-only SAN | Add `IP:` or stop connecting by address |
| Commit `broker.p12` “just for the lab” | Paths in the runbook; file on the VM |
| `chmod 777` the key dir so the daemon starts | Correct owner + mode + SELinux context |
| Disable TLS on AMQ 61616 “so SW can start” | Ticket the cert; keep 61617 |
| Discover expiry during the capstone demo | `checkend` timer from week one |

## File formats (recognize)

| Extension | Typical content |
|-----------|-----------------|
| `.pem` / `.crt` | Base64 `CERTIFICATE` / `KEY` blocks |
| `.key` | Private key (mode `600`) |
| `.csr` | Signing request |
| `.p12` / `.pfx` | PKCS#12 bag (key + certs) |
| `.jks` | Legacy Java keystore — do not create new ones |
| `.srl` | CA serial file from `-CAcreateserial` |

```bash
head -1 server.crt
# -----BEGIN CERTIFICATE-----
head -1 service.key
# -----BEGIN PRIVATE KEY-----     (OpenSSL 3 PKCS#8)
# -----BEGIN RSA PRIVATE KEY----- (legacy genrsa)
```

---

## Mutual TLS (awareness)

Server cert proves the broker. **Client cert** proves the publisher. Both sides present a cert; both sides have a truststore.

| Piece | Server (AMQ) | Client (sim / daemon) |
|-------|--------------|------------------------|
| Own identity | `broker.p12` (serverAuth) | client PKCS#12 (clientAuth EKU) |
| Trust | lab CA (+ client CA if different) | lab CA |
| Extra | `needClientAuth=true` (or equivalent) | Send the client cert |

Full mTLS on PRSAS is **extra credit this week** and required thinking in **admin-12**. Do not skip *server* TLS because mTLS did not land.

---

## Monday workshop (builds A04 + A04B + A04C)

1. **15 min** — `openssl version`, `update-crypto-policies --show`, `chronyc tracking`. Inspect a live lab HTTPS or the instructor’s `s_server`. Record subject, issuer, SAN, dates, serial, purpose. Flag table in the notebook. **That is A04 started.**
2. **25 min** — Stand up the mini lab CA; issue a SAN+EKU cert for `amq-c-01.ciss-lab.local` **and** `amq-c-01`. `-copy_extensions copy`. Paste SAN dump.
3. **15 min** — `s_server` + `s_client -CAfile` green; then omit `-CAfile` and paste the error (not the key).
4. **15 min** — Wrong-SAN re-issue; hostname mismatch evidence; fix; green again. **A04B.**
5. **20 min** — Install on `s_server` or httpd; drop in `ciss-cert-watch.sh`; `systemctl list-timers` or show `bash -n` + a dry run with `checkend 0` on the expired demo cert. Trust-distribution sentence (how SW gets `lab-ca.crt`). **A04C.**

Thursday: all three write-ups. A04 can use a public or lab endpoint. A04B and A04C must use **your** CA. No keys in GitLab.

## Drill (if no extra assignment hour)

1. `s_client` against a lab HTTPS endpoint (or `s_server`).
2. Record subject, issuer, notAfter, SANs, verify return code, clock.
3. Generate lab CA + leaf with SAN for `localhost` and EKU `serverAuth`.
4. Three-bullet: why Java might reject a cert Firefox accepts.
5. Name `sslmode=require` vs `verify-full`.
6. What does `checkend $((30*86400))` exiting 1 mean, and what is the fix (not `-k`).

## Integrity

- Lab / self-signed material is for training — not for impersonating real services outside the lab.
- No production private keys on intern laptops without written authorization.
- No classified or real program hostnames in public GitLab submissions — use `ciss-lab.local`.
- No keys, PKCS#12, or store passwords in the write-up. Redact `s_client` output if it ever echoed a secret (it should not).
- `curl -k` and `trustAll` in a screenshot is an integrity fail, not a workaround.
- Do not change the clock on a shared VM to “demo skew” without the instructor.

## Further reading

| Topic | Source |
|-------|--------|
| OpenSSL | `man openssl` · `man x509` · `man s_client` · `man verify` |
| TLS concepts | [MDN — Transport Layer Security](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) |
| SAN | [RFC 5280 §4.2.1.6](https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.6) |
| Let’s Encrypt / ACME | [letsencrypt.org/docs](https://letsencrypt.org/docs/) — conceptual; **not** the lab CA |
| Java JSSE | Search “Java Secure Socket Extension reference guide” |
| RHEL crypto-policies | `man crypto-policies` · `update-crypto-policies --show` |
| RHEL trust | `man update-ca-trust` |
| Postgres `sslmode` | [libpq SSL support](https://www.postgresql.org/docs/current/libpq-ssl.html) |
| systemd timers | `man systemd.timer` · `man systemd.time` |

## Next

**Identity Management — Active Directory and FreeIPA** — central accounts, Kerberos, SSSD, HBAC. Certs in IPA/Dogtag wait until **admin-12**; this week you already know how to inspect, issue, install, and watch PEM.
