# Team Workflow: Jira, Bitbucket, Nexus — and GitLab (CISS Lab)

## Learning outcomes

After this module you can:

- Describe the **program work environment** workflow: Jira DR → Bitbucket branch → PR → merge → Nexus  
- Map every step to the **CISS course environment**, which uses **GitLab**  
- Use the same discipline on either host: **ticket key → branch name → review → merge to `main`**  
- Open a **GitLab merge request** that would be a **Bitbucket pull request** at work  
- Explain where **Nexus** fits for Maven artifacts  

## Two environments, one workflow

You will **learn what the program does**, then **practice the same habits** on CISS tooling.

| Role | **Program (work)** | **CISS course / lab** |
|------|--------------------|------------------------|
| Work item / ticket | **Jira** Deficiency Report (`DR-###`) | GitLab **Issue** (or paper/stand-in ticket with same `DR-###` key) |
| Git remote host | **Bitbucket** | **GitLab** |
| Review + integrate | Bitbucket **Pull Request (PR)** → `main` | GitLab **Merge Request (MR)** → `main` |
| Artifacts / deps | **Nexus** | Nexus if provided, or Maven Central / lab mirror |
| Git commands | Same (`clone`, `branch`, `commit`, `push`) | Same |

```text
SAME DISCIPLINE                          DIFFERENT UI / HOST
─────────────────                        ──────────────────
1. Open ticket (DR-123)          →       Jira (work)  |  GitLab Issue / stand-in (CISS)
2. Branch named DR-123           →       Bitbucket    |  GitLab
3. Commit + push                 →       git (identical)
4. Request review into main      →       Pull Request |  Merge Request
5. Review, CI, merge             →       Bitbucket UI |  GitLab UI
6. Consume / publish jars        →       Nexus        |  lab Nexus or Central
```

**Key idea:** employers care that you follow **ticket → branch → review → main**. CISS uses **GitLab** so the class has one shared lab host; the **names** change, the **habits** do not.

---

## Part A — Program environment (what we do at work)

### A1. Jira — Deficiency Reports (DR)

A **Deficiency Report** tracks something to fix, finish, or verify:

```text
DR-42
DR-108
DR-1003
```

| Do | Don’t |
|----|--------|
| One clear change per DR when practical | Vague titles (“misc fixes”) |
| Put `DR-###` on branch, commits, and PR | Work with no ticket (unless lead says so) |
| Update Jira when PR opens / merges | Leave DR open with no evidence |
| Link to FR / requirement when known | Paste secrets into Jira |

SE link:

```text
DR-42  →  may implement or fix  FR-CI-02
```

### A2. Bitbucket — branch and pull request

```bash
git checkout main
git pull origin main
git checkout -b DR-42
# optional: DR-42-double-checkin

# … work …
git add -A
git commit -m "DR-42 Reject double check-in when already checked in"
git push -u origin DR-42
```

In **Bitbucket** UI:

1. Create **Pull Request**  
2. Source `DR-42` → destination **`main`**  
3. Title starts with `DR-42`  
4. Reviewers, CI if any, merge per team policy  

`main` is usually **protected** — no direct push.

### A3. Nexus — artifacts

**Nexus** holds Maven/Gradle dependencies and (often) jars your CI publishes.

```text
Build  →  resolve deps from Nexus  →  (optional) deploy artifact back to Nexus
```

Program builds typically point `settings.xml` / `pom.xml` at the org Nexus URL. Never commit Nexus passwords.

---

## Part B — CISS lab environment (GitLab translation)

On the **CISS Capstone** course host you practice with **GitLab**. Translate each program step as follows.

### Translation table (memorize)

| Program term | CISS GitLab term | You still… |
|--------------|------------------|------------|
| Jira **DR-42** | GitLab **Issue** titled/linked as `DR-42`, or instructor-issued `DR-42` | Start from a ticket key |
| Bitbucket **repository** | GitLab **project** | `git clone` / `git remote` |
| Bitbucket **branch** `DR-42` | GitLab **branch** `DR-42` | Same branch name |
| Bitbucket **Pull Request** | GitLab **Merge Request (MR)** | Request review into `main` |
| Bitbucket **approve / merge** | GitLab **approve / merge** | Human review before integrate |
| Pipeline on PR | Pipeline on MR (`.gitlab-ci.yml`) and/or **Jenkins** | Fix red pipelines before merge |
| **Jenkins** (program CI) | Lab Jenkins and/or GitLab CI | Same idea: automated build/test |
| Nexus | Lab Nexus **or** public Central via lab mirror | Resolve deps; no secrets in Git |

### B1. Clone the CISS GitLab project

```bash
git clone git@gitlab.ciss-lab.example:group/ciss-capstone-demo.git
cd ciss-capstone-demo
git remote -v    # origin → GitLab
```

Use the real GitLab URL from your instructor.

### B2. Same branch discipline

```bash
git checkout main
git pull origin main
git checkout -b DR-42
git commit -m "DR-42 Reject double check-in when already checked in"
git push -u origin DR-42
```

Branch naming stays **`DR-###`** so habits transfer 1:1 to Bitbucket.

### B3. Open a Merge Request (this is the PR)

In **GitLab** UI after push:

1. **Create merge request** (banner often appears after push)  
2. Source: `DR-42` → Target: **`main`**  
3. Title: `DR-42 …`  
4. Description (same content as a work PR):

```markdown
## Ticket
DR-42
(Program equivalent: Jira Deficiency Report DR-42 → Bitbucket PR)

## Summary
What problem does this solve?

## Requirements (if known)
- FR-…

## How to test
1. …
2. …

## Risk / notes
- Config? Migration? Breaking API?
```

5. Assign reviewers → wait for CI → address comments → **Merge**.

### B4. If Jira is not available in class

| Option | How |
|--------|-----|
| GitLab Issue | Create issue titled `DR-42: …` and mention it in the MR |
| Instructor list | Use assigned DR numbers for the lab |
| Paper stand-in | Still use branch/commit/MR text `DR-42` so the habit sticks |

You are training the **program pattern**, not inventing a different process.

### B5. Nexus in the lab

| Situation | What to do |
|-----------|------------|
| Lab provides Nexus URL | Configure Maven `settings.xml` as instructed |
| No Nexus yet | Use Central; still learn *what* Nexus will replace |
| “Could not resolve artifact” | Wrong URL, auth, VPN, or offline — same debugging skills as at work |

---

## Side-by-side: one change, both worlds

```text
PROGRAM                              CISS LAB (GitLab)
───────                              ─────────────────
Jira: open DR-42                     Issue or stand-in: DR-42
git checkout -b DR-42                git checkout -b DR-42
git push origin DR-42                git push origin DR-42
Bitbucket: Pull Request → main       GitLab: Merge Request → main
Merge after review                   Merge after review
Nexus serves / stores jars           Lab Nexus or Central
```

Only the **website** and some button labels change. Interview answer:

> “At work we use Jira DRs and Bitbucket PRs; in the CISS lab we use GitLab MRs with the same DR branch naming and review-into-main discipline.”

---

## Review checklist (either host)

**Author**

- [ ] Branch = `DR-###`  
- [ ] Commits and PR/MR title cite `DR-###`  
- [ ] Description explains test steps  
- [ ] No secrets; builds locally  

**Reviewer**

- [ ] Matches the ticket intent  
- [ ] Edge cases / errors considered  
- [ ] Feedback is professional (A6)  

---

## Drill (35–45 min) — do it on GitLab

1. Obtain ticket key **DR-101** (Jira if available, else GitLab issue / instructor).  
2. On the **CISS GitLab** project: branch `DR-101` from `main`.  
3. Tiny change; commit message includes `DR-101`; push.  
4. Open a **Merge Request** to `main` using the description template (include the “Program equivalent” line once).  
5. In discussion or lab notes, write one sentence mapping your MR to a **Bitbucket PR** for the same DR.  
6. Optional: resolve a dependency and note whether it came from Nexus or Central.  

Offline fallback: write branch name, commit message, and full MR/PR body locally; still use `DR-###` everywhere.

---

## Integrity

- Do not bypass required review without instructor approval.  
- Do not push classified data to course GitLab.  
- Same AI citation rules as SE modules.

## Further reading

| Topic | Source |
|-------|--------|
| GitLab merge requests | [GitLab Docs — Merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/) |
| GitLab basics | [GitLab — Get started](https://docs.gitlab.com/ee/tutorials/gitlab_basics/) |
| Bitbucket pull requests | [Bitbucket — Pull requests](https://support.atlassian.com/bitbucket-cloud/docs/pull-requests/) |
| Jira basics | [Jira Software get started](https://www.atlassian.com/software/jira/guides/getting-started/basics) |
| Nexus Repository | [Sonatype Nexus docs](https://help.sonatype.com/repomanager3) |
| Git foundation | Course **Working with Git** |

## Next

**VS Code for Java Development** — implement on `DR-###` branches; push to **GitLab** for CISS labs (same flow as Bitbucket at work). Later: **CI/CD and Jenkins** for automated build/test on those branches.
