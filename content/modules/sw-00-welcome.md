# Software Development — Track Overview

> **Track status:** active foundation path.  
> **Program (work):** Jira (`DR-###`), Bitbucket PRs, **Jenkins** CI, Nexus.  
> **CISS lab:** same habits on **GitLab** (MRs + pipelines) and/or lab Jenkins. Plus Java, PostgreSQL, ActiveMQ, JavaFX.  
> **Runtime:** labs use **VMs** (not Docker) for brokers, databases, and app hosts.

## Learning outcomes

After this overview you can:

- Explain how **software development** supports the CISS selection pathway  
- Distinguish **program tools** (Jira / Bitbucket / Nexus) from **CISS lab tools** (GitLab) while keeping one workflow  
- Navigate the **module path** (Git → team workflow → Java tooling → data/messaging → daemons → JavaFX → **CI/CD/Jenkins**)  
- Relate software craft to **systems engineering** artifacts (requirements, interfaces, V&V)  

## Why this track exists

CISS needs engineers who can **build and ship** software with discipline — not only write requirements. This track develops:

| Theme | What “good” looks like |
|-------|------------------------|
| **Craft** | Clear design, readable code, sensible structure |
| **Quality** | Tests, reviews, defect thinking |
| **Delivery** | Jira DRs + Bitbucket PRs + **Jenkins** at work; **GitLab MRs/CI** in CISS lab; Nexus for artifacts |
| **Integration** | Databases, ActiveMQ, long-running workers, desktop UIs **on lab VMs** |
| **Teamwork** | Review culture, integrity (same professionalism bar as SE) |

Software work still sits under the program’s SE cascade: vision → needs → use cases → requirements → **implementation** → verification.

## Tooling map — program vs CISS lab

| Role | Program (work) | CISS course / lab |
|------|----------------|-------------------|
| Ticket | **Jira** `DR-###` | GitLab Issue / stand-in still labeled `DR-###` |
| Git host | **Bitbucket** | **GitLab** |
| Review | **Pull Request** → `main` | **Merge Request** → `main` |
| CI | **Jenkins** | GitLab CI and/or lab **Jenkins** |
| Artifacts | **Nexus** | Lab Nexus or Maven Central |
| Runtime | **VMs** (vSphere / ESXi guests, RHEL-class) | Same — **not Docker as the default** |
| Git CLI | Same | Same |
| Java / DB / messaging / GUI | Same stack taught in later modules | Same |

### Standard change flow

```text
PROGRAM:  Jira DR-123 → branch DR-123 → push Bitbucket → Jenkins CI → PR → main → Nexus
CISS LAB: DR-123 → branch DR-123 → push GitLab → pipeline (GitLab CI / Jenkins) → MR → main
                 ↑ same discipline, different host / button names
```

## Module path (this track)

| Order | Module | You will… |
|-------|--------|-----------|
| 1 | **Working with Git** | Daily loop; **DR-###** branch names |
| 2 | **Team workflow (Jira/Bitbucket/Nexus → GitLab)** | Learn program flow; practice on GitLab MRs |
| 3 | **VS Code for Java** | Run/debug Java projects |
| 4 | **PostgreSQL with Java** | JDBC, pools, JBoss DS, safe SQL |
| 5 | **AMQP with Java (ActiveMQ)** | Publish/consume JMS; factories / pooling |
| 6 | **Java Daemons** | Long-running consumers and scheduled jobs |
| 7 | **JavaFX for Desktop GUIs** | Operator/engineer desktop UIs |
| 8 | **CI/CD and Jenkins** | Automated build/test/publish; map to GitLab CI |

## Lab prerequisites (cumulative)

| Module | Typical lab needs |
|--------|-------------------|
| Git / team workflow | Git; **GitLab** for CISS labs; know Jira+Bitbucket for program |
| Nexus | Program + lab `settings.xml` / URL from instructor when available |
| VS Code + Java | JDK (see Java versions module), VS Code, Extension Pack for Java, Maven |
| PostgreSQL | **Postgres on a lab VM** (or service endpoint the instructor provides) |
| ActiveMQ | **ActiveMQ on a lab VM** (`61616`, console often `8161`) |
| Daemons | Prior ActiveMQ + optional Postgres on the same or linked VMs |
| JavaFX | OpenJFX libs / javafx-maven-plugin (or lab template) |
| CI/CD | Access to Jenkins and/or GitLab pipelines (instructor) |

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
