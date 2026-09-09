# Package Management Systems

## Learning outcomes

After this module you can:

- Choose the right **package manager** for OS vs language ecosystems  
- Use **DNF 5** (RHEL 10.2) and **RPM** to query/install/update packages safely  
- Translate leftover **yum** habits from RHEL 7 runbooks  
- Use **npm**, **pip** / **uv**, and **Maven** for app dependencies  
- Install and update packages in **offline / air-gapped** labs (ISO, `file://` repo, USB bag of RPMs, Nexus inside the enclave)  
- Explain how **Nexus** proxies and hosts packages for the program  
- Avoid polluting systems (venv, user installs, version pins)  

## Why this matters

Integration breaks when hosts have “mystery” library versions. Package managers give you:

| Benefit | Example |
|---------|---------|
| Repeatability | Same version on lab and demo |
| Provenance | What RPM/jar was installed? |
| Updates | Security patches via channels |
| Isolation | Python venv / Node project `node_modules` |

SE link: dependency versions are **design constraints**; pin them when they affect behavior under test.

## Map of package systems

| Manager | Ecosystem | Typical on RHEL 10.2 lab |
|---------|-----------|--------------------------|
| **dnf** / **rpm** | OS packages (RHEL 10.2, DNF 5) | `sudo dnf install …` |
| **yum** | Compatibility wrapper around DNF 5 | Do not teach it; rewrite to `dnf` |
| **npm** | Node.js / JavaScript | Front-end / tools (AppStream Node 24 available) |
| **pip** | Python 3.12+ (AppStream 3.14) | Scripts, CLIs, services |
| **uv** | Python (modern, fast) | Preferred new Python workflows |
| **Maven** / **Gradle** | Java | App deps + build (SW track) |
| **Nexus** | Org-wide artifact proxy/host | Mirrors all of the above often |

```text
Language app deps          OS packages
      │                        │
  npm / pip / uv / Maven      dnf / rpm
      │                        │
      └────────►  Nexus  ◄─────┘
                   ▲
              CI (GitLab) publish
```

---

## DNF 5 / RPM (RHEL 10.2)

**RPM** = package file format. **DNF 5** = dependency resolver + repo client. On RHEL 7 this job was **yum**. On RHEL 8/9 it was DNF 4 (`dnf` with a `yum` alias). RHEL 10 ships **DNF 5**.

The `yum` command may still exist as a wrapper. **Course standard is `dnf`.** Interns who type `yum` in tickets will be asked to rewrite.

### Query

```bash
dnf --version
rpm -q bash
rpm -ql bash | head          # files owned by package
rpm -qf $(command -v sshd)   # which package owns this file?
dnf provides /usr/sbin/sshd
dnf list installed | head
dnf info httpd
dnf search nmap
dnf history
```

### Install / update / remove (privileged)

```bash
sudo dnf install -y tree
sudo dnf upgrade -y <package>
sudo dnf remove -y tree
sudo dnf clean all
dnf needs-restarting -r      # does this host need a reboot?
```

| Habit | Why |
|-------|-----|
| Read `dnf info` before install | Size, repo, version |
| Prefer distro packages for system tools | Supported, patched |
| Don’t disable GPG checks | Supply-chain safety |
| Record what you installed | Lab notes / DR description / `dnf history` |
| Check `needs-restarting` after kernel/glibc | 10.2 livepatch may cover some kernels; still verify |

### Repos

```bash
dnf repolist
ls /etc/yum.repos.d/
ls /etc/dnf/
```

Repo definition files still live under **`/etc/yum.repos.d/`** even though the client is DNF 5. Program hosts may point at **internal mirrors / Nexus raw or yum repos**. If `dnf` fails, check repo URLs and subscription/mirror access — same class of problem as Maven + Nexus.

### AppStreams (languages and databases)

RHEL 10.2 Application Streams (install with instructor approval):

| Stream | 10.2 notes |
|--------|------------|
| Python | System 3.12+; **Python 3.14** stream available |
| Node.js | **24** |
| PostgreSQL | **18** (`postgresql` module / packages; service name may be `postgresql-18`) |
| OpenJDK | 21 LTS default family; **25** stream |
| PHP | 8.4 |
| Git | 2.51+ |

Do not mix a stream JDK with the program’s documented Java 8 alternative without writing `JAVA_HOME` in the runbook.

---

## Offline and air-gapped labs

CISS / PRSAS guests often **cannot reach cdn.redhat.com, PyPI, npmjs.com, or Maven Central**. “It worked on my laptop on hotel Wi-Fi” is not an install plan.

> **Instructor note:** Spend 15 minutes here. Interns who only know `dnf install tree` freeze the first time the CDN is unreachable.

### Two different words that both say “offline”

| Phrase | What it means | When you use it |
|--------|---------------|-----------------|
| **Air-gapped / offline environment** | No path to the public internet (or even to Satellite). Packages must already be *inside* the enclave. | Almost every program lab. **This section.** |
| `dnf install --offline` / `dnf offline reboot` | DNF 5 **reboot-safe transaction**: download/prepare now, apply at next boot in a minimal environment. The box may still have network. | Kernel / glibc upgrades you do not want to apply under a running Java/AMQ stack. **Not** a substitute for an air-gap repo. |

Say both names out loud. Interns mix them the same way they mix `set -e` and `[[ -e ]]`.

### Preferred sources (pick the highest that exists)

```text
1. Program Nexus / Satellite / HTTP mirror   ← still “offline” from the internet
2. RHEL 10.2 DVD ISO (BaseOS + AppStream)    ← file:// or internal httpd/nfs
3. USB / NFS bag of RPMs + createrepo_c      ← one package family, one transfer
```

Do **not** set `gpgcheck=0` to “make the ISO work.” Import the key; leave checks on.

### Pattern A — mount the DVD / ISO (no createrepo needed)

The 10.2 DVD already has `repodata/` under `BaseOS/` and `AppStream/`.

```bash
sudo mkdir -p /mnt/iso
sudo mount -o loop,ro /media/rhel-10.2-x86_64-dvd.iso /mnt/iso
ls /mnt/iso/BaseOS /mnt/iso/AppStream
```

```ini
# /etc/yum.repos.d/lab-iso.repo
[lab-iso-baseos]
name=Lab ISO BaseOS
baseurl=file:///mnt/iso/BaseOS
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release

[lab-iso-appstream]
name=Lab ISO AppStream
baseurl=file:///mnt/iso/AppStream
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
```

```bash
sudo dnf clean metadata
dnf repolist
sudo dnf install -y tree --disablerepo='*' --enablerepo='lab-iso-*'
```

On Rocky/Alma 10 clones the ISO layout is the same idea; the GPG key path is the clone’s key under `/etc/pki/rpm-gpg/`. Quote `VERSION_ID` first.

| Flag / field | Meaning |
|--------------|---------|
| `mount -o loop,ro` | Treat the ISO as a block device; **r**ead-**o**nly |
| `baseurl=file:///…` | Local path (three slashes: `file://` + `/mnt/…`) |
| `gpgcheck=1` | Refuse unsigned / wrong-key RPMs |
| `--disablerepo='*'` | Ignore CDN / leftover repos (the `*` is quoted so the shell does not glob) |
| `--enablerepo='lab-iso-*'` | Only the ISO repos we just defined |
| `dnf clean metadata` | Drop stale CDN metadata that would otherwise time out |

To serve the same tree to many guests, copy `BaseOS/` and `AppStream/` to an internal httpd/NFS export and change `baseurl=` to `http://mirror.ciss-lab.local/rhel10/BaseOS`. Do not invent a public URL.

### Pattern B — USB bag of RPMs (one package + dependencies)

On a **connected** jump host (or the lab bastion that *can* see Nexus/Satellite):

```bash
sudo dnf install -y 'dnf-command(download)' createrepo_c
mkdir -p /media/usb/rpms && cd /media/usb/rpms
dnf download --resolve --alldeps --destdir=/media/usb/rpms tree
createrepo_c /media/usb/rpms
```

RHEL 7 muscle memory was `yumdownloader --resolve` from `yum-utils`. That package is gone. Course verb is `dnf download`.

Walk the USB (or NFS) to the air-gapped guest:

```ini
# /etc/yum.repos.d/usb.repo
[usb]
name=USB bag
baseurl=file:///media/usb/rpms
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
```

```bash
sudo dnf --disablerepo='*' --enablerepo=usb install -y tree
```

One-shot without a repo file (no further deps allowed to be fetched):

```bash
sudo dnf install --disablerepo='*' /media/usb/rpms/*.rpm
```

`dnf install ./tree-*.rpm` **without** `--disablerepo='*'` will still try the CDN for missing deps and hang. That is the usual air-gap failure.

| Flag | Meaning |
|------|---------|
| `dnf download` | Write RPMs to disk; do **not** install |
| `--resolve` | Also download dependencies that are not already installed on *this* jump host |
| `--alldeps` | With `--resolve`, download **every** dep even if the jump host already has it (needed so the air-gapped guest is complete) |
| `--destdir=DIR` | Where the RPMs land (DNF 5 name; not `-p`) |
| `createrepo_c DIR` | Build `repodata/` so DNF can resolve from that directory |
| `--disablerepo='*'` | Do not talk to any configured network repo |

`--alldeps` is required when the jump host is not identical to the guest (different `dnf history`, different AppStream). Prefer it for USB bags.

### Pattern C — keep the DNF cache (repeat installs, still no CDN)

```bash
# /etc/dnf/dnf.conf  (snippet)
keepcache=True
```

```bash
sudo dnf install -y --cacheonly tree     # use RPMs already in /var/cache/libdnf5 ; fail if missing
```

| Flag / key | Meaning |
|------------|---------|
| `keepcache=True` | Do not delete RPMs from the cache after install |
| `--cacheonly` | Never hit the network; succeed from cache or fail |

This is a **same-host** convenience, not a transfer method. Do not assume `/var/cache` survived a golden-image clone.

### Pattern D — program Nexus / Satellite (still air-gapped from the internet)

This is the steady-state. Guests point **only** at the internal hub:

```bash
dnf repolist
# expect something like:
# rhel-10-baseos     Nexus / Satellite  …  rhel-10-for-x86_64-baseos-rpms
# rhel-10-appstream  Nexus / Satellite  …  rhel-10-for-x86_64-appstream-rpms
```

If `dnf install` hangs ~30s then fails, it is almost always: wrong `baseurl`, expired cert/cred, or a leftover CDN repo still `enabled=1`. Fix the `.repo` file; do not disable GPG.

Satellite/capsule and Nexus **yum/dnf hosted** are the same idea: one inside-the-wire URL, many guests.

### Language ecosystems go air-gapped too

A lockfile is not a package. You still have to *carry the bits*.

| Ecosystem | On the connected host | On the air-gapped guest |
|-----------|----------------------|-------------------------|
| **npm** | `npm ci` against Nexus, or `npm pack` + tarball the `node_modules` you will actually run | `npm ci --offline` (needs a populated cache) or unpack the vendor tarball. Registry = Nexus npm group, never registry.npmjs.org |
| **pip / uv** | `python -m pip download -r requirements.txt -d wheels/` | `python -m pip install --no-index --find-links=./wheels -r requirements.txt` |
| **Maven** | `mvn -B -DskipTests dependency:go-offline` (fills `~/.m2/repository`) | `mvn -o -B package` (`-o` = **o**ffline — fail if anything is missing from `~/.m2`) |
| **Java 8 alternative** | Carry the documented JDK tarball / vendor RPM; do not `dnf install java-1.8.0-openjdk` and hope | Same tarball; record `JAVA_HOME` |

```bash
# pip: flags in the commands above
python -m pip download -r requirements.txt -d wheels/
python -m pip install --no-index --find-links=./wheels -r requirements.txt

# Maven
mvn -B -DskipTests dependency:go-offline
mvn -o -B package
```

| Flag | Meaning |
|------|---------|
| `pip download -d DIR` | Fetch wheels into DIR; do not install |
| `--no-index` | Do not hit PyPI / the configured index |
| `--find-links=DIR` | Only look in this directory of wheels |
| `mvn -o` | **O**ffline: use `~/.m2` only |
| `mvn -B` | **B**atch — no interactive prompts |
| `npm ci --offline` | Install from lockfile + local cache; fail if the cache is incomplete |

SE link: the **transfer artifact** (ISO, USB repo, Nexus hosted repo, wheelhouse tarball) is a configuration item. Name it, version it, and say which DR produced it.

---

## Node — npm

```bash
node -v
npm -v
```

Project-local install (preferred):

```bash
cd my-ui
npm install                 # reads package.json / lockfile
npm ci                      # clean CI install from lockfile
npm install lodash --save
npm test
npm run build
```

| File | Role |
|------|------|
| `package.json` | Declared deps and scripts |
| `package-lock.json` / `npm-shrinkwrap` | Pinned tree — **commit it** |
| `node_modules/` | Installed tree — **don’t commit** |

```bash
npm config get registry
# Program may set registry to Nexus npm group URL
# Air-gapped: npm ci --offline  (see Offline section)
```

---

## Python — pip and uv

RHEL 10.2 has **no Python 2**. `/usr/bin/python` is Python 3. Shebangs `#!/usr/bin/python` must be 3-safe.

### pip + venv (classic)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install requests
python -m pip freeze > requirements.txt
```

```bash
python -m pip install -r requirements.txt
deactivate
```

Never `sudo pip install` into system Python on shared hosts unless policy says so. Never `sudo dnf remove python3` to “clean up.”

### uv (modern)

[uv](https://github.com/astral-sh/uv) is a fast Python package/env manager used increasingly in labs.

```bash
# install per upstream docs / lab image
uv venv
source .venv/bin/activate
uv pip install requests
uv pip compile pyproject.toml -o requirements.txt   # if using that workflow
```

| Prefer | Avoid |
|--------|-------|
| Project venv / uv env | Global installs mixed for many apps |
| Pin versions for services | Floating `package` with no bound on production |
| Internal index when provided | Random unpinned git URLs in production |

```bash
pip config list
# index-url may point at Nexus PyPI proxy
```

---

## Java — Maven (and friends)

Covered deeply in the Software track; admin view:

```bash
mvn -v
mvn -B -DskipTests package
mvn -B dependency:tree
```

On RHEL 10.2 the OS JDK is **not** Java 8. If the program still runs JBoss/AMQ on Java 8, that runtime is a documented tarball or alternative package — record `java -version` and `echo $JAVA_HOME` in every evidence pack.

| File | Role |
|------|------|
| `pom.xml` | Deps + plugins |
| `~/.m2/settings.xml` | **Nexus** mirrors, credentials |
| `~/.m2/repository/` | Local cache |

```bash
# settings.xml points at Nexus group "maven-public"
```

Gradle is analogous (`build.gradle`, caches under `~/.gradle`).

---

## Nexus (admin perspective)

| Nexus feature | Use |
|---------------|-----|
| **Proxy** repos | Cache Maven Central, npm, PyPI |
| **Hosted** repos | Your CI-published jars |
| **Group** repos | Single URL for apps to use |
| **yum/dnf hosted** | Internal RPM mirrors for air-gapped labs |

When a build fails with “Could not resolve…”:

1. Network / VPN  
2. Wrong Nexus URL in `settings.xml` / `.npmrc` / pip index  
3. Auth expired  
4. Artifact not yet published  
5. Version typo  

Coordinate with **GitLab CI/CD** (SW track CI module): the pipeline often publishes; apps consume.

---

## Choosing a manager (decision table)

| You need to… | Use |
|--------------|-----|
| Install `tree`, `git`, `httpd` on RHEL 10.2 | **dnf** |
| Add a JS charting library to a UI | **npm** in that project |
| Run a Python health-check script | **venv + pip** or **uv** (Python 3 only) |
| Build a Java service | **Maven/Gradle** (+ Nexus) |
| Share an internal Java library | Publish to **Nexus** hosted repo |
| Patch OpenSSL on the OS | **dnf** (not pip) |
| Run a container experiment | **podman** (not `docker` as the lab default) |

---

## Drill (40 min)

1. On the RHEL 10.2 lab: `dnf info` a package; show whether it is installed (`rpm -q`). Capture `dnf --version`.  
2. Show `dnf history` (or explain why it is empty on a fresh clone).  
3. Create a Python 3 venv (or uv env); install `requests`; `python -m pip freeze`. Confirm `python --version` is 3.x.  
4. In a tiny Node folder: `npm init -y`; install one dep; show `package-lock.json` exists.  
5. Run `mvn -v` (or note missing) and locate whether `~/.m2/settings.xml` mentions Nexus. Record `java -version`.  
6. Write a 5-line lab note: which tools are OS-level vs project-level, plus one RHEL 7 `yum` command rewritten as `dnf`.
7. **Air-gap sketch (no install required):** how would you get `tree` onto a guest that cannot reach the CDN? Name the pattern (ISO / USB bag / Nexus) and the exact `dnf` flags (`--disablerepo`, `--enablerepo`, or `--cacheonly`). State that `dnf offline reboot` is **not** the answer.

## Integrity

- Don’t disable signature checks to “make install work.” `gpgcheck=0` is not an air-gap strategy.  
- Don’t commit `.npmrc` / `settings.xml` with plaintext passwords.  
- Don’t install random packages on shared servers without approval.
- Don’t install `yum-utils` / `net-tools` solely to keep RHEL 7 muscle memory. `yumdownloader` is `dnf download`.
- Don’t leave a CDN repo `enabled=1` on an air-gapped guest “just in case.” It will hang every transaction.

## Further reading

| Topic | Source |
|-------|--------|
| DNF 5 | `man dnf` · RHEL 10 *Managing software with the DNF tool* |
| DNF 5 download | `man dnf-download` · `dnf download --help` |
| DNF 5 reboot-safe offline transactions | `man dnf-offline` (not air-gap) |
| Local / ISO repo | `man yum.conf` (repo file format) · RHEL 10 install-source chapter |
| npm | [docs.npmjs.com](https://docs.npmjs.com/) |
| pip | [pip.pypa.io](https://pip.pypa.io/) |
| uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Maven | [maven.apache.org](https://maven.apache.org/guides/) · `mvn -o` |
| Nexus | [Sonatype Nexus docs](https://help.sonatype.com/repomanager3) |
| Program CI | SW module **CI/CD and GitLab** |

## Next

**TLS certificate management** — trust stores, keys, CSRs, crypto-policies, and fixing HTTPS/AMQPS failures.
