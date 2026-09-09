# Package Management Systems

## Learning outcomes

After this module you can:

- Choose the right **package manager** for OS vs language ecosystems  
- Use **DNF 5** (RHEL 10.2) and **RPM** to query/install/update packages safely  
- Translate leftover **yum** habits from RHEL 7 runbooks  
- Use **npm**, **pip** / **uv**, and **Maven** for app dependencies  
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
              CI (Jenkins) publish
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

Coordinate with **Jenkins** (SW track CI module): CI often publishes; apps consume.

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

## Integrity

- Don’t disable signature checks to “make install work.”  
- Don’t commit `.npmrc` / `settings.xml` with plaintext passwords.  
- Don’t install random packages on shared servers without approval.
- Don’t install `yum-utils` / `net-tools` solely to keep RHEL 7 muscle memory.

## Further reading

| Topic | Source |
|-------|--------|
| DNF 5 | `man dnf` · RHEL 10 system admin docs |
| npm | [docs.npmjs.com](https://docs.npmjs.com/) |
| pip | [pip.pypa.io](https://pip.pypa.io/) |
| uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Maven | [maven.apache.org](https://maven.apache.org/guides/) |
| Nexus | [Sonatype Nexus docs](https://help.sonatype.com/repomanager3) |
| Program CI | SW module **CI/CD and Jenkins** |

## Next

**TLS certificate management** — trust stores, keys, CSRs, crypto-policies, and fixing HTTPS/AMQPS failures.
