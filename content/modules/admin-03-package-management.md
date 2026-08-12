# Package Management Systems

## Learning outcomes

After this module you can:

- Choose the right **package manager** for OS vs language ecosystems  
- Use **YUM** (RHEL 7) to query/install/update packages safely  
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

| Manager | Ecosystem | Typical on RHEL lab |
|---------|-----------|---------------------|
| **yum** / **rpm** | OS packages (RHEL 7) | `yum install …` |
| **dnf** | OS packages (RHEL 8+) | Know the name; same job as yum |
| **npm** | Node.js / JavaScript | Front-end / tools |
| **pip** | Python | Scripts, CLIs, services |
| **uv** | Python (modern, fast) | Preferred new Python workflows |
| **Maven** / **Gradle** | Java | App deps + build (SW track) |
| **Nexus** | Org-wide artifact proxy/host | Mirrors all of the above often |

```text
Language app deps          OS packages
      │                        │
  npm / pip / uv / Maven      yum / rpm
      │                        │
      └────────►  Nexus  ◄─────┘
                   ▲
              CI (Jenkins) publish
```

---

## YUM / RPM (RHEL 7)

**RPM** = package file format. **YUM** = dependency resolver + repo client.

### Query

```bash
rpm -q bash
rpm -ql bash | head          # files owned by package
rpm -qf $(which sshd)        # which package owns this file?
yum list installed | head
yum info httpd
yum search nmap
```

### Install / update / remove (privileged)

```bash
sudo yum install -y tree
sudo yum update -y <package>
sudo yum remove -y tree
sudo yum clean all
```

| Habit | Why |
|-------|-----|
| Read `yum info` before install | Size, repo, version |
| Prefer distro packages for system tools | Supported, patched |
| Don’t disable GPG checks | Supply-chain safety |
| Record what you installed | Lab notes / DR description |

### Repos

```bash
yum repolist
ls /etc/yum.repos.d/
```

Program hosts may point at **internal mirrors / Nexus raw or yum repos**. If `yum` fails, check repo URLs and subscription/mirror access — same class of problem as Maven + Nexus.

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

### pip + venv (classic)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install requests
pip freeze > requirements.txt
```

```bash
pip install -r requirements.txt
deactivate
```

Never `sudo pip install` into system Python on shared hosts unless policy says so.

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
| Install `tree`, `git`, `httpd` on RHEL 7 | **yum** |
| Add a JS charting library to a UI | **npm** in that project |
| Run a Python health-check script | **venv + pip** or **uv** |
| Build a Java service | **Maven/Gradle** (+ Nexus) |
| Share an internal Java library | Publish to **Nexus** hosted repo |
| Patch OpenSSL on the OS | **yum** (not pip) |

---

## Drill (40 min)

1. On RHEL 7 lab: `yum info` a package; show whether it is installed (`rpm -q`).  
2. Create a Python venv (or uv env); install `requests`; `pip freeze`.  
3. In a tiny Node folder: `npm init -y`; install one dep; show `package-lock.json` exists.  
4. Run `mvn -v` (or note missing) and locate whether `~/.m2/settings.xml` mentions Nexus.  
5. Write a 5-line lab note: which tools are OS-level vs project-level.  

## Integrity

- Don’t disable signature checks to “make install work.”  
- Don’t commit `.npmrc` / `settings.xml` with plaintext passwords.  
- Don’t install random packages on shared servers without approval.

## Further reading

| Topic | Source |
|-------|--------|
| YUM | `man yum` · RHEL 7 system admin docs |
| npm | [docs.npmjs.com](https://docs.npmjs.com/) |
| pip | [pip.pypa.io](https://pip.pypa.io/) |
| uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Maven | [maven.apache.org](https://maven.apache.org/guides/) |
| Nexus | [Sonatype Nexus docs](https://help.sonatype.com/repomanager3) |
| Program CI | SW module **CI/CD and Jenkins** |

## Next

**TLS certificate management** — trust stores, keys, CSRs, and fixing HTTPS/AMQPS failures.
