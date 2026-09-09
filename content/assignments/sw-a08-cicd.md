# SW-A08 — CI Pipeline for Your Lab Project

**Weight:** 15% · **Due:** After sw-08-gitlab-cicd · **Module:** sw-08-gitlab-cicd

## Prompt

Automate **build (+ test if present) → package** for one of your SW labs using **GitLab CI/CD**. Course CI is GitLab. Do not submit a `Jenkinsfile` or a GitHub Actions workflow.

## Deliverables

1. **Pipeline definition:** `.gitlab-ci.yml` in the repo — stages at least: build, test (or explicit “no tests yet”), package. Jobs use a **shell runner** tag (or the instructor’s documented executor). No `image:` pulled from Docker Hub unless the instructor says the lab is not air-gapped.
2. **Green run evidence:** GitLab pipeline URL or screenshots of success on an MR.
3. **Failed run write-up:** deliberately break the build once; paste the key **job** log lines; fix; show green again.
4. **Artifact story:** what artifact is produced (jar/war) and where it would land in **Nexus**. Name the CI/CD variables you would use for Nexus credentials (do not put real passwords in the YAML).
5. **SE note:** one paragraph on pipeline status as **verification evidence** (and what it does *not* prove).
6. **Naming note:** one sentence distinguishing GitHub Actions from GitLab CI/CD (pipeline / job / runner).

## Quality bar

- Pipeline is reproducible on a clean GitLab Runner.
- Failure diagnosis is specific (not “it failed”).
- No secrets committed in `.gitlab-ci.yml`.
- No Jenkins / GitHub Actions file as the primary evidence.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| automation | 15 | Working multi-stage `.gitlab-ci.yml` |
| diagnosis | 10 | Break/fix with job-log evidence |
| communication | 5 | Artifact + SE note + GitLab vs Actions naming |
