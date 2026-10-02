# SW-A08 — CI Pipeline for Your Lab Project

**Weight:** 15% · **Due:** After sw-08-jenkins-cicd · **Module:** sw-08-jenkins-cicd

## Prompt

Automate **build (+ test if present) → package** for one of your SW labs using **GitLab CI** and/or **Jenkins** (as available). Map the same stages to the program Jenkins + Nexus story.

## Deliverables

1. **Pipeline definition:** `.gitlab-ci.yml` **or** Jenkinsfile / job screenshots — stages at least: checkout/build, test (or explicit “no tests yet”), package.
2. **Green run evidence:** pipeline URL or screenshots of success.
3. **Failed run write-up:** deliberately break the build once; paste the key log lines; fix; show green again.
4. **Artifact story:** what artifact is produced (jar/war) and where it would land in **Nexus** at work vs lab.
5. **SE note:** one paragraph on pipeline status as **verification evidence** (and what it does *not* prove).

## Quality bar

- Pipeline is reproducible on a clean agent/runner.
- Failure diagnosis is specific (not “it failed”).
- No secrets committed in CI files.

## Rubric

| Dimension | Max | What we look for |
|-----------|-----|------------------|
| automation | 15 | Working multi-stage pipeline |
| diagnosis | 10 | Break/fix with log evidence |
| communication | 5 | Artifact + SE note clear |
