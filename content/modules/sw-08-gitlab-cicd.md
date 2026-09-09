# CI/CD and GitLab

## Learning outcomes

After this module you can:

- Explain **CI** and **CD** in plain language and why teams use them  
- Describe a typical **pipeline**: checkout → build → test → package → publish  
- Author a **`.gitlab-ci.yml`**: stages, jobs, `script`, `rules`, `artifacts`, variables  
- Use a **GitLab Runner** (shell executor on a RHEL 10.2 lab VM; not Docker-as-default)  
- Read a **failed pipeline** job log and fix it on `DR-###` before merge  
- Publish a jar to **Nexus** from CI without putting passwords in Git  

This course does **not** use Jenkins. Do not write a `Jenkinsfile`. Do not open a Jenkins dashboard for evidence.

## Why automation matters

Manual “build on my laptop and copy the jar” does not scale and is hard to **verify**.

| Without CI/CD | With CI/CD |
|---------------|------------|
| “Works on my machine” | Same steps every time on a clean runner |
| Reviewers guess if tests ran | Pipeline status is evidence |
| Late integration surprises | `main` stays buildable more often |
| Mystery jars | Versioned artifacts in **Nexus** |

SE link: a green pipeline is **verification evidence** (“we ran the automated checks”). It does not replace validation with stakeholders.

---

## Names: “Actions” vs GitLab CI/CD

Interns who used GitHub say **“GitLab Actions.”** GitLab’s product is **GitLab CI/CD**. Use GitLab names in tickets and interviews.

| GitHub Actions (do not write this here) | GitLab CI/CD (course standard) |
|-----------------------------------------|--------------------------------|
| `.github/workflows/*.yml` | **`.gitlab-ci.yml`** at the repo root |
| Workflow | **Pipeline** |
| Job / step | **Job** (`script:` is the steps) |
| `runs-on:` | **Runner** (`tags:` or the project’s default runner) |
| Marketplace Action | **CI/CD component** / `include:` (optional; not required this lab) |

If you paste a GitHub Actions file into a GitLab project, the pipeline will not run.

---

## CI vs CD (intro)

```text
CI  Continuous Integration
    Every push / MR: build + automated tests (+ lint/scan)
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
1. Checkout source (GitLab does this before your script)
2. Resolve dependencies (Nexus — air-gapped labs never hit Maven Central)
3. Compile / package (mvn -B package)
4. Unit / integration tests
5. Static checks (optional: format, spotbugs)
6. Publish artifact to Nexus (on main / tag, not on every DR branch)
7. Notify — optional
```

Not every job does every step. **Know which stages your project runs.**

---

## Lab environment

| Role | CISS course / lab |
|------|-------------------|
| Git host | **GitLab** |
| Ticket | Issue / stand-in `DR-###` |
| CI | **GitLab CI/CD** — `.gitlab-ci.yml` + **GitLab Runner** |
| Artifacts | Lab **Nexus** or `target/` on the runner |
| Trigger | Push to `DR-###`, MR pipeline, or **Run pipeline** |
| Runtime for the *app* | RHEL 10.2 **VM** (not Docker as the default) |
| Runtime for the *job* | **Shell executor** on a RHEL 10.2 runner VM (JDK 21 / Maven from the golden image or Nexus). Docker executor only if the instructor says so and the image is on the internal registry. |

```text
push DR-42 branch / open MR  →  GitLab pipeline  →  green?  →  review merge  →  (maybe) publish Nexus
```

Air-gap reminder (admin-03): the runner cannot reach `repo.maven.apache.org` or `hub.docker.com`. Point Maven at Nexus. Do not `image: maven:3.9` from Docker Hub on an air-gapped guest.

---

## GitLab CI/CD concepts

```text
GitLab project
  └── .gitlab-ci.yml
        └── pipeline (one run per push / MR / schedule)
              └── stages (ordered)
                    └── jobs (parallel inside a stage, unless needs:)
                          └── runner executes script:
```

| Concept | Meaning |
|---------|---------|
| **`.gitlab-ci.yml`** | Pipeline as code. Commit it. Review it on the MR like any other file. |
| **Pipeline** | One execution of the file (push #, MR pipeline, scheduled). |
| **Stage** | Ordered group: `build`, `test`, `package`. A stage starts when the previous stage’s jobs succeeded. |
| **Job** | Named unit with a `script:` list. Failure of a required job fails the pipeline. |
| **Runner** | Process that picks up jobs (`gitlab-runner`). Lab: shell executor on RHEL 10.2. |
| **`tags:`** | Selects which runner may take the job (e.g. `rhel10`, `maven`). |
| **Artifact** | Files kept after the job (`paths:`) for download or later jobs. |
| **Cache** | Optional speed-up (`~/.m2/repository`). Not a substitute for Nexus. |
| **CI/CD variable** | Project/group/runtime secret or setting. **Masked.** Not in the YAML. |
| **`rules:`** | When this job runs (MR vs `main` vs schedule). |

### Minimal `.gitlab-ci.yml` (Maven on a shell runner)

```yaml
# .gitlab-ci.yml — CISS lab sketch (shell executor, RHEL 10.2, JDK 21)
stages:
  - build
  - test
  - package

variables:
  MAVEN_OPTS: "-Dhttps.protocols=TLSv1.2"

default:
  tags:
    - rhel10
    - maven

build:
  stage: build
  script:
    - java -version
    - mvn -B -DskipTests package
  artifacts:
    paths:
      - target/*.jar
    expire_in: 1 week

test:
  stage: test
  script:
    - mvn -B test
  artifacts:
    when: always
    reports:
      junit: target/surefire-reports/TEST-*.xml

package:
  stage: package
  script:
    - mvn -B -DskipTests deploy
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

| YAML / flag | Meaning |
|-------------|---------|
| `stages:` | Order of work. Jobs without a stage go to `test`. |
| `default: tags:` | Every job uses these runner tags unless it overrides. |
| `script:` | Shell lines. Stop on first non-zero exit (`set -e` equivalent). |
| `mvn -B` | **B**atch — no interactive prompts (required in CI). |
| `-DskipTests` | Compile/package without running tests (tests have their own job). |
| `artifacts: paths:` | Keep these files after the job (jars for download / next stage). |
| `expire_in:` | How long GitLab keeps the artifact. |
| `when: always` | Keep JUnit reports even if tests failed. |
| `reports: junit:` | GitLab MR test widget. |
| `rules: if:` | Run `package` only on the default branch (`main`), not on every `DR-###`. |
| `$CI_COMMIT_BRANCH` | Predefined variable — the branch that triggered the pipeline. |
| `$CI_DEFAULT_BRANCH` | Usually `main`. |

Your project file will differ — **read the one in the repo** and change it on a `DR-###` branch.

Do **not** put Nexus passwords in this file. Store them as **masked CI/CD variables** (`NEXUS_USER`, `NEXUS_PASSWORD`) and reference `$NEXUS_USER` in `~/.m2/settings.xml` on the runner, or a `settings.xml` generated in `before_script` from those variables.

### Merge-request pipelines

```yaml
test:
  stage: test
  script:
    - mvn -B test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH
```

| Value | Meaning |
|-------|---------|
| `merge_request_event` | Pipeline attached to the MR (the one reviewers see) |
| `$CI_COMMIT_BRANCH` | Also run on branch pushes |

Policy: **MR pipeline green before merge.** Same habit as “don’t merge red.”

---

## Runners on RHEL 10.2 (admin overlap)

The GitLab **server** schedules; a **runner** does the work. In this lab the runner is usually a RHEL 10.2 VM with `gitlab-runner` and a **shell** executor — it runs `script:` as the `gitlab-runner` user, using the JDK/Maven already on the golden image.

```bash
# awareness — do not register a runner without instructor approval
sudo systemctl status gitlab-runner
sudo gitlab-runner list
java -version          # expect 21 (or JAVA_HOME to the documented alternative)
mvn -v
```

| Executor | When |
|----------|------|
| **shell** | Course default. Uses the VM’s JDK/Maven. Air-gap friendly. |
| **docker** | Only if the instructor provides an **internal** image (Nexus/Harbor). Do not pull `maven:3.9` from the internet. |

Tie-in: admin-03 air-gap — the runner’s `dnf` and Maven both point at **Nexus**, not CDN / Maven Central.

---

## Reading a failed pipeline (skill)

1. Open the MR → **Pipelines** → the red pipeline.  
2. Click the **failed job** (not just the pipeline badge).  
3. Jump near the first `ERROR` / `FAILURE` / non-zero exit.  
4. Reproduce **locally** (`mvn -B test`) when possible.  
5. Fix on `DR-###`, push, wait for a new pipeline.  

| Failure type | Typical fix |
|--------------|-------------|
| Compile error | Fix code / imports |
| Test failure | Fix logic or outdated test |
| Dependency resolve | Nexus URL, CI variable, `settings.xml` on the runner, version typo |
| `image:` pull fail | Air-gap — drop Docker Hub; use the shell runner |
| Runner stuck `pending` | No runner with those `tags:` — ask admin |
| `yaml invalid` | Indentation / unknown keyword — GitLab CI linter in the project |

Do **not** merge red “to save time” without instructor/lead approval.

---

## Quality gates (what “green” means)

Green means **automated checks in `.gitlab-ci.yml` passed**. It does **not** automatically mean:

- Product is validated with ops  
- Performance is fine  
- Security review is done  
- The DR is closed  

Still required: human review, DR hygiene, and any manual test notes in the MR.

---

## Drill (40–50 min)

On the **CISS GitLab** project:

1. Open **CI/CD → Editor** (or the `.gitlab-ci.yml` in the repo). Confirm it is GitLab YAML, not a `Jenkinsfile` and not `.github/workflows`.  
2. Open a recent **green** and **red** pipeline; skim the red **job** log for the failing step.  
3. On branch `DR-###`, add or fix a job (or deliberately break a test).  
4. Push; confirm a new pipeline starts on the MR; get to green.  
5. Write three bullets: trigger, stages you saw, where artifacts went (job artifacts and/or Nexus).  
6. One sentence: why `image: maven:3.9` from Docker Hub is the wrong default on an air-gapped RHEL 10.2 runner.

**Offline (no GitLab UI):**

1. Draw commit → GitLab pipeline → Nexus.  
2. Label which steps are CI vs delivery.  
3. List five keys that belong in `.gitlab-ci.yml` for a Java Maven service (`stages`, `script`, `artifacts`, `rules`, `tags` or `default`).

---

## Integrity

- Do not put production passwords in `.gitlab-ci.yml` — use **masked CI/CD variables**.  
- Do not disable tests to force green without agreement.  
- No classified logs in screenshots for course submission.  
- Do not install Jenkins “so it matches an old blog.” Course CI is GitLab.

## Further reading

| Topic | Source |
|-------|--------|
| GitLab CI/CD | [docs.gitlab.com/ci](https://docs.gitlab.com/ci/) |
| `.gitlab-ci.yml` keyword reference | [docs.gitlab.com/ci/yaml](https://docs.gitlab.com/ci/yaml/) |
| GitLab Runner | [docs.gitlab.com/runner](https://docs.gitlab.com/runner/) |
| CI concept | Fowler, “Continuous Integration” (classic essay — search title) |
| Nexus | Course **Team Workflow** module + [Sonatype Nexus docs](https://help.sonatype.com/repomanager3) |
| Air-gapped DNF / Maven | Course **Package Management** (admin-03) |

## Next

Return to **Software Development — Track Overview**, or apply CI habits on every later lab: push `DR-###`, wait for **green GitLab pipeline**, then request review.
