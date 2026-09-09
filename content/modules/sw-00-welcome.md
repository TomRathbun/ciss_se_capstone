# Software Development — Track Overview

> **Track status:** active foundation path.  
> **Program (work):** Jira (`DR-###`), Bitbucket PRs historically; **CISS ships on GitLab**.  
> **CISS lab:** **GitLab** for git (MRs) **and** CI/CD (pipelines). Plus Java, PostgreSQL, ActiveMQ, JavaFX. **No Jenkins.**  
> **Runtime:** labs use **VMs** (not Docker) for brokers, databases, and app hosts.

## Learning outcomes

After this overview you can:

- Explain how **software development** supports the CISS selection pathway  
- Distinguish **program tools** (Jira / Bitbucket / Nexus) from **CISS lab tools** (GitLab) while keeping one workflow  
- Navigate the **module path** (Git → team workflow → **Python→Java** → Java tooling → data/messaging → daemons → JavaFX → **CI/CD / GitLab**)  
- State the **hiring bar**: Python is a translation aid; **Java** is what the contract pays for  
- Relate software craft to **systems engineering** artifacts (requirements, interfaces, V&V)  

## Why this track exists

CISS needs engineers who can **build and ship** software with discipline — not only write requirements. This track develops:

| Theme | What “good” looks like |
|-------|------------------------|
| **Craft** | Clear design, readable code, sensible structure |
| **Quality** | Tests, reviews, defect thinking |
| **Delivery** | Jira DRs + review-into-`main`; **GitLab MRs + GitLab CI/CD**; Nexus for artifacts |
| **Integration** | Databases, ActiveMQ, long-running workers, desktop UIs **on lab VMs** |
| **Teamwork** | Review culture, integrity (same professionalism bar as SE) |

Software work still sits under the program’s SE cascade: vision → needs → use cases → requirements → **implementation** → verification.

## Language: Python on-ramp, Java destination

Many interns are fastest in **Python**. That is expected. This track still trains **Java programmers**, because hired work is JDBC, JMS/ActiveMQ, daemons, and JavaFX on VMs — not a new Python microservice.

| You may | You may not (after the bridge module) |
|---------|----------------------------------------|
| Think the algorithm out in Python | Turn in Python as the lab implementation |
| Keep a personal scratch notebook | Pretend `pip` is how program services deploy |
| Use the **From Python to Java** tables | Skip Java types, Maven, and `.equals` |

The bridge module sits **after Git/workflow** and **before** VS Code/Java labs. Graded Java starts there.

## Tooling map — program vs CISS lab

| Role | Program (work) | CISS course / lab |
|------|----------------|-------------------|
| Ticket | **Jira** `DR-###` | GitLab Issue / stand-in still labeled `DR-###` |
| Git host | **Bitbucket** | **GitLab** |
| Review | **Pull Request** → `main` | **Merge Request** → `main` |
| CI | **GitLab CI/CD** (`.gitlab-ci.yml` + runner) | Same — **not Jenkins**, not GitHub Actions |
| Artifacts | **Nexus** | Lab Nexus or Maven Central |
| Runtime | **VMs** (vSphere / ESXi guests, **RHEL 10.2**) | Same — **not Docker as the default**; Podman is the native container tool if you must |
| Git CLI | Same | Same |
| Java / DB / messaging / GUI | Same stack taught in later modules | Same |

### Standard change flow

```text
CISS LAB:  DR-123 → branch DR-123 → push GitLab → GitLab CI/CD pipeline → MR → main → (Nexus)
PROGRAM:   same discipline; git host may still be described as Bitbucket in old docs — CI for this course is GitLab
                 ↑ ticket → branch → green pipeline → review → main
```

## Module path (this track)

| Order | Module | You will… |
|-------|--------|-----------|
| 1 | **Working with Git** | Daily loop; **DR-###** branch names |
| 2 | **Team workflow (Jira/Bitbucket/Nexus → GitLab)** | Learn program flow; practice on GitLab MRs |
| 3 | **From Python to Java** | Translate mental models; hiring bar is Java |
| 4 | **VS Code for Java** | Run/debug Java projects |
| 5 | **PostgreSQL with Java** | JDBC, pools, JBoss DS, safe SQL |
| 6 | **AMQP with Java (ActiveMQ)** | Publish/consume JMS; factories / pooling |
| 7 | **Java Daemons** | Long-running consumers and scheduled jobs |
| 8 | **JavaFX for Desktop GUIs** | Operator/engineer desktop UIs |
| 9 | **CI/CD and GitLab** | Automated build/test/publish with `.gitlab-ci.yml`; green pipeline before merge |

## Lab prerequisites (cumulative)

| Module | Typical lab needs |
|--------|-------------------|
| Git / team workflow | Git; **GitLab** for CISS labs; know Jira+Bitbucket for program |
| Python → Java | Comfort reading Python; willingness to type Java by hand |
| Nexus | Program + lab `settings.xml` / URL from instructor when available |
| VS Code + Java | JDK (see Java versions module), VS Code, Extension Pack for Java, Maven |
| PostgreSQL | **Postgres on a lab VM** (or service endpoint the instructor provides) |
| ActiveMQ | **ActiveMQ on a lab VM** (`61616`, console often `8161`) |
| Daemons | Prior ActiveMQ + optional Postgres on the same or linked VMs |
| JavaFX | OpenJFX libs / javafx-maven-plugin (or lab template) |
| CI/CD | GitLab project with a runner (instructor); `.gitlab-ci.yml` |

Record **hostname / IP, port, username** for each service from the lab sheet — do not assume `localhost` unless your code runs on the same VM as the service.

## Relationship to other tracks

| Track | Overlap with software |
|-------|------------------------|
| **Systems Engineering** | Requirements, ICDs, RTM — software implements them; DR may fix an FR |
| **Networking** | Hosts, ports, TLS for DB and brokers |
| **SysAdmin & Integration** | Deploy workers on VMs, Nexus, env config, restarts, vSphere |
| **Military** | Domain language for mission-facing features |

## Integrity

- Your own work; cite AI for substantial generated code.  
- Never commit secrets, tokens, or classified data.  
- Same A6 professionalism standards as SE workshops.

## Further reading

| Topic | Source |
|-------|--------|
| SEBoK | [sebokwiki.org](https://sebokwiki.org/) — realization / implementation topics |
| Pro Git | [git-scm.com/book](https://git-scm.com/book/en/v2) |
| Java tutorials | [dev.java](https://dev.java/learn/) |

## Next

**Working with Git** — foundation for every later software module, including `DR-###` branches.
