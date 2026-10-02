# CI/CD and Jenkins

## Learning outcomes

After this module you can:

- Explain **CI** and **CD** in plain language and why teams use them  
- Describe a typical **pipeline**: checkout → build → test → package → publish  
- Navigate **Jenkins** concepts: job, pipeline, agent, stage, artifact  
- Relate Jenkins (program) to **GitLab CI** (CISS lab) so habits transfer  
- Read a **failed build** log and know what to fix before merging  

## Why automation matters

Manual “build on my laptop and copy the jar” does not scale and is hard to **verify**.

| Without CI/CD | With CI/CD |
|---------------|------------|
| “Works on my machine” | Same steps every time on a clean agent |
| Reviewers guess if tests ran | Pipeline status is evidence |
| Late integration surprises | Main stays buildable more often |
| Mystery jars | Versioned artifacts in **Nexus** |

SE link: a green pipeline is **verification evidence** (“we ran the automated checks”). It does not replace validation with stakeholders.

---

## CI vs CD (intro)

```text
CI  Continuous Integration
    Every push/MR/PR: build + automated tests (+ lint/scan)
    Goal: integrate small changes often; catch breaks early

CD  Continuous Delivery  and/or  Continuous Deployment
    Delivery: always *able* to release (artifact ready, approved)
    Deployment: automatically ship to an environment when checks pass
```

| Term | Meaning for interns |
|------|---------------------|
| **Continuous Integration (CI)** | Automated build + test on each change |
| **Continuous Delivery** | Pipeline produces a release-ready artifact; humans approve go-live |
| **Continuous Deployment** | Pipeline also deploys automatically (stricter culture/tooling) |

This course focuses on **CI** and “publish artifact” style **delivery**. Full production deploy policies are program-specific.

### What usually runs in a pipeline

```text
1. Checkout source (from Bitbucket / GitLab)
2. Resolve dependencies (often via Nexus)
3. Compile / package (e.g. mvn package)
4. Unit / integration tests
5. Static checks (optional: format, spotbugs, OWASP dep check)
6. Publish artifact to Nexus (on main / tag / release job)
7. Notify (chat/email) — optional
```

Not every job does every step. **Know which stages your project runs.**

---

## Two environments (same idea)

| Role | **Program (work)** | **CISS course / lab** |
|------|--------------------|------------------------|
| Git host | Bitbucket | GitLab |
| Ticket | Jira `DR-###` | Issue / stand-in `DR-###` |
| CI server | **Jenkins** | **Jenkins** and/or **GitLab CI** (instructor will say) |
| Artifacts | **Nexus** | Lab Nexus or local `target/` |
| Trigger | PR/branch push, or timed jobs | MR push, or manual “Build now” |

```text
PROGRAM:  push DR-42 branch / PR  →  Jenkins job  →  green?  →  review merge  →  (maybe) publish Nexus
CISS LAB: push DR-42 branch / MR  →  Jenkins and/or GitLab pipeline  →  green?  →  merge
```

If the lab only has GitLab pipelines first, still learn **Jenkins vocabulary** — that is what you will see at work.

---

## Jenkins concepts

```text
Jenkins controller
  └── jobs / pipelines
        └── runs on agents (executors)
              └── stages / steps
                    └── logs + artifacts + status
```

| Concept | Meaning |
|---------|---------|
| **Job / Pipeline** | Named automation (e.g. `ciss-service-ci`) |
| **Build / Run** | One execution (#42, #43, …) |
| **Agent / node** | Machine that runs the steps (JDK, Maven installed) |
| **Stage** | Logical phase: Build, Test, Publish |
| **Artifact** | Files kept from the run (jar, reports) |
| **Workspace** | Checkout directory for that run |
| **Webhook / trigger** | Bitbucket/GitLab tells Jenkins “code changed” |
| **Credentials** | Stored secrets for Nexus, Git, etc. (not in the repo) |

### Freestyle vs Pipeline

| Style | What it is |
|-------|------------|
| **Freestyle job** | Configured in Jenkins UI (older, still common) |
| **Pipeline as code** | `Jenkinsfile` in the repo — reviewable, versioned |

Prefer **Pipeline as code** for anything you maintain long-term: the same DR/PR discipline applies to Jenkinsfile changes.

### Minimal `Jenkinsfile` (declarative sketch)

```groovy
pipeline {
  agent any
  tools {
    // names must match what Jenkins admin configured
    maven 'Maven-3.9'
    jdk 'JDK-17'
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps { sh 'mvn -B -DskipTests package' }
    }
    stage('Test') {
      steps { sh 'mvn -B test' }
    }
    stage('Publish') {
      when { branch 'main' }
      steps {
        // example only — real URL/creds come from Jenkins credentials + Nexus
        sh 'mvn -B deploy -DskipTests'
      }
    }
  }
  post {
    always {
      junit '**/target/surefire-reports/*.xml'
      archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
    }
  }
}
```

Your program’s `Jenkinsfile` will differ — **read the real one** in the repo.

### Multibranch Pipeline (common with Bitbucket/GitLab)

- Jenkins discovers branches / PRs automatically  
- Branch `DR-42` gets its own build  
- PR/MR build must be **green** before merge (when policy requires it)  

---

## GitLab CI mapping (CISS lab)

If the course project uses GitLab CI, a `.gitlab-ci.yml` is the cousin of a `Jenkinsfile`:

| Jenkins | GitLab CI |
|---------|-----------|
| `Jenkinsfile` | `.gitlab-ci.yml` |
| Stage | `stage:` |
| Agent | Runner / `tags:` |
| Build # | Pipeline / job |
| Blue/green ball | Pipeline status badge |

```yaml
# Conceptual sketch — not a full production file
build:
  stage: build
  script:
    - mvn -B -DskipTests package
test:
  stage: test
  script:
    - mvn -B test
```

**Transfer sentence for interviews:**

> “We use Jenkins at work for CI; in the CISS lab we also use GitLab pipelines. Same idea: every change builds and tests before merge; artifacts can go to Nexus.”

---

## Reading a failed build (skill)

1. Open the **red** run.  
2. Find the **failed stage** (Build vs Test vs Publish).  
3. Open the **console log**; jump near the first `ERROR` / `FAILURE`.  
4. Reproduce **locally** (`mvn test`) when possible.  
5. Fix on `DR-###`, push, wait for a new run.  

| Failure type | Typical fix |
|--------------|-------------|
| Compile error | Fix code / imports |
| Test failure | Fix logic or outdated test |
| Dependency resolve | Nexus URL, credentials, VPN, version typo |
| Agent missing tool | Wrong JDK/Maven tool name — ask admin |
| Flaky test | Stabilize test; don’t merge “hope” |

Do **not** merge red “to save time” without instructor/lead approval.

---

## Quality gates (what “green” means)

Green means **automated checks configured for this job passed**. It does **not** automatically mean:

- Product is validated with ops  
- Performance is fine  
- Security review is done  
- The DR is closed  

Still required: human review, DR hygiene, and any manual test notes in the PR/MR.

---

## Drill (40–50 min)

**If Jenkins is available**

1. Open the course/program Jenkins dashboard.  
2. Find the job for your sample repo (or a demo job).  
3. Locate a recent green and red build; skim the red console for the failing step.  
4. On branch `DR-###`, make a tiny change (or fix a deliberate broken test).  
5. Push; confirm a new build starts; get to green.  
6. Write three bullets: trigger, stages you saw, where artifacts went (if any).  

**If only GitLab CI is available**

1. Open the MR pipeline for your branch.  
2. Map each GitLab job to a Jenkins **stage** name on paper.  
3. Force a failing test, push, read the log, fix, push again.  

**Offline**

1. Draw a pipeline from commit → Jenkins → Nexus.  
2. Label which steps are CI vs delivery.  
3. List five things that belong in a `Jenkinsfile` for a Java Maven service.  

---

## Integrity

- Do not put production passwords in Jenkinsfiles or Git — use **Jenkins credentials**.  
- Do not disable tests to force green without agreement.  
- No classified logs in screenshots for course submission.

## Further reading

| Topic | Source |
|-------|--------|
| Jenkins user handbook | [jenkins.io/doc](https://www.jenkins.io/doc/) |
| Declarative pipeline | [Jenkins — Pipeline syntax](https://www.jenkins.io/doc/book/pipeline/syntax/) |
| GitLab CI | [GitLab CI/CD](https://docs.gitlab.com/ee/ci/) |
| CI concept | Fowler, “Continuous Integration” (classic essay — search title) |
| Nexus | Course **Team Workflow** module + [Sonatype Nexus docs](https://help.sonatype.com/repomanager3) |

## Next

Return to **Software Development — Track Overview**, or apply CI habits on every later lab: push `DR-###`, wait for green, then request review.
